"""Strategy preset config + player factory."""

from __future__ import annotations

from players.registry import create_player, create_players
from players.strategy_presets import get_preset, list_strategy_ids, load_presets, ui_choices


def test_presets_include_current_s2() -> None:
    ids = list_strategy_ids()
    assert "rule_ai" in ids
    assert "random" in ids
    assert "current_s2" in ids
    p = get_preset("current_s2")
    assert p is not None
    assert p.get("use_f0011") is True
    assert p.get("player") == "rule_ai"
    assert ui_choices()


def test_create_current_s2_player() -> None:
    pl = create_player("current_s2", seat=2, seed=42)
    assert pl.__class__.__name__ == "RuleAIPlayer"
    assert getattr(pl, "use_f0011", False) is True
    assert getattr(pl, "strategy_id", None) == "current_s2"


def test_create_players_mixed_presets() -> None:
    ps = create_players("rule_ai,current_s2,random,rule_ai", base_seed=1)
    assert len(ps) == 4
    assert getattr(ps[0], "use_f0011", False) is False
    assert getattr(ps[1], "use_f0011", False) is True
    assert ps[2].__class__.__name__ == "RandomPlayer"


def test_hub_accepts_current_s2() -> None:
    from players.seat_ui_hub import SeatUIHub

    hub = SeatUIHub(num_players=4, human_seat=None)
    hub.apply_seat_settings_msg(
        {"type": "seat_settings", "seat": 1, "ai_type": "current_s2"}
    )
    assert hub.seat_ai_types.get(1) == "current_s2"
    spec = hub.compose_players_spec("rule_ai,rule_ai,rule_ai,rule_ai")
    assert "current_s2" in spec.split(",")
