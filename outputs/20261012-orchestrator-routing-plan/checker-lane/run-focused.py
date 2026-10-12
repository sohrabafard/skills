"""Retain exact focused static gate evidence; no aggregate/root/inference checks."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

repo = Path.cwd()
artifact = repo / "outputs/20261012-orchestrator-routing-plan/checker-lane"
owner = repo / "skills/sohrab/alaa-prompting-guide"
commands = [
    (owner, ["scripts/check_codex_model_policy.py", "--self-test"]),
    (owner, ["scripts/check_agent_evals.py", "--self-test"]),
    (owner, ["scripts/check_agent_evals.py"]),
    (owner, ["scripts/check_agent_evals.py", "--history-manifest", "assets/evals/history/20261009/manifest.json"]),
    (owner, ["scripts/check_allocation_evals.py", "--self-test"]),
    (owner, ["scripts/check_allocation_evals.py"]),
    (repo / "skills/sohrab/alaa-codex-orchestrator", ["scripts/check_agent_contracts.py", "--self-test"]),
    (repo / "skills/sohrab/alaa-cc-orchestrator", ["scripts/check_agent_contracts.py", "--self-test"]),
]
selection = [int(index) for index in sys.argv[1:]] or list(range(len(commands)))
results_path = artifact / "focused-results.jsonl"
environment = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
for index in selection:
    cwd, arguments = commands[index]
    result = subprocess.run([sys.executable, *arguments], cwd=cwd, env=environment, capture_output=True, text=True, timeout=120)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    log = artifact / f"focused-{index}-{stamp}.log"
    log.write_text(result.stdout + result.stderr, encoding="utf-8")
    record = {"command": "python " + " ".join(arguments), "cwd": cwd.relative_to(repo).as_posix(), "exit": result.returncode,
              "resource_policy": "sequential ordinary static Python; timeout 120 seconds; PYTHONDONTWRITEBYTECODE=1",
              "timestamp": stamp, "proof": "static/unit checker fixtures only", "tier": "focused", "log": log.relative_to(repo).as_posix()}
    with results_path.open("a", encoding="utf-8") as output:
        output.write(json.dumps(record) + "\n")
    print(index, result.returncode, (result.stdout + result.stderr).strip()[:1600])
    if result.returncode:
        break
