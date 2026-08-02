"""Run one fixed-game smoke evaluation for all 12 F0037 presets."""
from pathlib import Path
import json
from players.humanlike.personality_presets import PRESET_IDS
from players.registry import create_players
import time
from engine.config import EngineConfig
from engine.orchestrator import PlayerGameRunner

OUT=Path("data/ai_capability/results/f0037_12_presets_smoke")
OUT.mkdir(parents=True, exist_ok=True)
rows=[]
for index, preset in enumerate(PRESET_IDS):
    players = create_players(["humanlike_v2"]*4, humanlike_presets=[preset]*4)
    timing = [{"seconds": [], "phases": {}} for _ in players]
    result=PlayerGameRunner(players, EngineConfig(num_players=4), game_id=f"f0037-preset-{index:02d}-001").run()
    row=result.to_dict(); row["decision_timing"]=timing
    row["preset_id"]=preset; rows.append(row)
(OUT/"summary.json").write_text(json.dumps({"games":len(rows),"presets":PRESET_IDS,"rows":rows},ensure_ascii=False,indent=2),encoding="utf-8")
print(OUT/"summary.json")
