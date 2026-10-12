from pathlib import Path
import difflib, hashlib, json
from datetime import datetime, timezone
repo = Path.cwd()
base = repo / 'outputs/20261012-orchestrator-routing-plan/checker-lane'
bundle = base / 'probe-v2'
source = repo / 'skills/sohrab/alaa-prompting-guide/scripts/check_allocation_evals.py'
before = (bundle / 'checker-before.py').read_bytes()
after = source.read_bytes()
for entry in json.loads((bundle / 'preservation.json').read_bytes())['preserved_paths']:
    assert hashlib.sha256((repo / entry['path']).read_bytes()).hexdigest() == entry['sha256'], entry['path']
# Check the consumer region is identical, rather than relying on changed-file scope.
assert before[:before.index(b'def probe_input(')].replace(b'\r\n', b'\n') == after[:after.index(b'def response_schema(')].replace(b'\r\n', b'\n')
old_main = before[before.index(b'def main():'):].decode().replace('\r\n', '\n')
new_main = after[after.index(b'def main():'):].decode().replace('\r\n', '\n')
assert old_main == new_main.replace('            probe_schema_self_test(corpus, policies)\n', '')
(bundle / 'source-change.patch').write_text(''.join(difflib.unified_diff(before.decode().splitlines(True), after.decode().splitlines(True), fromfile='checker-before', tofile='check_allocation_evals.py')), encoding='utf-8')
records = []
for path in sorted(bundle.iterdir()):
    if path.is_file(): records.append({'path': path.relative_to(repo).as_posix(), 'bytes': path.stat().st_size, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
manifest = {'observed_on': datetime.now(timezone.utc).isoformat(), 'source_frozen': True, 'source_changes': [{'path': source.relative_to(repo).as_posix(), 'before_sha256': hashlib.sha256(before).hexdigest(), 'after_sha256': hashlib.sha256(after).hexdigest(), 'bytes': len(after)}], 'consumer_regions': 'Byte-identical after newline normalization; only emitter/schema/helper plus self-test call changed', 'preservation': 'Original known input/request/manifest/loaded-source/template hashes unchanged; captures never read or edited by this lane', 'inputs': [{'path': path.relative_to(repo).as_posix(), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()} for path in (repo / 'skills/sohrab/alaa-prompting-guide/assets/evals/allocation-cases.json', repo / 'skills/sohrab/alaa-prompting-guide/assets/evals/allocation-oracle.json')], 'bundle_files': records}
(bundle / 'bundle-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
print(json.dumps(manifest['source_changes'], indent=2))
for runtime in ('codex', 'claude-code'):
    record = json.loads((bundle / f'{runtime}-probe-manifest.json').read_bytes())
    print(runtime, 'input', record['input_sha256'], 'request', record['request_sha256'])
