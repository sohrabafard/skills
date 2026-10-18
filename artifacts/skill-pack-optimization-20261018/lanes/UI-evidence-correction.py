"""Correct manifest ordering only; do not execute product validation or edit inputs."""
from pathlib import Path
import hashlib
import json

BASE = Path('artifacts/skill-pack-optimization-20261018/lanes')
ALGORITHM = ('SHA-256 of concatenated records in ascending case-sensitive relative POSIX '
             'path string order; each record is UTF-8 path + one NUL byte + raw file bytes; '
             'no separator after file bytes.')

def read(name):
    return json.loads((BASE / name).read_text(encoding='utf-8'))

def write(name, value):
    (BASE / name).write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8', newline='\n')

def correct(manifest):
    digest = hashlib.sha256()
    for row in manifest['files']:
        data = Path(row['path']).read_bytes()
        assert len(data) == row['bytes'], row['path']
        assert hashlib.sha256(data).hexdigest() == row['sha256'], row['path']
        digest.update(row['path'].encode('utf-8') + b'\0' + data)
    assert digest.hexdigest() == manifest['sha256'], 'Former stored-order digest mismatch'
    previous = manifest['sha256']
    manifest['files'].sort(key=lambda row: row['path'])
    digest = hashlib.sha256()
    for row in manifest['files']:
        digest.update(row['path'].encode('utf-8') + b'\0' + Path(row['path']).read_bytes())
    manifest['sha256'] = digest.hexdigest()
    manifest['algorithm'] = ALGORITHM
    return {'previous_sha256': previous, 'corrected_sha256': digest.hexdigest(),
            'files': len(manifest['files'])}

snapshot = read('UI-task-snapshot.json')
verification = read('UI-verification.json')
task = correct(snapshot['manifest'])
changed = correct(verification['changed_manifest'])
provenance = read('UI-read-provenance.json')
owned = {row['path'] for row in provenance['files']}
covered = {row['path'] for row in snapshot['manifest']['files']}
assert owned <= covered
extra = sorted(covered - owned)
assert len(owned) == 131 and len(extra) == 5 and task['files'] == 136
write('UI-task-snapshot.json', snapshot)
write('UI-verification.json', verification)
diff = read('UI-diff.json')
assert diff['changed_manifest'] == changed['previous_sha256']
diff['changed_manifest'] = changed['corrected_sha256']
write('UI-diff.json', diff)
report = {'cwd': '.', 'resource_policy': 'Bounded normal-priority evidence-only assertions.',
          'command': ['python', '-B', (BASE / 'UI-evidence-correction.py').as_posix()],
          'former_algorithm': 'Same record bytes, in Windows pathlib.Path sorted order (case-insensitive), as stored in each former files array.',
          'algorithm': ALGORITHM, 'task_manifest': task, 'changed_manifest': changed,
          'read_provenance_files': len(owned), 'additional_validation_and_shared_inputs': extra,
          'checks': {'all_current_file_sizes_and_sha256_match': True,
                     'former_digests_reproduced_in_stored_order': True,
                     'product_and_checker_inputs_modified': False,
                     'fleet_links_and_product_checks_rerun': False}, 'exit': 0}
write('UI-evidence-correction.json', report)
print(json.dumps(report, indent=2))
