"""F0010-L prediction log + analysis."""

from __future__ import annotations

from pathlib import Path

from engine.config import EngineConfig
from engine.deal import create_dealt_game
from players.analysis.hand_predict import (
    apply_oracle_accuracy,
    predict_opponent_hands,
)
from players.analysis.predict_log import (
    PredictLogWriter,
    analyze_predict_logs,
    build_predict_tick,
    random_baseline_f1,
)
from players.analysis.remain import remain_map


def test_random_baseline_and_tick_roundtrip(tmp_path: Path) -> None:
    st = create_dealt_game("plog-1", config=EngineConfig(num_players=4))
    fcs = predict_opponent_hands(st, 0, top_k=3, seed=1)
    oracle = {str(p.seat): [t.id for t in p.hand] for p in st.players if p.seat != 0}
    fcs = apply_oracle_accuracy(fcs, oracle)
    remain = remain_map(st, 0)
    true = oracle["1"]
    base = random_baseline_f1(true, remain, seed=0)
    assert 0.0 <= base <= 1.0
    row = build_predict_tick(
        game_id="plog-1",
        self_seat=0,
        forecasts=fcs,
        oracle_hands=oracle,
        discard_fp="test",
        used_continuity=False,
        remain=remain,
        meta_by_seat={
            1: {"n_discards": 0, "n_melds": 0, "dingque": None},
            2: {"n_discards": 1, "n_melds": 0, "dingque": "wan"},
            3: {"n_discards": 2, "n_melds": 0, "dingque": None},
        },
        source="test",
    )
    assert row["type"] == "predict_tick"
    assert row["mean_accuracy"] is not None
    assert len(row["opponents"]) == 3
    w = PredictLogWriter("plog-1", log_dir=tmp_path)
    w.emit(row)
    w.close()
    analysis = analyze_predict_logs(tmp_path)
    assert analysis.n_ticks == 1
    assert analysis.n_opponent_samples == 3
    assert analysis.mean_best_f1 is not None
    assert analysis.causes


def test_eval_one_game_writes_logs(tmp_path: Path) -> None:
    from players.analysis.predict_eval import evaluate_one_game

    meta = evaluate_one_game(
        "plog-eval-0",
        log_dir=tmp_path,
        self_seats=[0],
        max_steps=200,
    )
    assert meta["n_ticks"] >= 1
    files = list(tmp_path.glob("*.jsonl"))
    assert files
    analysis = analyze_predict_logs(tmp_path)
    assert analysis.n_ticks >= 1
