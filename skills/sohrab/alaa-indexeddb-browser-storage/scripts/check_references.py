#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
TOPIC = ROOT / 'references' / '00-topic-map.md'

links = re.findall(r'`(references/[^`]+\.md)`|`(examples/[^`]+\.ts)`|`(assets/[^`]+)`', TOPIC.read_text(encoding='utf-8'))
missing = []
for groups in links:
    rel = next((g for g in groups if g), None)
    if rel and not (ROOT / rel).exists():
        missing.append(rel)

if missing:
    raise SystemExit('Missing referenced files: ' + ', '.join(missing))
print('OK: topic-map references exist')
