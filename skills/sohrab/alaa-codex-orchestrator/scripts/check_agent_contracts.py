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
                     "Do not implement product changes",
                     "alaa-workflow references/artifact-lifecycle.md",
                     "Plan-only work grants no product execution, branch, or commit authority",
                     "report saved plan/checkpoint paths when admitted",
                     "Commit only with explicit user authorization",
                     "local-only completion requires no merge prompt",
                     "Independent verification and review inspect the actual artifact",
                     "Retain required retrieval, focused implementer checks and independent acceptance gates",
                     "Do not infer a universal watchdog timeout"):
        if required not in text:
            errors.append(f"missing authority contract: {required}")
    for forbidden in ("On activation, idempotently installs", "Auto-install authority",
                      "Commit on the run's own work branch at each completed subtask",
                      "continue with general-purpose subagents",
                      "Every profile runs all six phases",
                      "**Do not add verification instructions.**",
                      "A watchdog ends a lane on silence rather than on duration",
                      "Do not edit repository files, and do not create workflow artifacts",
                      "Do not edit files or imply implementation occurred",
                      "Advisor mode runs none of them: Phases A, B, and F"):
        if forbidden in text:
            errors.append(f"retired authority/fallback contract: {forbidden}")
    return errors


def dispatch_failures(text: str) -> list[str]:
    errors = []
    for required in ("<skills>", "exact names, sources, activation conditions, and absence actions",
                     "alaa-workflow references/companion-routing.md"):
        if required not in text:
            errors.append(f"missing dispatch skill bindings: {required}")
    if "<progress>report meaningful progress under the active host contract" not in text:
        errors.append("missing host-specific dispatch progress contract")
    if "Do not infer a universal watchdog timeout" not in text:
        errors.append("missing watchdog evidence boundary in dispatch")
    for retired in ("emit one line between steps", "a stream watchdog can kill it mid-run"):
        if retired in text:
            errors.append(f"retired dispatch progress claim: {retired}")
    return errors


def planning_failures(gates: str, implementation: str) -> list[str]:
    errors = []
    for required in ("resolved skill bindings under `alaa-workflow references/companion-routing.md`",
                     "executable phase/task skill bindings before implementation or write-lane dispatch"):
        if required not in gates:
            errors.append(f"missing plan/lane skill bindings: {required}")
    blocks = re.findall(r"```xml\s*\n(.*?)```", implementation, re.S)
    if not blocks:
        errors.append("missing implementation dispatch template")
    for index, block in enumerate(blocks, 1):
        if "<skills>" not in block or "resolved lane bindings" not in block:
            errors.append(f"implementation template {index}: missing resolved skill bindings")
        if "<clean_code_skill>" in block:
            errors.append(f"implementation template {index}: clean-code-only skill routing")
    return errors


def self_test() -> int:
    good = (ROOT / "agents" / next(iter(sorted(
        path.name for path in (ROOT / "agents").glob("alaa-instruction-reviewer.*"))))).read_text(encoding="utf-8")
    # A source definition contains the same contract whether represented as a
    # multiline body or a serialized scalar; these checks do not execute it.
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    dispatch = (ROOT / "references/delegation-prompts.md").read_text(encoding="utf-8")
    gates = (ROOT / "references/verification-and-gates.md").read_text(encoding="utf-8")
    implementation = (ROOT / "references/delegation-prompts/30-implementation.md").read_text(encoding="utf-8")
    cases = [
        ("valid identity and authority", not agent_failures(good)),
        ("host-specific dispatch progress", not dispatch_failures(dispatch)),
        ("dispatch missing progress rejected", bool(dispatch_failures(dispatch.replace("<progress>report meaningful progress under the active host contract", "<progress>silent")))),
        ("per-command narration rejected", bool(dispatch_failures(dispatch + "\nemit one line between steps"))),
        ("dispatch watchdog claim rejected", bool(dispatch_failures(dispatch + "\na stream watchdog can kill it mid-run"))),
        ("unknown observation required", bool(agent_failures(good.replace("otherwise unknown", "use the pin")))),
        ("identity assertion rejected", bool(agent_failures(good + "\nAGENT: fixture | MODEL: configured | EFFORT: high"))),
        ("verdict first", bool(agent_failures(good + "\nIdentity line: begin the report"))),
        ("effective permissions required", bool(agent_failures(good.replace("parent overrides", "declaration")))),
        ("advisory and authority accepted", not orchestrator_failures(skill)),
        ("plan-only execution boundary required", bool(orchestrator_failures(skill.replace("Plan-only work grants no product execution, branch, or commit authority", "Plan means execute")))),
        ("workflow admission owner required", bool(orchestrator_failures(skill.replace("alaa-workflow references/artifact-lifecycle.md", "Unowned admission")))),
        ("saved-plan report required", bool(orchestrator_failures(skill.replace("report saved plan/checkpoint paths when admitted", "Plans are chat-only")))),
        ("blanket advisor no-files rejected", bool(orchestrator_failures(skill + "\nDo not edit repository files, and do not create workflow artifacts"))),
        ("advisor output no-files rejected", bool(orchestrator_failures(skill + "\nDo not edit files or imply implementation occurred"))),
        ("blanket phase-write rationale rejected", bool(orchestrator_failures(skill + "\nAdvisor mode runs none of them: Phases A, B, and F"))),
        ("complete lane bindings accepted", not planning_failures(gates, implementation)),
        ("lane bindings omitted rejected", bool(planning_failures(gates.replace("resolved skill bindings under `alaa-workflow references/companion-routing.md`", "clean code only"), implementation))),
        ("phase bindings omitted rejected", bool(planning_failures(gates.replace("executable phase/task skill bindings before implementation or write-lane dispatch", "implicit skills"), implementation))),
        ("implementation bindings omitted rejected", bool(planning_failures(gates, implementation.replace("<skills>", "<omitted>", 1)))),
        ("clean-code-only implementation rejected", bool(planning_failures(gates, implementation.replace("<skills>", "<clean_code_skill>", 1)))),
        ("dispatch bindings omitted rejected", bool(dispatch_failures(dispatch.replace("<skills>", "<omitted>")))),
        ("dispatch binding owner omitted rejected", bool(dispatch_failures(dispatch.replace("alaa-workflow references/companion-routing.md", "implicit owner")))),
        ("activation install rejected", bool(orchestrator_failures(skill + "\nOn activation, idempotently installs"))),
        ("implicit commit rejected", bool(orchestrator_failures(skill + "\nCommit on the run's own work branch at each completed subtask"))),
        ("forced integration rejected", bool(orchestrator_failures(skill + "\nEvery profile runs all six phases"))),
        ("independent review preserved", bool(orchestrator_failures(skill.replace("Independent verification and review inspect the actual artifact", "Check summaries")))),
        ("silent fallback rejected", bool(orchestrator_failures(skill + "\ncontinue with general-purpose subagents"))),
        ("focused checks preserved", bool(orchestrator_failures(skill.replace("Retain required retrieval, focused implementer checks and independent acceptance gates", "Omit checks")))),
        ("blanket no-verification rejected", bool(orchestrator_failures(skill + "\n**Do not add verification instructions.**"))),
        ("invented watchdog rejected", bool(orchestrator_failures(skill + "\nA watchdog ends a lane on silence rather than on duration"))),
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
        errors.extend(dispatch_failures((ROOT / "references/delegation-prompts.md").read_text(encoding="utf-8")))
        errors.extend(planning_failures(
            (ROOT / "references/verification-and-gates.md").read_text(encoding="utf-8"),
            (ROOT / "references/delegation-prompts/30-implementation.md").read_text(encoding="utf-8")))
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
