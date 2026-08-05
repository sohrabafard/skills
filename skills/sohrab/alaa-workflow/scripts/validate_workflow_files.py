#!/usr/bin/env python3
"""Semantically validate adaptive and legacy Alaa workflow artifacts."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable

PROFILES = ("auto", "direct", "resumable", "orchestrated", "legacy")
ADAPTIVE_STATE_KEYS = (
    "schema_version",
    "task_id",
    "task",
    "status",
    "plan_path",
    "current_phase",
    "next_actions",
    "blockers",
    "last_validation",
    "updated_at",
)
UNRESOLVED_RE = re.compile(
    r"\{\{[^{}]+\}\}|NEEDS_(?:FILL|CONFIRMATION|LIVE_VERIFICATION)|\[(?:todo|question|gap)\]",
    re.IGNORECASE,
)
COMPANION_LABELS = {
    "prompts": ("prompt pack", "phase prompts", "phase prompt pack"),
    "checkpoint": ("checkpoint", "continuation state", "state doc"),
    "state": ("machine state", "json state", "state file"),
}
HANDOFF_HEADING_RE = re.compile(r"^#{2,3}\s+handoff package\s*$", re.I | re.M)
HANDOFF_FIELDS = (
    "Confirmed facts",
    "Open assumptions",
    "Ruled out",
    "Read first on resume",
    "Environment notes",
    "Traps",
)
PHASE_FIELDS = ("Depends on", "Owned scope", "Excluded from this phase", "Evidence observed")
COMBINED_VALIDATION_RE = re.compile(r"^\s*[-*]\s*validation commands\s*/\s*evidence\s*:", re.I | re.M)
PLANNING_STATUSES = ("planning", "draft", "proposed", "not started")


def error(invariant: str, message: str, remediation: str) -> str:
    return f"ERROR [{invariant}] {message} Remediation: {remediation}"


def warning(invariant: str, message: str, remediation: str) -> str:
    return f"WARN [{invariant}] {message} Remediation: {remediation}"


def portable(path: Path) -> str:
    return str(path).replace("\\", "/")


def newest_file(candidates: Iterable[Path]) -> Path | None:
    files = [path for path in candidates if path.exists()]
    return max(files, key=lambda path: path.stat().st_mtime) if files else None


def resolve_auto_plan() -> Path | None:
    plans = list(Path("docs/_agent_plans").glob("*.md")) + list(Path("docs/plan").glob("*.md"))
    return newest_file(path for path in plans if not path.name.endswith("__phase-prompts.md"))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def has(content: str, pattern: str) -> bool:
    return re.search(pattern, content, re.IGNORECASE | re.MULTILINE) is not None


def detect_profile(content: str) -> str:
    match = re.search(r"^\s*[-*]?\s*profile\s*:\s*`?(direct|resumable|orchestrated|legacy)`?", content, re.I | re.M)
    return match.group(1).lower() if match else "legacy"


def detect_status(content: str) -> str:
    match = re.search(r"^\s*[-*]?\s*(?:current\s+)?status\s*(?::|—|-)\s*`?([^\n`]+)", content, re.I | re.M)
    return match.group(1).strip().lower() if match else ""


def is_complete_status(status: str) -> bool:
    return any(token in status for token in ("complete", "completed", "done", "closed"))


def is_planning_status(status: str) -> bool:
    return not status or any(token in status for token in PLANNING_STATUSES)


def section_block(content: str, heading: re.Pattern[str]) -> str | None:
    match = heading.search(content)
    if not match:
        return None
    rest = content[match.end():]
    end = re.search(r"^#{1,3}\s+", rest, re.M)
    return rest[: end.start()] if end else rest


def field_value(block: str, label: str) -> str | None:
    match = re.search(rf"^\s*[-*]\s*{re.escape(label)}\b[^:\n]*:\s*(.*)$", block, re.I | re.M)
    return match.group(1).strip() if match else None


def phase_blocks(content: str) -> list[tuple[str, str]]:
    blocks: list[tuple[str, str]] = []
    for match in re.finditer(r"^###\s+(.+)$", content, re.M):
        title = match.group(1).strip()
        if "phase" not in title.lower():
            continue
        rest = content[match.end():]
        following = re.search(r"^#{1,3}\s+", rest, re.M)
        blocks.append((title, rest[: following.start()] if following else rest))
    return blocks


def unresolved_messages(content: str, complete: bool, invariant: str) -> list[str]:
    matches = sorted(set(match.group(0) for match in UNRESOLVED_RE.finditer(content)))
    if not matches:
        return []
    sample = ", ".join(matches[:3])
    if complete:
        return [error(invariant, f"Completed artifact contains unresolved markers: {sample}.", "Resolve or explicitly classify every marker before completion.")]
    return [warning(invariant, f"Draft artifact contains unresolved markers: {sample}.", "Resolve them before execution or completion.")]


def validate_handoff(content: str, profile: str, status: str) -> list[str]:
    """Check the plan's handoff package, the section that owns what the work has learned."""
    block = section_block(content, HANDOFF_HEADING_RE)
    if block is None:
        return [
            warning(
                "plan.handoff",
                "Plan has no '## Handoff Package' section, so knowledge learned during the work has no home and dies with the conversation.",
                "Add the six-field handoff package from assets/plan-template.md: confirmed facts, open assumptions, ruled out, read first on resume, environment notes, traps.",
            )
        ]

    level = warning if profile == "legacy" else error
    messages: list[str] = []
    missing = [label for label in HANDOFF_FIELDS if field_value(block, label) is None]
    if missing:
        messages.append(
            level(
                "plan.handoff",
                f"Handoff package is missing required fields: {', '.join(missing)}.",
                "Keep all six fields present; leave a field empty rather than deleting it.",
            )
        )
    read_first = field_value(block, "Read first on resume")
    if read_first and UNRESOLVED_RE.search(read_first) and not is_planning_status(status):
        messages.append(
            level(
                "plan.handoff.read-first",
                f"Plan status '{status}' is past planning but 'Read first on resume' is still unfilled, so a cold start has no entry point.",
                "List the two or three exact paths a resuming agent must read before touching anything.",
            )
        )
    return messages


def validate_workspace(content: str, profile: str, status: str, adaptive_plan: bool) -> list[str]:
    """Check that the plan records the branch its commits are landing on.

    Two facts are load-bearing once execution begins. Without the work branch, this run's
    commits cannot be told apart from commits on the user's base branch. Without the base
    branch and commit, the integration handshake has no merge target to name and no
    baseline to compare against, so it cannot decide whether the exhaustive-tier evidence
    still describes the tree being merged. Both are therefore errors, not records.

    Checked only once the plan is past planning, because a plan being drafted has written
    nothing yet, and only on adaptive non-legacy plans, because completed legacy records
    are history rather than runs in flight.
    """
    if not adaptive_plan or profile == "legacy" or is_planning_status(status):
        return []
    messages: list[str] = []
    work_branch = field_value(content, "Work branch")
    if work_branch is None:
        messages.append(
            error(
                "plan.workspace",
                f"Plan status '{status}' is past planning but no work branch is recorded, so nothing distinguishes this run's commits from commits on the base branch.",
                "Add 'Work branch' and 'Base branch and commit' to the plan header per assets/plan-template.md.",
            )
        )
    elif UNRESOLVED_RE.search(work_branch):
        messages.append(
            error(
                "plan.workspace",
                f"Plan status '{status}' is past planning but the work branch is still unfilled.",
                "Record the branch this run's commits land on, and the base branch and commit it started from.",
            )
        )
    else:
        base = field_value(content, "Base branch and commit")
        if base is None or UNRESOLVED_RE.search(base):
            messages.append(
                error(
                    "plan.workspace",
                    f"Plan status '{status}' is past planning but the base branch and commit are not recorded, so the integration handshake has no merge target to name and no baseline to decide whether its verification evidence still describes the tree being merged.",
                    "Record 'Base branch and commit' in the plan header per assets/plan-template.md, naming the branch this work merges back into and the commit it started from.",
                )
            )
    return messages


def validate_phases(content: str, profile: str, adaptive_plan: bool, status: str = "") -> list[str]:
    """Check that each phase carries dependencies, ownership, exclusions, and observed evidence."""
    level = error if adaptive_plan and profile != "legacy" else warning
    messages: list[str] = []
    for title, block in phase_blocks(content):
        combined = COMBINED_VALIDATION_RE.search(block) is not None
        missing = [
            label
            for label in PHASE_FIELDS
            if field_value(block, label) is None and not (combined and label == "Evidence observed")
        ]
        if field_value(block, "Validation commands") is None:
            missing.append("Validation commands")
        if missing:
            messages.append(
                level(
                    "plan.phase-fields",
                    f"{title} is missing phase fields: {', '.join(missing)}.",
                    "Add them per assets/plan-template.md so a fresh agent can own the phase without re-deriving its boundaries.",
                )
            )
        if combined:
            messages.append(
                warning(
                    "plan.phase-fields",
                    f"{title} uses the superseded 'Validation commands/evidence' field.",
                    "Split it into 'Validation commands' (what to run) and 'Evidence observed' (what it returned).",
                )
            )
        if field_value(block, "Commit") is None:
            # An absent field and a phase that changed nothing are different states, and only
            # the field makes them distinguishable. Recording 'none', or that the user declined
            # the branch protocol, satisfies this; omitting it leaves the work unrecoverable
            # with no record of the decision that made it so.
            commit_level = warning if is_planning_status(status) else level
            messages.append(
                commit_level(
                    "plan.phase-commit",
                    f"{title} records no commit, so work it claims has no recoverable point to return to and nothing says whether that was intended.",
                    "Add 'Commit' per assets/plan-template.md. A phase that changed nothing records 'none'; a run the user excused from committing records that.",
                )
            )
    return messages


def validate_plan(path: Path, profile: str) -> list[str]:
    content = read_text(path)
    status = detect_status(content)
    complete = is_complete_status(status)
    messages: list[str] = []

    invariants = (
        ("plan.outcome", r"\b(summary|outcome|goal|objective)\b", "Define the intended outcome and current repository truth."),
        ("plan.scope", r"\b(scope|in[ -]scope|out[ -]of[ -]scope|constraints?)\b", "Define in-scope, out-of-scope, and constraints."),
        ("plan.ordered-work", r"\b(ordered work|phases?|implementation plan|tasks?)\b", "Add ordered phases or tasks with dependencies where relevant."),
        ("plan.acceptance", r"\b(acceptance|done condition|completion criteria|definition of done)\b", "State observable acceptance criteria."),
        ("plan.validation", r"\b(validation|validate|tests?|commands?|gates?|evidence)\b", "Name validation commands or required evidence."),
    )
    for invariant, pattern, remediation in invariants:
        if not has(content, pattern):
            level = warning if profile == "legacy" and invariant in {"plan.scope", "plan.acceptance", "plan.validation"} else error
            messages.append(level(invariant, "Required workflow meaning is missing.", remediation))

    if not has(content, r"(?:^\s*[-*]\s+\[[ xX-]\]|^\s*\d+[.)]\s+|^###\s+.*phase)"):
        messages.append(error("plan.ordered-work", "No executable ordered work was found.", "Add numbered steps, phases, or checklist items."))

    for invariant, pattern, remediation in (
        ("plan.status", r"\bstatus\s*(?::|—|-)", "Record the current plan status."),
        ("plan.blockers", r"\bblockers?\b", "Record blockers explicitly, including 'none known'."),
    ):
        if not has(content, pattern):
            message = f"Legacy plan does not expose {invariant.split('.')[-1]} semantics."
            if profile == "legacy":
                messages.append(warning(invariant, message, remediation))
            else:
                messages.append(error(invariant, message, remediation))

    adaptive_plan = HANDOFF_HEADING_RE.search(content) is not None
    messages.extend(validate_handoff(content, profile, status))
    messages.extend(validate_workspace(content, profile, status, adaptive_plan))
    messages.extend(validate_phases(content, profile, adaptive_plan, status))
    messages.extend(unresolved_messages(content, complete, "plan.placeholders"))
    return messages


def extract_reference(content: str, labels: tuple[str, ...]) -> str | None:
    label_pattern = "|".join(re.escape(label) for label in labels)
    match = re.search(rf"^\s*[-*]?\s*(?:{label_pattern})\s*:\s*(.+?)\s*$", content, re.I | re.M)
    if not match:
        return None
    value = match.group(1).strip().strip("`").strip()
    if value.lower() in {"none", "not created", "n/a", "null", ""}:
        return None
    return value


def path_from_reference(value: str | None, plan_path: Path) -> Path | None:
    if not value:
        return None
    candidate = Path(value)
    if candidate.is_absolute() or candidate.exists():
        return candidate
    adjacent = plan_path.parent / candidate
    return adjacent if adjacent.exists() else candidate


def same_stem_paths(plan_path: Path) -> dict[str, Path]:
    return {
        "prompts": plan_path.with_name(f"{plan_path.stem}__phase-prompts.md"),
        "checkpoint": Path("docs/agents") / f"{plan_path.stem}-state.md",
        "state": Path(".codex/state") / f"{plan_path.stem}.json",
    }


def legacy_state_references(state_path: Path) -> dict[str, Path]:
    if not state_path.exists():
        return {}
    try:
        data = json.loads(read_text(state_path))
    except (json.JSONDecodeError, OSError):
        return {}
    if not isinstance(data, dict):
        return {}
    result: dict[str, Path] = {}
    for key, aliases in {
        "checkpoint": ("continuation_state_path", "state_doc"),
        "prompts": ("phase_prompts_path", "phase_prompts"),
    }.items():
        for alias in aliases:
            value = data.get(alias)
            if isinstance(value, str) and value:
                result[key] = Path(value)
                break
    return result


def resolve_companions(plan_path: Path, content: str) -> dict[str, Path | None]:
    stems = same_stem_paths(plan_path)
    resolved: dict[str, Path | None] = {}
    for kind, labels in COMPANION_LABELS.items():
        explicit = path_from_reference(extract_reference(content, labels), plan_path)
        resolved[kind] = explicit or (stems[kind] if stems[kind].exists() else None)

    state_path = resolved["state"]
    if state_path is not None:
        for kind, candidate in legacy_state_references(state_path).items():
            if resolved.get(kind) is None:
                resolved[kind] = candidate
    return resolved


def validate_checkpoint(path: Path, plan_path: Path | None, profile: str) -> list[str]:
    content = read_text(path)
    messages: list[str] = []
    if profile == "legacy":
        for label, pattern in (
            ("status", r"\bstatus\b"),
            ("next action", r"\b(next|remaining|handoff)\b"),
            ("validation", r"\b(validation|verified|evidence)\b"),
        ):
            if not has(content, pattern):
                messages.append(warning(f"checkpoint.{label}", f"Legacy checkpoint lacks {label} semantics.", f"Add {label} when this record becomes active again."))
    else:
        fields = (
            ("status", r"^\s*[-*]\s*status\s*:"),
            ("current-phase", r"^\s*[-*]\s*current phase\s*:"),
            ("last-verified", r"^\s*[-*]\s*last verified result\s*:"),
            ("blockers", r"^\s*[-*]\s*blockers\s*:"),
            ("next-action", r"^\s*[-*]\s*next action\s*:"),
            ("touched-surfaces", r"^\s*[-*]\s*touched surfaces\s*:"),
        )
        for name, pattern in fields:
            if not has(content, pattern):
                messages.append(error(f"checkpoint.{name}", "Compact checkpoint field is missing.", f"Add the {name.replace('-', ' ')} field without duplicating the plan."))
    if plan_path:
        declared = extract_reference(content, ("plan",))
        if declared is None:
            if plan_path.name not in content and portable(plan_path) not in content:
                messages.append(error("checkpoint.plan", "Checkpoint does not reference the selected plan.", "Add a '- Plan: `<path>`' field naming the selected plan."))
            else:
                level = warning if profile == "legacy" else error
                messages.append(level("checkpoint.plan", "Checkpoint has no 'Plan:' field, so its link back to the plan is not machine-checkable.", "Add a '- Plan: `<path>`' field naming the selected plan."))
        elif Path(declared).name != plan_path.name:
            messages.append(error("checkpoint.plan", f"Checkpoint's Plan field points at a different plan: {declared}.", "Point the Plan field at the selected plan, or select the matching checkpoint."))
    messages.extend(unresolved_messages(content, is_complete_status(detect_status(content)), "checkpoint.placeholders"))
    return messages


def validate_prompt_pack(path: Path, plan_path: Path | None, profile: str) -> list[str]:
    content = read_text(path)
    messages: list[str] = []
    if profile != "legacy":
        concepts = (
            ("roles", r"\bimplementer\b[\s\S]*\bindependent reviewer\b"),
            ("outcome", r"\boutcome\b"),
            ("read-first", r"\bread first\b"),
            ("scope", r"\bscope\b"),
            ("validation", r"\bvalidation\b"),
            ("done", r"\bdone\b"),
            ("blocked", r"\bblocked\b"),
            ("freshness", r"\bverified on\b[\s\S]*\bverification sources\b[\s\S]*\bruntime/model\b"),
        )
        for name, pattern in concepts:
            if not has(content, pattern):
                messages.append(error(f"prompts.{name}", "Required role-prompt meaning is missing.", f"Add compact {name.replace('-', ' ')} information."))
    if plan_path and plan_path.name not in content and portable(plan_path) not in content:
        messages.append(error("prompts.plan", "Prompt pack does not reference the selected plan.", "Add the selected plan path."))
    unresolved = sorted(set(match.group(0) for match in UNRESOLVED_RE.finditer(content)))
    if unresolved:
        messages.append(error("prompts.freshness", f"Prompt pack is unresolved: {', '.join(unresolved[:3])}.", "Verify official docs and record resolved runtimes, models, sources, and date."))
    return messages


def json_contains_unresolved(value: Any) -> bool:
    if isinstance(value, str):
        return UNRESOLVED_RE.search(value) is not None
    if isinstance(value, list):
        return any(json_contains_unresolved(item) for item in value)
    if isinstance(value, dict):
        return any(json_contains_unresolved(item) for item in value.values())
    return False


def validate_state(path: Path, plan_path: Path | None = None, profile: str = "auto") -> list[str]:
    try:
        data = json.loads(read_text(path))
    except json.JSONDecodeError as exc:
        return [error("state.json", f"Invalid JSON at line {exc.lineno}, column {exc.colno}.", "Repair the JSON syntax.")]
    if not isinstance(data, dict):
        return [error("state.root", "State root is not an object.", "Use one JSON object.")]

    adaptive = profile != "legacy" and (profile != "auto" or data.get("schema_version") == 2)
    messages: list[str] = []
    if not adaptive:
        if not any(key in data for key in ("status", "phases", "next_step", "handoff")):
            messages.append(warning("state.legacy-status", "Legacy state has no recognizable status surface.", "Add status or next-step data if reactivating it."))
        if plan_path:
            declared = data.get("plan_path") or data.get("plan")
            if isinstance(declared, str) and declared and Path(declared).name != plan_path.name:
                messages.append(error("state.plan", "Legacy state points to a different plan.", "Select the matching state or correct its explicit plan reference."))
        return messages

    for key in ADAPTIVE_STATE_KEYS:
        if key not in data:
            messages.append(error(f"state.{key}", "Required compact state field is missing.", f"Add {key} without restoring legacy duplicate sections."))
    if data.get("schema_version") != 2:
        messages.append(error("state.schema-version", "Adaptive state schema_version is not 2.", "Set schema_version to 2."))
    if "next_actions" in data and not isinstance(data["next_actions"], list):
        messages.append(error("state.next-actions", "next_actions is not an array.", "Use an array of concise executable actions."))
    if "blockers" in data and not isinstance(data["blockers"], list):
        messages.append(error("state.blockers", "blockers is not an array.", "Use an array, empty when unblocked."))
    if "last_validation" in data and not isinstance(data["last_validation"], (dict, str)):
        messages.append(error("state.last-validation", "last_validation has an unsupported type.", "Use a concise object or string result."))
    if plan_path:
        declared = data.get("plan_path")
        if isinstance(declared, str) and declared and Path(declared).name != plan_path.name:
            messages.append(error("state.plan", "State points to a different plan.", "Correct plan_path or select the matching state."))
    if json_contains_unresolved(data):
        complete = is_complete_status(str(data.get("status", "")))
        level = error if complete else warning
        messages.append(level("state.placeholders", "State contains unresolved markers.", "Resolve them before completion."))
    return messages


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", help="Plan path, or auto to select the newest plan only.")
    parser.add_argument("--profile", choices=PROFILES, default="auto", help="Override profile detection.")
    parser.add_argument("--state", help="Explicit state path, or auto with a selected plan.")
    parser.add_argument("--phase-prompts", help="Explicit prompt-pack path, or auto with a selected plan.")
    parser.add_argument("--continuation", help="Explicit checkpoint path, or auto with a selected plan.")
    return parser.parse_args()


def report(kind: str, path: Path, messages: list[str]) -> bool:
    print(f"{kind}: {portable(path)}")
    for message in messages:
        print(message)
    return any(message.startswith("ERROR") for message in messages)


def explicit_path(value: str | None, correlated: Path | None, kind: str, plan_path: Path | None) -> Path | None:
    if value is None:
        return correlated
    if value == "auto":
        if plan_path is None:
            raise ValueError(f"--{kind} auto requires --plan so artifacts cannot cross-correlate.")
        return correlated
    return Path(value)


def main() -> int:
    args = parse_args()
    if not any((args.plan, args.state, args.phase_prompts, args.continuation)):
        print("Nothing to validate. Pass --plan or an explicit companion path.")
        return 1

    had_error = False
    plan_path: Path | None = None
    profile = args.profile
    companions: dict[str, Path | None] = {"prompts": None, "checkpoint": None, "state": None}

    if args.plan:
        plan_path = resolve_auto_plan() if args.plan == "auto" else Path(args.plan)
        if plan_path is None or not plan_path.exists():
            print(error("plan.path", "Selected plan does not exist.", "Pass an existing plan path."))
            return 1
        content = read_text(plan_path)
        profile = detect_profile(content) if profile == "auto" else profile
        companions = resolve_companions(plan_path, content)
        had_error = report("plan", plan_path, validate_plan(plan_path, profile)) or had_error

    try:
        companions["prompts"] = explicit_path(args.phase_prompts, companions["prompts"], "phase-prompts", plan_path)
        companions["checkpoint"] = explicit_path(args.continuation, companions["checkpoint"], "continuation", plan_path)
        companions["state"] = explicit_path(args.state, companions["state"], "state", plan_path)
    except ValueError as exc:
        print(error("correlation", str(exc), "Pass an explicit path or select a plan."))
        return 1

    required = {
        "direct": set(),
        "resumable": {"checkpoint"},
        "orchestrated": {"checkpoint", "state"},
        "legacy": {"prompts", "checkpoint", "state"},
        "auto": set(),
    }[profile]
    validators = {
        "prompts": lambda path: validate_prompt_pack(path, plan_path, profile),
        "checkpoint": lambda path: validate_checkpoint(path, plan_path, profile),
        "state": lambda path: validate_state(path, plan_path, profile),
    }

    for kind in ("prompts", "checkpoint", "state"):
        path = companions[kind]
        was_explicit = {
            "prompts": args.phase_prompts,
            "checkpoint": args.continuation,
            "state": args.state,
        }[kind] is not None
        if path is None or not path.exists():
            if kind in required or was_explicit:
                remediation = f"Create the correlated {kind} artifact or select a profile that does not require it."
                print(error(f"artifact.{kind}", f"Profile {profile} requires a correlated {kind} file.", remediation))
                had_error = True
            continue
        had_error = report(kind, path, validators[kind](path)) or had_error

    if not had_error:
        print(f"Validation completed without blocking errors (profile: {profile}).")
    return 1 if had_error else 0


if __name__ == "__main__":
    sys.exit(main())
