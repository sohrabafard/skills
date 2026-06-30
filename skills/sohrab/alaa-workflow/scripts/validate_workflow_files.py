#!/usr/bin/env python3
"""Validate Alaa workflow plan/state/phase-prompt artifacts quickly."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Iterable

REQUIRED_PARENT_PLAN_HEADINGS = [
    "## Summary",
    "## Goal",
    "## Assumptions",
    "## Constraints",
    "## Closest existing patterns",
    "## Phases (with dependencies)",
    "## Parallel-safe work split",
    "## Commands to run",
    "## Phase prompt pack",
    "## Files touched (append-only log)",
    "## Done / Remaining",
    "## Draft-to-final rewrite record",
]

REQUIRED_LANE_PLAN_HEADINGS = [
    "## Summary",
    "## Goal",
    "## Assumptions",
    "## Constraints",
    "## Closest existing patterns",
    "## Phases (with dependencies)",
    "## Parallel-safe work split",
    "## Commands to run",
    "## Files touched (append-only log)",
    "## Done / Remaining",
    "## Draft-to-final rewrite record",
]

REQUIRED_PHASE_PROMPT_HEADINGS = [
    "## Summary",
    "## How to run this cadence",
    "## Standing rules for every phase prompt",
    "## Phase prompts",
    "## Cross-phase review cadence",
    "## Draft-to-final rewrite record",
]

REQUIRED_STATE_KEYS = [
    "task_id",
    "task",
    "mode",
    "status",
    "created_at",
    "updated_at",
    "plan_path",
    "phase_prompts_path",
    "continuation_state_path",
    "state_path",
    "lanes",
    "handoff",
]


def newest_file(candidates: Iterable[Path]) -> Path | None:
    files = [path for path in candidates if path.exists()]
    if not files:
        return None
    return max(files, key=lambda path: path.stat().st_mtime)


def resolve_auto_plan() -> Path | None:
    plans = list(Path("docs/_agent_plans").glob("*.md")) + list(Path("docs/plan").glob("*.md"))
    plans = [p for p in plans if not p.name.endswith("__phase-prompts.md")]
    return newest_file(plans)


def resolve_auto_state() -> Path | None:
    return newest_file(Path(".codex/state").glob("*.json"))


def resolve_auto_phase_prompts(plan_path: Path | None) -> Path | None:
    if plan_path is not None:
        candidate = plan_path.with_name(f"{plan_path.stem}__phase-prompts.md")
        if candidate.exists():
            return candidate
    prompts = list(Path("docs/_agent_plans").glob("*__phase-prompts.md")) + list(Path("docs/plan").glob("*__phase-prompts.md"))
    return newest_file(prompts)


def resolve_auto_continuation(plan_path: Path | None) -> Path | None:
    if plan_path is not None:
        candidate = Path("docs/agents") / f"{plan_path.stem}-state.md"
        if candidate.exists():
            return candidate
    return newest_file(Path("docs/agents").glob("*-state.md"))


def validate_plan(path: Path) -> list[str]:
    errors: list[str] = []
    warnings: list[str] = []
    content = path.read_text(encoding="utf-8")

    is_lane_plan = content.lstrip().startswith("# Lane Plan")
    required_headings = REQUIRED_LANE_PLAN_HEADINGS if is_lane_plan else REQUIRED_PARENT_PLAN_HEADINGS

    for heading in required_headings:
        if heading not in content:
            errors.append(f"missing required heading: {heading}")

    if "{{" in content or "}}" in content:
        warnings.append("template placeholders appear to still be present")

    if not re.search(r"\n\s*- \[[ xX-]\] ", content):
        errors.append("no Markdown checkbox checklist items found")

    phase_section = content.split("## Phases (with dependencies)", 1)[1] if "## Phases (with dependencies)" in content else ""
    if "Mandatory skills:" not in phase_section:
        errors.append("phase section does not list mandatory skills")
    if "Test-first checklist:" not in phase_section:
        errors.append("phase section does not include a test-first checklist")
    if "Validation checklist:" not in phase_section:
        errors.append("phase section does not include a validation checklist")
    if not is_lane_plan and ("Final Phase" not in phase_section or "Documentation alignment" not in phase_section):
        errors.append("final documentation alignment phase not found")

    if not is_lane_plan:
        expected_phase_prompts = path.with_name(f"{path.stem}__phase-prompts.md")
        if expected_phase_prompts.exists():
            if str(expected_phase_prompts).replace("\\", "/") not in content and expected_phase_prompts.name not in content:
                warnings.append(f"expected phase prompt path exists but is not referenced: {expected_phase_prompts}")
        else:
            errors.append(f"missing same-stem phase prompt pack: {expected_phase_prompts}")

    expected_continuation = Path("docs/agents") / f"{path.stem}-state.md"
    if not expected_continuation.exists():
        warnings.append(f"expected continuation state file not found: {expected_continuation}")

    return [f"ERROR {msg}" for msg in errors] + [f"WARN {msg}" for msg in warnings]


def validate_phase_prompts(path: Path, plan_path: Path | None = None) -> list[str]:
    errors: list[str] = []
    warnings: list[str] = []
    content = path.read_text(encoding="utf-8")

    for heading in REQUIRED_PHASE_PROMPT_HEADINGS:
        if heading not in content:
            errors.append(f"missing required heading: {heading}")

    for needle in ["/goal", "Claude Opus", "GPT-5.5", "Mandatory skills", "Fix-loop", "subagents"]:
        if needle.lower() not in content.lower():
            errors.append(f"phase prompt pack missing required concept: {needle}")

    if "{{" in content or "}}" in content:
        warnings.append("template placeholders appear to still be present")

    if plan_path and plan_path.name not in content and str(plan_path).replace("\\", "/") not in content:
        warnings.append(f"phase prompt pack does not reference plan path: {plan_path}")

    return [f"ERROR {msg}" for msg in errors] + [f"WARN {msg}" for msg in warnings]


def validate_continuation(path: Path, plan_path: Path | None = None) -> list[str]:
    errors: list[str] = []
    warnings: list[str] = []
    content = path.read_text(encoding="utf-8")

    for heading in ["## Resume protocol", "## Current summary", "## Validation evidence", "## Handoff"]:
        if heading not in content:
            errors.append(f"missing required heading: {heading}")

    if plan_path and plan_path.name not in content and str(plan_path).replace("\\", "/") not in content:
        warnings.append(f"continuation state does not reference plan path: {plan_path}")

    if "main plan" not in content.lower():
        errors.append("continuation state does not explicitly require reading the main plan")

    return [f"ERROR {msg}" for msg in errors] + [f"WARN {msg}" for msg in warnings]


def validate_state(path: Path) -> list[str]:
    messages: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"ERROR invalid JSON: {exc}"]

    if not isinstance(data, dict):
        return ["ERROR state root must be a JSON object"]

    for key in REQUIRED_STATE_KEYS:
        if key not in data:
            messages.append(f"ERROR missing required key: {key}")

    handoff = data.get("handoff")
    if not isinstance(handoff, dict):
        messages.append("ERROR handoff must be a JSON object")
    lanes = data.get("lanes")
    if not isinstance(lanes, dict):
        messages.append("ERROR lanes must be a JSON object")

    for path_key in ["plan_path", "phase_prompts_path", "continuation_state_path"]:
        ref = data.get(path_key)
        if isinstance(ref, str) and ref and not Path(ref).exists():
            messages.append(f"WARN referenced {path_key} does not exist on disk: {ref}")

    resume = data.get("resume_protocol")
    if not isinstance(resume, dict):
        messages.append("ERROR resume_protocol must be a JSON object")
    else:
        must_read = resume.get("must_read_first")
        plan_path = data.get("plan_path")
        if isinstance(plan_path, str) and isinstance(must_read, list) and plan_path not in must_read:
            messages.append("ERROR resume_protocol.must_read_first does not include plan_path")

    return messages


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", help="Path to a plan markdown file, or 'auto'.")
    parser.add_argument("--state", help="Path to a state JSON file, or 'auto'.")
    parser.add_argument("--phase-prompts", help="Path to a phase prompt markdown file, or 'auto'.")
    parser.add_argument("--continuation", help="Path to a continuation markdown file, or 'auto'.")
    return parser.parse_args()


def report(kind: str, path: Path | None, messages: list[str]) -> bool:
    had_error = False
    if path is None or not path.exists():
        print(f"ERROR no {kind} file found")
        return True
    print(f"{kind.capitalize()}: {path}")
    for message in messages:
        print(message)
        had_error = had_error or message.startswith("ERROR")
    return had_error


def main() -> int:
    args = parse_args()
    had_error = False

    plan_path: Path | None = None
    if args.plan:
        plan_path = resolve_auto_plan() if args.plan == "auto" else Path(args.plan)
        if plan_path is None or not plan_path.exists():
            print("ERROR no plan file found")
            had_error = True
        else:
            had_error = report("plan", plan_path, validate_plan(plan_path)) or had_error

    if args.phase_prompts:
        phase_path = resolve_auto_phase_prompts(plan_path) if args.phase_prompts == "auto" else Path(args.phase_prompts)
        had_error = report("phase prompts", phase_path, validate_phase_prompts(phase_path, plan_path) if phase_path else []) or had_error

    if args.continuation:
        continuation_path = resolve_auto_continuation(plan_path) if args.continuation == "auto" else Path(args.continuation)
        had_error = report("continuation", continuation_path, validate_continuation(continuation_path, plan_path) if continuation_path else []) or had_error

    if args.state:
        state_path = resolve_auto_state() if args.state == "auto" else Path(args.state)
        had_error = report("state", state_path, validate_state(state_path) if state_path else []) or had_error

    if not args.plan and not args.state and not args.phase_prompts and not args.continuation:
        print("Nothing to validate. Pass --plan, --state, --phase-prompts, --continuation, or a combination.")
        return 1

    if not had_error:
        print("Validation completed without blocking errors.")
    return 1 if had_error else 0


if __name__ == "__main__":
    sys.exit(main())
