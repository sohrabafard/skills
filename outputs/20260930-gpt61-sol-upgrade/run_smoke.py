"""Run a fresh read-only CLI controller against three installed custom roles.

No model substitution, global configuration edits, installation or calibration.
Caller supplies the writable fixture/cache directory. Evidence is retained.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ROLES = {"alaa-spec-analyst": "medium", "alaa-reviewer": "high", "alaa-rule-writer": "medium"}


def portable(value: str, fixture_root: Path) -> str:
    sources = [(str(fixture_root), "<smoke-fixtures>"), (str(ROOT), "<repo>"), (str(Path.home()), "<user-home>")]
    powershell = shutil.which("pwsh")
    if powershell:
        sources.append((powershell, "<powershell>"))
    for source, replacement in sources:
        for spelling in (source, source.replace("\\", "/"), source.replace("\\", "\\\\"), source.replace("\\", "\\\\\\\\")):
            value = value.replace(spelling, replacement)
    return value


def portable_events(value: str, fixture_root: Path) -> str:
    records = []
    for line in value.splitlines():
        record = json.loads(line)
        item = record.get("item", {})
        if item.get("type") == "command_execution" and isinstance(item.get("command"), str):
            command = item["command"]
            item["command"] = f"[Native command retained outside Git; UTF-8 SHA256 {hashlib.sha256(command.encode()).hexdigest()}]"
        if item.get("type") == "command_execution" and isinstance(item.get("aggregated_output"), str):
            output = item["aggregated_output"]
            item["aggregated_output"] = f"[Native command output retained outside Git; UTF-8 SHA256 {hashlib.sha256(output.encode()).hexdigest()}]"
        records.append(portable(json.dumps(record, ensure_ascii=False), fixture_root))
    return "\n".join(records) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixtures", type=Path, required=True)
    parser.add_argument("--evidence-dir", type=Path, default=HERE)
    parser.add_argument("--persistent-controller", action="store_true", help="Persist the fresh controller so collaboration can resolve its thread")
    args = parser.parse_args()
    args.evidence_dir = args.evidence_dir.resolve()
    args.evidence_dir.mkdir(parents=True, exist_ok=True)
    args.fixtures.mkdir(parents=True, exist_ok=False)
    fixtures = {
        "requirements.txt": "The report export stays disabled until generation completes. A failed generation shows a retry action. Export writes one local CSV selected by the user. Sending email or messages is outside scope.\n",
        "invoice.py": "INVOICES = {1: {'tenant': 'alpha', 'amount': 10}, 2: {'tenant': 'beta', 'amount': 20}}\n\ndef invoice_for_tenant(invoice_id, tenant):\n    # Required contract: reject a different tenant before returning any invoice.\n    return INVOICES[invoice_id]\n",
    }
    for name, content in fixtures.items():
        (args.fixtures / name).write_text(content, encoding="utf-8")
    original = {name: hashlib.sha256((args.fixtures / name).read_bytes()).hexdigest() for name in fixtures}
    codex = shutil.which("codex")
    if not codex:
        print("BLOCKED: installed Codex CLI unavailable")
        return 2

    pins = {}
    import tomllib
    for role, effort in ROLES.items():
        definition = tomllib.loads((Path.home() / ".codex/agents" / f"{role}.toml").read_text(encoding="utf-8"))
        if definition["model"] != "gpt-6.1-sol" or definition["model_reasoning_effort"] != effort:
            print(f"BLOCKED: installed pin drift for {role}")
            return 2
        pins[role] = {"requested_model": "gpt-6.1-sol", "requested_effort": effort, "definition_sha256": hashlib.sha256((Path.home() / ".codex/agents" / f"{role}.toml").read_bytes()).hexdigest()}

    prompt = """Run the authorized custom-agent activation smoke. Do no implementation or installation. Use only the following THREE named installed custom roles, each exactly once. Their TOML model/effort pins are the configuration under test; do not override them or choose a substitute role/model. Do not delegate any additional work. The controller model intentionally differs from the target agent pins. If target selection fails, report BLOCKED and the exact host error; do not fix configuration or retry with another model. Native and MCP writes, network/app actions and unrelated reads are forbidden for all smoke lanes.

1. Dispatch alaa-spec-analyst on requirements.txt: extract checkable acceptance criteria, the email/messaging exclusion and material ambiguities. Read only that fixture. Preserve its role output contract.
2. Dispatch alaa-reviewer on invoice.py: review only its explicit tenant-ownership contract. Report the planted blocking authorization defect with file and line evidence, preserve its verdict-first findings/evidence/risks contract, and never fix it. Do not run application suites or inspect unrelated repositories.
3. Dispatch alaa-rule-writer using this envelope:
item_id: smoke-tenant-rule
artifact_type: rule or prompt
draft: When handling any request to read an invoice belonging to a tenant, make sure to reject any mismatch in tenant ownership before returning the invoice. You must never change data that belongs to another tenant. If you cannot establish ownership, stop.
immutable_behavior_and_decisions: Applies to tenant-scoped invoice reads; reject tenant mismatch before returning; never change another tenant's data; stop if ownership cannot be established. Preserve constraint force and scope; invent no policy.
required_sources_of_truth: the supplied draft and invariants; the installed prompting-guide doctrine required by its definition. No other sources.
output_mode: single

Wait for all dispatched agents. Return each child's complete output in a JSON object with keys role, activation_status, requested_model, requested_effort, observed_model, observed_effort, configuration_control_evidence, output, blocker. Requested pins are gpt-6.1-sol/medium, gpt-6.1-sol/high and gpt-6.1-sol/medium respectively. Observed identity is unknown unless reliable host evidence exposes it; self-report is not proof. Record dispatch identifiers and any host evidence of resolution separately. Do not declare quality benchmark superiority or calibration. Do not add commit messages for this read-only smoke.\n"""
    (args.evidence_dir / "smoke-prompt.txt").write_text(prompt, encoding="utf-8")
    version = subprocess.run([codex, "--version"], text=True, encoding="utf-8", errors="replace", capture_output=True, timeout=30)
    catalog = subprocess.run([codex, "debug", "models"], cwd=args.fixtures, text=True, encoding="utf-8", errors="replace", capture_output=True, timeout=45)
    try:
        models = json.loads(catalog.stdout).get("models", [])
        target = next((m for m in models if m.get("slug") == "gpt-6.1-sol"), None)
        catalog_record = {"exit_code": catalog.returncode, "target_present": target is not None, "target": target, "model_slugs": [m.get("slug") for m in models]}
    except (ValueError, AttributeError):
        catalog_record = {"exit_code": catalog.returncode, "target_present": None, "error": "catalog unreadable"}
    (args.evidence_dir / "cli-catalog.json").write_text(json.dumps(catalog_record, indent=2) + "\n", encoding="utf-8")
    command = [codex, "exec", "--model", "gpt-6-sol", "-c", 'model_reasoning_effort="low"', "--sandbox", "read-only", "--skip-git-repo-check", "--json", "--output-last-message", str(args.evidence_dir / "smoke-controller-output.txt"), "-"]
    if not args.persistent_controller:
        command.insert(8, "--ephemeral")
    started = time.monotonic()
    process = subprocess.Popen(command, cwd=args.fixtures, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8")
    try:
        stdout, stderr = process.communicate(prompt, timeout=600)
        code = process.returncode
    except subprocess.TimeoutExpired:
        process.kill()
        stdout, stderr = process.communicate()
        stderr += "\nController exceeded its 600-second bound; smoke incomplete."
        code = 2
    (args.fixtures / "raw-smoke-events.jsonl").write_text(stdout, encoding="utf-8")
    (args.fixtures / "raw-smoke-stderr.txt").write_text(stderr, encoding="utf-8")
    (args.evidence_dir / "smoke-events.jsonl").write_text(portable_events(stdout, args.fixtures), encoding="utf-8")
    (args.evidence_dir / "smoke-stderr.txt").write_text(portable(stderr, args.fixtures), encoding="utf-8")
    output_file = args.evidence_dir / "smoke-controller-output.txt"
    if output_file.exists():
        output_file.write_text(portable(output_file.read_text(encoding="utf-8"), args.fixtures), encoding="utf-8")
    unchanged = all(hashlib.sha256((args.fixtures / name).read_bytes()).hexdigest() == sha for name, sha in original.items())
    metadata = {"controller": {"model": "gpt-6-sol", "effort": "low", "ephemeral": not args.persistent_controller, "purpose": "Fresh-session orchestration only; not a fallback for target agents"}, "cli_version": version.stdout.strip(), "exit_code": code, "elapsed_seconds": round(time.monotonic() - started, 3), "pins": pins, "fixtures": original, "fixtures_unchanged": unchanged, "comparison_or_calibration": "unrun", "verdict": "requires evidence review", "served_identity": "unknown"}
    (args.evidence_dir / "smoke-execution.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(f"Smoke controller exit {code}; fixture preservation {unchanged}; inspect retained events and outputs. No pass inferred.")
    return 0 if code == 0 and unchanged else 2


if __name__ == "__main__":
    sys.exit(main())
