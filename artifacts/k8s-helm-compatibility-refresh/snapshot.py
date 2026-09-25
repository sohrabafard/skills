"""Capture deterministic, repository-relative SHA-256 evidence without Git writes."""
import hashlib
import difflib
import json
from pathlib import Path
import subprocess
import sys

root = Path.cwd()
out = root / 'artifacts/k8s-helm-compatibility-refresh'
label = sys.argv[1]
if not label.replace('-', '').isalnum():
    raise SystemExit('Invalid snapshot label')
paths = sorted(
    set(p for p in (root / 'skills/sohrab/alaa-k8s-helm').rglob('*') if p.is_file())
    | set(root / 'scripts' / n for n in (
        'validate_sohrab_skill_pack.py', 'check_skill_index.py',
        'check_fleet_references.py', 'check_lifecycle_contract.py')),
    key=lambda p: p.relative_to(root).as_posix(),
)
manifest = ''.join(hashlib.sha256(p.read_bytes()).hexdigest() + '  '
                   + p.relative_to(root).as_posix() + '\n' for p in paths)
digest = hashlib.sha256(manifest.encode()).hexdigest()
(out / (label + '-manifest.sha256')).write_text(manifest, encoding='utf-8', newline='\n')
diff = subprocess.run(['git', 'diff', '--', 'skills/sohrab/alaa-k8s-helm'],
                      check=True, capture_output=True).stdout
untracked = subprocess.check_output(
    ['git', 'ls-files', '--others', '--exclude-standard', '--', 'skills/sohrab/alaa-k8s-helm'],
    text=True).splitlines()
for name in sorted(untracked):
    content = (root / name).read_text(encoding='utf-8').splitlines(keepends=True)
    diff += ''.join(difflib.unified_diff([], content, fromfile='/dev/null',
                                       tofile='b/' + name)).encode('utf-8')
(out / (label + '.diff')).write_bytes(diff)
print(json.dumps({'snapshot': label, 'files': len(paths), 'sha256': digest,
                  'head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()}))
