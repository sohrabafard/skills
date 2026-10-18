from pathlib import Path
import difflib
import hashlib
import json
import re
import tomllib

base = Path(__file__).parent
old = json.loads((base / 'ORCH-FINAL-read-baseline.json').read_text(encoding='utf-8'))['files']
changed = []
diffs = []
for item in old:
    path = Path(item['path'])
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if digest != item['sha256']:
        assert not data.startswith(b'\xef\xbb\xbf') and b'\r' not in data, path
        changed.append({'path': item['path'], 'before_sha256': item['sha256'], 'after_sha256': digest,
                        'bytes_before': item['bytes'], 'bytes_after': len(data),
                        'baseline_crlf': item['text'].count('\r\n')})
        diffs.append(''.join(difflib.unified_diff(item['text'].replace('\r\n', '\n').splitlines(True),
                     data.decode('utf-8').splitlines(True), fromfile='before/' + item['path'],
                     tofile='after/' + item['path'])))
assert len(changed) == 10, changed
controls = {}
for name, suffix in [('alaa-codex-orchestrator', '.toml'), ('alaa-cc-orchestrator', '.md')]:
    path = Path('skills/sohrab') / name / ('agents/alaa-architecture-critic' + suffix)
    previous = next(item['text'] for item in old if item['path'] == path.as_posix()).replace('\r\n', '\n')
    now = path.read_text(encoding='utf-8')
    if suffix == '.toml':
        before, after = tomllib.loads(previous), tomllib.loads(now)
        keys = {key for key in set(before) | set(after) if before.get(key) != after.get(key)}
        assert keys == {'description', 'developer_instructions'}, keys
        assert all(key not in after for key in ('model', 'model_reasoning_effort'))
        controls[name] = {'changed_keys': sorted(keys), 'sandbox_unchanged': True, 'neutral': True}
    else:
        before, after = previous.split('\n---\n', 1)[0], now.split('\n---\n', 1)[0]
        assert [line for line in before.splitlines() if not line.startswith('description:')] == [line for line in after.splitlines() if not line.startswith('description:')]
        controls[name] = {'metadata_except_description_unchanged': True}
    # The existing aggregate's runtime-isolation rule applies to this changed checker.
    checker = path.parent.parent / 'scripts/check_agent_contracts.py'
    forbidden = r'\b(claude|opus|sonnet|fable|haiku|anthropic)\b' if suffix == '.toml' else r'\b(codex|gpt-?[56]|openai|sol|terra|luna|astra)\b|opus 4'
    assert not re.search(forbidden, checker.read_text(encoding='utf-8'), re.I), checker
digest = hashlib.sha256()
for item in sorted(changed, key=lambda value: value['path']):
    digest.update(item['path'].encode('utf-8') + b'\0' + Path(item['path']).read_bytes())
snapshot = {'changed': changed, 'changed_candidate_sha256': digest.hexdigest(), 'controls_grants': controls,
            'read_provenance': '133 owned files fully decoded/read (834177 baseline bytes); Python scripts parsed as code; relevant gate/template/checker/projection text directly inspected; identical runtime sources reused after byte comparison.',
            'evidence_probe_repair': 'Initial CC metadata assertion failed because baseline was CRLF and frontmatter split was LF-only. One evidence-probe repair normalized baseline newlines; source unchanged; repaired retry passed.',
            'limits': ['No broad checker/self-test/validate_pack aggregate run by this lane.', 'No live instruction compliance, installation/activation or serving-identity proof.', 'Independent acceptance remains with the parent final review stage.']}
(base / 'ORCH-FINAL-final-snapshot.json').write_text(json.dumps(snapshot, indent=2) + '\n', encoding='utf-8', newline='\n')
(base / 'ORCH-FINAL-diff.txt').write_text(''.join(diffs), encoding='utf-8', newline='\n')
checks = [
    {'command': 'python -B artifacts/skill-pack-optimization-20261018/lanes/ORCH-FINAL-focused.py', 'cwd': 'repository root', 'exit': 0, 'observed': 'Each runtime: 34/34 fixtures, 3/3 caller-seam diagnostics, 5 baseline-red early-review diagnostics; rerun after runtime suffix correction.'},
    {'command': 'python -B scripts/render_agents.py --write', 'cwd': 'each owned orchestrator root', 'exit': 0, 'observed': '34 Codex / 30 Claude outputs; only each manifest changed beyond hand-maintained critic sources.'},
    {'command': 'python -B scripts/render_agents.py --check', 'cwd': 'each owned orchestrator root', 'exit': 0, 'observed': '34 Codex / 30 Claude generated files agree; reused after checker-only suffix correction, which is outside renderer inputs.'},
    {'command': 'python -B scripts/check_fleet_references.py --skill alaa-codex-orchestrator --skill alaa-cc-orchestrator', 'cwd': 'repository root', 'exit': 0, 'observed': '2 skills, 74 Markdown files, 288 citations; no findings, 2 pre-existing informational unmarked paths.'},
    {'command': 'git diff --check -- skills/sohrab/alaa-codex-orchestrator skills/sohrab/alaa-cc-orchestrator', 'cwd': 'repository root', 'exit': 0, 'observed': 'No whitespace errors; final invocation retained in parent tool evidence.'},
]
(base / 'ORCH-FINAL-checks.json').write_text(json.dumps({'resource_policy': 'Lightweight static/in-memory checks; normal priority, single Python process per check, bounded output; no CPU-heavy suite.', 'checks': checks}, indent=2) + '\n', encoding='utf-8', newline='\n')
print('I1 final snapshot:', len(changed), 'files;', digest.hexdigest())
