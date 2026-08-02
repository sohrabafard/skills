#!/usr/bin/env python3
"""Validate repo-local Markdown links, heading anchors, localized pairs, and opt-in line budgets.

Scope, stated so nobody builds a gate on more than this proves. It checks Markdown-syntax links
only -- [text](target) and resolved reference-style links -- with their heading anchors. Each
--localized-pair BASE COMPANION checks that one explicitly scoped pair for orphan and structural
drift, regardless of its language suffix or directory layout. It never infers another companion.
With --line-budget it also classifies explicitly selected Markdown files by physical line count
and fails on red files unless each was explicitly allowed. It does NOT see inline-code path
citations such as `references/10-x.md` or
`alaa-foo references/10-x.md`, which carry most cross-skill references in this pack; those resolve
against a skill root rather than the citing file's directory and belong to
skills/scripts/check_fleet_references.py. Do not widen this script to cover them.

Exit codes: 0 clean, 1 findings, 2 could not run (nothing was proven).
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Optional, Sequence, Set, Tuple

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)(?:\s+#+\s*)?$")
INLINE_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
REF_DEF_RE = re.compile(r"^\s{0,3}\[([^\]]+)\]:\s*(\S+)")
REF_LINK_RE = re.compile(r"!?\[([^\]]+)\]\[([^\]]*)\]")
# A Windows drive letter is one character before the colon; a URI scheme is two or more. Keeping
# SCHEME_RE at 2+ is what stops "D:/repo/x.md" from being waved through as an external URI.
WINDOWS_ABS_RE = re.compile(r"^[A-Za-z]:[\\/]")
SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]+:")
CODE_SPAN_RE = re.compile(r"``[^`]*``|`[^`]*`")
FENCE_RE = re.compile(r"^(```+|~~~+)")

DEFAULT_EXCLUDES = ("vendor", "_to_delete", "node_modules", "fixtures")

LINE_STATE_GREEN = "GREEN"
LINE_STATE_YELLOW = "YELLOW"
LINE_STATE_ORANGE = "ORANGE"
LINE_STATE_RED = "RED"


class Blocked(Exception):
    """The check could not run against a file. Callers must exit 2, never 1."""


@dataclass
class Issue:
    file: Path
    line_no: int
    code: str
    message: str

    def render(self, root: Path) -> str:
        where = f"{self.file.relative_to(root).as_posix()}:{self.line_no}"
        return f"{where}: {self.code} {self.message}"


def slugify_heading(text: str) -> str:
    """Anchor slug. Unicode letters survive, so a Persian heading resolves instead of slugging empty."""
    text = re.sub(r"[`*_~]", "", text.strip().lower())
    kept = [ch for ch in text if ch.isalnum() or ch in "-_" or ch.isspace()]
    slug = re.sub(r"\s+", "-", "".join(kept))
    return re.sub(r"-+", "-", slug).strip("-")


def split_link_target(raw: str) -> str:
    target = raw.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1].strip()
    for quote in (' "', " '"):
        idx = target.find(quote)
        if idx != -1:
            return target[:idx].strip()
    return target


def read_lines(path: Path) -> List[str]:
    try:
        return path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, PermissionError, OSError) as exc:
        raise Blocked(f"cannot read {path}: {exc.__class__.__name__}: {exc}") from exc


def line_budget_state(line_count: int) -> str:
    if line_count < 50:
        return LINE_STATE_GREEN
    if line_count <= 100:
        return LINE_STATE_YELLOW
    if line_count <= 200:
        return LINE_STATE_ORANGE
    return LINE_STATE_RED


def check_line_budgets(root: Path, paths: Sequence[Path], allowed_red: Sequence[str]
                       ) -> Tuple[List[Issue], List[Tuple[Path, int, str]]]:
    allowed = {resolve_repo_path(root, path_arg) for path_arg in allowed_red}
    selected = set(paths)
    outside_scope = sorted(path for path in allowed if path not in selected)
    if outside_scope:
        raise Blocked("--allow-red path is not selected by --files: " +
                      ", ".join(str(path.relative_to(root)) for path in outside_scope))
    issues: List[Issue] = []
    statuses: List[Tuple[Path, int, str]] = []
    for path in paths:
        line_count = len(read_lines(path))
        state = line_budget_state(line_count)
        statuses.append((path, line_count, state))
        if state == LINE_STATE_RED and path not in allowed:
            issues.append(Issue(path, 1, "DOC-LINES-RED",
                                f"{line_count} physical lines; explicit human approval required"))
    return issues, statuses


def iter_markdown_files(root: Path, excludes: Sequence[str]) -> Iterator[Path]:
    for path in sorted(root.rglob("*.md")):
        parts = path.relative_to(root).parts
        if any(p.startswith(".") or p in excludes for p in parts):
            continue
        if path.is_file():
            yield path


def iter_body(lines: Iterable[str]) -> Iterator[Tuple[int, str]]:
    """Yield (line number, line with fenced blocks and inline code removed)."""
    fence: Optional[str] = None
    for idx, line in enumerate(lines, start=1):
        marker = FENCE_RE.match(line.strip())
        if fence is None:
            if marker:
                fence = marker.group(1)[:3]
                continue
        else:
            if marker and marker.group(1).startswith(fence):
                fence = None
            continue
        yield idx, CODE_SPAN_RE.sub(" ", line)


def collect_headings(path: Path) -> Set[str]:
    slugs: Set[str] = set()
    counts: Dict[str, int] = {}
    for _, line in iter_body(read_lines(path)):
        match = HEADING_RE.match(line)
        if not match:
            continue
        slug = slugify_heading(match.group(2))
        if not slug:
            continue
        count = counts.get(slug, 0)
        counts[slug] = count + 1
        slugs.add(slug if count == 0 else f"{slug}-{count}")
    return slugs


def extract_targets(path: Path) -> List[Tuple[int, str]]:
    lines = read_lines(path)
    ref_defs: Dict[str, str] = {}
    for _, line in iter_body(lines):
        match = REF_DEF_RE.match(line)
        if match:
            ref_defs[match.group(1).strip().lower()] = split_link_target(match.group(2))
    targets: List[Tuple[int, str]] = []
    for idx, line in iter_body(lines):
        for match in INLINE_LINK_RE.finditer(line):
            targets.append((idx, split_link_target(match.group(1))))
        for match in REF_LINK_RE.finditer(line):
            label = (match.group(2) or match.group(1)).strip().lower()
            if label in ref_defs:
                targets.append((idx, ref_defs[label]))
    return targets


def is_external(target: str) -> bool:
    if target.startswith("#"):
        return False
    if target.startswith("//"):
        return True
    return bool(SCHEME_RE.match(target))


def validate_target(root: Path, file_path: Path, line_no: int, target: str,
                    cache: Dict[Path, Set[str]]) -> List[Issue]:
    if not target:
        return []
    if target.startswith("file://"):
        return [Issue(file_path, line_no, "LINK-FILE-SCHEME", f"file:// link: {target}")]
    # Checked before is_external on purpose: "D:" would otherwise read as a URI scheme.
    if WINDOWS_ABS_RE.match(target) or target.startswith("/"):
        return [Issue(file_path, line_no, "LINK-ABSOLUTE", f"absolute local path: {target}")]
    if "\\" in target:
        return [Issue(file_path, line_no, "LINK-BACKSLASH", f"use forward slashes: {target}")]
    if is_external(target):
        return []

    path_part, _, anchor = target.partition("#")
    resolved = file_path.resolve() if not path_part else (file_path.parent / path_part).resolve()
    try:
        resolved.relative_to(root)
    except ValueError:
        return [Issue(file_path, line_no, "LINK-OUTSIDE-ROOT", f"resolves outside root: {target}")]
    if path_part and not resolved.exists():
        return [Issue(file_path, line_no, "LINK-MISSING", f"target does not exist: {target}")]
    if anchor:
        if resolved.suffix.lower() != ".md":
            return [Issue(file_path, line_no, "LINK-ANCHOR-NON-MD",
                          f"anchors are validated for Markdown only: {target}")]
        slugs = cache.setdefault(resolved, collect_headings(resolved))
        if anchor not in slugs:
            return [Issue(file_path, line_no, "LINK-ANCHOR", f"heading anchor not found: {target}")]
    return []


def resolve_repo_path(root: Path, path_arg: str) -> Path:
    """Resolve a CLI path and reject reads outside the declared repository root."""
    path = (root / path_arg).resolve()
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise Blocked(f"path resolves outside repository root: {path_arg}") from exc
    return path


def structure_signature(path: Path) -> Tuple[List[int], List[str]]:
    """Heading levels in order, and fenced-block bodies in order. Language-independent."""
    levels: List[int] = []
    fences: List[str] = []
    fence: Optional[str] = None
    buf: List[str] = []
    for line in read_lines(path):
        marker = FENCE_RE.match(line.strip())
        if fence is None:
            if marker:
                fence, buf = marker.group(1)[:3], []
                continue
            match = HEADING_RE.match(line)
            if match:
                levels.append(len(match.group(1)))
        else:
            if marker and marker.group(1).startswith(fence):
                fence = None
                fences.append("\n".join(buf))
            else:
                buf.append(line)
    return levels, fences


def check_pairs(root: Path, pairs: Sequence[Tuple[str, str]]) -> List[Issue]:
    issues: List[Issue] = []
    for base_arg, companion_arg in pairs:
        base = resolve_repo_path(root, base_arg)
        companion = resolve_repo_path(root, companion_arg)
        if not companion.exists():
            raise Blocked(f"localized companion does not exist: {companion_arg}")
        if base == companion:
            raise Blocked(f"localized pair paths must differ: {base_arg}")
        if not base.exists():
            issues.append(Issue(companion, 1, "PAIR-ORPHAN",
                                "localized companion has no explicitly named base document at "
                                f"{base.relative_to(root).as_posix()}"))
            continue
        if structure_signature(base) != structure_signature(companion):
            issues.append(Issue(companion, 1, "PAIR-DRIFT",
                                "heading sequence or fenced blocks differ from "
                                f"{base.relative_to(root).as_posix()}; the base structure wins"))
    return issues


def run_checks(root: Path, files: Optional[Sequence[str]],
               excludes: Sequence[str],
               localized_pairs: Sequence[Tuple[str, str]] = ()
               ) -> Tuple[List[Issue], List[Path]]:
    if files:
        selected = [resolve_repo_path(root, rel) for rel in files]
        missing = [p for p in selected if not p.exists()]
        if missing:
            raise Blocked("missing file(s): " + ", ".join(str(p) for p in missing))
    else:
        selected = list(iter_markdown_files(root, excludes))
    selected = [p for p in selected if p.suffix.lower() == ".md"]
    cache: Dict[Path, Set[str]] = {}
    issues: List[Issue] = []
    for path in selected:
        for line_no, target in extract_targets(path):
            issues.extend(validate_target(root, path, line_no, target, cache))
    issues.extend(check_pairs(root, localized_pairs))
    return issues, selected


SELF_TEST_CASES = (
    ("clean", 0, "code spans, ~~~ fence, Persian anchor, valid explicit pair",
     (("note.md", "note.fa.md"),)),
    ("windows-abs", 1, "D:/ and C:\\ links, this skill's own counter-examples", ()),
    ("broken-link", 1, "relative link to a missing file", ()),
    ("pair-orphan", 1, "explicit companion with no named base document",
     (("x.md", "x.fa.md"),)),
    ("pair-drift", 1, "explicit pair with differing heading sequence",
     (("guide.md", "guide.fa.md"),)),
    ("pair-generic", 1, "non-Persian explicit pair with differing heading sequence",
     (("guide.md", "guide.fr.md"),)),
    ("pair-missing", 0, "an unrelated localized pair does not require another companion", ()),
    ("undecodable", 2, "a .md file that is not valid UTF-8", ()),
)

LINE_BUDGET_SELF_TESTS = (
    (49, LINE_STATE_GREEN),
    (50, LINE_STATE_YELLOW),
    (100, LINE_STATE_YELLOW),
    (101, LINE_STATE_ORANGE),
    (200, LINE_STATE_ORANGE),
    (201, LINE_STATE_RED),
)


def self_test(fixtures: Path) -> int:
    if not fixtures.is_dir():
        print(f"self-test fixtures not found: {fixtures}", file=sys.stderr)
        return 2
    blocked = failed = 0
    for name, expected, what, localized_pairs in SELF_TEST_CASES:
        root = (fixtures / name).resolve()
        if not root.is_dir():
            print(f"BLOCKED {name}: fixture directory missing")
            blocked += 1
            continue
        try:
            issues, _ = run_checks(root, None, (), localized_pairs=localized_pairs)
            observed = 1 if issues else 0
        except Blocked:
            observed = 2
        if observed == expected:
            verdict = "PASS"
        elif observed == 2:
            verdict, blocked = "BLOCKED", blocked + 1
        else:
            verdict, failed = "FAIL", failed + 1
        print(f"{verdict} {name}: expected {expected}, observed {observed} -- {what}")
    outside_root = (fixtures / "pair-missing").resolve()
    try:
        run_checks(outside_root, ("../clean/note.md",), ())
        observed = 0
    except Blocked:
        observed = 2
    if observed == 2:
        verdict = "PASS"
    else:
        verdict, failed = "FAIL", failed + 1
    print(f"{verdict} files-outside-root: expected 2, observed {observed} -- "
          "explicit files cannot escape the repository root")
    unscoped_pair_root = (fixtures / "pair-drift").resolve()
    try:
        issues, _ = run_checks(unscoped_pair_root, None, ())
        observed = 1 if issues else 0
    except Blocked:
        observed = 2
    if observed == 0:
        verdict = "PASS"
    elif observed == 2:
        verdict, blocked = "BLOCKED", blocked + 1
    else:
        verdict, failed = "FAIL", failed + 1
    print(f"{verdict} unscoped-pair: expected 0, observed {observed} -- "
          "an unrelated drifting pair is not checked")
    for line_count, expected in LINE_BUDGET_SELF_TESTS:
        observed_state = line_budget_state(line_count)
        if observed_state == expected:
            verdict = "PASS"
        else:
            verdict, failed = "FAIL", failed + 1
        print(f"{verdict} line-budget-{line_count}: expected {expected}, "
              f"observed {observed_state}")
    if blocked:
        print(f"\n{blocked} case(s) could not run.", file=sys.stderr)
        return 2
    if failed:
        print(f"\n{failed} case(s) failed.", file=sys.stderr)
        return 1
    print(f"\nAll {len(SELF_TEST_CASES) + 2 + len(LINE_BUDGET_SELF_TESTS)} "
          "self-test cases passed.")
    return 0


def main(argv: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Validate repo-local Markdown links and anchors, with explicitly scoped "
                    "localized-pair and line-budget checks. Inline-code path citations are out "
                    "of scope: see skills/scripts/check_fleet_references.py.")
    parser.add_argument("repo_root", nargs="?", help="Repository root that links resolve within")
    parser.add_argument("--files", nargs="*", default=None,
                        help="Specific Markdown files, relative to repo_root")
    parser.add_argument("--exclude", nargs="*", default=list(DEFAULT_EXCLUDES),
                        help=f"Directory names to skip (default: {' '.join(DEFAULT_EXCLUDES)})")
    parser.add_argument("--self-test", action="store_true",
                        help="Run the committed fixtures and report PASS/FAIL/BLOCKED")
    parser.add_argument("--localized-pair", nargs=2, action="append", default=[],
                        metavar=("BASE", "COMPANION"),
                        help="Check one explicitly scoped localized pair; repeat for more pairs")
    parser.add_argument("--line-budget", action="store_true",
                        help="Classify selected Markdown files by physical line count and fail red")
    parser.add_argument("--allow-red", nargs="*", default=[], metavar="PATH",
                        help="Human-approved red files; valid only with --line-budget and --files")
    parser.add_argument("--fixtures", default=None,
                        help="Fixture root for --self-test (default: ../assets/fixtures beside this script)")
    args = parser.parse_args(argv)

    if args.self_test:
        fixtures = Path(args.fixtures) if args.fixtures else Path(sys.argv[0]).resolve().parent.parent / "assets" / "fixtures"
        return self_test(fixtures)

    if args.allow_red and (not args.line_budget or not args.files):
        parser.print_usage(sys.stderr)
        print("--allow-red requires --line-budget and explicit --files", file=sys.stderr)
        return 2

    if not args.repo_root:
        parser.print_usage(sys.stderr)
        print("repo_root is required unless --self-test is given", file=sys.stderr)
        return 2
    root = Path(args.repo_root).resolve()
    if not root.is_dir():
        print(f"Repository root not found or not a directory: {root}", file=sys.stderr)
        return 2

    try:
        issues, checked = run_checks(
            root,
            args.files,
            tuple(args.exclude),
            localized_pairs=tuple((base, companion)
                                  for base, companion in args.localized_pair),
        )
        line_statuses: List[Tuple[Path, int, str]] = []
        if args.line_budget:
            line_issues, line_statuses = check_line_budgets(root, checked, args.allow_red)
            issues.extend(line_issues)
    except Blocked as exc:
        print(f"Could not run: {exc}", file=sys.stderr)
        return 2

    for path, line_count, state in line_statuses:
        print(f"{path.relative_to(root).as_posix()}: {state} {line_count} physical lines")
    if issues:
        for issue in issues:
            print(issue.render(root))
        print(f"\nFound {len(issues)} issue(s) in {len(checked)} file(s).", file=sys.stderr)
        return 1
    scopes = ["links"]
    if args.localized_pair:
        scopes.append("localized pairs")
    if args.line_budget:
        scopes.append("line budgets")
    scope = ", ".join(scopes)
    print(f"Validated {scope} in {len(checked)} Markdown file(s) under {root}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
