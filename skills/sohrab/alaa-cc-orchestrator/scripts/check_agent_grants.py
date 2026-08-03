#!/usr/bin/env python3
"""Enforce the exact per-role tool grant of every managed Claude Code agent.

The catalog assigns named MCP tools to each allowlisted role. Implementation roles
inherit the runtime tool set, but must carry the exact safety deny set. Roles that
use MCP tools preload the routing skill instead of receiving the unscoped ``Skill``
tool, which would make every model-invocable skill reachable.

  exit 0  every invariant holds
  exit 1  at least one invariant failed
  exit 2  usage or parse error

Run with --self-test to prove the gate rejects known-bad definitions.
"""
from __future__ import annotations
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AGENTS = os.path.join(ROOT, "agents")

ROUTING_SKILL = "/alaa-code-intelligence-routing"
MUST_DENY = frozenset((
    "Skill",
    "mcp__serena__execute_shell_command",
))

CODEGRAPH = {"mcp__codegraph"}
SERENA_READ = {
    "mcp__serena__find_symbol",
    "mcp__serena__get_symbols_overview",
    "mcp__serena__find_referencing_symbols",
    "mcp__serena__find_declaration",
    "mcp__serena__find_implementations",
    "mcp__serena__get_diagnostics_for_file",
}
BOOST_DOCS = {
    "mcp__laravel-boost__search-docs",
    "mcp__laravel-boost__application-info",
}
BOOST_ROUTING = {"mcp__laravel-boost__get-absolute-url"}
BOOST_SCHEMA = {
    "mcp__laravel-boost__database-schema",
    "mcp__laravel-boost__database-connections",
}
BOOST_ERRORS = {
    "mcp__laravel-boost__last-error",
    "mcp__laravel-boost__read-log-entries",
}
BOOST_BROWSER = {"mcp__laravel-boost__browser-logs"}

EXPECTED_MCP = {
    "alaa-accessibility-reviewer": BOOST_DOCS | BOOST_ROUTING,
    "alaa-adversarial-reviewer": CODEGRAPH | SERENA_READ | BOOST_DOCS | BOOST_SCHEMA,
    "alaa-api-contract-reviewer": CODEGRAPH | BOOST_DOCS | BOOST_ROUTING | BOOST_SCHEMA,
    "alaa-architecture-critic": CODEGRAPH | BOOST_DOCS | BOOST_SCHEMA,
    "alaa-browser-qa": BOOST_DOCS | BOOST_ROUTING | BOOST_ERRORS | BOOST_BROWSER,
    "alaa-dependency-auditor": BOOST_DOCS,
    "alaa-documenter": BOOST_DOCS | BOOST_ROUTING,
    "alaa-explorer": CODEGRAPH | BOOST_DOCS | BOOST_ROUTING,
    "alaa-failure-analyst": CODEGRAPH | SERENA_READ | BOOST_DOCS | BOOST_ERRORS | BOOST_BROWSER,
    "alaa-implementer-opus": None,
    "alaa-implementer": None,
    "alaa-migration-guardian": CODEGRAPH | BOOST_DOCS | BOOST_SCHEMA,
    "alaa-observability-reviewer": CODEGRAPH | BOOST_DOCS | BOOST_ERRORS | BOOST_BROWSER,
    "alaa-performance-profiler": CODEGRAPH | BOOST_DOCS | BOOST_SCHEMA | BOOST_ERRORS,
    "alaa-release-guardian": BOOST_DOCS,
    "alaa-researcher": BOOST_DOCS,
    "alaa-reviewer": CODEGRAPH | SERENA_READ | BOOST_DOCS | BOOST_SCHEMA,
    "alaa-security-reviewer": CODEGRAPH | SERENA_READ | BOOST_DOCS | BOOST_SCHEMA,
    "alaa-spec-analyst": CODEGRAPH | BOOST_DOCS,
    "alaa-test-strategist": CODEGRAPH | BOOST_DOCS | BOOST_SCHEMA,
    "alaa-verifier": set(),
}


def frontmatter(path: str) -> dict[str, str | list[str]]:
    text = open(path, encoding="utf-8").read().replace("\r\n", "\n")
    head = text.split("\n---\n")[0].lstrip("-\n")
    out: dict[str, str | list[str]] = {}
    list_key: str | None = None
    for line in head.split("\n"):
        m = re.match(r"^(tools|disallowedTools|model|effort|skills):\s*(.*)$", line)
        if m:
            key, value = m.group(1), m.group(2)
            if key == "skills" and not value:
                out[key] = []
                list_key = key
            else:
                out[key] = value
                list_key = None
            continue
        item = re.match(r"^\s+-\s+(.+?)\s*$", line)
        if item and list_key:
            value = out[list_key]
            assert isinstance(value, list)
            value.append(item.group(1))
        elif line.strip():
            list_key = None
    return out


def csv(value: str | list[str]) -> list[str]:
    if isinstance(value, list):
        return value
    return [x.strip() for x in value.split(",") if x.strip()]


def grant_failures(name: str, fm: dict[str, str | list[str]]) -> tuple[list[str], str]:
    failures: list[str] = []
    expected = EXPECTED_MCP[name]
    allow = csv(fm["tools"]) if "tools" in fm else None
    deny = set(csv(fm.get("disallowedTools", "")))
    skills = set(csv(fm.get("skills", [])))

    if expected is None:
        granted = "inherits all, exact safety deny"
        if allow is not None:
            failures.append(f"{name}: implementation role must inherit tools, but defines an allowlist")
        if deny != MUST_DENY:
            missing = sorted(MUST_DENY - deny)
            extra = sorted(deny - MUST_DENY)
            detail = []
            if missing:
                detail.append(f"missing {', '.join(missing)}")
            if extra:
                detail.append(f"unexpected {', '.join(extra)}")
            failures.append(f"{name}: safety deny set differs from the catalog ({'; '.join(detail)})")
        if ROUTING_SKILL not in skills:
            failures.append(f"{name}: must preload {ROUTING_SKILL}")
        return failures, granted

    if allow is None:
        failures.append(f"{name}: allowlisted role omits tools and therefore inherits every tool")
        return failures, "invalid inherited grant"

    actual_mcp = {tool for tool in allow if tool.startswith("mcp__")}
    native = [tool for tool in allow if not tool.startswith("mcp__")]
    if not native:
        failures.append(f"{name}: allowlist contains only MCP entries and may not launch without them")
    if "Skill" in allow:
        failures.append(f"{name}: grants unscoped Skill access; preload only the routing skill")
    if deny:
        failures.append(f"{name}: allowlisted role has an unexpected disallowedTools overlay")
    if actual_mcp != expected:
        missing = sorted(expected - actual_mcp)
        extra = sorted(actual_mcp - expected)
        detail = []
        if missing:
            detail.append(f"missing {', '.join(missing)}")
        if extra:
            detail.append(f"unexpected {', '.join(extra)}")
        failures.append(f"{name}: MCP grant differs from the catalog ({'; '.join(detail)})")
    if expected and ROUTING_SKILL not in skills:
        failures.append(f"{name}: MCP grant requires preloaded {ROUTING_SKILL}")

    return failures, ", ".join(sorted(actual_mcp)) or "none"


def main() -> int:
    if not os.path.isdir(AGENTS):
        print(f"no agents directory at {AGENTS}", file=sys.stderr)
        return 2
    names = sorted(f for f in os.listdir(AGENTS) if f.endswith(".md"))
    if not names:
        print("no agent definitions found", file=sys.stderr)
        return 2

    actual_names = {filename[:-3] for filename in names}
    expected_names = set(EXPECTED_MCP)
    if actual_names != expected_names:
        missing = sorted(expected_names - actual_names)
        extra = sorted(actual_names - expected_names)
        if missing:
            print(f"missing catalog roles: {', '.join(missing)}", file=sys.stderr)
        if extra:
            print(f"uncatalogued roles: {', '.join(extra)}", file=sys.stderr)
        return 2

    failures: list[str] = []
    width = max(len(n) - 3 for n in names)
    print("Effective code-intelligence grant")
    for filename in names:
        name = filename[:-3]
        fm = frontmatter(os.path.join(AGENTS, filename))
        role_failures, granted = grant_failures(name, fm)
        failures.extend(role_failures)
        print(f"  {name:<{width}}  {granted}")

    print()
    if failures:
        print("FAILED")
        for line in failures:
            print(f"  - {line}")
        return 1
    print(f"OK: {len(names)} agents match the catalog's exact MCP and skill grants")
    return 0


def self_test() -> int:
    """Prove the gate can fail. A checker never observed rejecting a bad input is
    indistinguishable from one that always passes."""
    import textwrap
    cases = [
        ("unexpected server on a no-MCP role", "alaa-verifier",
         "tools: Read, Bash, mcp__codegraph", "MCP grant differs"),
        ("missing CodeGraph from explorer", "alaa-explorer",
         "tools: Read, Bash, mcp__laravel-boost__search-docs, mcp__laravel-boost__application-info, mcp__laravel-boost__get-absolute-url",
         "MCP grant differs"),
        ("bare Skill access", "alaa-researcher",
         "tools: Read, Bash, Skill, mcp__laravel-boost__search-docs, mcp__laravel-boost__application-info",
         "unscoped Skill"),
        ("MCP grant without routing preload", "alaa-researcher",
         "tools: Read, Bash, mcp__laravel-boost__search-docs, mcp__laravel-boost__application-info",
         "requires preloaded"),
        ("inherited role missing Skill deny", "alaa-implementer", None, "safety deny set differs"),
    ]
    failures = []
    for label, name, tools, expected_message in cases:
        lines = ["name: fixture", "description: red fixture", "model: sonnet"]
        if tools:
            lines.append(tools)
        if name == "alaa-implementer":
            lines.append("disallowedTools: mcp__serena__execute_shell_command")
            lines.extend(("skills:", f"  - {ROUTING_SKILL}"))
        elif label != "MCP grant without routing preload":
            lines.extend(("skills:", f"  - {ROUTING_SKILL}"))
        body = textwrap.dedent("---\n" + "\n".join(lines) + "\n---\n\nbody\n")
        import tempfile
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False) as fixture:
            fixture.write(body)
            fixture_path = fixture.name
        try:
            observed, _ = grant_failures(name, frontmatter(fixture_path))
        finally:
            os.unlink(fixture_path)
        if not any(expected_message in item for item in observed):
            failures.append(f"{label}: did not observe {expected_message!r}; got {observed}")
    print()
    if failures:
        print("SELF-TEST FAILED")
        for line in failures:
            print(f"  - {line}")
        return 1
    print(f"SELF-TEST OK: {len(cases)} red fixtures each rejected")
    return 0


if __name__ == "__main__":
    sys.exit(self_test() if "--self-test" in sys.argv[1:] else main())
