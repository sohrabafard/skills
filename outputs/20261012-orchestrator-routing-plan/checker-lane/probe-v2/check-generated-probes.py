"""Test only the JSON Schema keyword subset emitted by this probe, plus consumer parity."""
from pathlib import Path
import copy, json, re, sys
repo = Path.cwd()
bundle = repo / 'outputs/20261012-orchestrator-routing-plan/checker-lane/probe-v2'
owner = repo / 'skills/sohrab/alaa-prompting-guide'
sys.path.insert(0, str(owner / 'scripts'))
from check_allocation_evals import CORPUS, RUNTIMES, probe_schema_self_test, response_failures, schema_fixture, claude_policy, codex_policy
policies = {'codex': codex_policy(), 'claude-code': claude_policy()}
corpus = json.loads(CORPUS.read_bytes())
probes = {runtime: json.loads((bundle / f'{runtime}-probe-input.json').read_bytes()) for runtime in RUNTIMES}
probe_schema_self_test(corpus, policies, probes)
def matches(value, schema):
    if 'const' in schema and json.dumps(value, sort_keys=True) != json.dumps(schema['const'], sort_keys=True): return False
    if 'enum' in schema and not any(type(value) is type(item) and value == item for item in schema['enum']): return False
    types = {'object': dict, 'array': list, 'string': str, 'boolean': bool, 'null': type(None)}
    if 'type' in schema and type(value) is not types[schema['type']]: return False
    if isinstance(value, str) and (len(value) < schema.get('minLength', 0) or ('pattern' in schema and not re.search(schema['pattern'], value))): return False
    if isinstance(value, dict):
        if any(key not in value for key in schema.get('required', [])): return False
        if schema.get('additionalProperties') is False and set(value) - set(schema.get('properties', {})): return False
        if any(key in value and not matches(value[key], item) for key, item in schema.get('properties', {}).items()): return False
    if isinstance(value, list):
        if len(value) < schema.get('minItems', 0): return False
        if 'items' in schema and any(not matches(item, schema['items']) for item in value): return False
    if 'allOf' in schema and not all(matches(value, item) for item in schema['allOf']): return False
    if 'anyOf' in schema and not any(matches(value, item) for item in schema['anyOf']): return False
    if 'not' in schema and matches(value, schema['not']): return False
    if 'if' in schema:
        branch = 'then' if matches(value, schema['if']) else 'else'
        if branch in schema and not matches(value, schema[branch]): return False
    return True
positives = 0
for runtime, probe in probes.items():
    common = probe['response_schema']
    for case in probe['cases']:
        schema = {'allOf': [common, {'properties': {'role': {'const': case['response_role']}}}]}
        role = case['response_role']
        for action in common['properties']['action']['enum']:
            response = schema_fixture(common)
            response.update(role=role, action=action)
            if action != 'allocate': response['proposed_worker'] = None
            assert matches(response, schema), (runtime, case['input']['case'], action)
            assert not response_failures(response, {'action': action, 'allowed_models': {runtime: []}}, runtime, policies[runtime], role, False)
            positives += 1
        response = schema_fixture(common); response.update(role=role)
        for field, value in (('alternatives', [{'pair': 'model/effort', 'reason': 'fixture', 'evidence': 'fixture'}]), ('role', 'task authority role'), ('proposed_worker', 'model/effort'), ('proposed_worker', None), ('model_reason', ' ')):
            bad = copy.deepcopy(response); bad[field] = value
            assert not matches(bad, schema), field
            assert response_failures(bad, {'action': 'allocate', 'allowed_models': {runtime: []}}, runtime, policies[runtime], role, False), field
        bad = copy.deepcopy(response); bad['action'] = 'reject'
        assert not matches(bad, schema), 'nonallocation proposal must be null'
    case = probe['cases'][0]
    schema = {'allOf': [common, {'properties': {'role': {'const': case['response_role']}}}]}
    response = schema_fixture(common); response.update(role=case['response_role'])
    response['proposed_worker'] = {'model': 'gpt-6-astra' if runtime == 'codex' else 'claude-fable-5-1', 'effort': 'medium'}
    assert not matches(response, schema), 'frontier ordinary admission must fail'
    response['admission']['kind'] = 'official-task-priority'
    assert matches(response, schema)
    for field in ('source', 'remaining_reasoning', 'rejected_cheaper', 'decomposition'):
        bad = copy.deepcopy(response); del bad['admission'][field]
        assert not matches(bad, schema), field
    for verdict in ('equivalent', 'loss'):
        response['compression']['verdict'] = verdict
        response['compression']['invariants'] = {name: True for name in response['compression']['invariants']}
        if verdict == 'loss': response['compression']['invariants']['force'] = False
        assert matches(response, schema)
        bad = copy.deepcopy(response); bad['compression']['invariants']['force'] = 'false'
        assert not matches(bad, schema)
    bad = copy.deepcopy(response); bad['compression']['invariants']['force'] = True
    assert not matches(bad, schema), 'loss needs a failed invariant'
    bad['compression']['verdict'] = 'equivalent'; bad['compression']['invariants']['force'] = False
    assert not matches(bad, schema), 'equivalent cannot lose force'
print(f'OK: generated neutral schema/consumer parity; {positives} action/role positives, former shape mismatches and conditional admission/compression reds; synthetic only')
