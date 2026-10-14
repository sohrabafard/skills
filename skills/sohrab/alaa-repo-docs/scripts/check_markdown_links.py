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
scripts/check_fleet_references.py. Do not widen this script to cover them.

Mirror awareness is opt-in and never discovered. --mirror LOCAL ORIGIN (repeatable) or
--mirror-config PATH (JSON {"mirrors": [{"local": ..., "origin": ..., "origin_root": ...}]}, paths
resolved from the config file's directory, origin_root optional) declares LOCAL, a directory inside
repo_root, a copy of ORIGIN, a directory that may lie outside it. Inside a mirror, a link that
leaves LOCAL is checked in ORIGIN instead of here, and a link that breaks inside LOCAL is
re-checked in ORIGIN to separate local drift from an upstream error. Origin lookups may not leave
the origin repository root (origin_root, else the nearest ancestor of ORIGIN holding a .git entry;
none found blocks the run). A file with no counterpart, or a link absent from that counterpart,
gets ordinary local checks. An ORIGIN that does not exist is reported per link and exits 2.

Exit codes: 0 clean, 1 findings, 2 could not run (nothing was proven), or a declared origin was
unavailable for at least one link. 2 outranks 1: findings printed in a 2 run are real, and the
run proves nothing for the unproven links.
"""

from __future__ import annotations

import argparse
import contextlib
import io
import json
import os
import re
import shutil
import sys
import tempfile
from collections import Counter
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

CODE_MIRROR_OK = "MIRROR-ORIGIN-OK"
CODE_MIRROR_UPSTREAM = "MIRROR-UPSTREAM"
CODE_MIRROR_DRIFT = "MIRROR-DRIFT"
CODE_MIRROR_UNAVAILABLE = "MIRROR-ORIGIN-UNAVAILABLE"
CODE_MIRROR_OUTSIDE = "MIRROR-OUTSIDE-ORIGIN"

FAILURE_LABELS = {
    "LINK-MISSING": "missing file",
    "LINK-ANCHOR": "anchor not found",
    "LINK-ANCHOR-NON-MD": "non-md anchor",
}

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


@dataclass(frozen=True)
class Mirror:
    """LOCAL (resolved, inside the repository root) is a copy of ORIGIN (resolved, may be anywhere)."""
    local: Path
    origin: Path
    # The origin repository root: links resolved in origin may not leave it. None only while
    # origin is missing, where nothing is resolved in origin.
    origin_root: Optional[Path] = None


@dataclass(frozen=True)
class Tally:
    local: int
    upstream: int
    healthy: int
    unavailable: int

    @property
    def counted(self) -> int:
        return self.local + self.upstream

    @property
    def exit_code(self) -> int:
        if self.unavailable:
            return 2
        return 1 if self.counted else 0

    def describe(self) -> str:
        return (f"local findings: {self.local}, upstream errors: {self.upstream}, "
                f"healthy in origin: {self.healthy}, origin unavailable: {self.unavailable}")


def tally_issues(issues: Sequence[Issue]) -> Tally:
    """Classify result lines. Every code except the three mirror outcomes is an ordinary local finding."""
    codes = [issue.code for issue in issues]
    healthy = codes.count(CODE_MIRROR_OK)
    upstream = codes.count(CODE_MIRROR_UPSTREAM)
    unavailable = codes.count(CODE_MIRROR_UNAVAILABLE)
    return Tally(len(codes) - healthy - upstream - unavailable, upstream, healthy, unavailable)


def slugify_heading(text: str) -> str:
    """Anchor slug. Unicode letters survive, so a Persian heading resolves instead of slugging empty."""
    text = text.strip().lower()
    # Code-span text survives (backticks go; the punctuation filter below still applies, keeping
    # `-` and `_`). Outside a span, emphasis markers `*_~` are stripped as before.
    pieces: List[str] = []
    cursor = 0
    for span in CODE_SPAN_RE.finditer(text):
        pieces.append(re.sub(r"[`*_~]", "", text[cursor:span.start()]))
        pieces.append(span.group(0).replace("`", ""))
        cursor = span.end()
    pieces.append(re.sub(r"[`*_~]", "", text[cursor:]))
    text = "".join(pieces)
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


def iter_body(lines: Iterable[str], keep_code_spans: bool = False) -> Iterator[Tuple[int, str]]:
    """Yield (line number, line with fenced blocks removed and, by default, inline code removed).

    Link extraction keeps the default so a link inside a code span stays invisible. Heading
    collection passes keep_code_spans=True: GitHub slugs the text of a code span, and
    slugify_heading already drops the backticks themselves."""
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
        yield idx, line if keep_code_spans else CODE_SPAN_RE.sub(" ", line)


def collect_headings(path: Path) -> Set[str]:
    slugs: Set[str] = set()
    counts: Dict[str, int] = {}
    for _, line in iter_body(read_lines(path), keep_code_spans=True):
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


LOCAL_MESSAGES = {
    "LINK-MISSING": "target does not exist: {target}",
    "LINK-ANCHOR-NON-MD": "anchors are validated for Markdown only: {target}",
    "LINK-ANCHOR": "heading anchor not found: {target}",
}


def is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def posix_rel(root: Path, path: Path) -> str:
    """Path relative to the repository root as POSIX, so no machine path is ever printed."""
    try:
        return Path(os.path.relpath(path, root)).as_posix()
    except ValueError:
        return f"<other-drive>/{path.name}"


def resolve_from(base_file: Path, path_part: str) -> Path:
    return base_file.resolve() if not path_part else (base_file.parent / path_part).resolve()


def probe_resolved(resolved: Path, anchor: str, cache: Dict[Path, Set[str]]) -> Optional[str]:
    """The one existence-and-anchor check, used for local and origin targets alike.

    Returns the failing issue code, or None when the target is healthy. The heading cache is keyed
    by the resolved path, so a local file and its origin counterpart are cached separately."""
    if not resolved.exists():
        return "LINK-MISSING"
    if anchor:
        if resolved.suffix.lower() != ".md":
            return "LINK-ANCHOR-NON-MD"
        slugs = cache.get(resolved)
        if slugs is None:
            slugs = cache[resolved] = collect_headings(resolved)
        if anchor not in slugs:
            return "LINK-ANCHOR"
    return None


def find_mirror(mirrors: Sequence[Mirror], file_path: Path) -> Optional[Mirror]:
    """The mirror a file belongs to. A file whose origin counterpart is absent while the origin
    directory exists is local-only: it is not mirrored and gets the ordinary checks."""
    resolved = file_path.resolve()
    for mirror in mirrors:
        if is_within(resolved, mirror.local):
            counterpart = mirror.origin / resolved.relative_to(mirror.local)
            if mirror.origin.is_dir() and not counterpart.is_file():
                return None
            return mirror
    return None


def validate_mirrored(root: Path, file_path: Path, line_no: int, target: str, path_part: str,
                      anchor: str, resolved: Path, mirror: Mirror,
                      cache: Dict[Path, Set[str]],
                      origin_targets: Dict[Path, Set[str]]) -> List[Issue]:
    """Links in a mirrored file: outside LOCAL they are judged in ORIGIN; inside LOCAL, a local
    failure is re-checked in ORIGIN to tell drift from an upstream error."""
    local_failure: Optional[str] = None
    if is_within(resolved, mirror.local):
        local_failure = probe_resolved(resolved, anchor, cache)
        if local_failure is None:
            return []
    local_label = FAILURE_LABELS[local_failure] if local_failure else "not checked locally"
    if not mirror.origin.is_dir():
        return [Issue(file_path, line_no, CODE_MIRROR_UNAVAILABLE,
                      f"origin unavailable, link not proven ({local_label}): {target} "
                      f"(origin directory {posix_rel(root, mirror.origin)} not found)")]
    origin_file = mirror.origin / file_path.resolve().relative_to(mirror.local)
    if mirror.origin_root is not None and not is_within(origin_file.resolve(), mirror.origin_root):
        return [Issue(file_path, line_no, CODE_MIRROR_OUTSIDE,
                      f"source file escapes the origin repository: {posix_rel(root, origin_file)}")]
    targets = origin_targets.get(origin_file)
    if targets is None:
        targets = origin_targets[origin_file] = {link for _, link in extract_targets(origin_file)}
    if target not in targets:
        # A local edit has no upstream provenance; use the same ordinary checks as an undeclared file.
        return validate_target(root, file_path, line_no, target, cache)
    origin_resolved = resolve_from(origin_file, path_part)
    origin_rel = posix_rel(root, origin_resolved)
    if mirror.origin_root is not None and not is_within(origin_resolved, mirror.origin_root):
        return [Issue(file_path, line_no, CODE_MIRROR_OUTSIDE,
                      f"link escapes the origin repository: {target} (origin {origin_rel})")]
    origin_failure = probe_resolved(origin_resolved, anchor, cache)
    if origin_failure is None:
        if local_failure is None:
            return [Issue(file_path, line_no, CODE_MIRROR_OK,
                          f"healthy in origin: {target} (origin {origin_rel}); not checked locally")]
        return [Issue(file_path, line_no, CODE_MIRROR_DRIFT,
                      f"local copy diverged from origin ({local_label}): {target} "
                      f"(healthy in origin {origin_rel})")]
    origin_label = FAILURE_LABELS[origin_failure]
    broken = (f"{local_label} locally and {origin_label} in origin" if local_failure
              else f"{origin_label} in origin")
    return [Issue(file_path, line_no, CODE_MIRROR_UPSTREAM,
                  f"upstream error ({broken}): {target} (origin {origin_rel})")]


def validate_target(root: Path, file_path: Path, line_no: int, target: str,
                    cache: Dict[Path, Set[str]],
                    mirrors: Sequence[Mirror] = (),
                    origin_targets: Optional[Dict[Path, Set[str]]] = None) -> List[Issue]:
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
    resolved = resolve_from(file_path, path_part)
    mirror = find_mirror(mirrors, file_path)
    if mirror is not None:
        return validate_mirrored(root, file_path, line_no, target, path_part, anchor, resolved,
                                 mirror, cache, {} if origin_targets is None else origin_targets)
    if not is_within(resolved, root):
        return [Issue(file_path, line_no, "LINK-OUTSIDE-ROOT", f"resolves outside root: {target}")]
    failure = probe_resolved(resolved, anchor, cache)
    if failure:
        return [Issue(file_path, line_no, failure, LOCAL_MESSAGES[failure].format(target=target))]
    return []


def resolve_repo_path(root: Path, path_arg: str) -> Path:
    """Resolve a CLI path and reject reads outside the declared repository root."""
    path = (root / path_arg).resolve()
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise Blocked(f"path resolves outside repository root: {path_arg}") from exc
    return path


def relative_arg(field: str, value: object) -> str:
    """A declaration path must be a non-empty relative POSIX path."""
    if not isinstance(value, str) or not value.strip():
        raise Blocked(f"mirror {field} must be a non-empty string")
    if WINDOWS_ABS_RE.match(value) or value.startswith("/"):
        raise Blocked(f"mirror {field} must be a relative path: {value}")
    if "\\" in value:
        raise Blocked(f"mirror {field} must use forward slashes: {value}")
    return value


def discover_origin_root(origin: Path) -> Optional[Path]:
    """The nearest ancestor of origin (inclusive) holding a .git entry, or None."""
    for candidate in (origin, *origin.parents):
        if (candidate / ".git").exists():
            return candidate
    return None


def resolve_mirror(root: Path, base: Path, local_arg: object, origin_arg: object,
                   origin_root_arg: object = None) -> Mirror:
    """The single place a mirror declaration is validated and resolved.

    LOCAL and ORIGIN are relative POSIX paths resolved from base (the repository root for --mirror,
    the config file's directory for --mirror-config). LOCAL must be an existing directory inside
    root. ORIGIN may lie outside root and may be missing: that is reported per link, not here.
    When ORIGIN exists, links resolved in it are bounded by origin_root: the explicit
    origin_root_arg, else the nearest ancestor of ORIGIN holding a .git entry."""
    local_value = relative_arg("local", local_arg)
    origin_value = relative_arg("origin", origin_arg)
    local = (base / local_value).resolve()
    origin = (base / origin_value).resolve()
    if not is_within(local, root):
        if is_within(Path(os.path.abspath(base / local_value)), root):
            raise Blocked("mirror local path is a symlink or junction that resolves outside "
                          f"repository root: {local_arg}")
        raise Blocked(f"mirror local path resolves outside repository root: {local_arg}")
    if not local.is_dir():
        raise Blocked(f"mirror local path is not an existing directory: {local_arg}")
    origin_root: Optional[Path] = None
    if origin_root_arg is not None:
        origin_root = (base / relative_arg("origin_root", origin_root_arg)).resolve()
        if not is_within(origin, origin_root):
            raise Blocked("mirror origin_root must be an ancestor of or equal to origin: "
                          f"{origin_root_arg}")
    elif origin.is_dir():
        origin_root = discover_origin_root(origin)
        if origin_root is None:
            raise Blocked("cannot determine the origin repository root (no .git above "
                          f"{posix_rel(root, origin)}); set origin_root in a --mirror-config entry")
    return Mirror(local, origin, origin_root)


def parse_mirror_config(root: Path, base: Path, text: str) -> List[Mirror]:
    """Parse {"mirrors": [{"local": ..., "origin": ...}]}; any other shape blocks the run."""
    try:
        data = json.loads(text)
    except ValueError as exc:
        raise Blocked(f"mirror config is not valid JSON: {exc}") from exc
    if not isinstance(data, dict) or set(data) != {"mirrors"}:
        raise Blocked('mirror config must be an object with exactly one key, "mirrors"')
    entries = data["mirrors"]
    if not isinstance(entries, list) or not entries:
        raise Blocked('mirror config "mirrors" must be a non-empty array')
    mirrors: List[Mirror] = []
    for index, entry in enumerate(entries):
        if (not isinstance(entry, dict) or not {"local", "origin"} <= set(entry)
                or set(entry) - {"local", "origin", "origin_root"}):
            raise Blocked(f'mirror config entry {index} must have the keys "local" and "origin" '
                          'and may add "origin_root"')
        mirrors.append(resolve_mirror(root, base, entry["local"], entry["origin"],
                                      entry.get("origin_root")))
    return mirrors


def reject_overlapping(root: Path, mirrors: Sequence[Mirror]) -> None:
    for index, first in enumerate(mirrors):
        for second in mirrors[index + 1:]:
            if first.local == second.local:
                raise Blocked(f"duplicate mirror local directory: {posix_rel(root, first.local)}")
            if is_within(first.local, second.local) or is_within(second.local, first.local):
                raise Blocked("overlapping mirror local directories: "
                              f"{posix_rel(root, first.local)} and {posix_rel(root, second.local)}")


def load_mirrors(root: Path, pairs: Sequence[Tuple[str, str]],
                 config_arg: Optional[str]) -> List[Mirror]:
    """Both declaration forms feed one list; nothing is ever discovered."""
    mirrors = [resolve_mirror(root, root, local, origin) for local, origin in pairs]
    if config_arg:
        config = resolve_repo_path(root, config_arg)
        if not config.is_file():
            raise Blocked(f"mirror config is not a file: {config_arg}")
        try:
            text = config.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError) as exc:
            raise Blocked(f"cannot read mirror config {config_arg}: {exc.__class__.__name__}") from exc
        mirrors.extend(parse_mirror_config(root, config.parent, text))
    reject_overlapping(root, mirrors)
    for mirror in mirrors:
        if not mirror.origin.is_dir():
            print("warning: mirror origin is not an existing directory: "
                  f"{posix_rel(root, mirror.origin)}", file=sys.stderr)
    return mirrors


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
               localized_pairs: Sequence[Tuple[str, str]] = (),
               mirrors: Sequence[Mirror] = ()
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
    origin_targets: Dict[Path, Set[str]] = {}
    issues: List[Issue] = []
    for path in selected:
        for line_no, target in extract_targets(path):
            issues.extend(validate_target(root, path, line_no, target, cache, mirrors, origin_targets))
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

@dataclass(frozen=True)
class ExactCase:
    """A self-test case that asserts the exit class AND the exact multiset of result codes."""
    name: str
    fixture: str
    expected_exit: int
    expected_codes: Dict[str, int]
    what: str
    mirror_pairs: Tuple[Tuple[str, str], ...] = ()
    mirror_config: Optional[str] = None
    blocked_fragment: str = ""


_SVC = "pkg/docs/contracts/svc"
_SVC_ORIGIN = "../origin/svc-repo/docs/contracts/svc"

EXACT_CASES = (
    ExactCase("inline-code-anchor", "inline-code-anchor", 0, {},
              "code-span heading text is slugged verbatim (my_func keeps its underscore), "
              "duplicates get -1, and a link inside a code span stays invisible"),
    ExactCase("mirror-origin-ok", "mirror/ok/consumer", 0, {CODE_MIRROR_OK: 2},
              "links leaving the mirror resolve in origin and are informational; a link that "
              "passes locally but would fail in origin, and a link to the mirror root, are silent",
              mirror_config="mirror.json"),
    ExactCase("mirror-config-valid", "mirror/ok/consumer", 0, {CODE_MIRROR_OK: 2},
              "config paths resolve from the config file's directory, not the repository root",
              mirror_config="conf/mirror.json"),
    ExactCase("mirror-undeclared", "mirror/ok/consumer", 1, {"LINK-MISSING": 2},
              "regression: the same consumer tree without a declaration reports the plain "
              "missing-file findings"),
    ExactCase("mirror-upstream", "mirror/upstream/consumer", 1,
              {CODE_MIRROR_UPSTREAM: 2, "LINK-MISSING": 1},
              "an origin-broken outside link and an inside link broken in both trees are upstream "
              "errors; a broken link in a file outside the mirror stays an ordinary finding",
              mirror_config="mirror.json"),
    ExactCase("mirror-drift", "mirror/drift/consumer", 1, {CODE_MIRROR_DRIFT: 1},
              "an inside link broken locally but healthy in origin is local drift",
              mirror_config="mirror.json"),
    ExactCase("mirror-escape", "mirror/escape/consumer", 1,
              {CODE_MIRROR_OK: 1, CODE_MIRROR_OUTSIDE: 1},
              "an origin lookup that leaves the origin repository is refused even though the "
              "file exists there; a lookup inside the boundary stays healthy",
              mirror_config="mirror.json"),
    ExactCase("mirror-local-only", "mirror/local-only/consumer", 1,
              {"LINK-MISSING": 2, "LINK-OUTSIDE-ROOT": 1},
              "a file with no origin counterpart is not mirrored: ordinary codes, including "
              "LINK-OUTSIDE-ROOT",
              mirror_config="mirror.json"),
    ExactCase("mirror-locally-added-links", "mirror/local-edit/consumer", 1,
              {"LINK-MISSING": 3, "LINK-ANCHOR": 1, "LINK-OUTSIDE-ROOT": 1,
               CODE_MIRROR_OK: 1},
              "filesystem integration: links absent from the origin document remain local, "
              "even when their targets exist in origin; shared links survive reformatting",
              mirror_config="mirror.json"),
    ExactCase("mirror-origin-unavailable", "mirror/unavailable/consumer", 2,
              {CODE_MIRROR_UNAVAILABLE: 2},
              "a declared origin that is absent proves nothing and never exits 0 or 1",
              mirror_pairs=((_SVC, _SVC_ORIGIN),)),
    ExactCase("mirror-unavailable-mixed", "mirror/unavailable-mixed/consumer", 2,
              {CODE_MIRROR_UNAVAILABLE: 1, "LINK-MISSING": 1},
              "an ordinary counted finding next to an unavailable origin still exits 2",
              mirror_pairs=((_SVC, _SVC_ORIGIN),)),
    ExactCase("mirror-config-malformed-file", "mirror/ok/consumer", 2, {},
              "a malformed config file blocks the run because its JSON does not parse",
              mirror_config="conf/mirror-malformed.json", blocked_fragment="not valid JSON"),
)

# (name, pairs, config JSON text, expected message fragment, what). Each must raise Blocked.
MIRROR_REJECT_CASES = (
    ("reject-local-outside-root", (("../origin", "x"),), None, "outside repository root",
     "LOCAL must resolve inside the repository root"),
    ("reject-local-missing", (("pkg/nope", "x"),), None, "not an existing directory",
     "LOCAL must exist as a directory"),
    ("reject-absolute", (("/pkg", "x"),), None, "relative path", "absolute paths are refused"),
    ("reject-backslash", (("pkg" + chr(92) + "docs", "x"),), None, "forward slashes",
     "backslashes are refused"),
    ("reject-duplicate", ((_SVC, "a"), (_SVC, "b")), None, "duplicate mirror local",
     "the same LOCAL twice is refused"),
    ("reject-overlap", (("pkg/docs", "a"), (_SVC, "b")), None, "overlapping",
     "nested LOCAL directories are refused"),
    ("reject-config-json", (), "{", "not valid JSON", "unparseable JSON is refused"),
    ("reject-config-extra-key", (), '{"mirrors": [], "extra": 1}', "exactly one key",
     "an extra top-level key is refused"),
    ("reject-config-entry-extra", (),
     '{"mirrors": [{"local": "pkg", "origin": "x", "note": "y"}]}', 'may add "origin_root"',
     "an unknown entry field is refused"),
    ("reject-config-type", (), '{"mirrors": [{"local": 1, "origin": "x"}]}', "non-empty string",
     "a non-string field is refused"),
    ("reject-config-empty", (), '{"mirrors": []}', "non-empty array",
     "an empty declaration is refused"),
    ("reject-origin-root-not-ancestor", (),
     '{"mirrors": [{"local": "pkg", "origin": "x", "origin_root": "pkg"}]}', "ancestor",
     "origin_root must contain origin"),
)

# (name, argv builder key, expected return code, stderr fragment, what). See run_cli_cases.
CLI_CASES = (
    ("cli-mirror-discovers-git-root", "temp-git", 0, "",
     "--mirror alone works when a .git marks the origin repository root"),
    ("cli-mirror-no-boundary", "temp-no-git", 2, "origin_root",
     "--mirror against an existing origin with no .git above it blocks and names origin_root"),
    ("cli-mirror-config", "config-ok", 0, "",
     "--mirror-config returns the shared exit code for a healthy mirror"),
    ("cli-drift-exit", "config-drift", 1, "local findings: 1",
     "a counted mirror finding returns 1 and reports the split summary"),
    ("cli-unavailable-mixed-exit", "config-mixed", 2, "origin unavailable: 1",
     "an ordinary finding plus an unavailable origin returns 2, never 1"),
)

LINE_BUDGET_SELF_TESTS = (
    (49, LINE_STATE_GREEN),
    (50, LINE_STATE_YELLOW),
    (100, LINE_STATE_YELLOW),
    (101, LINE_STATE_ORANGE),
    (200, LINE_STATE_ORANGE),
    (201, LINE_STATE_RED),
)


def run_exact_cases(fixtures: Path) -> int:
    """Run ExactCase entries; return the failure count. A missing fixture is a failure."""
    failed = 0
    for case in EXACT_CASES:
        root = (fixtures / case.fixture).resolve()
        observed_exit, observed_codes, message = 2, {}, ""
        try:
            with contextlib.redirect_stderr(io.StringIO()):
                mirrors = load_mirrors(root, case.mirror_pairs, case.mirror_config)
            issues, _ = run_checks(root, None, (), mirrors=mirrors)
            observed_exit = tally_issues(issues).exit_code
            observed_codes = dict(Counter(issue.code for issue in issues))
        except Blocked as exc:
            message = str(exc)
        ok = (observed_exit == case.expected_exit and observed_codes == case.expected_codes
              and case.blocked_fragment in message)
        if not ok:
            failed += 1
        print(f"{'PASS' if ok else 'FAIL'} {case.name}: expected {case.expected_exit} "
              f"{case.expected_codes}, observed {observed_exit} {observed_codes}"
              f"{' ' + repr(message) if message else ''} -- {case.what}")
    return failed


def run_cli_cases(fixtures: Path) -> Tuple[int, int]:
    """Drive main() itself, so the return code is proven to come from the shared tally.

    Returns (failed, blocked). The no-boundary case needs a temp tree with no .git above it; a host
    whose temp directory sits under a git checkout cannot run it, which is BLOCKED, never a verdict.
    The discovers-git-root case is immune: the .git it plants is the nearest ancestor and wins."""
    failed = blocked = 0
    ok_pair = ["--mirror", _SVC, _SVC_ORIGIN]
    with tempfile.TemporaryDirectory() as tmp:
        copy = Path(tmp) / "ok"
        shutil.copytree(fixtures / "mirror" / "ok", copy)
        plans = {
            "temp-no-git": ([str(copy / "consumer")] + ok_pair, None),
            "temp-git": ([str(copy / "consumer")] + ok_pair, copy / "origin" / "svc-repo" / ".git"),
            "config-ok": ([str(fixtures / "mirror" / "ok" / "consumer"),
                           "--mirror-config", "mirror.json"], None),
            "config-drift": ([str(fixtures / "mirror" / "drift" / "consumer"),
                              "--mirror-config", "mirror.json"], None),
            "config-mixed": ([str(fixtures / "mirror" / "unavailable-mixed" / "consumer")]
                             + ok_pair, None),
        }
        for name, key, expected, fragment, what in CLI_CASES:
            argv, marker = plans[key]
            if key == "temp-no-git":
                stray = discover_origin_root(copy / "origin" / "svc-repo" / "docs" / "contracts" / "svc")
                if stray is not None:
                    blocked += 1
                    print(f"BLOCKED {name}: host condition, the temp directory has a .git ancestor "
                          f"({stray.name}); point TMP/TEMP/TMPDIR outside any git checkout -- {what}")
                    continue
            if marker is not None:
                marker.mkdir()
            out, err = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                observed = main(argv)
            if marker is not None:
                marker.rmdir()
            ok = observed == expected and fragment in err.getvalue()
            if not ok:
                failed += 1
            print(f"{'PASS' if ok else 'FAIL'} {name}: expected {expected}, observed {observed}"
                  f"{'' if ok else ' stderr=' + repr(err.getvalue()[-200:])} -- {what}")
    return failed, blocked


def run_reject_cases(fixtures: Path) -> int:
    failed = 0
    root = (fixtures / "mirror" / "ok" / "consumer").resolve()
    for name, pairs, config_text, fragment, what in MIRROR_REJECT_CASES:
        message = ""
        try:
            mirrors = [resolve_mirror(root, root, local, origin) for local, origin in pairs]
            if config_text is not None:
                mirrors.extend(parse_mirror_config(root, root, config_text))
            reject_overlapping(root, mirrors)
        except Blocked as exc:
            message = str(exc)
        ok = fragment in message
        if not ok:
            failed += 1
        print(f"{'PASS' if ok else 'FAIL'} {name}: expected Blocked containing "
              f"{fragment!r}, observed {message!r} -- {what}")
    return failed


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
    failed += run_exact_cases(fixtures)
    failed += run_reject_cases(fixtures)
    cli_failed, cli_blocked = run_cli_cases(fixtures)
    failed += cli_failed
    blocked += cli_blocked
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
    total = (len(SELF_TEST_CASES) + 2 + len(EXACT_CASES) + len(MIRROR_REJECT_CASES)
             + len(CLI_CASES) + len(LINE_BUDGET_SELF_TESTS))
    print(f"\nAll {total} self-test cases passed.")
    return 0


def main(argv: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Validate repo-local Markdown links and anchors, with explicitly scoped "
                    "localized-pair, mirror and line-budget checks. Inline-code path citations "
                    "are out of scope: see scripts/check_fleet_references.py.")
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
    parser.add_argument("--mirror", nargs=2, action="append", default=[],
                        metavar=("LOCAL", "ORIGIN"),
                        help="Declare LOCAL (a directory inside repo_root) a copy of ORIGIN "
                             "(relative to repo_root, may lie outside it). Links leaving LOCAL "
                             "are checked in ORIGIN, bounded by the nearest ancestor of "
                             "ORIGIN holding a .git entry; repeatable; never auto-discovered")
    parser.add_argument("--mirror-config", default=None, metavar="PATH",
                        help='JSON file (relative to repo_root) {"mirrors": [{"local": ..., '
                             '"origin": ..., "origin_root": ...}]}; paths resolve from the '
                             "config file's directory; origin_root (optional) bounds origin "
                             "lookups and overrides .git discovery. Combines with --mirror")
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
        mirrors = load_mirrors(root, tuple((local, origin) for local, origin in args.mirror),
                               args.mirror_config)
        issues, checked = run_checks(
            root,
            args.files,
            tuple(args.exclude),
            localized_pairs=tuple((base, companion)
                                  for base, companion in args.localized_pair),
            mirrors=mirrors,
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
    for issue in issues:
        print(issue.render(root))
    tally = tally_issues(issues)
    detail = f" ({tally.describe()})" if mirrors else ""
    exit_code = tally.exit_code
    if exit_code == 2:
        print(f"\nIncomplete: {tally.unavailable} link(s) could not be proven because a declared "
              f"origin is unavailable; {tally.counted} issue(s) in {len(checked)} file(s)"
              f"{detail}.", file=sys.stderr)
        return exit_code
    if exit_code == 1:
        print(f"\nFound {tally.counted} issue(s) in {len(checked)} file(s){detail}.",
              file=sys.stderr)
        return exit_code
    scopes = ["links"]
    if args.localized_pair:
        scopes.append("localized pairs")
    if args.line_budget:
        scopes.append("line budgets")
    scope = ", ".join(scopes)
    print(f"Validated {scope} in {len(checked)} Markdown file(s) under {root}.{detail}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
