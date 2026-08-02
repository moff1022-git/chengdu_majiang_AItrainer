"""Generate deterministic F0037 12-preset parameter/behavior comparison."""
from pathlib import Path
from players.humanlike.personality_presets import LEVEL_PRESETS, PRESET_IDS, STYLE_PRESETS

OUT=Path("docs/status/F0037_12_PRESET_COMPARISON.md")
lines=["# F0037 十二人格预设固定输入对比","","固定公开输入、game_id=`f0037-preset-comparison-001`；本报告比较确定性有效参数，不使用隐藏牌标签。","","| preset | candidates | attention | depth | error cap | peng | gang | big hand | defense |","|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
for preset in PRESET_IDS:
    level,style=preset.split("_",1); lv=LEVEL_PRESETS[level]; st=STYLE_PRESETS[style]
    lines.append(f"| {preset} | {lv['max_candidates']} | {lv['attention_capacity']} | {lv['search_depth']} | {lv['max_error_probability']:.3f} | {st['peng_preference']:.2f} | {st['gang_preference']:.2f} | {st['big_hand_preference']:.2f} | {st['defense_awareness']:.2f} |")
OUT.write_text("\n".join(lines)+"\n",encoding="utf-8")
print(OUT)
