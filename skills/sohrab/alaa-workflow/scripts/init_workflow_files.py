#!/usr/bin/env python3
"""Create adaptive Alaa workflow artifacts from a repository root."""

from __future__ import annotations

import argparse
import json
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
    path.write_text(content, encoding="utf-8")


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
    parser.add_argument(
        "--profile",
        choices=PROFILES,
        help=(
            "Artifact profile. Default: resumable, because anything with more than one phase "
            "needs a checkpoint to survive compaction, a new session, or a fresh agent, and the "
            "checkpoint costs about ten lines written at four moments. Choose direct deliberately "
            "for genuinely single-phase bounded work."
        ),
    )
    parser.add_argument("--with-prompts", action="store_true", help="Create the same-stem role prompt pack.")
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
    if any(fields) and not all(fields):
        raise Misuse("Provide all implementer/reviewer runtime and model values together.")
    if any(documenter_fields) and not all(documenter_fields):
        raise Misuse("Provide documenter runtime and model values together.")
    if any(documenter_fields) and not all(fields):
        raise Misuse("Documenter metadata requires the implementer/reviewer metadata.")
    if not active and (any(fields) or any(documenter_fields) or args.verified_on or args.verification_source):
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
        "verification_status": "verified",
        "verified_on": verified_on,
        "verification_sources": sources,
        "implementer_runtime": args.implementer_runtime,
        "implementer_model": args.implementer_model,
        "reviewer_runtime": args.reviewer_runtime,
        "reviewer_model": args.reviewer_model,
        "documenter_runtime": args.documenter_runtime or "not included",
        "documenter_model": args.documenter_model or "not included",
    }


def run(args: argparse.Namespace) -> int:
    profile = resolve_profile(args)
    include_prompts = args.with_prompts or profile == "legacy"
    prompt_metadata = resolve_prompt_metadata(args, include_prompts)

    parent_plan = Path(args.parent_plan) if args.parent_plan else None
    if args.lane and parent_plan is None:
        raise Misuse("--lane requires --parent-plan.")
    if parent_plan and not parent_plan.exists():
        raise Misuse(f"Parent plan not found: {parent_plan}")

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
        **prompt_metadata,
    }

    planned: list[tuple[Path, str]] = []

    if not args.state_only:
        planned.append((plan_path, render("plan-template.md", values)))
        if include_prompts:
            planned.append((prompt_path, render("phase-prompts-template.md", values)))
        if include_checkpoint:
            planned.append((checkpoint_path, render("continuation-state-template.md", values)))
    if include_state:
        planned.append((state_path, render_json(values)))

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
        "mode": mode,
        "profile": profile,
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
