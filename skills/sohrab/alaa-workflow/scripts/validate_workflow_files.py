#!/usr/bin/env python3
"""Validate workflow plan/state artifacts quickly."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Iterable

REQUIRED_HEADINGS = [
    "## Goal",
    "## Assumptions",
    "## Constraints",
    "## Closest existing patterns",
    "## Phases (with dependencies)",
    "## Parallel-safe work split",
    "## Commands to run",
    "## Files touched (append-only log)",
    "## Done / Remaining",
]

REQUIRED_STATE_KEYS = [
    "task_id",
    "task",
    "mode",
    "status",
    "created_at",
    "updated_at",
    "plan_path",
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
    return newest_file(plans)


def resolve_auto_state() -> Path | None:
    return newest_file(Path(".codex/state").glob("*.json"))


def validate_plan(path: Path) -> list[str]:
    errors: list[str] = []
    warnings: list[str] = []
    content = path.read_text(encoding="utf-8")
    for heading in REQUIRED_HEADINGS:
        if heading not in content:
            errors.append(f"missing required heading: {heading}")
    if "{{" in content or "}}" in content:
        warnings.append("template placeholders appear to still be present")
    if "### Remaining now" not in content:
        warnings.append("recommended subsection '### Remaining now' not found under Done / Remaining")
    return [f"ERROR {msg}" for msg in errors] + [f"WARN {msg}" for msg in warnings]


def validate_state(path: Path) -> list[str]:
    messages: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"ERROR invalid JSON: {exc}"]

    for key in REQUIRED_STATE_KEYS:
        if key not in data:
            messages.append(f"ERROR missing required key: {key}")

    if isinstance(data, dict):
        handoff = data.get("handoff")
        if not isinstance(handoff, dict):
            messages.append("ERROR handoff must be a JSON object")
        lanes = data.get("lanes")
        if not isinstance(lanes, dict):
            messages.append("ERROR lanes must be a JSON object")

    plan_path = data.get("plan_path")
    if isinstance(plan_path, str) and plan_path and not Path(plan_path).exists():
        messages.append(f"WARN referenced plan_path does not exist on disk: {plan_path}")

    return messages


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", help="Path to a plan markdown file, or 'auto'.")
    parser.add_argument("--state", help="Path to a state JSON file, or 'auto'.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    had_error = False

    if args.plan:
        plan_path = resolve_auto_plan() if args.plan == "auto" else Path(args.plan)
        if plan_path is None or not plan_path.exists():
            print("ERROR no plan file found")
            had_error = True
        else:
            print(f"Plan: {plan_path}")
            for message in validate_plan(plan_path):
                print(message)
                had_error = had_error or message.startswith("ERROR")

    if args.state:
        state_path = resolve_auto_state() if args.state == "auto" else Path(args.state)
        if state_path is None or not state_path.exists():
            print("ERROR no state file found")
            had_error = True
        else:
            print(f"State: {state_path}")
            for message in validate_state(state_path):
                print(message)
                had_error = had_error or message.startswith("ERROR")

    if not args.plan and not args.state:
        print("Nothing to validate. Pass --plan, --state, or both.")
        return 1

    if not had_error:
        print("Validation completed without blocking errors.")
    return 1 if had_error else 0


if __name__ == "__main__":
    sys.exit(main())
