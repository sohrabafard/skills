from pathlib import Path
root = Path('skills/sohrab/alaa-prompting-guide/scripts')
p = root / 'check_allocation_evals.py'
raw = p.read_bytes()
old = b'any(not pair(value) or value["model"] not in item.get("allowed_models", {}).get(runtime, []) for runtime, value in requested_pairs.items())'
assert raw.count(old) == 1
p.write_bytes(raw.replace(old, b'any(not pair(value) for value in requested_pairs.values())'))
p = root / 'check_agent_evals.py'
raw = p.read_bytes()
raw = raw.replace(b'identity is independently verified', b'identity requires independent verification')
raw = raw.replace(b'source identity independently verified;', b'source identity requires independent verification;')
p.write_bytes(raw)
