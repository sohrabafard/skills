#!/usr/bin/env python3
"""Prove this skill's two checkers on committed fixtures before trusting either one.

Every assertion these scripts ship is paired here with an input that violates it. A green
checker with no red fixture is decoration: it cannot distinguish a correct artifact from a
check that silently never fired.

Exit codes, matching the contract in references/60-validation-and-output-contract.md:

  0  every case behaved as expected
  1  at least one case FAILED: the target ran and gave the wrong answer
  2  at least one case was BLOCKED, or this harness could not run

A case whose target exits 2 when 2 was not the expected code records BLOCKED rather than
FAIL, because "the checker could not run" is not evidence about the artifact. Any BLOCKED
case makes the whole run exit 2, so a CI gate never reads a broken checker as a red test.

Run it with:

    python3 scripts/selftest.py --self-test

On Windows use `py -3` instead of `python3`. The harness re-invokes the checkers with
`sys.executable`, so the interpreter that started it is the one that runs them.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

EXIT_OK = 0
EXIT_FAILED = 1
EXIT_BLOCKED = 2

SCRIPTS_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPTS_DIR.parent

VALIDATOR = "validator"
AUDITOR = "auditor"

DOC_SECTIONS = (
    "Purpose",
    "Flow position",
    "Request",
    "Response",
    "Access",
    "Errors",
    "Frontend notes",
    "Security notes",
)
# The full-strength invocation from references/60-validation-and-output-contract.md.
FULL_STRENGTH = [
    "--require-saved-responses",
    "--require-success-example",
    "--require-error-examples",
    "1",
    "--require-tests",
    "--require-correlation-assertion",
    "--require-token-capture",
    "--require-success-guarded-captures",
    "--require-secret-typing",
    "--forbid-pinned-vendor-identifier",
    "--min-description-chars",
    "400",
    *[argument for section in DOC_SECTIONS for argument in ("--require-doc-section", section)],
]

# (name, target, argv built from fixture paths, expected exit code, expected output text)
CASES: tuple[tuple[str, str, list[str], int, str], ...] = (
    (
        "validator accepts a conforming collection at full strength",
        VALIDATOR,
        ["@clean.postman_collection.json", "--env", "@clean.postman_environment.json", "--skip-schema", *FULL_STRENGTH],
        0,
        "Validation passed with no issues.",
    ),
    (
        "validator rejects a saved response attached to a different endpoint",
        VALIDATOR,
        ["@wrong-endpoint.postman_collection.json", "--skip-schema"],
        1,
        "originalRequest endpoint does not match the request endpoint",
    ),
    (
        "validator rejects a capture that writes on an error response",
        VALIDATOR,
        [
            "@unguarded-capture.postman_collection.json",
            "--env",
            "@clean.postman_environment.json",
            "--skip-schema",
            "--require-success-guarded-captures",
        ],
        1,
        "on a path an error response also reaches",
    ),
    (
        "validator rejects a collection of folders with no requests",
        VALIDATOR,
        ["@folders-only.postman_collection.json", "--env", "@clean.postman_environment.json", "--skip-schema", *FULL_STRENGTH],
        1,
        "no request items",
    ),
    (
        "validator rejects an environment that pins a vendor model identifier",
        VALIDATOR,
        [
            "@clean.postman_collection.json",
            "--env",
            "@pinned-vendor.postman_environment.json",
            "--skip-schema",
            "--forbid-pinned-vendor-identifier",
        ],
        1,
        "pins a vendor model or engine identifier",
    ),
    (
        "validator leaves the pinned identifier alone without the flag, so the flag is what gates it",
        VALIDATOR,
        ["@clean.postman_collection.json", "--env", "@pinned-vendor.postman_environment.json", "--skip-schema"],
        0,
        "Validation passed with no issues.",
    ),
    (
        "validator refuses to pass when --require-schema could not validate against the schema",
        VALIDATOR,
        ["@clean.postman_collection.json", "--env", "@clean.postman_environment.json", "--skip-schema", "--require-schema"],
        2,
        "could not run",
    ),
    (
        "validator reports a truncated collection as could-not-run, not as a finding",
        VALIDATOR,
        ["@truncated.postman_collection.json", "--skip-schema"],
        2,
        "cannot read JSON",
    ),
    (
        "auditor accepts a conforming collection",
        AUDITOR,
        [
            "--require-saved-responses",
            "--require-success-guarded-captures",
            "--min-description-chars",
            "120",
            "--environment",
            "@clean.postman_environment.json",
            "clean=@clean.postman_collection.json",
        ],
        0,
        "errors=0",
    ),
    (
        "auditor rejects a saved response attached to a different endpoint",
        AUDITOR,
        ["--min-description-chars", "0", "wrong=@wrong-endpoint.postman_collection.json"],
        1,
        "originalRequest endpoint does not match the request endpoint",
    ),
    (
        "auditor rejects a collection of folders with no requests",
        AUDITOR,
        ["--environment", "@clean.postman_environment.json", "empty=@folders-only.postman_collection.json"],
        1,
        "contains no request items",
    ),
    (
        "auditor reports a truncated collection as could-not-run, not as a finding",
        AUDITOR,
        ["--environment", "@clean.postman_environment.json", "broken=@truncated.postman_collection.json"],
        2,
        "cannot read Postman JSON",
    ),
)


def resolve(token: str, fixtures: Path) -> str:
    """Expand a `@fixture-name` token, including inside an auditor `label=@path` argument."""
    if token.startswith("@"):
        return str(fixtures / token[1:])
    if "=@" in token:
        label, name = token.split("=@", 1)
        return f"{label}={fixtures / name}"
    return token


def run_case(
    target_path: Path, argv: list[str], fixtures: Path
) -> tuple[int, str]:
    completed = subprocess.run(
        [sys.executable, str(target_path), *(resolve(token, fixtures) for token in argv)],
        capture_output=True,
        text=True,
        check=False,
    )
    return completed.returncode, completed.stdout + completed.stderr


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run this skill's checkers against their committed red and clean fixtures."
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run every fixture case. Required; without it this harness does nothing and exits 2.",
    )
    parser.add_argument(
        "--fixtures",
        type=Path,
        default=SKILL_DIR / "test" / "fixtures",
        help="Directory holding the committed fixtures",
    )
    parser.add_argument(
        "--validator",
        type=Path,
        default=SCRIPTS_DIR / "validate_postman_artifacts.py",
        help="Path to validate_postman_artifacts.py",
    )
    parser.add_argument(
        "--auditor",
        type=Path,
        default=SCRIPTS_DIR / "audit_collection_contract.py",
        help="Path to audit_collection_contract.py",
    )
    return parser


def main() -> int:
    options = build_parser().parse_args()
    if not options.self_test:
        print("ERROR: pass --self-test to run the fixture cases", file=sys.stderr)
        return EXIT_BLOCKED

    targets = {VALIDATOR: options.validator, AUDITOR: options.auditor}
    for name, path in targets.items():
        if not path.is_file():
            print(f"ERROR: cannot find the {name} at `{path}`", file=sys.stderr)
            return EXIT_BLOCKED
    if not options.fixtures.is_dir():
        print(f"ERROR: cannot find the fixture directory at `{options.fixtures}`", file=sys.stderr)
        return EXIT_BLOCKED

    failed = 0
    blocked = 0
    for name, target, argv, expected_exit, expected_text in CASES:
        code, output = run_case(targets[target], argv, options.fixtures)
        if code == expected_exit and expected_text in output:
            print(f"PASS    [{target}] {name}")
            continue
        if code == EXIT_BLOCKED and expected_exit != EXIT_BLOCKED:
            blocked += 1
            print(f"BLOCKED [{target}] {name}: the checker could not run (exit 2)")
        else:
            failed += 1
            if code != expected_exit:
                reason = f"expected exit {expected_exit}, got exit {code}"
            else:
                reason = f"exit {code} was right but the output never said {expected_text!r}"
            print(f"FAIL    [{target}] {name}: {reason}")
        for line in output.strip().splitlines():
            print(f"          {line}")

    print(f"Cases: {len(CASES)} passed={len(CASES) - failed - blocked} failed={failed} blocked={blocked}")
    if blocked:
        return EXIT_BLOCKED
    if failed:
        return EXIT_FAILED
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
