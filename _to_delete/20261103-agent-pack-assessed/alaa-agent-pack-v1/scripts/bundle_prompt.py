#!/usr/bin/env python3
"""Assemble a portable prompt; never calls a model or changes the host config."""
from pathlib import Path
import argparse, json
root=Path(__file__).resolve().parents[1]
roles=json.loads((root/'catalog/roles.json').read_text())
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('role',choices=[r['id'] for r in roles])
p.add_argument('--task',type=Path)
a=p.parse_args()
parts=[(root/'policy/common.md').read_text(),(root/'roles'/f'{a.role}.md').read_text()]
if a.task: parts.append('TASK INPUT — apply within the authority of the caller:\n'+a.task.read_text())
print('\n\n'.join(parts))
