from tools.ai_capability_test import capability_experiments, choose_option, choose_batch_presets, confirm_run, game_ids, progress_bar, run_game, summarize, verification_code
import tools.ai_capability_test as capability_test


def test_capability_progress_line_contains_total_game_count(monkeypatch, capsys, tmp_path):
    monkeypatch.setattr(capability_test, "run_game", lambda specs, gid: {
        "game_id": gid, "scores": {"0": 1, "1": 0, "2": 0, "3": 0},
        "rankings": [0, 1, 2, 3], "hu_sequence": [], "decision_timing": [{"seconds": [0], "phases": {}} for _ in range(4)]
    })
    monkeypatch.setattr(capability_test, "write_outputs", lambda *args, **kwargs: None)
    monkeypatch.setattr(capability_test, "STOP", False)
    capability_test.run_capability_mode("random", 100, tmp_path)
    output = capsys.readouterr().out
    assert "总局数 1/1200" in output
    assert "已运行" in output
    assert "剩余约" in output


def test_capability_report_name_contains_run_timestamp(tmp_path, monkeypatch):
    monkeypatch.setattr(capability_test, "run_game", lambda specs, gid: {
        "game_id": gid, "scores": {"0": 1, "1": 0, "2": 0, "3": 0},
        "rankings": [0, 1, 2, 3], "hu_sequence": [], "decision_timing": [{"seconds": [0], "phases": {}} for _ in range(4)]
    })
    monkeypatch.setattr(capability_test, "write_outputs", lambda *args, **kwargs: None)
    monkeypatch.setattr(capability_test, "STOP", False)
    capability_test.run_capability_mode("random", 100, tmp_path)
    reports = list(tmp_path.glob("capability_report_*.md"))
    assert len(reports) == 1
    stamp = reports[0].stem.removeprefix("capability_report_")
    assert len(stamp) == 15 and stamp[8] == "_" and stamp.replace("_", "").isdigit()


def test_progress_bar_is_bounded_and_shows_percent():
    bar = progress_bar(25, 100, width=20)
    assert bar.startswith("[#####")
    assert "25.00%" in bar


def test_verification_code_changes_with_game_count():
    common = {"game_id_list": ["batch-20260301-0"], "players": ["random"] * 4, "mode": "batch"}
    assert verification_code(games=100, **common) != verification_code(games=200, **common)


def test_capability_summary_ignores_isolated_failed_game():
    row = {"status": "FAILED", "scores": {}, "rankings": [], "hu_sequence": [], "decision_timing": [{"seconds": [], "phases": {}} for _ in range(4)]}
    summary = summarize([row], ["random"] * 4, 1, True)
    assert all(seat["games"] == 1 and seat["decisions"] == 0 for seat in summary["seats"])


def test_numbered_menu_returns_selected_option():
    answers = iter(["2"])
    assert choose_option("mode", ["batch", "capability"], input_fn=lambda _: next(answers)) == "capability"


def test_confirmation_requires_explicit_yes_and_estimates_capability_scope():
    prompts = []
    assert not confirm_run(100, "capability", "humanlike_v2", input_fn=lambda prompt: prompts.append(prompt) or "n")
    assert "1200 局" in prompts[0]
    assert confirm_run(100, "capability", "humanlike_v2", input_fn=lambda _: "y")

def test_estimate_seconds_accounts_for_threads():
    from tools.ai_capability_test import estimate_seconds
    assert estimate_seconds(100, "capability", threads=5) < estimate_seconds(100, "capability", threads=1)
    prompts = []
    confirm_run(100, "batch", threads=10, input_fn=lambda prompt: prompts.append(prompt) or "n")
    assert "并发线程 10" in prompts[0]


def test_capability_mode_rotates_target_across_all_seats():
    experiments = capability_experiments("humanlike_v2")
    assert len(experiments) == 12
    assert {item["seat"] for item in experiments} == {0, 1, 2, 3}
    assert {item["baseline"] for item in experiments} == {"random", "rule_ai", "rule_ai_plus"}
    for item in experiments:
        assert item["players"][item["seat"]] == "humanlike_v2"

def test_batch_preset_menu_only_prompts_humanlike_seats():
    answers = iter(["1", "2"])
    presets = choose_batch_presets(["humanlike_v2", "random", "humanlike_v2", "rule_ai"], input_fn=lambda _: next(answers))
    assert presets[0] == list(capability_test.PRESET_IDS)[0]
    assert presets[1] is None
    assert presets[2] == list(capability_test.PRESET_IDS)[1]

def test_capability_manifest_records_scalar_preset(tmp_path, monkeypatch):
    monkeypatch.setattr(capability_test, "run_game", lambda specs, gid, presets=None: {"game_id": gid, "scores": {"0": 0, "1": 0, "2": 0, "3": 0}, "rankings": [], "hu_sequence": [], "decision_timing": [{"seconds": [], "phases": {}} for _ in range(4)]})
    monkeypatch.setattr(capability_test, "write_outputs", lambda *args, **kwargs: None)
    monkeypatch.setattr(capability_test, "STOP", False)
    capability_test.run_capability_mode("humanlike_v2", 100, tmp_path, ["low_aggressive"] * 4, 1)
    manifest = __import__('json').loads((tmp_path / "manifest.json").read_text())
    assert manifest["humanlike_preset"] == "low_aggressive"


def test_fixed_game_ids_are_numeric_and_unique():
    ids = game_ids(100)
    assert ids[:3] == ["batch-20260301-0", "batch-20260301-1", "batch-20260301-2"]
    assert len(ids) == len(set(ids)) == 100


def test_smoke_game_records_scores_and_decision_latency():
    specs = ["random", "rule_ai", "rule_ai_plus", "humanlike_v2"]
    row = run_game(specs, "batch-20260301-0")
    summary = summarize([row], specs, 1, False)
    assert set(row["scores"]) == {"0", "1", "2", "3"}
    assert all(seat["decisions"] > 0 for seat in summary["seats"])
    assert all(seat["avg_response_ms"] >= 0 for seat in summary["seats"])
