#!/usr/bin/env python3
"""Validate Alaa project constitution templates and generated constitutions."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_MODULES = (
    "MONOREPO_PACKAGES_SDK_CLI",
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
        "Sync Impact Report",
        "# {{PROJECT_NAME}} Constitution",
        "### 3.4 Constitution maintenance contract",
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
    return parser.parse_args()


def main() -> int:
    args = parse_args()
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
