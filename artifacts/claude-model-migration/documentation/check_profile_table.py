import json
import re
from pathlib import Path

policy = json.loads(Path('skills/sohrab/alaa-prompting-guide/assets/claude-model-policy.json').read_text(encoding='utf-8'))
lines = Path('docs/claude-model-migration.md').read_text(encoding='utf-8').splitlines()
start = lines.index('| Profile | Before: model / effort | After: model / effort |')
rows = []
for line in lines[start + 2:]:
    if not line.startswith('|'):
        break
    rows.append([cell.strip() for cell in line.strip('|').split('|')])
actual = [re.match(r'`([^`]+)` / ([^ ]+)$', row[2]).groups() for row in rows]
expected = [(profile['model'], profile['effort']) for profile in policy['profiles'].values()]
assert len(rows) == 24, len(rows)
assert actual == expected, (actual, expected)
assert rows[9][0] == 'Reviewer (standard and deep scopes)'
print('PASS: 24 profile rows match canonical model/effort pairs; reviewer row covers standard and deep scopes.')
