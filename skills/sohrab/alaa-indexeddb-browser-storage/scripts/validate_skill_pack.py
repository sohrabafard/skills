#!/usr/bin/env python3
"""Validate the pack's structure, trigger syntax, boundaries, and budget templates.

Exit codes
  0  clean.
  1  findings, each with file and line. Resolve every one before reporting complete.
  2  could not run: the root or a required file is missing or unreadable. Never a pass.

Checks, and why each exists:
  * required files exist and are non-empty
  * the frontmatter description is under 1024 characters (a hard validator limit) and
    carries a "Do not use" clause -- a description that is all "use when" fires on
    every neighbouring skill's tasks
  * no model name is pinned anywhere: model and effort route to /alaa-prompting-guide
  * every `$alaa-x` occurrence has a `/alaa-x` sibling on the same line, except in
    agents/openai.yaml which is Codex-only and stays `$`-form
  * no forbidden value is written to storage anywhere in the pack, not only in
    examples/ -- the previous version scanned examples/*.ts and three localStorage
    regexes, which the actual risk (an IndexedDB write) evaded entirely
  * no example persists or decodes a permission bitmap
  * the data-classification YAML and the reference table agree on the class set
  * a filled budget policy has no unfilled placeholders
  * skill-pack-manifest.json matches the filesystem
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from pathlib import Path

EXIT_CLEAN, EXIT_FINDINGS, EXIT_CANNOT_RUN = 0, 1, 2

SKILL_NAME = "alaa-indexeddb-browser-storage"
REQUIRED = [
    "SKILL.md",
    "agents/openai.yaml",
    "skill-pack-manifest.json",
    "references/00-topic-map.md",
    "references/99-sources-and-maintenance.md",
    "assets/data-classification-policy.yaml",
    "assets/capability-tier-contract.json",
    "assets/browser-test-matrix.yaml",
]
SCANNED_SUFFIXES = {".md", ".ts", ".yaml", ".json", ".py"}

MODEL_PIN = re.compile(r"\b(gpt-[0-9]|claude-[0-9a-z]*-?[0-9]|o[0-9]-(mini|preview)|sonnet|opus|haiku)\b", re.I)
DOLLAR_TRIGGER = re.compile(r"\$(alaa-[a-z0-9-]+)")
SLASH_TRIGGER = re.compile(r"/(alaa-[a-z0-9-]+)")

# The real risk in this domain is a token reaching IndexedDB, which no localStorage
# pattern covers. These match the write, not one spelling of the variable name.
FORBIDDEN_WRITES = [
    (re.compile(r"\.put\(\s*\{[^}]*\b(access|refresh|session|bearer)_?[Tt]oken\b", re.S), "a token written to an object store"),
    (re.compile(r"\.(put|add)\([^)]*\bjwt\b", re.I), "a JWT written to an object store"),
    (re.compile(r"localStorage\.setItem\([^)]*\btoken\b", re.I), "a token written to localStorage"),
    (re.compile(r"\b(decodePermission|decodeBitmap|parsePermissionBitmap)\s*\(", re.I), "a permission bitmap decoded in storage code"),
    (re.compile(r"\.(put|add)\([^)]*\bpermissionBitmap\b", re.I), "a permission bitmap persisted"),
    (re.compile(r"\.(put|add)\([^)]*\bX-(Access|User-Id|Project-Id|Authz)\b", re.I), "a trusted gateway header persisted"),
]

PLACEHOLDER = re.compile(r"<[a-z][^>]*>")
# Built from code points so this file does not trip its own check.
ARABIC_SCRIPT = re.compile("[" + chr(0x0600) + "-" + chr(0x06FF) + chr(0x0750) + "-" + chr(0x077F) + "]")

EXPECTED_CLASSES = {
    "public_cache",
    "user_private_low_risk",
    "user_generated_unsynced",
    "analytics_outbox",
    "pii_moderate_high",
    "secret_or_credential",
    "trusted_gateway_context",
    "authorization_truth",
}


def scan(root: Path, check_budgets: bool) -> list[str]:
    findings: list[str] = []

    for rel in REQUIRED:
        path = root / rel
        if not path.exists():
            findings.append(f"{rel}: missing required file")
        elif path.stat().st_size == 0:
            findings.append(f"{rel}: required file is empty")
    if findings:
        return findings

    skill = (root / "SKILL.md").read_text(encoding="utf-8")
    if not skill.startswith("---\n"):
        findings.append("SKILL.md:1: must start with YAML frontmatter")
    if f"name: {SKILL_NAME}" not in skill:
        findings.append(f"SKILL.md: name must be {SKILL_NAME}")

    description = re.search(r'^description:\s*"(.*?)"\s*$', skill, re.M | re.S)
    if not description:
        findings.append("SKILL.md: description missing or not a double-quoted scalar")
    else:
        text = description.group(1)
        if len(text) >= 1024:
            findings.append(f"SKILL.md: description is {len(text)} characters; the hard limit is 1024")
        if not re.search(r"\bDo not use\b", text):
            findings.append("SKILL.md: description has no 'Do not use ... which is /owner' clause")

    body = skill.split("---", 2)[2] if skill.count("---") >= 2 else skill
    if len(body.encode("utf-8")) > 8900:
        findings.append(f"SKILL.md: body is {len(body.encode('utf-8'))} bytes net of frontmatter; ceiling is 8900")

    for path in sorted(p for p in root.rglob("*") if p.is_file() and p.suffix in SCANNED_SUFFIXES):
        rel = path.relative_to(root).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as error:
            findings.append(f"{rel}: unreadable ({error})")
            continue

        if not text.strip():
            findings.append(f"{rel}: file is empty")
            continue

        lines = text.splitlines()
        for lineno, line in enumerate(lines, start=1):
            if rel != "scripts/validate_skill_pack.py" and MODEL_PIN.search(line):
                findings.append(
                    f"{rel}:{lineno}: a model name is pinned; model and effort route to "
                    "/alaa-prompting-guide ($alaa-prompting-guide)"
                )

            # agents/openai.yaml is Codex-only and stays $-form by design.
            # The `/x` (`$x`) pair legitimately wraps at the right margin, so the
            # call site is a two-line window, not a single line.
            if rel != "agents/openai.yaml" and not rel.startswith("scripts/"):
                window = line if lineno == 1 else lines[lineno - 2] + " " + line
                if lineno < len(lines):
                    window += " " + lines[lineno]
                for name in DOLLAR_TRIGGER.findall(line):
                    if name not in SLASH_TRIGGER.findall(window):
                        findings.append(
                            f"{rel}:{lineno}: `${name}` has no `/{name}` sibling at the same call site"
                        )

            if path.suffix in {".ts", ".md", ".yaml", ".json"}:
                for pattern, why in FORBIDDEN_WRITES:
                    # A rule that names the prohibition is not a violation of it.
                    if pattern.search(line) and "never" not in line.lower() and "not " not in line.lower():
                        findings.append(f"{rel}:{lineno}: {why}")

        if rel != "scripts/validate_skill_pack.py" and ARABIC_SCRIPT.search(text):
            findings.append(f"{rel}: contains non-ASCII Arabic-script text; every artifact is English")

    classification = (root / "assets/data-classification-policy.yaml").read_text(encoding="utf-8")
    declared = set(re.findall(r"^  ([a-z_]+):$", classification, re.M))
    missing = EXPECTED_CLASSES - declared
    extra = declared - EXPECTED_CLASSES
    if missing:
        findings.append(f"assets/data-classification-policy.yaml: missing class(es) {sorted(missing)}")
    if extra:
        findings.append(f"assets/data-classification-policy.yaml: undeclared class(es) {sorted(extra)}")
    for name in sorted(EXPECTED_CLASSES):
        if name not in (root / "references/60-data-classification.md").read_text(encoding="utf-8"):
            findings.append(f"references/60-data-classification.md: class `{name}` is in the YAML and not the table")

    if check_budgets:
        for path in sorted(root.rglob("storage-budget-policy*.md")):
            rel = path.relative_to(root).as_posix()
            if path.name == "storage-budget-policy-template.md":
                continue  # the template is expected to carry placeholders
            for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
                if PLACEHOLDER.search(line):
                    findings.append(f"{rel}:{lineno}: unfilled placeholder; a blank cap is not a default")

    manifest_path = root / "skill-pack-manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        findings.append(f"skill-pack-manifest.json: invalid JSON ({error})")
    else:
        listed = set(manifest.get("root_files", []))
        actual = {
            p.relative_to(root).as_posix()
            for p in root.rglob("*")
            if p.is_file() and not p.name.startswith(".") and "__pycache__" not in p.parts
        }
        for rel in sorted(listed - actual):
            findings.append(f"skill-pack-manifest.json: lists `{rel}`, which does not exist")
        for rel in sorted(actual - listed):
            findings.append(f"skill-pack-manifest.json: does not list `{rel}`")

    return findings


def self_test() -> int:
    """Prove each check fails when it should."""
    cases = 0
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "references").mkdir()
        (root / "assets").mkdir()
        (root / "agents").mkdir()
        (root / "examples").mkdir()

        (root / "SKILL.md").write_text(
            "---\n"
            f"name: {SKILL_NAME}\n"
            'description: "Use it for storage."\n'
            "---\n\n"
            "Pair with $alaa-reliability-sla.\n"
            "Aligned to the gpt-5 prompting guide.\n",
            encoding="utf-8",
        )
        (root / "agents/openai.yaml").write_text("default_prompt: Use $alaa-x\n", encoding="utf-8")
        (root / "skill-pack-manifest.json").write_text('{"root_files": ["SKILL.md"]}', encoding="utf-8")
        (root / "references/00-topic-map.md").write_text("router\n", encoding="utf-8")
        (root / "references/99-sources-and-maintenance.md").write_text("sources\n", encoding="utf-8")
        (root / "references/60-data-classification.md").write_text("table\n", encoding="utf-8")
        (root / "assets/data-classification-policy.yaml").write_text("classes:\n  public_cache:\n", encoding="utf-8")
        (root / "assets/capability-tier-contract.json").write_text("{}", encoding="utf-8")
        (root / "assets/browser-test-matrix.yaml").write_text("lanes: []\n", encoding="utf-8")
        (root / "examples/bad.ts").write_text(
            "store.put({ id: 'a', accessToken: token });\n", encoding="utf-8"
        )

        findings = scan(root, check_budgets=False)
        for needle, label in [
            ("no 'Do not use", "missing do-not-use clause"),
            ("model name is pinned", "model pin"),
            ("has no `/alaa-reliability-sla` sibling", "dollar-only trigger"),
            ("token written to an object store", "token written to IndexedDB"),
            ("missing class(es)", "classification drift"),
            ("does not list", "manifest drift"),
        ]:
            if not any(needle in f for f in findings):
                print(f"SELF-TEST FAIL: did not report {label}", file=sys.stderr)
                print("\n".join(findings), file=sys.stderr)
                return EXIT_FINDINGS
            cases += 1

    print(f"SELF-TEST OK: {cases} checks each fail on a fixture that violates them")
    return EXIT_CLEAN


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="validate_skill_pack.py",
        description="Validate pack structure, trigger syntax, storage boundaries, and budgets.",
        epilog="Exit 0 clean, 1 findings, 2 could not run. Exit 2 is never a pass.",
    )
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--self-test", action="store_true", help="run the built-in fixtures")
    parser.add_argument("--check-budgets", action="store_true", help="reject unfilled budget policies")
    args = parser.parse_args()

    if args.self_test:
        return self_test()

    root: Path = args.root.resolve()
    if not root.is_dir() or not (root / "SKILL.md").is_file():
        print(f"CANNOT RUN: {root} is not a skill pack root", file=sys.stderr)
        return EXIT_CANNOT_RUN

    try:
        findings = scan(root, args.check_budgets)
    except OSError as error:
        print(f"CANNOT RUN: {error}", file=sys.stderr)
        return EXIT_CANNOT_RUN

    if findings:
        for finding in findings:
            print(f"FINDING: {finding}", file=sys.stderr)
        print(f"{len(findings)} finding(s)", file=sys.stderr)
        return EXIT_FINDINGS

    print("OK: structure, description, triggers, storage boundaries, classification and manifest all validate")
    return EXIT_CLEAN


if __name__ == "__main__":
    raise SystemExit(main())
