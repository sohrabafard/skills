#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACK_DIR = ROOT / "skills" / "sohrab"

PATH_RE = re.compile(r"`((?:references|docs|examples|scripts|assets|output|test|tests)/[^`]+)`")


def load_skill(skill_dir: Path):
    raw = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    m = re.match(r"^---\n([\s\S]*?)\n---\n?", raw)
    if not m:
        return None, raw
    front = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        front[key.strip()] = value.strip().strip('"')
    return front, raw[m.end():]


def main() -> int:
    errors = []
    warnings = []
    for skill_dir in sorted([p for p in PACK_DIR.iterdir() if (p / "SKILL.md").exists()]):
        front, body = load_skill(skill_dir)
        if not front:
            errors.append(f"{skill_dir.name}: missing or invalid frontmatter")
            continue
        if not front.get("name") or not front.get("description"):
            errors.append(f"{skill_dir.name}: frontmatter must include name and description")
        if "## When NOT to use" not in body and "## When NOT to Use" not in body and "## Do NOT Use" not in body:
            errors.append(f"{skill_dir.name}: missing When NOT to use section")
        lines = body.count("\n") + 1
        if lines > 120:
            warnings.append(f"{skill_dir.name}: top-level body is {lines} lines")
        for match in PATH_RE.findall(body):
            if not (skill_dir / match).exists():
                errors.append(f"{skill_dir.name}: referenced path does not exist -> {match}")
        openai_path = skill_dir / "agents" / "openai.yaml"
        if not openai_path.exists():
            errors.append(f"{skill_dir.name}: missing agents/openai.yaml")
        else:
            raw_yaml = openai_path.read_text(encoding="utf-8")
            short_m = re.search(r'short_description:\s*"([^"]+)"', raw_yaml)
            prompt_m = re.search(r'default_prompt:\s*"([^"]+)"', raw_yaml)
            short_description = short_m.group(1) if short_m else ""
            default_prompt = prompt_m.group(1) if prompt_m else ""
            if not (25 <= len(short_description) <= 64):
                errors.append(f"{skill_dir.name}: short_description must be 25-64 chars")
            if ("$" + front["name"]) not in default_prompt:
                errors.append(f"{skill_dir.name}: default_prompt must mention $" + front["name"])
        for topic_map in [skill_dir / "references" / "00-topic-map.md", skill_dir / "docs" / "00-topic-map.md"]:
            if topic_map.exists():
                topic_raw = topic_map.read_text(encoding="utf-8")
                for rel in PATH_RE.findall(topic_raw):
                    if not (skill_dir / rel).exists():
                        errors.append(f"{skill_dir.name}: topic map path missing -> {rel}")
    if errors:
        print("Errors:")
        for err in errors:
            print(f"- {err}")
    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"- {warning}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
