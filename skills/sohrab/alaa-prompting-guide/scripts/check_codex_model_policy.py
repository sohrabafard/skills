#!/usr/bin/env python3
"""Validate policy and optional agent files. Exit 0 clean, 1 findings, 2 cannot run."""
from __future__ import annotations

import argparse
import sys
import tomllib
from pathlib import Path

sys.dont_write_bytecode = True
from codex_model_policy import PolicyLoadError, load_policy, validate_agent_pin


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--policy", type=Path)
    parser.add_argument("--agent-root", action="append", type=Path, default=[], help="TOML file or directory of agent TOMLs; repeatable")
    args = parser.parse_args()
    try:
        policy = load_policy(args.policy)
        findings, count = [], 0
        for root in args.agent_root:
            paths = [root] if root.is_file() else sorted(root.rglob("*.toml"))
            if not paths:
                raise OSError(f"no agent TOMLs at {root}")
            for path in paths:
                agent = tomllib.loads(path.read_text(encoding="utf-8"))
                findings.extend(f"{path}: {item}" for item in validate_agent_pin(agent, policy))
                count += 1
        if findings:
            print("\n".join(findings))
            return 1
        print(f"OK: model policy and {count} model-neutral agents")
        return 0
    except (PolicyLoadError, tomllib.TOMLDecodeError) as exc:
        print(f"could not run: {exc}", file=sys.stderr)
        return 2
    except ValueError as exc:
        print(f"FINDINGS: {exc}", file=sys.stderr)
        return 1
    except (OSError, UnicodeError) as exc:
        print(f"could not run: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
