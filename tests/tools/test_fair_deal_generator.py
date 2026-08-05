import hashlib, json
from tools.fair_deal_generator import generate, validate

def test_fair_generator_reproducible_and_seed_distinct(tmp_path):
    a,b,c=tmp_path/'a',tmp_path/'b',tmp_path/'c'
    ma=generate('fair-a','seed-a',12,a);mb=generate('fair-a','seed-a',12,b);mc=generate('fair-c','seed-c',12,c)
    validate(a);validate(b);validate(c)
    assert (a/'deals.jsonl').read_bytes()==(b/'deals.jsonl').read_bytes()
    assert ma['sha256']==mb['sha256'] and ma['sha256']!=mc['sha256']
    rows=[json.loads(x) for x in (a/'deals.jsonl').read_text().splitlines()]
    assert [r['dealer'] for r in rows[:8]]==[0,1,2,3,0,1,2,3]
