"""Run the parent's bounded PLATFORM prose checks and preserve exact evidence."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
root = Path.cwd()
lane = Path("artifacts/skill-pack-optimization-20261018/lanes")
skills = ["caas-arvan-kuber", "alaa-docker-production", "alaa-haproxy",
          "alaa-haproxy-lua", "alaa-k8s-helm", "alaa-gitlab-ci-cd",
          "ansible-generator", "ansible-validator"]
roots = [f"skills/sohrab/{name}" for name in skills]
changed = subprocess.check_output(
    ["git", "diff", "--name-only", "--", *roots], text=True, encoding="utf-8"
).splitlines()
assert len(changed) == 23, changed
assert all(Path(name).suffix == ".md" for name in changed)
assert not any("/caas-arvan-kuber/" in n or "/ansible-validator/" in n for n in changed)
evidence = [lane / "PLATFORM.md", lane / "PLATFORM-draft.md",
            lane / "PLATFORM-read-manifest.json", lane / "PLATFORM-verify.py"]
paths = sorted(changed + [p.as_posix() for p in evidence])
for name in paths:
    p = Path(name)
    p.write_text(p.read_text(encoding="utf-8"), encoding="utf-8", newline="\n")

digest = hashlib.sha256()
inputs = []
for name in paths:
    data = Path(name).read_bytes()
    data.decode("utf-8")
    assert not data.startswith(b"\xef\xbb\xbf"), name
    assert b"\r" not in data, name
    digest.update(name.encode("utf-8") + b"\0" + data)
    inputs.append({"path": name, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
report = {
    "head": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
    "resource_policy": "ordinary serial low-cost; no CPU-heavy or live checks",
    "cwd": ".",
    "manifest_algorithm": "SHA256 of sorted repository-relative UTF8 path + NUL + raw bytes",
    "manifest_sha256": digest.hexdigest(),
    "inputs": inputs,
    "commands": [],
    "unrun": ["product/parser/runtime/self-test suites: no covered executable input changed",
              "live cluster, runner provisioning, deploy, installs: outside authority",
              "full-pack aggregate and independent review: parent Phase 4"],
}
commands = [
    ["python", "-B", "scripts/check_fleet_references.py",
     *[arg for name in skills for arg in ("--skill", name)]],
    ["python", "-B", "skills/sohrab/alaa-repo-docs/scripts/check_markdown_links.py",
     ".", "--files", *[n for n in paths if n.endswith(".md")]],
    ["git", "diff", "--check", "--", *paths],
]
for command in commands:
    result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
    report["commands"].append({"argv": command, "cwd": ".", "exit_code": result.returncode,
                               "stdout": result.stdout, "stderr": result.stderr})
    print(command[2] if command[0] == "python" else "git diff --check",
          "exit", result.returncode)
    print(result.stdout + result.stderr)
    if result.returncode:
        break
output = lane / "PLATFORM-verification.json"
output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n",
                  encoding="utf-8", newline="\n")
print("manifest", report["manifest_sha256"], "inputs", len(inputs))
sys.exit(0 if len(report["commands"]) == 3 and all(
    c["exit_code"] == 0 for c in report["commands"]) else 1)
