"""Generate current-run SPEC-V3 pilot evidence with real hashes and replay."""
from __future__ import annotations
import hashlib, json, platform, subprocess, time
from datetime import datetime, timezone
from pathlib import Path
from engine.action import Action, ActionType
from engine.audit import canonical_hash, load_audit, verify_audit
from engine.config import EngineConfig
from engine.legal import legal_discards
from engine.orchestrator import PlayerGameRunner
from engine.physical_tile import PHYSICAL_REGIONS, validate_physical_ownership
from engine.score import LedgerTransfer, apply_conserved_transfers
from engine.session import build_ready_game
from engine.tile import Suit, Tile
from players.humanlike.attention import rank_attention_cues
from players.humanlike.belief import model_001_rule_baseline
from players.registry import create_players
from protocols.player_view_builder import PlayerViewBuilder
from training.action_codec_v2 import legal_action_mask

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"docs/spec-v3/reports/task15_evidence"
CODE_FILES=("engine/legal.py","engine/physical_tile.py","engine/score.py","engine/audit.py","protocols/player_view_builder.py","protocols/player_view_v2.py","players/humanlike/attention.py","players/humanlike/belief.py","training/action_codec_v2.py")
def bytes_hash(paths):
    h=hashlib.sha256()
    for name in paths: h.update(name.encode()); h.update((ROOT/name).read_bytes())
    return h.hexdigest()
def pct(xs,q): return sorted(xs)[min(len(xs)-1,int((len(xs)-1)*q))]/1000
def audited_game(folder:Path, game_id:str):
    runner=PlayerGameRunner(create_players(["humanlike_v2","humanlike_v2"],base_seed=45),EngineConfig(num_players=2),game_id=game_id,save_dir=folder,save_every_decision=True)
    runner.run(); path=folder/f"{game_id}.audit.jsonl"; verified=verify_audit(path)
    return path,verified,canonical_hash(runner.state.to_dict())
def main():
    OUT.mkdir(parents=True,exist_ok=True)
    ruleset_hash=bytes_hash(("成都麻将AI人类化决策规则_v1.md","成都麻将AI训练模拟器程序实现规范_v2.0.0.md"))
    config_hash=canonical_hash(EngineConfig(num_players=2).to_dict()); code_hash=bytes_hash(CODE_FILES)
    dirty=bool(subprocess.run(["git","status","--porcelain"],cwd=ROOT,text=True,capture_output=True,check=True).stdout)
    state=build_ready_game("task15-unit-evidence",num_players=4); state.phase="discard"; state.current_seat=0; state.players[0].dingque=Suit.WAN
    builder=PlayerViewBuilder(); view=builder.build(state,0); regions={n:[] for n in PHYSICAL_REGIONS}; regions["wall"]=list(range(108))
    actions=[Action(ActionType.PASS),Action(ActionType.DISCARD,tiles=(Tile(Suit.WAN,1),))]
    calls={"RULE-003":lambda:legal_discards(state,0),"RULE-016":lambda:builder.build(state,0),"ALGO-001":lambda:validate_physical_ownership(regions),"ALGO-010":lambda:builder.build(state,0),"HEUR-019":lambda:rank_attention_cues(({"candidate_key":"a","mandatory":True,"salience":0,"freshness":0,"memory_strength":0},),capacity=1),"MODEL-001":lambda:model_001_rule_baseline(({"seat":1},)),"STATE-005":lambda:view.stable_hash,"SCORE-001":lambda:apply_conserved_transfers((0,0,0,0),(LedgerTransfer(1,0,4),)),"TRAIN-003":lambda:legal_action_mask(actions),"AUDIT-003":lambda:canonical_hash({"a":1,"previous_record_hash":None})}
    rows=[]; now=lambda:datetime.now(timezone.utc).isoformat().replace("+00:00","Z")
    for uid,fn in calls.items():
        for _ in range(100): fn()
        oracle=canonical_hash(str(fn())); times=[]
        for _ in range(1000): t=time.perf_counter_ns(); fn(); times.append(time.perf_counter_ns()-t)
        assert canonical_hash(str(fn()))==oracle
        rows.append({"timestamp_utc":now(),"run_id":"TASK15-REMEDIATION","game_id":state.game_id,"event_id":uid+"-PERF","unit_id":uid,"implementation_version":"SPEC-V3-3.0.3","ruleset_hash":ruleset_hash,"config_hash":config_hash,"code_hash":code_hash,"worktree_dirty":dirty,"seed_ref":None,"input_hash":canonical_hash(uid),"output_hash":oracle,"accepted":True,"error_code":None,"latency_us":{"p50":pct(times,.5),"p95":pct(times,.95),"p99":pct(times,.99),"max":max(times)/1000},"evidence_scope":"current-run","samples":1000,"warmup":100,"python":platform.python_version(),"os":platform.platform(),"cpu":platform.processor() or platform.machine()})
    runtime=OUT/"pilot_runtime.jsonl"; runtime.write_text("".join(json.dumps(r,ensure_ascii=False,sort_keys=True,separators=(",",":"))+"\n" for r in rows),encoding="utf-8")
    a,va,sa=audited_game(OUT/"run_a","task15-fixed-seed-game"); b,vb,sb=audited_game(OUT/"run_b","task15-fixed-seed-game")
    ah=[r["record_hash"] for r in load_audit(a)]; bh=[r["record_hash"] for r in load_audit(b)]
    comparison={"timestamp_utc":now(),"game_id":"task15-fixed-seed-game","seed_source":"game_id+base_seed=45","ruleset_hash":ruleset_hash,"config_hash":config_hash,"code_hash":code_hash,"run_a":str(a.relative_to(ROOT)),"run_b":str(b.relative_to(ROOT)),"decision_count":va.decision_count,"state_hash_equal":sa==sb,"record_hashes_equal":ah==bh,"final_state_hash":sa,"final_record_hash":va.final_record_hash,"reproducible":sa==sb and ah==bh and va.decision_count==vb.decision_count}
    replay=OUT/"fixed_seed_replay_comparison.json"; replay.write_text(json.dumps(comparison,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"runtime_sha256":hashlib.sha256(runtime.read_bytes()).hexdigest(),"replay_sha256":hashlib.sha256(replay.read_bytes()).hexdigest(),**comparison},ensure_ascii=False))
if __name__=="__main__": main()
