#!/usr/bin/env python3
"""Validate the representative evaluation corpus, not model quality. 0/1/2 exit contract."""
from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
from codex_model_policy import load_policy, PolicyLoadError

CORPUS = Path(__file__).resolve().parents[1] / "assets/evals/agent-comparisons.json"
EXPECTED = {"exploration", "bounded-implementation", "debugging", "known-defect-review", "architecture", "instruction-rewrite", "documentation", "failed-check"}


def validate(corpus: dict, policy: dict) -> list[str]:
    if not isinstance(corpus, dict) or corpus.get("schema_version") != 1:
        return ["unsupported corpus schema"]
    errors = []
    if corpus.get("policy_version") != policy["policy_version"]:
        errors.append("corpus policy version drift")
    scenarios = corpus.get("scenarios")
    if not isinstance(scenarios, list):
        return errors + ["scenarios must be a list"]
    names = [case.get("id") for case in scenarios if isinstance(case, dict)]
    if len(names) != len(scenarios) or len(names) != len(EXPECTED) or set(names) != EXPECTED:
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
        profile = policy["profiles"].get(case.get("profile"))
        candidate, comparator = case.get("candidate"), case.get("comparator")
        if not isinstance(candidate, dict) or not isinstance(comparator, dict):
            errors.append(f"{name}: candidate and comparator must be objects")
            continue
        if not profile or candidate != {"model": profile["model"], "effort": profile["effort"]}:
            errors.append(f"{name}: candidate differs from role profile")
        if sum(candidate.get(key) != comparator.get(key) for key in ("model", "effort")) != 1:
            errors.append(f"{name}: comparison must change exactly one factor")
        for config in (candidate, comparator):
            model = policy["models"].get(config.get("model"), {})
            if config.get("effort") not in model.get("supported_efforts", []):
                errors.append(f"{name}: unsupported comparison pair")
    return errors


def self_test(corpus: dict, policy: dict) -> None:
    assert not validate(corpus, policy)
    bad = copy.deepcopy(corpus)
    bad["scenarios"].pop()
    assert validate(bad, policy)
    for field, value in (("inputs", {}), ("acceptance_criteria", []), ("forbidden_actions", []), ("status", "pass"), ("repetitions", 1), ("prompt", "TODO")):
        bad = copy.deepcopy(corpus)
        bad["scenarios"][0][field] = value
        assert validate(bad, policy), field
    bad = copy.deepcopy(corpus)
    bad["scenarios"][0]["comparator"] = {"model": "gpt-6-sol", "effort": "low"}
    assert validate(bad, policy)
    bad = copy.deepcopy(corpus)
    bad["scenarios"][0]["comparator"] = bad["scenarios"][0]["candidate"].copy()
    assert validate(bad, policy)


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


def results_self_test(corpus: dict) -> None:
    rows = [{"scenario": case["id"], "configuration": kind, "repetition": rep, "requested": case[kind], "status": "unrun"} for case in corpus["scenarios"] for kind in ("candidate", "comparator") for rep in (1, 2)]
    baseline = {"schema_version": 1, "complete": False, "runs": rows}
    assert not validate_results(baseline, corpus)
    assert validate_results({**baseline, "runs": rows[:-1]}, corpus)
    assert validate_results({**baseline, "runs": rows + [rows[0]]}, corpus)
    assert validate_results({**baseline, "complete": True}, corpus)
    bad = copy.deepcopy(baseline)
    bad["runs"][0]["status"] = "passed"
    assert validate_results(bad, corpus)
    completed = copy.deepcopy(baseline)
    first = completed["runs"][0]
    first.update(status="passed", output_evidence="synthetic/output.txt", reviewer="independent fixture reviewer", execution_surface="synthetic host", fixture_revision="fixture-v1", criterion_verdicts=["pass"] * len(corpus["scenarios"][0]["acceptance_criteria"]), forbidden_actions_observed=[], configuration_verified=True, observed=first["requested"].copy())
    assert not validate_results(completed, corpus)
    for field, value in (("model", "gpt-5.6-sol"), ("effort", "low")):
        bad = copy.deepcopy(completed)
        bad["runs"][0]["observed"][field] = value
        assert any("mismatch" in error for error in validate_results(bad, corpus)), field
        bad["runs"][0].update(status="failed", configuration_verified=False)
        assert not validate_results(bad, corpus), "honest mismatch failure must remain reportable"
    unknown = copy.deepcopy(completed)
    unknown["runs"][0]["observed"] = {"model": "unknown", "effort": "unknown"}
    assert any("configuration_control_evidence" in error for error in validate_results(unknown, corpus))
    for invalid in (True, [], " "):
        unknown["runs"][0]["configuration_control_evidence"] = invalid
        assert validate_results(unknown, corpus)
    unknown["runs"][0]["configuration_control_evidence"] = "synthetic/host-resolved-configuration.json"
    assert not validate_results(unknown, corpus)
    failed = copy.deepcopy(completed)
    failed["runs"][0].update(status="failed", configuration_verified=False, forbidden_actions_observed=["edited outside scope"])
    assert not validate_results(failed, corpus)
    for field, invalid in (("forbidden_actions_observed", None), ("forbidden_actions_observed", "none"), ("forbidden_actions_observed", [False]), ("forbidden_actions_observed", [""]), ("configuration_verified", None), ("configuration_verified", "false"), ("configuration_verified", 0)):
        bad = copy.deepcopy(failed)
        bad["runs"][0][field] = invalid
        assert any(field in error for error in validate_results(bad, corpus)), (field, invalid)
    for field in ("forbidden_actions_observed", "configuration_verified"):
        bad = copy.deepcopy(failed)
        del bad["runs"][0][field]
        assert any(field in error for error in validate_results(bad, corpus)), field


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", type=Path, default=CORPUS)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--results", type=Path, help="optional result matrix; never executes models")
    args = parser.parse_args()
    try:
        policy = load_policy()
        corpus = json.loads(args.corpus.read_text(encoding="utf-8"))
        if args.self_test:
            self_test(corpus, policy)
            results_self_test(corpus)
            print("OK: corpus coverage and negative cases; no model runs executed")
            return 0
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
    except (ValueError, AssertionError) as exc:
        print(f"FINDINGS: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
