#!/usr/bin/env python3
"""Check WSL installer output while intercepting all installation commands."""

from __future__ import annotations

import errno
import os
import pathlib
import pty
import select
import shlex
import shutil
import subprocess
import tempfile
import time


ANSI = "\x1b["
TIMEOUT = 5


def system_command(name: str) -> str:
    command = shutil.which(name, path=os.defpath)
    if command is None:
        raise RuntimeError(f"missing system command: {name}")
    return str(pathlib.Path(command).resolve(strict=True))


def fixture_tree(root: pathlib.Path, wrappers: pathlib.Path, name: str) -> pathlib.Path:
    fixture = root / "fixture"
    for source_root in ("skills", "conflict"):
        skill = fixture / source_root / name
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text("fixture\n", encoding="utf-8")
    script = pathlib.Path(__file__).resolve().parents[1] / "install-skills.wsl.sh"
    shutil.copy2(script, fixture / script.name)
    write_roots(fixture, "skills")

    wrappers.mkdir()
    # No fallback to system mkdir/ln is available in the fixture PATH.
    for command in ("cat", "dirname", "readlink", "uname"):
        (wrappers / command).symlink_to(system_command(command))
    for command in ("mkdir", "ln"):
        wrapper = wrappers / command
        wrapper.write_text(
            "#!/bin/sh\n"
            'printf "%s\\000" "$0" "$@" >> "$TASK_LOG"\n',
            encoding="utf-8",
        )
        wrapper.chmod(0o755)
    return fixture


def write_roots(fixture: pathlib.Path, *roots: str) -> None:
    entries = "".join(f'"{root}"\n' for root in roots)
    (fixture / "install-skills.md").write_text(
        f"## Source roots\n```text\n{entries}```\n", encoding="utf-8"
    )


def environment(
    parent: dict[str, str], wrappers: pathlib.Path, task_log: pathlib.Path
) -> dict[str, str]:
    # Preserve the home values under test without importing startup, functions or PATH.
    env = {key: parent[key] for key in ("HOME", "CODEX_HOME") if key in parent}
    env.update(PATH=str(wrappers), TASK_LOG=str(task_log), TERM="xterm")
    return env


def command(bash: str, fixture: pathlib.Path, *args: str) -> list[str]:
    return [bash, "-p", str(fixture / "install-skills.wsl.sh"), *args]


def run_redirected(
    bash: str, fixture: pathlib.Path, env: dict[str, str], *args: str, expected: int = 0
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        command(bash, fixture, *args),
        cwd=fixture,
        env=env,
        stdin=subprocess.DEVNULL,
        text=True,
        capture_output=True,
        timeout=TIMEOUT,
    )
    if result.returncode != expected:
        raise AssertionError(f"installer exited {result.returncode}: {result.stderr}")
    return result


def run_pty(
    bash: str, fixture: pathlib.Path, env: dict[str, str], *args: str, tty: str = "stdout"
) -> tuple[str, str]:
    master, slave = pty.openpty()
    try:
        with tempfile.TemporaryFile(dir=fixture) as redirected:
            with subprocess.Popen(
                command(bash, fixture, *args),
                cwd=fixture,
                env=env,
                stdin=subprocess.DEVNULL,
                stdout=slave if tty == "stdout" else redirected,
                stderr=slave if tty == "stderr" else redirected,
            ) as process:
                os.close(slave)
                slave = None
                deadline = time.monotonic() + TIMEOUT
                output = bytearray()
                try:
                    while True:
                        remaining = deadline - time.monotonic()
                        if remaining <= 0 or not select.select([master], [], [], remaining)[0]:
                            raise AssertionError(f"installer {tty} timed out")
                        try:
                            chunk = os.read(master, 4096)
                        except OSError as error:
                            if error.errno != errno.EIO:
                                raise
                            break
                        if not chunk:
                            break
                        output.extend(chunk)
                    process.wait(timeout=max(0, deadline - time.monotonic()))
                finally:
                    if process.poll() is None:
                        process.kill()
                        process.wait()
                redirected.seek(0)
                tty_output = output.decode()
                other_output = redirected.read().decode()
                if process.returncode:
                    raise AssertionError(f"installer exited {process.returncode}: {tty_output}{other_output}")
                return (tty_output, other_output) if tty == "stdout" else (other_output, tty_output)
    finally:
        if slave is not None:
            os.close(slave)
        os.close(master)


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"PASS {message}")


def require_absent(destinations: list[str]) -> None:
    for destination in destinations:
        try:
            pathlib.Path(destination).lstat()
        except FileNotFoundError:
            continue
        raise AssertionError(f"live installer destination exists: {destination}")


def hostile_environment(
    root: pathlib.Path, parent: dict[str, str]
) -> tuple[dict[str, str], pathlib.Path]:
    marker = root / "unexpected-shell-startup"
    # Every hostile hook is benign even if it executes. It can only mark the fixture.
    mark = f'printf "%s\\n" hostile >> {shlex.quote(str(marker))}'
    startup = root / "bash-env"
    startup.write_text(mark + "\n", encoding="utf-8")
    fake_bash = root / "bash"
    fake_bash.write_text("#!/bin/sh\n" + mark + "\n", encoding="utf-8")
    fake_bash.chmod(0o755)
    hostile = dict(parent)
    hostile.update(BASH_ENV=str(startup), PATH=str(root))
    for name in ("mkdir", "ln"):
        hostile[f"BASH_FUNC_{name}%%"] = f"() {{ {mark}; }}"
    return hostile, marker


def main() -> None:
    parent = dict(os.environ)
    if not os.path.isabs(parent.get("HOME", "")):
        raise RuntimeError("HOME must already be an absolute path; this check never overrides it")
    bash = system_command("bash")

    with tempfile.TemporaryDirectory(prefix="wsl-installer-output-", dir="/tmp") as temporary:
        root = pathlib.Path(temporary).resolve()
        name = root.name
        wrappers = root / "bin"
        fixture = fixture_tree(root, wrappers, name)
        destinations = [f"{parent['HOME']}/.{runtime}/skills/{name}"
                        for runtime in ("codex", "claude")]
        require_absent(destinations)
        source = fixture / "skills" / name
        task_log = root / "intercepted-install-commands.log"
        plain_env = environment(parent, wrappers, task_log)

        write_roots(fixture, "skills", "conflict", "missing")
        plain = run_redirected(bash, fixture, plain_env, "--dry-run")
        check(
            ANSI not in plain.stdout + plain.stderr
            and plain.stdout.count("WOULD-LINK") == 2
            and plain.stdout.count("EXIST ") == 2
            and plain.stderr.count("WARN skipped: different target: ") == 2
            and "WARN source root missing, skipped: " in plain.stderr
            and "Links: 2  Existing/skipped: 2  Conflicts: 2  Dry run: true" in plain.stdout
            and not task_log.exists(),
            "redirected dry-run reports conflicts without ANSI or install commands",
        )
        stdout, stderr = run_pty(bash, fixture, plain_env, "--dry-run")
        check(
            stdout.count("\x1b[1;36mWOULD-LINK") == 2
            and stdout.count("\x1b[1;90mEXIST") == 2
            and ANSI not in stderr
            and not task_log.exists(),
            "stdout TTY colors WOULD-LINK and EXIST while redirected warnings stay plain",
        )
        stdout, stderr = run_pty(bash, fixture, plain_env, "--dry-run", tty="stderr")
        check(
            ANSI not in stdout
            and stderr.count("\x1b[1;33mWARN\x1b[0m skipped: different target: ") == 2
            and "\x1b[1;33mWARN\x1b[0m source root missing, skipped: " in stderr
            and not task_log.exists(),
            "stderr TTY colors conflict warnings while redirected statuses stay plain",
        )

        write_roots(fixture, "skills")
        hostile, marker = hostile_environment(root, parent)
        link_env = environment(hostile, wrappers, task_log)
        stdout, stderr = run_pty(bash, fixture, link_env)
        expected_calls = []
        for destination in destinations:
            expected_calls.extend((
                str(wrappers / "mkdir"), "-p", "--", destination.rsplit("/", 1)[0],
                str(wrappers / "ln"), "-s", "--", str(source), destination,
            ))
        calls = task_log.read_bytes().split(b"\0")
        check(
            stdout.count("\x1b[1;32mLINK") == 2
            and "\x1b[1;34m[codex]" in stdout
            and "\x1b[1;35m[claude]" in stdout
            and not stderr
            and calls == [os.fsencode(arg) for arg in expected_calls] + [b""]
            and not marker.exists(),
            "TTY LINK colors and exact intercepted arguments survive hostile shell startup inputs",
        )
        require_absent(destinations)

        for label, setting in (
            ("NO_COLOR", {"NO_COLOR": "1"}),
            ("TERM=dumb", {"TERM": "dumb"}),
        ):
            stdout, stderr = run_pty(bash, fixture, {**plain_env, **setting}, "--dry-run")
            check(ANSI not in stdout + stderr, f"{label} disables ANSI on a TTY")

        stdout, stderr = run_pty(bash, fixture, {**plain_env, "NO_COLOR": ""}, "--dry-run")
        check(
            "\x1b[1;36mWOULD-LINK" in stdout and not stderr,
            "empty NO_COLOR follows documented non-empty disable semantics",
        )

        help_result = run_redirected(bash, fixture, plain_env, "--help")
        run_redirected(bash, fixture, plain_env, "--invalid", expected=2)
        check("NO_COLOR" in help_result.stdout, "help documents NO_COLOR and invalid usage exits 2")


if __name__ == "__main__":
    main()
