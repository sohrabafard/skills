"""Run source gates once per identified candidate and retain portable receipts."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
GUIDE = "skills/sohrab/alaa-prompting-guide"
PACK = "skills/sohrab/alaa-codex-orchestrator"


def source_snapshot() -> dict:
    records = []
    for prefix in (GUIDE, PACK):
        for path in sorted((ROOT / prefix).rglob("*")):
            if path.is_file() and "__pycache__" not in path.parts:
                records.append({"path": path.relative_to(ROOT).as_posix(), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    digest = hashlib.sha256(json.dumps(records, sort_keys=True).encode()).hexdigest()
    return {"head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(), "scoped_sha256": digest, "files": records}


def portable(text: str) -> str:
    for path, marker in ((ROOT, "<repo>"), (Path.home() / ".codex", "<user-codex>"), (Path.home(), "<user-home>")):
        text = text.replace(str(path), marker).replace(path.as_posix(), marker)
    return text


def main() -> int:
    py = [sys.executable, "-B"]
    gates = [
        ("preservation", py + [str(HERE / "verify_preservation.py")]),
        ("model-policy", py + [f"{GUIDE}/scripts/check_codex_model_policy.py", "--agent-root", f"{PACK}/agents", "--agent-root", f"{GUIDE}/assets/rule-writer/codex"]),
        ("model-policy-self-test", py + [f"{GUIDE}/scripts/check_codex_model_policy.py", "--self-test"]),
        ("eval-corpus", py + [f"{GUIDE}/scripts/check_agent_evals.py"]),
        ("eval-self-test", py + [f"{GUIDE}/scripts/check_agent_evals.py", "--self-test"]),
        ("rule-writer", py + [f"{GUIDE}/scripts/check_rule_writer_grants.py"]),
        ("renderer", py + [f"{PACK}/scripts/render_agents.py", "--check"]),
        ("agent-contracts", py + [f"{PACK}/scripts/check_agent_contracts.py"]),
        ("agent-grants", py + [f"{PACK}/scripts/check_agent_grants.py"]),
        ("orchestrator-pack", py + [f"{PACK}/scripts/validate_pack.py"]),
        ("skill-structure", py + ["scripts/validate_sohrab_skill_pack.py"]),
        ("skill-index", py + ["scripts/check_skill_index.py"]),
        ("fleet-references", py + ["scripts/check_fleet_references.py"]),
        ("lifecycle", py + ["scripts/check_lifecycle_contract.py"]),
        ("whitespace", ["git", "diff", "--check"]),
    ]
    before = source_snapshot()
    (HERE / "source-snapshot.json").write_text(json.dumps(before, indent=2) + "\n", encoding="utf-8")
    results = []
    for name, command in gates:
        start = time.monotonic()
        try:
            result = subprocess.run(command, cwd=ROOT, text=True, encoding="utf-8", errors="replace", capture_output=True, timeout=120)
            output = result.stdout + result.stderr
            code = result.returncode
        except subprocess.TimeoutExpired:
            output, code = "Gate exceeded its 120-second bound; unavailable proof.", 2
        output_path = HERE / f"gate-{name}.txt"
        output_path.write_text(portable(output), encoding="utf-8")
        row = {"gate": name, "command": portable(" ".join(command)).replace(str(Path(sys.executable)), "python"), "working_directory": "repository root", "exit_code": code, "elapsed_seconds": round(time.monotonic() - start, 3), "output": output_path.name, "scoped_sha256": before["scoped_sha256"]}
        results.append(row)
        (HERE / "gates.json").write_text(json.dumps({"snapshot": before["scoped_sha256"], "results": results}, indent=2) + "\n", encoding="utf-8")
        print(f"{name}: exit {code}", flush=True)
        if code:
            print(portable(output[-3000:]), flush=True)
            return 1
    after = source_snapshot()
    if before != after:
        print("FAIL: source changed during verification")
        return 1
    print(f"PASS: {len(results)} gates on unchanged source {before['scoped_sha256']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
