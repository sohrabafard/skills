from pathlib import Path
import hashlib
import json
import re
import subprocess

BASE = Path('artifacts/skill-pack-optimization-20261018/lanes')
paths = json.loads((BASE / 'UI-changed-paths.json').read_text())
skills = ['alaa-frontend-developer', 'alaa-frontend-devops', 'alaa-vue-typescript-clean-code',
          'alaa-quasar-app-vite-v3', 'alaa-ui-ux-design-system']

for name in paths:
    p = Path(name)
    s = p.read_text(encoding='utf-8')
    s = re.sub(r'`(/[-a-z0-9]+)`\s+\(`\$[-a-z0-9]+`\)', r'`\1`', s)
    p.write_text(s, encoding='utf-8', newline='\n')

# Preserve raw evidence in ASCII-escaped JSON; literal emoji are not artifact prose.
p = BASE / 'UI-edit.py'
s = p.read_text(encoding='utf-8').replace('\u2705', r'\u2705').replace('\u274c', r'\u274c')
p.write_text(s, encoding='utf-8', newline='\n')
p = BASE / 'UI-diff.txt'
if p.exists() and not p.read_text(encoding='utf-8').startswith('Raw scoped diff'):
    (BASE / 'UI-diff.json').write_text(json.dumps({'diff': p.read_text(encoding='utf-8')}, indent=2)
                                    + '\n', encoding='utf-8', newline='\n')
    p.write_text('Raw scoped diff is preserved as ASCII-escaped JSON in UI-diff.json.\n',
                 encoding='utf-8', newline='\n')

all_owned = sorted(p for name in skills for p in (Path('skills/sohrab') / name).rglob('*') if p.is_file())
inputs = sorted(set(all_owned + [Path('scripts/check_fleet_references.py'),
    Path('skills/sohrab/alaa-repo-docs/scripts/check_markdown_links.py'),
    Path('skills/sohrab/alaa-observability-soc/references/20-instrumentation-gates.md'),
    Path('skills/sohrab/alaa-observability-soc/references/60-sentry-and-profiling.md'),
    Path('skills/sohrab/alaa-services-contract/references/21-alaa-platform-observability-directive.md')]))

def manifest(selected):
    h = hashlib.sha256()
    result = []
    # Platform-independent, case-sensitive ordering of relative POSIX path strings.
    for p in sorted(selected, key=lambda item: item.as_posix()):
        data = p.read_bytes()
        h.update(p.as_posix().encode() + b'\0' + data)
        result.append({'path': p.as_posix(), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
    return {'sha256': h.hexdigest(), 'files': result}

commands = [
    ['python', '-B', 'scripts/check_fleet_references.py'] +
        [arg for name in skills for arg in ['--skill', name]],
    ['python', '-B', 'skills/sohrab/alaa-repo-docs/scripts/check_markdown_links.py', '.', '--files'] + paths,
    ['git', 'diff', '--check', '--'] + paths,
]
snapshot = {'cwd': '.', 'head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
            'resource_policy': 'Bounded non-heavy static checks; normal priority; no parallel heavy work.',
            'observer': 'UI implementer only; independent final acceptance remains parent-owned.',
            'manifest': manifest(inputs), 'commands': commands}
(BASE / 'UI-task-snapshot.json').write_text(json.dumps(snapshot, indent=2) + '\n', encoding='utf-8', newline='\n')

results = []
for i, command in enumerate(commands):
    r = subprocess.run(command, cwd='.', capture_output=True, text=True, encoding='utf-8')
    output = BASE / f'UI-check-{i+1}.txt'
    log = (r.stdout + r.stderr).replace(str(Path.cwd()), '.')
    output.write_text(log or f'(no output; exit {r.returncode})\n', encoding='utf-8', newline='\n')
    results.append({'command': command, 'cwd': '.', 'exit': r.returncode, 'output': output.as_posix()})
    print(f'check {i+1}: exit {r.returncode}; {output.as_posix()}')

encoding = []
for p in [Path(x) for x in paths] + sorted(BASE.glob('UI*')):
    if not p.is_file():
        continue
    b = p.read_bytes()
    b.decode('utf-8')
    if b.startswith(b'\xef\xbb\xbf') or b'\r' in b or not b:
        encoding.append(p.as_posix())
results.append({'check': 'UTF-8 without BOM, LF and nonzero bytes', 'findings': encoding,
                'exit': 1 if encoding else 0})
results.append({'check': 'Frozen input manifest unchanged across commands',
                'exit': 0 if snapshot['manifest'] == manifest(inputs) else 1})

baseline = json.loads((BASE / 'UI-read-provenance.json').read_text())
unexpected = [row['path'] for row in baseline['files'] if row['path'] not in paths
              and hashlib.sha256(Path(row['path']).read_bytes()).hexdigest() != row['sha256']]
results.append({'check': 'Untouched owned baseline preserved', 'findings': unexpected,
                'exit': 1 if unexpected else 0})
(BASE / 'UI-verification.json').write_text(json.dumps({'cwd': '.', 'results': results,
    'changed_manifest': manifest(sorted(Path(x) for x in paths))}, indent=2) + '\n',
    encoding='utf-8', newline='\n')
print('all static checks clean:', all(r['exit'] == 0 for r in results))
