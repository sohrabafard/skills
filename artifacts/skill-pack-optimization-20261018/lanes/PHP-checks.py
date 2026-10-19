"""Bounded source acceptance for the PHP optimization lane; no runtime proof."""
from pathlib import Path
import hashlib
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
SKILLS = ["alaa-php-clean-code", "alaa-laravel-architecture",
          "alaa-laravel-upgrade-all-packages", "alaa-octane-performance",
          "alaa-async-messaging", "alaa-laravel-job-rabbitmq",
          "alaa-laravel-public-api-contract-pack"]
roots = [f"skills/sohrab/{name}" for name in SKILLS]
paths = sorted([p for root in roots for p in (ROOT / root).rglob("*") if p.is_file()]
               + [Path(__file__).resolve()])
digest = hashlib.sha256()
manifest = []
for path in paths:
    rel = path.relative_to(ROOT).as_posix()
    data = path.read_bytes()
    digest.update(rel.encode() + b"\0" + data)
    manifest.append({"path": rel, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)})
head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
changed = subprocess.check_output(["git", "diff", "--name-only", "--", *roots], cwd=ROOT, text=True).splitlines()
fleet = ["python", "-B", "scripts/check_fleet_references.py"]
for name in SKILLS:
    fleet.extend(["--skill", name])
snapshot = {"head": head, "manifest_sha256": digest.hexdigest(), "manifest": manifest,
            "changed": changed, "command": fleet, "observer": "PHP implementation lane",
            "cwd": ".", "resource_policy": "normal priority; sequential bounded static checks; no heavy checks"}
(OUT / "PHP-snapshot.json").write_text(json.dumps(snapshot, indent=2) + "\n", encoding="utf-8", newline="\n")
findings = []
link_count = 0
for name in changed:
    path = ROOT / name
    data = path.read_bytes()
    if data.startswith(b"\xef\xbb\xbf") or b"\r" in data:
        findings.append(f"encoding: {name}")
    text = data.decode("utf-8")
    if path.suffix == ".md":
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
            if re.match(r"[a-z]+:|#", target):
                continue
            target = target.split("#", 1)[0]
            if target:
                link_count += 1
                if not (path.parent / target).resolve().exists():
                    findings.append(f"link: {name}: {target}")
results = [{"check": "changed UTF-8-no-BOM/LF and relative Markdown links", "exit": int(bool(findings)),
            "files": len(changed), "links": link_count, "findings": findings}]
for command in [fleet, ["git", "diff", "--check", "--", *changed]]:
    proc = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    results.append({"command": command, "exit": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr})
(OUT / "PHP-checks.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8", newline="\n")
for result in results:
    print(json.dumps({key: value for key, value in result.items() if key not in ("stdout", "stderr")}, ensure_ascii=True))
    if result.get("exit"):
        print(result.get("stdout", ""), result.get("stderr", ""))
raise SystemExit(int(any(result["exit"] for result in results)))
