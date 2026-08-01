"""Generate MODEL-001 simulation samples with the production game engine."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import random
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Callable

from engine.action import Action, ActionType
from engine.config import EngineConfig
from engine.hand_utils import melds_from_raw, tiles_to_counts
from engine.orchestrator import PlayerGameRunner
from engine.physical_tile import physical_tile
from engine.tile import Suit
from engine.win_check import WinForm, can_form_all_koutsu, is_winning_hand
from players.base_player import BasePlayer
from protocols.messages import ActionRequest, Decision

FEATURE_SCHEMA_VERSION = "MODEL001-FEATURE-SCHEMA 1.0.0"
LABEL_SCHEMA_VERSION = "MODEL001-LABEL-SCHEMA 1.0.0"
GENERATOR_VERSION = "model001-sim-v1"
STYLE_VERSION = "1.0.0"
ALLOWED_STYLES = ("conservative", "balanced", "aggressive", "legal-random")
FORBIDDEN_FEATURE_KEYS = {
    "opponent_hidden_hand", "wall_order", "oracle", "truth", "label",
    "future_event", "other_seat_private_memory", "raw_seed",
}


def _canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def stable_split(game_id: str) -> str:
    bucket = int.from_bytes(hashlib.sha256(game_id.encode("utf-8")).digest(), "big") % 100
    return "train" if bucket < 70 else "validation" if bucket < 85 else "test"


class ProgrammaticStylePlayer(BasePlayer):
    """Small PlayerView-only policy; it never receives GameState or model artifacts."""

    def __init__(self, style_id: str, *, seed: int, on_decision: Callable[[int, Any, ActionRequest], None]):
        if style_id not in ALLOWED_STYLES:
            raise ValueError(f"unknown style: {style_id}")
        super().__init__(name=f"model001-{style_id}", player_id=f"model001-{style_id}", seed=seed)
        self.style_id = style_id
        self.style_version = STYLE_VERSION
        self._on_decision = on_decision

    def on_join(self, seat: int, config: dict) -> None:
        self.seat = seat
        self.config = dict(config)

    def decide(self, request: ActionRequest) -> Decision:
        if not self.last_observation:
            raise RuntimeError("decision without PlayerView")
        self._on_decision(request.seat, self.last_observation, request)
        legal = list(request.legal_actions)
        if not legal:
            raise RuntimeError("no legal actions")
        hu = next((a for a in legal if a.type == ActionType.HU), None)
        if hu is not None:  # Chengdu mandatory-win safety for every style.
            choice = hu
        elif self.style_id == "legal-random":
            choice = self.rng.choice(legal)
        else:
            choice = self._ranked_choice(legal)
        return Decision(request.request_id, choice, f"model001:{self.style_id}:{choice.type.value}")

    def _ranked_choice(self, legal: list[Action]) -> Action:
        if self.style_id == "conservative":
            order = (ActionType.PASS, ActionType.DISCARD, ActionType.PONG, ActionType.GANG_MING, ActionType.GANG_AN, ActionType.GANG_JIA)
        elif self.style_id == "aggressive":
            order = (ActionType.GANG_AN, ActionType.GANG_JIA, ActionType.GANG_MING, ActionType.PONG, ActionType.DISCARD, ActionType.PASS)
        else:
            order = (ActionType.GANG_AN, ActionType.GANG_JIA, ActionType.PONG, ActionType.DISCARD, ActionType.PASS, ActionType.GANG_MING)
        for typ in order:
            candidates = [a for a in legal if a.type == typ]
            if candidates:
                return self.rng.choice(candidates)
        return self.rng.choice(legal)


class SampleCollector:
    def __init__(self, game_id: str, styles: list[str], state_getter: Callable[[], Any]):
        self.game_id = game_id
        self.styles = styles
        self.state_getter = state_getter
        self.pending: list[tuple[dict, dict]] = []
        self.decision_index = 0

    def capture(self, observer_seat: int, observation: Any, request: ActionRequest) -> None:
        state = self.state_getter()
        if state is None:
            raise RuntimeError("missing authoritative state")
        self.decision_index += 1
        decision_id = f"d{self.decision_index:06d}"
        view = copy.deepcopy(observation.view)
        for opponent in state.players:
            if opponent.seat == observer_seat or opponent.status != "active":
                continue
            sample_id = f"{self.game_id}:{decision_id}:{observer_seat}:{opponent.seat}"
            feature = {
                "sample_id": sample_id, "game_id": self.game_id, "decision_id": decision_id,
                "observer_seat": observer_seat, "opponent_seat": opponent.seat,
                "style_id": self.styles[opponent.seat], "style_version": STYLE_VERSION,
                "split": stable_split(self.game_id), "policy_features": view,
            }
            label = {"sample_id": sample_id, **current_labels(opponent), "shape": None, "label_source": "SIMULATOR_TRUTH"}
            self.pending.append((feature, label))

    def finalize(self, state: Any) -> list[tuple[dict, dict]]:
        shapes = {p.seat: terminal_shape(state, p) for p in state.players}
        for feature, label in self.pending:
            label["shape"] = shapes[feature["opponent_seat"]]
        return self.pending


def _meld_tiles(player: Any) -> list[Any]:
    return [meld.face for meld in player.melds for _ in range(len(meld.tile_ids))]


def current_labels(player: Any) -> dict[str, Any]:
    concealed = [tile.face for tile in player.hand]
    cleared = int(player.dingque is not None and all(tile.suit != player.dingque for tile in concealed))
    counts = Counter(tile.suit for tile in concealed + _meld_tiles(player))
    values = {s: counts[s] for s in Suit}
    maximum = max(values.values(), default=0)
    winners = [s for s, count in values.items() if maximum > 0 and count == maximum]
    dominant = winners[0].value if len(winners) == 1 else "mixed"
    return {"cleared_dingque": cleared, "dominant_suit": dominant}


def terminal_shape(state: Any, player: Any) -> str:
    if player.status != "finished" or not player.last_win:
        return "other"
    hand = [tile.face for tile in player.hand]
    if not bool(player.last_win.get("zimo")):
        winning_record = next(
            (
                record
                for owner in state.players
                for record in owner.discard_records
                if record.claimed_by == player.seat and record.claim_kind == "hu"
            ),
            None,
        )
        if winning_record is None:
            return "other"
        hand.append(physical_tile(winning_record.tile_id).face)
    melds = melds_from_raw(player.melds)
    check = is_winning_hand(hand, melds, player.dingque)
    if not check.ok or check.form is None:
        return "other"
    if check.form == WinForm.SEVEN_PAIRS:
        return "seven_pairs"
    all_tiles = hand + _meld_tiles(player)
    if all_tiles and len({tile.suit for tile in all_tiles}) == 1:
        return "pure_suit"
    if check.form == WinForm.STANDARD and can_form_all_koutsu(tiles_to_counts(hand), len(melds)) and all(m.kind != "chow" for m in melds):
        return "all_pongs"
    if check.form == WinForm.STANDARD:
        return "standard"
    return "other"


def _walk_validate_features(value: Any, path: tuple[str, ...] = ()) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if str(key).lower() in FORBIDDEN_FEATURE_KEYS:
                raise ValueError(f"forbidden feature field: {'.'.join(path + (str(key),))}")
            _walk_validate_features(child, path + (str(key),))
    elif isinstance(value, (list, tuple)):
        for index, child in enumerate(value):
            _walk_validate_features(child, path + (str(index),))
    elif isinstance(value, float) and not math.isfinite(value):
        raise ValueError(f"non-finite feature value: {'.'.join(path)}")


def validate_dataset(features: list[dict], labels: list[dict], requested: int, completed_games: set[str], illegal_actions: int) -> None:
    fids = [x["sample_id"] for x in features]
    lids = [x["sample_id"] for x in labels]
    if len(fids) != len(set(fids)) or len(lids) != len(set(lids)) or set(fids) != set(lids):
        raise ValueError("sample_id uniqueness/parity validation failed")
    if len(features) < requested:
        raise ValueError("actual_samples below requested_samples")
    split_by_game: dict[str, set[str]] = {}
    for feature in features:
        _walk_validate_features(feature["policy_features"])
        split_by_game.setdefault(feature["game_id"], set()).add(feature["split"])
    if any(len(splits) != 1 for splits in split_by_game.values()):
        raise ValueError("game split overlap")
    if set(split_by_game) != completed_games:
        raise ValueError("samples reference incomplete game")
    if illegal_actions:
        raise ValueError("illegal action rate is non-zero")
    allowed_dominant = {"wan", "tong", "tiao", "mixed"}
    allowed_shape = {"seven_pairs", "pure_suit", "all_pongs", "standard", "other"}
    if any(x["cleared_dingque"] not in (0, 1) or x["dominant_suit"] not in allowed_dominant or x["shape"] not in allowed_shape for x in labels):
        raise ValueError("invalid label enum")


def generate_dataset(samples: int, styles: list[str], seed: int, output: Path, games_limit: int | None = None) -> dict:
    if samples < 1:
        raise ValueError("--samples must be positive")
    if not styles or any(s not in ALLOWED_STYLES for s in styles):
        raise ValueError(f"--styles must use {','.join(ALLOWED_STYLES)}")
    config = EngineConfig(num_players=4)
    ruleset_hash = hashlib.sha256(_canonical(config.to_dict())).hexdigest()
    all_features: list[dict] = []
    all_labels: list[dict] = []
    completed_games: set[str] = set()
    game_index = 0
    while len(all_features) < samples and (games_limit is None or game_index < games_limit):
        game_id = f"model001-sim-v1-{seed}-{game_index:08d}"
        seat_styles = [styles[(game_index * 4 + seat) % len(styles)] for seat in range(4)]
        runner_box: dict[str, Any] = {}
        collector = SampleCollector(game_id, seat_styles, lambda: runner_box["runner"].state)
        players = [ProgrammaticStylePlayer(style, seed=seed ^ (game_index << 8) ^ seat, on_decision=collector.capture) for seat, style in enumerate(seat_styles)]
        runner = PlayerGameRunner(players, config, game_id=game_id, shutdown_players_on_end=True)
        runner_box["runner"] = runner
        runner.run()
        if runner.state is None or runner.state.phase != "finished":
            raise RuntimeError(f"game did not finish: {game_id}")
        pairs = collector.finalize(runner.state)
        for feature, label in pairs:
            feature["ruleset_hash"] = ruleset_hash
            all_features.append(feature)
            all_labels.append(label)
        completed_games.add(game_id)
        game_index += 1
    validate_dataset(all_features, all_labels, samples, completed_games, 0)
    output.mkdir(parents=True, exist_ok=True)
    for name, rows in (("features.jsonl", all_features), ("labels.jsonl", all_labels)):
        (output / name).write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
    style_counts = Counter(row["style_id"] for row in all_features)
    class_counts = {key: dict(Counter(row[key] for row in all_labels)) for key in ("cleared_dingque", "dominant_suit", "shape")}
    manifest = {
        "requested_samples": samples, "actual_samples": len(all_features), "games": game_index,
        "seed": seed, "styles": styles, "style_counts": dict(style_counts), "class_counts": class_counts,
        "excluded_samples": 0, "ruleset_hash": ruleset_hash, "feature_schema_version": FEATURE_SCHEMA_VERSION,
        "label_schema_version": LABEL_SCHEMA_VERSION, "generator_version": GENERATOR_VERSION,
        "cleared_target": "CURRENT_HIDDEN_STATE", "dominant_suit_target": "CURRENT_HIDDEN_STATE",
        "shape_target": "EVENTUAL_TERMINAL_OUTCOME", "validation_scope": "SIMULATION", "data_origin": "SIMULATION",
        "external_validity": "NOT_EVALUATED", "illegal_actions": 0, "valid": True,
    }
    (output / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", type=int, required=True)
    parser.add_argument("--styles", required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--games", type=int)
    args = parser.parse_args(argv)
    styles = [value.strip() for value in args.styles.split(",") if value.strip()]
    try:
        manifest = generate_dataset(args.samples, styles, args.seed, args.output, args.games)
    except Exception as exc:
        args.output.mkdir(parents=True, exist_ok=True)
        failure = {"requested_samples": args.samples, "actual_samples": 0, "valid": False, "error": f"{type(exc).__name__}: {exc}"}
        (args.output / "manifest.json").write_text(json.dumps(failure, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"MODEL-001 generation failed: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(manifest, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
