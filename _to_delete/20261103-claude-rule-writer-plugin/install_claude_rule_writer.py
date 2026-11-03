#!/usr/bin/env python3
"""Install or update the repository's Claude Code rule-writer plugin."""

from __future__ import annotations

import argparse
import fcntl
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

PLUGIN_NAME = "alaa-rule-writer"
MANIFEST = Path(".claude-plugin/plugin.json")
AGENT = Path("agents") / f"{PLUGIN_NAME}.md"
SOURCE = (
    Path(__file__).resolve().parents[1]
    / "skills/sohrab/alaa-prompting-guide/assets/rule-writer/claude"
    / AGENT.name
)
NEW_MANIFEST = {
    "name": PLUGIN_NAME,
    "version": "1.0.0",
    "description": "Alaa rule-writer agent; requires alaa-prompting-guide.",
}
VALIDATION_TIMEOUT = 30


class Conflict(Exception):
    """An input or target failed a safety check."""


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


def inspect_skills(claude_home: Path) -> Path:
    if ".." in claude_home.parts:
        raise Conflict("Claude home must not contain '..' path components")
    skills = claude_home / "skills"
    for directory in (*reversed(skills.parents), skills):
        check_type(directory, stat.S_ISDIR, required=True)

    # Personal skills can be symlinks installed from a separate checkout.
    dependency = skills / "alaa-prompting-guide/SKILL.md"
    if not dependency.is_file():
        raise Conflict(f"Missing required personal skill: {dependency}")
    with dependency.open("rb"):
        pass
    return skills


def unique_fields(pairs: list[tuple[str, object]]) -> dict[str, object]:
    fields = {}
    for key, value in pairs:
        if key in fields:
            raise ValueError("Duplicate manifest key")
        fields[key] = value
    return fields


def reject_constant(value: str) -> None:
    raise ValueError(f"Invalid JSON constant: {value}")


def inspect_target(target: Path, source: bytes) -> tuple[str, bytes, bytes | None]:
    if not check_type(target, stat.S_ISDIR):
        manifest = (json.dumps(NEW_MANIFEST, indent=2) + "\n").encode()
        return "create", manifest, None

    manifest_path = target / MANIFEST
    check_type(manifest_path.parent, stat.S_ISDIR, required=True)
    check_type(manifest_path, stat.S_ISREG, required=True)
    manifest = manifest_path.read_bytes()
    try:
        metadata = json.loads(
            manifest, object_pairs_hook=unique_fields, parse_constant=reject_constant
        )
    except (ValueError, RecursionError):
        raise Conflict(f"Invalid plugin manifest: {manifest_path}") from None
    if not isinstance(metadata, dict) or metadata.get("name") != PLUGIN_NAME:
        raise Conflict(f"Manifest name must be {PLUGIN_NAME}: {manifest_path}")

    agent = target / AGENT
    if check_type(agent.parent, stat.S_ISDIR) and check_type(agent, stat.S_ISREG):
        previous = agent.read_bytes()
    else:
        previous = None
    return ("unchanged" if previous == source else "update"), manifest, previous


def validate_candidate(candidate: Path, workspace: Path) -> None:
    claude = shutil.which("claude")
    if claude is None:
        raise OSError("Claude Code CLI (claude) is required on PATH")

    # Keep the validator away from the caller's profile, credentials and caches.
    home = workspace / "home"
    home.mkdir()
    env = {
        "PATH": os.environ.get("PATH", os.defpath),
        "HOME": str(home),
        "CLAUDE_CONFIG_DIR": str(home / ".claude"),
        "XDG_CONFIG_HOME": str(home / ".config"),
        "XDG_CACHE_HOME": str(home / ".cache"),
        "XDG_DATA_HOME": str(home / ".local/share"),
        "XDG_STATE_HOME": str(home / ".local/state"),
        "TMPDIR": str(workspace),
        "DISABLE_TELEMETRY": "1",
        "DISABLE_AUTOUPDATER": "1",
    }
    result = subprocess.run(
        [str(Path(claude).absolute()), "plugin", "validate", str(candidate)],
        cwd=home,
        env=env,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        timeout=VALIDATION_TIMEOUT,
        check=False,
    )
    if result.returncode == 1:
        raise Conflict("Claude Code rejected the candidate (plugin validate exited 1)")
    if result.returncode:
        raise OSError(f"Claude Code plugin validate exited {result.returncode}")


def publish_update(target: Path, candidate: Path, previous: bytes | None) -> None:
    agent = target / AGENT
    if not agent.parent.exists():
        (candidate / AGENT.parent).rename(agent.parent)
        return

    # Stage in the agent's directory so replacement is atomic on its filesystem.
    with tempfile.NamedTemporaryFile(
        dir=agent.parent, prefix=".rule-writer-", suffix=".tmp", delete=False
    ) as staged:
        staged_path = Path(staged.name)
        try:
            staged.write((candidate / AGENT).read_bytes())
            staged.close()
            if previous is not None:
                with tempfile.NamedTemporaryFile(
                    dir=target, prefix=f"{AGENT.name}.", suffix=".bak", delete=False
                ) as backup:
                    backup.write(previous)
                print(f"Backup: {backup.name}", flush=True)
            os.replace(staged_path, agent)
        finally:
            staged_path.unlink(missing_ok=True)


def apply(skills: Path, source: bytes) -> None:
    fd = os.open(skills, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise Conflict(f"Another installer holds the lock on {skills}") from None

        target = skills / PLUGIN_NAME
        action, manifest, previous = inspect_target(target, source)
        if action != "unchanged":
            # The immediate scratch child has no manifest. Only its nested
            # candidate does, so it is outside the skills discovery layout.
            with tempfile.TemporaryDirectory(dir=skills, prefix=".rule-writer-") as temp:
                workspace = Path(temp)
                candidate = workspace / PLUGIN_NAME
                (candidate / MANIFEST.parent).mkdir(parents=True)
                (candidate / MANIFEST).write_bytes(manifest)
                (candidate / AGENT.parent).mkdir()
                (candidate / AGENT).write_bytes(source)
                validate_candidate(candidate, workspace)
                if action == "create":
                    candidate.rename(target)
                else:
                    publish_update(target, candidate, previous)
        print(f"{action}: {target}")
    finally:
        os.close(fd)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="preview only (default)")
    mode.add_argument("--apply", action="store_true", help="validate and publish the change")
    parser.add_argument(
        "--claude-home", type=Path, metavar="PATH",
        help="Claude config directory (default: CLAUDE_CONFIG_DIR or ~/.claude)",
    )
    args = parser.parse_args()

    try:
        config_dir = os.environ.get("CLAUDE_CONFIG_DIR")
        claude_home = args.claude_home
        if claude_home is None:
            claude_home = Path(config_dir) if config_dir else Path.home() / ".claude"
        skills = inspect_skills(claude_home.expanduser().absolute())
        source = SOURCE.read_bytes()
        if args.apply:
            apply(skills, source)
        else:
            target = skills / PLUGIN_NAME
            action, _, _ = inspect_target(target, source)
            print(f"dry-run {action}: {target}")
        return 0
    except Conflict as error:
        print(f"Conflict: {error}", file=sys.stderr)
        return 1
    except subprocess.TimeoutExpired:
        print(f"Error: Claude Code validation exceeded {VALIDATION_TIMEOUT}s", file=sys.stderr)
        return 2
    except (OSError, RuntimeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
