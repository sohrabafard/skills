#!/usr/bin/env python3
"""Report and enforce the effective code-intelligence grant of every managed agent.

A static parse proves the file is well-formed; it does not prove what the role can
reach. This resolves each definition the way the runtime does and fails on the
boundaries that matter: a read-only lane holding a mutation tool, a lane holding a
server it was never meant to have, a lane granted a server but unable to reach the
routing contract, and an allowlist that could refuse to launch.

  exit 0  every invariant holds
  exit 1  at least one invariant failed
  exit 2  usage or parse error

Run with --self-test to prove the gate rejects known-bad definitions.
"""
from __future__ import annotations
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AGENTS = os.path.join(ROOT, "agents")

MUTATING = ("replace_", "insert_", "rename_", "safe_delete", "create_text_file",
            "execute_shell_command", "write_memory", "delete_memory", "edit_memory")
FORBIDDEN_BOOST = ("mcp__laravel-boost__tinker", "mcp__laravel-boost__record-rule")
MUST_DENY = ("mcp__laravel-boost__tinker", "mcp__laravel-boost__record-rule",
             "mcp__serena__execute_shell_command")


def frontmatter(path: str) -> dict[str, str]:
    text = open(path, encoding="utf-8").read().replace("\r\n", "\n")
    head = text.split("\n---\n")[0].lstrip("-\n")
    out: dict[str, str] = {}
    for line in head.split("\n"):
        m = re.match(r"^(tools|disallowedTools|model|effort|skills):\s*(.*)$", line)
        if m:
            out[m.group(1)] = m.group(2)
    return out


def csv(value: str) -> list[str]:
    return [x.strip() for x in value.split(",") if x.strip()]


def main() -> int:
    if not os.path.isdir(AGENTS):
        print(f"no agents directory at {AGENTS}", file=sys.stderr)
        return 2
    names = sorted(f for f in os.listdir(AGENTS) if f.endswith(".md"))
    if not names:
        print("no agent definitions found", file=sys.stderr)
        return 2

    failures: list[str] = []
    width = max(len(n) - 3 for n in names)
    print("Effective code-intelligence grant")
    for filename in names:
        name = filename[:-3]
        fm = frontmatter(os.path.join(AGENTS, filename))
        allow = csv(fm["tools"]) if "tools" in fm else None
        deny = csv(fm.get("disallowedTools", ""))

        if allow is None:
            granted = "inherits every tool" + (f", minus {', '.join(deny)}" if deny else "")
            for required in MUST_DENY:
                if required not in deny:
                    failures.append(f"{name}: inherits every tool but does not deny {required}")
        else:
            mcp = [t for t in allow if t.startswith("mcp__")]
            native = [t for t in allow if not t.startswith("mcp__")]
            granted = ", ".join(mcp) or "(no code-intelligence server)"
            if not native:
                failures.append(f"{name}: allowlist contains only MCP entries, so the role "
                                f"cannot launch in a repository without those servers")
            if mcp and "Skill" not in allow:
                failures.append(f"{name}: granted a code-intelligence server but cannot invoke "
                                f"the routing skill; add Skill to its tools")
            for tool in mcp:
                if tool.startswith("mcp__serena__") and any(k in tool for k in MUTATING):
                    failures.append(f"{name}: read-only allowlist holds a mutating semantic tool ({tool})")
                if tool in FORBIDDEN_BOOST:
                    failures.append(f"{name}: holds a forbidden framework tool ({tool})")
        print(f"  {name:<{width}}  {granted}")

    print()
    if failures:
        print("FAILED")
        for line in failures:
            print(f"  - {line}")
        return 1
    print(f"OK: {len(names)} agents, every grant invariant holds")
    return 0


def self_test() -> int:
    """Prove the gate can fail. A checker never observed rejecting a bad input is
    indistinguishable from one that always passes."""
    import tempfile, textwrap
    global AGENTS
    cases = [
        ("read-only lane holding a mutating semantic tool",
         "tools: Read, Bash, Skill, mcp__serena__replace_symbol_body", ""),
        ("granted a server but unable to reach the routing skill",
         "tools: Read, Bash, mcp__codegraph", ""),
        ("allowlist that resolves only to MCP entries",
         "tools: mcp__codegraph, mcp__serena__find_symbol", ""),
        ("forbidden framework tool in an allowlist",
         "tools: Read, Bash, Skill, mcp__laravel-boost__tinker", ""),
        ("inherit-all lane that denies nothing",
         None, "disallowedTools: mcp__serena__find_symbol"),
    ]
    failures = []
    for label, tools, deny in cases:
        with tempfile.TemporaryDirectory() as tmp:
            agents = os.path.join(tmp, "agents")
            os.makedirs(agents)
            body = textwrap.dedent(f"""\
                ---
                name: fixture
                description: red fixture
                model: sonnet
                {tools or deny}
                ---

                body
                """)
            open(os.path.join(agents, "fixture.md"), "w", encoding="utf-8").write(body)
            AGENTS = agents
            code = main()
            if code != 1:
                failures.append(f"{label}: expected exit 1, got {code}")
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
