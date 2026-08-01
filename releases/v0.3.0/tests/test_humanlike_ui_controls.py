from display.lobby_view import humanlike_status, toggle_humanlike_players


def test_global_toggle_preserves_humans_and_enables_all_ai():
    enabled = toggle_humanlike_players("human,rule_ai,random,current_s2")
    assert enabled == "human,humanlike_v2,humanlike_v2,humanlike_v2"
    assert humanlike_status(enabled) == "开启"


def test_global_disable_only_restores_humanlike():
    disabled = toggle_humanlike_players("human,humanlike_v2,humanlike_v2,humanlike_v2")
    assert disabled == "human,rule_ai,rule_ai,rule_ai"
    assert humanlike_status("human,humanlike_v2,random,rule_ai") == "混合"
