"""Player failure / crash handling policies."""

from __future__ import annotations

import json
import random
import traceback
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Callable

from engine.action import Action, ActionType
from engine.legal import action_in_legal
from engine.state import GameState
from players.base_player import BasePlayer
from protocols.messages import ActionRequest, Decision

def _default_crash_path() -> Path:
    try:
        from app_paths import configs_dir

        return configs_dir() / "crash_policy.json"
    except Exception:
        return (
            Path(__file__).resolve().parent.parent / "configs" / "crash_policy.json"
        )


_DEFAULT_PATH = _default_crash_path()


class CrashPolicy(str, Enum):
    ABORT_RESTART = "abort_restart"
    REPLACE_PLAYER = "replace_player"
    FORCE_PASS = "force_pass"


@dataclass
class CrashConfig:
    policy: CrashPolicy = CrashPolicy.REPLACE_PLAYER
    timeout_ms: int = 120_000
    max_crashes: int = 3
    fallback_player: str = "random"
    log_stack: bool = True
    restart_on_abort: bool = False

    @classmethod
    def load(cls, path: Path | str | None = None) -> CrashConfig:
        p = Path(path) if path else _DEFAULT_PATH
        if not p.exists():
            return cls()
        data = json.loads(p.read_text(encoding="utf-8"))
        return cls(
            policy=CrashPolicy(str(data.get("policy", "replace_player"))),
            timeout_ms=int(data.get("timeout_ms", 120_000)),
            max_crashes=int(data.get("max_crashes", 3)),
            fallback_player=str(data.get("fallback_player", "random")),
            log_stack=bool(data.get("log_stack", True)),
            restart_on_abort=bool(data.get("restart_on_abort", False)),
        )

    def to_dict(self) -> dict:
        d = asdict(self)
        d["policy"] = self.policy.value
        return d


@dataclass
class CrashEvent:
    seat: int
    error: str
    policy: str
    turn_index: int
    stack: str | None = None


class AbortGame(Exception):
    """Signal orchestrator to end the game due to crash policy."""

    def __init__(self, reason: str = "player_crash"):
        super().__init__(reason)
        self.reason = reason


class CrashHandler:
    def __init__(
        self,
        config: CrashConfig | None = None,
        *,
        rng: random.Random | None = None,
        create_fallback: Callable[[int, str], BasePlayer] | None = None,
    ) -> None:
        self.config = config or CrashConfig.load()
        self.rng = rng or random.Random(0)
        self.create_fallback = create_fallback
        self.crash_counts: dict[int, int] = {}
        self.crash_log: list[dict] = []

    def note(
        self,
        state: GameState,
        seat: int,
        error: BaseException,
        *,
        policy_used: CrashPolicy | None = None,
    ) -> None:
        pol = (policy_used or self.config.policy).value
        stack = traceback.format_exc() if self.config.log_stack else None
        entry = {
            "seat": seat,
            "error": f"{type(error).__name__}: {error}",
            "policy": pol,
            "turn_index": state.turn_index,
            "stack": stack,
        }
        self.crash_log.append(entry)
        self.crash_counts[seat] = self.crash_counts.get(seat, 0) + 1

    def should_abort_seat(self, seat: int) -> bool:
        return self.crash_counts.get(seat, 0) >= self.config.max_crashes

    def force_legal_decision(
        self,
        request: ActionRequest,
        legal: list[Action],
        *,
        reason_prefix: str = "crash:force",
    ) -> Decision:
        if not legal:
            # synthesize PASS if possible
            legal = [Action(ActionType.PASS)]
        # Prefer PASS, else random discard/legal
        passes = [a for a in legal if a.type == ActionType.PASS]
        discards = [a for a in legal if a.type == ActionType.DISCARD]
        if passes and request.phase == "response":
            action = passes[0]
        elif discards:
            action = self.rng.choice(discards)
        else:
            action = self.rng.choice(list(legal))
        return Decision(
            request_id=request.request_id,
            action=action,
            reason=f"{reason_prefix}:{action.type.value}",
        )

    def handle(
        self,
        state: GameState,
        seat: int,
        error: BaseException,
        request: ActionRequest,
        legal: list[Action],
        players: list[BasePlayer],
    ) -> Decision:
        """
        Apply crash policy. May mutate players list (replace).
        Raises AbortGame when policy aborts.
        """
        self.note(state, seat, error)
        if self.should_abort_seat(seat) and self.config.policy != CrashPolicy.ABORT_RESTART:
            # too many crashes → abort
            raise AbortGame(f"player_crash_seat_{seat}_max")

        policy = self.config.policy
        if policy == CrashPolicy.ABORT_RESTART:
            raise AbortGame("player_crash")

        if policy == CrashPolicy.REPLACE_PLAYER:
            self._replace(seat, players, state)
            # after replace, force a legal action this turn
            return self.force_legal_decision(
                request, legal, reason_prefix="crash:replace_force"
            )

        # FORCE_PASS (and default fallback)
        return self.force_legal_decision(
            request, legal, reason_prefix="crash:force"
        )

    def handle_illegal(
        self,
        state: GameState,
        seat: int,
        request: ActionRequest,
        legal: list[Action],
        bad: Decision | None = None,
    ) -> Decision:
        err = ValueError(f"illegal decision: {bad.action if bad else '?'}")
        self.note(state, seat, err, policy_used=CrashPolicy.FORCE_PASS)
        return self.force_legal_decision(
            request, legal, reason_prefix="crash:illegal_force"
        )

    def _replace(
        self, seat: int, players: list[BasePlayer], state: GameState
    ) -> None:
        old = players[seat]
        try:
            old.shutdown()
        except Exception:
            pass
        if self.create_fallback is None:
            from players.registry import create_player

            def _cf(s: int, kind: str) -> BasePlayer:
                return create_player(kind, seat=None, seed=self.rng.randint(0, 1_000_000))

            self.create_fallback = _cf
        new_p = self.create_fallback(seat, self.config.fallback_player)
        new_p.on_join(seat, state.config or {})
        players[seat] = new_p
