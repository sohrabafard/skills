#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "vendor" / "subtrees.json"
DEFAULT_DEST_ROOT = Path.home() / ".codex" / "skills"


@dataclass(frozen=True)
class VendorEntry:
    name: str
    prefix: str


@dataclass(frozen=True)
class SkillRecord:
    vendor_name: str
    vendor_prefix: str
    skill_name: str
    skill_dir: Path


def load_vendors() -> list[VendorEntry]:
    raw = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    entries = raw.get("subtrees", [])
    vendors: list[VendorEntry] = []
    for entry in entries:
        prefix = str(entry["prefix"])
        skills_root = ROOT / prefix / "skills"
        if not skills_root.exists():
            continue
        vendors.append(VendorEntry(name=str(entry["name"]), prefix=prefix))
    return vendors


def discover_skills(vendors: list[VendorEntry]) -> list[SkillRecord]:
    records: list[SkillRecord] = []
    for vendor in vendors:
        skills_root = ROOT / vendor.prefix / "skills"
        for skill_dir in sorted([p for p in skills_root.iterdir() if p.is_dir() and (p / "SKILL.md").exists()]):
            records.append(
                SkillRecord(
                    vendor_name=vendor.name,
                    vendor_prefix=vendor.prefix,
                    skill_name=skill_dir.name,
                    skill_dir=skill_dir,
                )
            )
    return records


def normalize_path(path: Path) -> str:
    return os.path.normcase(str(path.resolve(strict=False)))


def destination_for(record: SkillRecord, dest_root: Path) -> Path:
    return dest_root / record.skill_name


def installed_state(record: SkillRecord, dest_root: Path) -> tuple[str, str]:
    dest = destination_for(record, dest_root)
    if dest.is_symlink():
        target = normalize_path(dest)
        expected = normalize_path(record.skill_dir)
        if target == expected:
            return "linked", str(dest.resolve(strict=False))
        return "linked-other", str(dest.resolve(strict=False))
    if dest.exists():
        return "occupied", str(dest)
    return "missing", str(dest)


def apply_vendor_filter(records: list[SkillRecord], vendor_filters: list[str]) -> list[SkillRecord]:
    if not vendor_filters:
        return records
    allowed = set(vendor_filters)
    return [record for record in records if record.vendor_name in allowed]


def select_records(records: list[SkillRecord], args: argparse.Namespace, *, require_explicit: bool) -> list[SkillRecord]:
    filtered = apply_vendor_filter(records, args.vendor)
    if args.all:
        selected = filtered
    else:
        names = set(args.skill)
        prefixes = list(args.skill_prefix)
        selected = [
            record
            for record in filtered
            if (record.skill_name in names) or any(record.skill_name.startswith(prefix) for prefix in prefixes)
        ]
    if require_explicit and not selected:
        raise SystemExit("[vendor-skill-links] no skills matched the requested selection")
    return selected


def ensure_unique_destinations(records: list[SkillRecord], dest_root: Path) -> None:
    by_dest: dict[Path, list[SkillRecord]] = {}
    for record in records:
        by_dest.setdefault(destination_for(record, dest_root), []).append(record)
    collisions = {dest: items for dest, items in by_dest.items() if len(items) > 1}
    if not collisions:
        return
    lines = ["[vendor-skill-links] selection produces name collisions:"]
    for dest, items in collisions.items():
        sources = ", ".join(f"{item.vendor_name}/{item.skill_name}" for item in items)
        lines.append(f"- {dest.name}: {sources}")
    raise SystemExit("\n".join(lines))


def print_vendors(vendors: list[VendorEntry], records: list[SkillRecord]) -> None:
    counts: dict[str, int] = {}
    for record in records:
        counts[record.vendor_name] = counts.get(record.vendor_name, 0) + 1
    for vendor in vendors:
        print(f"- {vendor.name}: prefix={vendor.prefix} skills={counts.get(vendor.name, 0)}")


def print_records(records: list[SkillRecord], dest_root: Path) -> None:
    for record in records:
        state, detail = installed_state(record, dest_root)
        print(f"- {record.skill_name}: vendor={record.vendor_name} state={state} path={detail}")


def create_symlink(source: Path, dest: Path) -> None:
    try:
        os.symlink(str(source), str(dest), target_is_directory=True)
    except OSError as exc:
        raise SystemExit(
            "[vendor-skill-links] failed to create symlink. "
            "On Windows, enable Developer Mode or run with the required permissions."
        ) from exc


def link_records(records: list[SkillRecord], dest_root: Path, *, dry_run: bool) -> int:
    ensure_unique_destinations(records, dest_root)
    if not dry_run:
        dest_root.mkdir(parents=True, exist_ok=True)
    exit_code = 0
    for record in records:
        dest = destination_for(record, dest_root)
        state, detail = installed_state(record, dest_root)
        if state == "linked":
            print(f"[vendor-skill-links] exists: {record.skill_name} -> {detail}")
            continue
        if state in {"occupied", "linked-other"}:
            print(
                f"[vendor-skill-links] conflict: {record.skill_name} cannot link because destination is {state} ({detail})",
                file=sys.stderr,
            )
            exit_code = 1
            continue
        if dry_run:
            print(f"[vendor-skill-links] would link: {record.skill_name} -> {record.skill_dir}")
            continue
        create_symlink(record.skill_dir, dest)
        print(f"[vendor-skill-links] linked: {record.skill_name} -> {record.skill_dir}")
    return exit_code


def unlink_records(records: list[SkillRecord], dest_root: Path, *, dry_run: bool) -> int:
    ensure_unique_destinations(records, dest_root)
    exit_code = 0
    for record in records:
        dest = destination_for(record, dest_root)
        state, detail = installed_state(record, dest_root)
        if state == "missing":
            print(f"[vendor-skill-links] missing: {record.skill_name}")
            continue
        if state == "linked":
            if dry_run:
                print(f"[vendor-skill-links] would unlink: {record.skill_name} -> {detail}")
                continue
            dest.unlink()
            print(f"[vendor-skill-links] unlinked: {record.skill_name}")
            continue
        print(
            f"[vendor-skill-links] skip: {record.skill_name} destination is {state} ({detail})",
            file=sys.stderr,
        )
        exit_code = 1
    return exit_code


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Selectively expose vendored skills to Codex without linking every vendor skill pack."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    vendors_parser = subparsers.add_parser("vendors", help="List vendored skill packs that expose a skills directory.")
    vendors_parser.add_argument("--dest-root", default=str(DEFAULT_DEST_ROOT), help=argparse.SUPPRESS)

    list_parser = subparsers.add_parser("list", help="List vendored skills and whether each one is currently linked.")
    list_parser.add_argument("--vendor", action="append", default=[], help="Filter by vendor name from vendor/subtrees.json")
    list_parser.add_argument("--skill", action="append", default=[], help="Filter by exact skill name")
    list_parser.add_argument("--skill-prefix", action="append", default=[], help="Filter by skill name prefix")
    list_parser.add_argument("--all", action="store_true", help="List all matching skills after vendor filtering")
    list_parser.add_argument("--dest-root", default=str(DEFAULT_DEST_ROOT), help="Destination Codex skills directory")

    for command_name, help_text in [
        ("link", "Create symlinks for a selected subset of vendored skills."),
        ("unlink", "Remove symlinks for a selected subset of vendored skills."),
    ]:
        action_parser = subparsers.add_parser(command_name, help=help_text)
        action_parser.add_argument("--vendor", action="append", default=[], help="Filter by vendor name")
        action_parser.add_argument("--skill", action="append", default=[], help="Select an exact skill name")
        action_parser.add_argument(
            "--skill-prefix",
            action="append",
            default=[],
            help="Select every skill whose name starts with the given prefix",
        )
        action_parser.add_argument("--all", action="store_true", help="Select all skills after vendor filtering")
        action_parser.add_argument("--dest-root", default=str(DEFAULT_DEST_ROOT), help="Destination Codex skills directory")
        action_parser.add_argument("--dry-run", action="store_true", help="Show actions without changing the filesystem")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    vendors = load_vendors()
    records = discover_skills(vendors)
    dest_root = Path(args.dest_root)

    if args.command == "vendors":
        print_vendors(vendors, records)
        return 0

    if args.command == "list":
        filtered = apply_vendor_filter(records, args.vendor)
        if args.skill or args.skill_prefix:
            filtered = select_records(filtered, args, require_explicit=True)
        elif not args.all and args.vendor:
            filtered = filtered
        elif not args.all:
            filtered = records
        print_records(filtered, dest_root)
        return 0

    if args.command == "link":
        selected = select_records(records, args, require_explicit=True)
        return link_records(selected, dest_root, dry_run=args.dry_run)

    if args.command == "unlink":
        selected = select_records(records, args, require_explicit=True)
        return unlink_records(selected, dest_root, dry_run=args.dry_run)

    parser.error(f"unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
