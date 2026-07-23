#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys
import tomllib

ROOT = Path(__file__).resolve().parent.parent
AGENTS = ROOT / "agents"
REQUIRED = {
    "alaa-explorer",
    "alaa-researcher",
    "alaa-test-strategist",
    "alaa-implementer",
    "alaa-implementer-sol",
    "alaa-verifier",
    "alaa-failure-analyst",
    "alaa-reviewer",
    "alaa-architecture-critic",
    "alaa-security-reviewer",
    "alaa-migration-guardian",
    "alaa-browser-qa",
    "alaa-performance-profiler",
    "alaa-observability-reviewer",
    "alaa-release-guardian",
    "alaa-documenter",
}
VALID_SANDBOX = {"read-only", "workspace-write", "danger-full-access"}
VALID_EFFORT = {"minimal", "low", "medium", "high", "xhigh"}

errors: list[str] = []

skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
match = re.match(r"^---\n(.*?)\n---\n", skill, re.S)
if not match:
    errors.append("SKILL.md is missing YAML frontmatter")
else:
    fm = match.group(1)
    for key in ("name:", "description:"):
        if key not in fm:
            errors.append(f"SKILL.md frontmatter missing {key}")
    if "name: alaa-codex-orchestrator" not in fm:
        errors.append("SKILL.md name is not alaa-codex-orchestrator")

names: set[str] = set()
for path in sorted(AGENTS.glob("*.toml")):
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{path.name}: invalid TOML: {exc}")
        continue
    for key in ("name", "description", "developer_instructions"):
        if not isinstance(data.get(key), str) or not data[key].strip():
            errors.append(f"{path.name}: missing/non-string {key}")
    name = data.get("name")
    if isinstance(name, str):
        if name in names:
            errors.append(f"duplicate agent name: {name}")
        names.add(name)
        if path.stem != name:
            errors.append(f"{path.name}: filename should match name {name}")
    if data.get("sandbox_mode") not in VALID_SANDBOX:
        errors.append(f"{path.name}: invalid sandbox_mode {data.get('sandbox_mode')!r}")
    if data.get("model_reasoning_effort") not in VALID_EFFORT:
        errors.append(f"{path.name}: invalid model_reasoning_effort {data.get('model_reasoning_effort')!r}")

missing = REQUIRED - names
extra = names - REQUIRED
if missing:
    errors.append(f"missing required agents: {sorted(missing)}")
if extra:
    errors.append(f"unexpected agents: {sorted(extra)}")

for rel in [
    "references/agent-catalog.md",
    "references/routing-matrix.md",
    "references/delegation-prompts.md",
    "references/resource-policy.md",
    "references/failure-taxonomy.md",
    "references/verification-and-gates.md",
    "references/installation.md",
    "scripts/Install-AlaaCodexAgents.ps1",
    "scripts/Install-AlaaCodexOrchestrator.ps1",
    "scripts/Get-AlaaCodexAgentStatus.ps1",
    "scripts/Invoke-AlaaLowPriority.ps1",
    "scripts/install-agents.sh",
    "scripts/install-skill.sh",
    "scripts/run-low-priority.sh",
    "agents/openai.yaml",
    "README-fa.md",
    "VERSION",
]:
    if not (ROOT / rel).is_file():
        errors.append(f"missing file: {rel}")

catalog = (ROOT / "references/agent-catalog.md").read_text(encoding="utf-8")
routing = (ROOT / "references/routing-matrix.md").read_text(encoding="utf-8")
for name in REQUIRED:
    if name not in catalog:
        errors.append(f"agent absent from catalog: {name}")
    if name not in skill and name not in routing:
        errors.append(f"agent absent from skill/routing: {name}")

if "--browser chromium" not in skill or "--browser chromium" not in (ROOT / "references/resource-policy.md").read_text(encoding="utf-8"):
    errors.append("hard browser chromium preservation rule is missing")

if errors:
    print("PACK VALIDATION FAILED", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print(f"PACK VALID: {len(names)} agents, skill version {(ROOT / 'VERSION').read_text().strip()}")
