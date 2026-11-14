#!/usr/bin/env python3
"""Re-derive the pinned version values in references/version-awareness.md.

A version number written into a file goes stale silently. This script turns that
silence into a finding: it reads the "Pinned values" table in
`references/version-awareness.md`, fetches the vendors' own pages, and reports
every value that has moved.

Exit codes, shared by every script in this skill:
    0  the pinned values match the vendors' pages
    1  findings: at least one pinned value has drifted
    2  could not run: no network, a blocked proxy, an unreadable reference file,
       or a page from which no stable version or required date could be extracted

Pure Python 3 with the standard library only, no shell, no curl.
Proxies: `urllib` reads `HTTPS_PROXY` and `NO_PROXY` from the environment, so a
sandboxed or corporate egress path works without extra flags.

The script resolves the reference file from its own path and never writes
anything, so a read-only checkout is fine.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import urllib.error
import urllib.request

EXIT_CLEAN = 0
EXIT_FINDINGS = 1
EXIT_CANNOT_RUN = 2

SCRIPT_PATH = os.path.abspath(__file__)
SCRIPT_DIR = os.path.dirname(SCRIPT_PATH)
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
DEFAULT_REFERENCE = os.path.join(SKILL_DIR, "references", "version-awareness.md")

USER_AGENT = "version-check/1"

CHECKS = [
    {
        "id": "kubernetes-latest",
        "label": "latest Kubernetes minor",
        "url": "https://kubernetes.io/releases/",
        "page_pattern": r"\b1\.(\d{2})\.\d+(?![\w.+-])",
        "pinned_row": "Latest Kubernetes minor",
        "pinned_pattern": r"\b(1\.\d{2})\b",
        "reduce": "max",
    },
    {
        "id": "helm-latest",
        "label": "latest Helm release",
        "url": "https://github.com/helm/helm/releases",
        "page_pattern": r"\bv(\d+\.\d+\.\d+)(?![\w.+-])",
        "pinned_row": "Current Helm major",
        "pinned_pattern": r"latest (\d+\.\d+\.\d+)",
        "reduce": "max-semver",
    },
    {
        "id": "helm3-eol",
        "label": "Helm 3 end-of-life date",
        "url": "https://helm.sh/blog/helm-v3-end-of-life/",
        "page_pattern": r"\b(20\d{2}-\d{2}-\d{2}|February 10(?:th)?,? 20\d{2})\b",
        "pinned_row": "Helm 3 end of life",
        "pinned_pattern": r"\*\*(20\d{2}-\d{2}-\d{2})\*\*",
        "reduce": "date-mentioned",
    },
]


class CouldNotRun(Exception):
    pass


def read_reference(path: str) -> str:
    if not os.path.isfile(path):
        raise CouldNotRun(f"reference file not found: {path}")
    try:
        with open(path, "r", encoding="utf-8", newline=None) as handle:
            return handle.read()
    except OSError as exc:
        raise CouldNotRun(f"cannot read {path}: {exc}") from exc


def pinned_value(reference: str, row_label: str, pattern: str) -> str:
    for line in reference.splitlines():
        if line.lstrip().startswith("|") and row_label in line:
            match = re.search(pattern, line)
            if match:
                return match.group(1)
            raise CouldNotRun(
                f"found the '{row_label}' row but no value matching {pattern!r}; "
                "the pinned table's shape changed and this script must be updated with it"
            )
    raise CouldNotRun(
        f"no row labelled '{row_label}' in the pinned values table; "
        "the reference file and this script have diverged"
    )


def fetch(url: str, timeout: float) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read()
    except urllib.error.HTTPError as exc:
        raise CouldNotRun(f"{url} returned HTTP {exc.code}") from exc
    except (urllib.error.URLError, OSError) as exc:
        raise CouldNotRun(f"{url} is unreachable: {exc}") from exc
    return raw.decode("utf-8", errors="replace")


def semver_key(value: str) -> tuple[int, ...]:
    return tuple(int(part) for part in value.split("."))


def observed_value(check: dict, page: str) -> str:
    matches = re.findall(check["page_pattern"], page)
    if not matches:
        raise CouldNotRun(
            f"{check['url']} contained nothing matching {check['page_pattern']!r}; "
            "the page shape changed and this check cannot return a verdict"
        )
    if check["reduce"] == "max":
        return "1." + max(matches, key=int)
    if check["reduce"] == "max-semver":
        return max(matches, key=semver_key)
    if check["reduce"] == "date-mentioned":
        return "|".join(sorted({str(m) for m in matches}))
    raise CouldNotRun(f"unknown reduce mode {check['reduce']!r}")


def compare(check: dict, pinned: str, observed: str) -> str | None:
    if check["reduce"] == "date-mentioned":
        iso = pinned
        try:
            year, month, day = iso.split("-")
        except ValueError:
            return f"pinned date {iso!r} is not ISO-8601"
        prose = rf"\bFebruary {int(day)}(?:th)?,? {re.escape(year)}\b"
        if iso in observed.split("|") or (month == "02" and re.search(prose, observed)):
            return None
        return (f"pinned {check['label']} is {pinned}, and that date is not mentioned on "
                f"{check['url']}")
    if pinned != observed:
        return f"pinned {check['label']} is {pinned}, the vendor page says {observed}"
    return None


def run_checks(reference_path: str, timeout: float) -> list[str]:
    reference = read_reference(reference_path)
    findings: list[str] = []
    for check in CHECKS:
        pinned = pinned_value(reference, check["pinned_row"], check["pinned_pattern"])
        page = fetch(check["url"], timeout)
        observed = observed_value(check, page)
        problem = compare(check, pinned, observed)
        if problem:
            findings.append(f"{check['id']}: {problem}")
    return findings


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="check_versions.py",
        description=(
            "Compare the pinned values in references/version-awareness.md against the "
            "vendors' own release pages, so version drift is a finding rather than a discovery."
        ),
        epilog="Exit codes: 0 pinned values match, 1 drift, 2 could not run.",
    )
    parser.add_argument("--reference", default=DEFAULT_REFERENCE,
                        help="path to version-awareness.md (default: the one beside this script)")
    parser.add_argument("--timeout", type=float, default=15.0,
                        help="per-request timeout in seconds (default: 15)")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        findings = run_checks(args.reference, args.timeout)
    except CouldNotRun as exc:
        print(f"check_versions: could not run: {exc}", file=sys.stderr)
        print("check_versions: this is exit 2, not a clean verdict; the pinned values were "
              "not checked.", file=sys.stderr)
        return EXIT_CANNOT_RUN
    if not findings:
        print(f"check_versions: {len(CHECKS)} pinned values still match the vendors' pages")
        return EXIT_CLEAN
    for line in findings:
        print(line)
    print(f"check_versions: {len(findings)} pinned value(s) have drifted; update "
          f"{args.reference} and re-run", file=sys.stderr)
    return EXIT_FINDINGS


if __name__ == "__main__":
    sys.exit(main())
