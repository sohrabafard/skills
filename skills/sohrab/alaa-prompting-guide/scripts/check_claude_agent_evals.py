#!/usr/bin/env python3
"""Validate Claude comparison design and evidence records; never invoke models."""
from __future__ import annotations

import argparse
import copy
import math
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
from claude_model_policy import (CannotRun, DEFAULT_POLICY, SKILL_ROOT, load_policy,
    nonempty, pair_valid, read_json, relative_file, semver_key)

CORPUS = SKILL_ROOT / "assets/evals/claude-agent-comparisons.json"
EXPECTED = frozenset("exploration bounded-implementation debugging known-defect-review architecture instruction-rewrite documentation failed-check".split())


def validate_corpus(corpus, policy):
    if not isinstance(corpus, dict) or type(corpus.get("schema_version")) is not int or corpus["schema_version"] != 1:
        return ["invalid corpus schema"]
    errors = []
    if corpus.get("policy_version") != policy["policy_version"]:
        errors.append("corpus policy version drift")
    cases = corpus.get("scenarios")
    if not isinstance(cases, list):
        return errors + ["scenarios must be an array"]
    names = [case.get("id") for case in cases if isinstance(case, dict)]
    if len(names) != len(EXPECTED) or any(not isinstance(x, str) for x in names) or set(names) != EXPECTED:
        errors.append("exactly eight representative scenarios required")
    for case in cases:
        if not isinstance(case, dict):
            errors.append("scenario must be object")
            continue
        if type(case.get("repetitions")) is not int or case["repetitions"] != 2 or case.get("status") != "unrun":
            errors.append("corpus must stay unrun with two repetitions")
        if not nonempty(case.get("prompt")) or len(case["prompt"]) < 40:
            errors.append("concrete prompt required")
        inputs = case.get("inputs")
        if not isinstance(inputs, dict) or not inputs or any(relative_file(k) is None or not nonempty(v) or len(v) < 20 for k,v in inputs.items()):
            errors.append("safe substantive input fixtures required")
        for key in ("acceptance_criteria", "forbidden_actions"):
            values = case.get(key)
            if not isinstance(values, list) or len(values) < 2 or any(not nonempty(v) for v in values):
                errors.append(f"{key} required")
        profile = policy["profiles"].get(case.get("profile")) if isinstance(case.get("profile"), str) else None
        candidate, comparator = case.get("candidate"), case.get("comparator")
        if not isinstance(candidate, dict) or not isinstance(comparator, dict):
            errors.append("candidate/comparator objects required")
            continue
        if not profile or candidate != {"model":profile["model"], "effort":profile["effort"]}:
            errors.append("candidate profile drift")
        if sum(candidate.get(k) != comparator.get(k) for k in ("model", "effort")) != 1:
            errors.append("comparison must change exactly one factor")
        for pair in (candidate, comparator):
            if set(pair) != {"model", "effort"} or not pair_valid(pair, policy):
                errors.append("invalid comparison pair")
    return errors


def validate_resolution(record):
    """Check a recorded/synthetic precedence claim, not the serving runtime."""
    if not isinstance(record, dict):
        return ["resolution record required"]
    errors = []
    version = record.get("claude_code_version")
    if not isinstance(version, str) or not re.fullmatch(r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)", version):
        return ["resolution needs exact Claude Code version"]
    parts = tuple(int(x) for x in version.split("."))
    controls = record.get("model_controls")
    keys = {"invocation", "frontmatter", "environment", "parent", "force"}
    if not isinstance(controls, dict) or set(controls) != keys or any(v is not None and not nonempty(v) for v in controls.values()):
        return ["resolution model_controls invalid"]
    if controls["force"] and parts < (2,1,257):
        errors.append("force override unsupported for recorded version")
    order = ("invocation", "frontmatter", "environment", "parent") if parts >= (2,1,251) else ("environment", "invocation", "frontmatter", "parent")
    if controls["force"] and parts >= (2,1,257):
        order = ("force",) + order
    # These records require resolved full IDs; aliases/inherit need separate host evidence.
    if any(v in ("opus", "sonnet", "fable", "haiku", "inherit") for v in controls.values()):
        errors.append("resolution contract requires resolved IDs, not aliases/inherit")
    expected = next((key for key in order if controls[key]), None)
    if expected is None or record.get("selected_source") != expected:
        errors.append("recorded precedence mismatch")
    if record.get("provider_and_caps_checked") is not True or not nonempty(record.get("evidence")):
        errors.append("resolution needs provider/cap checks and evidence")
    return errors


def validate_availability(version, requested, case, configuration, policy):
    """Require sourced model minima; candidate roles may impose a higher minimum."""
    model = policy["models"][requested["model"]]
    minimum = model.get("minimum_claude_code")
    try:
        threshold = semver_key(minimum)
    except ValueError:
        return [f"{requested['model']}: completed run requires canonical minimum_claude_code evidence"]
    if configuration == "candidate":
        profile_minimum = policy["profiles"][case["profile"]]["availability"]["minimum_claude_code"]
        if semver_key(profile_minimum) > threshold:
            minimum, threshold = profile_minimum, semver_key(profile_minimum)
    if semver_key(version) < threshold:
        return [f"{case['id']}/{configuration}: Claude Code {version} is below minimum_claude_code {minimum} for {requested['model']}"]
    return []


def validate_results(results, corpus, policy):
    if not isinstance(results, dict) or type(results.get("schema_version")) is not int or results["schema_version"] != 1:
        return ["invalid results schema"]
    errors = []
    if results.get("policy_version") != policy["policy_version"]:
        errors.append("result policy version drift")
    if type(results.get("complete")) is not bool or type(results.get("synthetic")) is not bool:
        errors.append("complete and synthetic must be booleans")
    cases = {case["id"]:case for case in corpus["scenarios"]}
    expected = {(name, kind, rep) for name in cases for kind in ("candidate", "comparator") for rep in (1,2)}
    rows = results.get("runs")
    if not isinstance(rows, list):
        return errors + ["runs must be array"]
    seen = set()
    for row in rows:
        if not isinstance(row, dict):
            errors.append("run must be object")
            continue
        key = row.get("scenario"), row.get("configuration"), row.get("repetition")
        if not isinstance(key[0], str) or not isinstance(key[1], str) or type(key[2]) is not int or key not in expected or key in seen:
            errors.append("unexpected or duplicate run key")
            continue
        seen.add(key)
        case = cases[key[0]]
        requested = case[key[1]]
        if row.get("requested") != requested:
            errors.append("requested configuration drift")
        status = row.get("status")
        if status not in ("passed", "failed", "blocked", "unrun"):
            errors.append("invalid run status")
        if status == "blocked" and not nonempty(row.get("blocker")):
            errors.append("blocked run needs blocker")
        if status not in ("passed", "failed"):
            if row.get("configuration_verified") is True:
                errors.append("unrun or blocked work cannot verify a configuration")
            continue
        for field in ("output_evidence", "reviewer", "execution_surface", "fixture_revision", "account_type"):
            if not nonempty(row.get(field)):
                errors.append(f"completed run needs {field}")
        if row.get("independent_review") is not True:
            errors.append("completed result requires independent review")
        for field in ("elapsed_seconds", "usage", "correction_count"):
            value = row.get(field)
            if value != "unknown" and (type(value) not in (int,float) or not math.isfinite(value) or value < 0):
                errors.append(f"{field} must be nonnegative number or unknown")
        verdicts = row.get("criterion_verdicts")
        if not isinstance(verdicts, list) or len(verdicts) != len(case["acceptance_criteria"]) or any(v not in ("pass", "fail", "unknown") for v in verdicts):
            errors.append("one criterion verdict per acceptance criterion required")
        forbidden = row.get("forbidden_actions_observed")
        if not isinstance(forbidden, list) or any(not nonempty(x) for x in forbidden):
            errors.append("forbidden_actions_observed invalid")
        if type(row.get("configuration_verified")) is not bool:
            errors.append("configuration_verified must be boolean")
        observed = row.get("observed")
        if not isinstance(observed, dict) or set(observed) != {"model","effort"} or not nonempty(observed.get("model")) or (observed.get("effort") is not None and not nonempty(observed.get("effort"))):
            errors.append("observed identity required; unavailable is unknown")
        else:
            mismatch = any(observed[k] != "unknown" and observed[k] != requested[k] for k in ("model","effort"))
            if mismatch and (status == "passed" or row.get("configuration_verified") is True):
                errors.append("observed mismatch cannot pass or verify requested configuration")
            if "unknown" in observed.values() and row.get("configuration_verified") is True and not nonempty(row.get("configuration_control_evidence")):
                errors.append("unknown identity requires configuration_control_evidence")
        resolution = row.get("resolution")
        resolution_errors = validate_resolution(resolution)
        errors.extend(resolution_errors)
        if not resolution_errors:
            errors.extend(validate_availability(resolution["claude_code_version"], requested, case, key[1], policy))
            resolved = resolution["model_controls"][resolution["selected_source"]]
            if resolved != requested["model"] and (status == "passed" or row.get("configuration_verified") is True):
                errors.append("resolved control mismatch cannot pass or verify requested configuration")
        fallback = row.get("fallback")
        if not isinstance(fallback, dict) or fallback.get("kind") not in ("none","safety","overload","unknown") or fallback.get("safeguards_preserved") is not True or type(fallback.get("disclosed")) is not bool:
            errors.append("fallback must record kind, disclosure and preserved safeguards")
        elif fallback["kind"] != "none":
            if not fallback["disclosed"] or not nonempty(fallback.get("evidence")):
                errors.append("fallback/uncertainty must be disclosed with evidence")
            if status == "passed" or row.get("configuration_verified") is True:
                errors.append("fallback run cannot prove requested pair")
        if status == "passed" and (not isinstance(verdicts,list) or any(v != "pass" for v in verdicts) or forbidden != [] or row.get("configuration_verified") is not True):
            errors.append("pass requires all criteria, no forbidden action, verified configuration")
    if seen != expected:
        errors.append("results require all 32 run keys, including explicit unrun work")
    if results.get("complete") is True and any(not isinstance(row,dict) or row.get("status") not in ("passed","failed") for row in rows):
        errors.append("complete cannot hide blocked/unrun work")
    return errors


def validate_calibration(path, role, profile, policy):
    corpus = read_json(CORPUS)
    results = read_json(path)
    errors = validate_corpus(corpus, policy)
    if errors:
        return errors
    errors = validate_results(results, corpus, policy)
    if not isinstance(results, dict):
        return errors
    if results.get("complete") is not True or results.get("synthetic") is not False:
        errors.append(f"{role}: calibration requires complete nonsynthetic evidence")
    cases = {case["id"] for case in corpus["scenarios"] if case["profile"] == role}
    if not cases:
        errors.append(f"{role}: no matching representative scenario for calibration")
    rows = results.get("runs", [])
    if isinstance(rows, list):
        candidate_rows = [row for row in rows if isinstance(row,dict) and row.get("scenario") in cases and row.get("configuration") == "candidate"]
        pair = {"model":profile["model"], "effort":profile["effort"]}
        if len(candidate_rows) != 2 * len(cases) or any(row.get("status") != "passed" or row.get("observed") != pair for row in candidate_rows):
            errors.append(f"{role}: calibration requires both matching observed candidate runs to pass")
    return errors


def availability_self_test(corpus, policy, completed_row):
    """Synthetic contract records only; never persisted or reported as live evidence."""
    from contextlib import redirect_stderr
    from io import StringIO
    from unittest.mock import patch

    results = {"schema_version":1, "policy_version":policy["policy_version"],
               "complete":True, "synthetic":False, "runs":[]}
    for case in corpus["scenarios"]:
        for kind in ("candidate", "comparator"):
            for repetition in (1, 2):
                row = copy.deepcopy(completed_row)
                pair = case[kind]
                row.update(scenario=case["id"], configuration=kind, repetition=repetition,
                           requested=pair.copy(), observed=pair.copy(),
                           criterion_verdicts=["pass"] * len(case["acceptance_criteria"]))
                row["resolution"].update(claude_code_version="2.1.280", selected_source="frontmatter",
                    model_controls={"invocation":None,"frontmatter":pair["model"],
                                    "environment":None,"parent":None,"force":None})
                results["runs"].append(row)

    role = "alaa-reviewer"
    def calibration_errors(value, selected_policy=policy):
        def inputs(path):
            return corpus if Path(path) == CORPUS else value
        with patch(__name__ + ".read_json", side_effect=inputs):
            return validate_calibration(Path("synthetic-record.json"), role,
                                        selected_policy["profiles"][role], selected_policy)

    assert not validate_results(results, corpus, policy)
    assert not calibration_errors(results)
    cases = {case["id"]:case for case in corpus["scenarios"]}
    # Exercise each selected model for both candidate and comparator rows.
    tested = set()
    for index, row in enumerate(results["runs"]):
        key = row["requested"]["model"], row["configuration"]
        if key in tested:
            continue
        tested.add(key)
        case = cases[row["scenario"]]
        minimum = policy["models"][key[0]]["minimum_claude_code"]
        if key[1] == "candidate":
            profile_minimum = policy["profiles"][case["profile"]]["availability"]["minimum_claude_code"]
            minimum = max((minimum, profile_minimum), key=semver_key)
        parts = minimum.split(".")
        below = ".".join(parts[:-1] + [str(int(parts[-1]) - 1)])
        for version, findings in ((below, True), (minimum, False), ("2.1.282", False)):
            changed = copy.deepcopy(results)
            changed["runs"][index]["resolution"]["claude_code_version"] = version
            errors = validate_results(changed, corpus, policy)
            assert bool(errors) == findings, (key, version, errors)
            assert bool(calibration_errors(changed)) == findings, ("calibration", key, version)
    impossible = copy.deepcopy(results)
    for row in impossible["runs"]:
        row["resolution"]["claude_code_version"] = "0.0.0"
    assert any("minimum_claude_code" in e for e in validate_results(impossible, corpus, policy))
    assert any("minimum_claude_code" in e for e in calibration_errors(impossible))
    higher = copy.deepcopy(policy)
    higher["profiles"][role]["availability"]["minimum_claude_code"] = "2.1.281"
    assert any("minimum_claude_code" in e for e in validate_results(results, corpus, higher))
    assert any("minimum_claude_code" in e for e in calibration_errors(results, higher))
    unknown = copy.deepcopy(policy)
    del unknown["models"]["claude-fable-5-1"]["minimum_claude_code"]
    assert any("canonical minimum_claude_code" in e for e in validate_results(results, corpus, unknown))
    assert any("canonical minimum_claude_code" in e for e in calibration_errors(results, unknown))
    deferred = copy.deepcopy(impossible)
    deferred["complete"] = False
    for row in deferred["runs"]:
        row.update(status="blocked", blocker="CLI below required version", configuration_verified=False)
    assert not validate_results(deferred, corpus, unknown)
    for row in deferred["runs"]:
        row["status"] = "unrun"
    assert not validate_results(deferred, corpus, unknown)
    deferred["runs"][0]["configuration_verified"] = True
    assert validate_results(deferred, corpus, unknown)

    malformed = SKILL_ROOT / "scripts/fixtures/claude-policy/malformed.json"
    for source in ("result", "corpus"):
        try:
            with patch(__name__ + ".CORPUS", malformed if source == "corpus" else CORPUS):
                validate_calibration(malformed, role, policy["profiles"][role], policy)
        except CannotRun:
            pass
        else:
            raise AssertionError(f"malformed {source} did not preserve CannotRun")
    read_text = Path.read_text
    def deny_evidence(path, *args, **kwargs):
        if path == malformed:
            raise PermissionError("synthetic unreadable evidence fixture")
        return read_text(path, *args, **kwargs)
    try:
        with patch.object(Path, "read_text", deny_evidence):
            validate_calibration(malformed, role, policy["profiles"][role], policy)
    except CannotRun:
        pass
    else:
        raise AssertionError("unreadable result did not preserve CannotRun")
    for option in ("--results", "--corpus"):
        with patch.object(sys, "argv", ["check_claude_agent_evals.py", option, str(malformed)]), redirect_stderr(StringIO()):
            assert main() == 2, f"malformed {option} did not return exit 2"
    with patch.object(sys, "argv", ["check_claude_agent_evals.py", "--results", str(malformed)]), patch.object(Path, "read_text", deny_evidence), redirect_stderr(StringIO()):
        assert main() == 2, "unreadable evidence did not return exit 2"


def self_test(corpus, policy):
    assert not validate_corpus(corpus, policy)
    base = {"schema_version":1,"policy_version":policy["policy_version"],"complete":False,"synthetic":True,"runs":[{"scenario":c["id"],"configuration":kind,"repetition":rep,"requested":c[kind],"status":"unrun"} for c in corpus["scenarios"] for kind in ("candidate","comparator") for rep in (1,2)]}
    assert not validate_results(base,corpus,policy)
    assert validate_results({**base,"complete":True},corpus,policy)
    assert validate_results({**base,"runs":base["runs"][:-1]},corpus,policy)
    complete = copy.deepcopy(base)
    first=complete["runs"][0]
    pair=first["requested"]
    first.update(status="passed",output_evidence="synthetic/output",reviewer="independent fixture",execution_surface="synthetic",fixture_revision="fixture-v1",account_type="synthetic",independent_review=True,elapsed_seconds="unknown",usage="unknown",correction_count=0,criterion_verdicts=["pass"]*len(corpus["scenarios"][0]["acceptance_criteria"]),forbidden_actions_observed=[],configuration_verified=True,observed=pair.copy(),resolution={"claude_code_version":"2.1.280","model_controls":{"invocation":None,"frontmatter":pair["model"],"environment":"claude-opus-5-5","parent":"claude-opus-5-5","force":None},"selected_source":"frontmatter","provider_and_caps_checked":True,"evidence":"synthetic/control"},fallback={"kind":"none","disclosed":True,"safeguards_preserved":True})
    assert not validate_results(complete,corpus,policy)
    availability_self_test(corpus, policy, first)
    for field,value in (("observed",{"model":"unknown","effort":"unknown"}),("forbidden_actions_observed",["edited outside scope"]),("independent_review",False),("configuration_verified",False)):
        bad=copy.deepcopy(complete);bad["runs"][0][field]=value
        assert validate_results(bad,corpus,policy),field
    unknown=copy.deepcopy(complete);unknown["runs"][0].update(observed={"model":"unknown","effort":"unknown"},configuration_control_evidence="synthetic/resolved-settings")
    assert not validate_results(unknown,corpus,policy)
    mismatch=copy.deepcopy(complete);mismatch["runs"][0]["observed"]["model"]="claude-opus-5-5"
    assert validate_results(mismatch,corpus,policy)
    mismatch["runs"][0].update(status="failed",configuration_verified=False)
    assert not validate_results(mismatch,corpus,policy)
    resolution=first["resolution"]
    old=copy.deepcopy(resolution);old["claude_code_version"]="2.1.221"
    assert validate_resolution(old)
    old["selected_source"]="environment";assert not validate_resolution(old)
    forced=copy.deepcopy(resolution);forced["model_controls"]["force"]="claude-opus-5-5"
    assert validate_resolution(forced)
    forced["selected_source"]="force";assert not validate_resolution(forced)
    forced["claude_code_version"]="2.1.251";assert validate_resolution(forced)
    for kind in ("safety","overload","unknown"):
        fallback=copy.deepcopy(complete);r=fallback["runs"][0]
        r["fallback"].update(kind=kind,evidence="synthetic/fallback")
        assert validate_results(fallback,corpus,policy)
        r.update(status="failed",configuration_verified=False)
        assert not validate_results(fallback,corpus,policy)
        r["fallback"]["safeguards_preserved"]=False
        assert validate_results(fallback,corpus,policy)
    print("OK: corpus, identity, precedence, availability boundaries, fallback and evidence exit fixtures; no live runs")


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus",type=Path,default=CORPUS)
    parser.add_argument("--results",type=Path)
    parser.add_argument("--self-test",action="store_true")
    args=parser.parse_args()
    try:
        policy=load_policy(DEFAULT_POLICY)
        corpus=read_json(args.corpus)
        errors=validate_corpus(corpus,policy)
        if not errors and args.self_test:
            self_test(corpus,policy)
        if not errors and args.results:
            errors.extend(validate_results(read_json(args.results),corpus,policy))
        if errors:
            print("\n".join(errors));return 1
        print("OK: Claude comparison records valid; source validation is not calibration")
        return 0
    except (CannotRun,OSError,UnicodeError) as exc:
        print(f"could not run: {exc}",file=sys.stderr);return 2
    except (ValueError,AssertionError) as exc:
        print(f"FINDINGS: {exc}",file=sys.stderr);return 1


if __name__=="__main__":
    raise SystemExit(main())
