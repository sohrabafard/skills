#!/usr/bin/env python3
"""Enforce the HAProxy `defaults` association rule on one or more config files.

A `defaults` section applies only to the proxies that follow it, up to the next
`defaults` section, or to the proxies that name it with `from`. It is never
file-wide. Two configs that are each correct alone therefore change one another's
behaviour when concatenated, and the result parses and starts.

This checker reports a violation of the rule stated in
`references/20-core-config-and-timeouts.md`.

Pure Python 3 standard library.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

EXIT_CLEAN = 0
EXIT_FINDINGS = 1
EXIT_CANNOT_RUN = 2

# Section keywords that may appear unindented at the start of a line.
SECTION_KEYWORDS = {
    "global", "defaults", "frontend", "backend", "listen", "peers", "resolvers",
    "cache", "ring", "log-forward", "mailers", "userlist", "http-errors",
    "crt-store", "traces", "fcgi-app", "acme", "healthcheck", "program",
}

# Sections that inherit from a `defaults` section.
PROXY_SECTIONS = {"frontend", "backend", "listen"}

RULES = {
    "HP-DEF-001": "a file that declares any `defaults` section must name every one of them",
    "HP-DEF-002": "every frontend, backend and listen in such a file must select its defaults with `from <name>`",
    "HP-DEF-003": "every `from <name>` must resolve to a `defaults` section declared in the same file",
    "HP-DEF-004": "no two `defaults` sections may share a name (a startup error from HAProxy 3.3)",
}


class Finding:
    def __init__(self, path: str, line: int, rule: str, detail: str) -> None:
        self.path = path
        self.line = line
        self.rule = rule
        self.detail = detail

    def __str__(self) -> str:
        return "{}:{}: {}: {}".format(self.path, self.line, self.rule, self.detail)


def skill_root(start: Path) -> Path | None:
    """Ascend from `start` until a directory containing SKILL.md is found.

    Deliberately not `Path(__file__).parents[N]`: the depth of this script inside
    the skill is not a fact this script should encode.
    """
    current = start.resolve()
    for _ in range(8):
        if (current / "SKILL.md").is_file():
            return current
        if current.parent == current:
            break
        current = current.parent
    return None


def strip_comment(line: str) -> str:
    """Remove a HAProxy comment. `#` starts one at line start or after whitespace."""
    out = []
    prev = ""
    for index, char in enumerate(line):
        if char == "#" and prev != "\\" and (index == 0 or prev.isspace()):
            break
        out.append(char)
        prev = char
    return "".join(out)


def read_lines(path: Path) -> list[str]:
    """Read as text with universal newlines, then defend against a stray CR.

    A CRLF file otherwise leaves a carriage return on the last field of every parsed
    line and every comparison fails while the rendered bytes look identical.
    """
    with path.open("r", encoding="utf-8", errors="replace", newline=None) as handle:
        return [line.rstrip("\r\n") for line in handle]


def analyse(path: Path, display: str) -> list[Finding]:
    findings: list[Finding] = []
    lines = read_lines(path)

    defaults_names: dict[str, int] = {}
    unnamed_defaults: list[int] = []
    proxies: list[tuple[int, str, str, str | None]] = []  # line, kind, name, from

    for number, raw in enumerate(lines, start=1):
        if raw[:1].isspace() or not raw.strip():
            continue
        if raw.lstrip().startswith("."):
            continue  # preprocessor directive
        text = strip_comment(raw).strip()
        if not text:
            continue
        tokens = text.split()
        kind = tokens[0]
        if kind not in SECTION_KEYWORDS:
            continue

        from_name = None
        if "from" in tokens[1:]:
            position = tokens.index("from", 1)
            if position + 1 < len(tokens):
                from_name = tokens[position + 1]

        if kind == "defaults":
            # `defaults`, `defaults <name>`, `defaults <name> from <base>`
            name = None
            if len(tokens) > 1 and tokens[1] != "from":
                name = tokens[1]
            if name is None:
                unnamed_defaults.append(number)
            elif name in defaults_names:
                findings.append(Finding(
                    display, number, "HP-DEF-004",
                    "duplicate `defaults {}` (first at line {})".format(name, defaults_names[name])))
            else:
                defaults_names[name] = number
        elif kind in PROXY_SECTIONS:
            name = tokens[1] if len(tokens) > 1 else "(unnamed)"
            proxies.append((number, kind, name, from_name))

    declares_defaults = bool(defaults_names) or bool(unnamed_defaults)
    if not declares_defaults:
        # Nothing to associate. A file with no `defaults` neither inherits nor governs.
        return findings

    for number in unnamed_defaults:
        findings.append(Finding(
            display, number, "HP-DEF-001",
            "unnamed `defaults` section. It governs every proxy that follows it until the "
            "next `defaults`, which cannot be reviewed and changes meaning when this file is "
            "concatenated with another. Give it a name."))

    for number, kind, name, from_name in proxies:
        if from_name is None:
            findings.append(Finding(
                display, number, "HP-DEF-002",
                "`{} {}` inherits the nearest preceding `defaults` positionally. Add "
                "`from <defaults-name>`.".format(kind, name)))
        elif from_name not in defaults_names:
            findings.append(Finding(
                display, number, "HP-DEF-003",
                "`{} {} from {}` names a `defaults` section that this file does not "
                "declare.".format(kind, name, from_name)))

    return findings


def collect_targets(raw_targets: list[str]) -> tuple[list[tuple[Path, str]], str | None]:
    targets: list[tuple[Path, str]] = []
    for entry in raw_targets:
        path = Path(entry)
        if not path.exists():
            return [], "path does not exist: {}".format(entry)
        if path.is_dir():
            found = sorted(path.rglob("*.cfg"))
            if not found:
                return [], "no *.cfg files under directory: {}".format(entry)
            for item in found:
                targets.append((item, str(item)))
        elif path.is_file():
            targets.append((path, str(path)))
        else:
            return [], "not a file or directory: {}".format(entry)
    if not targets:
        return [], "no input files resolved"
    return targets, None


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="check_defaults_scope.py",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=__doc__,
        epilog=(
            "Rules\n"
            + "".join("  {}  {}\n".format(rule, text) for rule, text in sorted(RULES.items()))
            + "\n"
            "A file that declares no `defaults` section at all is exempt: there is nothing to\n"
            "associate.\n"
            "\n"
            "Exit codes\n"
            "  0  clean\n"
            "  1  findings reported\n"
            "  2  could not run: a path that does not exist, a directory with no *.cfg,\n"
            "     or an unreadable file\n"
        ),
    )
    parser.add_argument(
        "targets", nargs="*",
        help="config files or directories to check. Defaults to examples/haproxy in this skill.")
    return parser


def main(argv: list[str]) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    script_dir = Path(__file__).resolve().parent

    raw_targets = args.targets
    if not raw_targets:
        root = skill_root(script_dir)
        if root is None:
            print("could not locate SKILL.md above {}; pass an explicit path".format(script_dir),
                  file=sys.stderr)
            return EXIT_CANNOT_RUN
        raw_targets = [str(root / "examples" / "haproxy")]

    targets, error = collect_targets(raw_targets)
    if error is not None:
        print("could not run: {}".format(error), file=sys.stderr)
        return EXIT_CANNOT_RUN

    findings: list[Finding] = []
    for path, display in targets:
        try:
            findings.extend(analyse(path, display))
        except OSError as exc:
            print("could not run: cannot read {}: {}".format(display, exc), file=sys.stderr)
            return EXIT_CANNOT_RUN

    for finding in findings:
        print(str(finding))

    print("checked {} file(s); {} finding(s)".format(len(targets), len(findings)))
    return EXIT_FINDINGS if findings else EXIT_CLEAN


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
