"""Preserve managed agents and check a model-only update. Recovery stays outside Git."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import tomllib
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PACK = ROOT / "skills/sohrab/alaa-codex-orchestrator"
GUIDE = ROOT / "skills/sohrab/alaa-prompting-guide"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def managed_names() -> list[str]:
    return sorted([p.name for p in (PACK / "agents").glob("*.toml")] + ["alaa-rule-writer.toml", ".alaa-codex-orchestrator.version", ".alaa-codex-orchestrator.mcp-inventory"])


def reconcile_disabled_overlays(old: dict, new: dict) -> list[dict]:
    """Permit only disabled transport refreshes and new explicit-deny overlays.

    The official materializer owns live inventory; this permits no enabled grant,
    tools, instruction or sandbox change. Unknown new servers must stay disabled.
    """
    changes = []
    previous = old.get("mcp_servers", {})
    current = new.get("mcp_servers", {})
    assert previous.keys() <= current.keys(), "an installed MCP override was removed"
    for server, cfg in current.items():
        if server not in previous:
            assert cfg.get("enabled") is False and set(cfg) <= {"command", "url", "enabled"}, f"new server is not a pure explicit deny: {server}"
            changes.append({"server": server, "change": "new explicit disabled override"})
            previous[server] = cfg
            continue
        before = previous[server]
        if before == cfg:
            continue
        assert before.get("enabled") is False and cfg.get("enabled") is False, f"enabled MCP configuration changed: {server}"
        assert set(before) == set(cfg), f"MCP transport/configuration shape changed: {server}"
        assert {k: v for k, v in before.items() if k not in ("command", "url")} == {k: v for k, v in cfg.items() if k not in ("command", "url")}, f"MCP permission fields changed: {server}"
        changes.append({"server": server, "change": "disabled transport discriminator refreshed from live inventory"})
        previous[server] = cfg
    return changes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("backup", "check"))
    parser.add_argument("--agents", required=True, type=Path)
    parser.add_argument("--recovery", required=True, type=Path)
    parser.add_argument("--staged", type=Path, help="Inspect materialized pack before installation")
    args = parser.parse_args()
    try:
        names = managed_names()
        if args.mode == "backup":
            args.recovery.mkdir(parents=True, exist_ok=False)
            for name in names:
                source = args.agents / name
                if not source.is_file():
                    raise OSError(f"missing managed installed file: {name}")
                destination = args.recovery / name
                shutil.copy2(source, destination)
                assert digest(source) == digest(destination), f"backup mismatch: {name}"
            manifest = {"managed": {name: digest(args.recovery / name) for name in names}, "unrelated": {p.name: digest(p) for p in args.agents.iterdir() if p.is_file() and p.name not in names}, "global_config_sha256": digest(args.agents.parent / "config.toml")}
            (args.recovery / "recovery-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
            (HERE / "preinstall.json").write_text(json.dumps({"managed_file_count": len(names), "managed_hashes": manifest["managed"], "unrelated_hashes": manifest["unrelated"], "global_config_sha256": manifest["global_config_sha256"], "recovery_verified": True, "recovery_location": "Caller-supplied task cache outside Git; see installation receipt."}, indent=2) + "\n", encoding="utf-8")
            print(f"PASS: preserved and hash-verified {len(names)} managed files outside Git")
            return 0

        manifest = json.loads((args.recovery / "recovery-manifest.json").read_text())
        policy = json.loads((GUIDE / "assets/codex-model-policy.json").read_text())
        migrated = []
        inactive_overlay_changes = {}
        for name in names:
            assert digest(args.recovery / name) == manifest["managed"][name], f"recovery changed: {name}"
            if not name.endswith(".toml"):
                continue
            old = tomllib.loads((args.recovery / name).read_text(encoding="utf-8"))
            if old["model"] == "gpt-6-sol":
                old["model"] = "gpt-6.1-sol"
                migrated.append(old["name"])
            source = (args.staged / name) if args.staged and name != "alaa-rule-writer.toml" else (GUIDE / "assets/rule-writer/codex/alaa-rule-writer.toml" if args.staged else args.agents / name)
            new = tomllib.loads(source.read_text(encoding="utf-8"))
            changes = reconcile_disabled_overlays(old, new)
            if changes:
                inactive_overlay_changes[new["name"]] = changes
            assert old == new, f"installed/staged non-model semantic drift: {name}"
            profile = policy["profiles"][new["name"]]
            assert new["model"] == profile["model"] and new["model_reasoning_effort"] == profile["effort"], f"pin mismatch: {name}"
        assert len(migrated) == 15
        assert digest(args.agents.parent / "config.toml") == manifest["global_config_sha256"], "global configuration changed"
        current_unrelated = {p.name: digest(p) for p in args.agents.iterdir() if p.is_file() and p.name not in names}
        assert current_unrelated == manifest["unrelated"], "unrelated installed file changed"
        if not args.staged:
            assert (args.agents / ".alaa-codex-orchestrator.version").read_text().strip() == "4.1.0"
            (HERE / "installed-verification.json").write_text(json.dumps({"migrated_agents": migrated, "efforts_and_instructions_preserved": True, "active_mcp_grants_preserved": True, "inactive_overlay_changes": inactive_overlay_changes, "global_configuration_preserved": True, "unrelated_files_preserved": True, "mcp_inventory_sha256": digest(args.agents / ".alaa-codex-orchestrator.mcp-inventory"), "managed_hashes": {name: digest(args.agents / name) for name in names}}, indent=2) + "\n", encoding="utf-8")
        print(f"PASS: {len(migrated)} model pins updated; efforts, instructions, active grants, config and unrelated files preserved; {len(inactive_overlay_changes)} roles have recorded inactive-overlay refreshes")
        return 0
    except AssertionError as exc:
        print(f"FINDINGS: {exc}")
        return 1
    except (OSError, ValueError) as exc:
        print(f"could not run: {exc}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
