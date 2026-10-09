#!/usr/bin/env python3
"""Validate policy and optional agent files. Exit 0 clean, 1 findings, 2 cannot run."""
from __future__ import annotations

import argparse
import copy
import sys
import tomllib
from pathlib import Path

sys.dont_write_bytecode = True
from codex_model_policy import PolicyLoadError, load_policy, validate_agent_pin, validate_policy
from task_model_controls import selection_self_test


def self_test() -> None:
    policy = load_policy()
    pairs = ({"model":"gpt-6-luna", "effort":"low"}, {"model":"gpt-6.1-sol", "effort":"high"})
    count = selection_self_test(policy, pairs)
    for role, profile in policy["profiles"].items():
        if profile["selection_mode"] != "task-selected":
            continue
        good = {"name":role}
        assert not validate_agent_pin(good, policy)
        for key, value in (("model", "gpt-6-astra"), ("model_reasoning_effort", "high"), ("effort", "low")):
            assert validate_agent_pin({**good,key:value},policy)
        missing = copy.deepcopy(policy)
        del missing["profiles"][role]
        assert any("coverage" in error for error in validate_policy(missing))
        fixed = copy.deepcopy(policy)
        fixed["profiles"][role]["model"] = "gpt-6-astra"
        assert validate_policy(fixed)
    assert validate_agent_pin({"name":"unregistered"},policy)
    for key,value in (("schema_version",True),("schema_version",1),("verified_on","2026-02-30")):
        bad=copy.deepcopy(policy);bad[key]=value;assert validate_policy(bad)
    for model,effort in (("gpt-6-luna","ultra"),("gpt-6.1-sol","none")):
        from task_model_controls import validate_task_selection
        assert validate_task_selection("alaa-reviewer",{"model":model,"effort":effort},policy)
    bad=copy.deepcopy(policy);bad["models"]["gpt-6.1-sol-preview"]=bad["models"]["gpt-6.1-sol"].copy()
    assert validate_policy(bad)
    bad=copy.deepcopy(policy);bad["models"]["gpt-6.1-sol"]["recommended_start"]="none"
    assert validate_policy(bad)
    assert validate_policy([])
    print(f"OK: {count} roles with distinct task pairs, explicit controls, coverage and stale-pin rejection")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--policy", type=Path)
    parser.add_argument("--agent-root", action="append", type=Path, default=[], help="TOML file or directory of agent TOMLs; repeatable")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        if args.self_test:
            self_test()
            print("OK: model policy positive and negative cases")
            return 0
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
    except AssertionError as exc:
        print(f"SELF-TEST FAILED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
