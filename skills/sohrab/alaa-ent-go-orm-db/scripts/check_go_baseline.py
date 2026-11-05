#!/usr/bin/env python3
"""Read a module/workspace baseline and an installed compiler without downloads.

Requires Python >=3.10; no third-party packages. See 10-go-and-generation.md.
Writes JSON to stdout. Exit 0: baseline met; 1: violation; 2: proof unavailable.
This is not a compiler, a go.mod parser, or a compatibility/performance test.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys

MINIMUM = (1, 27, 3)
STABLE = re.compile(r"([1-9][0-9]*)\.(0|[1-9][0-9]*)(?:\.(0|[1-9][0-9]*))?")


def version(value: str, *, prefixed: bool = False) -> tuple[int, int, int] | None:
    if prefixed:
        if not value.startswith("go"):
            return None
        value = value[2:]
    match = STABLE.fullmatch(value)
    if not match:
        return None
    try:
        return tuple(int(part or 0) for part in match.groups())
    except ValueError:
        # Preserve Python's integer-conversion safety limit and the JSON contract.
        return None


def display(value: tuple[int, int, int]) -> str:
    return ".".join(map(str, value))


def directives(path: Path) -> dict[str, str]:
    # Only directive lines matter; this intentionally does not validate go.mod.
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    result: dict[str, str] = {}
    for line in text.splitlines():
        line = line.split("//", 1)[0].strip()
        match = re.fullmatch(r"(go|toolchain)\s+(\S+)", line)
        if not match:
            if re.match(r"^(go|toolchain)(?:\s|$)", line):
                raise ValueError("malformed Go/toolchain directive")
            continue
        key, value = match.groups()
        if key in result:
            raise ValueError("duplicate " + key + " directive")
        result[key] = value
    return result


def workspace_for(project: Path) -> Path | None:
    setting = os.environ.get("GOWORK", "")
    if setting == "off":
        return None
    if setting:
        path = Path(setting)
        if not path.is_absolute():
            raise ValueError("GOWORK must be off or an absolute file path")
        return path
    for directory in (project, *project.parents):
        candidate = directory / "go.work"
        if candidate.is_file():
            return candidate
    return None


def check(project: Path, go_binary: str, releases: Path | None) -> tuple[dict, int]:
    report: dict = {
        "minimum": display(MINIMUM),
        "project": str(project),
        "scope": "local installed compiler and module/workspace directives only",
        "automatic_toolchain_selection": "not exercised; GOTOOLCHAIN=local used",
        "directives": [],
        "findings": [],
        "unavailable": [],
        "notes": [],
    }
    findings, unavailable = report["findings"], report["unavailable"]
    required = MINIMUM
    if not project.is_dir():
        unavailable.append("project directory is unavailable")
    paths = [project / "go.mod"]
    try:
        workspace = workspace_for(project)
        if workspace is not None:
            paths.append(workspace)
    except ValueError as error:
        unavailable.append(str(error))
    for path in paths:
        try:
            values = directives(path)
        except (OSError, UnicodeError, ValueError) as error:
            unavailable.append(f"cannot inspect {path.name}: {type(error).__name__}: {error}")
            continue
        report["directives"].append({"path": str(path), **values})
        minimum = version(values.get("go", ""))
        if minimum is None:
            unavailable.append(f"{path.name}: missing or unsupported stable go directive")
        else:
            required = max(required, minimum)
            if minimum < MINIMUM:
                findings.append(f"{path.name}: go {display(minimum)} is below {display(MINIMUM)}")
        suggestion = values.get("toolchain")
        if suggestion and suggestion != "default":
            suggested = version(suggestion, prefixed=True)
            if suggested is None:
                unavailable.append(f"{path.name}: unsupported stable toolchain directive")
            elif minimum is not None and suggested < minimum:
                report["notes"].append(f"{path.name}: toolchain suggestion is older than its go directive; review configuration")
    report["required_local_compiler"] = display(required)
    local = None
    try:
        environment = dict(os.environ)
        environment["GOTOOLCHAIN"] = "local"
        run = subprocess.run(
            [go_binary, "version"], cwd=project, env=environment,
            capture_output=True, text=True, timeout=10, check=False,
        )
        if run.returncode != 0:
            unavailable.append(f"go version failed with exit {run.returncode}; output omitted")
        else:
            match = re.fullmatch(r"go version (go[^\s]+) [^\s]+", run.stdout.strip())
            local = version(match.group(1), prefixed=True) if match else None
            if local is None:
                unavailable.append("go version did not identify a supported stable compiler")
            else:
                report["local_go_version"] = display(local)
                if local < required:
                    findings.append(f"installed Go {display(local)} is below required {display(required)}")
    except (OSError, subprocess.TimeoutExpired, UnicodeError) as error:
        unavailable.append(f"cannot run installed Go: {type(error).__name__}")
    if releases is not None:
        try:
            data = json.loads(releases.read_text(encoding="utf-8"))
            if not isinstance(data, list):
                raise ValueError("official release metadata must be an array")
            stable = [
                parsed for item in data
                if isinstance(item, dict) and item.get("stable") is True
                and isinstance(item.get("version"), str)
                and (parsed := version(item["version"], prefixed=True)) is not None
            ]
            if not stable:
                raise ValueError("no stable release found")
            latest = max(stable)
            report["latest_stable_in_supplied_metadata"] = display(latest)
            report["notes"].append("release metadata provenance and retrieval date require separate verification")
            if latest < MINIMUM:
                unavailable.append("supplied release metadata predates the required baseline")
            if local is not None and latest > local:
                report["notes"].append("a newer stable release is listed; no upgrade was attempted")
        except (OSError, UnicodeError, ValueError) as error:
            unavailable.append(f"release metadata unavailable: {type(error).__name__}: {error}")
    code = 2 if unavailable else (1 if findings else 0)
    report["status"] = {0: "baseline-met", 1: "baseline-violation", 2: "proof-unavailable"}[code]
    return report, code


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True, help="module root containing go.mod")
    parser.add_argument("--go", default="go", help="already installed Go executable; no installation occurs")
    parser.add_argument("--releases-json", type=Path, help="optional trusted official Go download metadata")
    args = parser.parse_args()
    report, code = check(args.project.resolve(), args.go, args.releases_json)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return code


if __name__ == "__main__":
    sys.exit(main())
