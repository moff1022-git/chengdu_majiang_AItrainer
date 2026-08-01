from players.humanlike.rp_archive import dual_view, load_envelopes, payload_view, save_envelopes
from players.humanlike.rp_schema import make_envelope

def test_archive_roundtrip_and_dual_views(tmp_path):
    values={"RP-001": make_envelope("RP-001", {"round_id":"g"}, event_index=0), "RP-029": make_envelope("RP-029", [{"x":1}], event_index=1, visibility="audit_only")}
    path=tmp_path/"rp.json"; save_envelopes(path, values); loaded=load_envelopes(path)
    assert loaded["RP-001"]["payload"] == {"round_id":"g"}
    assert "RP-029" not in payload_view(loaded)
    assert payload_view(loaded, include_audit=True)["RP-029"] == [{"x":1}]
    assert "envelope" in dual_view(loaded) and "payload" in dual_view(loaded)
