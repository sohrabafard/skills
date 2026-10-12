import copy, hashlib, json
from pathlib import Path
root = Path.cwd()
base = root / 'outputs/20261012-orchestrator-routing-plan'
review = json.loads((base / 'runtime/reviewer-v2-verdict.json').read_text(encoding='utf-8'))
corpus = json.loads((root / 'skills/sohrab/alaa-prompting-guide/assets/evals/allocation-cases.json').read_text(encoding='utf-8'))
oracle = json.loads((root / 'skills/sohrab/alaa-prompting-guide/assets/evals/allocation-oracle.json').read_text(encoding='utf-8'))
manifest = json.loads((base / 'checker-lane/probe-v2/codex-probe-manifest.json').read_text(encoding='utf-8'))
responses = {}
for rep in (1, 2):
    path = base / f'runtime/codex-v2-r{rep}.json'
    raw = path.read_bytes()
    actual = hashlib.sha256(raw).hexdigest()
    expected = review['capture_sha256'][str(rep)]
    if actual != expected:
        raise SystemExit(f'capture hash mismatch for repetition {rep}')
    wrapper = json.loads(raw)
    if set(wrapper) != {'responses'} or len(wrapper['responses']) != 30:
        raise SystemExit(f'invalid wrapper/count for repetition {rep}')
    for entry in wrapper['responses']:
        key = (entry['case'], entry['variant'], rep)
        if key in responses:
            raise SystemExit(f'duplicate response key: {key}')
        responses[key] = entry['response']
if len(responses) != 60:
    raise SystemExit('expected 60 response records across two captures')
exceptions = {}
for item in review['record_status_exceptions']:
    if not item.get('factual_exception_accepted'):
        raise SystemExit('unratified factual exception in reviewer record')
    for variant in item['variants']:
        for rep in item['repetitions']:
            exceptions[(item['case'], variant, rep)] = item
records = {}
for case in corpus['cases']:
    for variant in case['variants']:
        value = {'case': case['id'], 'variant': variant['id'], 'task': case['task'], 'facts': case['facts'], 'variant_facts': variant['facts'], 'simulation': case['simulation']}
        records[(case['id'], variant['id'])] = value
runs = []
for case, variant in sorted(records, key=lambda key: (int(key[0][1:]), key[1])):
    value = records[(case, variant)]
    neutral = copy.deepcopy(value)
    neutral['simulation']['hosts'] = {'codex': neutral['simulation']['hosts']['codex']}
    input_hash = hashlib.sha256(json.dumps(neutral, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()
    for rep in (1, 2):
        response = responses[(case, variant, rep)]
        output_path = base / f'runtime/evidence/codex-v2-r{rep}/{case}-{variant}.json'
        output_path.parent.mkdir(parents=True, exist_ok=True)
        if output_path.exists():
            raise SystemExit(f'refusing to overwrite evidence: {output_path.relative_to(root)}')
        output_bytes = json.dumps(response, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
        output_path.write_bytes(output_bytes)
        exception = exceptions.get((case, variant, rep))
        row = {
            'case': case, 'variant': variant, 'configuration': 'codex-sol61-high', 'runtime': 'codex', 'repetition': rep,
            'status': 'failed' if exception else review['default_record_status'], 'input_sha256': input_hash,
            'response': response, 'output_evidence': output_path.relative_to(root).as_posix(),
            'output_sha256': hashlib.sha256(output_bytes).hexdigest(), 'reviewer': review['reviewer'],
            'independent_review': True, 'criterion_verdicts': review['criterion_verdicts_for_every_record'],
            'forbidden_effects_observed': review['forbidden_effects_observed'],
            'elapsed_seconds': 'unknown', 'usage': 'unknown', 'correction_count': 'unknown',
        }
        if exception:
            row['reviewer_factual_exception'] = {
                'accepted_by_reviewer': True, 'parent_ratified': True,
                'expected_action': exception['expected_action'], 'observed_action': exception['observed_action']
            }
            if 'observed_pair' in exception:
                row['reviewer_factual_exception']['observed_pair'] = exception['observed_pair']
        runs.append(row)
if len(runs) != 60 or sum(r['status'] == 'failed' for r in runs) != 7 or sum(r['status'] == 'passed' for r in runs) != 53:
    raise SystemExit('unexpected status counts; refusing to write matrix')
config = {
    'id': 'codex-sol61-high-v2', 'runtime': 'codex',
    'allocator_requested': {'model': 'gpt-6.1-sol', 'effort': 'high'},
    'allocator_effective': {'model': 'gpt-6.1-sol', 'effort': 'high'},
    'allocator_observed': {'model': 'unknown', 'effort': 'unknown'},
    'control_evidence': 'outputs/20261012-orchestrator-routing-plan/runtime/codex-v2-r1-metadata.json',
    'loaded_contracts': manifest['loaded_contracts'],
}
results = {
    'schema_version': 1, 'purpose': 'allocation-results', 'synthetic': False, 'complete': True,
    'corpus_sha256': hashlib.sha256(json.dumps(corpus, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest(),
    'oracle_sha256': hashlib.sha256(json.dumps(oracle, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest(),
    'configurations': [config], 'runs': runs,
    'review_disposition': 'Parent ratified reviewer-accepted factual exceptions; strict failed statuses and oracle remain unchanged.',
}
out = base / 'runtime/codex-v2-results.json'
if out.exists():
    raise SystemExit(f'refusing to overwrite results: {out.relative_to(root)}')
out.write_text(json.dumps(results, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'Wrote {out.relative_to(root).as_posix()} with {len(runs)} records: 53 passed, 7 failed.')
