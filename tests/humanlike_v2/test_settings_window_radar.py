from players.humanlike.config import load_config
from players.humanlike.personality_presets import PRESET_IDS, apply_personality_preset
from players.humanlike.player import default_humanlike_config_path
from players.humanlike.settings_window import SettingsWindow


def test_radar_uses_resolved_nonhuman_values_in_stable_axis_order():
    template = load_config(default_humanlike_config_path()).normalized_dict()["players"][0]
    player = apply_personality_preset(template, "nonhuman_optimized")
    window = object.__new__(SettingsWindow)
    outer, inner = window._radar_data(player)
    assert len(PRESET_IDS) == 13
    assert len(outer) == 12
    assert len(inner) == 7
    assert outer[1] == 0.50
    assert outer[8:12] == [0.40, 0.20, 0.25, 0.15]
    assert inner[:5] == [1.0, 1.0, 1.0, 1.0, 1.0]
