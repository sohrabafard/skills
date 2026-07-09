#!/usr/bin/env python3
"""Create adaptive Alaa workflow artifacts from a repository root."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
PROFILES = ("direct", "resumable", "orchestrated", "legacy")
UNRESOLVED = "NEEDS_LIVE_VERIFICATION"


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


def write_text(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"Refusing to overwrite existing file: {path}")
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
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", required=True, help="Human task title used for naming and template fill.")
    parser.add_argument("--profile", choices=PROFILES, help="Artifact profile. Defaults to direct.")
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
        raise ValueError("timestamp must match YYYYMMDD-HHMMSS")
    return stamp


def resolve_profile(args: argparse.Namespace) -> str:
    profile = args.profile or "direct"
    if args.with_state:
        warn("--with-state is a compatibility alias; use --profile orchestrated or legacy.")
        profile = "legacy" if args.profile is None else ("orchestrated" if profile != "legacy" else profile)
    if args.state_only:
        warn("--state-only is a compatibility alias; prefer an orchestrated profile with its plan.")
        profile = "orchestrated" if args.profile is None else profile
    if args.no_continuation:
        warn("--no-continuation is compatibility-only and produces a legacy exception.")
        if profile != "direct":
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
    if any(fields) and not all(fields):
        raise SystemExit("Provide all implementer/reviewer runtime and model values together.")
    if not active and (any(fields) or args.verified_on or args.verification_source):
        raise SystemExit("Prompt verification metadata requires --with-prompts.")
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
        }
    if not args.verified_on or not args.verification_source:
        raise SystemExit("Resolved prompt metadata requires --verified-on and at least one --verification-source.")
    verified_on = args.verified_on
    try:
        date.fromisoformat(verified_on)
    except ValueError as exc:
        raise SystemExit("--verified-on must match YYYY-MM-DD") from exc
    sources = ", ".join(args.verification_source)
    return {
        "verification_status": "verified",
        "verified_on": verified_on,
        "verification_sources": sources,
        "implementer_runtime": args.implementer_runtime,
        "implementer_model": args.implementer_model,
        "reviewer_runtime": args.reviewer_runtime,
        "reviewer_model": args.reviewer_model,
    }


def main() -> int:
    args = parse_args()
    profile = resolve_profile(args)
    include_prompts = args.with_prompts or profile == "legacy"
    prompt_metadata = resolve_prompt_metadata(args, include_prompts)

    parent_plan = Path(args.parent_plan) if args.parent_plan else None
    if args.lane and parent_plan is None:
        raise SystemExit("--lane requires --parent-plan.")
    if parent_plan and not parent_plan.exists():
        raise SystemExit(f"Parent plan not found: {parent_plan}")

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

    outputs: list[Path] = []

    def emit(path: Path, content: str) -> None:
        outputs.append(path)
        if not args.dry_run:
            write_text(path, content, force=args.force)

    if not args.state_only:
        emit(plan_path, render("plan-template.md", values))
        if include_prompts:
            emit(prompt_path, render("phase-prompts-template.md", values))
        if include_checkpoint:
            emit(checkpoint_path, render("continuation-state-template.md", values))
    if include_state:
        emit(state_path, render_json(values))

    payload: dict[str, Any] = {
        "task": args.task,
        "mode": mode,
        "profile": profile,
        "outputs": [portable(path) for path in outputs],
    }
    print(json.dumps(payload, indent=2, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
