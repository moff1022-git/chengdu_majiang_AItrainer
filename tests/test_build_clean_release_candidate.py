import subprocess
from tools import build_clean_release_candidate as builder


def test_clean_candidate_excludes_runtime_data(tmp_path, monkeypatch):
    evidence = tmp_path / "e.json"; evidence.write_text("{}")
    monkeypatch.setattr(builder, "ROOT", tmp_path)
    (tmp_path / "ok.py").write_text("ok")
    monkeypatch.setattr(subprocess, "check_output", lambda args, **kwargs: ("ok.py\0data/x\0" if kwargs.get("text") else b"ok.py\0data/x\0") if "ls-files" in args else ("abc\n" if kwargs.get("text") else b"abc\n"))
    result = builder.build(tmp_path / "out", [evidence])
    source = tmp_path / "out/v0.3.1-f0066-rc-source"
    assert (source / "ok.py").is_file()
    assert not (source / "data").exists()
    assert len(result["archives"]) == 2


def test_cli_accepts_release_version(tmp_path, monkeypatch):
    evidence = tmp_path / "e.json"; evidence.write_text("{}")
    monkeypatch.setattr(builder, "ROOT", tmp_path)
    (tmp_path / "ok.py").write_text("ok")
    monkeypatch.setattr(subprocess, "check_output", lambda args, **kwargs: ("ok.py\0" if kwargs.get("text") else b"ok.py\0") if "ls-files" in args else ("abc\n" if kwargs.get("text") else b"abc\n"))
    assert builder.main(["--output", str(tmp_path / "out"), "--evidence", str(evidence), "--version", "0.3.2"]) == 0
    assert (tmp_path / "out/v0.3.2-source.zip").is_file()
