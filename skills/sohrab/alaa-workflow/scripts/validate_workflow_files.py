#!/usr/bin/env python3
"""Semantically validate adaptive and legacy Alaa workflow artifacts."""

from __future__ import annotations

import argparse
import json
import re
import sys
import traceback
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
SKILL_HEADING_RE = re.compile(r"^##\s+Skill Bindings\s*$", re.I | re.M)
SKILL_COLUMNS = ("Skill", "Source", "Load before", "When", "If unavailable")
SKILL_NAME_RE = re.compile(r"[a-z0-9][a-z0-9_.:-]*")
TASK_SKILLS_RE = re.compile(r"\[skills:\s*([^\]]+)\]\s*$", re.I)
TASK_LINE_RE = re.compile(r"^\s*(?:[-*]\s+\[[ xX-]\]|\d+[.)])\s+(.+)$", re.M)
VAGUE_SKILLS_RE = re.compile(r"\b(?:relevant|appropriate|related|matching)\s+skills?\b", re.I)


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
    header = re.split(r"^#{2,6}\s+", content, maxsplit=1, flags=re.M)[0]
    match = re.search(r"^[ \t]*[-*]?[ \t]*(?:current[ \t]+)?status[ \t]*(?::|—|-)[ \t]*`?([^\n`]+)", header, re.I | re.M)
    return match.group(1).strip().lower() if match else ""


def is_complete_status(status: str) -> bool:
    return status.strip().lower() in {"complete", "completed", "done", "closed"}


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
    return [(title, content[start:end]) for title, start, end in phase_regions(content)]


def phase_regions(content: str) -> list[tuple[str, int, int]]:
    blocks: list[tuple[str, int, int]] = []
    for match in re.finditer(r"^###\s+(.+)$", content, re.M):
        title = match.group(1).strip()
        if not re.match(r"phase\b", title, re.I):
            continue
        rest = content[match.end():]
        following = re.search(r"^#{1,3}\s+", rest, re.M)
        end = match.end() + following.start() if following else len(content)
        blocks.append((title, match.end(), end))
    return blocks


def skill_frontmatter_name(content: str) -> str | None:
    frontmatter = re.match(r"\A---[ \t]*\r?\n([\s\S]*?)\r?\n---[ \t]*(?:\r?\n|\Z)", content)
    if frontmatter is None:
        return None
    declarations = re.findall(r"^name:[ \t]*(.*)$", frontmatter.group(1), re.M)
    if len(declarations) != 1:
        return None
    value = declarations[0].strip()
    if value.startswith(("'", '"')):
        if len(value) < 2 or value[-1] != value[0]:
            return None
        value = value[1:-1]
    return value if SKILL_NAME_RE.fullmatch(value) else None


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
    """Check that an active plan identifies its checkout and starting base.

    These fields attribute work and let a resumed agent detect checkout drift. They do not
    grant or imply commit or integration authority.

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
                f"Plan status '{status}' is past planning but no work branch or checkout is recorded, so this run's changes cannot be attributed to a workspace.",
                "Add 'Work branch' (or describe a detached checkout there) and 'Base branch and commit' to the plan header per assets/plan-template.md.",
            )
        )
    elif UNRESOLVED_RE.search(work_branch):
        messages.append(
            error(
                "plan.workspace",
                f"Plan status '{status}' is past planning but the work branch is still unfilled.",
                "Record the current branch or checkout and the starting base branch and commit.",
            )
        )
    else:
        base = field_value(content, "Base branch and commit")
        if base is None or UNRESOLVED_RE.search(base):
            messages.append(
                error(
                    "plan.workspace",
                    f"Plan status '{status}' is past planning but the starting base branch and commit are not recorded, so later changes cannot be compared with their baseline.",
                    "Record 'Base branch and commit' in the plan header per assets/plan-template.md.",
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
        commit = field_value(block, "Commit")
        snapshot = field_value(block, "Snapshot")
        if commit is None and snapshot is None:
            snapshot_level = warning if is_planning_status(status) else level
            messages.append(
                snapshot_level(
                    "plan.phase-snapshot",
                    f"{title} records neither a commit nor a scoped worktree snapshot, so its evidence has no identity.",
                    "Record an authorized 'Commit' or an observed 'Snapshot' per assets/plan-template.md; a phase that changed no files states that explicitly.",
                )
            )
        elif adaptive_plan and profile != "legacy" and is_complete_status(field_value(block, "Status") or ""):
            authorized_commit = bool(commit and re.fullmatch(r"(?:[0-9a-f]{7,40}|`[0-9a-f]{7,40}`)", commit, re.I))
            no_changes = any(
                value is not None and re.fullmatch(r"(?:none;\s*)?(?:no files changed|this phase changed no files)\.?", value, re.I)
                for value in (commit, snapshot)
            )
            scoped_snapshot = bool(snapshot and (
                re.search(r"\bHEAD\s+[0-9a-f]{7,40}\b", snapshot, re.I)
                and re.search(r"\bSHA-?256\s+[0-9a-f]{64}\b", snapshot, re.I)
                and re.search(r"\bpaths?\s+\S+", snapshot, re.I)
            ))
            if not (authorized_commit or no_changes or scoped_snapshot):
                messages.append(
                    level(
                        "plan.phase-snapshot",
                        f"{title} is complete but records no commit ID or scoped worktree snapshot.",
                        "Record an authorized commit ID, the actual HEAD and SHA-256 digest of the scoped path/content manifest, or state exactly that no files changed.",
                    )
                )
    return messages


def validate_skill_bindings(content: str, path: Path, profile: str, status: str) -> list[str]:
    """Resolve phase/task owners without treating a conditional absence as installed."""
    block = section_block(content, SKILL_HEADING_RE)
    historical = is_complete_status(status) and (profile == "legacy" or block is None)
    level = warning if historical else error
    executing = not is_planning_status(status) or any(
        (field_value(phase, "Status") or "pending").lower() not in {"pending", "planning", "draft"}
        for _, phase in phase_blocks(content)
    )
    unresolved_level = level if executing and not historical else warning
    messages: list[str] = []
    bindings: dict[str, list[str]] = {}
    if block is None:
        messages.append(level("plan.skills", "Plan has no Skill Bindings table.", "Add exact skill names, sources, load points, conditions and absence actions before execution; retain completed history unchanged."))
    else:
        rows = [
            [cell.strip().strip("`") for cell in line.strip().strip("|").split("|")]
            for line in block.splitlines() if line.strip().startswith("|")
        ]
        if not rows or tuple(rows[0]) != SKILL_COLUMNS:
            messages.append(level("plan.skills", "Skill Bindings columns are missing or unsupported.", "Use Skill | Source | Load before | When | If unavailable."))
        else:
            for row in rows[1:]:
                if all(re.fullmatch(r":?-+:?", cell) for cell in row):
                    continue
                if len(row) != len(SKILL_COLUMNS) or any(not cell for cell in row):
                    messages.append(level("plan.skills", "Skill binding has empty or missing fields.", "Populate all five columns."))
                    continue
                if any(UNRESOLVED_RE.search(cell) for cell in row):
                    messages.append(unresolved_level("plan.skills", "Skill binding is unresolved.", "Replace draft markers with verified catalog names and source paths before execution."))
                    continue
                name, source, load_before, condition, absence = row
                if not SKILL_NAME_RE.fullmatch(name) or VAGUE_SKILLS_RE.search(" ".join(row)):
                    messages.append(level("plan.skills", f"Skill binding is vague or has no exact name: {name}.", "Use the exact available catalog/frontmatter name and concrete activation facts."))
                    continue
                if name in bindings:
                    messages.append(level("plan.skills", f"Duplicate skill binding: {name}.", "Keep one binding per exact skill name."))
                    continue
                bindings[name] = row
                if source.lower() == "unavailable":
                    if condition.lower() == "always":
                        messages.append(level("plan.skills-source", f"Unconditional skill {name} is unavailable.", "Block its work or record an explicitly authorized fallback; never silently substitute or install."))
                    continue
                source_path = Path(source)
                if not source_path.is_absolute() and not source_path.exists():
                    source_path = path.parent / source_path
                if source_path.name != "SKILL.md" or not source_path.is_file():
                    messages.append(level("plan.skills-source", f"Skill {name} has a dangling source: {source}.", "Name a readable SKILL.md or explicitly mark a conditional owner unavailable."))
                    continue
                if skill_frontmatter_name(read_text(source_path)) != name:
                    messages.append(level("plan.skills-source", f"Skill {name} does not match source frontmatter.", "Use the source's exact catalog name."))

    def check_names(value: str | None, where: str, inherit: str | None = None) -> None:
        if value is None or not value.strip():
            messages.append(level("plan.skills-mapping", f"{where} has no skill mapping.", "Name exact Skill Bindings or use task [skills: inherit] under an explicit phase list."))
            return
        if value.lower() == "inherit":
            if inherit is None:
                messages.append(level("plan.skills-mapping", f"{where} has no phase list to inherit.", "Populate the phase Required skills field."))
                return
            value = inherit
        if UNRESOLVED_RE.search(value):
            messages.append(unresolved_level("plan.skills-mapping", f"{where} has unresolved skills.", "Populate exact names before executing the task."))
            return
        if re.fullmatch(r"none\s*\(.+\)", value, re.I):
            return
        names = [name.strip().strip("`") for name in value.split(",")]
        if any(not SKILL_NAME_RE.fullmatch(name) for name in names) or VAGUE_SKILLS_RE.search(value):
            messages.append(level("plan.skills-mapping", f"{where} uses vague skills: {value}.", "List exact names separated by commas, or none (specific reason)."))
        else:
            missing = [name for name in names if name not in bindings]
            if missing:
                messages.append(level("plan.skills-mapping", f"{where} refers to unbound skills: {', '.join(missing)}.", "Add their complete Skill Bindings rows."))

    regions = phase_regions(content)
    if not regions:
        messages.append(level("plan.skills-structure", "Plan has no executable phase structure.", "Put ordered tasks inside Phase headings with explicit Required skills fields."))
    for title, start, end in regions:
        phase = content[start:end]
        required = field_value(phase, "Required skills")
        check_names(required, title)
        for task in TASK_LINE_RE.finditer(phase):
            mapping = TASK_SKILLS_RE.search(task.group(1))
            check_names(mapping.group(1) if mapping else None, f"{title} task '{task.group(1)}'", required)
    ordered = re.search(r"^##\s+Ordered Work\s*$", content, re.I | re.M)
    ordered_end = len(content)
    if ordered:
        following = re.search(r"^#{1,2}\s+", content[ordered.end():], re.M)
        if following:
            ordered_end = ordered.end() + following.start()
    for task in TASK_LINE_RE.finditer(content):
        in_phase = any(start <= task.start() < end for _, start, end in regions)
        checkbox = re.match(r"\s*[-*]\s+\[", task.group(0)) is not None
        in_ordered_work = ordered is not None and ordered.end() <= task.start() < ordered_end
        if not in_phase and (checkbox or in_ordered_work):
            messages.append(level("plan.skills-structure", f"Task '{task.group(1)}' is outside a phase.", "Move it into an explicit phase; every task needs a mapping or phase inheritance."))
    return messages


def validate_plan(path: Path, profile: str) -> list[str]:
    content = read_text(path)
    status = effective_plan_status(content, path, profile)
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
    messages.extend(validate_skill_bindings(content, path, profile, status))
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


def effective_plan_status(content: str, plan_path: Path, profile: str) -> str:
    """An explicit plan status wins; correlated terminal legacy state can prove history."""
    status = detect_status(content)
    if status or profile != "legacy":
        return status
    state_path = resolve_companions(plan_path, content)["state"]
    if state_path is None or not state_path.is_file():
        return status
    try:
        data = json.loads(read_text(state_path))
    except json.JSONDecodeError:
        return status
    if not isinstance(data, dict):
        return status
    declared_plan = data.get("plan_path") or data.get("plan")
    if not isinstance(declared_plan, str) or not references_selected_plan(declared_plan, plan_path):
        return status
    terminal = {"complete", "completed", "done", "closed"}
    declared_status = str(data.get("status", "")).strip().lower()
    if declared_status:
        return "complete" if declared_status in terminal else status
    phases = data.get("phases")
    all_terminal = isinstance(phases, dict) and bool(phases) and all(
        isinstance(value, str) and value.strip().lower() in terminal for value in phases.values()
    )
    next_step = str(data.get("next_step", ""))
    terminal_next = re.search(r"^none\b[^\n]*\bcomplete(?:d)?\b", next_step.strip(), re.I)
    return "complete" if all_terminal and terminal_next else status


def references_selected_plan(declared: str, plan_path: Path) -> bool:
    candidate = Path(declared)
    selected = plan_path.resolve()
    if candidate.is_absolute():
        return candidate.resolve() == selected
    return candidate.resolve() == selected or (plan_path.parent / candidate).resolve() == selected


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


def prompt_task_controls_failures(content: str) -> list[str]:
    """Check selected-control completeness; never claim effective runtime proof."""
    messages = []
    for role in ("Implementer", "Independent reviewer", "Documenter"):
        pair = field_value(content, role + " runtime/model")
        effort = field_value(content, role + " effort")
        if role == "Documenter" and pair == "not included / not included":
            continue
        runtime, separator, model = (pair or "").partition("/")
        selected = [runtime.strip(), model.strip(), (effort or "").strip()]
        if not separator or any(not value or value.lower() == "not included" or
                                UNRESOLVED_RE.search(value) for value in selected):
            messages.append(error("prompts.task-controls", f"{role} lacks explicit selected model AND effort.",
                                  "Record both task controls from the runtime orchestrator; inherited defaults are incomplete."))
    if "verify BOTH effective model and effort" not in content:
        messages.append(error("prompts.effective-controls", "Dispatch-time control verification is absent.",
                              "Route every dispatch to the active orchestrator's verified control surface."))
    return messages


def validate_prompt_pack(path: Path, plan_path: Path | None, profile: str) -> list[str]:
    content = read_text(path)
    messages: list[str] = []
    if profile != "legacy":
        messages.extend(prompt_task_controls_failures(content))
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
    parser = argparse.ArgumentParser(
        prog="validate_workflow_files.py",
        description=__doc__,
        epilog=(
            "exit 0  no blocking error. Warnings alone do not reach 1.\n"
            "exit 1  a blocking error in the artifacts. Repair it before the plan advances; "
            "an error is a defect in the artifacts, never a reason to relax the check.\n"
            "exit 2  the validation could not run -- nothing was selected, the plan does not "
            "exist, a companion cannot be correlated, or a selected file cannot be read. "
            "Exit 2 is a failed gate, never evidence that the artifacts are clean."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
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
        # Could not run, not clean and not findings. Exiting 1 here would be read as
        # "the artifacts are wrong" when in fact nothing was ever checked.
        print("Nothing to validate. Pass --plan or an explicit companion path.")
        return 2

    had_error = False
    plan_path: Path | None = None
    profile = args.profile
    companions: dict[str, Path | None] = {"prompts": None, "checkpoint": None, "state": None}

    if args.plan:
        plan_path = resolve_auto_plan() if args.plan == "auto" else Path(args.plan)
        if plan_path is None or not plan_path.exists():
            print(error("plan.path", "Selected plan does not exist.", "Pass an existing plan path."))
            return 2
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
        return 2

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

    raw_flags = {
        "prompts": args.phase_prompts,
        "checkpoint": args.continuation,
        "state": args.state,
    }

    for kind in ("prompts", "checkpoint", "state"):
        path = companions[kind]
        raw = raw_flags[kind]
        # A path the caller typed and a path this run correlated are different claims. The
        # first not existing is a broken invocation; the second not existing is a real gap in
        # the artifact family. "auto" is a request to correlate, so it belongs to the second.
        was_named = raw is not None and raw != "auto"
        was_explicit = raw is not None
        if path is None or not path.exists():
            if was_named:
                print(
                    error(
                        f"artifact.{kind}",
                        f"Explicitly selected {kind} path does not exist: {raw}.",
                        "Pass a path that exists, or drop the flag and let the plan stem correlate the companion.",
                    )
                )
                return 2
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
    # An artifact that cannot be read, or a validator that raised, is a validation that did
    # not happen. Both would otherwise leave through Python's default exit 1 and be
    # indistinguishable from findings, which is the one misreading this gate cannot afford.
    try:
        sys.exit(main())
    except (OSError, UnicodeDecodeError) as exc:
        print(
            error("runner", f"Validation could not run: {exc}.", "Make every selected artifact readable, then re-run."),
            file=sys.stderr,
        )
        sys.exit(2)
    except Exception:  # noqa: BLE001 - a validator bug is a failed gate, not a finding
        traceback.print_exc()
        print(
            error("runner", "Validation could not run: the validator raised.", "Report the traceback above; it is not a result."),
            file=sys.stderr,
        )
        sys.exit(2)
