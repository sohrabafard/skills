#!/usr/bin/env python3
"""Report two defect classes nothing else in this toolchain catches.

1. A file mode that grants write to `other`. ansible-lint's yaml[octal-values]
   fires on the unquoted form only, so `mode: '0777'` on a directory and
   `mode: '0666'` on a secret both pass a production-profile lint run. Measured
   2026-07-29 against ansible-lint 26.6.0.

2. A Jinja expression interpolated into the free-form or `cmd` value of
   `command`, `shell` or `raw` without the `quote` filter. That is the command
   injection class, and neither ansible-lint's production profile nor Checkov's
   ansible framework reports it. Measured 2026-07-29.

Runs on Windows: pure Python, pathlib, no shell, no Path(__file__).parents[N],
and no temporary directory anywhere.

Exit codes: 0 clean, 1 findings, 2 could not run, 64 usage error.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

EXIT_OK = 0
EXIT_FINDINGS = 1
EXIT_CANNOT_RUN = 2
EXIT_USAGE = 64

try:
    import yaml
except ImportError:  # pragma: no cover
    print(
        "BLOCKED: PyYAML is not installed. Install it with "
        "'python3 -m pip install -r scripts/requirements.txt'. "
        "This is exit 2: the check could not run. It is not a pass.",
        file=sys.stderr,
    )
    sys.exit(EXIT_CANNOT_RUN)

from ansible_walk import iter_scalars, iter_tasks, line_of  # noqa: E402

MODE_KEY = "mode"
COMMAND_ACTIONS = {
    "command",
    "shell",
    "raw",
    "ansible.builtin.command",
    "ansible.builtin.shell",
    "ansible.builtin.raw",
    "ansible.legacy.command",
    "ansible.legacy.shell",
}
JINJA = re.compile(r"\{\{(.+?)\}\}", re.DOTALL)
# A Jinja expression is safe inside a command when its last filter is `quote`.
QUOTED = re.compile(r"\|\s*quote\s*$")
OCTAL = re.compile(r"^0?[0-7]{3,4}$")


class Finding:
    __slots__ = ("path", "line", "rule", "message", "remediation")

    def __init__(self, path, line, rule, message, remediation):
        self.path = path
        self.line = line
        self.rule = rule
        self.message = message
        self.remediation = remediation

    def as_dict(self):
        return {
            "file": self.path,
            "line": self.line,
            "rule": self.rule,
            "message": self.message,
            "remediation": self.remediation,
        }


def check_mode(value: str, node, path: str, findings: list) -> None:
    text = str(value).strip().strip("'\"")
    if not OCTAL.match(text):
        # A symbolic mode such as u=rw,g=r, or a Jinja expression. A symbolic
        # mode that grants o+w is reported by the substring test below.
        if "o+w" in text or "o=rw" in text or "a+w" in text or "a=rw" in text:
            findings.append(
                Finding(
                    path,
                    line_of(node),
                    "mode[world-writable]",
                    f"symbolic mode {text!r} grants write to other",
                    "State an explicit numeric mode whose last digit is 0, 4 or 5.",
                )
            )
        return
    digits = text[-3:]
    other = int(digits[-1])
    if other & 0o2:
        findings.append(
            Finding(
                path,
                line_of(node),
                "mode[world-writable]",
                f"mode {text!r} grants write to other",
                "Secrets are '0600' and their directories '0700'; configuration "
                "is '0644' and its directories '0755'. No shipped artifact may "
                "grant write to other. references/security_checklist.md states "
                "the full table.",
            )
        )


def check_command(action: str, value, node, path: str, findings: list) -> None:
    """Report an unquoted Jinja expression in a command's free-form or cmd value."""
    texts = []
    if isinstance(value, str):
        texts.append((value, node))
    elif isinstance(node, yaml.MappingNode):
        for key_node, val_node in node.value:
            if key_node.value in ("cmd", "_raw_params") and isinstance(val_node, yaml.ScalarNode):
                texts.append((val_node.value, val_node))
    for text, where in texts:
        for match in JINJA.finditer(text):
            expr = match.group(1).strip()
            if QUOTED.search(expr):
                continue
            findings.append(
                Finding(
                    path,
                    line_of(where),
                    "command[unquoted-jinja]",
                    f"{action} interpolates {{{{ {expr} }}}} without the quote filter",
                    "Either use a module that takes the value as a parameter "
                    "instead of a command string, or append '| quote' to the "
                    "expression. A value that reaches this line from inventory, "
                    "an extra var or a registered result is attacker-controlled "
                    "until proved otherwise.",
                )
            )


def walk(node, path: str, findings: list) -> None:
    """Two independent passes over the same document.

    `mode` is a parameter, not an action, and a world-writable mode is equally
    wrong in a task, a defaults file and a variables file, so every `mode`
    scalar anywhere in the document is checked.

    A command action is only a command action when it is the action key of a
    task. `shell:` is also a parameter of ansible.builtin.user, and reporting
    that as a command would be the same structure-blind mistake the pre-repair
    FQCN checker made.
    """
    for scalar in iter_scalars(node, MODE_KEY):
        check_mode(scalar.value, scalar, path, findings)

    for _task, key_node, value_node in iter_tasks(node):
        action = key_node.value
        if action in COMMAND_ACTIONS:
            value = value_node.value if isinstance(value_node, yaml.ScalarNode) else None
            check_command(action, value, value_node, path, findings)


def scan_file(path: Path, findings: list, errors: list) -> None:
    try:
        with path.open("r", encoding="utf-8") as handle:
            node = yaml.compose(handle)
    except (yaml.YAMLError, UnicodeDecodeError, OSError) as exc:
        errors.append(f"{path}: {exc}")
        return
    if node is not None:
        walk(node, str(path), findings)


def collect(target: Path) -> list:
    if target.is_file():
        return [target]
    skip = {".git", "venv", ".venv", "node_modules", "__pycache__", ".molecule", ".tox"}
    out = []
    for pattern in ("*.yml", "*.yaml"):
        for candidate in sorted(target.rglob(pattern)):
            if skip.intersection(candidate.parts):
                continue
            out.append(candidate)
    return out


def self_test() -> int:
    here = Path(__file__).resolve().parent
    fixtures = here.parent / "test" / "fixtures" / "tasks"
    passed = failed = 0
    print("self-test: check_task_safety.py")

    cases = [
        ("safe-tasks.yml", set(), "safe tasks report nothing"),
        (
            "unsafe-tasks.yml",
            {"mode[world-writable]", "command[unquoted-jinja]"},
            "world-writable mode and unquoted Jinja in shell are both reported",
        ),
    ]
    for name, expected_rules, label in cases:
        path = fixtures / name
        if not path.exists():
            print(f"  FAIL {label}: fixture missing at {path}")
            failed += 1
            continue
        findings, errors = [], []
        scan_file(path, findings, errors)
        rules = {f.rule for f in findings}
        if errors:
            print(f"  FAIL {label}: fixture did not parse: {errors[0]}")
            failed += 1
        elif rules == expected_rules:
            print(f"  ok   {label} ({len(findings)} finding(s))")
            passed += 1
        else:
            print(f"  FAIL {label}: expected rules {sorted(expected_rules)}, got {sorted(rules)}")
            failed += 1

    print()
    if failed:
        print(f"self-test: {passed} passed, {failed} FAILED")
        return EXIT_FINDINGS
    print(f"self-test: {passed} assertion(s) passed")
    return EXIT_OK


def main(argv: list) -> int:
    parser = argparse.ArgumentParser(
        prog="check_task_safety.py",
        description=(
            "Report file modes that grant write to other, and Jinja "
            "expressions interpolated into command, shell or raw without the "
            "quote filter."
        ),
        epilog="Exit codes: 0 clean, 1 findings, 2 could not run, 64 usage error.",
    )
    parser.add_argument("target", nargs="?", help="playbook, role directory or project directory")
    parser.add_argument("--self-test", action="store_true", help="run against the shipped fixtures")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    try:
        args = parser.parse_args(argv)
    except SystemExit:
        return EXIT_USAGE

    if args.self_test:
        return self_test()

    if not args.target:
        print("Usage error: a target path is required. Run with --help.", file=sys.stderr)
        return EXIT_USAGE

    target = Path(args.target)
    if not target.exists():
        print(
            f"BLOCKED: target not found: {target}. "
            "This is exit 2: the check could not run. It is not a pass.",
            file=sys.stderr,
        )
        return EXIT_CANNOT_RUN

    files = collect(target)
    if not files:
        print(
            f"BLOCKED: no .yml or .yaml files under {target}. "
            "This is exit 2: the check could not run. It is not a pass.",
            file=sys.stderr,
        )
        return EXIT_CANNOT_RUN

    findings, errors = [], []
    for path in files:
        scan_file(path, findings, errors)

    if errors:
        for err in errors:
            print(f"BLOCKED: could not parse {err}", file=sys.stderr)
        print(
            "This is exit 2: the check could not run over every file. It is not a pass.",
            file=sys.stderr,
        )
        return EXIT_CANNOT_RUN

    if args.format == "json":
        print(json.dumps({"findings": [f.as_dict() for f in findings]}, indent=2))
    else:
        if not findings:
            print("PASS - no world-writable mode and no unquoted Jinja in a command")
        else:
            for f in findings:
                print(f"{f.path}:{f.line}: {f.rule}: {f.message}")
                print(f"    {f.remediation}")
                print()

    return EXIT_FINDINGS if findings else EXIT_OK


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
