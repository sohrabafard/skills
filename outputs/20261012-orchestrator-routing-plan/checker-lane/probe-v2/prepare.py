from pathlib import Path
import hashlib, json, os, subprocess, sys
repo = Path.cwd()
base = repo / 'outputs/20261012-orchestrator-routing-plan/checker-lane'
bundle = base / 'probe-v2'
owner = repo / 'skills/sohrab/alaa-prompting-guide'
sys.path.insert(0, str(owner / 'scripts'))
from check_allocation_evals import contract_paths, digest, records, neutral_input, UNKNOWN_PAIR
corpus = json.loads((owner / 'assets/evals/allocation-cases.json').read_bytes())
oracle = json.loads((owner / 'assets/evals/allocation-oracle.json').read_bytes())
template = {'schema_version': 1, 'purpose': 'allocation-results', 'synthetic': False, 'complete': False, 'corpus_sha256': digest(corpus), 'oracle_sha256': digest(oracle), 'configurations': [], 'runs': []}
for runtime, model, identifier in (('codex', 'gpt-6.1-sol', 'codex-sol61-high'), ('claude-code', 'claude-sonnet-5-5', 'claude-sonnet55-high')):
    loaded = [{'path': path, 'sha256': hashlib.sha256((repo / path).read_bytes()).hexdigest()} for path in contract_paths(runtime)]
    previous = json.loads((base / f'{runtime}-probe-manifest.json').read_bytes())
    assert loaded == previous['loaded_contracts'], 'Nine loaded source owners changed; return to parent before capture'
    emitted = subprocess.run([sys.executable, 'scripts/check_allocation_evals.py', '--probe-input', runtime], cwd=owner, env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'}, capture_output=True, text=True, timeout=120)
    (bundle / f'{runtime}-emission.log').write_text(emitted.stderr, encoding='utf-8')
    assert emitted.returncode == 0, emitted.stderr + emitted.stdout
    input_path = bundle / f'{runtime}-probe-input.json'
    input_path.write_text(emitted.stdout, encoding='utf-8')
    source = '\n\n'.join(f"SOURCE: {item['path']}\nSHA256: {item['sha256']}\n" + (repo / item['path']).read_text(encoding='utf-8') for item in loaded)
    (bundle / f'{runtime}-loaded-contracts.txt').write_text(source + '\n', encoding='utf-8')
    request = 'This is a decision-only allocation observation. Apply the supplied frozen contracts to each supplied simulated worker scenario. Actual allocator controls do not establish worker host availability or child control realization. Do not execute operational commands, dispatch a worker or use tools.\n\n' + source + '\n\nNEUTRAL PROBE INPUT:\n' + emitted.stdout
    request += '\nReturn exactly one JSON object {"responses":[{"case":"case ID","variant":"variant ID","response":{all required response properties}}]}. Include each case/variant exactly once, without Markdown, fences or commentary. Follow response_schema and response_rules. Copy response_role exactly. Use object pairs, never a string such as model/effort. proposed_worker is an object iff action=allocate; otherwise JSON null. Evidence strings must be concise and nonempty.\n'
    request_path = bundle / f'{runtime}-allocation-request.txt'
    request_path.write_text(request, encoding='utf-8')
    manifest = {'bundle': 'probe-v2', 'runtime': runtime, 'command': 'python scripts/check_allocation_evals.py --probe-input ' + runtime, 'exit': emitted.returncode, 'input_sha256': hashlib.sha256(input_path.read_bytes()).hexdigest(), 'request_sha256': hashlib.sha256(request_path.read_bytes()).hexdigest(), 'emitter_path': 'skills/sohrab/alaa-prompting-guide/scripts/check_allocation_evals.py', 'emitter_sha256': hashlib.sha256((owner / 'scripts/check_allocation_evals.py').read_bytes()).hexdigest(), 'loaded_contracts': loaded, 'claims': 'neutral response-contract repair only; no inference, grading, actual allocation or worker dispatch'}
    (bundle / f'{runtime}-probe-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    template['configurations'].append({'id': identifier, 'runtime': runtime, 'allocator_requested': {'model': model, 'effort': 'high'}, 'allocator_effective': UNKNOWN_PAIR.copy(), 'allocator_observed': UNKNOWN_PAIR.copy(), 'control_evidence': 'unknown', 'loaded_contracts': loaded})
    for (case, variant), value in records(corpus).items():
        for repetition in (1, 2):
            template['runs'].append({'case': case, 'variant': variant, 'configuration': identifier, 'runtime': runtime, 'repetition': repetition, 'status': 'unrun', 'input_sha256': digest(neutral_input(value, runtime))})
(bundle / 'allocation-results-unrun.json').write_text(json.dumps(template, indent=2) + '\n', encoding='utf-8')
print('Prepared v2 for both runtimes, unchanged nine source owners/cases/private oracle; 120 explicit unrun keys. No runtime execution.')
