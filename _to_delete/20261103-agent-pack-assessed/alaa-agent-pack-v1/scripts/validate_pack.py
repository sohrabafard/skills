#!/usr/bin/env python3
"""Structural validation only; not Codex runtime or model-quality validation."""
from pathlib import Path
import json, tomllib
root=Path(__file__).resolve().parents[1]
roles=json.loads((root/'catalog/roles.json').read_text())
models=json.loads((root/'catalog/models.json').read_text())['models']
allowed={m['id'] for m in models.values()}
assert len(roles)==30 and len({r['id'] for r in roles})==30
for r in roles:
    assert r['model'] in allowed and r['effort'] in {'medium','high'}
    assert r['checks'] and r['inputs'] and r['outputs']
    assert (root/'roles'/f"{r['id']}.md").is_file()
    t=tomllib.loads((root/'codex/agents'/f"alaa-{r['id']}.toml").read_text())
    assert set(t)=={'name','description','model','model_reasoning_effort','developer_instructions'}
    assert t['model']==r['model'] and t['model_reasoning_effort']==r['effort']
    assert t['name']=='alaa_'+r['id'].replace('-','_')
    assert r['mission'] in t['developer_instructions']
    assert 'never fabricate' in t['developer_instructions']
cfg=tomllib.loads((root/'codex/config-snippet.toml').read_text())
assert cfg['agents']['max_concurrent_threads_per_session']==3
cases=json.loads((root/'evals/cases.json').read_text())
assert len(cases)==36 and len({c['case_id'] for c in cases})==36
assert all(c['role'] in {r['id'] for r in roles} for c in cases)
assert all(c['status']=='blueprint_requires_repository_fixture' for c in cases)
for f in root.rglob('*.json'): json.loads(f.read_text())
print(f'PASS: {len(roles)} role definitions, 31 TOML files, {len(cases)} evaluation blueprints and JSON structure.')
print('NOT TESTED: user repository, Codex runtime loading, model performance, live deployment.')
