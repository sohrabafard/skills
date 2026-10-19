from pathlib import Path
import ast
import json
import runpy
import sys

evidence = Path(__file__).parent
baseline = {entry['path']: entry for entry in json.loads((evidence / 'ORCH-FINAL-read-baseline.json').read_text(encoding='utf-8'))['files']}
results = []
for name, suffix in [('alaa-codex-orchestrator', '.toml'), ('alaa-cc-orchestrator', '.md')]:
    root = Path('skills/sohrab') / name
    checker = root / 'scripts/check_agent_contracts.py'
    ast.parse(checker.read_text(encoding='utf-8'))
    api = runpy.run_path(str(checker))
    current = api['specialist_cadence_sources']()
    failures = api['specialist_cadence_failures'](*current)
    cases = api['specialist_cadence_self_tests']()
    # Exercise the changed caller seam only; broad cadence self-tests stay with
    # the independent verifier. A missing consumer clause must propagate.
    integrated = list(api['cadence_sources']())
    propagated = []
    for index, label in [(6, 'design template'), (7, 'contract template'), (8, 'architecture critic')]:
        broken = list(integrated)
        broken[index] = broken[index].replace('declared phase|final boundary', 'omitted')
        expected = label + ': missing specialist cadence: declared phase|final boundary'
        propagated.append((label, expected in api['cadence_failures'](*broken)))
    old = tuple(baseline[(root / path).as_posix()]['text'] for path in (
        'references/delegation-prompts/20-design.md',
        'references/delegation-prompts/60-contract-review.md',
        'agents/alaa-architecture-critic' + suffix))
    old_failures = api['specialist_cadence_failures'](*old)
    regressions = [item for item in old_failures if 'premature specialist judgment' in item]
    passed = not failures and all(ok for _, ok in cases + propagated) and len(regressions) >= 4
    results.append({'runtime': name, 'passed': passed, 'assertion_errors': failures,
                    'self_tests': cases, 'caller_seam': propagated,
                    'baseline_red_diagnostics': regressions,
                    'scope': 'specialist cadence source assertions, isolated mutations, changed cadence consumer seam; no full checker or pack'})
    print(f'{name}: assertion errors={len(failures)}; self-tests={sum(ok for _, ok in cases)}/{len(cases)}; caller seam={sum(ok for _, ok in propagated)}/3; original early-review diagnostics={len(regressions)}')
(evidence / 'ORCH-FINAL-focused.json').write_text(json.dumps(results, indent=2) + '\n', encoding='utf-8', newline='\n')
sys.exit(0 if all(item['passed'] for item in results) else 1)
