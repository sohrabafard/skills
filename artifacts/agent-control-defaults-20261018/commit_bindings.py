"""Commit one verified binding candidate, preserving unrelated index/worktree state."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess

SUBJECT = 'fix(beads): standardize per-agent ownership binding'


def run(root, *args):
    result = subprocess.run(['git', '-C', str(root), *args], capture_output=True)
    if result.returncode:
        raise RuntimeError(f'git {args}: exit {result.returncode}\n' +
                           (result.stdout + result.stderr).decode('utf-8', errors='replace'))
    return result.stdout


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--project-root', type=Path, required=True)
    p.add_argument('--manifest', type=Path, required=True)
    p.add_argument('--repo', required=True)
    args = p.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding='utf-8'))
    assert not manifest.get('findings'), 'unresolved verification findings'
    candidate = next(r for r in manifest['repositories'] if r['name'] == args.repo)
    assert Path(args.repo).name == args.repo and args.repo not in {'.', '..'}, 'invalid repository component'
    root = (args.project_root / args.repo).resolve()
    assert root.parent == args.project_root.resolve(), 'checkout escapes authorized parent'
    paths = [f['path'] for f in candidate['files']]
    assert paths and set(paths) <= {'AGENTS.md', 'CLAUDE.md'}, 'invalid commit scope'
    before = run(root, 'rev-parse', 'HEAD').decode().strip()
    assert before == candidate['base_head'], 'HEAD moved after audit'
    assert run(root, 'branch', '--show-current').decode().strip() == candidate['branch'], 'branch changed'
    assert not run(root, 'diff', '--cached', '--name-only', '--', *paths), 'staged binding overlap'
    for file in candidate['files']:
        assert digest((root / file['path']).read_bytes()) == file['sha256'], 'candidate bytes changed'
    exclusions = [f':(exclude){path}' for path in paths]
    staged_before = run(root, 'diff', '--cached', '--binary', '--', '.', *exclusions)
    dirty = run(root, 'diff', 'HEAD', '--name-only', '-z', '--', '.', *exclusions)
    untouched = {}
    for raw in filter(None, dirty.split(b'\0')):
        rel = raw.decode('utf-8')
        file = root / rel
        untouched[rel] = digest(os.fsencode(os.readlink(file)) if file.is_symlink() else file.read_bytes())
    result = subprocess.run(['git', '-C', str(root), 'commit', '--only', '-m', SUBJECT, '--', *paths], capture_output=True)
    log = (result.stdout + result.stderr).decode('utf-8', errors='replace')
    receipt = {'repository': args.repo, 'branch': candidate['branch'], 'base_head': before,
               'paths': paths, 'subject': SUBJECT, 'commit_exit': result.returncode,
               'timestamp_utc': datetime.now(timezone.utc).isoformat(), 'output': log,
               'verified': False}
    receipt_path = Path(__file__).resolve().parent / f'commit-{args.repo}.json'
    receipt_path.write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8', newline='\n')
    if result.returncode:
        print(log)
        return result.returncode
    after = run(root, 'rev-parse', 'HEAD').decode().strip()
    assert run(root, 'rev-parse', 'HEAD^').decode().strip() == before, 'unexpected parent'
    assert run(root, 'branch', '--show-current').decode().strip() == candidate['branch'], 'post-commit branch drift'
    committed = run(root, 'diff-tree', '--no-commit-id', '--name-only', '-r', 'HEAD').decode().splitlines()
    assert set(committed) == set(paths), f'commit scope drift: {committed}'
    assert run(root, 'log', '-1', '--format=%B').decode().strip() == SUBJECT, 'unexpected message/trailer'
    assert run(root, 'diff', '--cached', '--binary', '--', '.', *exclusions) == staged_before, 'unrelated staged diff changed'
    for rel, old_sha in untouched.items():
        file = root / rel
        assert digest(os.fsencode(os.readlink(file)) if file.is_symlink() else file.read_bytes()) == old_sha, f'unrelated worktree change: {rel}'
    for file in candidate['files']:
        path = file['path']
        assert digest((root / path).read_bytes()) == file['sha256'], 'hook changed candidate bytes'
        assert run(root, 'hash-object', f'--path={path}', path).strip() == run(root, 'rev-parse', f'HEAD:{path}').strip(), 'commit blob mismatch'
    receipt.update({'commit': after, 'verified': True, 'unrelated_staged_sha256': digest(staged_before),
                    'unrelated_tracked_preserved': len(untouched),
                    'post_status': run(root, 'status', '--porcelain=v1', '--untracked-files=normal').decode()})
    receipt_path.write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(f'{args.repo}: {after} ({candidate["branch"]}); verified {len(paths)} binding file(s)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
