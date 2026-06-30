#!/usr/bin/env python3
"""Create Alaa workflow plan/state/phase-prompt artifacts.

Run from a repository root. By default, parent plans also get a same-stem
`__phase-prompts.md` file and a `docs/agents/<stem>-state.md` continuation file.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "task"


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


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"Refusing to overwrite existing file: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def render_markdown(template_name: str, values: dict[str, str]) -> str:
    content = read_text(ASSETS / template_name)
    for key, value in values.items():
        content = content.replace(f"{{{{{key}}}}}", value)
    return content


def render_json(values: dict[str, str]) -> str:
    content = read_text(ASSETS / "state-template.json")
    for key, value in values.items():
        content = content.replace(f"{{{{{key}}}}}", value)
    data = json.loads(content)
    return json.dumps(data, indent=2, ensure_ascii=True) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", required=True, help="Human task title used for naming and template fill.")
    parser.add_argument("--slug", help="Optional explicit slug. Defaults to a slugified task title.")
    parser.add_argument(
        "--mode",
        default="plan",
        choices=["plan", "execute", "resume", "delegated", "review"],
        help="Primary workflow mode for the created artifact.",
    )
    parser.add_argument(
        "--plan-dir",
        default="auto",
        help="Plan directory to use. Defaults to auto selection between docs/_agent_plans and docs/plan.",
    )
    parser.add_argument("--with-state", action="store_true", help="Also create a matching .codex/state JSON file.")
    parser.add_argument("--state-only", action="store_true", help="Create only the state file.")
    parser.add_argument("--lane", help="Optional lane name for child-lane artifacts.")
    parser.add_argument("--parent-plan", help="Required for lane mode. Path to the parent plan file.")
    parser.add_argument("--timestamp", help="Optional fixed timestamp in YYYYMMDD-HHMMSS format.")
    parser.add_argument("--force", action="store_true", help="Overwrite output files if they already exist.")
    parser.add_argument("--dry-run", action="store_true", help="Print paths without writing files.")
    parser.add_argument(
        "--no-continuation",
        action="store_true",
        help="Do not create docs/agents/<stem>-state.md. Use only when file creation is constrained.",
    )
    return parser.parse_args()


def validate_timestamp(stamp: str) -> str:
    if not re.match(r"^\d{8}-\d{6}$", stamp):
        raise ValueError("timestamp must match YYYYMMDD-HHMMSS")
    return stamp


def main() -> int:
    args = parse_args()

    parent_plan = Path(args.parent_plan) if args.parent_plan else None
    if args.lane and parent_plan is None:
        raise SystemExit("--lane requires --parent-plan so child artifacts can stay adjacent to the parent stem.")
    if parent_plan and not parent_plan.exists():
        raise SystemExit(f"Parent plan not found: {parent_plan}")

    stamp = validate_timestamp(args.timestamp) if args.timestamp else now_stamp()
    created_at = now_iso()
    slug = slugify(args.slug or args.task)

    is_lane = parent_plan is not None
    if is_lane:
        stem = parent_plan.stem
        parent_task_id = stem
        lane = slugify(args.lane or slug)
        stem = f"{stem}__{lane}"
        mode = "delegated"
        lane_key = lane
        lane_scope = "lane-owned execution"
    else:
        stem = f"{stamp}_{slug}"
        parent_task_id = ""
        lane = ""
        mode = args.mode
        lane_key = "parent"
        lane_scope = "orchestration and integration"

    plan_dir = choose_plan_dir(args.plan_dir, parent_plan)
    plan_path = plan_dir / f"{stem}.md"
    state_path = Path(".codex/state") / f"{stem}.json"
    phase_prompts_path = plan_dir / f"{stem}__phase-prompts.md" if not is_lane else plan_dir / f"{parent_plan.stem}__phase-prompts.md"
    continuation_state_path = Path("docs/agents") / f"{stem}-state.md"

    values = {
        "task": args.task,
        "task_id": stem,
        "parent_task_id": parent_task_id,
        "parent_plan_path": str(parent_plan).replace("\\", "/") if parent_plan else "",
        "lane": lane,
        "created_at": created_at,
        "mode": mode,
        "plan_path": str(plan_path).replace("\\", "/"),
        "phase_prompts_path": str(phase_prompts_path).replace("\\", "/"),
        "continuation_state_path": str(continuation_state_path).replace("\\", "/"),
        "state_path": str(state_path).replace("\\", "/"),
        "parent_task_id_json": json.dumps(parent_task_id or None),
        "parent_plan_path_json": json.dumps(str(parent_plan).replace("\\", "/") if parent_plan else None),
        "lane_json": json.dumps(lane or None),
        "lane_key_json": json.dumps(lane_key),
        "lane_scope_json": json.dumps(lane_scope),
    }

    outputs: list[Path] = []

    if not args.state_only:
        template_name = "lane-plan-template.md" if is_lane else "plan-template.md"
        plan_text = render_markdown(template_name, values)
        outputs.append(plan_path)
        if not args.dry_run:
            write_text(plan_path, plan_text, force=args.force)

        if not is_lane:
            phase_text = render_markdown("phase-prompts-template.md", values)
            outputs.append(phase_prompts_path)
            if not args.dry_run:
                write_text(phase_prompts_path, phase_text, force=args.force)

        if not args.no_continuation:
            continuation_text = render_markdown("continuation-state-template.md", values)
            outputs.append(continuation_state_path)
            if not args.dry_run:
                write_text(continuation_state_path, continuation_text, force=args.force)

    if args.with_state or args.state_only:
        state_text = render_json(values)
        outputs.append(state_path)
        if not args.dry_run:
            write_text(state_path, state_text, force=args.force)

    payload: dict[str, Any] = {
        "task": args.task,
        "mode": mode,
        "outputs": [str(path).replace("\\", "/") for path in outputs],
    }
    print(json.dumps(payload, indent=2, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
