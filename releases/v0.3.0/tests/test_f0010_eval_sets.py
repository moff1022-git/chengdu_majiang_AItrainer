"""Fixed F0010 eval game_id sets (20 ⊂ 50 ⊂ 100)."""

from __future__ import annotations

from players.analysis.predict_eval import load_eval_set, list_eval_sets


def test_eval_sets_nested_and_unique() -> None:
    sizes = list_eval_sets()
    assert sizes.get("20") == 20
    assert sizes.get("50") == 50
    assert sizes.get("100") == 100

    s20 = load_eval_set("20")
    s50 = load_eval_set("50")
    s100 = load_eval_set("100")
    assert len(s20) == 20
    assert len(s50) == 50
    assert len(s100) == 100

    # nested supersets
    assert [e["game_id"] for e in s20] == [e["game_id"] for e in s50[:20]]
    assert [e["game_id"] for e in s50] == [e["game_id"] for e in s100[:50]]
    assert [e["play_seed"] for e in s20] == [e["play_seed"] for e in s50[:20]]

    ids = [e["game_id"] for e in s100]
    assert len(ids) == len(set(ids))
    seeds = [e["play_seed"] for e in s100]
    assert all(isinstance(s, int) for s in seeds)
    assert all(e["game_id"].startswith("f0010-bench-") for e in s100)


def test_eval_set_load_invalid() -> None:
    try:
        load_eval_set("999")
        assert False, "expected KeyError"
    except KeyError:
        pass
