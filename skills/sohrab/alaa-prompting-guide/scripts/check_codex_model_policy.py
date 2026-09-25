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


def self_test() -> None:
    policy = load_policy()
    profile = policy["profiles"]["alaa-rule-writer"]
    good = {"name": "alaa-rule-writer", "model": profile["model"], "model_reasoning_effort": profile["effort"]}
    assert not validate_agent_pin(good, policy)
    for key, value in (("model", "gpt-5.6-sol"), ("model_reasoning_effort", "max"), ("name", "unregistered")):
        assert validate_agent_pin({**good, key: value}, policy), (key, value)
    for model, effort in (("gpt-6-luna", "ultra"), ("gpt-6-sol", "none"), ("gpt-6-astra", "max"), ("gpt-6-sol", "ultra"), ("gpt-5.6-sol", "medium")):
        bad = copy.deepcopy(policy)
        bad["profiles"]["alaa-rule-writer"].update(model=model, effort=effort)
        assert validate_policy(bad), (model, effort)
    bad = copy.deepcopy(policy)
    bad["legacy_exceptions"] = [{"profile": "alaa-rule-writer"}]
    assert validate_policy(bad)
    bad = copy.deepcopy(policy)
    bad["profiles"]["alaa-rule-writer"]["calibration_status"] = "evaluated"
    assert validate_policy(bad)
    for invalid in (True, [], " "):
        bad["profiles"]["alaa-rule-writer"]["evaluation_evidence"] = invalid
        assert validate_policy(bad)
    assert validate_policy([])
    # A documented exception is possible, but never enabled by default.
    legacy = copy.deepcopy(policy)
    legacy["models"]["gpt-5.6-sol"] = {"supported_efforts": ["medium"], "recommended_start": "medium"}
    legacy["profiles"]["alaa-rule-writer"]["model"] = "gpt-5.6-sol"
    legacy["legacy_exceptions"] = [{"profile": "alaa-rule-writer", "model": "gpt-5.6-sol", "effort": "medium", **{key: "synthetic fixture only" for key in ("reason", "scope", "evidence", "review_condition", "approved_by", "approved_on")}}]
    legacy["legacy_exceptions"][0]["approved_on"] = "2026-09-25"
    assert not validate_policy(legacy)


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
        print(f"OK: model policy and {count} agent pins")
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
