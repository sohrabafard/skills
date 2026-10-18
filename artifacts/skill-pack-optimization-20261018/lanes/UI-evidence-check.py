"""Read-only canonical manifest and artifact encoding assertions."""
from pathlib import Path
import hashlib
import json

BASE = Path('artifacts/skill-pack-optimization-20261018/lanes')
def load(name):
    return json.loads((BASE / name).read_text(encoding='utf-8'))

checks = []
for name, key in [('UI-task-snapshot.json', 'manifest'),
                  ('UI-verification.json', 'changed_manifest')]:
    manifest = load(name)[key]
    rows = manifest['files']
    assert [r['path'] for r in rows] == sorted(r['path'] for r in rows)
    digest = hashlib.sha256()
    for row in rows:
        data = Path(row['path']).read_bytes()
        assert len(data) == row['bytes']
        assert hashlib.sha256(data).hexdigest() == row['sha256']
        digest.update(row['path'].encode('utf-8') + b'\0' + data)
    assert digest.hexdigest() == manifest['sha256']
    checks.append({'file': name, 'entries': len(rows), 'sha256': digest.hexdigest(), 'exit': 0})
assert load('UI-diff.json')['changed_manifest'] == load('UI-verification.json')['changed_manifest']['sha256']
encoded = []
for path in sorted(BASE.glob('UI*')):
    if path.is_file():
        data = path.read_bytes()
        data.decode('utf-8')
        assert data and not data.startswith(b'\xef\xbb\xbf') and b'\r' not in data, path
        encoded.append(path.as_posix())
report = {'cwd': '.', 'command': ['python', '-B', (BASE / 'UI-evidence-check.py').as_posix()],
          'resource_policy': 'Bounded normal-priority evidence-only assertions.',
          'manifest_checks': checks, 'diff_pointer_matches': True,
          'utf8_no_bom_lf_nonempty_files': encoded, 'exit': 0}
(BASE / 'UI-evidence-check.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8', newline='\n')
print(json.dumps({'manifest_checks': checks, 'diff_pointer_matches': True,
                  'encoding_files': len(encoded), 'exit': 0}, indent=2))
