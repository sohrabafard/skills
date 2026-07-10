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
    "## Authority and Scope",
    "## Core Principles",
    "## Canonical Sources",
    "## Change Governance",
    "## Amendments and Exceptions",
)

FORBIDDEN_FINAL_PATTERNS = (
    (r"Sync Impact Report", "Sync Impact Report"),
    (r"Constitution Metadata", "Constitution Metadata"),
    (r"Evidence Ledger", "evidence ledger"),
    (r"Conditional Project Modules", "module inventory"),
    (r"Project Validation Matrix", "validation matrix"),
    (r"Agent Operating Contract", "agent operating tutorial"),
    (r"AGENTS\.md and CLAUDE\.md Binding", "binding section"),
    (r"Final Ratification", "finalization narrative"),
    (r"Finalization and binding next step", "finalization narrative"),
    (r"@CONSTITUTION\.md", "runtime import syntax"),
    (r"Owner decision state\s*:", "owner-decision telemetry"),
    (r"Finalization outcome\s*:", "finalization telemetry"),
    (r"Binding effect\s*:", "binding telemetry"),
    (r"Template used\s*:", "template telemetry"),
    (r"Validation performed\s*:", "validation telemetry"),
)

PLACEHOLDER_RE = re.compile(r"\{\{[A-Z0-9_]+\}\}")
SEMVER_PATTERN = r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)"
FOOTER_RE = re.compile(
    rf"^\*\*Version\*\*:\s*(?P<version>{SEMVER_PATTERN})\s*\|\s*"
    r"\*\*Status\*\*:\s*(?P<status>DRAFT|BINDING|NEEDS_REVIEW|SUPERSEDED)\s*\|\s*"
    r"\*\*Ratified\*\*:\s*(?P<ratified>[^|\n]+?)\s*\|\s*"
    r"\*\*Last Amended\*\*:\s*(?P<amended>[^|\n]+?)\s*\|\s*"
    r"\*\*Last Evidence Review\*\*:\s*(?P<reviewed>[^|\n]+?)\s*$",
    re.IGNORECASE | re.MULTILINE,
)
TODO_RE = re.compile(
    r"TODO\([a-z0-9][a-z0-9._-]*\):\s*[^;\n]+;\s*"
    r"reason:\s*[^;\n]+;\s*owner:\s*[^;\n]+;\s*blocking:\s*(?:yes|no)\.?",
    re.IGNORECASE,
)

THIN_MAX_BYTES = 12 * 1024
THIN_MAX_LINES = 160
FULL_MAX_BYTES = 24 * 1024
FULL_MAX_LINES = 280
ADAPTER_MAX_BYTES = 1536
AGENTS_ADAPTER_START_MAX_BYTES = 8 * 1024
CLAUDE_IMPORT_MAX_LINE = 20
CODEX_DEFAULT_PROJECT_DOC_BUDGET = 32 * 1024
CLAUDE_GUIDANCE_LINE_WARNING = 200
COMMAND_PREFIX_RE = re.compile(
    r"^(?:go|make|npm|pnpm|yarn|python|php|composer|docker|kubectl|helm|terraform|"
    r"git|bash|sh|node|cargo|dotnet|pytest|mvn|gradle|\.[/\\])(?:\s|$)",
    re.IGNORECASE,
)
BACKTICK = chr(96)


def strip_html_comments(text: str) -> str:
    return re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)


def first_visible_line(text: str) -> str:
    for line in strip_html_comments(text).splitlines():
        if line.strip():
            return line.strip()
    return ""


def footer_match(text: str) -> re.Match[str] | None:
    matches = list(FOOTER_RE.finditer(text))
    return matches[-1] if matches else None


def duplicate_exact_commands(text: str) -> list[str]:
    candidates: list[str] = []
    for match in re.finditer(rf"{BACKTICK}([^{BACKTICK}\r\n]+){BACKTICK}", text):
        value = " ".join(match.group(1).split())
        if COMMAND_PREFIX_RE.match(value):
            candidates.append(value)

    in_fence = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith(BACKTICK * 3):
            in_fence = not in_fence
            continue
        if in_fence:
            value = " ".join(stripped.split())
            if COMMAND_PREFIX_RE.match(value):
                candidates.append(value)

    counts: dict[str, int] = {}
    for candidate in candidates:
        counts[candidate] = counts.get(candidate, 0) + 1
    return sorted(command for command, count in counts.items() if count > 1)


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
        "FINAL DOCUMENT IS LAW, NOT AUTHORING TELEMETRY",
        "FINAL CONSTITUTIONAL COMPRESSION PASS",
        "MINIMUM FINAL STRUCTURE",
        "# {{PROJECT_NAME}} Constitution",
        "## Authority and Scope",
        "## Core Principles",
        "## Canonical Sources",
        "## Change Governance",
        "## Amendments and Exceptions",
        "**Version**: {{SEMVER}}",
        "Constitution Metadata table",
        "AGENTS.md/CLAUDE.md binding instructions",
        "12 KiB and 160 physical lines",
    )
    for fragment in required_fragments:
        if fragment not in text:
            errors.append(f"missing template contract fragment: {fragment}")
    for module in REQUIRED_MODULES:
        if f"- {module}" not in text:
            errors.append(f"missing conditional module prompt: {module}")
    if len(PLACEHOLDER_RE.findall(text)) < 10:
        errors.append("template has too few structured placeholders")

    visible = strip_html_comments(text)
    old_headings = (
        "## 1. Constitution Metadata",
        "## 7. Conditional Project Modules",
        "## 8. Project Validation Matrix",
        "## 10. Agent Operating Contract",
        "## 11. AGENTS.md and CLAUDE.md Binding",
        "## 14. Final Ratification",
    )
    for heading in old_headings:
        if heading in visible:
            errors.append(f"visible template retains authoring-oriented heading: {heading}")
    authored_norms = sorted(
        set(re.findall(r"\b(?:MUST(?: NOT)?|SHOULD(?: NOT)?|MAY)\b", visible))
    )
    if authored_norms:
        errors.append(
            "visible template body contains pre-authored normative policy; keep policy in "
            f"placeholders: {', '.join(authored_norms)}"
        )
    return errors


def validate_final(text: str, shape: str = "thin") -> list[str]:
    errors = validate_common(text)
    if "<!--" in text or "-->" in text:
        errors.append("final constitution contains HTML comments; keep authoring notes outside the file")

    first = first_visible_line(text)
    if not re.fullmatch(r"#\s+.+\s+Constitution", first):
        errors.append("first visible line must be '# <Project Name> Constitution'")

    h1_count = len(re.findall(r"^#\s+", text, flags=re.MULTILINE))
    if h1_count != 1:
        errors.append(f"expected exactly one H1; found {h1_count}")

    if "TEMPLATE-ONLY" in text:
        errors.append("template-only generation instructions remain")
    placeholders = sorted(set(PLACEHOLDER_RE.findall(text)))
    if placeholders:
        errors.append(f"unresolved placeholders remain: {', '.join(placeholders[:10])}")

    for heading in REQUIRED_FINAL_HEADINGS:
        if heading not in text:
            errors.append(f"missing required constitutional heading: {heading}")

    for pattern, label in FORBIDDEN_FINAL_PATTERNS:
        if re.search(pattern, text, flags=re.IGNORECASE):
            errors.append(f"authoring/runtime residue remains in final constitution: {label}")

    match = footer_match(text)
    if not match:
        errors.append("missing canonical version/status/date footer")
        status = None
    else:
        status = match.group("status").upper()
        last_nonempty = next((line.strip() for line in reversed(text.splitlines()) if line.strip()), "")
        if last_nonempty != match.group(0).strip():
            errors.append("canonical version/status/date footer must be the last non-empty line")
        ratified = match.group("ratified").strip().lower()
        if status == "BINDING":
            if ratified in {"not ratified", "none", "n/a", "na", "unknown"} or "todo" in ratified:
                errors.append("BINDING status requires a ratification date in the footer")
            elif not re.fullmatch(r"\d{4}-\d{2}-\d{2}", match.group("ratified").strip()):
                errors.append("BINDING ratification footer value must use YYYY-MM-DD")
            if re.search(r"blocking:\s*yes", text, flags=re.IGNORECASE):
                errors.append("BINDING status cannot contain a blocking unresolved TODO")
        elif status in {"DRAFT", "NEEDS_REVIEW"}:
            if not re.search(r"TODO\([^\n]+blocking:\s*yes", text, flags=re.IGNORECASE):
                errors.append(f"{status} status requires a blocking structured TODO")

    byte_count = len(text.encode("utf-8"))
    line_count = len(text.splitlines())
    max_bytes, max_lines = (
        (THIN_MAX_BYTES, THIN_MAX_LINES)
        if shape == "thin"
        else (FULL_MAX_BYTES, FULL_MAX_LINES)
    )
    if byte_count > max_bytes or line_count > max_lines:
        errors.append(
            f"{shape.upper()} constitution exceeds compactness budget: "
            f"{byte_count} bytes/{line_count} lines; maximum is {max_bytes} bytes/{max_lines} lines"
        )

    duplicate_commands = duplicate_exact_commands(text)
    if duplicate_commands:
        errors.append(
            "exact validation commands are repeated; delegate command catalogs to their "
            f"canonical owner: {', '.join(duplicate_commands[:5])}"
        )

    bare_todos = []
    for todo_match in re.finditer(r"\bTODO\(", text, flags=re.IGNORECASE):
        window = text[todo_match.start() : todo_match.start() + 500]
        if re.match(r"TODO\(id\)", window, flags=re.IGNORECASE):
            continue
        if not TODO_RE.match(window):
            bare_todos.append(text.count("\n", 0, todo_match.start()) + 1)
    if bare_todos:
        errors.append(
            "TODOs must use 'TODO(id): ...; reason: ...; owner: ...; blocking: yes|no' "
            f"near line(s): {', '.join(map(str, bare_todos[:10]))}"
        )
    return errors


def extract_markdown_section(text: str, heading: str) -> str:
    match = re.search(
        rf"(?ms)^##\s+{re.escape(heading)}\s*$.*?(?=^##\s+|\Z)",
        text,
    )
    return match.group(0) if match else ""


def validate_bindings(root: Path, constitution_text: str) -> list[str]:
    errors: list[str] = []
    match = footer_match(constitution_text)
    if not match:
        return ["cannot validate bindings without the canonical status footer"]
    status = match.group("status").upper()

    agents_path = root / "AGENTS.md"
    claude_path = root / "CLAUDE.md"
    if status == "BINDING":
        for path in (agents_path, claude_path):
            if not path.is_file():
                errors.append(f"missing root binding file: {path.name}")
        if errors:
            return errors

    try:
        agents_text = agents_path.read_text(encoding="utf-8") if agents_path.is_file() else ""
        claude_text = claude_path.read_text(encoding="utf-8") if claude_path.is_file() else ""
    except (OSError, UnicodeError) as exc:
        return [f"cannot read root binding files: {exc}"]

    agents_section = extract_markdown_section(agents_text, "Project Constitution")
    claude_section = extract_markdown_section(claude_text, "Constitution Binding")

    if status in {"DRAFT", "NEEDS_REVIEW"}:
        if "CONSTITUTION.md" in agents_text:
            errors.append(f"{status} constitution must not be activated by AGENTS.md")
        if claude_section or "@CONSTITUTION.md" in claude_text:
            errors.append(f"{status} constitution must not be imported or bound by CLAUDE.md")
        return errors

    if not agents_section:
        errors.append("AGENTS.md has no '## Project Constitution' adapter")
    if "CONSTITUTION.md" not in agents_section:
        errors.append("AGENTS.md constitution adapter does not reference CONSTITUTION.md")
    if agents_section:
        section_start = agents_text.find(agents_section)
        if len(agents_text[:section_start].encode("utf-8")) > AGENTS_ADAPTER_START_MAX_BYTES:
            errors.append("AGENTS.md constitution adapter must begin within the first 8 KiB")
        if len(agents_section.encode("utf-8")) > ADAPTER_MAX_BYTES:
            errors.append("AGENTS.md constitution adapter exceeds 1.5 KiB")

    if not claude_section:
        errors.append("CLAUDE.md has no '## Constitution Binding' adapter")
    if "@CONSTITUTION.md" not in claude_text:
        errors.append("CLAUDE.md does not import @CONSTITUTION.md")
    else:
        import_line = next(
            (i for i, line in enumerate(claude_text.splitlines(), 1) if "@CONSTITUTION.md" in line),
            None,
        )
        if import_line and import_line > CLAUDE_IMPORT_MAX_LINE:
            errors.append("CLAUDE.md @CONSTITUTION.md import must appear within the first 20 lines")
    if claude_section and len(claude_section.encode("utf-8")) > ADAPTER_MAX_BYTES:
        errors.append("CLAUDE.md constitution adapter exceeds 1.5 KiB")

    adapter_sections = {
        "AGENTS.md": agents_section.lower(),
        "CLAUDE.md": claude_section.lower(),
    }
    if status == "BINDING":
        for name, section in adapter_sections.items():
            if "non-binding" in section or "not binding" in section:
                errors.append(f"{name} adapter incorrectly marks BINDING policy non-binding")
            elif "binding" not in section and "canonical project policy" not in section:
                errors.append(f"{name} adapter does not state BINDING effect")
    elif status == "SUPERSEDED":
        for name, section in adapter_sections.items():
            if "superseded" not in section and "inactive" not in section:
                errors.append(f"{name} adapter must mark SUPERSEDED constitution inactive")
    return errors


def binding_portability_warnings(root: Path) -> list[str]:
    warnings: list[str] = []
    agents_path = root / "AGENTS.md"
    claude_path = root / "CLAUDE.md"
    try:
        if agents_path.is_file():
            size = len(agents_path.read_bytes())
            if size > CODEX_DEFAULT_PROJECT_DOC_BUDGET:
                warnings.append(
                    f"AGENTS.md is {size} bytes; this alone exceeds Codex's common 32 KiB "
                    "project-instruction budget and may be truncated on default installations"
                )
        if claude_path.is_file():
            claude_text = claude_path.read_text(encoding="utf-8")
            lines = len(claude_text.splitlines())
            if lines > CLAUDE_GUIDANCE_LINE_WARNING:
                warnings.append(
                    f"CLAUDE.md is {lines} lines; review startup-context concision and imports"
                )
    except (OSError, UnicodeError) as exc:
        warnings.append(f"could not complete binding portability audit: {exc}")
    return warnings


def run_self_test() -> list[str]:
    valid_final = """# Example Project Constitution

This constitution protects the project's durable boundaries.

## Authority and Scope

Repository policy applies within project scope.

## Core Principles

### 1. Evidence

Current truth is inspected before claims are made.

## Canonical Sources

- CONTRACTS.md owns contracts.

## Change Governance

Risk determines proof and approval.

## Amendments and Exceptions

Amendments use semantic versioning; exceptions are bounded.

**Version**: 1.0.0 | **Status**: BINDING | **Ratified**: 2026-07-10 | **Last Amended**: 2026-07-10 | **Last Evidence Review**: 2026-07-10
"""
    failures: list[str] = []
    if validate_final(valid_final, "thin"):
        failures.append("valid final fixture was rejected")
    if not validate_final(valid_final.replace("1.0.0", "VERSION"), "thin"):
        failures.append("invalid semantic version was accepted")
    if not validate_final(
        valid_final.replace(
            "## Authority and Scope",
            "## Constitution Metadata\n\n| Field | Value |\n|---|---|\n| Status | BINDING |\n\n## Authority and Scope",
        ),
        "thin",
    ):
        failures.append("metadata table residue was accepted")
    if not validate_final(
        valid_final.replace(
            "## Amendments and Exceptions",
            "## AGENTS.md and CLAUDE.md Binding\n\nRuntime adapter.\n\n## Amendments and Exceptions",
        ),
        "thin",
    ):
        failures.append("binding section residue was accepted")
    oversized = valid_final.replace(
        "**Version**:",
        ("Constitutional sentence.\n" * 200) + "\n**Version**:",
    )
    if not validate_final(oversized, "thin"):
        failures.append("oversized thin constitution was accepted")
    duplicated_command = valid_final.replace(
        "## Amendments and Exceptions",
        "`go test ./...` and again `go test ./...`\n\n## Amendments and Exceptions",
    )
    if not validate_final(duplicated_command, "thin"):
        failures.append("duplicated exact command was accepted")
    blocking_binding = valid_final.replace(
        "## Amendments and Exceptions",
        "TODO(owner-choice): decide scope; reason: owner input missing; owner: owner; "
        "blocking: yes.\n\n## Amendments and Exceptions",
    )
    if not validate_final(blocking_binding, "thin"):
        failures.append("binding fixture with blocking TODO was accepted")

    valid_draft = valid_final.replace(
        "## Amendments and Exceptions",
        "## Unresolved Decisions\n\nTODO(owner-choice): decide scope; reason: owner deferred; "
        "owner: repository owner; blocking: yes.\n\n## Amendments and Exceptions",
    ).replace(
        "**Status**: BINDING",
        "**Status**: DRAFT",
    ).replace(
        "**Ratified**: 2026-07-10",
        "**Ratified**: Not ratified",
    ).replace(
        "**Version**: 1.0.0",
        "**Version**: 0.1.0",
    )
    if validate_final(valid_draft, "thin"):
        failures.append("valid draft fixture was rejected")
    if not validate_final(valid_draft + "\n@CONSTITUTION.md\n", "thin"):
        failures.append("draft fixture with runtime import residue was accepted")
    return failures


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--template", type=Path, help="validate a template file")
    mode.add_argument("--final", type=Path, help="validate a generated constitution")
    mode.add_argument("--self-test", action="store_true", help="run in-memory validator tests")
    parser.add_argument(
        "--shape",
        choices=("thin", "full"),
        default="thin",
        help="final constitution shape; controls compactness budget",
    )
    parser.add_argument(
        "--check-bindings",
        action="store_true",
        help="with --final, validate sibling root AGENTS.md and CLAUDE.md adapters",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    warnings: list[str] = []
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
        errors = validate_template(text) if args.template else validate_final(text, args.shape)
        if args.final and args.check_bindings:
            errors.extend(validate_bindings(path.parent, text))
            warnings.extend(binding_portability_warnings(path.parent))
        label = str(path)

    if errors:
        print(f"FAIL: {label}")
        for error in errors:
            print(f"- {error}")
        for warning in warnings:
            print(f"WARNING: {warning}")
        return 1
    print(f"PASS: {label}")
    for warning in warnings:
        print(f"WARNING: {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
