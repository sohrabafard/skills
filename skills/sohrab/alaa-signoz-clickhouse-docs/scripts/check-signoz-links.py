#!/usr/bin/env python3
"""Check that every URL this skill asserts still resolves, and does not silently move.

Exit codes, and they are the point of this script:
  0  every URL returned 200 and did not redirect to a different path
  1  at least one URL is dead or has moved
  2  the answer could not be determined -- no network, DNS failure, proxy refusal

A checker whose "could not run" is indistinguishable from its "clean" is worse than no
checker, because a CI gate built on it treats a broken network as a pass. So a single
transport failure forces exit 2: a dead link and a dead network look identical from here,
and this script refuses to guess which it saw.

Runs on Windows and POSIX: pure Python 3, no shell pipelines, no path separator assumptions.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

URL_RE = re.compile(r"https://[^\s<>\)\]\"'`|]+")
# A template, not an address: REGION, BASE_URL, <topic>, {{var}}. Fetching one proves nothing.
TEMPLATE_RE = re.compile(r"[A-Z_]{3,}|[<>{}]|\.\.\.")
TRAILING_PUNCT = ".,;:!?"

CLEAN = 0
FINDINGS = 1
BLOCKED = 2


def default_skill_dir() -> Path:
    """Default only, always overridable with --skill-dir. Never a hardcoded parents[N] path."""
    return Path(sys.argv[0]).resolve().parent.parent


def strip_trailing(url: str) -> str:
    while url and url[-1] in TRAILING_PUNCT:
        url = url[:-1]
    return url


def collect_urls(skill_dir: Path):
    """Yield (relative_path, line_number, url) for every checkable URL in the skill's markdown."""
    found = []
    for md in sorted(skill_dir.rglob("*.md")):
        try:
            text = md.read_text(encoding="utf-8")
        except OSError as exc:
            raise RuntimeError("cannot read {}: {}".format(md, exc))
        rel = md.relative_to(skill_dir).as_posix()
        for lineno, line in enumerate(text.splitlines(), start=1):
            for raw in URL_RE.findall(line):
                url = strip_trailing(raw)
                if TEMPLATE_RE.search(url):
                    continue
                found.append((rel, lineno, url))
    return found


def normalise(url: str) -> str:
    return url.rstrip("/")


def fetch(url: str, timeout: int):
    """Return (status, final_url) or raise TransportError when the network cannot answer."""
    request = urllib.request.Request(url, method="GET", headers={"User-Agent": "signoz-skill-link-check/1"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.status, response.geturl()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.url or url
    except Exception as exc:
        raise TransportError("{}: {}".format(type(exc).__name__, exc))


class TransportError(Exception):
    pass


def judge(url: str, status, final_url: str, allow_redirect: bool):
    """Pure decision function. Shared by the live run and the offline self-test."""
    if status != 200:
        return "HTTP {}".format(status)
    if not allow_redirect and normalise(final_url) != normalise(url):
        return "redirected to {}".format(final_url)
    return None


def run(skill_dir: Path, timeout: int, concurrency: int, allow_redirect: bool, as_json: bool) -> int:
    if not skill_dir.is_dir():
        print("BLOCKED: --skill-dir does not exist: {}".format(skill_dir), file=sys.stderr)
        return BLOCKED
    try:
        targets = collect_urls(skill_dir)
    except RuntimeError as exc:
        print("BLOCKED: {}".format(exc), file=sys.stderr)
        return BLOCKED
    if not targets:
        print("BLOCKED: no URLs found under {}".format(skill_dir), file=sys.stderr)
        return BLOCKED

    unique = sorted({url for _, _, url in targets})

    def probe(url):
        try:
            status, final_url = fetch(url, timeout)
            return url, status, final_url, None
        except TransportError as exc:
            return url, None, None, str(exc)

    results = {}
    with ThreadPoolExecutor(max_workers=max(1, concurrency)) as pool:
        for url, status, final_url, error in pool.map(probe, unique):
            results[url] = (status, final_url, error)

    blocked, findings = [], []
    for rel, lineno, url in targets:
        status, final_url, error = results[url]
        if error is not None:
            blocked.append({"file": rel, "line": lineno, "url": url, "reason": error})
            continue
        verdict = judge(url, status, final_url, allow_redirect)
        if verdict:
            findings.append({"file": rel, "line": lineno, "url": url, "reason": verdict})

    if as_json:
        print(json.dumps({"checked": len(targets), "unique": len(unique),
                          "findings": findings, "blocked": blocked}, indent=2))
    else:
        for item in blocked:
            print("BLOCKED {file}:{line}  {url}  {reason}".format(**item))
        for item in findings:
            print("FINDING {file}:{line}  {url}  {reason}".format(**item))
        print("checked {} references to {} unique URLs".format(len(targets), len(unique)))

    if blocked:
        print("exit 2: {} URL(s) could not be reached. A dead link and a dead network are "
              "indistinguishable from here, so this is not a pass.".format(len(blocked)), file=sys.stderr)
        return BLOCKED
    return FINDINGS if findings else CLEAN


def self_test(skill_dir: Path) -> int:
    """Two parts. Part A is offline and deterministic: it is the committed red fixture.

    Part A drives the same judge() and collect_urls() the live run uses, against
    test/fixtures/links/, with a stubbed responder. It must fail on a 404 and on a
    silent redirect with no network at all -- otherwise a green run proves nothing.
    Part B tries the network and records BLOCKED rather than FAIL when it cannot.
    """
    fixture = skill_dir / "test" / "fixtures" / "links"
    if not fixture.is_dir():
        print("BLOCKED: fixture missing: {}".format(fixture), file=sys.stderr)
        return BLOCKED

    stub = {
        "https://example.invalid/good/": (200, "https://example.invalid/good/"),
        "https://example.invalid/dead/": (404, "https://example.invalid/dead/"),
        "https://example.invalid/moved/page/": (200, "https://example.invalid/docs/"),
    }
    failures = []

    extracted = {url for _, _, url in collect_urls(fixture)}
    for url in stub:
        if url not in extracted:
            failures.append("extraction missed {}".format(url))
    if "https://example.invalid/ingest.REGION.host/" in extracted:
        failures.append("extraction did not skip the templated URL")

    expectations = [
        ("https://example.invalid/good/", None),
        ("https://example.invalid/dead/", "HTTP 404"),
        ("https://example.invalid/moved/page/", "redirected to https://example.invalid/docs/"),
    ]
    for url, expected in expectations:
        status, final_url = stub[url]
        actual = judge(url, status, final_url, allow_redirect=False)
        if actual != expected:
            failures.append("judge({}) returned {!r}, expected {!r}".format(url, actual, expected))

    if judge("https://example.invalid/moved/page/", 200,
             "https://example.invalid/docs/", allow_redirect=True) is not None:
        failures.append("--allow-redirect did not downgrade a redirect")

    print("self-test part A (offline, red fixture): {} assertion(s), {} failure(s)".format(
        len(expectations) + 3, len(failures)))
    for failure in failures:
        print("  FAIL {}".format(failure))
    if failures:
        return FINDINGS

    try:
        fetch("https://example.invalid/good/", 5)
        print("self-test part B (live): network reachable")
        return CLEAN
    except TransportError as exc:
        print("self-test part B (live): BLOCKED, not FAIL -- {}".format(exc))
        print("exit 2: part A passed, part B could not run.", file=sys.stderr)
        return BLOCKED


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify every URL asserted in this skill resolves and has not moved.",
        epilog="Exit 0 clean, 1 findings, 2 could not run. A 2 is never a pass.")
    parser.add_argument("--skill-dir", type=Path, default=None,
                        help="skill root to scan for *.md (default: the parent of this script's directory)")
    parser.add_argument("--timeout", type=int, default=20, help="per-request timeout in seconds (default 20)")
    parser.add_argument("--concurrency", type=int, default=4, help="parallel requests (default 4)")
    parser.add_argument("--allow-redirect", action="store_true",
                        help="treat a redirect to a different path as a note rather than a finding")
    parser.add_argument("--json", dest="as_json", action="store_true", help="machine-readable output")
    parser.add_argument("--self-test", action="store_true", help="run the committed fixture assertions")
    args = parser.parse_args()

    skill_dir = args.skill_dir if args.skill_dir is not None else default_skill_dir()
    if args.self_test:
        return self_test(skill_dir)
    return run(skill_dir, args.timeout, args.concurrency, args.allow_redirect, args.as_json)


if __name__ == "__main__":
    raise SystemExit(main())
