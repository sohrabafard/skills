#!/usr/bin/env python3
"""Fleet-scope cross-reference checker for skills/sohrab/.

WHAT THIS ASSERTS
    Every bundled-resource path cited inside a skill's Markdown resolves, and every
    cross-skill citation names the skill that owns the path. Citations in this fleet are
    written as inline code, not as Markdown links: a link checker built on Markdown link
    syntax inspects roughly one citation in four hundred here, so this tool reads raw text.

EXIT CODES
    0  clean          zero findings after baseline suppression
    1  findings       one or more findings, or a baseline entry that matches nothing
    2  could not run  root not found, skills/sohrab absent or unreadable, zero skills
                      discovered, a Markdown file that is not decodable UTF-8, or a
                      baseline file that is named but unreadable or malformed

THE TWO PATH NOTATIONS
    A skill's Markdown cites two kinds of path and, until this notation existed, nothing in
    the text distinguished them. `references/10-foo.md` means "the file I ship"; `docs/BIG_PICTURE.md`
    means "the file you are to write in the repository you are working on". Fleet-wide there are
    519 of the second kind. A checker that fails on them is switched off within a week, and an
    exclusion list of that size is a hand-maintained list -- the defect class this tool exists to end.

    So the pair is marked at the source instead:

        $SKILL_DIR/<path>   a path bundled inside the citing skill.  Checked: it must exist.
        <repo>/<path>       a path in the target repository the agent is working on.
                            Never resolved, never a finding.

    Both markers already occur in the tree, which is why they were chosen over inventing a
    third: `$SKILL_DIR/` at nine sites in alaa-postman-collections, and `<repo>/` in
    alaa-postman-collections/references/70-aggregate-collections-and-consumer-repos.md and
    vector-rust-observability-pipelines/INSTALL.md. A marked path stops matching the bare-path
    scanner entirely, so each edited citation moves from INFO to MARKED-TARGET-REPO one commit
    at a time. Until a site is marked, an unresolved non-references/ path is reported under
    I1-UNMARKED-TARGET-PATH, which is informational and never fails the run.

THE LIMIT OF INCREMENTAL ADOPTION -- measured, and narrower than "mark at leisure"
    An unmarked target-repository path lands in the informational I1-UNMARKED-TARGET-PATH class
    only while no other skill is named on the same line. Name one -- as every routing sentence
    does -- and step 7 of the resolution order promotes that same path to R1-DANGLING-NAMED,
    which fails. A line that routes to an owning skill and also names a target-repository path
    therefore has no passing unmarked state: it must be marked in the commit that writes it.
    Every other site can be marked at leisure.

    This is measured, not predicted. Batch 8's own rewrites added exactly that shape and turned
    13 informational items into hard findings without citing a single new path. Loosening the
    promotion rule was considered and rejected; fixtures/EXPECTED-FLEET-CENSUS.md records the
    measurement, the rejected alternative, and the reason.

WINDOWS
    Python 3 standard library only. No pip install, no npm install. Paths are built with
    pathlib, files are read as bytes and decoded explicitly, and CRLF is normalised before any
    line is parsed -- a carriage return left on the last field of a parsed line makes every
    comparison fail while the rendered bytes look identical. No temp directory is created.
    The tree is enumerated at runtime; no skill name is hardcoded anywhere in this file.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple

EXIT_CLEAN = 0
EXIT_FINDINGS = 1
EXIT_CANNOT_RUN = 2

PACK_RELATIVE = ("skills", "sohrab")

# Directory alternation. `docs`, `test` and `tests` are deliberately included even though
# almost every citation under them is a target-repository path: including them is what turns
# 519 invisible ambiguous paths into a countable INFO class that the notation can retire.
RESOURCE_DIRS = (
    "references",
    "scripts",
    "assets",
    "templates",
    "agents",
    "examples",
    "prompts",
    "evals",
    "fixtures",
    "docs",
    "test",
    "tests",
    "ci",
    "charts",
)

# Extensions ordered longest-first. The trailing lookahead already prevents `.js` from
# matching inside `.json`, but the ordering is kept as well: an earlier generation of this
# resolver truncated references/arvan-caas-openAPI-1.25.json to .js and invented two phantom
# dangling citations. Both guards are asserted by a fixture.
EXTENSIONS = (
    "jsonc",
    "json",
    "yaml",
    "toml",
    "conf",
    "cjs",
    "mjs",
    "ps1",
    "sql",
    "txt",
    "vrl",
    "yml",
    "cfg",
    "ini",
    "lua",
    "php",
    "tpl",
    "md",
    "js",
    "py",
    "sh",
    "ts",
    "go",
)

PATH_RE = re.compile(
    r"(?<![A-Za-z0-9_./-])"
    r"((?:\.\.?/|[A-Za-z0-9_.-]+/)*?"
    r"(?:" + "|".join(RESOURCE_DIRS) + r")"
    r"/[A-Za-z0-9_./-]+\.(?:" + "|".join(EXTENSIONS) + r"))"
    r"(?![A-Za-z0-9])"
)

MARKED_REPO_RE = re.compile(r"(?<![A-Za-z0-9_-])<repo>/([A-Za-z0-9_./-]+)")
MARKED_SKILLDIR_RE = re.compile(r"\$SKILL_DIR/([A-Za-z0-9_./-]+)")

# Exclusion 3: a sentence about a file this skill already retired is not a live citation.
# Evidence: ansible-validator/references/failure-classes.md:4,
# alaa-docker-production/references/00-source-map.md:4,
# alaa-indexeddb-browser-storage/references/99-sources-and-maintenance.md:74.
RETIREMENT_RE = re.compile(
    r"\b(was|were|formerly|replaces the former|replaced the former|used to be|retired|no longer)\b",
    re.I,
)
RETIREMENT_WINDOW = 80

INLINE_SPAN_RE = re.compile(r"`([^`\n]*)`")

TOPIC_MAP_NAMES = ("00-topic-map.md",)

SKIP_DIR_NAMES = {
    "__pycache__",
    "node_modules",
    ".git",
    "_to_delete",
    ".obsidian",
    ".claude",
    "vendor",
}
# alaa-repo-docs/assets/fixtures/undecodable/bad.md is deliberately invalid UTF-8 with a null
# byte. It is excluded from the scan by default and, when --include-fixtures forces it back in,
# it produces exit 2 rather than a crash. Both halves are asserted by fixtures.
FIXTURE_DIR_NAMES = {"fixtures"}

RULES: Dict[str, str] = {
    "R1-DANGLING-NAMED": "a citation whose owning skill is explicitly named does not resolve inside that skill",
    "R2-DANGLING-LOCAL": "a references/ citation with no named owner, or a $SKILL_DIR/ citation, resolves nowhere",
    "R3-AMBIGUOUS-MULTI": "a references/ citation with no named owner resolves in more than one other skill",
    "R4-AMBIGUOUS-BARE": "a references/ citation resolves only in another skill and names no owner in its paragraph",
    "R5-CONTEXTUAL": "the owning skill is named nearby but not on the same line as the path",
    "R6-TOPIC-MAP": "a path cited by a references/00-topic-map.md router resolves nowhere",
}
INFO_RULE = "I1-UNMARKED-TARGET-PATH"

# Classification labels, reported by --census.
CENSUS_ORDER = (
    "RESOLVES-LOCALLY",
    "RESOLVES-CROSS-SKILL",
    "RESOLVES-CROSS-SKILL-CONTEXTUAL",
    "RESOLVES-RELATIVE",
    "MARKED-BUNDLED",
    "MARKED-TARGET-REPO",
    "AMBIGUOUS-BARE",
    "AMBIGUOUS-MULTI",
    "DANGLING",
    "DANGLING-NAMED",
    "SKIPPED-COMMAND-EXAMPLE",
    "SKIPPED-RETIREMENT-PROSE",
)


class CannotRun(Exception):
    """Raised for every condition that means the checker could not evaluate its rules."""


class Finding:
    __slots__ = ("rule", "skill", "relpath", "line", "cited", "detail", "severity")

    def __init__(
        self,
        rule: str,
        skill: str,
        relpath: str,
        line: int,
        cited: str,
        detail: str,
        severity: str = "finding",
    ) -> None:
        self.rule = rule
        self.skill = skill
        self.relpath = relpath
        self.line = line
        self.cited = cited
        self.detail = detail
        self.severity = severity

    @property
    def key(self) -> str:
        """Baseline key. The line number is deliberately absent: it changes on every edit
        above the citation, which would churn the baseline and silently un-suppress real
        findings."""
        return f"{self.rule}|{self.skill}|{self.relpath}|{self.cited}"

    def as_text(self) -> str:
        return (
            f"- {self.rule} {self.skill}/{self.relpath}:{self.line}\n"
            f"    cited: {self.cited}\n"
            f"    {self.detail}"
        )

    def as_json(self) -> str:
        return json.dumps(
            {
                "rule": self.rule,
                "severity": self.severity,
                "skill": self.skill,
                "file": self.relpath,
                "line": self.line,
                "cited": self.cited,
                "detail": self.detail,
                "key": self.key,
            },
            sort_keys=True,
        )


# --------------------------------------------------------------------------------------
# Tree discovery
# --------------------------------------------------------------------------------------


def find_root(explicit: Optional[str]) -> Path:
    if explicit is not None:
        candidate = Path(explicit).expanduser()
        if not candidate.is_dir():
            raise CannotRun(f"--root is not a directory: {candidate}")
        if not candidate.joinpath(*PACK_RELATIVE).is_dir():
            raise CannotRun(
                f"--root {candidate} does not contain {'/'.join(PACK_RELATIVE)}"
            )
        return candidate
    here = Path.cwd().resolve()
    for candidate in (here, *here.parents):
        if candidate.joinpath(*PACK_RELATIVE).is_dir():
            return candidate
    raise CannotRun(
        f"no ancestor of {here} contains {'/'.join(PACK_RELATIVE)}; pass --root explicitly"
    )


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


def markdown_files(skill_dir: Path, include_fixtures: bool) -> List[Path]:
    out: List[Path] = []
    stack = [skill_dir]
    while stack:
        current = stack.pop()
        try:
            entries = sorted(current.iterdir())
        except OSError as exc:
            raise CannotRun(f"cannot read {current}: {exc}") from exc
        for entry in entries:
            if entry.is_symlink() and entry.is_dir():
                continue
            if entry.is_dir():
                if entry.name in SKIP_DIR_NAMES:
                    continue
                if not include_fixtures and entry.name in FIXTURE_DIR_NAMES:
                    continue
                stack.append(entry)
            elif entry.suffix.lower() == ".md":
                out.append(entry)
    return sorted(out)


def read_text(path: Path) -> str:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise CannotRun(f"cannot read {path}: {exc}") from exc
    if b"\x00" in raw:
        raise CannotRun(f"{path} contains a NUL byte and is not decodable text")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise CannotRun(f"{path} is not decodable UTF-8: {exc}")
    if text.startswith("\ufeff"):
        text = text[1:]
    # Normalise before any line is parsed. A trailing carriage return on the last field of a
    # line makes every comparison fail while the rendered bytes look identical.
    return text.replace("\r\n", "\n").replace("\r", "\n")


# --------------------------------------------------------------------------------------
# Resolution
# --------------------------------------------------------------------------------------


def normalise(path_text: str) -> str:
    return path_text.replace("\\", "/").strip()


def resolve_within(pack_dir: Path, skill: str, rel: str) -> bool:
    target = (pack_dir / skill / rel)
    try:
        return target.is_file()
    except OSError:
        return False


def owners_of(pack_dir: Path, skills: Sequence[str], rel: str, exclude: str) -> List[str]:
    return [s for s in skills if s != exclude and resolve_within(pack_dir, s, rel)]


def names_on(line: str, skills: Sequence[str]) -> List[Tuple[int, str]]:
    """Every known skill name occurring on the line, with its start offset.

    No adjacency requirement. The fleet's dominant citation form is
    `/owner` (`$owner`) `references/...`, where an intervening backtick and closing
    parenthesis separate the owner from the path. A resolver that required the owner to be the
    immediately preceding token rejected 150 correctly attributed citations and reported 582
    unresolved paths against a fleet that has eight real defects.
    """
    found: List[Tuple[int, str]] = []
    for name in skills:
        for m in re.finditer(
            r"(?<![A-Za-z0-9_-])" + re.escape(name) + r"(?![A-Za-z0-9_-])", line
        ):
            found.append((m.start(), name))
    found.sort()
    return found


def paragraph_names(
    lines: Sequence[str], index: int, skills: Sequence[str], span: int = 6
) -> Set[str]:
    """Skill names on the preceding lines of the same paragraph, stopping at a blank line."""
    out: Set[str] = set()
    for back in range(1, span + 1):
        j = index - back
        if j < 0:
            break
        if not lines[j].strip():
            break
        out.update(name for _, name in names_on(lines[j], skills))
    return out


def in_command_span(line: str, start: int, end: int) -> bool:
    """True when the citation sits inside an inline code span whose content has whitespace.

    Evidence: alaa-prompting-guide/references/60-skill-authoring.md:69 writes
    `Read references/failure-taxonomy.md when a check fails` -- an illustrative sentence in a
    code span, not a citation. validate_sohrab_skill_pack.py implements the same test as
    is_command_example.
    """
    for m in INLINE_SPAN_RE.finditer(line):
        if m.start(1) <= start and end <= m.end(1):
            return any(ch.isspace() for ch in m.group(1))
    return False


def in_retirement_prose(line: str, start: int) -> bool:
    window = line[max(0, start - RETIREMENT_WINDOW) : start]
    return RETIREMENT_RE.search(window) is not None


class Citation:
    __slots__ = ("skill", "relpath", "line_no", "cited", "cls", "detail", "prefix")

    def __init__(
        self, skill: str, relpath: str, line_no: int, cited: str, cls: str, detail: str
    ) -> None:
        self.skill = skill
        self.relpath = relpath
        self.line_no = line_no
        self.cited = cited
        self.cls = cls
        self.detail = detail
        self.prefix = cited.split("/", 1)[0] if "/" in cited else cited


def classify_line(
    pack_dir: Path,
    skills: Sequence[str],
    skill: str,
    file_relpath: str,
    file_dir_rel: str,
    lines: Sequence[str],
    index: int,
) -> List[Citation]:
    """Classify every citation on one line. Rule order is documented in --help and is the
    order the 2026-07-29 fleet census was measured with, plus the two markers."""
    line = lines[index]
    line_no = index + 1
    out: List[Citation] = []

    def add(cited: str, cls: str, detail: str = "") -> None:
        out.append(Citation(skill, file_relpath, line_no, cited, cls, detail))

    # Character ranges already consumed by a marker. Without this, `$SKILL_DIR/scripts/x.py`
    # is counted twice: the general scanner starts matching at SKILL_DIR, because the character
    # before it is `$`, which the lookbehind does not block.
    consumed: List[Tuple[int, int]] = []

    for m in MARKED_SKILLDIR_RE.finditer(line):
        consumed.append((m.start(), m.end()))
        rel = normalise(m.group(1))
        if resolve_within(pack_dir, skill, rel):
            add(f"$SKILL_DIR/{rel}", "MARKED-BUNDLED")
        else:
            add(
                f"$SKILL_DIR/{rel}",
                "DANGLING",
                f"marked as bundled but {skill}/{rel} does not exist",
            )

    for m in MARKED_REPO_RE.finditer(line):
        consumed.append((m.start(), m.end()))
        add(f"<repo>/{normalise(m.group(1))}", "MARKED-TARGET-REPO")

    for m in PATH_RE.finditer(line):
        if any(s < m.end(1) and m.start(1) < e for s, e in consumed):
            continue
        raw = m.group(1)
        cited = normalise(raw)
        if in_command_span(line, m.start(1), m.end(1)):
            add(cited, "SKIPPED-COMMAND-EXAMPLE")
            continue
        if in_retirement_prose(line, m.start(1)):
            add(cited, "SKIPPED-RETIREMENT-PROSE")
            continue

        # 1. explicit owning-skill prefix
        head = cited.split("/", 1)[0]
        if head in skills and "/" in cited:
            owner, rest = cited.split("/", 1)
            if resolve_within(pack_dir, owner, rest):
                add(cited, "RESOLVES-CROSS-SKILL", f"owner named as a path prefix: {owner}")
            else:
                add(cited, "DANGLING-NAMED", f"{owner} does not contain {rest}")
            continue

        # 2. ./ and ../ resolve against the citing file's directory, not the skill root.
        if cited.startswith("./") or cited.startswith("../"):
            base = (pack_dir / skill / file_dir_rel) if file_dir_rel else (pack_dir / skill)
            try:
                candidate = (base / cited).resolve()
                ok = candidate.is_file()
            except OSError:
                ok = False
            if ok:
                add(cited, "RESOLVES-RELATIVE", "resolves against the citing file's directory")
            else:
                add(
                    cited,
                    "DANGLING",
                    "relative path does not resolve against the citing file's directory",
                )
            continue

        named = names_on(line, skills)
        named_before = [n for pos, n in named if pos < m.start(1) and n != skill]
        named_after = [n for pos, n in named if pos >= m.end(1) and n != skill]

        # 3. owner named earlier on the same line and owns the path
        hit = next((n for n in named_before if resolve_within(pack_dir, n, cited)), None)
        if hit:
            add(cited, "RESOLVES-CROSS-SKILL", f"owner named on this line: {hit}")
            continue

        # 4. resolves inside the citing skill
        if resolve_within(pack_dir, skill, cited):
            add(cited, "RESOLVES-LOCALLY")
            continue

        # 5. owner named later on the same line and owns the path
        hit = next((n for n in named_after if resolve_within(pack_dir, n, cited)), None)
        if hit:
            add(cited, "RESOLVES-CROSS-SKILL", f"owner named on this line: {hit}")
            continue

        # 6. owner named on a preceding line of the same paragraph
        nearby = paragraph_names(lines, index, skills)
        hit = next(
            (n for n in sorted(nearby) if n != skill and resolve_within(pack_dir, n, cited)),
            None,
        )
        if hit:
            add(
                cited,
                "RESOLVES-CROSS-SKILL-CONTEXTUAL",
                f"owner {hit} is named nearby but not on this line",
            )
            continue

        # 7. a skill is named on the line but none of them owns the path
        others = [n for _, n in named if n != skill]
        if others:
            add(
                cited,
                "DANGLING-NAMED",
                "named on this line: "
                + ", ".join(sorted(set(others)))
                + "; none of them contains this path",
            )
            continue

        owners = owners_of(pack_dir, skills, cited, skill)
        if len(owners) == 1:
            add(cited, "AMBIGUOUS-BARE", f"owned only by {owners[0]}; name the owner on this line")
        elif len(owners) > 1:
            add(
                cited,
                "AMBIGUOUS-MULTI",
                "owned by " + ", ".join(owners) + "; name the intended owner on this line",
            )
        else:
            add(cited, "DANGLING", "resolves in no skill in the fleet")
    return out


def to_findings(citations: Iterable[Citation], strict_owner: bool) -> Tuple[List[Finding], List[Finding]]:
    findings: List[Finding] = []
    info: List[Finding] = []
    for c in citations:
        is_reference = c.cited.startswith("references/") or c.prefix == "references"
        is_topic_map = Path(c.relpath).name in TOPIC_MAP_NAMES
        marked_bundled = c.cited.startswith("$SKILL_DIR/")

        if c.cls == "DANGLING-NAMED":
            findings.append(
                Finding("R1-DANGLING-NAMED", c.skill, c.relpath, c.line_no, c.cited, c.detail)
            )
        elif c.cls == "DANGLING":
            if is_topic_map:
                findings.append(
                    Finding(
                        "R6-TOPIC-MAP",
                        c.skill,
                        c.relpath,
                        c.line_no,
                        c.cited,
                        c.detail + "; a router that points at nothing is worse than no router",
                    )
                )
            elif is_reference or marked_bundled:
                findings.append(
                    Finding("R2-DANGLING-LOCAL", c.skill, c.relpath, c.line_no, c.cited, c.detail)
                )
            else:
                info.append(
                    Finding(
                        INFO_RULE,
                        c.skill,
                        c.relpath,
                        c.line_no,
                        c.cited,
                        f"if this names a path in the target repository, write it as <repo>/{c.cited}",
                        severity="info",
                    )
                )
        elif c.cls == "AMBIGUOUS-MULTI":
            if is_reference:
                findings.append(
                    Finding("R3-AMBIGUOUS-MULTI", c.skill, c.relpath, c.line_no, c.cited, c.detail)
                )
        elif c.cls == "AMBIGUOUS-BARE":
            if is_reference:
                findings.append(
                    Finding("R4-AMBIGUOUS-BARE", c.skill, c.relpath, c.line_no, c.cited, c.detail)
                )
        elif c.cls == "RESOLVES-CROSS-SKILL-CONTEXTUAL" and strict_owner:
            findings.append(
                Finding("R5-CONTEXTUAL", c.skill, c.relpath, c.line_no, c.cited, c.detail)
            )
    return findings, info


def scan(
    root: Path,
    only_skills: Optional[Sequence[str]],
    strict_owner: bool,
    include_fixtures: bool,
) -> Tuple[List[Finding], List[Finding], Dict[str, int], Dict[str, int]]:
    pack_dir = root.joinpath(*PACK_RELATIVE)
    if not pack_dir.is_dir():
        raise CannotRun(f"{pack_dir} is not a directory")
    skills = discover_skills(pack_dir)
    if only_skills:
        unknown = [s for s in only_skills if s not in skills]
        if unknown:
            raise CannotRun("--skill names no such skill: " + ", ".join(sorted(unknown)))
        scan_list = [s for s in skills if s in set(only_skills)]
    else:
        scan_list = list(skills)

    citations: List[Citation] = []
    counts = {"skills": len(skills), "scanned_skills": len(scan_list), "files": 0}
    for skill in scan_list:
        skill_dir = pack_dir / skill
        for md in markdown_files(skill_dir, include_fixtures):
            counts["files"] += 1
            text = read_text(md)
            rel = md.relative_to(skill_dir).as_posix()
            dir_rel = md.parent.relative_to(skill_dir).as_posix()
            dir_rel = "" if dir_rel == "." else dir_rel
            lines = text.split("\n")
            for i in range(len(lines)):
                if not lines[i].strip():
                    continue
                citations.extend(
                    classify_line(pack_dir, skills, skill, rel, dir_rel, lines, i)
                )

    census: Dict[str, int] = {label: 0 for label in CENSUS_ORDER}
    for c in citations:
        census[c.cls] = census.get(c.cls, 0) + 1
    census["TOTAL"] = len(citations)

    refs = [c for c in citations if c.prefix == "references"]
    refs_census: Dict[str, int] = {label: 0 for label in CENSUS_ORDER}
    for c in refs:
        refs_census[c.cls] = refs_census.get(c.cls, 0) + 1
    refs_census["TOTAL"] = len(refs)

    findings, info = to_findings(citations, strict_owner)
    counts.update({"citations": len(citations)})
    return findings, info, census, refs_census, counts  # type: ignore[return-value]


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
    for lineno, line in enumerate(raw.replace("\r\n", "\n").replace("\r", "\n").split("\n"), 1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        payload, _, comment = stripped.partition("#")
        payload = payload.strip()
        fields = payload.split("|")
        if len(fields) != 4 or not all(f.strip() for f in fields):
            raise CannotRun(
                f"baseline {path}:{lineno} is malformed; expected "
                f"<rule-id>|<skill>|<file>|<cited-path>, got {stripped!r}"
            )
        rule = fields[0].strip()
        if rule not in RULES:
            raise CannotRun(f"baseline {path}:{lineno} names unknown rule {rule!r}")
        key = "|".join(f.strip() for f in fields)
        keys.add(key)
        owners[key] = comment.strip()
    return keys, owners


def write_baseline(path: Path, findings: Sequence[Finding]) -> None:
    lines = [
        "# Baseline for check_fleet_references.py.",
        "# One finding per line: <rule-id>|<skill>|<file>|<cited-path>",
        "# The line number is deliberately absent so an unrelated edit above a citation does",
        "# not churn this file. A baseline entry that matches no finding exits 1, so this list",
        "# can only shrink -- it never becomes a permanent amnesty.",
        "",
    ]
    for f in sorted(findings, key=lambda x: x.key):
        lines.append(f"{f.key}  # owner: {f.skill}")
    # Written as bytes with explicit LF: text mode on Windows would emit CRLF, and the next
    # reader would carry a carriage return on the last field of every key.
    path.write_bytes(("\n".join(lines) + "\n").encode("utf-8"))


# --------------------------------------------------------------------------------------
# Reporting
# --------------------------------------------------------------------------------------


def print_census(census: Dict[str, int], refs_census: Dict[str, int]) -> None:
    print("CENSUS -- all bundled-resource prefixes")
    for label in CENSUS_ORDER:
        print(f"  {census.get(label, 0):6d}  {label}")
    print(f"  {census.get('TOTAL', 0):6d}  TOTAL")
    print("CENSUS -- scoped to references/")
    for label in CENSUS_ORDER:
        print(f"  {refs_census.get(label, 0):6d}  {label}")
    print(f"  {refs_census.get('TOTAL', 0):6d}  TOTAL")
    print(
        "  Compare against the 2026-07-29 measurement recorded in "
        "fixtures/EXPECTED-FLEET-CENSUS.md."
    )


def report(
    findings: Sequence[Finding],
    info: Sequence[Finding],
    stale: Sequence[str],
    stale_owners: Dict[str, str],
    counts: Dict[str, int],
    fmt: str,
    show_info: bool,
) -> None:
    if fmt == "json":
        for f in findings:
            print(f.as_json())
        for f in info:
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

    print(
        f"check_fleet_references.py: {counts['scanned_skills']} of {counts['skills']} skills, "
        f"{counts['files']} Markdown files, {counts['citations']} citations"
    )
    if findings:
        print(f"\nFINDINGS ({len(findings)}):")
        for f in sorted(findings, key=lambda x: (x.rule, x.skill, x.relpath, x.line)):
            print(f.as_text())
    else:
        print("\nFINDINGS: none")

    if stale:
        print(f"\nSTALE BASELINE ENTRIES ({len(stale)}) -- remove each one:")
        for key in sorted(stale):
            suffix = f"  ({stale_owners[key]})" if stale_owners.get(key) else ""
            print(f"- {key}{suffix}")

    if info:
        by_skill: Dict[str, int] = {}
        for f in info:
            by_skill[f.skill] = by_skill.get(f.skill, 0) + 1
        print(
            f"\nINFO ({len(info)} unmarked target-repository paths across "
            f"{len(by_skill)} skills; these never fail the run)"
        )
        if show_info:
            for f in sorted(info, key=lambda x: (x.skill, x.relpath, x.line)):
                print(f.as_text())
        else:
            for skill, n in sorted(by_skill.items(), key=lambda kv: (-kv[1], kv[0])):
                print(f"  {n:4d}  {skill}")
            print("  Rerun with --show-info for every site, or --format json for all of them.")
            print("  Mark each one as <repo>/<path> to retire it from this list.")


# --------------------------------------------------------------------------------------
# Self-test
# --------------------------------------------------------------------------------------

# Each case is (fixture directory name, extra argv, expected exit, expected rule counts).
# expected rule counts of None means "not asserted".
SELF_TEST_CASES: Tuple[Tuple[str, Tuple[str, ...], int, Optional[Dict[str, int]]], ...] = (
    ("green", (), EXIT_CLEAN, {}),
    ("green-trap-forms", (), EXIT_CLEAN, {}),
    ("green-marked-notation", (), EXIT_CLEAN, {}),
    ("red-r1-dangling-named", (), EXIT_FINDINGS, {"R1-DANGLING-NAMED": 2}),
    ("red-r2-dangling-local", (), EXIT_FINDINGS, {"R2-DANGLING-LOCAL": 2}),
    ("red-r3-ambiguous-multi", (), EXIT_FINDINGS, {"R3-AMBIGUOUS-MULTI": 1}),
    ("red-r4-ambiguous-bare", (), EXIT_FINDINGS, {"R4-AMBIGUOUS-BARE": 1}),
    ("red-r5-contextual", (), EXIT_CLEAN, {}),
    ("red-r5-contextual", ("--strict-owner",), EXIT_FINDINGS, {"R5-CONTEXTUAL": 1}),
    ("red-r6-topic-map", (), EXIT_FINDINGS, {"R6-TOPIC-MAP": 1}),
    ("red-undecodable", (), EXIT_CLEAN, {}),
    ("red-undecodable", ("--include-fixtures",), EXIT_CANNOT_RUN, None),
    ("red-no-skills", (), EXIT_CANNOT_RUN, None),
)

# Baseline behaviour is asserted against the red-r4 fixture: suppressing its one finding must
# reach 0, and a baseline naming a finding that no longer exists must reach 1.
SELF_TEST_BASELINES: Tuple[Tuple[str, str, int], ...] = (
    ("red-r4-ambiguous-bare", "baseline-suppresses.txt", EXIT_CLEAN),
    ("red-r4-ambiguous-bare", "baseline-stale.txt", EXIT_FINDINGS),
    ("red-r4-ambiguous-bare", "baseline-malformed.txt", EXIT_CANNOT_RUN),
)


def run_case(root: Path, argv: Sequence[str]) -> Tuple[int, str]:
    """Run the checker in-process against one fixture root and capture its output."""
    import io
    import contextlib

    buf = io.StringIO()
    code = EXIT_CANNOT_RUN
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        code = main(["--root", str(root), *argv])
    return code, buf.getvalue()


def self_test(fixtures_dir: Path) -> int:
    if not fixtures_dir.is_dir():
        print(f"BLOCKED: fixture directory not found: {fixtures_dir}")
        return EXIT_CANNOT_RUN
    base = fixtures_dir / "fleet"
    if not base.is_dir():
        print(f"BLOCKED: fixture directory not found: {base}")
        return EXIT_CANNOT_RUN

    passed = failed = blocked = 0
    for name, extra, expect_code, expect_rules in SELF_TEST_CASES:
        root = base / name
        if not root.is_dir():
            print(f"BLOCKED  {name} {' '.join(extra)}: fixture root missing ({root})")
            blocked += 1
            continue
        code, out = run_case(root, extra)
        label = f"{name} {' '.join(extra)}".strip()
        if code != expect_code:
            if code == EXIT_CANNOT_RUN:
                print(f"BLOCKED  {label}: exit 2 (could not run), expected {expect_code}")
                print("         " + out.strip().replace("\n", "\n         "))
                blocked += 1
            else:
                print(f"FAIL     {label}: exit {code}, expected {expect_code}")
                print("         " + out.strip().replace("\n", "\n         "))
                failed += 1
            continue
        if expect_rules is not None:
            observed: Dict[str, int] = {}
            for line in out.split("\n"):
                stripped = line.strip()
                if stripped.startswith("- R"):
                    rule = stripped.split()[1]
                    observed[rule] = observed.get(rule, 0) + 1
            if observed != expect_rules:
                print(f"FAIL     {label}: rules {observed}, expected {expect_rules}")
                failed += 1
                continue
        print(f"PASS     {label}")
        passed += 1

    for name, baseline_name, expect_code in SELF_TEST_BASELINES:
        root = base / name
        baseline = base / name / baseline_name
        label = f"{name} --baseline {baseline_name}"
        if not baseline.is_file():
            print(f"BLOCKED  {label}: baseline fixture missing ({baseline})")
            blocked += 1
            continue
        code, out = run_case(root, ("--baseline", str(baseline)))
        if code != expect_code:
            if code == EXIT_CANNOT_RUN and expect_code != EXIT_CANNOT_RUN:
                print(f"BLOCKED  {label}: exit 2, expected {expect_code}")
                blocked += 1
            else:
                print(f"FAIL     {label}: exit {code}, expected {expect_code}")
                print("         " + out.strip().replace("\n", "\n         "))
                failed += 1
            continue
        print(f"PASS     {label}")
        passed += 1

    # The extension-ordering regression from the 2026-07-29 survey, asserted directly.
    probe = "see `references/arvan-caas-openAPI-1.25.json` for the matrix"
    got = PATH_RE.findall(probe)
    if got != ["references/arvan-caas-openAPI-1.25.json"]:
        print(f"FAIL     extension-ordering probe: matched {got!r}")
        failed += 1
    else:
        print("PASS     extension-ordering probe (.json is not truncated to .js)")
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
  R1-DANGLING-NAMED    a citation whose owning skill is explicitly named -- as a path prefix,
                       or as the only skills named on the line -- does not resolve in it.
  R2-DANGLING-LOCAL    a references/ citation with no named owner, or a $SKILL_DIR/ citation,
                       resolves nowhere in the fleet.
  R3-AMBIGUOUS-MULTI   a references/ citation with no named owner resolves in more than one
                       other skill.
  R4-AMBIGUOUS-BARE    a references/ citation resolves only in one other skill and names no
                       owner anywhere in its paragraph.
  R5-CONTEXTUAL        the owning skill is named nearby but not on the same line.
                       OFF unless --strict-owner: turning it on converts 154 currently passing
                       citations into findings, 58 of them in alaa-frontend-developer alone.
  R6-TOPIC-MAP         a path cited by a references/00-topic-map.md router resolves nowhere.
  I1-UNMARKED-TARGET-PATH
                       informational, never fails: a non-references/ path that resolves nowhere
                       and carries no marker. Write it as <repo>/<path> to retire it.
                       This class holds only while no other skill is named on the same line.
                       Name one and step 7 below promotes the same path to R1, so a routing
                       sentence has no passing unmarked state and must be marked when written.

path notations
  $SKILL_DIR/<path>    bundled inside the citing skill. Checked; missing file is R2.
  <repo>/<path>        in the target repository the agent is working on. Never resolved.

resolution order
  1 explicit owning-skill path prefix       2 ./ and ../ against the citing file's directory
  3 owner named earlier on the same line    4 resolves inside the citing skill
  5 owner named later on the same line      6 owner named on a preceding line of the paragraph
  7 a skill is named but owns nothing -> R1 8 one other owner -> R4, several -> R3, none -> R2/I1

exclusions
  * an inline code span whose content contains whitespace is an example, not a citation
  * a line whose 80 characters before the path say was/were/formerly/retired is retirement prose
  * globs and placeholders are not paths
  * directories named fixtures are skipped unless --include-fixtures

exit codes
  0 clean   1 findings, or a stale baseline entry   2 could not run
"""


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="check_fleet_references.py",
        description=(
            "Assert that every bundled-resource path cited in skills/sohrab/ resolves and "
            "that every cross-skill citation names the skill that owns it."
        ),
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument(
        "--root",
        help="repository root containing skills/sohrab. Default: nearest ancestor of the "
        "current directory that contains it.",
    )
    p.add_argument(
        "--skill",
        action="append",
        metavar="NAME",
        help="restrict scanning to this skill; repeatable. Resolution still sees every skill.",
    )
    p.add_argument(
        "--strict-owner",
        action="store_true",
        help="promote R5-CONTEXTUAL from pass to finding. Default off.",
    )
    p.add_argument("--baseline", metavar="PATH", help="suppress findings listed in this file.")
    p.add_argument(
        "--write-baseline",
        metavar="PATH",
        help="write the current findings as a baseline and exit 0.",
    )
    p.add_argument("--format", choices=("text", "json"), default="text")
    p.add_argument(
        "--census",
        action="store_true",
        help="print the classification histogram, full and references/-scoped.",
    )
    p.add_argument(
        "--show-info", action="store_true", help="list every informational item, not a summary."
    )
    p.add_argument(
        "--include-fixtures",
        action="store_true",
        help="scan directories named fixtures. An undecodable file then produces exit 2.",
    )
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
    """Strip surrounding whitespace, including a carriage return, from a path or name argument.

    A shell or Python driver that writes CRLF leaves a carriage return on the last field of every
    line it parses. Without this, `--root C:\\repo\\r` fails with a message showing a path that
    renders identically to the correct one, and the operator has nothing to look at.
    """
    return None if value is None else value.strip().strip("\r\n")


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    args.root = clean_arg(args.root)
    args.baseline = clean_arg(args.baseline)
    args.write_baseline = clean_arg(args.write_baseline)
    args.fixtures = clean_arg(args.fixtures)
    if args.skill:
        args.skill = [clean_arg(s) for s in args.skill]

    if args.self_test:
        fixtures = (
            Path(args.fixtures).expanduser()
            if args.fixtures
            # Sibling of this file, not an ancestor of it. Path(__file__).parents[N] is
            # forbidden here because it encodes a guess about the repository layout above the
            # script; "the fixtures next to me" encodes nothing.
            else Path(__file__).resolve().with_name("fixtures")
        )
        try:
            return self_test(fixtures)
        except CannotRun as exc:
            print(f"BLOCKED: {exc}")
            return EXIT_CANNOT_RUN

    try:
        root = find_root(args.root)
        findings, info, census, refs_census, counts = scan(
            root, args.skill, args.strict_owner, args.include_fixtures
        )
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

    if args.census:
        print_census(census, refs_census)
        print()

    report(findings, info, stale, stale_owners, counts, args.format, args.show_info)
    return EXIT_FINDINGS if (findings or stale) else EXIT_CLEAN


if __name__ == "__main__":
    raise SystemExit(main())
