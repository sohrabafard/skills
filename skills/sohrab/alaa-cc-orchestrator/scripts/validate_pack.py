#!/usr/bin/env python3
"""Structural validator for the alaa-cc-orchestrator pack.

Checks that every managed agent exists with a legal pin, that the skill and its
references agree with the agents on disk, and that no cross-runtime reference
has leaked into this pack. Run from anywhere; paths resolve against the pack root.
"""
from __future__ import annotations

from pathlib import Path
from check_agent_contracts import agent_failures, orchestrator_failures
from check_agent_grants import frontmatter
import argparse
import re
import subprocess
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
    "alaa-instruction-reviewer",
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

# Cross-runtime isolation: this pack must never name the other runtime's world.
FORBIDDEN = re.compile(r"\b(codex|gpt-?[56]|openai|sol|terra|luna|astra)\b|opus 4", re.I)

def validate() -> int:
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
        if "name: alaa-cc-orchestrator" not in fm:
            errors.append("SKILL.md name is not alaa-cc-orchestrator")

    names: set[str] = set()
    for path in sorted(AGENTS.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        frontmatter(str(path))  # Reject ambiguous or unsupported metadata, never skip it.
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

        errors.extend(f"{path.name}: {error}" for error in agent_failures(text))

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
        "scripts/check_agent_grants.py",
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
                errors.append(f"cross-runtime leak in {path.relative_to(ROOT)}:{lineno}: {hit.group(0)!r}")

    unavailable = False
    policy_check = ROOT.parent / "alaa-prompting-guide/scripts/check_claude_model_policy.py"
    for label, command in (
        ("canonical Claude policy", [sys.executable, "-B", str(policy_check), "--agent-root", str(AGENTS)]),
        ("agent grants", [sys.executable, "-B", str(ROOT / "scripts/check_agent_grants.py")]),
    ):
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        if result.returncode:
            unavailable |= result.returncode != 1
            detail = (result.stdout + result.stderr).strip().replace("\n", " | ")
            errors.append(f"{label} exited {result.returncode}: {detail}")

    if errors:
        print("PACK VALIDATION FAILED", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 2 if unavailable else 1

    print(f"PACK VALID: {len(names)} agents, skill version {(ROOT / 'VERSION').read_text().strip()}")
    return 0


def self_test() -> int:
    """Exercise consumer exit propagation; policy owns model/projection fixtures."""
    from unittest.mock import patch
    failures = []
    for policy_exit, grant_exit, expected in ((0, 0, 0), (1, 0, 1), (2, 0, 2), (0, 1, 1), (0, 2, 2), (9, 0, 2)):
        responses = [subprocess.CompletedProcess([], code, "fixture", "")
                     for code in (policy_exit, grant_exit)]
        with patch("subprocess.run", side_effect=responses):
            observed = validate()
        if observed != expected:
            failures.append(f"dependency exits {(policy_exit, grant_exit)}: {observed} != {expected}")
    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1
    print("PACK SELF-TEST OK: dependency findings and unavailable proof cannot pass")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        return self_test() if args.self_test else validate()
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"pack validation unavailable: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
