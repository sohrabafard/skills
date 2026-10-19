"""Run the parent's exact scoped GO gates and retain covered-input evidence."""
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
LANE = Path(__file__).parent
source = json.loads((LANE / 'GO-source-manifest.json').read_text(encoding='utf-8'))
skills = ['alaa-golang', 'alaa-golang-clean-code-principles', 'alaa-go-chi-development',
          'alaa-golang-fiber', 'alaa-data-layer', 'service-runtime-kit-governance']
changed = [r['path'] for r in source['files']
           if hashlib.sha256((ROOT / r['path']).read_bytes()).hexdigest() != r['sha256']]
md = [p for p in changed if p.endswith('.md')]
owner_paths = [
    'skills/sohrab/alaa-observability-soc/references/20-instrumentation-gates.md',
    'skills/sohrab/alaa-services-contract/references/20-operational-and-observability-contract.md',
    'skills/sohrab/alaa-reliability-sla/references/40-admission-and-shedding.md',
    'skills/sohrab/alaa-laravel-architecture/references/20-composition-and-boot.md',
    'skills/sohrab/alaa-repo-docs/scripts/check_markdown_links.py',
    'scripts/check_fleet_references.py',
    'artifacts/skill-pack-optimization-20261018/lanes/GO-checks.py',
    'artifacts/skill-pack-optimization-20261018/lanes/GO-verify.py',
    'artifacts/skill-pack-optimization-20261018/lanes/GO-source-manifest.json',
]
paths = sorted(set([r['path'] for r in source['files']] + owner_paths))
digest = hashlib.sha256()
records = []
for name in paths:
    data = (ROOT / name).read_bytes()
    digest.update(name.encode() + b'\0' + data)
    records.append({'path': name, 'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)})
snapshot = {
    'head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
    'cwd': '.', 'required_observer': 'GO implementation lane; not independent acceptance',
    'resource_policy': 'ordinary bounded non-heavy Python/static/Git commands; no broad suites',
    'manifest_sha256': digest.hexdigest(), 'files': records,
    'resolution_path_inventory': sorted(p.relative_to(ROOT).as_posix()
                                        for p in (ROOT / 'skills/sohrab').rglob('*') if p.is_file()),
    'changed_files': changed,
}
(LANE / 'GO-task-snapshot.json').write_text(json.dumps(snapshot, indent=2) + '\n', encoding='utf-8', newline='\n')
fleet = ['python', '-B', 'scripts/check_fleet_references.py']
for skill in skills:
    fleet += ['--skill', skill]
commands = [
    ('contracts', ['python', '-B', 'artifacts/skill-pack-optimization-20261018/lanes/GO-checks.py']),
    ('fleet', fleet),
    ('links', ['python', '-B', 'skills/sohrab/alaa-repo-docs/scripts/check_markdown_links.py', '.', '--files'] + md),
    ('diff', ['git', 'diff', '--check', '--'] + changed),
]
checks = []
for label, command in commands:
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
    artifact = LANE / ('GO-' + label + '-output.txt')
    log = (result.stdout + result.stderr).replace(str(ROOT), '<repo>').replace(ROOT.as_posix(), '<repo>')
    artifact.write_text(log, encoding='utf-8', newline='\n')
    checks.append({'name': label, 'command': command, 'cwd': '.',
                   'resource_policy': snapshot['resource_policy'], 'exit_code': result.returncode,
                   'manifest_sha256': snapshot['manifest_sha256'],
                   'output': artifact.relative_to(ROOT).as_posix()})
    print(label + ': exit ' + str(result.returncode) + '; ' + result.stdout.strip().split('\n')[-1])
    if result.returncode:
        break
(LANE / 'GO-verification.json').write_text(json.dumps(checks, indent=2) + '\n', encoding='utf-8', newline='\n')
raise SystemExit(0 if len(checks) == len(commands) and all(c['exit_code'] == 0 for c in checks) else 1)
