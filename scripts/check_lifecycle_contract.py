#!/usr/bin/env python3
"""Completion-lifecycle ownership checker for the skills/sohrab/ pack.

WHAT THIS ASSERTS
    The four completion-lifecycle states are defined in exactly one file, and both orchestrators
    report all four without carrying a second copy of the definitions.

    L1  the owner file carries a definition row for every state
    L2  each reporter's "Final report" section names every state
    L3  each reporter's "Final report" section cites the owner by its cross-skill path
    L4  no state name appears in a pack SKILL.md or references file outside its permitted sites
    L5  no definition row for a state exists outside the owner file

    The owner is alaa-workflow references/workspace-and-integration.md. The permitted naming sites
    for L4 are that file, the owner skill's SKILL.md, and each reporter's "Final report" section --
    everything else in the pack must reach the states through the owner rather than restate them.

    L2 and L5 are the pair that keeps the reporters honest in both directions. L2 fails when a
    report drops a state, which is how a run silently stops distinguishing a change that was merely
    written from one that was committed and reviewed. L5 fails when a reporter grows a definition
    row of its own, which is how the two orchestrators drift apart from each other and from the
    owner. Neither rule is implied by the other: a report that lists all four states and defines
    them locally passes L2 and fails L5.

    A definition row is a Markdown table row whose first cell is the backticked state name and
    nothing else. That is a structural test, not a phrase match, so rewording a condition never
    fires this checker and deleting the row that states it always does.

EXIT CODES
    0  clean          zero findings
    1  findings       one or more findings
    2  could not run  root not found, skills/sohrab absent, the owner file missing, a reporter
                      skill or its SKILL.md missing, a reporter with no "Final report" heading,
                      or a file that is not decodable UTF-8

WINDOWS
    Python 3 standard library only. pathlib throughout, files read as bytes and decoded explicitly,
    newlines normalised before any comparison, no temp directory, no reliance on a shebang. The
    tree is enumerated at runtime and no skill name outside the contract itself is hardcoded.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

EXIT_CLEAN = 0
EXIT_FINDINGS = 1
EXIT_CANNOT_RUN = 2

PACK_RELATIVE = ("skills", "sohrab")

STATES: Tuple[str, ...] = ("IMPLEMENTED", "MERGE_CANDIDATE", "RELEASE_CANDIDATE", "PUBLISHED")

OWNER_SKILL = "alaa-workflow"
OWNER_REFERENCE = "references/workspace-and-integration.md"
OWNER_CITATION = f"{OWNER_SKILL} {OWNER_REFERENCE}"

REPORTER_SKILLS: Tuple[str, ...] = ("alaa-cc-orchestrator", "alaa-codex-orchestrator")
REPORT_SECTION = "Final report"

# A heading at any level whose text is exactly the report section name.
REPORT_HEADING_RE = re.compile(r"^(#{1,6})\s+" + re.escape(REPORT_SECTION) + r"\s*$", re.I)
ANY_HEADING_RE = re.compile(r"^(#{1,6})\s+")

STATE_TOKEN_RE = re.compile(r"\b(" + "|".join(STATES) + r")\b")
# The first cell of a Markdown table row, holding the backticked state name and nothing else.
DEFINITION_ROW_RE = re.compile(r"^\s*\|\s*`(" + "|".join(STATES) + r")`\s*\|")

RULES: Dict[str, str] = {
    "L1-OWNER-STATE-UNDEFINED": "the owner file has no definition row for a state",
    "L2-REPORT-STATE-MISSING": "a reporter's final-report section does not name a state",
    "L3-REPORT-OWNER-NOT-CITED": "a reporter's final-report section does not cite the owner file",
    "L4-STATE-OUTSIDE-OWNER": "a state name appears outside its permitted sites",
    "L5-DEFINITION-OUTSIDE-OWNER": "a state definition row exists outside the owner file",
}


class CannotRun(Exception):
    """Raised for every condition that means the checker could not evaluate its rules."""


class Finding:
    __slots__ = ("rule", "subject", "location", "detail")

    def __init__(self, rule: str, subject: str, location: str, detail: str) -> None:
        self.rule = rule
        self.subject = subject
        self.location = location
        self.detail = detail

    def as_text(self) -> str:
        return f"- {self.rule}  {self.subject}\n    {self.location}\n    {self.detail}"

    def as_json(self) -> str:
        return json.dumps(
            {
                "rule": self.rule,
                "severity": "finding",
                "subject": self.subject,
                "location": self.location,
                "detail": self.detail,
            },
            sort_keys=True,
        )


# --------------------------------------------------------------------------------------
# Reading
# --------------------------------------------------------------------------------------


def read_lines(path: Path) -> List[str]:
    """Read a file as UTF-8 with newlines normalised, or raise CannotRun.

    Decoding is explicit because a file that is not UTF-8 must stop the run rather than be read
    through a replacement character that changes what the regexes match.
    """
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise CannotRun(f"cannot read {path}: {exc}") from exc
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise CannotRun(f"not decodable UTF-8: {path}: {exc}") from exc
    return text.replace("\r\n", "\n").replace("\r", "\n").split("\n")


def find_root(explicit: Optional[str]) -> Path:
    if explicit:
        root = Path(explicit).expanduser()
        if not (root / Path(*PACK_RELATIVE)).is_dir():
            raise CannotRun(f"no {'/'.join(PACK_RELATIVE)} under {root}")
        return root
    here = Path.cwd().resolve()
    for candidate in (here, *here.parents):
        if (candidate / Path(*PACK_RELATIVE)).is_dir():
            return candidate
    raise CannotRun(f"no ancestor of {here} contains {'/'.join(PACK_RELATIVE)}")


def report_section(lines: Sequence[str], subject: str) -> Tuple[int, int]:
    """Return the half-open line range of the report section, heading excluded, or raise CannotRun.

    A range rather than the lines themselves, because the permitted naming sites are positions in a
    file: matching on line content would silently permit an identical line written outside the
    section. The section ends at the next heading of the same or a shallower level, so a subsection
    inside the report stays part of it.
    """
    start = depth = None
    for i, line in enumerate(lines):
        match = REPORT_HEADING_RE.match(line)
        if match:
            start, depth = i + 1, len(match.group(1))
            break
    if start is None or depth is None:
        raise CannotRun(f"{subject}: no '{REPORT_SECTION}' heading")
    for j in range(start, len(lines)):
        nxt = ANY_HEADING_RE.match(lines[j])
        if nxt and len(nxt.group(1)) <= depth:
            return start, j
    return start, len(lines)


def instructional_files(pack: Path) -> List[Path]:
    """Every file in the pack that instructs an agent: each SKILL.md and each references file.

    A CHANGELOG records what happened, an index lists what exists, and the pack's own AGENTS.md
    names who owns what. None of the three is loaded as a skill body, so none is a site where a
    duplicated definition would be followed instead of the owner's.
    """
    found: List[Path] = []
    for skill in sorted(p for p in pack.iterdir() if p.is_dir() and not p.name.startswith(".")):
        body = skill / "SKILL.md"
        if body.is_file():
            found.append(body)
        references = skill / "references"
        if references.is_dir():
            found.extend(sorted(p for p in references.rglob("*.md") if p.is_file()))
    return found


# --------------------------------------------------------------------------------------
# Rules
# --------------------------------------------------------------------------------------


def run_checks(root: Path) -> Tuple[List[Finding], Dict[str, str]]:
    pack = root / Path(*PACK_RELATIVE)
    if not pack.is_dir():
        raise CannotRun(f"no {'/'.join(PACK_RELATIVE)} under {root}")

    owner = pack / OWNER_SKILL / Path(*OWNER_REFERENCE.split("/"))
    if not owner.is_file():
        raise CannotRun(f"owner file missing: {owner}")
    owner_body = pack / OWNER_SKILL / "SKILL.md"
    if not owner_body.is_file():
        raise CannotRun(f"owner skill body missing: {owner_body}")

    findings: List[Finding] = []
    owner_lines = read_lines(owner)

    # L1 -- the owner defines every state.
    defined = {m.group(1) for m in (DEFINITION_ROW_RE.match(ln) for ln in owner_lines) if m}
    for state in STATES:
        if state not in defined:
            findings.append(
                Finding(
                    "L1-OWNER-STATE-UNDEFINED",
                    state,
                    f"{OWNER_CITATION}",
                    "add a table row whose first cell is the backticked state name",
                )
            )

    # L2 and L3 -- each reporter names every state and cites the owner, inside its report section.
    permitted_report_range: Dict[Path, Tuple[int, int]] = {}
    for name in REPORTER_SKILLS:
        body = pack / name / "SKILL.md"
        if not body.is_file():
            raise CannotRun(f"reporter body missing: {body}")
        lines = read_lines(body)
        start, end = report_section(lines, f"{name}/SKILL.md")
        permitted_report_range[body] = (start, end)
        text = "\n".join(lines[start:end])
        for state in STATES:
            if not re.search(r"\b" + re.escape(state) + r"\b", text):
                findings.append(
                    Finding(
                        "L2-REPORT-STATE-MISSING",
                        state,
                        f"{name}/SKILL.md '{REPORT_SECTION}'",
                        "the report must state every lifecycle state with its own verdict",
                    )
                )
        if OWNER_CITATION not in text:
            findings.append(
                Finding(
                    "L3-REPORT-OWNER-NOT-CITED",
                    name,
                    f"{name}/SKILL.md '{REPORT_SECTION}'",
                    f"cite `{OWNER_CITATION}` as the owner of what earns each state",
                )
            )

    # L4 and L5 -- nothing outside the permitted sites names or defines a state.
    for path in instructional_files(pack):
        relative = path.relative_to(pack).as_posix()
        lines = read_lines(path)
        allowed_start, allowed_end = permitted_report_range.get(path, (0, 0))
        naming_is_free = path == owner or path == owner_body
        for index, line in enumerate(lines):
            number = index + 1
            definition = DEFINITION_ROW_RE.match(line)
            if definition and path != owner:
                findings.append(
                    Finding(
                        "L5-DEFINITION-OUTSIDE-OWNER",
                        definition.group(1),
                        f"{relative}:{number}",
                        f"only `{OWNER_CITATION}` defines a state; cite it instead",
                    )
                )
                continue
            if naming_is_free or allowed_start <= index < allowed_end:
                continue
            named = STATE_TOKEN_RE.search(line)
            if named:
                findings.append(
                    Finding(
                        "L4-STATE-OUTSIDE-OWNER",
                        named.group(1),
                        f"{relative}:{number}",
                        f"reach the lifecycle through `{OWNER_CITATION}` rather than naming a state here",
                    )
                )

    notes = {
        "root": str(root),
        "owner": OWNER_CITATION,
        "states": ", ".join(STATES),
        "reporters": ", ".join(REPORTER_SKILLS),
    }
    return findings, notes


# --------------------------------------------------------------------------------------
# Reporting
# --------------------------------------------------------------------------------------


def report(findings: Sequence[Finding], notes: Dict[str, str], fmt: str) -> None:
    if fmt == "json":
        for f in findings:
            print(f.as_json())
        return
    print("check_lifecycle_contract.py")
    for key, value in notes.items():
        print(f"  {key}: {value}")
    if findings:
        print(f"\nFINDINGS ({len(findings)}):")
        for f in sorted(findings, key=lambda x: (x.rule, x.location, x.subject)):
            print(f.as_text())
    else:
        print("\nFINDINGS: none")


# --------------------------------------------------------------------------------------
# Self-test
# --------------------------------------------------------------------------------------

SELF_TEST_CASES: Tuple[Tuple[str, int, Optional[Dict[str, int]]], ...] = (
    ("green", EXIT_CLEAN, {}),
    ("red-l1-owner-state-undefined", EXIT_FINDINGS, {"L1-OWNER-STATE-UNDEFINED": 1}),
    ("red-l2-report-state-missing", EXIT_FINDINGS, {"L2-REPORT-STATE-MISSING": 1}),
    ("red-l3-report-owner-not-cited", EXIT_FINDINGS, {"L3-REPORT-OWNER-NOT-CITED": 1}),
    ("red-l4-state-outside-owner", EXIT_FINDINGS, {"L4-STATE-OUTSIDE-OWNER": 1}),
    ("red-l5-definition-outside-owner", EXIT_FINDINGS, {"L5-DEFINITION-OUTSIDE-OWNER": 1}),
    ("red-no-owner", EXIT_CANNOT_RUN, None),
    ("red-no-report-section", EXIT_CANNOT_RUN, None),
)


def run_case(root: Path) -> Tuple[int, str]:
    import contextlib
    import io

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        code = main(["--root", str(root)])
    return code, buf.getvalue()


def self_test(fixtures_dir: Path) -> int:
    base = fixtures_dir / "lifecycle"
    if not base.is_dir():
        print(f"BLOCKED: fixture directory not found: {base}")
        return EXIT_CANNOT_RUN
    passed = failed = blocked = 0
    for name, expect_code, expect_rules in SELF_TEST_CASES:
        root = base / name
        if not root.is_dir():
            print(f"BLOCKED  {name}: fixture root missing ({root})")
            blocked += 1
            continue
        code, out = run_case(root)
        if code != expect_code:
            if code == EXIT_CANNOT_RUN:
                print(f"BLOCKED  {name}: exit 2 (could not run), expected {expect_code}")
                print("         " + out.strip().replace("\n", "\n         "))
                blocked += 1
            else:
                print(f"FAIL     {name}: exit {code}, expected {expect_code}")
                print("         " + out.strip().replace("\n", "\n         "))
                failed += 1
            continue
        if expect_rules is not None:
            observed: Dict[str, int] = {}
            for line in out.split("\n"):
                stripped = line.strip()
                if stripped.startswith("- L"):
                    rule = stripped.split()[1]
                    observed[rule] = observed.get(rule, 0) + 1
            if observed != expect_rules:
                print(f"FAIL     {name}: rules {observed}, expected {expect_rules}")
                failed += 1
                continue
        print(f"PASS     {name}")
        passed += 1
    print(f"\nself-test: {passed} passed, {failed} failed, {blocked} blocked")
    if blocked:
        return EXIT_CANNOT_RUN
    return EXIT_FINDINGS if failed else EXIT_CLEAN


# --------------------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------------------

EPILOG = """\
rules
  L1-OWNER-STATE-UNDEFINED     the owner file has no definition row for a state
  L2-REPORT-STATE-MISSING      a reporter's final-report section does not name a state
  L3-REPORT-OWNER-NOT-CITED    a reporter's final-report section does not cite the owner file
  L4-STATE-OUTSIDE-OWNER       a state name appears in a pack SKILL.md or references file that is
                               neither the owner file, the owner skill's body, nor a reporter's
                               final-report section
  L5-DEFINITION-OUTSIDE-OWNER  a state definition row exists outside the owner file

what counts as a definition
  A Markdown table row whose first cell is the backticked state name and nothing else. Rewording
  the condition beside it never fires this checker; deleting the row always does.

what is not scanned
  CHANGELOG files, the pack's AGENTS.md and its indexes, agent definitions, assets, and scripts.
  They record, declare ownership, list, or execute; none is loaded as a skill body, so none can
  stand in for the owner at the moment a run is reported.

exit codes
  0 clean   1 findings   2 could not run
"""


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="check_lifecycle_contract.py",
        description=(
            "Assert that the four completion-lifecycle states are defined in one file and that "
            "both orchestrators report all four without restating the definitions."
        ),
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument(
        "--root",
        help="repository root containing skills/sohrab. Default: nearest ancestor of the "
        "current directory that contains it.",
    )
    p.add_argument("--format", choices=("text", "json"), default="text")
    p.add_argument(
        "--self-test",
        action="store_true",
        help="run against the bundled fixtures. 0 pass, 1 fail, 2 a fixture could not be run.",
    )
    p.add_argument(
        "--fixtures",
        metavar="PATH",
        help="fixture directory. Default: the fixtures directory beside this script.",
    )
    return p


def clean_arg(value: Optional[str]) -> Optional[str]:
    """Strip surrounding whitespace, including a carriage return, from a path argument.

    A driver that writes CRLF leaves a carriage return on the last field of every line it parses.
    Without this, the failure message shows a path that renders identically to the correct one.
    """
    return None if value is None else value.strip().strip("\r\n")


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    args.root = clean_arg(args.root)
    args.fixtures = clean_arg(args.fixtures)

    if args.self_test:
        fixtures = (
            Path(args.fixtures).expanduser()
            if args.fixtures
            # Sibling of this file. Path(__file__).parents[N] is forbidden here because it
            # encodes a guess about the repository layout above the script.
            else Path(__file__).resolve().with_name("fixtures")
        )
        try:
            return self_test(fixtures)
        except CannotRun as exc:
            print(f"BLOCKED: {exc}")
            return EXIT_CANNOT_RUN

    try:
        root = find_root(args.root)
        findings, notes = run_checks(root)
    except CannotRun as exc:
        print(f"could not run: {exc}", file=sys.stderr)
        return EXIT_CANNOT_RUN
    except OSError as exc:
        print(f"could not run: {exc}", file=sys.stderr)
        return EXIT_CANNOT_RUN

    report(findings, notes, args.format)
    return EXIT_FINDINGS if findings else EXIT_CLEAN


if __name__ == "__main__":
    raise SystemExit(main())
