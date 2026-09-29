"""Capture this task's HEAD-relative and untracked source; never stage files."""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("name", help="New immutable snapshot name, such as candidate-5")
args = parser.parse_args()
if not re.fullmatch(r"candidate-[0-9]+", args.name):
    parser.error("Use candidate-N")
out = Path(__file__).resolve().parent
root = out.parents[4]
excluded = out.relative_to(root).as_posix() + "/"

def git(*arguments):
    return subprocess.run(
        ["git", "-c", "core.quotepath=false", *arguments], cwd=root,
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    ).stdout

for suffix in (".json", ".sha256"):
    if (out / (args.name + suffix)).exists():
        parser.error("Snapshot already exists; choose the next number")
paths = set()
for raw in (
    git("diff", "--name-only", "-z", "HEAD", "--", "skills/sohrab"),
    git("ls-files", "--others", "--exclude-standard", "-z", "--", "skills/sohrab"),
):
    paths.update(p for p in raw.decode("utf-8").split("\0") if p and not p.startswith(excluded))
previous = {}
if (out / "candidate.sha256").exists():
    previous = {p: h for h, p in (line.split("  ", 1) for line in
                (out / "candidate.sha256").read_text(encoding="utf-8").splitlines())}
current = {p: hashlib.sha256((root / p).read_bytes()).hexdigest() for p in sorted(paths)}
manifest = "".join(f"{h}  {p}\n" for p, h in current.items()).encode("utf-8")
record = {
    "head": git("rev-parse", "HEAD").decode().strip(),
    "branch": git("branch", "--show-current").decode().strip(),
    "files": len(current), "skills": len({p.split('/')[2] for p in current}),
    "manifest_sha256": hashlib.sha256(manifest).hexdigest(),
    "excluded": excluded.rstrip("/"),
    "selection": "git diff HEAD plus untracked source; sorted raw-byte SHA256 double-space path LF lines",
    "changed_from_previous": [p for p, h in current.items() if previous.get(p) != h],
    "missing_from_previous": sorted(previous.keys() - current.keys()),
    "publication": "uncommitted; staging preserved",
    "independent_gates": "Reconcile changed inputs before citing prior proof",
}
for name in (args.name, "candidate"):
    (out / (name + ".sha256")).write_bytes(manifest)
    (out / (name + ".json")).write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
print(json.dumps({k: record[k] for k in ("files", "skills", "manifest_sha256")}))
