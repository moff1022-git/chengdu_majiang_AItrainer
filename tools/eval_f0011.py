#!/usr/bin/env python3
"""A6: compare baseline vs F0011 discard advisor on fixed eval set states.

Usage:
  .venv/bin/python tools/eval_f0011.py --set 20
  .venv/bin/python tools/eval_f0011.py --set 20 --max-decisions 80
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="F0011 discard advisor eval (A6)")
    p.add_argument("--set", dest="eval_set", default="20", choices=["20", "50", "100"])
    p.add_argument("--max-decisions", type=int, default=120)
    p.add_argument("--max-steps", type=int, default=400)
    args = p.parse_args(argv)

    from engine.action import ActionType
    from engine.blood_battle import PlayError, finalize_game
    from engine.config import EngineConfig
    from engine.session import GameSession, build_ready_game
    from players.analysis.opponent_model import estimate_opponents
    from players.analysis.pipeline import analyze_for_seat
    from players.analysis.predict_eval import load_eval_set
    from players.analysis.strategy import rank_discards

    specs = load_eval_set(args.eval_set)
    cfg = EngineConfig(num_players=4)

    n_cmp = 0
    agree = 0
    base_danger_score = 0.0
    f11_danger_score = 0.0
    base_sh = 0.0
    f11_sh = 0.0
    dang_rank = {"critical": 4, "high": 3, "medium": 2, "low": 1, "safe": 0, "unknown": 2}

    for spec in specs:
        if n_cmp >= args.max_decisions:
            break
        gid = str(spec["game_id"])
        rng = random.Random(int(spec["play_seed"]))
        state = build_ready_game(gid, num_players=4, config=cfg)
        session = GameSession(state, cfg)
        try:
            session.start_play()
            steps = 0
            while not session.is_terminal() and steps < args.max_steps:
                steps += 1
                st = session.state
                if st.phase == "draw":
                    session.step_auto_draw()
                    continue
                if st.phase == "discard":
                    seat = st.current_seat
                    assert seat is not None
                    acts = session.legal_actions(seat)
                    discs = [a for a in acts if a.type == ActionType.DISCARD]
                    if not discs:
                        action = rng.choice(acts)
                        session.apply(seat, action)
                        continue
                    # only compare for seat 0
                    if seat == 0 and n_cmp < args.max_decisions:
                        hand = list(st.players[0].hand)
                        melds = st.players[0].melds
                        dq = st.players[0].dingque
                        ops = estimate_opponents(st, 0)
                        base = rank_discards(
                            st, 0, hand, melds, dq, ops, legal_discards=discs
                        )
                        snap = analyze_for_seat(
                            st, 0, legal_discards=discs, use_f0011=True, f0011_top_k=3
                        )
                        f11 = snap.discard_ranks
                        if base and f11:
                            b0, f0 = base[0], f11[0]
                            n_cmp += 1
                            if b0.tile_id == f0.tile_id:
                                agree += 1
                            base_danger_score += dang_rank.get(b0.danger, 2)
                            f11_danger_score += dang_rank.get(f0.danger, 2)
                            base_sh += b0.shanten_after
                            f11_sh += f0.shanten_after
                    # play random legal discard to advance
                    session.apply(seat, rng.choice(discs))
                    continue
                if st.phase == "response":
                    for rseat in list(st.response_seats or []):
                        if session.is_terminal() or st.phase != "response":
                            break
                        if rseat not in (st.response_seats or []):
                            continue
                        if rseat in (st.pending_claims or {}):
                            continue
                        acts = session.legal_actions(rseat)
                        if not acts:
                            continue
                        passes = [a for a in acts if a.type == ActionType.PASS]
                        session.apply(
                            rseat, passes[0] if passes else rng.choice(acts)
                        )
                    continue
                if st.phase == "ready":
                    session.start_play()
                    continue
                if st.phase == "finished":
                    break
                raise PlayError(f"stuck {st.phase}")
            if not session.is_terminal():
                st = session.state
                st.phase = "finished"
                st.finished_reason = st.finished_reason or "max_steps"
                finalize_game(st, cfg)
        except Exception as e:
            print(f"[skip] {gid}: {e}", file=sys.stderr)
            continue

    report = {
        "eval_set": args.eval_set,
        "n_compare_decisions": n_cmp,
        "agree_rate": round(agree / n_cmp, 4) if n_cmp else None,
        "baseline_mean_danger_rank": round(base_danger_score / n_cmp, 4) if n_cmp else None,
        "f0011_mean_danger_rank": round(f11_danger_score / n_cmp, 4) if n_cmp else None,
        "baseline_mean_shanten_after": round(base_sh / n_cmp, 4) if n_cmp else None,
        "f0011_mean_shanten_after": round(f11_sh / n_cmp, 4) if n_cmp else None,
        "note": "lower danger_rank is safer; lower shanten_after is more offensive",
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    out = Path("logs/predict") / f"f0011-set{args.eval_set}-report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
