"""Identify W2 native-gate inputs; freeze is lead-only, check is read-only."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
DEST = Path(__file__).with_name("tested-manifest.json")


def current():
    names = subprocess.check_output(
        ["git", "ls-files", "-z", "--", "skills/sohrab", "scripts", "AGENTS.md", "CLAUDE.md"],
        cwd=ROOT,
    ).decode().split("\0")
    names += subprocess.check_output(
        ["git", "ls-files", "--others", "--exclude-standard", "-z", "--", "skills/sohrab", "scripts"],
        cwd=ROOT,
    ).decode().split("\0")
    entries = []
    for name in sorted(set(filter(None, names))):
        path = ROOT / name
        entries.append({"path": name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    raw = "".join(e["path"] + "\0" + e["sha256"] + "\n" for e in entries).encode()
    return {
        "head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT).decode().strip(),
        "branch": subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT).decode().strip(),
        "digest": hashlib.sha256(raw).hexdigest(),
        "entries": entries,
    }


if __name__ == "__main__":
    state = current()
    if sys.argv[1:] == ["freeze"]:
        state["observed_at"] = datetime.now(timezone.utc).isoformat()
        state["method"] = "SHA-256 of sorted UTF-8 repo-relative path + NUL + lowercase file SHA-256 + LF"
        DEST.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        print("FROZEN", state["head"], state["digest"], len(state["entries"]))
    elif sys.argv[1:] == ["check"]:
        expected = json.loads(DEST.read_text(encoding="utf-8"))
        if any(state[k] != expected[k] for k in ("head", "branch", "digest", "entries")):
            old = {e["path"]: e["sha256"] for e in expected["entries"]}
            new = {e["path"]: e["sha256"] for e in state["entries"]}
            print("CONTAMINATED", [p for p in sorted(old.keys() | new.keys()) if old.get(p) != new.get(p)])
            raise SystemExit(1)
        print("UNCHANGED", state["head"], state["digest"], len(state["entries"]))
    else:
        raise SystemExit("usage: snapshot.py freeze|check")
