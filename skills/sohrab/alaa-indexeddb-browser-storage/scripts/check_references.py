#!/usr/bin/env python3
"""Check that the router routes: every reference is reachable and every path resolves.

Exit codes
  0  clean: every router path resolves and every reference file is routed.
  1  findings: at least one dangling path, unrouted file, or second router. Each is
     printed with file and line. Resolve every one before reporting a change complete.
  2  could not run: the pack root or the router is missing or unreadable. Exit 2 is
     never a pass -- run the checks by hand and report each.

The pack root is resolved from this file's location (`parents[1]`), which is
CWD-independent and correct as long as the script stays in `scripts/`. `--root`
overrides it, so the script also works if it is ever vendored elsewhere.
"""
from __future__ import annotations

import argparse
import re
import sys
import tempfile
from pathlib import Path

EXIT_CLEAN, EXIT_FINDINGS, EXIT_CANNOT_RUN = 0, 1, 2

ROUTER = "references/00-topic-map.md"
BODY = "SKILL.md"

# The router writes reference rows as bare filenames and example/asset rows as paths.
# Accepting only the `references/...` form is why the previous version validated zero
# reference files and still printed a success message about references.
BARE_REF = re.compile(r"`(\d{2}-[a-z0-9-]+\.md)`")
FULL_PATH = re.compile(r"`(references/[^`]+\.md|examples/[^`]+\.ts|assets/[^`]+|scripts/[^`]+)`")

SELF = "alaa-indexeddb-browser-storage"
# A cross-skill reference always names the owning skill beside the path. A line that
# names another skill points into that skill's tree and is not resolved here; a line
# that does not must resolve locally. That is the rule this pattern enforces.
OTHER_SKILL = re.compile(r"[/$](alaa-[a-z0-9-]+|playwright[a-z-]*|golang-[a-z-]+|caas-[a-z-]+)")


def names_another_skill(line: str) -> bool:
    return any(name != SELF for name in OTHER_SKILL.findall(line))


def find(root: Path) -> list[str]:
    findings: list[str] = []
    router_path = root / ROUTER

    router_text = router_path.read_text(encoding="utf-8")
    routed: set[str] = set()

    for lineno, line in enumerate(router_text.splitlines(), start=1):
        for name in BARE_REF.findall(line):
            routed.add(name)
            if not (root / "references" / name).exists():
                findings.append(f"{ROUTER}:{lineno}: dangling reference `{name}`")
        if names_another_skill(line):
            continue
        for rel in FULL_PATH.findall(line):
            if not (root / rel).exists():
                findings.append(f"{ROUTER}:{lineno}: dangling path `{rel}`")
            if rel.startswith("references/"):
                routed.add(Path(rel).name)

    # Every reference file must be named by the router. An unrouted file is reachable
    # only by directory listing, which is how a 75 KB unreachable duplicate survived.
    for path in sorted((root / "references").glob("*.md")):
        if path.name == "00-topic-map.md":
            continue
        if path.name not in routed:
            findings.append(f"references/{path.name}: not named by {ROUTER}")

    # One router per skill. A table in the body is a second router that will drift.
    body_path = root / BODY
    if body_path.exists():
        body_text = body_path.read_text(encoding="utf-8")
        ref_rows = 0
        for lineno, line in enumerate(body_text.splitlines(), start=1):
            if line.lstrip().startswith("|") and (BARE_REF.search(line) or "references/" in line):
                ref_rows += 1
                if ref_rows > 1:
                    findings.append(
                        f"{BODY}:{lineno}: a second router in the body; the router is {ROUTER}"
                    )
                    break
        for lineno, line in enumerate(body_text.splitlines(), start=1):
            cross_skill = names_another_skill(line)
            for rel in FULL_PATH.findall(line):
                if cross_skill:
                    # Owned elsewhere. Rule 8 is satisfied: the owning skill is named.
                    continue
                if not (root / rel).exists():
                    findings.append(
                        f"{BODY}:{lineno}: dangling path `{rel}` with no owning skill named beside it"
                    )

    return findings


def self_test() -> int:
    """Prove the checker fails when it should. A green that cannot go red is not evidence."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "references").mkdir()
        (root / "references" / "00-topic-map.md").write_text(
            "| you are about to X | `10-present.md` |\n"
            "| you are about to Y | `99-absent.md` |\n",
            encoding="utf-8",
        )
        (root / "references" / "10-present.md").write_text("ok\n", encoding="utf-8")
        (root / "references" / "50-orphan.md").write_text("ok\n", encoding="utf-8")

        findings = find(root)
        expected_dangling = any("99-absent.md" in f and "dangling" in f for f in findings)
        expected_orphan = any("50-orphan.md" in f and "not named" in f for f in findings)

        if not expected_dangling:
            print("SELF-TEST FAIL: a dangling reference row was not reported", file=sys.stderr)
            return EXIT_FINDINGS
        if not expected_orphan:
            print("SELF-TEST FAIL: an unrouted reference file was not reported", file=sys.stderr)
            return EXIT_FINDINGS

        # And prove it goes green on a correct fixture.
        (root / "references" / "00-topic-map.md").write_text(
            "| you are about to X | `10-present.md` |\n"
            "| you are about to Z | `50-orphan.md` |\n",
            encoding="utf-8",
        )
        (root / "references" / "99-absent.md").write_text("ok\n", encoding="utf-8")
        (root / "references" / "00-topic-map.md").write_text(
            "| X | `10-present.md` |\n| Z | `50-orphan.md` |\n| W | `99-absent.md` |\n",
            encoding="utf-8",
        )
        if find(root):
            print(f"SELF-TEST FAIL: clean fixture reported {find(root)}", file=sys.stderr)
            return EXIT_FINDINGS

    print("SELF-TEST OK: the checker reports a dangling path, an unrouted file, and a clean pack")
    return EXIT_CLEAN


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="check_references.py",
        description="Check that every router path resolves and every reference is routed.",
        epilog="Exit 0 clean, 1 findings, 2 could not run. Exit 2 is never a pass.",
    )
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--self-test", action="store_true", help="run the built-in fixtures")
    args = parser.parse_args()

    if args.self_test:
        return self_test()

    root: Path = args.root.resolve()
    if not (root / ROUTER).is_file():
        print(f"CANNOT RUN: {root / ROUTER} is missing or unreadable", file=sys.stderr)
        return EXIT_CANNOT_RUN

    try:
        findings = find(root)
    except OSError as error:
        print(f"CANNOT RUN: {error}", file=sys.stderr)
        return EXIT_CANNOT_RUN

    if findings:
        for finding in findings:
            print(f"FINDING: {finding}", file=sys.stderr)
        print(f"{len(findings)} finding(s)", file=sys.stderr)
        return EXIT_FINDINGS

    routed = len(list((root / "references").glob("*.md"))) - 1
    print(f"OK: {routed} reference file(s) routed, every router path resolves")
    return EXIT_CLEAN


if __name__ == "__main__":
    raise SystemExit(main())
