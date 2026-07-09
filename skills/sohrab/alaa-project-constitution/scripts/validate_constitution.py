#!/usr/bin/env python3
"""Validate Alaa project constitution templates and generated constitutions."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_MODULES = (
    "MONOREPO_PACKAGES_SDK_CLI",
    "UPSTREAM_KIT_FRAMEWORK_CONTRACTS",
    "API_CONTRACTS",
    "GO_CHI",
    "LARAVEL_PHP_OCTANE",
    "FRONTEND_WEB_SSR_PWA",
    "GATEWAY_PROXY_TRUST",
    "DATA_MIGRATIONS",
    "REDIS_CACHE_LOCKS",
    "ASYNC_JOBS_EVENTS",
    "REALTIME_STREAMING",
    "INTEGRATIONS_WEBHOOKS",
    "MEDIA_FILES",
    "SEARCH_INDEXING",
    "INFRA_CI_RUNTIME",
    "OBSERVABILITY_SOC",
    "DOCS_GENERATED_AGENT_GUIDANCE",
)

REQUIRED_FINAL_HEADINGS = (
    "## 1. Constitution Metadata",
    "## 2. Scope, Authority, and Conflict Resolution",
    "## 5. Universal Principles",
    "## 8. Project Validation Matrix",
    "## 10. Agent Operating Contract",
    "## 11. AGENTS.md and CLAUDE.md Binding",
    "## 12. Governance, Amendments, and Exceptions",
    "## 14. Final Ratification",
)

PLACEHOLDER_RE = re.compile(r"\{\{[A-Z0-9_]+\}\}")
SEMVER_RE = re.compile(r"(?<!\d)(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?!\d)")
TODO_RE = re.compile(
    r"TODO\([a-z0-9][a-z0-9._-]*\):\s*[^;\n]+;\s*"
    r"reason:\s*[^;\n]+;\s*owner:\s*[^;\n]+;\s*blocking:\s*(?:yes|no)\.?",
    re.IGNORECASE,
)


def strip_html_comments(text: str) -> str:
    return re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)


def first_visible_line(text: str) -> str:
    visible = strip_html_comments(text)
    for line in visible.splitlines():
        if line.strip():
            return line.strip()
    return ""


def validate_common(text: str) -> list[str]:
    errors: list[str] = []
    if not text.strip():
        errors.append("document is empty")
    if "\t" in text:
        errors.append("document contains tab characters")
    trailing = [i for i, line in enumerate(text.splitlines(), 1) if line.rstrip() != line]
    if trailing:
        errors.append(f"trailing whitespace on line(s): {', '.join(map(str, trailing[:10]))}")
    return errors


def validate_template(text: str) -> list[str]:
    errors = validate_common(text)
    required_fragments = (
        "TEMPLATE-ONLY: PROJECT CONSTITUTION GENERATION CONTRACT",
        "Phase C - Writing pass 1",
        "Phase D - Writing pass 2",
        "UPDATE / PERIODIC REVIEW RULES",
        "THIN_CHARTER",
        "FULL_CHARTER",
        "Sync Impact Report",
        "# {{PROJECT_NAME}} Constitution",
        "### 2.5 Constitutional corpus and non-duplication",
        "### 3.4 Constitution maintenance contract",
        "Binding effect: {{BINDING_NON_BINDING_OR_INACTIVE}}",
        "## 11. AGENTS.md and CLAUDE.md Binding",
        "TODO(<stable-id>)",
        "PROPOSAL(<stable-id>)",
    )
    for fragment in required_fragments:
        if fragment not in text:
            errors.append(f"missing template contract fragment: {fragment}")
    for module in REQUIRED_MODULES:
        if f"### Module {module}" not in text:
            errors.append(f"missing conditional module: {module}")
    if len(PLACEHOLDER_RE.findall(text)) < 40:
        errors.append("template has too few structured placeholders")
    visible = strip_html_comments(text)
    authored_norms = sorted(
        set(re.findall(r"\b(?:MUST(?: NOT)?|SHOULD(?: NOT)?|MAY)\b", visible))
    )
    if authored_norms:
        errors.append(
            "visible template body contains pre-authored normative policy; move it into "
            f"TEMPLATE-ONLY guidance: {', '.join(authored_norms)}"
        )
    return errors


def validate_final(text: str) -> list[str]:
    errors = validate_common(text)
    if not text.lstrip().startswith("<!--"):
        errors.append("Sync Impact Report must be the first HTML comment")
    opening_comment = re.match(r"\s*<!--(.*?)-->", text, flags=re.DOTALL)
    if not opening_comment or "Sync Impact Report" not in opening_comment.group(1):
        errors.append("first HTML comment is not a Sync Impact Report")

    first = first_visible_line(text)
    if not re.fullmatch(r"#\s+.+\s+Constitution", first):
        errors.append("first visible line must be '# <Project Name> Constitution'")

    visible = strip_html_comments(text)
    h1_count = len(re.findall(r"^#\s+", visible, flags=re.MULTILINE))
    if h1_count != 1:
        errors.append(f"expected exactly one visible H1; found {h1_count}")

    if "TEMPLATE-ONLY" in text:
        errors.append("template-only generation instructions remain")
    placeholders = sorted(set(PLACEHOLDER_RE.findall(text)))
    if placeholders:
        errors.append(f"unresolved placeholders remain: {', '.join(placeholders[:10])}")

    for heading in REQUIRED_FINAL_HEADINGS:
        if heading not in visible:
            errors.append(f"missing required heading: {heading}")

    if not SEMVER_RE.search(visible):
        errors.append("no semantic version found")
    if not re.search(r"\b(?:DRAFT|BINDING|NEEDS_REVIEW|SUPERSEDED)\b", visible):
        errors.append("no recognized constitution status found")

    status_match = re.search(
        r"\|\s*Status\s*\|\s*(DRAFT|BINDING|NEEDS_REVIEW|SUPERSEDED)\s*\|",
        visible,
        flags=re.IGNORECASE,
    )
    effect_match = re.search(
        r"\|\s*Binding effect\s*\|\s*(BINDING|NON_BINDING|INACTIVE)\s*\|",
        visible,
        flags=re.IGNORECASE,
    )
    if not status_match:
        errors.append("metadata table has no recognized Status row")
    if not effect_match:
        errors.append("metadata table has no recognized Binding effect row")
    if status_match and effect_match:
        status = status_match.group(1).upper()
        effect = effect_match.group(1).upper()
        expected = "BINDING" if status == "BINDING" else "INACTIVE" if status == "SUPERSEDED" else "NON_BINDING"
        if effect != expected:
            errors.append(
                f"status/effect mismatch: {status} requires Binding effect {expected}, found {effect}"
            )

    if not re.search(
        r"\|\s*Constitution shape\s*\|\s*(THIN_CHARTER|FULL_CHARTER)\s*\|",
        visible,
        flags=re.IGNORECASE,
    ):
        errors.append("metadata table has no THIN_CHARTER or FULL_CHARTER shape")

    bare_todos = []
    for match in re.finditer(r"\bTODO\(", visible, flags=re.IGNORECASE):
        window = visible[match.start() : match.start() + 500]
        if re.match(r"TODO\(id\)", window, flags=re.IGNORECASE):
            continue
        if not TODO_RE.match(window):
            bare_todos.append(visible.count("\n", 0, match.start()) + 1)
    if bare_todos:
        errors.append(
            "TODOs must use 'TODO(id): ...; reason: ...; owner: ...; blocking: yes|no' "
            f"near visible line(s): {', '.join(map(str, bare_todos[:10]))}"
        )

    if "@CONSTITUTION.md" not in visible:
        errors.append("CLAUDE.md binding example/import path is missing")
    return errors


def extract_markdown_section(text: str, heading: str) -> str:
    match = re.search(
        rf"(?ms)^##\s+{re.escape(heading)}\s*$.*?(?=^##\s+|\Z)",
        text,
    )
    return match.group(0) if match else ""


def validate_bindings(root: Path, constitution_text: str) -> list[str]:
    errors: list[str] = []
    visible = strip_html_comments(constitution_text)
    status_match = re.search(
        r"\|\s*Status\s*\|\s*(DRAFT|BINDING|NEEDS_REVIEW|SUPERSEDED)\s*\|",
        visible,
        flags=re.IGNORECASE,
    )
    if not status_match:
        return ["cannot validate bindings without a recognized metadata Status row"]
    status = status_match.group(1).upper()

    agents_path = root / "AGENTS.md"
    claude_path = root / "CLAUDE.md"
    for path in (agents_path, claude_path):
        if not path.is_file():
            errors.append(f"missing root binding file: {path.name}")
    if errors:
        return errors

    try:
        agents_text = agents_path.read_text(encoding="utf-8")
        claude_text = claude_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return [f"cannot read root binding files: {exc}"]

    agents_section = extract_markdown_section(agents_text, "Project Constitution")
    claude_section = extract_markdown_section(claude_text, "Constitution Binding")
    if not agents_section:
        errors.append("AGENTS.md has no '## Project Constitution' adapter")
    if "CONSTITUTION.md" not in agents_section:
        errors.append("AGENTS.md constitution adapter does not reference CONSTITUTION.md")
    if not claude_section:
        errors.append("CLAUDE.md has no '## Constitution Binding' adapter")
    if "@CONSTITUTION.md" not in claude_text:
        errors.append("CLAUDE.md does not import @CONSTITUTION.md")

    adapter_sections = {
        "AGENTS.md": agents_section.lower(),
        "CLAUDE.md": claude_section.lower(),
    }
    if status == "BINDING":
        for name, section in adapter_sections.items():
            if "binding" not in section and "canonical project policy" not in section:
                errors.append(f"{name} adapter does not state BINDING effect")
    elif status in {"DRAFT", "NEEDS_REVIEW"}:
        for name, section in adapter_sections.items():
            if "non-binding" not in section and "not binding" not in section:
                errors.append(f"{name} adapter must explicitly say {status} is non-binding")
    elif status == "SUPERSEDED":
        for name, section in adapter_sections.items():
            if "superseded" not in section and "inactive" not in section:
                errors.append(f"{name} adapter must mark SUPERSEDED constitution inactive")
    return errors


def run_self_test() -> list[str]:
    valid_final = """<!--
Sync Impact Report
Mode: CREATE
-->
# Example Project Constitution

## 1. Constitution Metadata
| Field | Value |
|---|---|
| Status | BINDING |
| Binding effect | BINDING |
| Constitution shape | FULL_CHARTER |
| Version | 1.0.0 |

## 2. Scope, Authority, and Conflict Resolution
Rules.
## 5. Universal Principles
Rules.
## 8. Project Validation Matrix
Rules.
## 10. Agent Operating Contract
Rules.
## 11. AGENTS.md and CLAUDE.md Binding
`@CONSTITUTION.md`
## 12. Governance, Amendments, and Exceptions
Rules.
## 14. Final Ratification
**Version**: 1.0.0 | **Status**: BINDING
"""
    failures: list[str] = []
    if validate_final(valid_final):
        failures.append("valid final fixture was rejected")
    if not validate_final(valid_final.replace("1.0.0", "VERSION")):
        failures.append("invalid final fixture was accepted")
    return failures


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--template", type=Path, help="validate a template file")
    mode.add_argument("--final", type=Path, help="validate a generated constitution")
    mode.add_argument("--self-test", action="store_true", help="run in-memory validator tests")
    parser.add_argument(
        "--check-bindings",
        action="store_true",
        help="with --final, validate sibling root AGENTS.md and CLAUDE.md status-aware adapters",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.check_bindings and not args.final:
        print("FAIL: --check-bindings requires --final", file=sys.stderr)
        return 2
    if args.self_test:
        errors = run_self_test()
        label = "self-test"
    else:
        path: Path = args.template or args.final
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            print(f"FAIL: cannot read {path}: {exc}", file=sys.stderr)
            return 2
        errors = validate_template(text) if args.template else validate_final(text)
        if args.final and args.check_bindings:
            errors.extend(validate_bindings(path.parent, text))
        label = str(path)

    if errors:
        print(f"FAIL: {label}")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"PASS: {label}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
