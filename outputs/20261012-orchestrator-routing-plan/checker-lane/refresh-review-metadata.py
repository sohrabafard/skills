from pathlib import Path
import hashlib, json
from datetime import datetime, timezone
repo = Path.cwd()
artifact = repo / 'outputs/20261012-orchestrator-routing-plan/checker-lane'
owner = repo / 'skills/sohrab/alaa-prompting-guide'
oracle = json.loads((owner / 'assets/evals/allocation-oracle.json').read_bytes())
oracle_digest = hashlib.sha256(json.dumps(oracle, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()
p = artifact / 'allocation-results-unrun.json'
template = json.loads(p.read_bytes())
old_digest = template['oracle_sha256']
template['oracle_sha256'] = oracle_digest
p.write_text(json.dumps(template, indent=2) + '\n', encoding='utf-8')
p = artifact / 'source-snapshot.json'
snapshot = json.loads(p.read_bytes())
changes = []
for entry in snapshot['files']:
    data = (repo / entry['path']).read_bytes()
    new_hash = hashlib.sha256(data).hexdigest()
    if new_hash != entry['sha256']:
        changes.append({'path': entry['path'], 'before_sha256': entry['sha256'], 'after_sha256': new_hash, 'bytes': len(data)})
    entry.update(bytes=len(data), sha256=new_hash)
expected = {'skills/sohrab/alaa-prompting-guide/' + path for path in ('scripts/check_allocation_evals.py', 'scripts/check_agent_evals.py', 'assets/evals/allocation-oracle.json')}
assert {entry['path'] for entry in changes} == expected, changes
snapshot['observed_on'] = datetime.now(timezone.utc).isoformat()
snapshot['manifest_sha256'] = hashlib.sha256(json.dumps(snapshot['files'], sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()
p.write_text(json.dumps(snapshot, indent=2) + '\n', encoding='utf-8')
repair = {'scope': 'One parent-authorized correctness review fix cycle; no archive or neutral source/input changes', 'source_changes': changes, 'oracle_canonical_sha256': oracle_digest, 'previous_oracle_canonical_sha256': old_digest, 'unrun_template_sha256': hashlib.sha256((artifact / 'allocation-results-unrun.json').read_bytes()).hexdigest(), 'focused_results': [json.loads(line) for line in (artifact / 'focused-results.jsonl').read_text().splitlines()[-4:]], 'source_frozen': True}
(artifact / 'review-fix-evidence.json').write_text(json.dumps(repair, indent=2) + '\n', encoding='utf-8')
print(json.dumps(changes, indent=2))
