#!/usr/bin/env python3
"""Gather focused diagnostic data for a single Pod."""

from __future__ import annotations

import argparse
import shutil
import subprocess
from datetime import datetime, timezone
from typing import Iterable


def detect_cli() -> str:
    for tool in ("oc", "kubectl"):
        if shutil.which(tool):
            return tool
    raise SystemExit("kubectl or oc is required")


def run(cmd: list[str]) -> str:
    try:
        completed = subprocess.run(cmd, capture_output=True, text=True, timeout=45, check=False)
    except subprocess.TimeoutExpired:
        return "<command timed out>"
    output = completed.stdout.strip()
    error = completed.stderr.strip()
    if output and error:
        return f"{output}\n{error}"
    return output or error or "<no output>"


def print_section(title: str, cmd: list[str]) -> None:
    print(f"\n## {title} ##")
    print(run(cmd))


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Collect diagnostics for a pod")
    parser.add_argument("pod_name")
    parser.add_argument("-n", "--namespace", default="default")
    args = parser.parse_args(list(argv) if argv is not None else None)

    cli = detect_cli()
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    print("=" * 80)
    print(f"Pod diagnostics via {cli} for {args.namespace}/{args.pod_name}")
    print(f"Timestamp: {stamp}")
    print("=" * 80)

    base = [cli, "-n", args.namespace]
    print_section("POD", base + ["get", "pod", args.pod_name, "-o", "wide"])
    print_section("DESCRIBE", base + ["describe", "pod", args.pod_name])
    print_section("YAML", base + ["get", "pod", args.pod_name, "-o", "yaml"])
    print_section("EVENTS", base + ["get", "events", "--sort-by=.lastTimestamp"])
    print_section("CURRENT LOGS", base + ["logs", args.pod_name, "--all-containers", "--tail=200"])
    print_section("PREVIOUS LOGS", base + ["logs", args.pod_name, "--all-containers", "--previous", "--tail=200"])
    print_section("TOP", base + ["top", "pod", args.pod_name, "--containers"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
