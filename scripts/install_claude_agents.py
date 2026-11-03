#!/usr/bin/env python3
"""Install the repository's personal Claude Code agents."""

from __future__ import annotations

import argparse
from contextlib import contextmanager
from dataclasses import dataclass
import fcntl
import json
import os
from pathlib import Path
import stat
import sys
import tempfile

PACK = Path(__file__).resolve().parents[1] / "skills/sohrab"
ORCHESTRATOR_AGENTS = PACK / "alaa-cc-orchestrator/agents"
WRITER = "alaa-rule-writer"
WRITER_SOURCE = PACK / "alaa-prompting-guide/assets/rule-writer/claude" / f"{WRITER}.md"
ARCHIVE_DIR = "alaa-agent-backups"
MANIFEST = Path(".claude-plugin/plugin.json")


class Conflict(Exception):
    """An input or target failed a safety check."""


@dataclass(frozen=True)
class Agent:
    target: Path
    source: bytes
    previous: bytes | None

    @property
    def action(self) -> str:
        if self.previous == self.source:
            return "unchanged"
        return "create" if self.previous is None else "update"


@dataclass(frozen=True)
class Plan:
    agents: list[Agent]
    archive_root: Path
    legacy: Path | None


def check_type(path: Path, expected, *, required: bool = False) -> bool:
    try:
        mode = path.lstat().st_mode
    except FileNotFoundError:
        if required:
            raise Conflict(f"Missing required path: {path}") from None
        return False
    if not expected(mode):
        raise Conflict(f"Unexpected file type or symlink: {path}")
    return True


def unique_fields(pairs: list[tuple[str, object]]) -> dict[str, object]:
    fields = {}
    for key, value in pairs:
        if key in fields:
            raise ValueError("Duplicate manifest key")
        fields[key] = value
    return fields


def reject_constant(value: str) -> None:
    raise ValueError(f"Invalid JSON constant: {value}")


def inspect_legacy(skills: Path) -> Path | None:
    legacy = skills / WRITER
    if not check_type(legacy, stat.S_ISDIR):
        return None

    manifest = legacy / MANIFEST
    check_type(manifest.parent, stat.S_ISDIR, required=True)
    check_type(manifest, stat.S_ISREG, required=True)
    try:
        metadata = json.loads(
            manifest.read_bytes(), object_pairs_hook=unique_fields,
            parse_constant=reject_constant,
        )
    except (ValueError, RecursionError):
        raise Conflict(f"Invalid plugin manifest: {manifest}") from None
    if not isinstance(metadata, dict) or metadata.get("name") != WRITER:
        raise Conflict(f"Manifest name must be {WRITER}: {manifest}")

    directories = [legacy]
    while directories:
        for entry in directories.pop().iterdir():
            mode = entry.lstat().st_mode
            if stat.S_ISDIR(mode):
                directories.append(entry)
            elif not stat.S_ISREG(mode):
                raise Conflict(f"Unexpected file type or symlink: {entry}")
    return legacy


def source_inventory(only: str | None) -> list[Path]:
    sources = [WRITER_SOURCE]
    if only is None:
        check_type(ORCHESTRATOR_AGENTS, stat.S_ISDIR, required=True)
        wrappers = sorted(ORCHESTRATOR_AGENTS.glob("*.md"))
        if not wrappers:
            raise Conflict(f"No agent definitions in {ORCHESTRATOR_AGENTS}")
        sources = wrappers + sources

    names = set()
    for source in sources:
        for directory in reversed(source.parents):
            check_type(directory, stat.S_ISDIR, required=True)
        check_type(source, stat.S_ISREG, required=True)
        if source.name in names:
            raise Conflict(f"Duplicate agent destination: {source.name}")
        names.add(source.name)
    return sources


def preflight(home: Path, only: str | None) -> Plan:
    if ".." in home.parts:
        raise Conflict("Claude home must not contain '..' path components")
    for directory in (*reversed(home.parents), home):
        check_type(directory, stat.S_ISDIR, required=True)

    agents = home / "agents"
    skills = home / "skills"
    archive_root = home / ARCHIVE_DIR
    check_type(agents, stat.S_ISDIR)
    check_type(archive_root, stat.S_ISDIR)
    check_type(skills, stat.S_ISDIR, required=True)
    # A personal skill can point to a separate checkout.
    dependency = skills / "alaa-prompting-guide/SKILL.md"
    if not dependency.is_file():
        raise Conflict(f"Missing required personal skill: {dependency}")
    with dependency.open("rb") as skill:
        skill.read(1)

    legacy = inspect_legacy(skills)
    selected = []
    for source in source_inventory(only):
        target = agents / source.name
        previous = target.read_bytes() if check_type(target, stat.S_ISREG) else None
        selected.append(Agent(target, source.read_bytes(), previous))
    return Plan(selected, archive_root, legacy)


@contextmanager
def installer_lock(home: Path):
    # Lock the existing directory so previews and no-ops need no lock file.
    descriptor = os.open(home, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        try:
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise Conflict(f"Another installer holds the lock on {home}") from None
        yield
    finally:
        os.close(descriptor)


def publish(target: Path, content: bytes) -> None:
    with tempfile.NamedTemporaryFile(
        dir=target.parent, prefix=".alaa-agent-", suffix=".tmp", delete=False
    ) as staged:
        staged_path = Path(staged.name)
        try:
            staged.write(content)
            staged.close()
            os.replace(staged_path, target)
        finally:
            staged_path.unlink(missing_ok=True)


def apply(plan: Plan) -> None:
    archive = None
    if plan.legacy or any(agent.action == "update" for agent in plan.agents):
        plan.archive_root.mkdir(mode=0o700, exist_ok=True)
        archive = Path(tempfile.mkdtemp(prefix="install-", dir=plan.archive_root))
        print(f"Backup directory: {archive}", flush=True)

    for agent in plan.agents:
        if agent.action != "unchanged":
            agent.target.parent.mkdir(exist_ok=True)
            if agent.previous is not None:
                assert archive is not None
                publish(archive / agent.target.name, agent.previous)
            publish(agent.target, agent.source)
        print(f"{agent.action}: {agent.target}", flush=True)

    if plan.legacy is not None:
        assert archive is not None
        writer = next(agent for agent in plan.agents if agent.target.stem == WRITER)
        if writer.target.read_bytes() != writer.source:
            raise Conflict(f"Installed rule-writer differs from source: {writer.target}")
        archived_plugin = archive / WRITER
        plan.legacy.rename(archived_plugin)
        print(f"archive: {plan.legacy} -> {archived_plugin}", flush=True)


def main(argv: list[str] | None = None, *, only_writer: bool = False) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="preview only (default)")
    mode.add_argument("--apply", action="store_true", help="install selected personal agents")
    parser.add_argument(
        "--claude-home", type=Path, metavar="PATH",
        help="Claude config directory (default: CLAUDE_CONFIG_DIR or ~/.claude)",
    )
    if not only_writer:
        parser.add_argument("--only", choices=[WRITER], help="install only rule-writer")
    args = parser.parse_args(argv)

    try:
        configured = os.environ.get("CLAUDE_CONFIG_DIR")
        home = args.claude_home or (Path(configured) if configured else Path.home() / ".claude")
        home = home.expanduser().absolute()
        only = WRITER if only_writer else args.only
        plan = preflight(home, only)
        if args.apply:
            with installer_lock(home):
                apply(preflight(home, only))
        else:
            for agent in plan.agents:
                print(f"dry-run {agent.action}: {agent.target}")
            if plan.legacy is not None:
                print(f"dry-run archive: {plan.legacy} -> {plan.archive_root}")
        return 0
    except Conflict as error:
        print(f"Conflict: {error}", file=sys.stderr)
        return 1
    except (OSError, RuntimeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
