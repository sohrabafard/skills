#!/usr/bin/env python3
"""Static Claude goal preflight. Exit 0 clean, 1 findings, 2 unavailable proof.

Input is the final rendered condition only, excluding /goal and any Markdown fence.
Official goal/desktop documentation verified 2026-10-04 records a 4000-character cap:
https://code.claude.com/docs/en/goal and https://code.claude.com/docs/en/desktop.
Unicode semantics are unspecified; UTF-16 units conservatively avoid undercounting.
Desktop token checks reflect a user-observed composer diagnostic dated 2026-10-04,
not a universal CLI grammar. Text checks cannot inspect rich mention/link chips,
confirm runtime availability, judge completion semantics, or prove live acceptance.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

CAP = 4000
SURFACES = ("claude-code-cli", "claude-desktop-code", "claude-desktop-chat", "claude-cowork", "unknown")
DOCUMENTED_SURFACES = frozenset(SURFACES[:2])
FIXTURES = Path(__file__).resolve().parent / "fixtures/goal-conditions.json"

# Conservative text proxies for the observed Desktop rich-composer rejection.
# A standalone /name resembles a command; paths with a directory separator or
# extension remain plain text. @file chips cannot be distinguished in this input.
DESKTOP_TOKENS = (
    ("COMMAND", re.compile(r"(?<!\S)/[A-Za-z][\w-]*(?::[A-Za-z][\w-]*)?(?=\s|$|[.,;:!?](?:\s|$))")),
    ("MENTION", re.compile(r"(?<![\w])@[\w]")),
    ("LINK", re.compile(r"https?://\S+|!?\[[^\]\n]+\]\([^\n]*\)|<[^>\n]*(?:https?://|mailto:)[^>\n]*>", re.I)),
    ("FORMAT", re.compile(r"`|\*\*\S[^\n]*?\*\*|__\S[^\n]*?__|(?<!\w)\*\S[^\n]*?\*(?!\w)|(?<![\w/])_\S[^\n]*?_(?!\w)|~~\S[^\n]*?~~")),
)


def character_units(condition: str) -> int:
    """Conservative count, not a claim about the target runtime's parser."""
    return len(condition.encode("utf-16-le")) // 2


def findings(condition: str, surface: str) -> list[str]:
    errors = []
    if surface not in DOCUMENTED_SURFACES:
        errors.append("SURFACE: goal support is not established for this declared surface")
    if not condition.strip():
        errors.append("EMPTY: a rendered completion condition is required")
    if character_units(condition) > CAP:
        errors.append(f"LENGTH: {character_units(condition)} UTF-16 units exceed the documented {CAP}-character snapshot")
    if surface == "claude-desktop-code":
        for code, pattern in DESKTOP_TOKENS:
            if pattern.search(condition):
                errors.append(f"DESKTOP-{code}: use plain condition text; put rich content in plan context; a command-led kickoff uses plain skill names/paths and only its leading command")
    return errors


def check_file(path: Path, surface: str) -> tuple[list[str], int]:
    # Preserve actual newline characters: do not silently reduce the sent text.
    with path.open(encoding="utf-8", newline="") as stream:
        condition = stream.read()
    return findings(condition, surface), character_units(condition)


def self_test() -> None:
    cases = json.loads(FIXTURES.read_text(encoding="utf-8"))
    for case in cases:
        actual = {error.split(":", 1)[0] for error in findings(case["condition"], case["surface"])}
        if actual != set(case["expected"]):
            raise ValueError(f"fixture {case['name']}: expected {case['expected']}, got {sorted(actual)}")
    for surface in DOCUMENTED_SURFACES:
        if findings("a" * CAP, surface) or not findings("a" * (CAP + 1), surface):
            raise ValueError("limit boundary fixture failed")
    if character_units("\u0641\u0627\u0631\u0633\u06cc") != 5 or character_units("\U00010400") != 2:
        raise ValueError("Unicode conservative-count fixture failed")
    if findings("\U00010400" * (CAP // 2), "claude-desktop-code") or not findings("\U00010400" * (CAP // 2 + 1), "claude-desktop-code"):
        raise ValueError("astral limit boundary fixture failed")
    from contextlib import redirect_stderr, redirect_stdout
    from io import StringIO
    from unittest.mock import patch
    arguments = ["--surface", "claude-desktop-code", "--condition-file", "synthetic.txt"]
    for text, expected in (("plain condition", 0), ("Use /alaa-workflow.", 1), ("x" * (CAP + 1), 1)):
        with patch.object(Path, "open", return_value=StringIO(text)), redirect_stdout(StringIO()):
            if main(arguments) != expected:
                raise ValueError(f"CLI exit contract failed: expected {expected}")
    with patch.object(Path, "open", side_effect=FileNotFoundError("synthetic missing condition")), redirect_stderr(StringIO()):
        if main(arguments) != 2:
            raise ValueError("unavailable input must return exit 2")
    print(f"OK: {len(cases)} text fixtures plus length, Unicode and unavailable-input boundaries; static proof only")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--surface", choices=SURFACES)
    parser.add_argument("--condition-file", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.self_test:
            if args.surface or args.condition_file:
                parser.error("--self-test cannot be combined with condition inputs")
            self_test()
            return 0
        if not args.surface or args.condition_file is None:
            parser.error("--surface and --condition-file are required")
        errors, count = check_file(args.condition_file, args.surface)
        if errors:
            print("\n".join(errors))
            return 1
        print(f"OK: {count} UTF-16 units; declared surface/text match the dated preflight; live acceptance unverified")
        return 0
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f"could not run: {exc}", file=sys.stderr)
        return 2
    except (ValueError, KeyError, TypeError) as exc:
        print(f"FINDINGS: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
