#!/usr/bin/env python3
"""Validate inline and reference-style Markdown links for local docs."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterator, List, Sequence, Set, Tuple

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)(?:\s+#+\s*)?$")
INLINE_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
REF_DEF_RE = re.compile(r"^\s{0,3}\[([^\]]+)\]:\s*(\S+)")
REF_LINK_RE = re.compile(r"!?\[([^\]]+)\]\[([^\]]*)\]")
WINDOWS_ABS_RE = re.compile(r"^[A-Za-z]:[\/]")
SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")


@dataclass
class LinkIssue:
    file: Path
    line_no: int
    target: str
    message: str

    def render(self, root: Path) -> str:
        return f"{self.file.relative_to(root)}:{self.line_no}: {self.message}: {self.target}"


def slugify_heading(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[`*_~]", "", text)
    text = re.sub(r"[^a-z0-9_\-\s]", "", text)
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def split_link_target(raw: str) -> str:
    target = raw.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1].strip()
    for quote in (' "', " '"):
        idx = target.find(quote)
        if idx != -1:
            target = target[:idx].strip()
            break
    return target


def iter_markdown_files(root: Path) -> Iterator[Path]:
    root = root.resolve()
    for path in sorted(root.rglob("*.md")):
        rel_parts = path.relative_to(root).parts
        if any(part.startswith(".") for part in rel_parts):
            continue
        if path.is_file():
            yield path


def read_lines(path: Path) -> List[str]:
    return path.read_text(encoding="utf-8").splitlines()


def collect_headings(path: Path) -> Set[str]:
    slugs: Set[str] = set()
    counts: Dict[str, int] = {}
    in_fence = False
    for line in read_lines(path):
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
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


def collect_reference_definitions(lines: Sequence[str]) -> Dict[str, str]:
    defs: Dict[str, str] = {}
    in_fence = False
    for line in lines:
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = REF_DEF_RE.match(line)
        if match:
            defs[match.group(1).strip().lower()] = split_link_target(match.group(2))
    return defs


def extract_targets(path: Path) -> List[Tuple[int, str]]:
    lines = read_lines(path)
    ref_defs = collect_reference_definitions(lines)
    targets: List[Tuple[int, str]] = []
    in_fence = False
    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
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


def validate_target(root: Path, file_path: Path, line_no: int, target: str, heading_cache: Dict[Path, Set[str]]) -> List[LinkIssue]:
    issues: List[LinkIssue] = []
    if not target:
        return issues
    if target.startswith("file://"):
        return [LinkIssue(file_path, line_no, target, "file:// links are not allowed")]
    if is_external(target):
        return issues
    if WINDOWS_ABS_RE.match(target) or target.startswith("/"):
        return [LinkIssue(file_path, line_no, target, "absolute local paths are not allowed")]
    if "\\" in target:
        return [LinkIssue(file_path, line_no, target, "use POSIX-style forward slashes in links")]

    path_part, _, anchor = target.partition("#")
    resolved = file_path.resolve() if not path_part else (file_path.parent / path_part).resolve()
    try:
        resolved.relative_to(root)
    except ValueError:
        return [LinkIssue(file_path, line_no, target, "link resolves outside the repository root")]

    if path_part and not resolved.exists():
        return [LinkIssue(file_path, line_no, target, "target file does not exist")]

    if anchor:
        if resolved.suffix.lower() != ".md":
            return [LinkIssue(file_path, line_no, target, "anchors are only validated for Markdown files")]
        slugs = heading_cache.setdefault(resolved, collect_headings(resolved))
        if anchor not in slugs:
            return [LinkIssue(file_path, line_no, target, "target heading anchor was not found")]
    return issues


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate local Markdown links and anchors.")
    parser.add_argument("repo_root", help="Repository root that relative links should resolve within")
    parser.add_argument("--files", nargs="*", default=None, help="Specific Markdown files to validate relative to repo_root. Defaults to all Markdown files under repo_root.")
    return parser.parse_args(argv)


def main(argv: Sequence[str]) -> int:
    args = parse_args(argv)
    root = Path(args.repo_root).resolve()
    if not root.exists() or not root.is_dir():
        print(f"Repository root not found or not a directory: {root}", file=sys.stderr)
        return 2

    files = [Path(root / rel).resolve() for rel in args.files] if args.files else list(iter_markdown_files(root))
    missing = [path for path in files if not path.exists()]
    if missing:
        for path in missing:
            print(f"Missing file: {path}", file=sys.stderr)
        return 2

    heading_cache: Dict[Path, Set[str]] = {}
    issues: List[LinkIssue] = []
    for path in files:
        if path.suffix.lower() != ".md":
            continue
        for line_no, target in extract_targets(path):
            issues.extend(validate_target(root, path, line_no, target, heading_cache))

    if issues:
        for issue in issues:
            print(issue.render(root))
        print(f"\nFound {len(issues)} Markdown link issue(s).", file=sys.stderr)
        return 1

    checked = ", ".join(str(path.relative_to(root)) for path in files)
    print(f"Validated Markdown links successfully for: {checked}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
