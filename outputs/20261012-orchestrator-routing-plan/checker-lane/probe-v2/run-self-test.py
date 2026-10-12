from pathlib import Path
import json, os, subprocess, sys
from datetime import datetime, timezone
repo = Path.cwd()
bundle = repo / 'outputs/20261012-orchestrator-routing-plan/checker-lane/probe-v2'
owner = repo / 'skills/sohrab/alaa-prompting-guide'
command = [sys.executable, 'scripts/check_allocation_evals.py', '--self-test']
result = subprocess.run(command, cwd=owner, env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'}, timeout=120, capture_output=True, text=True)
(bundle / 'checker-self-test.log').write_text(result.stdout + result.stderr, encoding='utf-8')
(bundle / 'focused-results.jsonl').write_text(json.dumps({'command': 'python scripts/check_allocation_evals.py --self-test', 'cwd': owner.relative_to(repo).as_posix(), 'exit': result.returncode, 'timestamp': datetime.now(timezone.utc).isoformat(), 'resource_policy': 'sequential static Python, PYTHONDONTWRITEBYTECODE=1, timeout120s', 'log': 'checker-self-test.log', 'proof': 'synthetic only; no actual allocation'}) + '\n', encoding='utf-8')
print(result.stdout + result.stderr)
raise SystemExit(result.returncode)
