#!/usr/bin/env python3
"""Check source policy/projections. Exit 0 clean, 1 findings, 2 unavailable proof."""
from __future__ import annotations

import argparse
import copy
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
from claude_model_policy import (AGENT_DIR, ARTIFACTS, DEFAULT_POLICY, REPO_ROOT,
    SKILL_ROOT, WRITER_DIR, CannotRun, digest, load_policy, read_json,
    validate_agent_pin, validate_policy)

FIXTURES = SKILL_ROOT / "scripts/fixtures/claude-policy"


def parse_agent(text):
    # The source repository owns this strict parser; no optional permissive fallback.
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    try:
        from validate_sohrab_skill_pack import MiniYamlError, mini_yaml_load
    except ImportError as exc:
        raise CannotRun("repository MiniYaml parser unavailable; run from the source checkout") from exc
    match = re.match(r"\A---\s*\n(.*?)\n---\s*(?:\n|$)", text.replace("\r\n", "\n"), re.S)
    if not match:
        raise CannotRun("missing or unterminated YAML frontmatter")
    # MiniYaml intentionally accepts duplicate mapping keys. Agent metadata cannot:
    # otherwise two executable pins would be interpreted with silent last-value wins.
    keys = []
    for line in match[1].splitlines():
        if line and not line[0].isspace() and not line.startswith("#"):
            key = re.match(r"([A-Za-z_][A-Za-z0-9_-]*):(?:\s|$)", line)
            if not key:
                raise CannotRun("unsupported top-level YAML key syntax")
            if key[1] in keys:
                raise CannotRun(f"duplicate YAML key: {key[1]}")
            keys.append(key[1])
    try:
        return mini_yaml_load(match[1])
    except (MiniYamlError, ValueError) as exc:
        raise CannotRun(f"unparseable or unsupported YAML: {exc}") from exc


def agent_paths(roots):
    paths = []
    for root in roots:
        if not root.exists():
            raise CannotRun(f"missing agent root: {root}")
        found = [root] if root.is_file() else sorted(root.rglob("*.md"))
        if not found:
            raise CannotRun(f"no Markdown agents at {root}")
        paths.extend(found)
    return paths


def check(policy_path, roots=None):
    canonical = roots is None
    roots = roots or [REPO_ROOT / AGENT_DIR, REPO_ROOT / WRITER_DIR]
    paths = agent_paths(roots)
    tracked = [Path(policy_path), *paths]
    before = {path: digest(path) for path in tracked}
    policy = read_json(policy_path)
    if isinstance(policy, dict) and isinstance(policy.get("profiles"), dict):
        from claude_model_policy import relative_file
        for profile in policy["profiles"].values():
            if isinstance(profile, dict) and profile.get("calibration_status") == "evaluated":
                evidence = relative_file(profile.get("evaluation_evidence"))
                if evidence is not None and evidence.is_file():
                    before[evidence] = digest(evidence)
        corpus = SKILL_ROOT / "assets/evals/claude-agent-comparisons.json"
        if any(isinstance(p, dict) and p.get("calibration_status") == "evaluated" for p in policy["profiles"].values()):
            before[corpus] = digest(corpus)
    policy_errors = validate_policy(policy)
    if policy_errors:
        return policy_errors, len(paths)
    errors, seen = [], set()
    for path in paths:
        agent = parse_agent(path.read_text(encoding="utf-8"))
        errors.extend(f"{path}: {item}" for item in validate_agent_pin(agent, policy, path.name))
        role = agent.get("name") if isinstance(agent, dict) else None
        if isinstance(role, str):
            if role in seen:
                errors.append(f"duplicate executable profile: {role}")
            seen.add(role)
    for root in roots:
        selected = [p for p in paths if p == root or root in p.parents]
        if not any(p.stem in ARTIFACTS for p in selected):
            errors.append(f"root contains no managed artifact: {root}")
    if canonical and (seen != set(ARTIFACTS) or set(paths) != {REPO_ROOT / path for path in ARTIFACTS.values()}):
        errors.append("coverage: all canonical managed artifacts required")
    if paths != agent_paths(roots) or any(digest(path) != value for path, value in before.items()):
        raise CannotRun("scoped inputs changed during validation; freeze the candidate before checking")
    return errors, len(paths)


def self_test():
    policy = load_policy()
    fixtures = read_json(FIXTURES / "policy-cases.json")
    count = 0
    for case in fixtures:
        candidate = copy.deepcopy(policy)
        for operation in case["changes"]:
            parent = candidate
            for key in operation["path"][:-1]:
                parent = parent[key]
            key = operation["path"][-1]
            if operation.get("delete"):
                del parent[key]
            else:
                parent[key] = operation["value"]
        try:
            errors = validate_policy(candidate)
        except CannotRun:
            assert case.get("cannot_run") is True, case["name"]
            count += 1
            continue
        assert not case.get("cannot_run"), case["name"]
        assert bool(errors) == case["findings"], (case["name"], errors)
        count += 1
    role = "alaa-rule-writer"
    good = {"name": role, "model": policy["profiles"][role]["model"], "effort": policy["profiles"][role]["effort"]}
    assert not validate_agent_pin(good, policy, role + ".md")
    for key, value in (("model", "opus"), ("effort", "adaptive"), ("name", "unknown")):
        assert validate_agent_pin({**good, key: value}, policy, role + ".md")
    assert validate_agent_pin(good, policy, "alaa-reviewer.md")
    haiku = copy.deepcopy(policy)
    haiku["profiles"][role].update(model="claude-haiku-4-5-20251001", effort=None)
    assert any("minimum_claude_code" in error for error in validate_policy(haiku))
    # Hypothetical source evidence for a schema-only fixture, not a claimed Haiku version.
    haiku["models"]["claude-haiku-4-5-20251001"]["minimum_claude_code"] = "0.0.0"
    assert not validate_policy(haiku)
    assert not validate_agent_pin({"name":role, "model":"claude-haiku-4-5-20251001"}, haiku, role + ".md")
    assert validate_agent_pin({"name":role, "model":"claude-haiku-4-5-20251001", "effort":None}, haiku, role + ".md")
    for filename in ("duplicate.json", "malformed.json"):
        try:
            read_json(FIXTURES / filename)
        except CannotRun:
            pass
        else:
            raise AssertionError(f"accepted malformed JSON: {filename}")
    for path in sorted(FIXTURES.glob("red-*.md")):
        try:
            parse_agent(path.read_text(encoding="utf-8"))
        except CannotRun:
            count += 1
        else:
            raise AssertionError(f"accepted ambiguous YAML: {path}")
    for value in ([], True, None):
        assert validate_policy(value)
    print(f"OK: {count} policy/parser fixtures plus pin/coverage cases; static proof only")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--policy", type=Path, default=DEFAULT_POLICY)
    parser.add_argument("--agent-root", action="append", type=Path, help="selected source/generated agent file or directory; repeatable")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        if args.self_test:
            self_test()
            return 0
        errors, count = check(args.policy, args.agent_root)
        if errors:
            print("\n".join(errors))
            return 1
        print(f"OK: Claude policy and {count} projections; activation and calibration unproven")
        return 0
    except (CannotRun, OSError, UnicodeError) as exc:
        print(f"could not run: {exc}", file=sys.stderr)
        return 2
    except (ValueError, AssertionError) as exc:
        print(f"FINDINGS: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
