#!/usr/bin/env python3
"""Validate and materialize fail-closed MCP grants for managed Codex agents.

Codex custom-agent files are config layers. Omitting ``mcp_servers`` inherits the
parent configuration, but a portable source file cannot safely restate a machine's
transport. Managed sources are therefore marked templates. The installer resolves
the live parent inventory and emits the catalog's exact grant for each role while
disabling every unassigned server. It preserves each transport discriminator so the
merged role parses without committing machine-specific paths.

  exit 0  every invariant holds
  exit 1  at least one invariant failed
  exit 2  usage or parse error

Run with --self-test to prove the gate rejects known-bad definitions.
"""
from __future__ import annotations
import hashlib, json, os, re, shutil, subprocess, sys

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
        elif value == "{}":
            parsed = {}
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
TEMPLATE_MARKER = "# grant-template: materialize-live-parent-mcp"
INVENTORY_FILE = ".alaa-codex-orchestrator.mcp-inventory"
SAFE_NAME = re.compile(r"^[A-Za-z0-9_-]+$")

SERENA_READ = [
    "find_symbol",
    "get_symbols_overview",
    "find_referencing_symbols",
    "find_declaration",
    "find_implementations",
    "get_diagnostics_for_file",
]
BOOST_DOCS = ["search-docs", "application-info"]
BOOST_ROUTING = ["get-absolute-url"]
BOOST_SCHEMA = ["database-schema", "database-connections"]
BOOST_ERRORS = ["last-error", "read-log-entries"]
BOOST_BROWSER = ["browser-logs"]


def _only(tools: list[str]) -> dict[str, list[str]]:
    return {"enabled_tools": tools}


ROLE_POLICY: dict[str, dict[str, dict]] = {
    "alaa-accessibility-reviewer": {"laravel-boost": _only(BOOST_DOCS + BOOST_ROUTING)},
    "alaa-adversarial-reviewer": {
        "codegraph": {}, "serena": _only(SERENA_READ),
        "laravel-boost": _only(BOOST_DOCS + BOOST_SCHEMA),
    },
    "alaa-api-contract-reviewer": {
        "codegraph": {}, "laravel-boost": _only(BOOST_DOCS + BOOST_ROUTING + BOOST_SCHEMA),
    },
    "alaa-architecture-critic": {
        "codegraph": {}, "laravel-boost": _only(BOOST_DOCS + BOOST_SCHEMA),
    },
    "alaa-browser-qa": {
        "laravel-boost": _only(BOOST_DOCS + BOOST_ROUTING + BOOST_BROWSER + BOOST_ERRORS),
    },
    "alaa-dependency-auditor": {"laravel-boost": _only(BOOST_DOCS)},
    "alaa-documenter": {"laravel-boost": _only(BOOST_DOCS + BOOST_ROUTING)},
    "alaa-explorer": {
        "codegraph": {}, "laravel-boost": _only(BOOST_DOCS + BOOST_ROUTING),
    },
    "alaa-failure-analyst": {
        "codegraph": {}, "serena": _only(SERENA_READ),
        "laravel-boost": _only(BOOST_DOCS + BOOST_ERRORS + BOOST_BROWSER),
    },
    "alaa-implementer-sol": {
        "codegraph": {},
        "serena": {"disabled_tools": ["execute_shell_command"]},
        "laravel-boost": {"disabled_tools": ["tinker", "record-rule"]},
    },
    "alaa-implementer": {
        "codegraph": {},
        "serena": {"disabled_tools": ["execute_shell_command"]},
        "laravel-boost": {"disabled_tools": ["tinker", "record-rule"]},
    },
    "alaa-migration-guardian": {
        "codegraph": {}, "laravel-boost": _only(BOOST_DOCS + BOOST_SCHEMA),
    },
    "alaa-observability-reviewer": {
        "codegraph": {}, "laravel-boost": _only(BOOST_DOCS + BOOST_ERRORS + BOOST_BROWSER),
    },
    "alaa-performance-profiler": {
        "codegraph": {}, "laravel-boost": _only(BOOST_DOCS + BOOST_SCHEMA + BOOST_ERRORS),
    },
    "alaa-release-guardian": {"laravel-boost": _only(BOOST_DOCS)},
    "alaa-researcher": {"laravel-boost": _only(BOOST_DOCS)},
    "alaa-reviewer": {
        "codegraph": {}, "serena": _only(SERENA_READ),
        "laravel-boost": _only(BOOST_DOCS + BOOST_SCHEMA),
    },
    "alaa-security-reviewer": {
        "codegraph": {}, "serena": _only(SERENA_READ),
        "laravel-boost": _only(BOOST_DOCS + BOOST_SCHEMA),
    },
    "alaa-spec-analyst": {"codegraph": {}, "laravel-boost": _only(BOOST_DOCS)},
    "alaa-test-strategist": {
        "codegraph": {}, "laravel-boost": _only(BOOST_DOCS + BOOST_SCHEMA),
    },
    "alaa-verifier": {},
}


def _agent_paths(agents_dir: str) -> list[str]:
    if not os.path.isdir(agents_dir):
        raise OSError(f"no agents directory at {agents_dir}")
    paths = sorted(
        os.path.join(agents_dir, name)
        for name in os.listdir(agents_dir)
        if name.endswith(".toml")
    )
    if not paths:
        raise OSError(f"no agent definitions found in {agents_dir}")
    return paths


def _template_failures(name: str, text: str, data: dict) -> list[str]:
    failures = []
    if TEMPLATE_MARKER not in text:
        failures.append(f"{name}: inherited MCP omission lacks the installer materialization marker")
    if "mcp_servers" in data:
        failures.append(f"{name}: source template must not embed partial or machine-specific MCP transports")
    return failures


def _inventory() -> dict[str, tuple[str, str, bool]]:
    codex = shutil.which("codex")
    if not codex:
        raise OSError("codex is required to resolve the live parent MCP inventory")
    result = subprocess.run(
        [codex, "mcp", "list", "--json"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip().replace("\n", " | ")
        raise OSError(f"codex mcp list --json exited {result.returncode}: {detail}")
    try:
        raw = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise ValueError(f"codex mcp list --json returned invalid JSON: {exc}") from exc

    inventory: dict[str, tuple[str, str, bool]] = {}
    for entry in raw:
        name = entry.get("name")
        transport = entry.get("transport") or {}
        parent_enabled = entry.get("enabled")
        if not isinstance(name, str) or not SAFE_NAME.fullmatch(name):
            raise ValueError(f"unsupported MCP server name {name!r}; expected letters, digits, '_' or '-'")
        if not isinstance(parent_enabled, bool):
            raise ValueError(f"{name}: live inventory has no boolean enabled state")
        if transport.get("type") == "stdio" and isinstance(transport.get("command"), str):
            discriminator = ("command", transport["command"], parent_enabled)
        elif transport.get("type") in {"streamable_http", "sse"} and isinstance(transport.get("url"), str):
            discriminator = ("url", transport["url"], parent_enabled)
        else:
            raise ValueError(f"{name}: unsupported or incomplete transport {transport.get('type')!r}")
        if name in inventory:
            raise ValueError(f"duplicate MCP server in live inventory: {name}")
        inventory[name] = discriminator
    return inventory


def _fingerprint(inventory: dict[str, tuple[str, str, bool]]) -> str:
    payload = json.dumps(inventory, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _expected_overlay(
    name: str, inventory: dict[str, tuple[str, str, bool]]
) -> dict[str, dict]:
    policy = ROLE_POLICY[name]
    overlay = {}
    for server_name, (key, value, parent_enabled) in sorted(inventory.items()):
        cfg = {key: value}
        assignment = policy.get(server_name)
        if parent_enabled and assignment is not None:
            cfg["enabled"] = True
            cfg.update(assignment)
        else:
            cfg["enabled"] = False
        overlay[server_name] = cfg
    return overlay


def _normalized_cfg(cfg: dict) -> dict:
    normalized = dict(cfg)
    for key in ("enabled_tools", "disabled_tools"):
        if isinstance(normalized.get(key), list):
            normalized[key] = sorted(set(normalized[key]))
    return normalized


def _resolved_failures(
    name: str, data: dict, inventory: dict[str, tuple[str, str, bool]]
) -> list[str]:
    failures = []
    servers = data.get("mcp_servers")
    expected = _expected_overlay(name, inventory)
    if not expected and servers in (None, {}):
        return []
    if not isinstance(servers, dict):
        return [f"{name}: resolved role omits mcp_servers and inherits the live parent grant"]
    actual_names = set(servers)
    expected_names = set(expected)
    if actual_names != expected_names:
        missing = sorted(expected_names - actual_names)
        extra = sorted(actual_names - expected_names)
        if missing:
            failures.append(f"{name}: live MCP servers not overridden: {', '.join(missing)}")
        if extra:
            failures.append(f"{name}: stale MCP overrides not in the live inventory: {', '.join(extra)}")
    for server_name in sorted(actual_names & expected_names):
        cfg = servers[server_name]
        if not isinstance(cfg, dict):
            failures.append(f"{name}: {server_name} override is not a table")
            continue
        expected_cfg = _normalized_cfg(expected[server_name])
        actual_cfg = _normalized_cfg(cfg)
        if actual_cfg != expected_cfg:
            failures.append(
                f"{name}: {server_name} grant differs from the live catalog assignment "
                f"(expected {expected_cfg!r}, got {actual_cfg!r})"
            )
    return failures


def validate_templates(agents_dir: str = AGENTS) -> int:
    try:
        paths = _agent_paths(agents_dir)
    except OSError as exc:
        print(exc, file=sys.stderr)
        return 2
    actual_names = {os.path.basename(path)[:-5] for path in paths}
    expected_names = set(ROLE_POLICY)
    if actual_names != expected_names:
        missing = sorted(expected_names - actual_names)
        extra = sorted(actual_names - expected_names)
        if missing:
            print(f"missing catalog roles: {', '.join(missing)}", file=sys.stderr)
        if extra:
            print(f"uncatalogued roles: {', '.join(extra)}", file=sys.stderr)
        return 2

    failures = []
    for path in paths:
        name = os.path.basename(path)[:-5]
        try:
            text = open(path, encoding="utf-8").read()
            data = _load(path)
        except (ValueError, OSError) as exc:
            print(f"{name}: {exc}", file=sys.stderr)
            return 2
        failures.extend(_template_failures(name, text, data))
    if failures:
        print("FAILED")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(f"OK: {len(paths)} transport-neutral templates have exact per-role grant policies")
    return 0


def validate_resolved(
    agents_dir: str, inventory: dict[str, tuple[str, str, bool]] | None = None
) -> int:
    try:
        paths = _agent_paths(agents_dir)
        inventory = inventory if inventory is not None else _inventory()
    except (OSError, ValueError) as exc:
        print(exc, file=sys.stderr)
        return 2
    failures = []
    for path in paths:
        name = os.path.basename(path)[:-5]
        try:
            data = _load(path)
        except (ValueError, OSError) as exc:
            print(f"{name}: {exc}", file=sys.stderr)
            return 2
        failures.extend(_resolved_failures(name, data, inventory))
    if failures:
        print("FAILED")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(f"OK: {len(paths)} resolved agents match exact grants across {len(inventory)} live MCP servers")
    return 0


def materialize(source_dir: str, output_dir: str) -> int:
    template_code = validate_templates(source_dir)
    if template_code != 0:
        return template_code
    if os.path.exists(output_dir):
        print(f"output directory already exists: {output_dir}", file=sys.stderr)
        return 2
    try:
        inventory = _inventory()
        os.makedirs(output_dir)
        for source_path in _agent_paths(source_dir):
            name = os.path.basename(source_path)[:-5]
            blocks = []
            for server_name, cfg in sorted(_expected_overlay(name, inventory).items()):
                lines = [f"[mcp_servers.{server_name}]"]
                for key in ("command", "url", "enabled", "enabled_tools", "disabled_tools"):
                    if key in cfg:
                        value = cfg[key]
                        lines.append(f"{key} = {json.dumps(value, ensure_ascii=True)}")
                blocks.append("\n".join(lines))
            suffix = ("\n\n" + "\n\n".join(blocks) + "\n") if blocks else "\n"
            text = open(source_path, encoding="utf-8").read().rstrip() + suffix
            destination = os.path.join(output_dir, os.path.basename(source_path))
            with open(destination, "w", encoding="utf-8", newline="\n") as handle:
                handle.write(text)
        with open(os.path.join(output_dir, INVENTORY_FILE), "w", encoding="ascii", newline="\n") as handle:
            handle.write(_fingerprint(inventory) + "\n")
    except (OSError, ValueError) as exc:
        print(exc, file=sys.stderr)
        return 2
    return validate_resolved(output_dir, inventory)


def self_test() -> int:
    inventory = {
        "serena": ("command", "serena", True),
        "remote-docs": ("url", "https://example.invalid/mcp", True),
    }
    cases = [
        ("unmarked inherited omission", _template_failures("fixture", "", {}), "lacks"),
        ("partial source definition", _template_failures(
            "fixture", TEMPLATE_MARKER, {"mcp_servers": {"serena": {"enabled": False}}}), "must not embed"),
        ("resolved omission", _resolved_failures("alaa-reviewer", {}, inventory), "inherits"),
        ("missing inherited server", _resolved_failures(
            "alaa-reviewer", {"mcp_servers": {
                "serena": {"command": "serena", "enabled": True, "enabled_tools": SERENA_READ},
            }}, inventory), "not overridden"),
        ("unassigned server left enabled", _resolved_failures(
            "alaa-reviewer", {"mcp_servers": {
                "serena": {"command": "serena", "enabled": True, "enabled_tools": SERENA_READ},
                "remote-docs": {"url": "https://example.invalid/mcp", "enabled": True},
            }}, inventory), "grant differs"),
        ("read-only semantic server overgranted", _resolved_failures(
            "alaa-reviewer", {"mcp_servers": {
                "serena": {"command": "serena", "enabled": True},
                "remote-docs": {"url": "https://example.invalid/mcp", "enabled": False},
            }}, inventory), "grant differs"),
    ]
    failures = []
    for label, observed, expected_message in cases:
        if not any(expected_message in item for item in observed):
            failures.append(f"{label}: did not observe {expected_message!r}; got {observed}")
    if failures:
        print("SELF-TEST FAILED")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(f"SELF-TEST OK: {len(cases)} red fixtures each rejected")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        sys.exit(validate_templates())
    if args == ["--self-test"]:
        sys.exit(self_test())
    if len(args) == 2 and args[0] == "--agents-dir":
        sys.exit(validate_templates(args[1]))
    if len(args) == 2 and args[0] == "--resolved-agents-dir":
        sys.exit(validate_resolved(args[1]))
    if len(args) == 3 and args[0] == "--materialize":
        sys.exit(materialize(args[1], args[2]))
    if args == ["--inventory-fingerprint"]:
        try:
            print(_fingerprint(_inventory()))
            sys.exit(0)
        except (OSError, ValueError) as exc:
            print(exc, file=sys.stderr)
            sys.exit(2)
    print(
        "usage: check_agent_grants.py [--self-test | --agents-dir PATH | "
        "--resolved-agents-dir PATH | --materialize SOURCE OUTPUT | --inventory-fingerprint]",
        file=sys.stderr,
    )
    sys.exit(2)
