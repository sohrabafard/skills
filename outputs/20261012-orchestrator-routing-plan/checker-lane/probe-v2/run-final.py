from pathlib import Path
import json, os, subprocess, sys
from datetime import datetime, timezone
repo = Path.cwd()
bundle = repo / 'outputs/20261012-orchestrator-routing-plan/checker-lane/probe-v2'
owner = repo / 'skills/sohrab/alaa-prompting-guide'
steps = [(owner, ['scripts/check_allocation_evals.py', '--self-test'], 'checker-self-test-final'), (repo, ['outputs/20261012-orchestrator-routing-plan/checker-lane/probe-v2/prepare.py'], 'prepare'), (repo, ['outputs/20261012-orchestrator-routing-plan/checker-lane/probe-v2/check-generated-probes.py'], 'generated-parity')]
for cwd, arguments, name in steps:
    result = subprocess.run([sys.executable, *arguments], cwd=cwd, env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'}, timeout=120, capture_output=True, text=True)
    log = bundle / (name + '.log')
    log.write_text(result.stdout + result.stderr, encoding='utf-8')
    record = {'command': 'python ' + ' '.join(arguments), 'cwd': cwd.relative_to(repo).as_posix() or '.', 'exit': result.returncode, 'timestamp': datetime.now(timezone.utc).isoformat(), 'resource_policy': 'sequential static Python, PYTHONDONTWRITEBYTECODE=1, timeout120s', 'log': log.name, 'proof': 'synthetic schema/consumer evidence only; no runtime allocation'}
    with (bundle / 'focused-results.jsonl').open('a', encoding='utf-8') as output: output.write(json.dumps(record) + '\n')
    print(name, result.returncode, result.stdout + result.stderr)
    if result.returncode: raise SystemExit(result.returncode)
