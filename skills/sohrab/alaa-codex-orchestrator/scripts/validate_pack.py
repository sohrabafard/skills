#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys

try:
    import tomllib
except ModuleNotFoundError:  # Python < 3.11
    try:
        import tomli as tomllib  # type: ignore
    except ModuleNotFoundError:
        tomllib = None


_SCALAR = re.compile(r'^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*"([^"]*)"\s*$', re.M)
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
    data.update({key: value for key, value in _SCALAR.findall(text)})
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
VALID_EFFORT = {"none", "low", "medium", "high", "xhigh", "max"}
VALID_MODEL = {"gpt-5.6-sol", "gpt-5.6-terra", "gpt-5.6-luna"}
# Cross-runtime isolation: this pack must never name another vendor's model family.
FORBIDDEN = re.compile(r"\b(claude|opus|sonnet|fable|haiku|anthropic)\b", re.I)

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
    if data.get("model_reasoning_effort") not in VALID_EFFORT:
        errors.append(f"{path.name}: invalid model_reasoning_effort {data.get('model_reasoning_effort')!r}")
    if data.get("model") not in VALID_MODEL:
        errors.append(f"{path.name}: invalid model {data.get('model')!r}")
    if data.get("model_reasoning_effort") == "max":
        errors.append(f"{path.name}: 'max' is never a pin, only a per-invocation retry")

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
    for lineno, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        hit = FORBIDDEN.search(line)
        if hit:
            rel = path.relative_to(ROOT)
            errors.append(f"cross-runtime leak in {rel}:{lineno}: {hit.group(0)!r}")

if errors:
    print("PACK VALIDATION FAILED", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print(f"PACK VALID: {len(names)} agents, skill version {(ROOT / 'VERSION').read_text().strip()}")
