"""Build deterministic clean source/evidence release-candidate archives."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = ("data/", "releases/", "backup/", ".git/", ".venv", "logs/", "build/", "dist/")


def digest(path: Path) -> str: return hashlib.sha256(path.read_bytes()).hexdigest()


def manifest(root: Path) -> list[dict]:
    return [{"path": p.relative_to(root).as_posix(), "size": p.stat().st_size, "sha256": digest(p)}
            for p in sorted(root.rglob("*")) if p.is_file() and p.name != "MANIFEST.json"]


def _zip_tree(root: Path, target: Path) -> None:
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(root.rglob("*")):
            if path.is_file():
                info = zipfile.ZipInfo(f"{root.name}/{path.relative_to(root).as_posix()}", (2026, 8, 5, 0, 0, 0)); info.external_attr = 0o644 << 16
                archive.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED)


def build(output: Path, evidence: list[Path], version: str = "0.3.1-f0066-rc") -> dict:
    source = output / f"v{version}-source"; evdir = output / f"v{version}-evidence"
    for path in (source, evdir):
        if path.exists(): shutil.rmtree(path)
        path.mkdir(parents=True)
    tracked = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).decode().split("\0")
    for rel in tracked:
        if not rel or rel.startswith(EXCLUDED): continue
        src = ROOT / rel
        if src.is_file():
            dst = source / rel; dst.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(src, dst)
    for src in evidence:
        src = src.resolve(); dst = evdir / src.name; shutil.copy2(src, dst)
    provenance = {"version": version, "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
                  "evidence_files": [p.name for p in evidence]}
    (evdir / "PROVENANCE.json").write_text(json.dumps(provenance, indent=2) + "\n")
    for root in (source, evdir): (root / "MANIFEST.json").write_text(json.dumps(manifest(root), indent=2) + "\n")
    archives = []
    for root in (source, evdir):
        target = output / f"{root.name}.zip"; _zip_tree(root, target); archives.append({"path": target.name, "sha256": digest(target), "size": target.stat().st_size})
    result = {"version": version, "archives": archives}
    (output / "SHA256SUMS.json").write_text(json.dumps(result, indent=2) + "\n")
    return result


def main(argv=None) -> int:
    p = argparse.ArgumentParser(); p.add_argument("--output", type=Path, default=ROOT / "releases"); p.add_argument("--evidence", type=Path, action="append", required=True)
    p.add_argument("--version", default="0.3.1-f0066-rc", help="archive version label")
    args = p.parse_args(argv); print(json.dumps(build(args.output, args.evidence, version=args.version), indent=2)); return 0


if __name__ == "__main__": raise SystemExit(main())
