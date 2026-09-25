#!/usr/bin/env python3
"""Structural instruction-contract regression checks, not live behavior proof.

Exit 0 clean, 1 findings, 2 unavailable input. --self-test rejects known regressions.
"""
from __future__ import annotations
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent


def agent_failures(text: str) -> list[str]:
    errors = []
    for required in ("CONFIGURED", "REQUESTED", "OBSERVED", "otherwise unknown",
                     "Never infer observed identity from a pin or request",
                     "Report metadata after the verdict/status or opening outcome",
                     "Effective authority:", "parent overrides", "tool/MCP grants"):
        if required not in text:
            errors.append(f"missing metadata/authority contract: {required}")
    if "Identity line: begin" in text:
        errors.append("identity-first contradicts verdict/outcome-first")
    if re.search(r"AGENT:.*\| MODEL:.*\| EFFORT:", text):
        errors.append("configured identity presented as runtime assertion")
    return errors


def orchestrator_failures(text: str) -> list[str]:
    errors = []
    for required in ("Activation grants no installation or update authority",
                     "Never silently substitute a model or a generic role",
                     "Do not edit repository files, and do not create workflow artifacts",
                     "Commit only with explicit user authorization",
                     "local-only completion requires no merge prompt",
                     "Independent verification and review inspect the actual artifact"):
        if required not in text:
            errors.append(f"missing authority contract: {required}")
    for forbidden in ("On activation, idempotently installs", "Auto-install authority",
                      "Commit on the run's own work branch at each completed subtask",
                      "continue with general-purpose subagents",
                      "Every profile runs all six phases"):
        if forbidden in text:
            errors.append(f"retired authority/fallback contract: {forbidden}")
    return errors


def self_test() -> int:
    good = (ROOT / "agents" / next(iter(sorted(
        path.name for path in (ROOT / "agents").glob("alaa-instruction-reviewer.*"))))).read_text(encoding="utf-8")
    # A source definition contains the same contract whether represented as a
    # multiline body or a serialized scalar; these checks do not execute it.
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    cases = [
        ("valid identity and authority", not agent_failures(good)),
        ("unknown observation required", bool(agent_failures(good.replace("otherwise unknown", "use the pin")))),
        ("identity assertion rejected", bool(agent_failures(good + "\nAGENT: fixture | MODEL: configured | EFFORT: high"))),
        ("verdict first", bool(agent_failures(good + "\nIdentity line: begin the report"))),
        ("effective permissions required", bool(agent_failures(good.replace("parent overrides", "declaration")))),
        ("advisory and authority accepted", not orchestrator_failures(skill)),
        ("activation install rejected", bool(orchestrator_failures(skill + "\nOn activation, idempotently installs"))),
        ("implicit commit rejected", bool(orchestrator_failures(skill + "\nCommit on the run's own work branch at each completed subtask"))),
        ("forced integration rejected", bool(orchestrator_failures(skill + "\nEvery profile runs all six phases"))),
        ("independent review preserved", bool(orchestrator_failures(skill.replace("Independent verification and review inspect the actual artifact", "Check summaries")))),
        ("silent fallback rejected", bool(orchestrator_failures(skill + "\ncontinue with general-purpose subagents"))),
    ]
    for label, passed in cases:
        if not passed:
            print(f"SELF-TEST FAILED: {label}", file=sys.stderr)
    if not all(passed for _, passed in cases):
        return 1
    print(f"CONTRACT SELF-TEST OK: {len(cases)} positive/negative structural fixtures")
    return 0


def main() -> int:
    try:
        if sys.argv[1:] == ["--self-test"]:
            return self_test()
        if sys.argv[1:]:
            print("usage: check_agent_contracts.py [--self-test]", file=sys.stderr)
            return 2
        errors = orchestrator_failures((ROOT / "SKILL.md").read_text(encoding="utf-8"))
        for path in sorted((ROOT / "agents").glob("alaa-*")):
            if path.suffix in {".toml", ".md"}:
                errors.extend(f"{path.name}: {item}" for item in agent_failures(path.read_text(encoding="utf-8")))
        if errors:
            print("\n".join(errors), file=sys.stderr)
            return 1
        print("CONTRACT CHECK OK: metadata and authority source requirements")
        return 0
    except (OSError, ValueError, StopIteration) as exc:
        print(f"contract check unavailable: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
