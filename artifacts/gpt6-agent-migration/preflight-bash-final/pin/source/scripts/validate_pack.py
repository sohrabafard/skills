#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from check_agent_contracts import agent_failures, orchestrator_failures
from render_agents import policy_api, expected_outputs, drift
import re
import subprocess
import sys

try:
    import tomllib
except ModuleNotFoundError:  # Python < 3.11
    try:
        import tomli as tomllib  # type: ignore
    except ModuleNotFoundError:
        tomllib = None


_SCALAR = re.compile(r'^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*("(?:[^"\\\n]|\\.)*")\s*$', re.M)
_BLOCK = re.compile(r'^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*"""(.*?)"""', re.M | re.S)


def parse_toml(text: str) -> dict:
    """Parse this pack's agent TOMLs without tomllib.

    The agent files use only top-level string scalars plus one triple-quoted
    block, so a regex reader is sufficient and keeps the validator runnable on
    interpreters older than 3.11.
    """
    if tomllib is not None:
        return tomllib.loads(text)
    data = {key: value for key, value in _BLOCK.findall(text)}
    data.update({key: json.loads(value) for key, value in _SCALAR.findall(text)})
    return data

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
    "alaa-reviewer-deep",
    "alaa-instruction-reviewer",
    "alaa-architecture-critic",
    "alaa-security-reviewer",
    "alaa-migration-guardian",
    "alaa-browser-qa",
    "alaa-performance-profiler",
    "alaa-observability-reviewer",
    "alaa-release-guardian",
    "alaa-documenter",
    "alaa-spec-analyst",
    "alaa-adversarial-reviewer",
    "alaa-api-contract-reviewer",
    "alaa-dependency-auditor",
    "alaa-accessibility-reviewer",
}
VALID_SANDBOX = {"read-only", "workspace-write", "danger-full-access"}
# Cross-runtime isolation: this pack must never name another vendor's model family.
FORBIDDEN = re.compile(r"\b(claude|opus|sonnet|fable|haiku|anthropic)\b", re.I)

parser = argparse.ArgumentParser(description="Validate agent pins, grants, contracts, and generated artifacts")
parser.add_argument("--policy-root", type=Path)
args = parser.parse_args()
try:
    policy_module, policy = policy_api(args.policy_root)
except (OSError, ValueError) as exc:
    print(f"canonical policy unavailable: {exc}", file=sys.stderr)
    raise SystemExit(2)

errors: list[str] = []

skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
errors.extend(orchestrator_failures(skill))
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
        data = parse_toml(path.read_text(encoding="utf-8"))
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
    errors.extend(f"{path.name}: {error}" for error in policy_module.validate_agent_pin(data, policy))
    body = data.get("developer_instructions", "")
    errors.extend(f"{path.name}: {error}" for error in agent_failures(body))

missing = REQUIRED - names
extra = names - REQUIRED
if missing:
    errors.append(f"missing required agents: {sorted(missing)}")
if extra:
    errors.append(f"unexpected agents: {sorted(extra)}")

for rel in [
    "references/agent-catalog.md",
    "references/model-effort-policy.md",
    "references/routing-matrix.md",
    "references/delegation-prompts.md",
    "references/resource-policy.md",
    "references/failure-taxonomy.md",
    "references/verification-and-gates.md",
    "references/installation.md",
    "scripts/Install-AlaaCodexAgents.ps1",
    "scripts/Install-AlaaCodexOrchestrator.ps1",
    "scripts/Get-AlaaCodexAgentStatus.ps1",
    "scripts/check_agent_grants.py",
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

for path in sorted(ROOT.rglob("*")):
    if not path.is_file() or path.suffix not in {".md", ".toml", ".yaml", ".py", ".sh", ".ps1"}:
        continue
    # The sweep's own pattern lives in this file, and CHANGELOG.md is a historical
    # record that must be able to name what a revision migrated away from. Neither
    # is ever loaded into an agent's context, so neither can leak at runtime.
    if path.name in {"validate_pack.py", "CHANGELOG.md"}:
        continue
    # One line may name the other runtime: the negative-routing sentence inside
    # "When NOT to use", whose entire job is to say which runtime this pack does
    # not serve. Exempting the whole section would blind the sweep to anything
    # else later placed there, so the exemption is scoped to that one line shape
    # and still requires the line to route the reader elsewhere.
    negative_route = re.compile(
        r"^\s*[-*]\s+The runtime is .+ rather than .+\.", re.IGNORECASE)
    section = ""
    for lineno, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if path.suffix == ".md" and line.startswith("## "):
            section = line[3:].strip().lower()
        if section == "when not to use" and negative_route.match(line):
            continue
        hit = FORBIDDEN.search(line)
        if hit:
            rel = path.relative_to(ROOT)
            errors.append(f"cross-runtime leak in {rel}:{lineno}: {hit.group(0)!r}")

grant_check = subprocess.run(
    [sys.executable, str(ROOT / "scripts" / "check_agent_grants.py")],
    capture_output=True,
    text=True,
    check=False,
)
if grant_check.returncode != 0:
    detail = (grant_check.stdout + grant_check.stderr).strip().replace("\n", " | ")
    errors.append(
        f"agent grant checker exited {grant_check.returncode}"
        + (f": {detail}" if detail else "")
    )

try:
    for path in drift(expected_outputs(ROOT, policy)):
        errors.append(f"generated drift: {path.relative_to(ROOT)}; run scripts/render_agents.py --write")
except (OSError, ValueError, KeyError) as exc:
    print(f"generated artifacts could not be checked: {exc}", file=sys.stderr)
    raise SystemExit(2)

if errors:
    print("PACK VALIDATION FAILED", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print(f"PACK VALID: {len(names)} agents, skill version {(ROOT / 'VERSION').read_text().strip()}")
