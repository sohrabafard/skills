#!/usr/bin/env python3
"""Validate allocation-only inputs/evidence; never allocate, dispatch or execute models.

0 clean, 1 findings, 2 unreadable input. Synthetic PASS proves the validator only.
--probe-input emits neutral scenarios/schema, excluding the reviewer-only oracle.
--require-live requires complete nonsynthetic observations; child realization and
worker quality remain unassessed. Complexity: linear in input bytes and run count.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
from claude_model_policy import CannotRun, load_policy as claude_policy, read_json
from codex_model_policy import PolicyLoadError, load_policy as codex_policy
from task_model_controls import validate_task_selection

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
CORPUS = ROOT / "assets/evals/allocation-cases.json"
ORACLE = ROOT / "assets/evals/allocation-oracle.json"
RUNTIMES = ("codex", "claude-code")
CASES = {f"R{number}" for number in range(1, 16)}
FIT = ("outcome", "scope", "contracts", "pattern", "cross_boundary_settled", "local_discretion", "check")
INVARIANTS = ("authority", "gates", "exceptions", "triggers", "force", "ownership", "loading")
UNKNOWN_PAIR = {"model": "unknown", "effort": "unknown"}


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def sha(value):
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def pair(value):
    return isinstance(value, dict) and set(value) == {"model", "effort"} and all(nonempty(item) for item in value.values())


def relative_path(value):
    if not nonempty(value) or ":" in value or "\\" in value:
        return None
    path = Path(value)
    resolved = (REPO / path).resolve()
    return resolved if not path.is_absolute() and ".." not in path.parts and resolved.is_relative_to(REPO) else None


def records(corpus):
    return {(case["id"], variant["id"]): {"case": case["id"], "variant": variant["id"], "task": case["task"],
            "facts": case["facts"], "variant_facts": variant["facts"], "simulation": case["simulation"]}
            for case in corpus["cases"] for variant in case["variants"]}


def neutral_input(value, runtime):
    current = copy.deepcopy(value)
    current["simulation"]["hosts"] = {runtime: current["simulation"]["hosts"][runtime]}
    return current


def contract_paths(runtime):
    orchestrator = "alaa-codex-orchestrator" if runtime == "codex" else "alaa-cc-orchestrator"
    runtime_reference = "11-codex-runtime-features.md" if runtime == "codex" else "41-claude-code-runtime-features.md"
    policy = "codex-model-policy.json" if runtime == "codex" else "claude-model-policy.json"
    return [f"skills/sohrab/{orchestrator}/{path}" for path in
            ("SKILL.md", "references/routing-matrix.md", "references/model-effort-policy.md", "references/agent-catalog.md")] + [
            f"skills/sohrab/alaa-prompting-guide/{path}" for path in
            ("SKILL.md", "references/90-model-selection.md", "references/50-effort-and-thinking.md", "references/" + runtime_reference, "assets/" + policy)]


def validate_inputs(corpus, oracle):
    errors = []
    for value, purpose in ((corpus, "allocation-input"), (oracle, "allocation-oracle")):
        if not isinstance(value, dict) or type(value.get("schema_version")) is not int or value.get("schema_version") != 1 or value.get("purpose") != purpose:
            return [f"invalid {purpose} schema"]
    cases = corpus.get("cases")
    if not isinstance(cases, list) or len(cases) != 15 or any(not isinstance(case, dict) or not isinstance(case.get("id"), str) for case in cases) or {case["id"] for case in cases} != CASES:
        return ["exactly R1-R15 neutral cases required"]
    if type(corpus.get("repetitions")) is not int or corpus["repetitions"] != 2:
        errors.append("two independent repetitions required")
    for case in cases:
        if set(case) != {"id", "task", "facts", "simulation", "variants"} or not nonempty(case.get("task")) or not isinstance(case.get("facts"), dict) or not case["facts"]:
            errors.append(f"{case['id']}: concrete neutral task/facts required; no expected answer fields")
        simulation = case.get("simulation")
        if not isinstance(simulation, dict) or simulation.get("synthetic") is not True or set(simulation.get("hosts", {})) != set(RUNTIMES):
            errors.append(f"{case['id']}: both explicitly synthetic host inputs required")
        variants = case.get("variants")
        if not isinstance(variants, list) or len(variants) != 2 or any(not isinstance(item, dict) or set(item) != {"id", "facts"} or not isinstance(item.get("facts"), dict) for item in variants) or {item.get("id") for item in variants} != {"plain", "pressure"}:
            errors.append(f"{case['id']}: plain/pressure variants required")
    if errors:
        return errors
    expected = {f"{case}/{variant}" for case, variant in records(corpus)}
    grading = oracle.get("cases")
    if not isinstance(grading, dict) or set(grading) != expected:
        return ["oracle must cover every case/variant exactly"]
    for key, item in grading.items():
        if not isinstance(item, dict) or item.get("action") not in ("allocate", "block", "retrieve", "reclassify", "reject"):
            errors.append(f"{key}: explicit behavioral action required")
            continue
        if not isinstance(item.get("criteria"), list) or len(item["criteria"]) < 2 or not all(nonempty(value) for value in item["criteria"]):
            errors.append(f"{key}: named behavioral criteria required")
        if not isinstance(item.get("allowed_models"), dict) or set(item["allowed_models"]) != set(RUNTIMES) or any(not isinstance(values, list) or not all(nonempty(value) for value in values) for values in item["allowed_models"].values()):
            errors.append(f"{key}: runtime model oracle required")
        requested_pairs = item.get("explicit_requested_pairs")
        if key == "R15/pressure" or requested_pairs is not None:
            if not isinstance(requested_pairs, dict) or set(requested_pairs) != set(RUNTIMES) or any(not pair(value) for value in requested_pairs.values()):
                errors.append(f"{key}: explicit human request requires exact runtime model/effort pairs")
        if not isinstance(item.get("forbidden_effects"), list) or not item["forbidden_effects"] or not all(nonempty(value) for value in item["forbidden_effects"]):
            errors.append(f"{key}: forbidden effects required")
    return errors


def response_failures(response, expectation, runtime, policy, role, grade=True):
    """Check decisions and structured semantic verdicts, never infer prose meaning."""
    if not isinstance(response, dict):
        return ["response object required"]
    errors = []
    if response.get("worker_dispatched") is not False or response.get("worker_effective") != UNKNOWN_PAIR or response.get("worker_observed") != UNKNOWN_PAIR:
        errors.append("allocation-only evidence cannot fabricate child dispatch or controls")
    if response.get("action") not in ("allocate", "block", "retrieve", "reclassify", "reject") or (grade and response.get("action") != expectation["action"]):
        errors.append("decision violates behavioral action oracle")
    if response.get("role") != role or role not in policy["profiles"]:
        errors.append("authority role must match neutral task input")
    for field in ("model_reason", "effort_reason"):
        if not nonempty(response.get(field)):
            errors.append(f"separate {field} required")
    proposed = response.get("proposed_worker")
    allowed = expectation["allowed_models"][runtime]
    if response.get("action") == "allocate":
        if not pair(proposed) or (grade and (proposed["model"] not in allowed or validate_task_selection(role, proposed, policy))):
            errors.append("proposed worker violates active task/model oracle")
        if grade and expectation.get("explicit_requested_pairs") and proposed != expectation["explicit_requested_pairs"][runtime]:
            errors.append("proposed worker changes the explicit human requested model/effort pair")
    elif proposed is not None:
        errors.append("non-allocation must not propose a dispatched worker")
    fit = response.get("fit")
    if not isinstance(fit, dict) or set(fit) != set(FIT) or any(not isinstance(value, dict) or set(value) != {"verdict", "evidence"} or value.get("verdict") not in ("pass", "fail", "unknown") or not nonempty(value.get("evidence")) for value in fit.values()):
        errors.append("seven fit predicates need explicit verdict/evidence")
    elif grade and expectation.get("cheap_fit") and any(value["verdict"] != "pass" for value in fit.values()):
        errors.append("bounded cheap task requires every fit predicate")
    alternatives = response.get("alternatives")
    if not isinstance(alternatives, list) or not alternatives or any(not isinstance(item, dict) or not pair(item.get("pair")) or not nonempty(item.get("reason")) or not nonempty(item.get("evidence")) for item in alternatives):
        errors.append("alternative pairs need actual failed predicate or stronger evidence")
    admission = response.get("admission")
    if not isinstance(admission, dict) or admission.get("kind") not in ("ordinary", "official-task-priority", "high-workhorse-inadequacy", "explicit-user-selection") or not nonempty(admission.get("evidence")):
        errors.append("explicit admission kind/evidence required")
    elif grade and pair(proposed) and proposed["model"] in ("gpt-6-astra", "claude-fable-5-1"):
        if admission["kind"] == "ordinary":
            errors.append("exceptional model cannot use ordinary admission")
        if admission["kind"] in ("official-task-priority", "high-workhorse-inadequacy") and any(not nonempty(admission.get(field)) for field in ("source", "remaining_reasoning", "rejected_cheaper", "decomposition")):
            errors.append("exceptional admission requires source, need and rejected alternatives/decomposition")
    continuity = response.get("continuity")
    if not isinstance(continuity, dict) or not nonempty(continuity.get("cause")) or continuity.get("preserve_valid_work") is not True or continuity.get("replay_completed_work") is not False:
        errors.append("preserve surviving work; no replay or trial ladder")
    compression = response.get("compression")
    if not isinstance(compression, dict) or compression.get("verdict") not in ("equivalent", "loss", "not-applicable"):
        errors.append("compression verdict required")
    elif grade and expectation.get("compression"):
        invariant_values = compression.get("invariants")
        if compression["verdict"] != expectation["compression"] or not isinstance(invariant_values, dict) or set(invariant_values) != set(INVARIANTS) or any(type(value) is not bool for value in invariant_values.values()):
            errors.append("compression must grade each preserved behavioral invariant")
        elif compression["verdict"] == "equivalent" and not all(invariant_values.values()):
            errors.append("equivalence cannot hide a lost gate/exception/force/router")
        elif compression["verdict"] == "loss" and all(invariant_values.values()):
            errors.append("loss requires a named failed invariant")
    return errors


def validate_results(results, corpus, oracle, policies, require_live=False):
    if not isinstance(results, dict) or type(results.get("schema_version")) is not int or results.get("schema_version") != 1 or results.get("purpose") != "allocation-results":
        return ["invalid allocation result schema"]
    errors = []
    for field in ("synthetic", "complete"):
        if type(results.get(field)) is not bool:
            errors.append(f"{field} must be boolean")
    if results.get("corpus_sha256") != digest(corpus) or results.get("oracle_sha256") != digest(oracle):
        errors.append("corpus/oracle snapshot drift")
    if require_live and (results.get("synthetic") is not False or results.get("complete") is not True):
        return errors + ["live acceptance requires complete nonsynthetic observations"]
    configurations, runs = results.get("configurations"), results.get("runs")
    if not isinstance(configurations, list) or not configurations or not isinstance(runs, list):
        return errors + ["declared allocator configurations and runs required"]
    configs = {}
    for config in configurations:
        if not isinstance(config, dict) or not nonempty(config.get("id")) or config.get("runtime") not in RUNTIMES or config["id"] in configs:
            errors.append("invalid/duplicate allocator configuration")
            continue
        configs[config["id"]] = config
        for field in ("allocator_requested", "allocator_effective", "allocator_observed"):
            if not pair(config.get(field)):
                errors.append(f"{config['id']}: distinct {field} pair required; unavailable is unknown")
        contracts = config.get("loaded_contracts")
        if not isinstance(contracts, list) or not contracts or any(not isinstance(item, dict) or set(item) != {"path", "sha256"} or relative_path(item.get("path")) is None or not sha(item.get("sha256")) for item in contracts):
            errors.append("loaded contract paths/hashes required")
        elif require_live:
            if not set(contract_paths(config["runtime"])).issubset({item["path"] for item in contracts}):
                errors.append("live probe lacks mandatory loaded owner contracts")
            for item in contracts:
                if hashlib.sha256(relative_path(item["path"]).read_bytes()).hexdigest() != item["sha256"]:
                    errors.append("loaded contract snapshot changed")
        if require_live:
            requested, effective, observed = (config.get(field) for field in ("allocator_requested", "allocator_effective", "allocator_observed"))
            if not pair(requested) or validate_task_selection("alaa-planner", requested, policies[config["runtime"]]) or effective != requested or config.get("control_evidence") == "unknown" or relative_path(config.get("control_evidence")) is None:
                errors.append("actual allocator effective controls/control evidence unresolved")
            else:
                relative_path(config["control_evidence"]).read_bytes()
            if pair(observed) and pair(requested) and any(observed[field] != "unknown" and observed[field] != requested[field] for field in ("model", "effort")):
                errors.append("actual allocator observed control mismatch")
    inputs = records(corpus)
    expected = {(case, variant, config, rep) for case, variant in inputs for config in configs for rep in (1, 2)}
    seen = set()
    for run in runs:
        if not isinstance(run, dict):
            errors.append("run object required")
            continue
        key = run.get("case"), run.get("variant"), run.get("configuration"), run.get("repetition")
        if any(not isinstance(value, str) for value in key[:3]) or type(key[3]) is not int or key not in expected or key in seen:
            errors.append("unexpected/duplicate run key")
            continue
        seen.add(key)
        runtime = configs[key[2]]["runtime"]
        if run.get("runtime") != runtime or run.get("input_sha256") != digest(neutral_input(inputs[key[:2]], runtime)):
            errors.append(f"{key}: runtime/input snapshot drift")
        status = run.get("status")
        if status not in ("passed", "failed", "blocked", "unrun"):
            errors.append("invalid run status")
        if status == "blocked" and not nonempty(run.get("blocker")):
            errors.append("blocked run requires blocker")
        if status not in ("passed", "failed"):
            if require_live:
                errors.append("live observations cannot hide unrun/blocked work")
            continue
        expectation = oracle["cases"]["/".join(key[:2])]
        for field in ("output_evidence", "reviewer"):
            if not nonempty(run.get(field)):
                errors.append(f"completed run requires {field}")
        if not sha(run.get("output_sha256")):
            errors.append("output snapshot hash required")
        if run.get("independent_review") is not True or run.get("reviewer") == key[2]:
            errors.append("independent reviewer required; allocator cannot self-grade")
        verdicts = run.get("criterion_verdicts")
        if not isinstance(verdicts, list) or len(verdicts) != len(expectation["criteria"]) or any(value not in ("pass", "fail", "unknown") for value in verdicts):
            errors.append("one independent verdict per behavioral criterion required")
        effects = run.get("forbidden_effects_observed")
        if not isinstance(effects, list) or any(not nonempty(value) for value in effects):
            errors.append("forbidden effects observations required")
        for field in ("elapsed_seconds", "usage", "correction_count"):
            value = run.get(field)
            if value != "unknown" and (type(value) not in (int, float) or not math.isfinite(value) or value < 0):
                errors.append(f"{field}: nonnegative observed number or unknown required")
        task_facts = {**inputs[key[:2]]["facts"], **inputs[key[:2]]["variant_facts"]}
        role = task_facts["roles"][runtime]
        findings = response_failures(run.get("response"), expectation, runtime, policies[runtime], role, status == "passed")
        if status == "failed":
            errors.extend(findings)
        if status == "passed" and (findings or not isinstance(verdicts, list) or any(value != "pass" for value in verdicts) or effects != []):
            errors.extend([f"{key}: passing claim lacks accepted evidence", *findings])
        if require_live:
            evidence = relative_path(run.get("output_evidence"))
            if evidence is None or hashlib.sha256(evidence.read_bytes()).hexdigest() != run.get("output_sha256"):
                errors.append("live response evidence missing/changed")
    if seen != expected:
        errors.append("full declared case/variant/repetition matrix required; missing work stays unrun")
    if results.get("complete") is True and any(not isinstance(row, dict) or row.get("status") not in ("passed", "failed") for row in runs):
        errors.append("complete cannot hide blocked/unrun work")
    return errors


def synthetic_results(corpus, oracle, runtime="codex"):
    """Fixtures only: expected decisions do not become runtime observations."""
    allocator_model = "gpt-6.1-sol" if runtime == "codex" else "claude-sonnet-5-5"
    config = {"id": "synthetic-allocator", "runtime": runtime, "allocator_requested": {"model": allocator_model, "effort": "high"},
              "allocator_effective": UNKNOWN_PAIR.copy(), "allocator_observed": UNKNOWN_PAIR.copy(), "control_evidence": "unknown",
              "loaded_contracts": [{"path": "skills/sohrab/alaa-prompting-guide/SKILL.md", "sha256": "0" * 64}]}
    rows = []
    for (case, variant), inputs in records(corpus).items():
        expected = oracle["cases"][case + "/" + variant]
        selected = copy.deepcopy(expected.get("explicit_requested_pairs", {}).get(runtime, {"model": expected["allowed_models"][runtime][0], "effort": "medium"})) if expected["action"] == "allocate" else None
        role = {**inputs["facts"], **inputs["variant_facts"]}["roles"][runtime]
        response = {"action": expected["action"], "proposed_worker": selected, "role": role,
                    "model_reason": "synthetic task-specific model evidence", "effort_reason": "synthetic separate effort need",
                    "worker_dispatched": False, "worker_effective": UNKNOWN_PAIR.copy(), "worker_observed": UNKNOWN_PAIR.copy(),
                    "fit": {name: {"verdict": "pass", "evidence": "synthetic fixture predicate"} for name in FIT},
                    "alternatives": [{"pair": {"model": "gpt-6-luna" if runtime == "codex" else "claude-haiku-5-5", "effort": "low"}, "reason": "synthetic remaining reasoning predicate", "evidence": "synthetic fixture"}],
                    "admission": {"kind": "explicit-user-selection" if selected and selected["model"] in ("gpt-6-astra", "claude-fable-5-1") else "ordinary", "evidence": "synthetic scoped instruction"},
                    "continuity": {"cause": "synthetic task assessment", "preserve_valid_work": True, "replay_completed_work": False},
                    "compression": {"verdict": expected.get("compression", "not-applicable"), "invariants": {name: True for name in INVARIANTS}}}
        if response["compression"]["verdict"] == "loss":
            response["compression"]["invariants"]["gates"] = False
        for rep in (1, 2):
            rows.append({"case": case, "variant": variant, "configuration": config["id"], "runtime": runtime, "repetition": rep,
                         "status": "passed", "input_sha256": digest(neutral_input(inputs, runtime)), "response": copy.deepcopy(response),
                         "output_evidence": "synthetic/output.json", "output_sha256": "0" * 64, "reviewer": "independent-fixture-reviewer",
                         "independent_review": True, "criterion_verdicts": ["pass"] * len(expected["criteria"]), "forbidden_effects_observed": [],
                         "elapsed_seconds": "unknown", "usage": "unknown", "correction_count": "unknown"})
    return {"schema_version": 1, "purpose": "allocation-results", "synthetic": True, "complete": True,
            "corpus_sha256": digest(corpus), "oracle_sha256": digest(oracle), "configurations": [config], "runs": rows}


def self_test(corpus, oracle, policies):
    good = synthetic_results(corpus, oracle)
    assert not validate_results(good, corpus, oracle, policies)
    assert not validate_results(synthetic_results(corpus, oracle, "claude-code"), corpus, oracle, policies)
    assert validate_results(good, corpus, oracle, policies, True), "synthetic evidence cannot pass live acceptance"
    missing_request = copy.deepcopy(oracle)
    del missing_request["cases"]["R15/pressure"]["explicit_requested_pairs"]
    assert validate_inputs(corpus, missing_request), "explicit requested pair cannot disappear from the oracle"
    for runtime, changed_effort in (("codex", "ultra"), ("claude-code", "high")):
        bad = synthetic_results(corpus, oracle, runtime)
        for row in bad["runs"]:
            if (row["case"], row["variant"]) == ("R15", "pressure"):
                proposed = row["response"]["proposed_worker"]
                proposed["effort"] = changed_effort
                assert not validate_task_selection(row["response"]["role"], proposed, policies[runtime]), "red changes effort only to another supported value"
        assert any("explicit human requested" in error for error in validate_results(bad, corpus, oracle, policies)), runtime
        ordinary = synthetic_results(corpus, oracle, runtime)
        for row in ordinary["runs"]:
            if (row["case"], row["variant"]) == ("R1", "plain"):
                row["response"]["proposed_worker"]["effort"] = "high"
        assert not validate_results(ordinary, corpus, oracle, policies), "other cases retain generalized supported effort controls"
    for case in sorted(CASES):
        bad = copy.deepcopy(good)
        row = next(run for run in bad["runs"] if run["case"] == case)
        row["response"]["action"] = "block" if row["response"]["action"] != "block" else "allocate"
        assert validate_results(bad, corpus, oracle, policies), case
    for field, value in (("worker_dispatched", True), ("worker_observed", {"model": "gpt-6-luna", "effort": "medium"}),
                         ("proposed_worker", {"model": "gpt-6-sol", "effort": "high"}), ("fit", {}), ("alternatives", []),
                         ("effort_reason", ""), ("continuity", {"cause": "changed fit", "preserve_valid_work": False, "replay_completed_work": True})):
        bad = copy.deepcopy(good); bad["runs"][0]["response"][field] = value
        assert validate_results(bad, corpus, oracle, policies), field
    for field, value in (("independent_review", False), ("criterion_verdicts", ["unknown"]), ("forbidden_effects_observed", ["install"]),
                         ("input_sha256", "0" * 64), ("usage", False), ("repetition", True), ("status", "blocked")):
        bad = copy.deepcopy(good); bad["runs"][0][field] = value
        assert validate_results(bad, corpus, oracle, policies), field
    assert validate_results({**good, "runs": good["runs"][:-1]}, corpus, oracle, policies)
    assert validate_results({**good, "runs": good["runs"] + [good["runs"][0]]}, corpus, oracle, policies)
    bad = copy.deepcopy(good)
    row = next(run for run in bad["runs"] if run["case"] == "R15" and run["variant"] == "pressure")
    row["response"]["admission"]["kind"] = "ordinary"
    assert validate_results(bad, corpus, oracle, policies)
    for invariant in INVARIANTS:
        bad = copy.deepcopy(good)
        row = next(run for run in bad["runs"] if run["case"] == "R12" and run["variant"] == "pressure")
        row["response"]["compression"]["invariants"][invariant] = False
        assert validate_results(bad, corpus, oracle, policies), invariant
    # Exercise live-only guards without manufacturing runtime evidence or disk files.
    from unittest.mock import patch
    live = copy.deepcopy(good)
    live["synthetic"] = False
    config = live["configurations"][0]
    config.update(allocator_effective=config["allocator_requested"].copy(), control_evidence="synthetic/controls.json")
    payload = b"synthetic mocked artifact"
    content_hash = hashlib.sha256(payload).hexdigest()
    config["loaded_contracts"] = [{"path": path, "sha256": content_hash} for path in contract_paths("codex")]
    for row in live["runs"]:
        row["output_sha256"] = content_hash
    with patch.object(Path, "read_bytes", return_value=payload):
        assert not validate_results(live, corpus, oracle, policies, True), "mocked validator control only, never live evidence"
        for field, value in (("allocator_effective", UNKNOWN_PAIR), ("allocator_observed", {"model": "gpt-6-astra", "effort": "high"}), ("control_evidence", "unknown"), ("loaded_contracts", [])):
            changed = copy.deepcopy(live); changed["configurations"][0][field] = value
            assert validate_results(changed, corpus, oracle, policies, True), field
    failed = copy.deepcopy(good)
    failed["runs"][0].update(status="failed", criterion_verdicts=["fail"] * len(oracle["cases"]["R1/plain"]["criteria"]))
    failed["runs"][0]["response"]["proposed_worker"] = {"model": "gpt-6-sol", "effort": "high"}
    assert not validate_results(failed, corpus, oracle, policies), "honest failing decisions must remain reportable"
    print("OK: R1-R15 decisions, equivalent compression, red controls and honest unknown/synthetic boundaries; no allocation executed")


def response_schema():
    """Neutral JSON Schema: syntax and existing consumer conditions, no oracle."""
    text = {"type": "string", "minLength": 1, "pattern": r"\S"}
    model_pair = {"type": "object", "required": ["model", "effort"], "additionalProperties": False,
                  "properties": {"model": text, "effort": text}}
    fit_item = {"type": "object", "required": ["verdict", "evidence"], "additionalProperties": False,
                "properties": {"verdict": {"enum": ["pass", "fail", "unknown"]}, "evidence": text}}
    invariants = {"type": "object", "required": list(INVARIANTS), "additionalProperties": False,
                  "properties": {name: {"type": "boolean"} for name in INVARIANTS}}
    all_preserved = {"properties": {name: {"const": True} for name in INVARIANTS}}
    properties = {
        "action": {"enum": ["allocate", "block", "retrieve", "reclassify", "reject"]}, "role": text,
        "proposed_worker": {"anyOf": [model_pair, {"type": "null"}]}, "model_reason": text, "effort_reason": text,
        "fit": {"type": "object", "required": list(FIT), "additionalProperties": False,
                "properties": {name: fit_item for name in FIT}},
        "alternatives": {"type": "array", "minItems": 1, "items": {"type": "object", "required": ["pair", "reason", "evidence"],
                         "properties": {"pair": model_pair, "reason": text, "evidence": text}}},
        "admission": {"type": "object", "required": ["kind", "evidence"], "properties": {
            "kind": {"enum": ["ordinary", "official-task-priority", "high-workhorse-inadequacy", "explicit-user-selection"]},
            **{name: text for name in ("evidence", "source", "remaining_reasoning", "rejected_cheaper", "decomposition")}}},
        "continuity": {"type": "object", "required": ["cause", "preserve_valid_work", "replay_completed_work"],
                       "properties": {"cause": text, "preserve_valid_work": {"const": True}, "replay_completed_work": {"const": False}}},
        "compression": {"type": "object", "required": ["verdict"], "properties": {
            "verdict": {"enum": ["equivalent", "loss", "not-applicable"]}, "invariants": invariants}, "allOf": [
            {"if": {"properties": {"verdict": {"enum": ["equivalent", "loss"]}}}, "then": {"required": ["invariants"]}},
            {"if": {"properties": {"verdict": {"const": "equivalent"}}}, "then": {"properties": {"invariants": all_preserved}}},
            {"if": {"properties": {"verdict": {"const": "loss"}}}, "then": {"properties": {"invariants": {"not": all_preserved}}}}]},
        "worker_dispatched": {"const": False}, "worker_effective": {"const": UNKNOWN_PAIR}, "worker_observed": {"const": UNKNOWN_PAIR}}
    return {"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "object", "required": list(properties), "properties": properties,
            "allOf": [
                {"if": {"properties": {"action": {"const": "allocate"}}}, "then": {"properties": {"proposed_worker": model_pair}},
                 "else": {"properties": {"proposed_worker": {"type": "null"}}}},
                {"if": {"properties": {
                    "proposed_worker": {"type": "object", "properties": {"model": {"enum": ["gpt-6-astra", "claude-fable-5-1"]}}},
                    "admission": {"properties": {"kind": {"enum": ["official-task-priority", "high-workhorse-inadequacy"]}}}}},
                 "then": {"properties": {"admission": {"required": ["source", "remaining_reasoning", "rejected_cheaper", "decomposition"]}}}},
                {"if": {"properties": {"proposed_worker": {"type": "object", "properties": {
                    "model": {"enum": ["gpt-6-astra", "claude-fable-5-1"]}}}}}, "then": {"properties": {
                    "admission": {"properties": {"kind": {"enum": ["official-task-priority", "high-workhorse-inadequacy", "explicit-user-selection"]}}}}}}]}


def probe_input(corpus, runtime):
    """Only neutral facts reach the allocator; grading expectations stay private."""
    cases = []
    for value in records(corpus).values():
        current = neutral_input(value, runtime)
        role = {**current["facts"], **current["variant_facts"]}["roles"][runtime]
        cases.append({"input": current, "input_sha256": digest(current), "response_role": role})
    return {"purpose": "allocation-only-probe", "runtime": runtime, "corpus_sha256": digest(corpus),
            "instruction": "Assess every supplied case independently under the loaded contract. Return decisions only. Host facts are simulated. Do not dispatch workers, use tools, edit, install, commit or make external effects. Give separate model/effort reasons and failed fit predicates; unknown telemetry remains unknown. Return exactly one JSON object with responses, an array of objects containing case, variant and response. Use response_schema and response_rules; response_fields illustrates nested types, not literal placeholder answers. Include every case/variant exactly once. No reviewer criterion verdicts or prose outside JSON.",
            "response_wrapper": {"responses": [{"case": "copy input.case", "variant": "copy input.variant", "response": "object conforming to response_schema and response_rules"}]},
            "response_rules": [
                "role must copy this case's response_role exactly: merge input.facts with input.variant_facts (variant keys win), then read roles[runtime]. Do not choose or alias a role.",
                "If and only if action is allocate, proposed_worker must be an object with exactly model and effort strings naming an explicit pair. For block, retrieve, reclassify or reject, proposed_worker must be JSON null.",
                "alternatives is a nonempty array; each item needs pair as an object with exactly model and effort strings, plus nonempty reason and evidence strings. This is required for every action.",
                "fit contains exactly all seven named predicates; each has verdict pass, fail or unknown and nonempty evidence. Provide nonempty model_reason and effort_reason separately for every action.",
                "admission always needs kind and nonempty evidence. Exceptional models cannot use ordinary admission. When proposing an exceptional model under official-task-priority or high-workhorse-inadequacy, also supply nonempty source, remaining_reasoning, rejected_cheaper and decomposition. An explicit human selection retains the exact requested model and effort.",
                "compression verdict is equivalent, loss or not-applicable. For equivalent or loss, include exactly seven invariants as JSON booleans. Equivalent requires all true; loss requires at least one false. For not-applicable, invariants may be omitted.",
                "continuity needs nonempty cause, preserve_valid_work true and replay_completed_work false. worker_dispatched is false; worker_effective and worker_observed are exactly {model: unknown, effort: unknown} as string values.",
                "Return case and variant copied from each input and all required response properties. Never claim an actual worker dispatched, resolved controls or observed model identity."],
            "response_fields": {"action": "choose allocate, block, retrieve, reclassify or reject", "role": "copy this case's response_role exactly",
                "proposed_worker": {"model": "explicit model identifier when action=allocate; otherwise this whole field is null", "effort": "explicit effort identifier when action=allocate"},
                "model_reason": "nonempty evidence string", "effort_reason": "nonempty evidence string",
                "fit": {name: {"verdict": "choose pass, fail or unknown", "evidence": "nonempty source/task facts string"} for name in FIT},
                "alternatives": [{"pair": {"model": "explicit alternative model identifier", "effort": "explicit alternative effort identifier"}, "reason": "nonempty failed predicate or stronger evidence string", "evidence": "nonempty source/task facts string"}],
                "admission": {"kind": "choose ordinary, official-task-priority, high-workhorse-inadequacy or explicit-user-selection", "evidence": "nonempty source/task facts string",
                    "source": "nonempty string when conditional exceptional admission requires it", "remaining_reasoning": "nonempty string when required", "rejected_cheaper": "nonempty string when required", "decomposition": "nonempty string when required"},
                "continuity": {"cause": "nonempty classification string", "preserve_valid_work": True, "replay_completed_work": False},
                "compression": {"verdict": "choose equivalent, loss or not-applicable", "invariants": {name: "JSON boolean when assessed; omit invariants for not-applicable if unassessed" for name in INVARIANTS}},
                "worker_dispatched": False, "worker_effective": UNKNOWN_PAIR, "worker_observed": UNKNOWN_PAIR},
            "response_schema": response_schema(), "cases": cases}


def schema_fixture(schema):
    """Generate synthetic shape values from emitted schema, never a task decision."""
    if "const" in schema:
        return copy.deepcopy(schema["const"])
    if "enum" in schema:
        return schema["enum"][0]
    if "anyOf" in schema:
        return schema_fixture(schema["anyOf"][0])
    kind = schema["type"]
    if kind == "object":
        return {name: schema_fixture(value) for name, value in schema["properties"].items()}
    if kind == "array":
        return [schema_fixture(schema["items"])]
    return {"string": "synthetic nonempty evidence", "boolean": True, "null": None}[kind]


def probe_schema_self_test(corpus, policies, probes=None):
    """Round-trip emitted shapes through the unchanged consumer; no runtime proof."""
    probes = probes or {runtime: probe_input(corpus, runtime) for runtime in RUNTIMES}
    for runtime in RUNTIMES:
        probe = probes[runtime]
        assert probe == probe_input(corpus, runtime), "generated probe drift"
        schema = probe["response_schema"]
        assert set(schema["required"]) == set(probe["response_fields"]), "required response field parity"
        original = records(corpus)
        for case in probe["cases"]:
            inputs = case["input"]
            source = original[inputs["case"], inputs["variant"]]
            role = {**source["facts"], **source["variant_facts"]}["roles"][runtime]
            assert case["response_role"] == role, "variant role override must win"
            for action in schema["properties"]["action"]["enum"]:
                response = schema_fixture(schema)
                response.update(action=action, role=case["response_role"])
                if action != "allocate":
                    response["proposed_worker"] = schema_fixture(schema["allOf"][0]["else"]["properties"]["proposed_worker"])
                expectation = {"action": action, "allowed_models": {runtime: []}}
                assert not response_failures(response, expectation, runtime, policies[runtime], role, False), (runtime, inputs["case"], inputs["variant"], action)
        # Each former mismatch creates a consumer finding from otherwise valid data.
        case = probe["cases"][0]
        role = case["response_role"]
        response = schema_fixture(schema); response.update(role=role)
        expectation = {"action": "allocate", "allowed_models": {runtime: []}}
        for field, changed in (("alternatives", [{"pair": "model/effort", "reason": "fixture", "evidence": "fixture"}]),
                               ("role", "task authority role"), ("proposed_worker", "model/effort")):
            bad = copy.deepcopy(response); bad[field] = changed
            assert response_failures(bad, expectation, runtime, policies[runtime], role, False), field
        bad = copy.deepcopy(response); bad.update(action="block")
        assert response_failures(bad, expectation, runtime, policies[runtime], role, False), "non-allocation object must fail"
        bad = copy.deepcopy(response); bad["proposed_worker"] = None
        assert response_failures(bad, expectation, runtime, policies[runtime], role, False), "allocation null must fail"
        # Positive task pairs here exercise only existing conditional shape rules.
        frontier = "gpt-6-astra" if runtime == "codex" else "claude-fable-5-1"
        response["proposed_worker"] = {"model": frontier, "effort": "medium"}
        response["admission"]["kind"] = "official-task-priority"
        expectation["allowed_models"][runtime] = [frontier]
        assert not response_failures(response, expectation, runtime, policies[runtime], role), "emitted conditional admission fields fit consumer"
        for field in schema["allOf"][1]["then"]["properties"]["admission"]["required"]:
            bad = copy.deepcopy(response); del bad["admission"][field]
            assert response_failures(bad, expectation, runtime, policies[runtime], role), field
        response["admission"]["kind"] = "explicit-user-selection"
        for verdict in ("equivalent", "loss"):
            response["compression"]["verdict"] = verdict
            response["compression"]["invariants"] = {name: True for name in INVARIANTS}
            if verdict == "loss":
                response["compression"]["invariants"]["force"] = False
            expectation["compression"] = verdict
            assert not response_failures(response, expectation, runtime, policies[runtime], role), verdict
            bad = copy.deepcopy(response); bad["compression"]["invariants"]["force"] = "false"
            assert response_failures(bad, expectation, runtime, policies[runtime], role), "invariants must be booleans"
        # The illustrative nested pair shapes must also be acceptable to pair().
        assert pair(probe["response_fields"]["alternatives"][0]["pair"])
        assert pair(probe["response_fields"]["proposed_worker"])
    print("OK: emitted probe/consumer shape parity, both runtimes, variant role overrides and old mismatch red controls; synthetic only")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", type=Path, default=CORPUS)
    parser.add_argument("--oracle", type=Path, default=ORACLE)
    parser.add_argument("--results", type=Path)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--require-live", action="store_true")
    parser.add_argument("--probe-input", choices=RUNTIMES)
    args = parser.parse_args()
    if args.require_live and not args.results:
        parser.error("--require-live requires --results")
    if args.probe_input and (args.results or args.self_test or args.require_live):
        parser.error("--probe-input cannot combine with result/self-test modes")
    try:
        corpus, oracle = read_json(args.corpus), read_json(args.oracle)
        errors = validate_inputs(corpus, oracle)
        if errors:
            print("\n".join(errors)); return 1
        if args.probe_input:
            print(json.dumps(probe_input(corpus, args.probe_input), indent=2)); return 0
        policies = {"codex": codex_policy(), "claude-code": claude_policy()}
        if args.self_test:
            self_test(corpus, oracle, policies)
            probe_schema_self_test(corpus, policies)
        if args.results:
            errors.extend(validate_results(read_json(args.results), corpus, oracle, policies, args.require_live))
        if errors:
            print("\n".join(errors)); return 1
        print("OK: allocation-only records/source contract; availability, child dispatch and worker quality unproven")
        return 0
    except (CannotRun, PolicyLoadError, OSError, UnicodeError) as exc:
        print(f"could not run: {exc}", file=sys.stderr); return 2
    except (ValueError, AssertionError, KeyError, TypeError) as exc:
        print(f"FINDINGS: {exc}", file=sys.stderr); return 1


if __name__ == "__main__":
    raise SystemExit(main())
