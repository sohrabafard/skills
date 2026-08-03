#!/usr/bin/env python3
"""Structural validator for the alaa-cc-orchestrator pack.

Checks that every managed agent exists with a legal pin, that the skill and its
references agree with the agents on disk, and that no cross-runtime reference
has leaked into this pack. Run from anywhere; paths resolve against the pack root.
"""
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
AGENTS = ROOT / "agents"

REQUIRED = {
    "alaa-spec-analyst",
    "alaa-explorer",
    "alaa-researcher",
    "alaa-test-strategist",
    "alaa-implementer",
    "alaa-implementer-opus",
    "alaa-verifier",
    "alaa-failure-analyst",
    "alaa-reviewer",
    "alaa-adversarial-reviewer",
    "alaa-documenter",
    "alaa-architecture-critic",
    "alaa-security-reviewer",
    "alaa-migration-guardian",
    "alaa-api-contract-reviewer",
    "alaa-dependency-auditor",
    "alaa-accessibility-reviewer",
    "alaa-browser-qa",
    "alaa-performance-profiler",
    "alaa-observability-reviewer",
    "alaa-release-guardian",
}

VALID_MODEL = {"opus", "sonnet", "haiku", "inherit"}
VALID_EFFORT = {"low", "medium", "high", "xhigh", "max"}
# Sonnet's ceiling is `high`: above it, the correct move is a different model.
SONNET_CEILING = {"low", "medium", "high"}
# Cross-runtime isolation: this pack must never name the other runtime's world.
FORBIDDEN = re.compile(r"\b(codex|gpt-?5|openai|sol|terra|luna)\b|opus 4|fable", re.I)

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
    if "name: alaa-cc-orchestrator" not in fm:
        errors.append("SKILL.md name is not alaa-cc-orchestrator")

names: set[str] = set()
for path in sorted(AGENTS.glob("*.md")):
    text = path.read_text(encoding="utf-8")
    fm_match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not fm_match:
        errors.append(f"{path.name}: missing YAML frontmatter")
        continue
    fm = fm_match.group(1)

    def field(key: str) -> str | None:
        found = re.search(rf"^{key}:\s*(\S+)\s*$", fm, re.M)
        return found.group(1) if found else None

    name = field("name")
    if not name:
        errors.append(f"{path.name}: missing name")
    else:
        if name in names:
            errors.append(f"duplicate agent name: {name}")
        names.add(name)
        if path.stem != name:
            errors.append(f"{path.name}: filename should match name {name}")

    if "description:" not in fm:
        errors.append(f"{path.name}: missing description")

    model = field("model")
    effort = field("effort")
    if model not in VALID_MODEL:
        errors.append(f"{path.name}: invalid model {model!r}")
    if effort not in VALID_EFFORT:
        errors.append(f"{path.name}: invalid effort {effort!r}")
    if effort == "max":
        errors.append(f"{path.name}: 'max' is never a pin, only a per-invocation retry")
    if model == "sonnet" and effort not in SONNET_CEILING:
        errors.append(
            f"{path.name}: sonnet is capped at 'high'; a lane needing more changes model, not effort"
        )

    identity = re.search(r"AGENT:\s*(\S+)\s*\|\s*MODEL:\s*([^|]+?)\s*\|\s*EFFORT:\s*([a-z]+)", text)
    if not identity:
        errors.append(f"{path.name}: missing AGENT/MODEL/EFFORT identity line")
    else:
        id_name, id_model, id_effort = identity.groups()
        if name and id_name != name:
            errors.append(f"{path.name}: identity line names {id_name}, file declares {name}")
        if effort and id_effort != effort:
            errors.append(f"{path.name}: identity effort {id_effort} disagrees with pin {effort}")
        if model == "opus" and not id_model.lower().startswith("opus"):
            errors.append(f"{path.name}: identity model {id_model!r} disagrees with pin {model}")
        if model == "sonnet" and not id_model.lower().startswith("sonnet"):
            errors.append(f"{path.name}: identity model {id_model!r} disagrees with pin {model}")

missing = REQUIRED - names
extra = names - REQUIRED
if missing:
    errors.append(f"missing required agents: {sorted(missing)}")
if extra:
    errors.append(f"unexpected agents: {sorted(extra)}")

for rel in [
    "references/agent-catalog.md",
    "references/routing-matrix.md",
    "references/model-effort-policy.md",
    "references/delegation-prompts.md",
    "references/resource-policy.md",
    "references/failure-taxonomy.md",
    "references/verification-and-gates.md",
    "scripts/Invoke-AlaaLowPriority.ps1",
    "scripts/run-low-priority.sh",
    "VERSION",
]:
    if not (ROOT / rel).is_file():
        errors.append(f"missing file: {rel}")

catalog_path = ROOT / "references/agent-catalog.md"
routing_path = ROOT / "references/routing-matrix.md"
if catalog_path.is_file() and routing_path.is_file():
    catalog = catalog_path.read_text(encoding="utf-8")
    routing = routing_path.read_text(encoding="utf-8")
    for name in REQUIRED:
        if name not in catalog:
            errors.append(f"agent absent from catalog: {name}")
        if name not in skill and name not in routing:
            errors.append(f"agent absent from skill/routing: {name}")

resource_path = ROOT / "references/resource-policy.md"
if "--browser chromium" not in skill or (
    resource_path.is_file() and "--browser chromium" not in resource_path.read_text(encoding="utf-8")
):
    errors.append("hard browser chromium preservation rule is missing")

for path in sorted(ROOT.rglob("*")):
    if not path.is_file() or path.suffix not in {".md", ".yaml", ".py", ".sh", ".ps1"}:
        continue
    # The sweep's own pattern lives in this file, and CHANGELOG.md is a historical
    # record that must be able to name what a revision migrated away from. Neither
    # is ever loaded into an agent's context, so neither can leak at runtime.
    if path.name in {"validate_pack.py", "CHANGELOG.md"}:
        continue
    # A "When NOT to use" section exists to name the cases this pack does not
    # serve, and the other runtime is the first of them. Naming it there is the
    # section doing its job, so the sweep skips that section rather than forcing
    # the boundary to be stated in words that cannot say which runtime it means.
    section = ""
    for lineno, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if path.suffix == ".md" and line.startswith("## "):
            section = line[3:].strip().lower()
        if section == "when not to use":
            continue
        hit = FORBIDDEN.search(line)
        if hit:
            errors.append(f"cross-runtime leak in {path.relative_to(ROOT)}:{lineno}: {hit.group(0)!r}")

if errors:
    print("PACK VALIDATION FAILED", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print(f"PACK VALID: {len(names)} agents, skill version {(ROOT / 'VERSION').read_text().strip()}")
