#!/usr/bin/env python3
"""Validate the representative evaluation corpus, not model quality. 0/1/2 exit contract."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
from codex_model_policy import load_policy, PolicyLoadError, validate_task_selection, validate_policy

CORPUS = Path(__file__).resolve().parents[1] / "assets/evals/agent-comparisons.json"
EXPECTED = {"exploration", "bounded-implementation", "debugging", "known-defect-review", "architecture", "instruction-rewrite", "documentation", "failed-check"}


def validate(corpus: dict, policy: dict) -> list[str]:
    return _validate(corpus, policy, validate_task_selection)


def _validate(corpus: dict, policy: dict, pair_validator) -> list[str]:
    if not isinstance(corpus, dict) or type(corpus.get("schema_version")) is not int or corpus.get("schema_version") != 1:
        return ["unsupported corpus schema"]
    errors = []
    if corpus.get("policy_version") != policy["policy_version"]:
        errors.append("corpus policy version drift")
    scenarios = corpus.get("scenarios")
    if not isinstance(scenarios, list):
        return errors + ["scenarios must be a list"]
    names = [case.get("id") for case in scenarios if isinstance(case, dict)]
    if len(names) != len(scenarios) or any(not isinstance(name, str) for name in names) or len(names) != len(EXPECTED) or set(names) != EXPECTED:
        errors.append("exactly eight distinct representative scenarios are required")
    for case in scenarios:
        if not isinstance(case, dict):
            errors.append("scenario must be an object")
            continue
        name = case.get("id")
        if case.get("repetitions") != 2 or case.get("status") != "unrun":
            errors.append(f"{name}: reusable corpus requires two repetitions and unrun status; results belong in evidence")
        if not isinstance(case.get("prompt"), str) or len(case["prompt"].strip()) < 40:
            errors.append(f"{name}: concrete task prompt required")
        inputs = case.get("inputs")
        if not isinstance(inputs, dict) or not inputs or any(not isinstance(v, str) or len(v.strip()) < 20 for v in inputs.values()):
            errors.append(f"{name}: substantive input fixtures required")
        for key in ("acceptance_criteria", "forbidden_actions"):
            values = case.get(key)
            if not isinstance(values, list) or len(values) < 2 or any(not isinstance(v, str) or not v.strip() for v in values):
                errors.append(f"{name}: explicit {key} required")
        role = case.get("profile")
        profile = policy["profiles"].get(role) if isinstance(role, str) else None
        candidate, comparator = case.get("candidate"), case.get("comparator")
        if not isinstance(candidate, dict) or not isinstance(comparator, dict):
            errors.append(f"{name}: candidate and comparator must be objects")
            continue
        if not profile or pair_validator(role, candidate, policy):
            errors.append(f"{name}: explicit candidate task pair/role invalid")
        if sum(candidate.get(key) != comparator.get(key) for key in ("model", "effort")) != 1:
            errors.append(f"{name}: comparison must change exactly one factor")
        for config in (candidate, comparator):
            if pair_validator(role, config, policy):
                errors.append(f"{name}: unsupported comparison pair")
    return errors


def validate_history(manifest_path: Path) -> list[str]:
    """Check byte integrity, provenance-field syntax and support, not source identity."""
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict) or type(manifest.get("schema_version")) is not int or manifest.get("schema_version") != 1 or manifest.get("purpose") != "historical-only":
        return ["historical-only manifest schema required"]
    if not isinstance(manifest.get("source_commit"), str) or not re.fullmatch(r"[0-9a-f]{40}", manifest["source_commit"]):
        return ["archive source_commit requires 40 lowercase hexadecimal characters; identity requires independent verification"]
    if manifest.get("evidence_date") != "2026-10-09" or manifest.get("archived_on") != "2026-10-12":
        return ["archive evidence and capture dates drift"]
    entries = manifest.get("files")
    expected = {"agent-comparisons.json": "assets/evals/agent-comparisons.json", "codex-model-policy.json": "assets/codex-model-policy.json"}
    if not isinstance(entries, list) or len(entries) != 2 or any(not isinstance(entry, dict) or entry.get("file") not in expected for entry in entries):
        return ["archive requires original corpus and policy entries"]
    if {entry["file"] for entry in entries} != set(expected):
        return ["duplicate archive entry"]
    values = {}
    for entry in entries:
        name = entry["file"]
        if entry.get("source") != "skills/sohrab/alaa-prompting-guide/" + expected[name]:
            return ["archive declared source path drift"]
        data = (manifest_path.parent / name).read_bytes()
        if entry.get("sha256") != hashlib.sha256(data).hexdigest() or type(entry.get("bytes")) is not int or entry["bytes"] != len(data):
            return [f"archive hash/size drift: {name}"]
        values[name] = json.loads(data.decode("utf-8"))
    policy = values["codex-model-policy.json"]
    if not isinstance(policy, dict) or not isinstance(policy.get("models"), dict) or not isinstance(policy["models"].get("gpt-6-sol"), dict):
        return ["original policy snapshot missing"]
    # Validate the structural snapshot through its owner on a private ordinary-safe
    # copy; never return/load the historically enabled policy as task authority.
    ordinary = copy.deepcopy(policy)
    ordinary["models"]["gpt-6-sol"]["selection_enabled"] = False
    errors = validate_policy(ordinary)
    if errors:
        return errors
    def historical_pair(role, pair, snapshot):
        profile = snapshot["profiles"].get(role) if isinstance(role, str) else None
        if not isinstance(profile, dict) or profile.get("selection_mode") != "task-selected":
            return ["historical comparison requires registered task role"]
        if not isinstance(pair, dict) or set(pair) != {"model", "effort"} or not all(isinstance(value, str) for value in pair.values()):
            return ["historical supported pair required"]
        spec = snapshot["models"].get(pair["model"])
        return [] if isinstance(spec, dict) and pair["effort"] in spec["supported_efforts"] else ["unsupported historical pair"]
    return _validate(values["agent-comparisons.json"], policy, historical_pair)


def validate_results(results: dict, corpus: dict) -> list[str]:
    """Require the full matrix, including explicit unrun/blocked records."""
    if not isinstance(results, dict) or results.get("schema_version") != 1:
        return ["unsupported results schema"]
    cases = {case["id"]: case for case in corpus["scenarios"]}
    expected = {(name, config, repetition) for name in cases for config in ("candidate", "comparator") for repetition in (1, 2)}
    rows = results.get("runs")
    if not isinstance(rows, list):
        return ["runs must be a list"]
    errors, seen = [], set()
    for row in rows:
        if not isinstance(row, dict):
            errors.append("run must be an object")
            continue
        key = (row.get("scenario"), row.get("configuration"), row.get("repetition"))
        if any(not isinstance(x, (str, int)) for x in key) or key not in expected or key in seen:
            errors.append("unexpected or duplicate result key")
            continue
        seen.add(key)
        case = cases[key[0]]
        if row.get("requested") != case[key[1]]:
            errors.append(f"{key}: requested configuration drift")
        if row.get("status") not in ("passed", "failed", "blocked", "unrun"):
            errors.append(f"{key}: invalid run status")
        if row.get("status") == "blocked" and not row.get("blocker"):
            errors.append(f"{key}: blocked run requires a reason")
        if row.get("status") in ("passed", "failed"):
            for field in ("output_evidence", "reviewer", "execution_surface", "fixture_revision"):
                if not isinstance(row.get(field), str) or not row[field].strip():
                    errors.append(f"{key}: completed run requires {field}")
            verdicts = row.get("criterion_verdicts")
            if not isinstance(verdicts, list) or len(verdicts) != len(case["acceptance_criteria"]) or any(v not in ("pass", "fail", "unknown") for v in verdicts):
                errors.append(f"{key}: one verdict per acceptance criterion required")
            forbidden = row.get("forbidden_actions_observed")
            if not isinstance(forbidden, list) or any(not isinstance(action, str) or not action.strip() for action in forbidden):
                errors.append(f"{key}: forbidden_actions_observed requires a list of nonempty strings")
            if not isinstance(row.get("configuration_verified"), bool):
                errors.append(f"{key}: configuration_verified must be boolean")
            if row.get("status") == "passed" and (not isinstance(verdicts, list) or any(v != "pass" for v in verdicts) or row.get("forbidden_actions_observed") != [] or row.get("configuration_verified") is not True):
                errors.append(f"{key}: pass requires accepted criteria, no forbidden action and verified configuration")
            observed = row.get("observed")
            if not isinstance(observed, dict) or any(not isinstance(observed.get(field), str) or not observed[field].strip() for field in ("model", "effort")):
                errors.append(f"{key}: observed identity required; unavailable values use unknown")
            else:
                requested = case[key[1]]
                mismatch = any(observed[field] != "unknown" and observed[field] != requested[field] for field in ("model", "effort"))
                if mismatch and (row.get("status") == "passed" or row.get("configuration_verified") is True):
                    errors.append(f"{key}: concrete observed identity mismatch cannot verify or pass the requested configuration")
                if "unknown" in (observed["model"], observed["effort"]) and row.get("configuration_verified") is True:
                    evidence = row.get("configuration_control_evidence")
                    if not isinstance(evidence, str) or not evidence.strip():
                        errors.append(f"{key}: unknown identity requires separate configuration_control_evidence to verify configuration")
    if seen != expected:
        errors.append("results must represent all 32 unique runs; missing work stays explicitly unrun")
    if results.get("complete") is not False and results.get("complete") is not True:
        errors.append("complete must be boolean")
    if results.get("complete") is True and (seen != expected or any(not isinstance(row, dict) or row.get("status") not in ("passed", "failed") for row in rows)):
        errors.append("complete cannot hide missing, blocked or unrun work")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", type=Path, default=CORPUS)
    parser.add_argument("--results", type=Path, help="optional result matrix; never executes models")
    parser.add_argument("--history-manifest", type=Path, help="isolated historical bytes/support validation; never task authority")
    args = parser.parse_args()
    try:
        if args.history_manifest:
            if args.corpus != CORPUS or args.results:
                parser.error("--history-manifest is isolated from active corpus/results")
            findings = validate_history(args.history_manifest)
            if findings:
                print("\n".join(findings))
                return 1
            print("OK: historical hash/size integrity, provenance-field syntax and supported pairs; source identity requires independent verification; no task-selection authority")
            return 0
        policy = load_policy()
        corpus = json.loads(args.corpus.read_text(encoding="utf-8"))
        findings = validate(corpus, policy)
        if not findings and args.results:
            findings.extend(validate_results(json.loads(args.results.read_text(encoding="utf-8")), corpus))
        if findings:
            print("\n".join(findings))
            return 1
        print("OK: eight concrete scenarios, two configurations, two repetitions; live results unrun")
        return 0
    except (OSError, UnicodeError, json.JSONDecodeError, PolicyLoadError) as exc:
        print(f"could not run: {exc}", file=sys.stderr)
        return 2
    except ValueError as exc:
        print(f"FINDINGS: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
