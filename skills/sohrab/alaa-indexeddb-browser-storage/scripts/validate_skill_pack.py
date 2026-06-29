#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    'SKILL.md',
    'README.md',
    'agents/openai.yaml',
    'references/00-topic-map.md',
    'references/99-sources-and-maintenance.md',
]

FORBIDDEN_EXAMPLE_PATTERNS = [
    re.compile(r'refreshToken\s*[:=]', re.I),
    re.compile(r'accessToken\s*[:=]', re.I),
    re.compile(r'localStorage\.setItem\([^)]*token', re.I),
]


def fail(message: str) -> None:
    print(f'FAIL: {message}', file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    for rel in REQUIRED:
        path = ROOT / rel
        if not path.exists():
            fail(f'missing required file: {rel}')
        if path.stat().st_size == 0:
            fail(f'empty required file: {rel}')

    skill = (ROOT / 'SKILL.md').read_text(encoding='utf-8')
    if not skill.startswith('---\n'):
        fail('SKILL.md must start with YAML frontmatter')
    if 'name: alaa-indexeddb-browser-storage' not in skill:
        fail('SKILL.md has wrong skill name')
    if 'description:' not in skill:
        fail('SKILL.md missing description')

    for path in ROOT.rglob('*'):
      if path.is_file() and path.suffix in {'.md', '.ts', '.yaml', '.json'}:
        text = path.read_text(encoding='utf-8')
        if not text.strip():
            fail(f'empty file: {path.relative_to(ROOT)}')

    examples_text = '\n'.join(p.read_text(encoding='utf-8') for p in (ROOT / 'examples').glob('*.ts'))
    for pattern in FORBIDDEN_EXAMPLE_PATTERNS:
        if pattern.search(examples_text):
            fail(f'forbidden token-storage pattern in examples: {pattern.pattern}')

    print('OK: skill pack structure validated')


if __name__ == '__main__':
    main()
