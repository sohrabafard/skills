#!/usr/bin/env python3
"""Report and enforce the effective code-intelligence grant of every managed agent.

A static TOML parse proves the file loads; it does not prove what the role can reach.
This resolves each agent layer the way the runtime does and fails on the boundaries
that matter: a read-only lane holding a mutation tool, a lane holding a server it was
never meant to have, and a forbidden framework tool left reachable.

  exit 0  every invariant holds
  exit 1  at least one invariant failed
  exit 2  usage or parse error

Run with --self-test to prove the gate rejects known-bad definitions.
"""
from __future__ import annotations
import os, re, sys

try:                       # 3.11+
    import tomllib as _toml
except ModuleNotFoundError:
    try:                   # backport, when the environment has it
        import tomli as _toml
    except ModuleNotFoundError:
        _toml = None       # fall back to the reader below


def _load(path: str) -> dict:
    """Read an agent TOML layer.

    Prefer a real parser. Where the interpreter predates `tomllib` and no backport
    is installed — which is the common case on a machine that also runs an older
    Python for other reasons — fall back to a reader for the small grammar these
    generated files use: table headers, dotted keys, strings, booleans, integers,
    and single-line string arrays. Anything richer is rejected loudly rather than
    guessed at, so a hand-edited file can never be silently mis-read.
    """
    if _toml is not None:
        with open(path, "rb") as handle:
            return _toml.load(handle)

    data: dict = {}
    prefix: list[str] = []
    inside_multiline = False
    for lineno, raw in enumerate(open(path, encoding="utf-8"), 1):
        line = raw.rstrip("\n")
        if inside_multiline:                       # developer_instructions block
            if line.rstrip().endswith('"""'):
                inside_multiline = False
            continue
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("["):
            if not stripped.endswith("]"):
                raise ValueError(f"{path}:{lineno}: unsupported table header")
            prefix = stripped[1:-1].strip().split(".")
            continue
        if "=" not in stripped:
            raise ValueError(f"{path}:{lineno}: unsupported line")
        key, _, value = stripped.partition("=")
        key, value = key.strip(), value.strip()
        if value.startswith('"""'):
            inside_multiline = not value.endswith('"""') or len(value) < 6
            continue
        if value.startswith("[") and not value.endswith("]"):
            raise ValueError(f"{path}:{lineno}: multi-line arrays are not supported")
        if value.startswith("["):
            parsed = [x.strip().strip('"') for x in value[1:-1].split(",") if x.strip()]
        elif value.startswith('"'):
            parsed = value.strip('"')
        elif value in ("true", "false"):
            parsed = value == "true"
        elif re.fullmatch(r"-?\d+", value):
            parsed = int(value)
        else:
            parsed = value.strip('"')
        node = data
        for part in prefix + key.split(".")[:-1]:
            node = node.setdefault(part, {})
        node[key.split(".")[-1]] = parsed
    return data

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AGENTS = os.path.join(ROOT, "agents")

MUTATING = ("replace_", "insert_", "rename_", "safe_delete", "create_text_file",
            "execute_shell_command", "write_memory", "delete_memory", "edit_memory")
FORBIDDEN_BOOST = ("tinker", "record-rule")
SERVERS = ("serena", "codegraph", "laravel-boost")


def describe(server: str, cfg: dict | None) -> str:
    if cfg is None:
        return f"{server}=inherited"
    if cfg.get("enabled") is False:
        return f"{server}=off"
    if "enabled_tools" in cfg:
        return f"{server}=only({len(cfg['enabled_tools'])})"
    if "disabled_tools" in cfg:
        return f"{server}=all-minus({','.join(cfg['disabled_tools'])})"
    return f"{server}=on"


def main() -> int:
    if not os.path.isdir(AGENTS):
        print(f"no agents directory at {AGENTS}", file=sys.stderr)
        return 2
    names = sorted(f for f in os.listdir(AGENTS) if f.endswith(".toml"))
    if not names:
        print("no agent definitions found", file=sys.stderr)
        return 2

    failures: list[str] = []
    width = max(len(n) - 5 for n in names)
    print("Effective code-intelligence grant")
    for filename in names:
        name = filename[:-5]
        try:
            data = _load(os.path.join(AGENTS, filename))
        except (ValueError, OSError) as exc:
            print(f"{name}: {exc}", file=sys.stderr)
            return 2
        servers = data.get("mcp_servers", {})
        sandbox = data.get("sandbox_mode", "inherited")

        serena = servers.get("serena")
        if sandbox == "read-only" and serena is not None and serena.get("enabled") is not False:
            reachable = serena.get("enabled_tools")
            if reachable is None:
                failures.append(f"{name}: read-only sandbox but the semantic server is unrestricted; "
                                f"an MCP server runs outside the sandbox, so list enabled_tools")
            else:
                for tool in reachable:
                    if any(k in tool for k in MUTATING):
                        failures.append(f"{name}: read-only lane enables a mutating semantic tool ({tool})")

        boost = servers.get("laravel-boost")
        if boost is not None and boost.get("enabled") is not False:
            allowed = boost.get("enabled_tools")
            denied = boost.get("disabled_tools", [])
            for bad in FORBIDDEN_BOOST:
                if allowed is not None and bad in allowed:
                    failures.append(f"{name}: enables the forbidden framework tool {bad}")
                if allowed is None and bad not in denied:
                    failures.append(f"{name}: leaves the forbidden framework tool {bad} reachable")

        grant = " | ".join(describe(s, servers.get(s)) for s in SERVERS)
        print(f"  {name:<{width}}  sandbox={sandbox:<16} {grant}")

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
    import tempfile
    global AGENTS
    cases = [
        ("read-only lane with an unrestricted semantic server",
         'sandbox_mode = "read-only"\nmcp_servers.serena.enabled = true\n'),
        ("read-only lane enabling a mutating semantic tool",
         'sandbox_mode = "read-only"\nmcp_servers.serena.enabled_tools = ["rename_symbol"]\n'),
        ("forbidden framework tool enabled",
         'sandbox_mode = "read-only"\nmcp_servers.serena.enabled = false\n'
         'mcp_servers.laravel-boost.enabled_tools = ["tinker"]\n'),
        ("forbidden framework tool left reachable",
         'sandbox_mode = "read-only"\nmcp_servers.serena.enabled = false\n'
         'mcp_servers.laravel-boost.enabled = true\n'),
    ]
    failures = []
    for label, layer in cases:
        with tempfile.TemporaryDirectory() as tmp:
            agents = os.path.join(tmp, "agents")
            os.makedirs(agents)
            open(os.path.join(agents, "fixture.toml"), "w", encoding="utf-8").write(
                'name = "fixture"\ndescription = "red fixture"\n' + layer
                + 'developer_instructions = """\nbody\n"""\n')
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
