"""Save one bounded check's evidence; never repair, retry or change source."""
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys

label, *command = sys.argv[1:]
if not label.replace('-', '').isalnum() or not command:
    raise SystemExit('Expected safe label and command argv')
out = Path('artifacts/k8s-helm-compatibility-refresh/verification')
out.mkdir(parents=True, exist_ok=True)
start = datetime.now(timezone.utc).isoformat()
try:
    result = subprocess.run(command, capture_output=True, timeout=120)
    exit_code, stdout, stderr = result.returncode, result.stdout, result.stderr
except subprocess.TimeoutExpired as exc:
    exit_code, stdout, stderr = 124, exc.stdout or b'', exc.stderr or b''
(out / (label + '.stdout')).write_bytes(stdout)
(out / (label + '.stderr')).write_bytes(stderr)
record = {'label': label, 'command': command, 'cwd': '.', 'start': start,
          'end': datetime.now(timezone.utc).isoformat(), 'exit': exit_code,
          'operator': 'lead (supplemental checks; separate verifier evidence required)',
          'tier': 'affected', 'priority': 'BelowNormal', 'parallelism': 1,
          'head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
          'snapshot': 'candidate-manifest.sha256'}
(out / (label + '.json')).write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'label': label, 'exit': exit_code,
                  'output_tail': stdout.decode('utf-8', errors='replace')[-200:],
                  'error_tail': stderr.decode('utf-8', errors='replace')[-600:]}))
raise SystemExit(exit_code)
