#!/usr/bin/env python3
"""Collect focused, read-only diagnostic evidence for one Pod.

Exit codes, shared by every script in this skill:
    0  every section returned data
    1  findings: a section timed out or returned nothing, so the evidence is partial
    2  could not run: no kubectl or oc, or the Pod is not visible to this identity

A section that timed out is a finding rather than a success: the original
version of this script printed the timeout into its report and still exited 0,
so a caller that branched on exit status read an empty report as a healthy Pod.

Windows: pure Python 3 standard library, `shutil.which` for CLI discovery, and
a per-command timeout.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from datetime import datetime, timezone

EXIT_CLEAN = 0
EXIT_FINDINGS = 1
EXIT_CANNOT_RUN = 2

TIMED_OUT = "<command timed out>"
NO_OUTPUT = "<no output>"


def detect_cli() -> str | None:
    for tool in ("oc", "kubectl"):
        if shutil.which(tool):
            return tool
    return None


def run(cmd: list[str], timeout: float) -> tuple[str, bool]:
    """Return (text, ok). `ok` is False when the command produced no evidence."""
    try:
        completed = subprocess.run(cmd, capture_output=True, text=True,
                                   timeout=timeout, check=False)
    except subprocess.TimeoutExpired:
        return TIMED_OUT, False
    except OSError as exc:
        return f"<could not execute: {exc}>", False
    out = completed.stdout.strip()
    err = completed.stderr.strip()
    if out and err:
        return f"{out}\n{err}", True
    if out:
        return out, True
    if err:
        return err, False
    return NO_OUTPUT, False


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pod_diagnostics.py",
        description="Collect read-only diagnostics for a single Pod: status, describe, "
                    "spec, events, current and previous logs, and resource usage.",
        epilog="Exit codes: 0 every section returned data, 1 partial evidence, "
               "2 could not run.",
    )
    parser.add_argument("pod_name", nargs="?")
    parser.add_argument("-n", "--namespace", default="default")
    parser.add_argument("--timeout", type=float, default=45.0,
                        help="per-command timeout in seconds (default: 45)")
    parser.add_argument("--self-test", action="store_true",
                        help="verify argument handling, timeout accounting and exit codes; "
                             "needs no cluster")
    return parser


def self_test() -> int:
    failures: list[str] = []

    text, ok = run([sys.executable, "-c", "import time; time.sleep(5)"], timeout=0.5)
    if ok or text != TIMED_OUT:
        failures.append("a timed-out command was not reported as missing evidence")

    text, ok = run([sys.executable, "-c", "print('hello')"], timeout=10)
    if not ok or text != "hello":
        failures.append(f"a successful command was misreported: {text!r} ok={ok}")

    text, ok = run([sys.executable, "-c", ""], timeout=10)
    if ok or text != NO_OUTPUT:
        failures.append("a command with no output was reported as evidence")

    text, ok = run(["definitely-not-a-real-binary-xyz"], timeout=5)
    if ok:
        failures.append("a missing binary was reported as evidence")

    parser = build_parser()
    args = parser.parse_args(["mypod", "-n", "vk"])
    if args.pod_name != "mypod" or args.namespace != "vk":
        failures.append("argument parsing lost a value")

    if main(["--namespace", "vk"]) != EXIT_CANNOT_RUN:
        failures.append("a missing pod name did not exit 2")

    if failures:
        for line in failures:
            print(f"SELF-TEST FAIL: {line}", file=sys.stderr)
        return EXIT_FINDINGS
    print("pod_diagnostics --self-test: 6 cases passed (no cluster required)")
    return EXIT_CLEAN


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.self_test:
        return self_test()

    if not args.pod_name:
        print("pod_diagnostics: a pod name is required (or --self-test)", file=sys.stderr)
        return EXIT_CANNOT_RUN

    cli = detect_cli()
    if cli is None:
        print("pod_diagnostics: kubectl or oc is required and neither is on PATH",
              file=sys.stderr)
        return EXIT_CANNOT_RUN

    base = [cli, "-n", args.namespace]
    _, visible = run(base + ["get", "pod", args.pod_name, "-o", "name"], args.timeout)
    if not visible:
        print(f"pod_diagnostics: pod {args.namespace}/{args.pod_name} is not visible to "
              "this identity", file=sys.stderr)
        return EXIT_CANNOT_RUN

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    print("=" * 80)
    print(f"Pod diagnostics via {cli} for {args.namespace}/{args.pod_name}")
    print(f"Timestamp: {stamp}")
    print("=" * 80)

    sections = [
        ("POD", ["get", "pod", args.pod_name, "-o", "wide"]),
        ("DESCRIBE", ["describe", "pod", args.pod_name]),
        ("SPEC", ["get", "pod", args.pod_name, "-o", "yaml"]),
        ("EVENTS", ["get", "events", "--sort-by=.lastTimestamp"]),
        ("CURRENT LOGS", ["logs", args.pod_name, "--all-containers", "--tail=200"]),
        ("PREVIOUS LOGS", ["logs", args.pod_name, "--all-containers", "--previous", "--tail=200"]),
        ("TOP", ["top", "pod", args.pod_name, "--containers"]),
    ]

    incomplete: list[str] = []
    for title, cmd in sections:
        text, ok = run(base + cmd, args.timeout)
        print(f"\n## {title} ##")
        print(text)
        if not ok:
            incomplete.append(title)

    if incomplete:
        print(f"\npod_diagnostics: {len(incomplete)} section(s) returned no evidence "
              f"({', '.join(incomplete)}); this report is partial.", file=sys.stderr)
        return EXIT_FINDINGS
    print("\npod_diagnostics: every section returned evidence.")
    return EXIT_CLEAN


if __name__ == "__main__":
    sys.exit(main())
