#!/usr/bin/env python3
"""Index-identity checker for the skills/sohrab/ pack.

WHAT THIS ASSERTS
    Every index in this pack says the same thing as the disk, in both directions, and the two
    agent-instruction files that are supposed to be one file still are.

    X1  every skill directory appears in skills/sohrab/README.md's skill map
    X2  every name in that map is a skill directory
    X3  every skill directory appears in skills/sohrab/README.fa.md's group tables
    X4  every name in those tables is a skill directory
    X5  no name in README.md's "Consolidated or removed" list exists as a directory
    X6  root AGENTS.md and root CLAUDE.md agree after newline normalisation, or CLAUDE.md is
        an import bridge whose first line is @AGENTS.md
    X7  skills/sohrab/CLAUDE.md is not a file whose entire content is a path
    X8  every skill directory ships agents/openai.yaml
    X9  no name appears twice in either index

    X1 and X2 together are what makes README.md's own sentence "Every folder in this directory
    appears exactly once below" true, and X9 is the "exactly once" half.

    X6 compares normalised content on purpose. A byte comparison fires whenever the two files
    differ only in line endings, and the rule then gets switched off.

    X7 exists because skills/sohrab/CLAUDE.md is committed as git mode 120000 with a 9-byte blob
    whose content is the literal text "AGENTS.md". A checkout without symlink support
    materialises that as a 9-byte text file, and Claude Code loads it instead of the contract
    with no error and no warning. The observable condition is a CLAUDE.md whose entire content
    is a path that resolves beside it, and that is what this rule tests. An import bridge whose
    first line is @AGENTS.md passes.

EXIT CODES
    0  clean          zero findings after baseline suppression
    1  findings       one or more findings, or a baseline entry that matches nothing
    2  could not run  root not found, skills/sohrab absent or unreadable, zero skills
                      discovered, either README missing, README.md's skill map not locatable,
                      README.fa.md's tables not locatable, root AGENTS.md missing, a file that
                      is not decodable UTF-8, or a baseline that is unreadable or malformed

IMPLEMENTATION
    Python 3 standard library only. pathlib throughout, files read as bytes and decoded
    explicitly, newlines normalised before any comparison, no temp directory, no os.symlink.
    The tree is enumerated at runtime and no skill name is hardcoded.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Set, Tuple

EXIT_CLEAN = 0
EXIT_FINDINGS = 1
EXIT_CANNOT_RUN = 2

PACK_RELATIVE = ("skills", "sohrab")

MAP_START_MARKER = "<!-- skill-map:start -->"
MAP_END_MARKER = "<!-- skill-map:end -->"
MAP_HEADING_RE = re.compile(r"^##\s+Current skill map\s*$", re.I)
CONSOLIDATED_HEADING_RE = re.compile(r"^##\s+Consolidated or removed", re.I)
NEXT_H2_RE = re.compile(r"^##\s+")

BULLET_NAME_RE = re.compile(r"^\s*[-*]\s+`([a-z0-9][a-z0-9._-]*)`")
# The first cell of a group-table row. It may name more than one skill: README.fa.md:99 reads
# `| `ansible-generator` / `ansible-validator` | ... |`, so every backticked name in the cell
# counts, not only the first. Reading only the first name reported two real skills as missing.
TABLE_FIRST_CELL_RE = re.compile(r"^\s*\|([^|]*)\|")
SKILL_NAME_TOKEN_RE = re.compile(r"^[a-z0-9][a-z0-9._-]*$")
BACKTICK_TOKEN_RE = re.compile(r"`([^`\n]+)`")
# Separator between "these names were removed" and "this is what replaced them". The em and en
# dashes are written as escapes so re-saving this file in another encoding cannot silently
# change what the regex matches.
SEPARATOR_RE = re.compile("\\s(?:\u2014|\u2013|--|-)\\s")

IMPORT_BRIDGE_RE = re.compile(r"^@([A-Za-z0-9_.\-/]+)$")
BARE_PATH_RE = re.compile(r"^[A-Za-z0-9_.\-]+(?:/[A-Za-z0-9_.\-]+)*\.[A-Za-z0-9]+$")

RULES: Dict[str, str] = {
    "X1-DIR-NOT-IN-README": "a skill directory is absent from README.md's skill map",
    "X2-README-NAME-NOT-A-DIR": "a name in README.md's skill map has no directory",
    "X3-DIR-NOT-IN-README-FA": "a skill directory is absent from README.fa.md's group tables",
    "X4-README-FA-NAME-NOT-A-DIR": "a name in README.fa.md's group tables has no directory",
    "X5-CONSOLIDATED-STILL-EXISTS": "a name listed as consolidated or removed exists as a directory",
    "X6-AGENTS-CLAUDE-DIVERGED": "root AGENTS.md and root CLAUDE.md are neither equal nor bridged",
    "X7-CLAUDE-MD-IS-A-PATH-STUB": "skills/sohrab/CLAUDE.md's entire content is a path, not the contract",
    "X8-MISSING-OPENAI-YAML": "a skill directory has no agents/openai.yaml",
    "X9-DUPLICATE-IN-INDEX": "a name appears more than once in one index",
}


class CannotRun(Exception):
    """Raised for every condition that means the checker could not evaluate its rules."""


class Finding:
    __slots__ = ("rule", "subject", "location", "item", "detail")

    def __init__(self, rule: str, subject: str, location: str, item: str, detail: str) -> None:
        self.rule = rule
        self.subject = subject
        self.location = location
        self.item = item
        self.detail = detail

    @property
    def key(self) -> str:
        """Baseline key, deliberately without a line number so an unrelated edit above the
        subject does not churn the baseline."""
        return f"{self.rule}|{self.subject}|{self.location}|{self.item}"

    def as_text(self) -> str:
        return f"- {self.rule} {self.subject}\n    at: {self.location}\n    {self.detail}"

    def as_json(self) -> str:
        return json.dumps(
            {
                "rule": self.rule,
                "severity": "finding",
                "subject": self.subject,
                "location": self.location,
                "item": self.item,
                "detail": self.detail,
                "key": self.key,
            },
            sort_keys=True,
        )


# --------------------------------------------------------------------------------------
# Input
# --------------------------------------------------------------------------------------


def find_root(explicit: Optional[str]) -> Path:
    if explicit is not None:
        candidate = Path(explicit).expanduser()
        if not candidate.is_dir():
            raise CannotRun(f"--root is not a directory: {candidate}")
        if not candidate.joinpath(*PACK_RELATIVE).is_dir():
            raise CannotRun(f"--root {candidate} does not contain {'/'.join(PACK_RELATIVE)}")
        return candidate
    here = Path.cwd().resolve()
    for candidate in (here, *here.parents):
        if candidate.joinpath(*PACK_RELATIVE).is_dir():
            return candidate
    raise CannotRun(
        f"no ancestor of {here} contains {'/'.join(PACK_RELATIVE)}; pass --root explicitly"
    )


def read_text(path: Path, what: str) -> str:
    try:
        raw = path.read_bytes()
    except FileNotFoundError:
        raise CannotRun(f"{what} is missing: {path}")
    except OSError as exc:
        raise CannotRun(f"cannot read {what} at {path}: {exc}") from exc
    if b"\x00" in raw:
        raise CannotRun(f"{what} at {path} contains a NUL byte and is not decodable text")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise CannotRun(f"{what} at {path} is not decodable UTF-8: {exc}")
    if text.startswith("\ufeff"):
        text = text[1:]
    return text.replace("\r\n", "\n").replace("\r", "\n")


def discover_skills(pack_dir: Path) -> List[str]:
    try:
        entries = sorted(p for p in pack_dir.iterdir() if p.is_dir())
    except OSError as exc:
        raise CannotRun(f"cannot read {pack_dir}: {exc}") from exc
    names = [p.name for p in entries if (p / "SKILL.md").is_file()]
    if not names:
        raise CannotRun(
            f"zero skills found under {pack_dir}; a run from the wrong directory must not "
            f"look like a pass"
        )
    return names


# --------------------------------------------------------------------------------------
# Index extraction
# --------------------------------------------------------------------------------------


def slice_map_region(text: str) -> Tuple[List[str], str]:
    """Return the lines of README.md's skill map and how the region was located.

    Markers are preferred because they are unambiguous and survive a heading rename. The
    heading fallback exists because the markers are not in the file today and this checker is
    not allowed to edit README.md: a checker that exits 2 on the tree it ships with is a
    checker nobody runs.
    """
    lines = text.split("\n")
    start = end = None
    for i, line in enumerate(lines):
        if MAP_START_MARKER in line:
            start = i + 1
        elif MAP_END_MARKER in line and start is not None:
            end = i
            break
    if start is not None and end is not None and end > start:
        return lines[start:end], "markers"

    start = None
    for i, line in enumerate(lines):
        if MAP_HEADING_RE.match(line):
            start = i + 1
            break
    if start is None:
        raise CannotRun(
            "README.md: cannot locate the skill map. Expected "
            f"{MAP_START_MARKER} ... {MAP_END_MARKER} or a '## Current skill map' heading."
        )
    for j in range(start, len(lines)):
        if NEXT_H2_RE.match(lines[j]):
            return lines[start:j], "heading"
    return lines[start:], "heading"


def names_from_bullets(lines: Sequence[str]) -> List[str]:
    out: List[str] = []
    for line in lines:
        m = BULLET_NAME_RE.match(line)
        if m:
            out.append(m.group(1))
    return out


def names_from_tables(text: str) -> List[str]:
    out: List[str] = []
    for line in text.split("\n"):
        m = TABLE_FIRST_CELL_RE.match(line)
        if not m:
            continue
        for token in BACKTICK_TOKEN_RE.findall(m.group(1)):
            token = token.strip()
            if SKILL_NAME_TOKEN_RE.match(token):
                out.append(token)
    return out


def consolidated_names(text: str) -> List[str]:
    lines = text.split("\n")
    start = None
    for i, line in enumerate(lines):
        if CONSOLIDATED_HEADING_RE.match(line):
            start = i + 1
            break
    if start is None:
        return []
    end = len(lines)
    for j in range(start, len(lines)):
        if NEXT_H2_RE.match(lines[j]):
            end = j
            break
    out: List[str] = []
    for line in lines[start:end]:
        if not line.lstrip().startswith(("-", "*")):
            continue
        # Format of a bullet in this section, semicolon-separated clauses of
        #     `removed-name`, `removed-name` <separator> what replaced them
        # Only the names before the separator were removed. Taking every backticked token on
        # the line instead reports the replacing skill as removed, which fires on all four
        # bullets of the live README.md and is how this rule would have been switched off in
        # its first week. A clause with no separator is prose continuing the previous clause
        # and names nothing removed.
        for clause in line.lstrip("-* \t").split(";"):
            m = SEPARATOR_RE.search(clause)
            if not m:
                continue
            for token in BACKTICK_TOKEN_RE.findall(clause[: m.start()]):
                token = token.strip()
                # A wildcard family such as dockerfile-* names no single directory.
                if any(ch in token for ch in "*?[]<>/ "):
                    continue
                if re.fullmatch(r"[a-z0-9][a-z0-9._-]*", token):
                    out.append(token)
    return out


def duplicates(names: Sequence[str]) -> List[str]:
    seen: Set[str] = set()
    dupes: List[str] = []
    for n in names:
        if n in seen and n not in dupes:
            dupes.append(n)
        seen.add(n)
    return dupes


# --------------------------------------------------------------------------------------
# Rules
# --------------------------------------------------------------------------------------


def normalise_document(text: str) -> str:
    """Newlines already normalised by read_text. Trailing whitespace at the end of the document
    is stripped; per-line trailing whitespace is not, because two trailing spaces are a
    meaningful hard line break in Markdown and a checker must not silently accept a real
    difference."""
    return text.rstrip()


def check_agents_claude_pair(root: Path) -> List[Finding]:
    agents = root / "AGENTS.md"
    claude = root / "CLAUDE.md"
    agents_text = read_text(agents, "root AGENTS.md")

    if not claude.exists():
        return [
            Finding(
                "X6-AGENTS-CLAUDE-DIVERGED",
                "root CLAUDE.md",
                "CLAUDE.md",
                "missing",
                "root CLAUDE.md does not exist, so Claude Code loads no root instruction file. "
                "Create it as an import bridge whose first line is @AGENTS.md.",
            )
        ]
    claude_text = read_text(claude, "root CLAUDE.md")

    first = next((ln.strip() for ln in claude_text.split("\n") if ln.strip()), "")
    bridge = IMPORT_BRIDGE_RE.match(first)
    if bridge:
        target = root / bridge.group(1)
        if target.resolve() == agents.resolve() or target.name == agents.name:
            return []
        return [
            Finding(
                "X6-AGENTS-CLAUDE-DIVERGED",
                "root CLAUDE.md",
                "CLAUDE.md:1",
                f"@{bridge.group(1)}",
                f"the import bridge points at {bridge.group(1)}, not at AGENTS.md",
            )
        ]

    if normalise_document(agents_text) == normalise_document(claude_text):
        return []
    return [
        Finding(
            "X6-AGENTS-CLAUDE-DIVERGED",
            "root AGENTS.md and root CLAUDE.md",
            "AGENTS.md, CLAUDE.md",
            "content",
            "the two files differ after newline normalisation and CLAUDE.md is not an import "
            "bridge. Nothing fails when two maintained copies disagree, which is why they "
            "drift; collapse CLAUDE.md to a one-line @AGENTS.md bridge.",
        )
    ]


def check_pack_claude_md(pack_dir: Path) -> List[Finding]:
    claude = pack_dir / "CLAUDE.md"
    if not claude.exists():
        return [
            Finding(
                "X7-CLAUDE-MD-IS-A-PATH-STUB",
                "skills/sohrab/CLAUDE.md",
                "skills/sohrab/CLAUDE.md",
                "missing",
                "skills/sohrab/CLAUDE.md does not exist, so a Claude Code session working in "
                "the pack loads no pack contract. Create it as an import bridge whose first "
                "line is @AGENTS.md.",
            )
        ]
    try:
        size = claude.stat().st_size
    except OSError as exc:
        raise CannotRun(f"cannot stat {claude}: {exc}") from exc
    text = read_text(claude, "skills/sohrab/CLAUDE.md")
    stripped = text.strip()

    first = next((ln.strip() for ln in text.split("\n") if ln.strip()), "")
    if IMPORT_BRIDGE_RE.match(first):
        return []

    if BARE_PATH_RE.match(stripped) and (claude.parent / stripped).is_file():
        return [
            Finding(
                "X7-CLAUDE-MD-IS-A-PATH-STUB",
                "skills/sohrab/CLAUDE.md",
                "skills/sohrab/CLAUDE.md",
                stripped,
                f"the whole file is {size} bytes and its entire content is the path "
                f"{stripped!r}, which resolves beside it. This is what a git mode-120000 "
                f"symlink becomes on a checkout without symlink support, and Claude Code "
                f"loads it instead of the contract with no error. Replace it with an import "
                f"bridge whose first line is @{stripped}.",
            )
        ]
    return []


def check_openai_yaml(pack_dir: Path, skills: Sequence[str]) -> List[Finding]:
    out: List[Finding] = []
    for skill in skills:
        if (pack_dir / skill / "agents" / "openai.yaml").is_file():
            continue
        out.append(
            Finding(
                "X8-MISSING-OPENAI-YAML",
                skill,
                f"skills/sohrab/{skill}/agents/openai.yaml",
                "missing",
                "no agents/openai.yaml, so a Codex agent cannot load this skill. README.md "
                "allows exactly one shape of exception -- a Claude-Code-only skill whose Codex "
                "twin ships one. If that is this skill, record it in the baseline with the twin "
                "named in the comment, so the exception is written down and expires when the "
                "file appears rather than living in a hand-maintained list inside a checker.",
            )
        )
    return out


def check_indexes(
    pack_dir: Path, skills: Sequence[str]
) -> Tuple[List[Finding], Dict[str, str]]:
    findings: List[Finding] = []
    notes: Dict[str, str] = {}
    disk = set(skills)

    en_text = read_text(pack_dir / "README.md", "skills/sohrab/README.md")
    map_lines, how = slice_map_region(en_text)
    notes["README.md map located by"] = how
    if how == "heading":
        notes["README.md recommendation"] = (
            f"wrap the map in {MAP_START_MARKER} / {MAP_END_MARKER} so a heading rename cannot "
            f"silently empty this rule"
        )
    en_names = names_from_bullets(map_lines)
    if not en_names:
        raise CannotRun(
            "README.md: the skill map region holds no `name` bullets; the map is not locatable"
        )

    fa_text = read_text(pack_dir / "README.fa.md", "skills/sohrab/README.fa.md")
    fa_names = names_from_tables(fa_text)
    if not fa_names:
        raise CannotRun(
            "README.fa.md: no table row begins with a backticked skill name; the group tables "
            "are not locatable"
        )

    notes["README.md map entries"] = str(len(en_names))
    notes["README.fa.md table entries"] = str(len(fa_names))
    notes["skill directories"] = str(len(disk))

    for name in sorted(disk - set(en_names)):
        findings.append(
            Finding(
                "X1-DIR-NOT-IN-README",
                name,
                "skills/sohrab/README.md",
                name,
                "the directory exists and the skill map does not list it, so README.md's own "
                "sentence 'Every folder in this directory appears exactly once below' is false.",
            )
        )
    for name in sorted(set(en_names) - disk):
        findings.append(
            Finding(
                "X2-README-NAME-NOT-A-DIR",
                name,
                "skills/sohrab/README.md",
                name,
                "the skill map lists a name with no directory; a reader routing to it finds "
                "nothing.",
            )
        )
    for name in sorted(disk - set(fa_names)):
        findings.append(
            Finding(
                "X3-DIR-NOT-IN-README-FA",
                name,
                "skills/sohrab/README.fa.md",
                name,
                "the directory exists and the Persian index does not list it.",
            )
        )
    for name in sorted(set(fa_names) - disk):
        findings.append(
            Finding(
                "X4-README-FA-NAME-NOT-A-DIR",
                name,
                "skills/sohrab/README.fa.md",
                name,
                "the Persian index lists a name with no directory.",
            )
        )
    for name in duplicates(en_names):
        findings.append(
            Finding(
                "X9-DUPLICATE-IN-INDEX",
                name,
                "skills/sohrab/README.md",
                name,
                "listed more than once in the skill map.",
            )
        )
    for name in duplicates(fa_names):
        findings.append(
            Finding(
                "X9-DUPLICATE-IN-INDEX",
                name,
                "skills/sohrab/README.fa.md",
                name,
                "listed more than once in the group tables.",
            )
        )
    for name in sorted(set(consolidated_names(en_text))):
        if (pack_dir / name).is_dir():
            findings.append(
                Finding(
                    "X5-CONSOLIDATED-STILL-EXISTS",
                    name,
                    "skills/sohrab/README.md",
                    name,
                    "listed as consolidated or removed from this pack, but the directory "
                    "exists. One of the two statements is wrong.",
                )
            )
    return findings, notes


def run_checks(root: Path) -> Tuple[List[Finding], Dict[str, str]]:
    pack_dir = root.joinpath(*PACK_RELATIVE)
    if not pack_dir.is_dir():
        raise CannotRun(f"{pack_dir} is not a directory")
    skills = discover_skills(pack_dir)
    findings, notes = check_indexes(pack_dir, skills)
    findings.extend(check_agents_claude_pair(root))
    findings.extend(check_pack_claude_md(pack_dir))
    findings.extend(check_openai_yaml(pack_dir, skills))
    return findings, notes


# --------------------------------------------------------------------------------------
# Baseline
# --------------------------------------------------------------------------------------


def load_baseline(path: Path) -> Tuple[Set[str], Dict[str, str]]:
    try:
        raw = path.read_bytes().decode("utf-8")
    except OSError as exc:
        raise CannotRun(f"cannot read baseline {path}: {exc}") from exc
    except UnicodeDecodeError as exc:
        raise CannotRun(f"baseline {path} is not decodable UTF-8: {exc}")
    keys: Set[str] = set()
    owners: Dict[str, str] = {}
    for lineno, line in enumerate(
        raw.replace("\r\n", "\n").replace("\r", "\n").split("\n"), 1
    ):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        payload, _, comment = stripped.partition("#")
        fields = payload.strip().split("|")
        if len(fields) != 4 or not all(f.strip() for f in fields):
            raise CannotRun(
                f"baseline {path}:{lineno} is malformed; expected "
                f"<rule-id>|<subject>|<location>|<item>, got {stripped!r}"
            )
        if fields[0].strip() not in RULES:
            raise CannotRun(f"baseline {path}:{lineno} names unknown rule {fields[0].strip()!r}")
        key = "|".join(f.strip() for f in fields)
        keys.add(key)
        owners[key] = comment.strip()
    return keys, owners


def write_baseline(path: Path, findings: Sequence[Finding]) -> None:
    lines = [
        "# Baseline for check_skill_index.py.",
        "# One finding per line: <rule-id>|<subject>|<location>|<item>",
        "# A baseline entry that matches no finding exits 1, so this list can only shrink.",
        "# Record why each entry is here; an exception with no stated reason is a defect.",
        "",
    ]
    for f in sorted(findings, key=lambda x: x.key):
        lines.append(f"{f.key}  # owner: {f.subject}")
    # Bytes with explicit LF, so the next reader never sees a carriage return on a key field.
    path.write_bytes(("\n".join(lines) + "\n").encode("utf-8"))


# --------------------------------------------------------------------------------------
# Reporting
# --------------------------------------------------------------------------------------


def report(
    findings: Sequence[Finding],
    stale: Sequence[str],
    stale_owners: Dict[str, str],
    notes: Dict[str, str],
    fmt: str,
) -> None:
    if fmt == "json":
        for f in findings:
            print(f.as_json())
        for key in stale:
            print(
                json.dumps(
                    {
                        "rule": "BASELINE-STALE",
                        "severity": "finding",
                        "key": key,
                        "detail": "baseline entry matches no current finding; remove it",
                        "owner_comment": stale_owners.get(key, ""),
                    },
                    sort_keys=True,
                )
            )
        return
    print("check_skill_index.py")
    for k, v in notes.items():
        print(f"  {k}: {v}")
    if findings:
        print(f"\nFINDINGS ({len(findings)}):")
        for f in sorted(findings, key=lambda x: (x.rule, x.subject)):
            print(f.as_text())
    else:
        print("\nFINDINGS: none")
    if stale:
        print(f"\nSTALE BASELINE ENTRIES ({len(stale)}) -- remove each one:")
        for key in sorted(stale):
            suffix = f"  ({stale_owners[key]})" if stale_owners.get(key) else ""
            print(f"- {key}{suffix}")


# --------------------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------------------

EPILOG = """\
rules
  X1-DIR-NOT-IN-README          a skill directory is absent from README.md's skill map
  X2-README-NAME-NOT-A-DIR      a name in that map has no directory
  X3-DIR-NOT-IN-README-FA       a skill directory is absent from README.fa.md's group tables
  X4-README-FA-NAME-NOT-A-DIR   a name in those tables has no directory
  X5-CONSOLIDATED-STILL-EXISTS  a name listed as consolidated or removed exists as a directory
  X6-AGENTS-CLAUDE-DIVERGED     root AGENTS.md and root CLAUDE.md are neither equal after
                                newline normalisation nor joined by an @AGENTS.md bridge
  X7-CLAUDE-MD-IS-A-PATH-STUB   skills/sohrab/CLAUDE.md's entire content is a path that resolves
                                beside it -- what a mode-120000 symlink becomes on a checkout
                                without symlink support, loaded silently in place of the
                                contract
  X8-MISSING-OPENAI-YAML        a skill directory has no agents/openai.yaml
  X9-DUPLICATE-IN-INDEX         a name appears more than once in one index

how the map is located
  README.md is read between <!-- skill-map:start --> and <!-- skill-map:end --> when those
  markers exist, and otherwise from the '## Current skill map' heading to the next '## '.
  README.fa.md is read from every table row whose first cell is a backticked name.

exceptions
  There is no hardcoded exception list in this file. A legitimate exception goes in the baseline
  with its reason in the trailing comment, and a baseline entry that stops matching exits 1, so
  an exception cannot outlive the condition that justified it.

exit codes
  0 clean   1 findings, or a stale baseline entry   2 could not run
"""


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="check_skill_index.py",
        description=(
            "Assert that every index in skills/sohrab/ agrees with the disk in both directions, "
            "and that the agent-instruction files that are meant to be one file still are."
        ),
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument(
        "--root",
        help="repository root containing skills/sohrab. Default: nearest ancestor of the "
        "current directory that contains it.",
    )
    p.add_argument("--baseline", metavar="PATH", help="suppress findings listed in this file.")
    p.add_argument(
        "--write-baseline",
        metavar="PATH",
        help="write the current findings as a baseline and exit 0.",
    )
    p.add_argument("--format", choices=("text", "json"), default="text")
    return p


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        root = find_root(args.root)
        findings, notes = run_checks(root)
    except CannotRun as exc:
        print(f"could not run: {exc}", file=sys.stderr)
        return EXIT_CANNOT_RUN
    except OSError as exc:
        print(f"could not run: {exc}", file=sys.stderr)
        return EXIT_CANNOT_RUN

    if args.write_baseline:
        try:
            write_baseline(Path(args.write_baseline).expanduser(), findings)
        except OSError as exc:
            print(f"could not run: cannot write baseline: {exc}", file=sys.stderr)
            return EXIT_CANNOT_RUN
        print(f"wrote {len(findings)} baseline entries to {args.write_baseline}")
        return EXIT_CLEAN

    stale: List[str] = []
    stale_owners: Dict[str, str] = {}
    if args.baseline:
        try:
            keys, owners = load_baseline(Path(args.baseline).expanduser())
        except CannotRun as exc:
            print(f"could not run: {exc}", file=sys.stderr)
            return EXIT_CANNOT_RUN
        present = {f.key for f in findings}
        findings = [f for f in findings if f.key not in keys]
        stale = sorted(keys - present)
        stale_owners = {k: owners.get(k, "") for k in stale}

    report(findings, stale, stale_owners, notes, args.format)
    return EXIT_FINDINGS if (findings or stale) else EXIT_CLEAN


if __name__ == "__main__":
    raise SystemExit(main())
