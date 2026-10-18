#!/usr/bin/env python3
"""Create adaptive Alaa workflow artifacts from a repository root."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import traceback
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
PROFILES = ("direct", "resumable", "orchestrated", "legacy")
DEFAULT_PROFILE = "resumable"
UNRESOLVED = "NEEDS_LIVE_VERIFICATION"


class Misuse(Exception):
    """The invocation cannot produce artifacts, so nothing was created.

    Separated from a write conflict because the two oblige different repairs: a misuse is
    fixed in the command, a conflict is a decision about files already in the repository.
    """


def slugify(value: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", value.strip().lower())
    return re.sub(r"-+", "-", value).strip("-") or "task"


def now_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def choose_plan_dir(explicit: str | None, parent_plan: Path | None) -> Path:
    if parent_plan is not None:
        return parent_plan.parent
    if explicit and explicit != "auto":
        return Path(explicit)
    if Path("docs/_agent_plans").exists():
        return Path("docs/_agent_plans")
    if Path("docs/plan").exists():
        return Path("docs/plan")
    return Path("docs/_agent_plans")


def portable(path: Path) -> str:
    return str(path).replace("\\", "/")


def display_path(path: Path | None) -> str:
    return f"`{portable(path)}`" if path else "not created"


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def render(template_name: str, values: dict[str, str]) -> str:
    content = (ASSETS / template_name).read_text(encoding="utf-8")
    for key, value in values.items():
        content = content.replace(f"{{{{{key}}}}}", value)
    if "{{" in content or "}}" in content:
        raise ValueError(f"Unresolved template token in {template_name}")
    return content


def render_json(values: dict[str, str]) -> str:
    escaped = values.copy()
    for key in ("task", "task_id", "plan_path", "created_at"):
        escaped[key] = json.dumps(values[key], ensure_ascii=True)[1:-1]
    return json.dumps(json.loads(render("state-template.json", escaped)), indent=2, ensure_ascii=True) + "\n"


def warn(message: str) -> None:
    print(f"DEPRECATED: {message}", file=sys.stderr)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="init_workflow_files.py",
        description=__doc__,
        epilog=(
            "exit 0  the artifacts were created, or --dry-run printed the paths it would create.\n"
            "exit 1  an output already exists and --force was not given. Nothing was written; "
            "decide whether to continue the existing artifact family or to overwrite it.\n"
            "exit 2  the invocation could not run -- paired flags supplied alone, a parent plan "
            "that does not exist, a malformed timestamp or date, or an unreadable template. "
            "Exit 2 is not evidence that the artifacts exist."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--task", required=True, help="Human task title used for naming and template fill.")
    parser.add_argument("--plan-kind", required=True, choices=("design", "execution"), help="Design discussion or execution of an approved design.")
    parser.add_argument("--approved-design", help="Readable approved design plan required for execution; never modified.")
    parser.add_argument(
        "--profile",
        choices=PROFILES,
        help=(
            "Artifact profile. Default: resumable, because anything with more than one phase "
            "needs a checkpoint to survive compaction, a new session, or a fresh agent, and the "
            "checkpoint records position at material events. Choose direct deliberately "
            "for genuinely single-phase bounded work."
        ),
    )
    parser.add_argument("--with-prompts", action="store_true", help="Create the same-stem role prompt pack.")
    parser.add_argument("--task-store", choices=("local", "beads"), default="local", help="Task authority; local is valid only for new direct single-phase work. Phased/delegated plans require explicit beads and binding. No live tracker access.")
    parser.add_argument("--beads-binding", help="Portable project-relative binding owner reference for Beads.")
    parser.add_argument("--review-boundary", choices=("phase", "final"), help="Declared engagement review boundary; defaults to phase at the root, inherited from a parent plan.")
    parser.add_argument("--slug", help="Optional explicit slug.")
    parser.add_argument("--plan-dir", default="auto", help="Plan directory, or auto.")
    parser.add_argument("--timestamp", help="Fixed timestamp in YYYYMMDD-HHMMSS format.")
    parser.add_argument("--force", action="store_true", help="Overwrite outputs if they exist.")
    parser.add_argument("--dry-run", action="store_true", help="Print paths without writing files.")

    parser.add_argument("--implementer-runtime")
    parser.add_argument("--implementer-model")
    parser.add_argument("--reviewer-runtime")
    parser.add_argument("--reviewer-model")
    parser.add_argument("--documenter-runtime")
    parser.add_argument("--documenter-model")
    parser.add_argument("--implementer-effort")
    parser.add_argument("--reviewer-effort")
    parser.add_argument("--documenter-effort")
    parser.add_argument("--verified-on", help="Official-doc verification date in YYYY-MM-DD format.")
    parser.add_argument("--verification-source", action="append", default=[])

    # Transitional aliases retained for one compatibility period.
    parser.add_argument("--mode", default="plan", choices=["plan", "execute", "resume", "delegated", "review"], help="Deprecated metadata alias.")
    parser.add_argument("--with-state", action="store_true", help="Deprecated alias for the legacy/orchestrated state behavior.")
    parser.add_argument("--state-only", action="store_true", help="Deprecated: create only compact JSON state.")
    parser.add_argument("--no-continuation", action="store_true", help="Deprecated legacy exception.")
    parser.add_argument("--lane", help="Deprecated lane name; ownership now belongs in the plan or prompt.")
    parser.add_argument("--parent-plan", help="Deprecated parent-plan path used with --lane.")
    return parser.parse_args()


def validate_timestamp(stamp: str) -> str:
    if not re.fullmatch(r"\d{8}-\d{6}", stamp):
        raise Misuse("--timestamp must match YYYYMMDD-HHMMSS")
    return stamp


def resolve_profile(args: argparse.Namespace) -> str:
    aliased = bool(args.with_state or args.state_only)
    profile = args.profile or DEFAULT_PROFILE
    if args.with_state:
        warn("--with-state is a compatibility alias; use --profile orchestrated or legacy.")
        profile = "legacy" if args.profile is None else ("orchestrated" if profile != "legacy" else profile)
    if args.state_only:
        warn("--state-only is a compatibility alias; prefer an orchestrated profile with its plan.")
        profile = "orchestrated" if args.profile is None else profile
    if args.no_continuation:
        warn("--no-continuation is compatibility-only and produces a legacy exception.")
        if args.profile is None and not aliased:
            # The default is now resumable; a bare --no-continuation keeps its plan-only result.
            profile = "direct"
        elif profile != "direct":
            profile = "legacy"
    if args.lane or args.parent_plan:
        warn("--lane/--parent-plan remain transitional; record lane ownership in the parent plan or prompt.")
    if args.mode != "plan":
        warn("--mode is retained for metadata compatibility; profiles now control artifact admission.")
    return profile


def resolve_prompt_metadata(args: argparse.Namespace, active: bool) -> dict[str, str]:
    fields = [
        args.implementer_runtime,
        args.implementer_model,
        args.reviewer_runtime,
        args.reviewer_model,
    ]
    documenter_fields = [args.documenter_runtime, args.documenter_model]
    efforts = [args.implementer_effort, args.reviewer_effort]
    if any(value is not None and not value.strip() for value in
           fields + documenter_fields + efforts + [args.documenter_effort]):
        raise Misuse("Runtime, model and effort values must be nonempty.")
    if any(efforts) and (not all(efforts) or not all(fields)):
        raise Misuse("Provide both implementer/reviewer efforts with complete runtime/model metadata.")
    if args.documenter_effort and (not all(documenter_fields) or not all(efforts)):
        raise Misuse("Documenter effort requires complete documenter and implementer/reviewer controls.")
    if any(fields) and not all(fields):
        raise Misuse("Provide all implementer/reviewer runtime and model values together.")
    if any(documenter_fields) and not all(documenter_fields):
        raise Misuse("Provide documenter runtime and model values together.")
    if any(documenter_fields) and not all(fields):
        raise Misuse("Documenter metadata requires the implementer/reviewer metadata.")
    if not active and (any(fields) or any(documenter_fields) or any(efforts) or args.documenter_effort or args.verified_on or args.verification_source):
        raise Misuse("Prompt verification metadata requires --with-prompts.")
    if not active:
        return {}
    if not all(fields):
        print(
            "WARN prompt pack contains NEEDS_LIVE_VERIFICATION markers; verify official docs before use.",
            file=sys.stderr,
        )
        return {
            "verification_status": UNRESOLVED,
            "verified_on": UNRESOLVED,
            "verification_sources": UNRESOLVED,
            "implementer_runtime": UNRESOLVED,
            "implementer_model": UNRESOLVED,
            "reviewer_runtime": UNRESOLVED,
            "reviewer_model": UNRESOLVED,
            "documenter_runtime": UNRESOLVED,
            "documenter_model": UNRESOLVED,
            "implementer_effort": UNRESOLVED,
            "reviewer_effort": UNRESOLVED,
            "documenter_effort": UNRESOLVED,
        }
    if not args.verified_on or not args.verification_source:
        raise Misuse("Resolved prompt metadata requires --verified-on and at least one --verification-source.")
    verified_on = args.verified_on
    try:
        date.fromisoformat(verified_on)
    except ValueError as exc:
        raise Misuse("--verified-on must match YYYY-MM-DD") from exc
    sources = ", ".join(args.verification_source)
    return {
        "verification_status": ("configured intent; source metadata supplied; effective controls require dispatch verification"
                                if all(efforts) and (not all(documenter_fields) or args.documenter_effort)
                                else UNRESOLVED),
        "verified_on": verified_on,
        "verification_sources": sources,
        "implementer_runtime": args.implementer_runtime,
        "implementer_model": args.implementer_model,
        "reviewer_runtime": args.reviewer_runtime,
        "reviewer_model": args.reviewer_model,
        "documenter_runtime": args.documenter_runtime or "not included",
        "documenter_model": args.documenter_model or "not included",
        "implementer_effort": args.implementer_effort or UNRESOLVED,
        "reviewer_effort": args.reviewer_effort or UNRESOLVED,
        "documenter_effort": (args.documenter_effort or UNRESOLVED) if all(documenter_fields) else "not included",
    }


def task_store_values(args: argparse.Namespace, checkpoint: Path | None, profile: str) -> dict[str, str]:
    delegated = args.mode == "delegated" or bool(args.parent_plan or args.lane)
    if args.state_only and delegated:
        raise Misuse("Delegated work requires a bound plan; --state-only cannot represent its hierarchy.")
    hierarchy = not args.state_only
    if hierarchy and args.task_store != "beads":
        raise Misuse("New phased/delegated plans require --task-store beads and --beads-binding; continue existing local families in place.")
    binding = args.beads_binding
    if args.task_store == "local" and binding is not None:
        raise Misuse("--beads-binding requires --task-store beads.")
    if args.task_store == "beads":
        if args.state_only:
            raise Misuse("--task-store beads cannot use --state-only; a bound plan is required.")
        if not binding or not binding.strip():
            raise Misuse("--task-store beads requires --beads-binding.")
        if binding.strip() == "not applicable":
            raise Misuse("--beads-binding cannot be 'not applicable' in Beads mode.")
        if (re.search(r"[\r\n`\\]", binding) or re.match(r"(?:/|[a-zA-Z][a-zA-Z0-9+.-]*:)", binding.strip())
                or re.search(r"\{\{|\}\}|NEEDS_(?:FILL|CONFIRMATION|LIVE_VERIFICATION)|\[(?:todo|question|gap)\]", binding, re.I)
                or not binding.split("#", 1)[0].strip()):
            raise Misuse("--beads-binding must name a portable project-relative owner reference.")
        binding = binding.strip()
    local_work = (
        "  - [ ] T1: Read the named sources and verify current behavior. [depends: none] [skills: inherit]\n"
        "  - [ ] T2: Make the smallest in-scope change. [depends: T1] [skills: inherit]",
        "  - [ ] T3: Run the affected validation surface and repair failures. [depends: T2] [skills: inherit]\n"
        "  - [ ] T4: Reconcile documentation, status, blockers, and remaining work. [depends: T3] [skills: inherit]",
    )
    beads_work = tuple(
        (f"  - Task issue: NEEDS_FILL_TASK_{number} [skills: inherit]\n"
         f"    - Subtask issue: NEEDS_FILL_SUBTASK_{number} [skills: inherit]") if hierarchy else
        "  - Issue: NEEDS_FILL_ISSUE_1 [skills: inherit]\n  - Issue: NEEDS_FILL_ISSUE_2 [skills: inherit]"
        for number in (1, 2)
    )
    work = local_work if args.task_store == "local" else beads_work
    direct_cursor = "- Current task: none\n- Current subtask: none\n" if hierarchy else ""
    position = (f"## Execution Position\n\n- Position owner: {display_path(checkpoint)} (current phase/task/subtask, blockers, next action)."
                if checkpoint else "## Blockers and Next Action\n\n- Current phase: Phase 1\n" + direct_cursor + "- Blockers: none known.\n- Next action: Complete the plan's repository-grounding fields.")
    phase_count = 2 if profile != "direct" else 1
    phase_values = []
    for number in range(1, phase_count + 1):
        phase_values.append(render("phase-template.md", {
            "phase_number": str(number),
            "phase_title": "Ground and implement" if number == 1 else "Validate and reconcile",
            "phase_dependency": "none" if number == 1 else "Phase 1",
            "phase_mapping": f"- Phase issue: NEEDS_FILL_PHASE_{number}\n" if hierarchy else "",
            "phase_work": work[number - 1],
        }))
    return {
        "task_store": args.task_store,
        "task_binding": binding or "not applicable",
        "hierarchy_header": "- Task hierarchy: phase-task-subtask\n" if hierarchy else "",
        "review_boundary": args.review_boundary or "phase",
        "final_phase": f"Phase {phase_count}",
        "local_final_header": "",
        "ordered_work": "\n".join(phase_values),
        "cursor_fields": "- Current task: none\n- Current subtask: none\n" if hierarchy else "",
        "schema_version": "3" if hierarchy else "2",
        "json_cursor_fields": '  "current_task": "none",\n  "current_subtask": "none",\n' if hierarchy else "",
        "task_delegation": ("- Dependency edges and ready sets: Local task prerequisites above own dependency edges; derive readiness before dispatch."
                            if args.task_store == "local" else "- Dependency edges and ready sets: Beads owns issue dependencies and readiness; the plan owns phase barriers and shared-resource conflicts."),
        "position_section": position,
    }


def run(args: argparse.Namespace) -> int:
    if args.plan_kind == "design":
        incompatible = (args.approved_design or args.beads_binding or args.task_store != "local"
                        or args.review_boundary or args.with_prompts or args.with_state or args.state_only
                        or args.no_continuation or args.lane or args.parent_plan or args.mode != "plan"
                        or (args.profile is not None and args.profile != "resumable"))
        if incompatible:
            raise Misuse("Design requires resumable/local and rejects execution, hierarchy, prompt and state flags.")
    elif not args.approved_design:
        raise Misuse("Execution requires --approved-design naming a valid approved design plan.")
    elif args.state_only:
        raise Misuse("--state-only cannot represent an execution plan and its Beads hierarchy; continue historical state in place.")
    approved_design = None
    protected_design_paths: list[Path] = []
    if args.plan_kind == "execution":
        from validate_workflow_files import extract_reference, path_from_reference, read_text, require_approved_design
        approved_design = Path(args.approved_design).expanduser()
        try:
            require_approved_design(approved_design)
            design_checkpoint = path_from_reference(extract_reference(read_text(approved_design), ("checkpoint",)), approved_design)
        except (ValueError, OSError, UnicodeError) as exc:
            raise Misuse(f"Invalid --approved-design: {exc}") from exc
        protected_design_paths = [approved_design] + ([design_checkpoint] if design_checkpoint else [])
    profile = resolve_profile(args)
    include_prompts = args.with_prompts or profile == "legacy"
    prompt_metadata = resolve_prompt_metadata(args, include_prompts)

    parent_plan = Path(args.parent_plan) if args.parent_plan else None
    if args.lane and parent_plan is None:
        raise Misuse("--lane requires --parent-plan.")
    if parent_plan and not parent_plan.exists():
        raise Misuse(f"Parent plan not found: {parent_plan}")
    inherited = None
    if parent_plan:
        # Share the validator's contract rather than inventing nested defaults.
        from validate_workflow_files import resolve_review_contract
        try:
            inherited = resolve_review_contract(parent_plan)
        except (ValueError, OSError, UnicodeError) as exc:
            raise Misuse(f"Cannot inherit parent review contract: {exc}") from exc
        if args.review_boundary and args.review_boundary != inherited[0]:
            raise Misuse("--review-boundary conflicts with the canonical parent review boundary.")

    stamp = validate_timestamp(args.timestamp) if args.timestamp else now_stamp()
    created_at = now_iso()
    slug = slugify(args.slug or args.task)
    mode = "delegated" if parent_plan else args.mode
    stem = f"{stamp}_{slug}"
    if parent_plan:
        stem = f"{parent_plan.stem}__{slugify(args.lane or slug)}"

    plan_dir = choose_plan_dir(args.plan_dir, parent_plan)
    plan_path = plan_dir / f"{stem}.md"
    prompt_path = plan_dir / f"{stem}__phase-prompts.md"
    checkpoint_path = Path("docs/agents") / f"{stem}-state.md"
    state_path = Path(".codex/state") / f"{stem}.json"

    include_checkpoint = profile in {"resumable", "orchestrated", "legacy"} and not args.no_continuation
    include_state = profile in {"orchestrated", "legacy"} or args.state_only

    values = {
        "task": args.task,
        "task_id": stem,
        "mode": mode,
        "profile": profile,
        "created_at": created_at,
        "plan_path": portable(plan_path),
        "parent_plan_display": display_path(parent_plan),
        "phase_prompts_display": display_path(prompt_path if include_prompts else None),
        "continuation_state_display": display_path(checkpoint_path if include_checkpoint else None),
        "state_display": display_path(state_path if include_state else None),
        **(task_store_values(args, checkpoint_path if include_checkpoint and not args.state_only else None, profile)
           if args.plan_kind == "execution" else {}),
        **prompt_metadata,
    }
    if inherited:
        values["local_final_header"] = f"- Local final phase: {values['final_phase']}\n"
        values["review_boundary"], values["final_phase"] = inherited

    planned: list[tuple[Path, str]] = []

    if args.plan_kind == "design":
        planned.append((plan_path, render("design-plan-template.md", values)))
        planned.append((checkpoint_path, render("design-checkpoint-template.md", values)))
    elif not args.state_only:
        try:
            approved_design_link = Path(os.path.relpath(approved_design.resolve(), Path.cwd().resolve()))
        except ValueError as exc:
            raise Misuse("Approved design cannot be represented by a portable relative path from this repository.") from exc
        values["approved_design_display"] = display_path(approved_design_link)
        planned.append((plan_path, render("plan-template.md", values)))
        if include_prompts:
            planned.append((prompt_path, render("phase-prompts-template.md", values)))
        if include_checkpoint:
            planned.append((checkpoint_path, render("continuation-state-template.md", values)))
    if include_state:
        planned.append((state_path, render_json(values)))

    if any(path.resolve() == protected.resolve() for path, _ in planned for protected in protected_design_paths):
        raise Misuse("An output would overwrite the approved design or its checkpoint; choose a different task stem or directory.")

    # Every target is checked before any of them is written. Writing until the first
    # collision leaves half an artifact family behind, and the next run then cannot start
    # without --force even though the conflict was never the caller's doing.
    if not args.force:
        colliding = [path for path, _ in planned if path.exists()]
        if colliding:
            print(
                "Refusing to overwrite existing files; nothing was written: "
                + ", ".join(portable(path) for path in colliding)
                + ". Continue that artifact family instead, or pass --force to replace it.",
                file=sys.stderr,
            )
            return 1

    if not args.dry_run:
        for path, content in planned:
            write_text(path, content)

    payload: dict[str, Any] = {
        "task": args.task,
        "plan_kind": args.plan_kind,
        "mode": mode,
        "profile": profile,
        "task_store": args.task_store,
        "outputs": [portable(path) for path, _ in planned],
    }
    print(json.dumps(payload, indent=2, ensure_ascii=True))
    return 0


def main() -> int:
    args = parse_args()
    try:
        return run(args)
    except Misuse as exc:
        print(f"MISUSE: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    # A generator that could not run must not leave through Python's default exit 1, which
    # this script already uses for the one recoverable outcome: existing files it refused to
    # replace. Anything else that raises is exit 2, so no caller reads it as a write conflict.
    try:
        sys.exit(main())
    except (OSError, UnicodeDecodeError) as exc:
        print(f"MISUSE: could not read or write a required file: {exc}", file=sys.stderr)
        sys.exit(2)
    except Exception:  # noqa: BLE001 - a generator bug is not a write conflict
        traceback.print_exc()
        print("MISUSE: the initializer raised; no artifact set can be assumed.", file=sys.stderr)
        sys.exit(2)
