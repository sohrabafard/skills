#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACK_DIR = ROOT / "skills" / "sohrab"

PATH_RE = re.compile(r"`((?:references|docs|examples|scripts|assets|output|test|tests)/[^`]+)`")
BACKTICK_RE = re.compile(r"`([^`\n]+)`")
METRIC_RE = re.compile(r"^alaa_[a-z0-9]+(?:_[a-z0-9]+)*$")
BROKER_RE = re.compile(
    r"^(?:"
    r"[a-z][a-z0-9_]*\.events"
    r"|[a-z][a-z0-9_]*\.commands(?:\.dlx)?"
    r"|[a-z][a-z0-9_]*\.jobs\.[a-z0-9_]+"
    r"|notification\.command\.[a-z0-9_.]+"
    r"|notif\.[a-z0-9_.]+"
    r")(?:\.retry|\.dlq)?$"
)
REGISTRY_SKILL = "alaa-services-contract"
METRIC_REGISTRY = "references/24-metric-registry.md"
QUEUE_REGISTRY = "references/23-queue-and-exchange-registry.md"
LOCAL_RESOURCE_PREFIXES = ("references/", "examples/", "scripts/", "assets/")
TARGET_REPO_PREFIXES = ("docs/", "output/", "test/", "tests/")


def is_placeholder_or_glob(path: str) -> bool:
    return any(token in path for token in ("*", "?", "[", "]", "<", ">"))


def is_command_example(path: str) -> bool:
    return any(char.isspace() for char in path)


def should_validate_path(skill_dir: Path, path: str) -> bool:
    """Return true only for bundled skill resource paths.

    Skill docs often mention target-repository paths such as
    `docs/BIG_PICTURE.md` or command placeholders such as
    `scripts/validate_makefile.sh <file>`. Those are not bundled resources and
    should not fail pack validation.
    """
    normalized = path.replace("\\", "/").strip()

    if is_placeholder_or_glob(normalized) or is_command_example(normalized):
        return False

    if normalized.endswith("/"):
        return False

    for prefix in LOCAL_RESOURCE_PREFIXES:
        if normalized.startswith(prefix):
            return (skill_dir / prefix.rstrip("/")).exists()

    if normalized.startswith("docs/"):
        return (skill_dir / "docs").exists()

    if normalized.startswith(TARGET_REPO_PREFIXES):
        return False

    return True


# Plugin validation rejects a description over this length. It is stricter than the
# 1536-character listing cap documented for Claude Code, so this is the binding number.
DESCRIPTION_HARD_MAX = 1024
# Author target, leaving headroom so adding one clause later does not fail the build.
DESCRIPTION_TARGET_MAX = 950


SKILL_NAME_RE = re.compile(r"[/$]?\b((?:alaa|golang|caas|ansible|clickhouse|jitsi|service|tusd|vector|playwright|openfga|openai)[a-z0-9-]*)\b")


def local_reference_paths(skill_dir: Path, text: str):
    """Yield bundled-resource paths that this skill owns.

    A cross-skill pointer names the owning skill on the same line before the path —
    `alaa-services-contract` `references/22-...md`. Resolving such a path inside the
    citing skill is wrong, so the line is skipped once another skill is named on it.
    """
    own = skill_dir.name
    for line in text.splitlines():
        paths = PATH_RE.findall(line)
        if not paths:
            continue
        named = {n for n in SKILL_NAME_RE.findall(line) if n != own and (skill_dir.parent / n).is_dir()}
        if named:
            continue
        for path in paths:
            if should_validate_path(skill_dir, path):
                yield path


def check_registries(skill_dir: Path) -> list[str]:
    """Fail when this skill names a metric, exchange, or queue it never registered.

    A registry nothing checks goes stale. This proves one half: no reference file
    in alaa-services-contract may name an `alaa_*` metric absent from
    references/24-metric-registry.md, or a broker exchange or queue absent from
    references/23-queue-and-exchange-registry.md. The other half - that a service
    repository emits only registered names - cannot be checked from here and is
    stated as such in 24-metric-registry.md.
    """
    errors: list[str] = []
    refs = skill_dir / "references"
    if not refs.is_dir():
        return errors

    registries = {}
    for rel in (METRIC_REGISTRY, QUEUE_REGISTRY):
        path = skill_dir / rel
        if not path.exists():
            errors.append(f"{skill_dir.name}: registry file missing -> {rel}")
            return errors
        registries[rel] = path.read_text(encoding="utf-8")

    for md in sorted(refs.glob("*.md")):
        rel_name = f"references/{md.name}"
        text = md.read_text(encoding="utf-8")
        for token in BACKTICK_RE.findall(text):
            token = token.strip()
            if any(ch in token for ch in "<>*?[]/ \t"):
                continue
            if METRIC_RE.match(token):
                target = METRIC_REGISTRY
            elif BROKER_RE.match(token):
                target = QUEUE_REGISTRY
            else:
                continue
            if rel_name == target:
                continue
            if f"`{token}`" not in registries[target]:
                errors.append(
                    f"{skill_dir.name}: {rel_name} names `{token}` "
                    f"with no row in {target}"
                )
    return sorted(set(errors))


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
        else:
            # Plugin validation rejects a description over 1024 characters outright, which is a
            # harder limit than the 1536-character listing cap in the Claude Code docs. Measure the
            # collapsed single-line form, because a folded YAML scalar is counted that way.
            desc_len = len(" ".join(str(front["description"]).split()))
            if desc_len > DESCRIPTION_HARD_MAX:
                errors.append(
                    f"{skill_dir.name}: description is {desc_len} chars, over the "
                    f"{DESCRIPTION_HARD_MAX}-char plugin-validation limit"
                )
            elif desc_len > DESCRIPTION_TARGET_MAX:
                warnings.append(
                    f"{skill_dir.name}: description is {desc_len} chars, within "
                    f"{DESCRIPTION_HARD_MAX - desc_len} of the {DESCRIPTION_HARD_MAX}-char limit; "
                    f"keep it at or under {DESCRIPTION_TARGET_MAX} so one added clause cannot break the build"
                )
        # Accept any casing and either phrasing. The rule is that the body states a negative
        # scope somewhere; forcing one exact spelling only produced false failures.
        if not re.search(r"^#+\s+.*\b(when\s+not\s+to\s+use|do\s+not\s+use)\b", body, re.I | re.M):
            errors.append(f"{skill_dir.name}: missing a 'When not to use' or 'Do not use' section")
        lines = body.count("\n") + 1
        if lines > 120:
            warnings.append(f"{skill_dir.name}: top-level body is {lines} lines")
        for match in local_reference_paths(skill_dir, body):
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
        if skill_dir.name == REGISTRY_SKILL:
            errors.extend(check_registries(skill_dir))
        for topic_map in [skill_dir / "references" / "00-topic-map.md", skill_dir / "docs" / "00-topic-map.md"]:
            if topic_map.exists():
                topic_raw = topic_map.read_text(encoding="utf-8")
                for rel in local_reference_paths(skill_dir, topic_raw):
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
