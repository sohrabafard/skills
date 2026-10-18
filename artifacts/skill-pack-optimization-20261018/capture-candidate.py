"""Capture this engagement's candidate and preserve the original user index."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path.cwd()
BASE = Path('artifacts/skill-pack-optimization-20261018')
INTAKE = json.loads((BASE / 'intake-snapshot.json').read_text(encoding='utf-8'))
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output', choices=('phase3-candidate.json', 'final-candidate.json'), default='phase3-candidate.json')
args = parser.parse_args()


def git(*args):
    return subprocess.check_output(['git', *args])


def sha(data):
    return hashlib.sha256(data).hexdigest()


reports = {row['path'] for row in INTAKE['reports']}
preserved = [row for row in INTAKE['preexisting_changes'] if row['path'] not in reports]
for row in preserved:
    assert sha(Path(row['path']).read_bytes()) == row['sha256'], row['path']
index = git('diff', '--cached', '--raw', '--abbrev=9', '--', *[row['path'] for row in preserved]).decode()
assert index == INTAKE['index_tree'], 'Original unrelated index changed'
assert all(Path(p).read_bytes() == b'' for p in reports), 'Reports not exhausted'
changed = set(git('diff', 'HEAD', '--name-only', '-z').decode().split('\0')) - {''}
untracked = set(git('ls-files', '--others', '--exclude-standard', '-z').decode().split('\0')) - {''}
original = {row['path'] for row in preserved}
owned = sorted((changed | untracked) - original)
allowed = ('skills/sohrab/', BASE.as_posix() + '/')
specific = reports | {
    'AGENTS.md',  # CTRL ownership and exact bytes are recorded in phase1-snapshot.json.
    'docs/_agent_plans/20261018-000000_skill-pack-optimization.md',
    'docs/agents/20261018-000000_skill-pack-optimization-state.md',
}
unexpected = [p for p in owned if not p.startswith(allowed) and p not in specific]
assert not unexpected, unexpected
assert not git('diff', 'HEAD', '--name-only', '--diff-filter=D', '--', 'skills/sohrab').strip(), 'Deleted skill file'
assert sha(Path('skills/sohrab/alaa-bash-shell/references/00-topic-map.md').read_bytes()) == 'a83df1a9104bd2af70d56a7cee8a20746c4baa68286a3605100a25a3ab7d2867'
for path in owned:
    raw = Path(path).read_bytes()
    raw.decode('utf-8')
    assert not raw.startswith(b'\xef\xbb\xbf'), path
    assert b'\r' not in raw, path

product = set(git('ls-files', '-z', '--', 'skills/sohrab', 'scripts', 'AGENTS.md').decode().split('\0')) - {''}
product |= {p for p in untracked if p.startswith('skills/sohrab/')}
manifest = []
aggregate = hashlib.sha256()
for path in sorted(product):
    raw = Path(path).read_bytes()
    aggregate.update(path.encode() + b'\0' + raw)
    manifest.append({'path': path, 'bytes': len(raw), 'sha256': sha(raw)})
footprint = []
for path in sorted(p for p in changed if p.startswith('skills/sohrab/') and p.endswith('/SKILL.md')):
    old = git('show', 'HEAD:' + path).replace(b'\r\n', b'\n')
    new = Path(path).read_bytes()
    footprint.append({'path': path, 'before_bytes': len(old), 'after_bytes': len(new), 'delta_bytes': len(new) - len(old)})
result = {
    'head': git('rev-parse', 'HEAD').decode().strip(),
    'branch': git('branch', '--show-current').decode().strip(),
    'observer': 'parent candidate capture; independent acceptance lives in separate review and verification records',
    'algorithm': 'SHA256 case-sensitive sorted relative POSIX path + NUL + raw bytes',
    'product_manifest_sha256': aggregate.hexdigest(),
    'files': manifest,
    'owned_paths': owned,
    'changed_product_paths': sorted(p for p in owned if p.startswith('skills/sohrab/')),
    'preserved_unrelated_files': len(preserved),
    'original_unrelated_index_unchanged': True,
    'zero_byte_reports': sorted(reports),
    'body_footprint': footprint,
    'footprint_limit': 'Source UTF-8 byte counts only; no measured agent context, cost, speed or runtime compliance.',
}
(BASE / args.output).write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8', newline='\n')
print(json.dumps({'inputs': len(manifest), 'owned_paths': len(owned), 'changed_product_paths': len(result['changed_product_paths']), 'manifest_sha256': aggregate.hexdigest(), 'preserved_unrelated_files': len(preserved)}))
