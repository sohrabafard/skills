from pathlib import Path
import hashlib
import json
import re
import subprocess

root = Path.cwd()
out = root/'outputs/20261010-go-routing-ownership'
go = root/'skills/sohrab/alaa-golang'
routing = root/'skills/sohrab/alaa-code-intelligence-routing'

# Correct the metadata-resolution boundary in a new full draft, preserving earlier drafts.
p = routing/'references/10-routing-contract.md'
text = p.read_text(encoding='utf-8')
text = text.replace('Applicable native manifest/parser and inspected stack dependency recipe',
                    'Applicable native manifest/parser for declared metadata, or the inspected stack version/dependency recipe for resolved versions and upgrades')
revision = out/'authoring-drafts-revision-2'/p.relative_to(root)
revision.parent.mkdir(parents=True, exist_ok=True)
if not revision.exists():
    revision.write_text(text, encoding='utf-8', newline='\n')
text = text.replace('Applicable native manifest/parser for declared metadata, or the inspected stack version/dependency recipe for resolved versions and upgrades',
                    'Native manifest/parser for declared metadata; inspected stack version/dependency recipe for resolution or upgrade')
p.write_text(text, encoding='utf-8', newline='\n')

checks = []
def check(name, condition):
    assert condition, name
    checks.append(name)

paths = sorted(p for d in (go, routing) for p in d.rglob('*') if p.is_file())
changed = subprocess.run(['git', 'diff', '--name-only', '--', 'skills/sohrab/alaa-golang',
                          'skills/sohrab/alaa-code-intelligence-routing'], capture_output=True,
                         text=True, check=True).stdout.splitlines()
unchanged = []
for path in paths:
    relative = path.relative_to(root).as_posix()
    if relative not in changed:
        unchanged.append(relative)

body = (go/'SKILL.md').read_text(encoding='utf-8')
check('One Go topic-map pointer', body.count('references/00-topic-map.md') == 1)
check('Native build/vet/changed-package/full-test gate retained',
      all(x in body for x in ('go build ./...', 'go vet ./...', 'tests of the changed packages', 'go test ./...')))
check('Race/vulnerability triggers retained',
      all(x in body for x in ('go test -race ./...', 'goroutine, channel, mutex, cache, worker pool', 'package-level variable', 'govulncheck ./...', '`go.mod` or `go.sum` changed')))
check('Kit phase, P1-P13, drift/gap and four completion answers retained',
      all(x in body for x in ('before writing or reviewing a line', 'decision-record filename', 'only a project-owner instruction', 'P1-P13', 'gap test', 'both files as drift', 'What shipped', 'How it is operated', 'How it fails', 'Each validation command')))

provider_mentions = []
for path in go.rglob('*'):
    if path.is_file():
        for number, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
            if re.search(r'CodeGraph|Serena|gopls', line):
                provider_mentions.append({'path': path.relative_to(root).as_posix(), 'line': number, 'text': line})
check('Go provider names limited to catalogue/provenance facts',
      all(x['path'].split('/')[-1] in ('10-installed-golang-skills.md', '40-production-ready-package-catalog.md', 'SOURCES.md') for x in provider_mentions))
for relative in changed:
    path = root/relative
    text = path.read_text(encoding='utf-8')
    if path.suffix == '.md':
        check('Single Markdown invocation form: '+relative, not re.search(r'\$[a-z][a-z0-9-]*', text))
    check('No machine paths or emoji added: '+relative,
          not re.search(r'[A-Z]:\\|[\U0001f300-\U0001faff]', text))

for directory in (go, routing):
    skill = (directory/'SKILL.md').read_text(encoding='utf-8')
    header = skill.split('---')[1]
    check('Common frontmatter only: '+directory.name,
          re.findall(r'^([a-z_-]+):', header, re.M) == ['name', 'description'])
    description = re.search(r'description: "(.*)"', header).group(1)
    packaged = re.sub(r'/([a-z][a-z0-9-]*)', r'/so:\1', description)
    check('Packaged description <=1024 and no angle markup: '+directory.name,
          len(packaged) <= 1024 and not re.search('[<>]', description))
    metadata = (directory/'agents/openai.yaml').read_text(encoding='utf-8')
    check('Codex default prompt keeps dollar invocation: '+directory.name,
          f'${directory.name}' in metadata)

entries = [f'{p.relative_to(root).as_posix()} {hashlib.sha256(p.read_bytes()).hexdigest()}\n' for p in paths]
payload = ''.join(entries)
digest = hashlib.sha256(payload.encode('utf-8')).hexdigest()
(out/'authoring-final-manifest.txt').write_text(payload, encoding='utf-8', newline='\n')
summary = {'files':len(paths), 'sha256':digest, 'changed':changed, 'unchanged':unchanged,
           'content_checks': checks, 'provider_mentions':provider_mentions,
           'per_package':{}}
for directory in (go, routing):
    per_payload = ''.join(f'{p.relative_to(root).as_posix()} {hashlib.sha256(p.read_bytes()).hexdigest()}\n'
                          for p in sorted(directory.rglob('*')) if p.is_file())
    summary['per_package'][directory.name] = {'files':len([p for p in directory.rglob('*') if p.is_file()]),
                                            'sha256':hashlib.sha256(per_payload.encode('utf-8')).hexdigest()}
(out/'authoring-content-receipt.json').write_text(json.dumps(summary, indent=2)+'\n', encoding='utf-8', newline='\n')
print(f'PASS: {len(checks)} content/metadata checks; {len(changed)} changed files; {len(unchanged)} unchanged Git content files.')
print(f'Manifest: {len(paths)} files; SHA256 {digest}')
