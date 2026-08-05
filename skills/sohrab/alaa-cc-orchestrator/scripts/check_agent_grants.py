#!/usr/bin/env python3
"""Enforce the exact per-role tool grant of every managed Claude Code agent.

The catalog assigns named MCP tools to each allowlisted role. Implementation roles
inherit the runtime tool set, but must carry the exact safety deny set.

**A role can always reach a skill it is told to apply.** Two mechanisms serve that,
and they are complementary rather than alternatives. ``skills:`` preloads what a role
always needs — the routing contract, and the doctrine its verdict is measured against.
The ``Skill`` tool covers everything else: the skill a lane needs is often not knowable
when the definition is written, because it depends on the repository's language and the
surface the dispatch hands over, and the pack's rule is to name the one skill the lane
needs rather than preload every candidate into every lane. An allowlisted role keeps
``Skill`` for exactly that reason, and an implementation role inherits it.

Withholding ``Skill`` was tried and reverted. It narrows nothing on a role that already
holds ``Bash``, ``Read``, ``Write``, and ``Edit``; it makes the dispatch's own
``clean_code_skill`` field unsatisfiable; and it silently removed runtime invocation
from every specialist on the theory that its preload list was complete, which no
evidence supported. The safety deny set is therefore exactly Serena's shell tool, a
real second path to the shell that bypasses the runtime's approval rules.

What is checked instead is reachability, in both directions. Every preloaded name must
resolve to an installed skill, because a stale preload silently removes a standard. And
a role that does not hold ``Skill`` must preload every installed skill its body names,
because that role has no other way to reach one.

  exit 0  every invariant holds
  exit 1  at least one invariant failed
  exit 2  usage or parse error

Run with --self-test to prove the gate rejects known-bad definitions.
"""
from __future__ import annotations
import glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AGENTS = os.path.join(ROOT, "agents")
PACK = os.path.dirname(ROOT)
REPO = os.path.dirname(os.path.dirname(PACK))

ROUTING_SKILL = "/alaa-code-intelligence-routing"
MUST_DENY = frozenset((
    "mcp__serena__execute_shell_command",
))


def skill_roots() -> list[str]:
    """Directories that may contain an installable skill, newest layout first.

    Returns an empty list when this checker runs from an installed copy with no
    sibling skills around it. A root that cannot be seen proves nothing about the
    names inside it, so preload resolution is skipped rather than failed there.
    """
    roots = [PACK]
    roots += [os.path.join(REPO, "skills", ".curated"), os.path.join(REPO, "skills", ".system")]
    roots += sorted(glob.glob(os.path.join(REPO, "vendor", "*", "skills")))
    return [r for r in roots if os.path.isdir(r)]


def installed_skills(roots: list[str]) -> set[str]:
    return {entry for r in roots for entry in os.listdir(r) if os.path.isdir(os.path.join(r, entry))}


def unresolved_skills(names: set[str], roots: list[str]) -> list[str]:
    if not roots:
        return []
    return sorted(n for n in names if not any(os.path.isdir(os.path.join(r, n.lstrip("/"))) for r in roots))


def named_skills(body: str, roots: list[str]) -> set[str]:
    """Installed skills the body names. A bare ``/word`` is prose or a path far more
    often than it is a trigger, so only tokens matching a real skill directory count."""
    if not roots:
        return set()
    installed = installed_skills(roots)
    return {"/" + t for t in re.findall(r"(?<![\w-])/([\w-]+)", body) if t in installed}

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


def grant_failures(
    name: str,
    fm: dict[str, str | list[str]],
    roots: list[str] | None = None,
    body: str = "",
) -> tuple[list[str], str]:
    failures: list[str] = []
    expected = EXPECTED_MCP[name]
    allow = csv(fm["tools"]) if "tools" in fm else None
    deny = set(csv(fm.get("disallowedTools", "")))
    skills = set(csv(fm.get("skills", [])))
    roots = skill_roots() if roots is None else roots

    for unknown in unresolved_skills(skills, roots):
        failures.append(f"{name}: preloads {unknown}, which resolves to no installed skill")

    can_invoke = (allow is None and "Skill" not in deny) or (allow is not None and "Skill" in allow)
    if not can_invoke:
        for unreachable in sorted(named_skills(body, roots) - skills):
            failures.append(
                f"{name}: names {unreachable} but holds no Skill tool and does not preload it"
            )

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
    roots = skill_roots()
    width = max(len(n) - 3 for n in names)
    print("Effective code-intelligence grant")
    for filename in names:
        name = filename[:-3]
        path = os.path.join(AGENTS, filename)
        fm = frontmatter(path)
        text = open(path, encoding="utf-8").read().replace("\r\n", "\n")
        body = text.split("\n---\n", 1)[1] if "\n---\n" in text else ""
        role_failures, granted = grant_failures(name, fm, roots, body)
        failures.extend(role_failures)
        print(f"  {name:<{width}}  {granted}")

    print()
    if not roots:
        print("preload resolution skipped: no skill root is visible from this copy")
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
    import tempfile
    BOOST = "mcp__laravel-boost__search-docs, mcp__laravel-boost__application-info"
    SERENA_SHELL = "mcp__serena__execute_shell_command"
    # label, role, tools line, disallowedTools line, preloaded skills, body, expected message
    cases = [
        ("unexpected server on a no-MCP role", "alaa-verifier",
         "tools: Read, Bash, mcp__codegraph", None, [], "body", "MCP grant differs"),
        ("missing CodeGraph from explorer", "alaa-explorer",
         f"tools: Read, Bash, {BOOST}, mcp__laravel-boost__get-absolute-url", None,
         [ROUTING_SKILL], "body", "MCP grant differs"),
        ("MCP grant without routing preload", "alaa-researcher",
         f"tools: Read, Bash, {BOOST}", None, [], "body", "requires preloaded"),
        ("inherited role missing the Serena shell deny", "alaa-implementer",
         None, "disallowedTools: ", [ROUTING_SKILL], "body", "safety deny set differs"),
        ("inherited role carrying an extra deny", "alaa-implementer",
         None, f"disallowedTools: {SERENA_SHELL}, Write", [ROUTING_SKILL], "body",
         "safety deny set differs"),
        ("inherited role defining an allowlist", "alaa-implementer",
         "tools: Read, Bash", f"disallowedTools: {SERENA_SHELL}", [ROUTING_SKILL], "body",
         "must inherit tools"),
        ("preload naming a skill that does not exist", "alaa-researcher",
         f"tools: Read, Bash, {BOOST}", None, [ROUTING_SKILL, "/alaa-not-a-real-skill"], "body",
         "resolves to no installed skill"),
        ("named skill reachable by neither preload nor Skill", "alaa-researcher",
         f"tools: Read, Bash, {BOOST}", None, [ROUTING_SKILL],
         "Domain baseline: apply /alaa-testing-strategy when installed.",
         "holds no Skill tool and does not preload it"),
        ("inherited role that denies Skill and names an unpreloaded one", "alaa-implementer",
         None, f"disallowedTools: {SERENA_SHELL}, Skill", [ROUTING_SKILL],
         "Domain baseline: apply /alaa-php-clean-code when installed.",
         "holds no Skill tool and does not preload it"),
    ]

    roots = skill_roots()
    needs_roots = ("resolves to no installed skill", "holds no Skill tool and does not preload it")
    failures, skipped = [], []
    for label, name, tools, deny, skills, body, expected_message in cases:
        if expected_message in needs_roots and not roots:
            skipped.append(label)
            continue
        lines = ["name: fixture", "description: red fixture", "model: sonnet"]
        if tools:
            lines.append(tools)
        if deny is not None:
            lines.append(deny)
        if skills:
            lines.append("skills:")
            lines.extend(f"  - {s}" for s in skills)
        text = "---\n" + "\n".join(lines) + "\n---\n\n" + body + "\n"
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False) as fixture:
            fixture.write(text)
            fixture_path = fixture.name
        try:
            observed, _ = grant_failures(name, frontmatter(fixture_path), roots, body)
        finally:
            os.unlink(fixture_path)
        if not any(expected_message in item for item in observed):
            failures.append(f"{label}: did not observe {expected_message!r}; got {observed}")
    print()
    for label in skipped:
        print(f"SELF-TEST SKIPPED: {label} needs a visible skill root")
    if failures:
        print("SELF-TEST FAILED")
        for line in failures:
            print(f"  - {line}")
        return 1
    print(f"SELF-TEST OK: {len(cases) - len(skipped)} red fixtures each rejected")
    return 0


if __name__ == "__main__":
    sys.exit(self_test() if "--self-test" in sys.argv[1:] else main())
