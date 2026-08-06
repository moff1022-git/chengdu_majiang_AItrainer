from pathlib import Path


def test_manual_regression_workflow_is_evidence_gated():
    text = Path(".github/workflows/nonhuman-regression.yml").read_text()
    assert "workflow_dispatch:" in text
    assert "push:" not in text
    assert "artifact_run_id:" in text
    assert "artifact_sha256:" in text
    assert "actions/download-artifact@v4" in text
    assert "artifact SHA mismatch" in text
    assert "tools/nonhuman_regression_gate.py" in text
    assert "if: always()" in text
