"""Record non-gating B1-A performance baselines and the ALGO-009 1MB gate."""
from __future__ import annotations
import json, platform, statistics, sys, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from engine.rng_v2 import derive_coordinate_seed
from players.humanlike.config_v2 import canonical_v2_bytes
from players.humanlike.state010 import PARAMETER_IDS, SeatRuntimeStore, resolve_parameters

def stats(samples):
    ordered=sorted(samples); n=len(ordered)
    return {"samples":n,"p50_us":ordered[int(n*.50)],"p95_us":ordered[int(n*.95)],"p99_us":ordered[min(n-1,int(n*.99))],"max_us":max(ordered)}
def measure(fn,n=500):
    out=[]
    for _ in range(n):
        start=time.perf_counter_ns(); fn(); out.append((time.perf_counter_ns()-start)//1000)
    return stats(out)
def main():
    store=SeatRuntimeStore('bench')
    one_mb={"payload":"x"*(1024*1024)}
    report={"environment":{"python":sys.version,"platform":platform.platform()},"state010_resolve_60":measure(lambda:resolve_parameters({pid:{} for pid in PARAMETER_IDS},phase='match_create')),"state010_snapshot_33":measure(lambda:store.snapshot(0)),"algo009_canonical_1mb":measure(lambda:canonical_v2_bytes(one_mb),50),"algo011_coordinate":measure(lambda:derive_coordinate_seed(game_id='g'*64,stream_name='training_noise',consumer_kind='trainer',consumer_id='worker',event_id='event',sample_index=42))}
    report["algo009_under_50ms"] = report["algo009_canonical_1mb"]["max_us"] <= 50000
    path=ROOT/'docs/spec-v3/evidence/task18b_b1a/B1-A_performance_baseline.json'; path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); print(json.dumps(report))
if __name__=='__main__': main()
