from pathlib import Path
import hashlib, json
root = Path.cwd()
bundle = root / 'outputs/20261012-orchestrator-routing-plan/checker-lane/probe-v2'
source = root / 'skills/sohrab/alaa-prompting-guide/scripts/check_allocation_evals.py'
raw = source.read_bytes()
(bundle / 'checker-before.py').write_bytes(raw)
(bundle / 'preservation.json').write_text(json.dumps({'checker_before_sha256': hashlib.sha256(raw).hexdigest(), 'preserved_paths': [{'path': path.relative_to(root).as_posix(), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()} for path in (root / 'outputs/20261012-orchestrator-routing-plan/checker-lane').iterdir() if path.is_file() and (path.name.endswith(('-probe-input.json', '-probe-manifest.json', '-loaded-contracts.txt', '-allocation-request.txt')) or path.name == 'allocation-results-unrun.json')]}, indent=2) + '\n', encoding='utf-8')
newline = b'\r\n' if b'\r\n' in raw else b'\n'
start = raw.index(b'def probe_input(')
end = raw.index(newline + newline + b'def main():', start)
new = '''def response_schema():
    """Neutral JSON Schema: syntax and existing consumer conditions, no oracle."""
    text = {"type": "string", "minLength": 1}
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
                 "then": {"properties": {"admission": {"required": ["source", "remaining_reasoning", "rejected_cheaper", "decomposition"]}}}}]}


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
                "admission always needs kind and nonempty evidence. When proposing an exceptional model under official-task-priority or high-workhorse-inadequacy, also supply nonempty source, remaining_reasoning, rejected_cheaper and decomposition. An explicit human selection retains the exact requested model and effort.",
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
'''
source.write_bytes(raw[:start] + new.replace('\n', newline.decode()).encode() + raw[end:])
raw = source.read_bytes()
before = b'        if args.self_test:' + newline + b'            self_test(corpus, oracle, policies)'
assert raw.count(before) == 1
source.write_bytes(raw.replace(before, before + newline + b'            probe_schema_self_test(corpus, policies)'))
print('Only authorized source checker updated; consumer rules unchanged, neutral response schema clarified.')
