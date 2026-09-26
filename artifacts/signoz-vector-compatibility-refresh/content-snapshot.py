"""Print a deterministic content identity; never modify the tested tree."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parents[2]
scopes = [
    'skills/sohrab/alaa-signoz-clickhouse-docs',
    'skills/sohrab/vector-rust-observability-pipelines',
]
rows = []
for scope in scopes:
    for path in (root / scope).rglob('*'):
        if path.is_file():
            rows.append((path.relative_to(root).as_posix(), hashlib.sha256(path.read_bytes()).hexdigest()))
rows.sort()
manifest = ''.join(f'{path}\t{digest}\n' for path, digest in rows)
print(json.dumps({'method': 'SHA-256 of sorted UTF-8 relative-path TAB file-SHA256 LF rows; all files including untracked',
                  'scope': scopes, 'file_count': len(rows),
                  'sha256': hashlib.sha256(manifest.encode('utf-8')).hexdigest(),
                  'files': [{'path': path, 'sha256': digest} for path, digest in rows]}, indent=2))
