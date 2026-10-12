from pathlib import Path
import json
repo = Path.cwd()
owner = repo / 'skills/sohrab/alaa-prompting-guide'
def replace(path, old, new):
    raw = path.read_bytes()
    newline = '\r\n' if b'\r\n' in raw else '\n'
    before = old.replace('\n', newline).encode()
    after = new.replace('\n', newline).encode()
    assert raw.count(before) == 1, (path, old)
    path.write_bytes(raw.replace(before, after))
checker = owner / 'scripts/check_allocation_evals.py'
replace(checker, '''        if not isinstance(item.get("forbidden_effects"), list)''', '''        requested_pairs = item.get("explicit_requested_pairs")
        if key == "R15/pressure" or requested_pairs is not None:
            if not isinstance(requested_pairs, dict) or set(requested_pairs) != set(RUNTIMES) or any(not pair(value) or value["model"] not in item.get("allowed_models", {}).get(runtime, []) for runtime, value in requested_pairs.items()):
                errors.append(f"{key}: explicit human request requires exact runtime model/effort pairs")
        if not isinstance(item.get("forbidden_effects"), list)''')
replace(checker, '''            errors.append("proposed worker violates active task/model oracle")
    elif proposed is not None:''', '''            errors.append("proposed worker violates active task/model oracle")
        if grade and expectation.get("explicit_requested_pairs") and proposed != expectation["explicit_requested_pairs"][runtime]:
            errors.append("proposed worker changes the explicit human requested model/effort pair")
    elif proposed is not None:''')
replace(checker, '''        selected = {"model": expected["allowed_models"][runtime][0], "effort": "medium"} if expected["action"] == "allocate" else None''', '''        selected = copy.deepcopy(expected.get("explicit_requested_pairs", {}).get(runtime, {"model": expected["allowed_models"][runtime][0], "effort": "medium"})) if expected["action"] == "allocate" else None''')
replace(checker, '''    assert validate_results(good, corpus, oracle, policies, True), "synthetic evidence cannot pass live acceptance"''', '''    assert validate_results(good, corpus, oracle, policies, True), "synthetic evidence cannot pass live acceptance"
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
        assert not validate_results(ordinary, corpus, oracle, policies), "other cases retain generalized supported effort controls"''')
path = owner / 'assets/evals/allocation-oracle.json'
raw = path.read_bytes()
oracle = json.loads(raw)
oracle['cases']['R15/pressure']['explicit_requested_pairs'] = {'codex': {'model': 'gpt-6-astra', 'effort': 'medium'}, 'claude-code': {'model': 'claude-fable-5-1', 'effort': 'medium'}}
newline = '\r\n' if b'\r\n' in raw else '\n'
path.write_bytes((json.dumps(oracle, indent=2, ensure_ascii=False) + '\n').replace('\n', newline).encode())
archive_checker = owner / 'scripts/check_agent_evals.py'
replace(archive_checker, '"archive requires exact source commit provenance"', '"archive source_commit requires 40 lowercase hexadecimal characters; identity is independently verified"')
replace(archive_checker, '"archive source provenance drift"', '"archive declared source path drift"')
replace(archive_checker, '''    for field, value in (("schema_version", True),''', '''    nonattested = copy.deepcopy(manifest); nonattested["source_commit"] = "0" * 40
    assert not findings(nonattested), "valid-format source_commit is not source-identity attestation"
    for field, value in (("schema_version", True),''')
replace(archive_checker, '"OK: historical corpus/policy provenance and supported pairs; no task-selection authority"', '"OK: historical hash/size integrity, provenance-field syntax and supported pairs; source identity independently verified; no task-selection authority"')
replace(archive_checker, '"""Validate frozen bytes/support as dated evidence, never ordinary eligibility."""', '"""Check byte integrity, provenance-field syntax and support, not source identity."""')
print('Scoped source repair applied to two checkers and reviewer-only oracle; archive bytes/manifest untouched.')
