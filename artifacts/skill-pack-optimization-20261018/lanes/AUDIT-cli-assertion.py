"""Reproduce the focused partitioned-FK help and empty-root output assertions."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
AUDIT = ROOT / "skills/sohrab/alaa-partitioned-table-fk-audit/scripts/partitioned_fk_audit.py"
EMPTY_ROOT = ROOT / "artifacts/skill-pack-optimization-20261018/lanes/fixtures/empty-root"


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-B", str(AUDIT), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


help_result = run(["--help"])
assert help_result.returncode == 0
assert "no parent was found in the supplied roots" in help_result.stdout
assert "it proves neither" in help_result.stdout

empty_result = run([str(EMPTY_ROOT), "--require-parents"])
assert empty_result.returncode == 4
assert "this scan does not verify guard installation or database-engine behavior." in empty_result.stdout
