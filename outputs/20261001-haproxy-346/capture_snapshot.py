"""Capture package and repository-gate inputs without modifying the candidate."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import subprocess
import sys


def capture():
    root = Path(__file__).resolve().parents[2]
    paths = []
    for scope in ("skills/sohrab/alaa-haproxy", "skills/sohrab/alaa-haproxy-lua", "scripts"):
        paths.extend(p for p in (root / scope).rglob("*")
                     if p.is_file() and "__pycache__" not in p.parts)
    for name in ("AGENTS.md", "CLAUDE.md", "skills/sohrab/AGENTS.md",
                 "skills/sohrab/README.md", "skills/sohrab/README.fa.md",
                 "skills/sohrab/alaa-repo-docs/scripts/check_markdown_links.py",
                 "skills/sohrab/alaa-workflow/scripts/validate_workflow_files.py",
                 "outputs/README.md", "outputs/20261001-haproxy-346/README.md",
                 "outputs/20261001-haproxy-346/capture_snapshot.py"):
        paths.append(root / name)
    manifest = [{"path": p.relative_to(root).as_posix(),
                 "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
                for p in sorted(set(paths), key=lambda p: p.relative_to(root).as_posix())]
    encoded = json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode()
    return {"observed_at": datetime.now(timezone.utc).isoformat(),
            "HEAD": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root,
                                            text=True).strip(),
            "scope_sha256": hashlib.sha256(encoded).hexdigest(), "files": manifest}


if __name__ == "__main__":
    receipt = capture()
    if len(sys.argv) != 2:
        raise SystemExit("usage: python capture_snapshot.py <receipt.json>")
    Path(sys.argv[1]).write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(receipt["HEAD"], receipt["scope_sha256"], len(receipt["files"]))
