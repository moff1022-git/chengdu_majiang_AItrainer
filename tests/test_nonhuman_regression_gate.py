import json

from tools.nonhuman_regression_gate import evaluate


def _write(path, scores):
    path.write_text("".join(json.dumps({"game_id": f"g{i}", "scores": {"0": score}, "hu_sequence": [], "settle_tags": {"hua_zhu": []}}) + "\n" for i, score in enumerate(scores)))


def test_gate_pass_fail_and_error(tmp_path):
    n, e = tmp_path / "n.jsonl", tmp_path / "e.jsonl"
    _write(n, [2] * 20); _write(e, [0] * 20)
    spec = {"policy": {"bootstrap_iterations": 200, "metric_guardrails": {}}, "datasets": [{"test_id": "a", "dataset_sha256": "sha-a", "requested_games": 20, "nonhuman_games": str(n), "expert_games": str(e)}]}
    assert evaluate(spec)["status"] == "PASS"
    _write(n, [-1] * 20)
    assert evaluate(spec)["status"] == "FAIL"
    spec["datasets"][0]["requested_games"] = 21
    assert evaluate(spec)["status"] == "ERROR"


def test_gate_rejects_duplicate_dataset_sha(tmp_path):
    n, e = tmp_path / "n.jsonl", tmp_path / "e.jsonl"
    _write(n, [1] * 10); _write(e, [0] * 10)
    item = {"test_id": "a", "dataset_sha256": "same", "requested_games": 10, "nonhuman_games": str(n), "expert_games": str(e)}
    spec = {"policy": {"bootstrap_iterations": 100}, "datasets": [item, {**item, "test_id": "b"}]}
    assert evaluate(spec)["status"] == "ERROR"
