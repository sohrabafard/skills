#!/usr/bin/env python3
"""Lightweight validation for the tusd-upload-platform skill pack."""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except Exception as exc:
    raise SystemExit(f"PyYAML is required: {exc}")


def fail(message: str) -> None:
    raise SystemExit(f"ERROR: {message}")


def main() -> None:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    skill = root / "SKILL.md"
    if not skill.exists():
        fail("SKILL.md is missing")

    text = skill.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail("SKILL.md frontmatter is missing")
    _, fm, body = text.split("---\n", 2)
    data = yaml.safe_load(fm)
    if data.get("name") != "tusd-upload-platform":
        fail("unexpected skill name")
    if not data.get("description"):
        fail("description is missing")
    if len(data["description"]) > 1024:
        fail("description is too long")

    openai = root / "agents" / "openai.yaml"
    if not openai.exists():
        fail("agents/openai.yaml is missing")
    yaml.safe_load(openai.read_text(encoding="utf-8"))

    missing = []
    for match in re.findall(r"`((?:references|assets)/[^`]+)`", body):
        if not (root / match).exists():
            missing.append(match)
    if missing:
        fail("referenced files missing: " + ", ".join(sorted(set(missing))))

    all_text = "\n".join(
        p.read_text(encoding="utf-8", errors="ignore")
        for p in root.rglob("*")
        if p.is_file()
    )
    forbidden_image = "tusproject/tusd:" + "latest"
    if forbidden_image in all_text:
        fail("production assets must not use unpinned tusd latest image")
    legacy_header = "X-Correlation" + "-Id"
    if legacy_header in all_text:
        fail("use X-Request-Id/traceparent, not legacy correlation header")

    print(f"OK: {root}")


if __name__ == "__main__":
    main()
