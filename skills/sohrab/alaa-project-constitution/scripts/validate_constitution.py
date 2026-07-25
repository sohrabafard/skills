#!/usr/bin/env python3
"""Validate Alaa project constitution templates and generated constitutions.

Modes
  --template PATH   check a constitution-template.md against the generation contract
  --final PATH      check a generated CONSTITUTION.md
  --self-test       run the in-memory fixture suite; use this after editing this script

Options for --final
  --shape thin|full        select the compactness budget (default: thin)
  --check-bindings         also validate sibling root AGENTS.md and CLAUDE.md adapters
  --archetypes a,b,c       require the markers each matched archetype's obligations must leave
                           in the document; run --list-archetypes for the identifiers
"""

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

# (pattern, label, case_sensitive)
FORBIDDEN_FINAL_PATTERNS = (
    (r"Sync Impact Report", "Sync Impact Report", False),
    (r"Constitution Metadata", "Constitution Metadata", False),
    (r"Evidence Ledger", "evidence ledger", False),
    (r"Conditional Project Modules", "module inventory", False),
    (r"Project Validation Matrix", "validation matrix", False),
    (r"Agent Operating Contract", "agent operating tutorial", False),
    (r"AGENTS\.md and CLAUDE\.md Binding", "binding section", False),
    (r"Final Ratification", "finalization narrative", False),
    (r"Finalization and binding next step", "finalization narrative", False),
    (r"@CONSTITUTION\.md", "runtime import syntax", False),
    (r"Owner decision state\s*:", "owner-decision telemetry", False),
    (r"Finalization outcome\s*:", "finalization telemetry", False),
    (r"Binding effect\s*:", "binding telemetry", False),
    (r"Template used\s*:", "template telemetry", False),
    (r"Validation performed\s*:", "validation telemetry", False),
    # Authoring claim labels and dispositions are working state, never law.
    (r"\bOBSERVED\b", "claim label OBSERVED", True),
    (r"\bINHERITED\b", "claim label INHERITED", True),
    (r"\bINFERRED_CANDIDATE\b", "claim label INFERRED_CANDIDATE", True),
    (r"\bOWNER_DECIDED\b", "claim label OWNER_DECIDED", True),
    (r"\bREQUIRED_BY_ARCHETYPE\b", "disposition label", True),
    (r"\bREQUIRED_BY_EVIDENCE\b", "disposition label", True),
    (r"\bOWNER_DECISION_REQUIRED\b", "disposition label", True),
    (r"\bDELEGATE_TO_CANONICAL_SOURCE\b", "disposition label", True),
    (r"\bNON_CONSTITUTIONAL_FOLLOW_UP\b", "disposition label", True),
    (r"\bNOT_APPLICABLE\b", "disposition label", True),
    (r"\bTHIN_CHARTER\b|\bFULL_CHARTER\b", "charter-shape telemetry", True),
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
# Fields may wrap across lines: the separator is the semicolon, not the newline.
# `[^;]+?` therefore matches newlines deliberately, and the caller bounds the window.
TODO_RE = re.compile(
    r"TODO\([a-z0-9][a-z0-9._-]*\):\s*[^;]+?;\s*"
    r"reason:\s*[^;]+?;\s*owner:\s*[^;]+?;\s*blocking:\s*(?:yes|no)\.?",
    re.IGNORECASE,
)
TODO_WINDOW = 500

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
    r"^(?:go|make|npm|pnpm|yarn|python|python3|php|composer|docker|kubectl|helm|terraform|"
    r"git|bash|sh|node|cargo|dotnet|pytest|mvn|gradle|\.[/\\])(?:\s|$)",
    re.IGNORECASE,
)
BACKTICK = chr(96)

URL_RE = re.compile(r"https?://\S+")
ISO_DATE_RE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
# Metric and score tokens whose numeric value must never be written without provenance.
VOLATILE_METRIC_RE = re.compile(
    r"Largest Contentful Paint|Interaction to Next Paint|Cumulative Layout Shift|"
    r"Core Web Vitals|Lighthouse|\bLCP\b|\bINP\b|\bCLS\b|\bTTFB\b|\bFCP\b|"
    r"percentile|\bp50\b|\bp90\b|\bp95\b|\bp99\b",
    re.IGNORECASE,
)

# Markers an archetype's mandatory obligations must leave in a constitution.
# Each entry is (human description, regex). The regex proves the obligation was written;
# it cannot prove the obligation is correct, which is why reading is still required.
ARCHETYPE_REQUIRED_MARKERS: dict[str, tuple[tuple[str, str], ...]] = {
    "browser-web-client": (
        ("a named Core Web Vitals metric", r"Largest Contentful Paint|Interaction to Next Paint|Cumulative Layout Shift|Core Web Vitals|\bLCP\b|\bINP\b|\bCLS\b"),
        ("a Lighthouse category budget", r"Lighthouse"),
        ("an SEO or indexability rule", r"\bSEO\b|indexab|canonical URL|robots|sitemap|crawler"),
        ("a service-worker or explicit no-worker decision", r"service worker|service-worker|serviceWorker"),
        ("the rule that failed responses are never cached", r"(?is)fail\w*[^.]{0,120}cach|cach\w*[^.]{0,120}(?:never|not)[^.]{0,60}(?:fail|error|non-success)"),
        ("a cache invalidation rule", r"invalidat"),
        ("an offline or degraded-network rule", r"offline|degraded|unstable network|intermittent"),
        ("an accessibility conformance target", r"accessib|WCAG|a11y"),
    ),
    "public-http-api": (
        ("a versioning or compatibility rule", r"version|compatib|deprecat"),
        ("a single error contract", r"error (?:envelope|contract|shape|response)"),
        ("an authentication or authorization rule", r"authenticat|authoriz|auth\b"),
        ("a rate limit or overload rule", r"rate limit|admission|shed|throttl"),
        ("an idempotency rule", r"idempoten"),
        ("a timeout or retry rule", r"timeout|deadline|retr"),
        ("a pagination or result bound", r"paginat|page size|bounded"),
    ),
    "internal-service-api": (
        ("an explicit trust boundary", r"trust boundary|mTLS|caller identity|service identity"),
        ("a schema evolution rule", r"schema (?:evolution|compatib)|backward compat|additive"),
        ("a timeout, retry, or circuit-breaking rule", r"timeout|deadline|retr|circuit"),
        ("a backpressure or concurrency bound", r"backpressure|bounded concurrency|concurrency (?:limit|bound)"),
        ("a partial-failure contract", r"partial failure|degraded response"),
    ),
    "async-worker": (
        ("its delivery semantics", r"at-least-once|at least once|exactly-once|delivery semantic"),
        ("an idempotency or deduplication rule", r"idempoten|deduplicat|dedup"),
        ("a retry and backoff rule", r"retr\w*[^.]{0,80}(?:backoff|jitter)|backoff"),
        ("a dead-letter destination", r"dead[- ]letter|\bDLQ\b"),
        ("a backlog or lag signal", r"backlog|lag|drain"),
        ("a graceful shutdown rule", r"graceful shutdown|drain window|in-flight"),
    ),
    "scheduled-job": (
        ("an overlap rule", r"overlap|concurrent run|lock"),
        ("a missed-run rule", r"missed run|catch up|backfill|skip"),
        ("a bounded-work rule", r"maximum (?:batch|duration)|bounded|batch size"),
        ("explicit calendar or timezone semantics", r"timezone|time zone|daylight|\bUTC\b"),
        ("run observability", r"processed count|run outcome|has not succeeded|alert"),
    ),
    "admin-panel": (
        ("per-action or per-record authorization", r"per action|per record|deny by default|default(?:s)? to deny"),
        ("an audit trail", r"audit"),
        ("destructive-action protection", r"destructive|bulk|confirmation|blast radius"),
        ("export or field-level read control", r"export|mask|field-level"),
    ),
    "mobile-bff": (
        ("a minimum client version rule", r"minimum (?:supported )?(?:app|client) version|client version|support window"),
        ("a forced-update path", r"forced update|force update|update prompt"),
        ("a partial-upstream-failure contract", r"partial|absent section|degraded"),
        ("an offline or resumption rule", r"offline|resum|unsent"),
    ),
    "realtime-streaming": (
        ("connection authentication and re-authentication", r"re-authenticat|reauthenticat|credential expiry|token expiry"),
        ("a reconnect and resume rule", r"reconnect|resume (?:cursor|token)"),
        ("heartbeat or dead-peer detection", r"heartbeat|keepalive|dead peer|dead-peer"),
        ("fan-out bounds", r"concurrent connection|per connection|fan-out|fan out"),
        ("a backpressure rule", r"backpressure|drop policy|buffer bound"),
    ),
    "data-pipeline": (
        ("a lineage or source-of-truth rule", r"lineage|source of truth|upstream source"),
        ("reproducibility and a watermark", r"watermark|reproducib|deterministic"),
        ("an idempotent reload rule", r"idempoten|recomput|reload"),
        ("a freshness contract", r"freshness|maximum lag|\blag\b"),
        ("in-pipeline correctness assertions", r"assertion|row count|referential"),
        ("retention or deletion propagation", r"retention|deletion|personal data"),
    ),
}


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


def structured_todos(text: str) -> list[re.Match[str]]:
    """Return one match per well-formed structured TODO, wrapped or single-line."""
    found: list[re.Match[str]] = []
    for anchor in re.finditer(r"\bTODO\(", text, flags=re.IGNORECASE):
        window = text[anchor.start() : anchor.start() + TODO_WINDOW]
        match = TODO_RE.match(window)
        if match:
            found.append(match)
    return found


def malformed_todo_lines(text: str) -> list[int]:
    lines: list[int] = []
    for anchor in re.finditer(r"\bTODO\(", text, flags=re.IGNORECASE):
        window = text[anchor.start() : anchor.start() + TODO_WINDOW]
        if re.match(r"TODO\(id\)", window, flags=re.IGNORECASE):
            continue
        if not TODO_RE.match(window):
            lines.append(text.count("\n", 0, anchor.start()) + 1)
    return lines


def has_blocking_todo(text: str) -> bool:
    return any(
        re.search(r"blocking:\s*yes", match.group(0), flags=re.IGNORECASE)
        for match in structured_todos(text)
    )


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


def threshold_provenance_errors(text: str) -> list[str]:
    """A written performance or score value needs its source URL and verification date.

    Thresholds move between tool versions, so a number with no provenance cannot be
    revalidated and silently governs the wrong thing. The obligation is always allowed;
    only an unsourced number is rejected.
    """
    errors: list[str] = []
    for index, block in enumerate(re.split(r"\n\s*\n", text), 1):
        if not VOLATILE_METRIC_RE.search(block):
            continue
        stripped = ISO_DATE_RE.sub("", URL_RE.sub("", block))
        # Ignore ordinary structural digits: heading numbers and list markers.
        stripped = re.sub(r"(?m)^\s*(?:#{1,6}\s*)?\d+[.)]\s", "", stripped)
        stripped = re.sub(r"(?m)^#{1,6}\s.*$", "", stripped)
        if not re.search(r"\d", stripped):
            continue
        if not URL_RE.search(block) or not ISO_DATE_RE.search(block):
            snippet = " ".join(block.split())[:110]
            errors.append(
                "a performance or score value is stated without its source URL and "
                f"verification date (block {index}): {snippet}"
            )
    return errors


def archetype_marker_errors(text: str, archetypes: tuple[str, ...]) -> list[str]:
    errors: list[str] = []
    for name in archetypes:
        markers = ARCHETYPE_REQUIRED_MARKERS.get(name)
        if markers is None:
            errors.append(
                f"unknown archetype identifier: {name}; run --list-archetypes for valid values"
            )
            continue
        for description, pattern in markers:
            if not re.search(pattern, text, flags=re.IGNORECASE):
                errors.append(
                    f"archetype '{name}' is matched but the constitution does not state "
                    f"{description}; a matched archetype's obligation is written even when the "
                    "code does not implement it yet"
                )
    return errors


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
        # A template that reinstates a mandatory repository-root copy forks the contract per
        # repository, so the path rule is checked rather than trusted.
        "the generation contract wherever it is read from",
        "A repository is not required to hold a copy",
        "THE FACT/OBLIGATION SEAM",
        "Never invent a fact about this repository",
        "OBSERVED repository truth",
        "INFERRED_CANDIDATE",
        "PROJECT ARCHETYPE LAYER",
        "Largest Contentful Paint",
        "Failed responses are never cached.",
        "MANDATORY LIVE RESEARCH",
        "CROSS-CUTTING QUALITY BAR",
        "INTENT AND RISK DISCOVERY",
        "REQUIRED_BY_ARCHETYPE",
        "OWNER_DECISION_REQUIRED",
        "CROSS-CUTTING COVERAGE GATE",
        "INTERACTIVE OWNER DECISIONS",
        "FINAL DOCUMENT IS LAW, NOT AUTHORING TELEMETRY",
        "FINAL CONSTITUTIONAL COMPRESSION PASS",
        "Compression removes words, never obligations.",
        "Retention follows the matched archetypes",
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

    # A hardcoded threshold in the template would ship the defect to every repository.
    for pattern, label in (
        (r"(?i)\b(?:LCP|INP|CLS)\b\s*(?:budget\s*)?(?:of|=|:|<|>)?\s*\d", "a Core Web Vitals value"),
        (r"(?i)Lighthouse[^.\n]{0,40}\b(?:score\s*)?(?:of|=|:|>=|<=|at least)\s*\d", "a Lighthouse score"),
        (r"(?i)\bWCAG\s*\d", "a specific accessibility standard version"),
    ):
        if re.search(pattern, text):
            errors.append(
                f"template hardcodes {label}; state the metric and require a budget, and have "
                "the agent fetch the current value"
            )

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


def validate_final(
    text: str, shape: str = "thin", archetypes: tuple[str, ...] = ()
) -> list[str]:
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

    for pattern, label, case_sensitive in FORBIDDEN_FINAL_PATTERNS:
        flags = 0 if case_sensitive else re.IGNORECASE
        if re.search(pattern, text, flags=flags):
            errors.append(f"authoring/runtime residue remains in final constitution: {label}")

    match = footer_match(text)
    if not match:
        errors.append("missing canonical version/status/date footer")
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
            if has_blocking_todo(text):
                errors.append("BINDING status cannot contain a blocking unresolved TODO")
        elif status in {"DRAFT", "NEEDS_REVIEW"}:
            if not has_blocking_todo(text):
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

    bare_todos = malformed_todo_lines(text)
    if bare_todos:
        errors.append(
            "TODOs must use 'TODO(id): ...; reason: ...; owner: ...; blocking: yes|no' "
            f"near line(s): {', '.join(map(str, bare_todos[:10]))}"
        )

    errors.extend(threshold_provenance_errors(text))
    if archetypes:
        errors.extend(archetype_marker_errors(text, archetypes))
    return errors


def extract_markdown_section(text: str, heading: str) -> str:
    match = re.search(
        rf"(?ms)^##\s+{re.escape(heading)}\s*$.*?(?=^##\s+|\Z)",
        text,
    )
    return match.group(0) if match else ""


def activation_hits(text: str) -> list[str]:
    """Paragraphs that put the constitution into force for an agent.

    A historical or explanatory mention is not activation. Only wording that tells an agent
    the file is binding, or to read it before working, or that imports it, activates it.
    """
    hits: list[str] = []
    for block in re.split(r"\n\s*\n", text):
        if "CONSTITUTION.md" not in block:
            continue
        low = block.lower()
        if any(
            token in low
            for token in ("non-binding", "not binding", "superseded", "inactive", "historical", "draft", "proposal")
        ):
            continue
        if (
            re.search(r"\bbinding\b", low)
            or re.search(r"\bread\b[^.]{0,100}\bbefore\b", low)
            or "@CONSTITUTION.md" in block
        ):
            hits.append(" ".join(block.split())[:120])
    return hits


def validate_bindings(root: Path, constitution_text: str) -> list[str]:
    errors: list[str] = []
    match = footer_match(constitution_text)
    if not match:
        return ["cannot validate bindings without the canonical status footer"]
    status = match.group("status").upper()

    agents_path = root / "AGENTS.md"
    claude_path = root / "CLAUDE.md"
    try:
        agents_text = agents_path.read_text(encoding="utf-8") if agents_path.is_file() else ""
        claude_text = claude_path.read_text(encoding="utf-8") if claude_path.is_file() else ""
    except (OSError, UnicodeError) as exc:
        return [f"cannot read root binding files: {exc}"]

    agents_section = extract_markdown_section(agents_text, "Project Constitution")
    claude_section = extract_markdown_section(claude_text, "Constitution Binding")

    if status in {"DRAFT", "NEEDS_REVIEW"}:
        # A pre-existing historical mention is preserved deliberately and is not activation.
        for name, body in (("AGENTS.md", agents_text), ("CLAUDE.md", claude_text)):
            for hit in activation_hits(body):
                errors.append(
                    f"{status} constitution is activated by {name}; remove the adapter or import "
                    f"and report binding as deferred: {hit}"
                )
        if agents_section and "CONSTITUTION.md" in agents_section:
            errors.append(f"{status} constitution must not have a '## Project Constitution' adapter in AGENTS.md")
        if claude_section:
            errors.append(f"{status} constitution must not have a '## Constitution Binding' adapter in CLAUDE.md")
        return errors

    if status == "SUPERSEDED":
        # Both documented paths are valid: remove the reference, or point it at the successor.
        if "@CONSTITUTION.md" in claude_text:
            errors.append("SUPERSEDED constitution must not remain imported by CLAUDE.md")
        for name, section in (("AGENTS.md", agents_section), ("CLAUDE.md", claude_section)):
            if not section:
                continue
            low = section.lower()
            if "superseded" not in low and "inactive" not in low:
                errors.append(f"{name} adapter must mark the SUPERSEDED constitution inactive")
            if re.search(r"\bbinding\b", low) and not re.search(r"non-binding|not binding", low):
                if "successor" not in low and not re.search(r"instead|replaced by", low):
                    errors.append(
                        f"{name} adapter still presents the SUPERSEDED constitution as in force; "
                        "name the successor instead"
                    )
        return errors

    # status == BINDING
    for path in (agents_path, claude_path):
        if not path.is_file():
            errors.append(f"missing root binding file: {path.name}")
    if errors:
        return errors

    if not agents_section:
        errors.append("AGENTS.md has no '## Project Constitution' adapter")
    elif "CONSTITUTION.md" not in agents_section:
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

    for name, section in (("AGENTS.md", agents_section.lower()), ("CLAUDE.md", claude_section.lower())):
        if "non-binding" in section or "not binding" in section:
            errors.append(f"{name} adapter incorrectly marks BINDING policy non-binding")
        elif "binding" not in section and "canonical project policy" not in section:
            errors.append(f"{name} adapter does not state BINDING effect")
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


VALID_FINAL_FIXTURE = """# Example Project Constitution

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


def run_self_test() -> list[str]:
    failures: list[str] = []
    valid_final = VALID_FINAL_FIXTURE

    def expect_pass(name: str, text: str, **kwargs: object) -> None:
        result = validate_final(text, **kwargs)  # type: ignore[arg-type]
        if result:
            failures.append(f"{name}: expected pass, got {result}")

    def expect_fail(name: str, text: str, **kwargs: object) -> None:
        if not validate_final(text, **kwargs):  # type: ignore[arg-type]
            failures.append(f"{name}: expected failure, got pass")

    expect_pass("valid final fixture", valid_final)
    expect_fail("invalid semantic version", valid_final.replace("1.0.0", "VERSION"))
    expect_fail(
        "metadata table residue",
        valid_final.replace(
            "## Authority and Scope",
            "## Constitution Metadata\n\n| Field | Value |\n|---|---|\n| Status | BINDING |\n\n## Authority and Scope",
        ),
    )
    expect_fail(
        "binding section residue",
        valid_final.replace(
            "## Amendments and Exceptions",
            "## AGENTS.md and CLAUDE.md Binding\n\nRuntime adapter.\n\n## Amendments and Exceptions",
        ),
    )
    expect_fail(
        "claim label residue",
        valid_final.replace(
            "Current truth is inspected before claims are made.",
            "Current truth is inspected before claims are made. INFERRED_CANDIDATE rules apply.",
        ),
    )
    expect_fail(
        "oversized thin constitution",
        valid_final.replace("**Version**:", ("Constitutional sentence.\n" * 200) + "\n**Version**:"),
    )
    expect_fail(
        "duplicated exact command",
        valid_final.replace(
            "## Amendments and Exceptions",
            "`go test ./...` and again `go test ./...`\n\n## Amendments and Exceptions",
        ),
    )
    expect_fail(
        "binding fixture with blocking TODO",
        valid_final.replace(
            "## Amendments and Exceptions",
            "TODO(owner-choice): decide scope; reason: owner input missing; owner: owner; "
            "blocking: yes.\n\n## Amendments and Exceptions",
        ),
    )

    # Threshold provenance.
    expect_fail(
        "unsourced Core Web Vitals value",
        valid_final.replace(
            "Current truth is inspected before claims are made.",
            "Largest Contentful Paint stays under 2.5 seconds at p75.",
        ),
    )
    expect_pass(
        "sourced Core Web Vitals value",
        valid_final.replace(
            "Current truth is inspected before claims are made.",
            "Largest Contentful Paint stays under 2.5 seconds at p75 on the catalogue route "
            "(source: https://web.dev/articles/lcp, verified 2026-07-24).",
        ),
    )
    expect_pass(
        "metric named without a value",
        valid_final.replace(
            "Current truth is inspected before claims are made.",
            "Every indexable route holds a Largest Contentful Paint budget recorded in "
            "PERFORMANCE.md, which owns its current threshold.",
        ),
    )

    # Wrapped structured TODO in a draft: the separator is the semicolon, not the newline.
    wrapped_draft = (
        valid_final.replace(
            "## Amendments and Exceptions",
            "## Unresolved Decisions\n\nTODO(owner-choice): decide the offline scope of the\n"
            "checkout journey; reason: owner selected Decide later and the evidence cannot\n"
            "decide it; owner: repository owner; blocking: yes.\n\n## Amendments and Exceptions",
            1,
        )
        .replace("**Status**: BINDING", "**Status**: DRAFT")
        .replace("**Ratified**: 2026-07-10", "**Ratified**: Not ratified")
        .replace("**Version**: 1.0.0", "**Version**: 0.1.0")
    )
    expect_pass("wrapped structured TODO in a draft", wrapped_draft)
    expect_fail("draft with runtime import residue", wrapped_draft + "\n@CONSTITUTION.md\n")
    expect_fail(
        "draft without a blocking TODO",
        valid_final.replace("**Status**: BINDING", "**Status**: DRAFT").replace(
            "**Ratified**: 2026-07-10", "**Ratified**: Not ratified"
        ),
    )
    expect_fail(
        "malformed TODO",
        wrapped_draft.replace("reason: owner selected Decide later and the evidence cannot\ndecide it; ", ""),
    )

    # Archetype markers.
    expect_fail("browser archetype with no obligations written", valid_final, archetypes=("browser-web-client",))
    expect_fail("unknown archetype identifier", valid_final, archetypes=("not-an-archetype",))
    browser_ok = valid_final.replace(
        "Current truth is inspected before claims are made.",
        "Every indexable route holds a Largest Contentful Paint budget owned by "
        "PERFORMANCE.md, a Lighthouse category budget enforced in CI, an SEO canonical URL "
        "and sitemap owner, a stated service worker update strategy, cache invalidation keys, "
        "an offline state per journey, and an accessibility conformance target. A failed "
        "response is never written to any client cache.",
    )
    expect_pass("browser archetype with obligations written", browser_ok, archetypes=("browser-web-client",))

    # Binding validation across statuses, using in-memory temp roots.
    import tempfile

    def bindings_for(status_text: str, agents: str, claude: str) -> list[str]:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "AGENTS.md").write_text(agents, encoding="utf-8")
            (root / "CLAUDE.md").write_text(claude, encoding="utf-8")
            return validate_bindings(root, status_text)

    superseded = valid_final.replace("**Status**: BINDING", "**Status**: SUPERSEDED")
    if bindings_for(superseded, "# Guide\n\nOrdinary guidance only.\n", "# Guide\n\nOrdinary guidance only.\n"):
        failures.append("SUPERSEDED with the reference removed was rejected")
    if bindings_for(
        superseded,
        "# Guide\n\n## Project Constitution\n\n`CONSTITUTION.md` is SUPERSEDED and inactive historical policy. Read `CONSTITUTION-v3.md` instead.\n",
        "# Guide\n\n## Constitution Binding\n\n`CONSTITUTION.md` is SUPERSEDED and inactive. Read `CONSTITUTION-v3.md` instead.\n",
    ):
        failures.append("SUPERSEDED pointing at a successor was rejected")
    if not bindings_for(
        superseded,
        "# Guide\n\n## Project Constitution\n\nRead `CONSTITUTION.md` before work. It is binding project policy.\n",
        "# Guide\n\n@CONSTITUTION.md\n\n## Constitution Binding\n\nThe imported constitution is binding.\n",
    ):
        failures.append("SUPERSEDED still presented as in force was accepted")

    draft = wrapped_draft
    if bindings_for(
        draft,
        "# Guide\n\n## History\n\nIn 2025 the team discussed whether CONSTITUTION.md should exist. No adapter was added.\n",
        "# Guide\n\nOrdinary guidance only.\n",
    ):
        failures.append("DRAFT with a historical AGENTS.md mention was rejected")
    if not bindings_for(
        draft,
        "# Guide\n\n## Project Constitution\n\nRead `CONSTITUTION.md` before work. It is binding project policy.\n",
        "# Guide\n\nOrdinary guidance only.\n",
    ):
        failures.append("DRAFT activated by an AGENTS.md adapter was accepted")
    if not bindings_for(draft, "# Guide\n\nNothing.\n", "# Guide\n\n@CONSTITUTION.md\n"):
        failures.append("DRAFT imported by CLAUDE.md was accepted")

    if bindings_for(
        valid_final,
        "# Guide\n\n## Project Constitution\n\nRead `CONSTITUTION.md` in full before work. Treat it as binding project policy within its scope.\n",
        "# Guide\n\n@CONSTITUTION.md\n\n## Constitution Binding\n\nThe imported constitution is binding project policy within its scope.\n",
    ):
        failures.append("valid BINDING adapters were rejected")
    if not bindings_for(valid_final, "# Guide\n\nNothing.\n", "# Guide\n\nNothing.\n"):
        failures.append("BINDING with no adapters was accepted")

    return failures


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--template", type=Path, help="validate a template file")
    mode.add_argument("--final", type=Path, help="validate a generated constitution")
    mode.add_argument(
        "--self-test",
        action="store_true",
        help="run the in-memory fixture suite; use after editing this script",
    )
    mode.add_argument(
        "--list-archetypes",
        action="store_true",
        help="print the archetype identifiers accepted by --archetypes",
    )
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
    parser.add_argument(
        "--archetypes",
        default="",
        help="with --final, comma-separated matched archetype identifiers whose obligations "
        "must be present in the document",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    warnings: list[str] = []
    if args.list_archetypes:
        for name, markers in ARCHETYPE_REQUIRED_MARKERS.items():
            print(f"{name}: {', '.join(description for description, _ in markers)}")
        return 0
    if args.check_bindings and not args.final:
        print("FAIL: --check-bindings requires --final", file=sys.stderr)
        return 2
    if args.archetypes and not args.final:
        print("FAIL: --archetypes requires --final", file=sys.stderr)
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
        if args.template:
            errors = validate_template(text)
        else:
            selected = tuple(a.strip() for a in args.archetypes.split(",") if a.strip())
            errors = validate_final(text, args.shape, selected)
            if args.check_bindings:
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
