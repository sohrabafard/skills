#!/usr/bin/env python3
"""Check WSL installer output while intercepting all installation commands."""

from __future__ import annotations

import os
import pathlib
import pty
import select
import shutil
import subprocess
import tempfile


ANSI = "\x1b["


def fixture_tree(root: pathlib.Path, wrappers: pathlib.Path) -> pathlib.Path:
    fixture = root / "fixture"
    skill = fixture / "skills" / "sample"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("fixture\n", encoding="utf-8")
    script = pathlib.Path(__file__).resolve().parents[1] / "install-skills.wsl.sh"
    shutil.copy2(script, fixture / script.name)
    (fixture / "install-skills.md").write_text(
        '## Source roots\n```text\n"skills"\n```\n', encoding="utf-8"
    )

    wrappers.mkdir()
    for command in ("mkdir", "ln"):
        wrapper = wrappers / command
        wrapper.write_text(
            "#!/bin/sh\n"
            'printf "%s" "$0" >> "$TASK_LOG"\n'
            'printf "\\t%s" "$@" >> "$TASK_LOG"\n'
            'printf "\\n" >> "$TASK_LOG"\n',
            encoding="utf-8",
        )
        wrapper.chmod(0o755)
    return fixture


def environment(wrappers: pathlib.Path, task_log: pathlib.Path) -> dict[str, str]:
    env = os.environ.copy()
    env["PATH"] = f"{wrappers}{os.pathsep}{env['PATH']}"
    env["TASK_LOG"] = str(task_log)
    env.pop("NO_COLOR", None)
    return env


def run_redirected(
    fixture: pathlib.Path, env: dict[str, str], *args: str
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["bash", str(fixture / "install-skills.wsl.sh"), *args],
        cwd=fixture,
        env=env,
        text=True,
        capture_output=True,
        check=True,
    )


def run_pty(
    fixture: pathlib.Path, env: dict[str, str], *args: str
) -> tuple[str, str]:
    master, slave = pty.openpty()
    process = subprocess.Popen(
        ["bash", str(fixture / "install-skills.wsl.sh"), *args],
        cwd=fixture,
        env=env,
        stdin=subprocess.DEVNULL,
        stdout=slave,
        stderr=subprocess.PIPE,
    )
    os.close(slave)
    output: list[bytes] = []
    while True:
        ready, _, _ = select.select([master], [], [], 5)
        if not ready:
            process.kill()
            raise AssertionError("installer output timed out")
        try:
            chunk = os.read(master, 4096)
        except OSError:
            break
        if not chunk:
            break
        output.append(chunk)
    stderr = process.communicate(timeout=5)[1].decode()
    os.close(master)
    if process.returncode:
        raise AssertionError(f"installer exited {process.returncode}: {stderr}")
    return b"".join(output).decode(), stderr


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"PASS {message}")


def main() -> None:
    original_home = os.environ.get("HOME")
    if not original_home:
        raise RuntimeError("HOME must already be set; this check never overrides it")

    with tempfile.TemporaryDirectory(prefix="wsl-installer-output-") as temporary:
        root = pathlib.Path(temporary)
        wrappers = root / "bin"
        fixture = fixture_tree(root, wrappers)
        task_log = root / "intercepted-install-commands.log"

        plain_env = environment(wrappers, task_log)
        plain = run_redirected(fixture, plain_env, "--dry-run")
        check(
            ANSI not in plain.stdout + plain.stderr
            and plain.stdout.count("WOULD-LINK") == 2
            and "Links: 2" in plain.stdout
            and not task_log.exists(),
            "redirected dry-run is plain and performs no install commands",
        )

        link_env = environment(wrappers, task_log)
        link_env["TERM"] = "xterm"
        linked_stdout, linked_stderr = run_pty(fixture, link_env)
        linked = linked_stdout + linked_stderr
        calls = task_log.read_text(encoding="utf-8").splitlines()
        link_evidence = {
            "status_color": "\x1b[1;32mLINK" in linked,
            "codex_color": "\x1b[1;34m[codex]" in linked,
            "claude_color": "\x1b[1;35m[claude]" in linked,
            "intercepted_calls": len(calls),
        }
        if not all(link_evidence.values()) or link_evidence["intercepted_calls"] != 4:
            raise AssertionError(f"TTY LINK presentation/effect mismatch: {link_evidence}")
        check(True, "TTY LINK is colored by status/runtime; install calls are intercepted")

        for name, changes in (
            ("NO_COLOR", {"NO_COLOR": "1"}),
            ("TERM=dumb", {"TERM": "dumb"}),
        ):
            env = environment(wrappers, root / f"{name}.log")
            env.update(changes)
            stdout, stderr = run_pty(fixture, env)
            check(ANSI not in stdout + stderr, f"{name} disables ANSI on a TTY")

        empty_no_color = environment(wrappers, root / "empty-no-color.log")
        empty_no_color["NO_COLOR"] = ""
        stdout, stderr = run_pty(fixture, empty_no_color)
        check(
            ANSI in stdout + stderr,
            "empty NO_COLOR follows documented non-empty disable semantics",
        )

        help_result = run_redirected(fixture, plain_env, "--help")
        usage_result = subprocess.run(
            ["bash", str(fixture / "install-skills.wsl.sh"), "--invalid"],
            cwd=fixture,
            env=plain_env,
            text=True,
            capture_output=True,
        )
        check(
            "NO_COLOR" in help_result.stdout and usage_result.returncode == 2,
            "help documents NO_COLOR and usage errors retain exit status 2",
        )


if __name__ == "__main__":
    main()
