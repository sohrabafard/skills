from pathlib import Path
p = Path('skills/sohrab/alaa-prompting-guide/scripts/check_allocation_evals.py')
raw = p.read_bytes()
newline = b'\r\n' if b'\r\n' in raw else b'\n'
def replace(old, new):
    global raw
    before = old.replace('\n', newline.decode()).encode()
    assert raw.count(before) == 1, old
    raw = raw.replace(before, new.replace('\n', newline.decode()).encode())
replace('text = {"type": "string", "minLength": 1}', 'text = {"type": "string", "minLength": 1, "pattern": r"\\S"}')
replace('''                 "then": {"properties": {"admission": {"required": ["source", "remaining_reasoning", "rejected_cheaper", "decomposition"]}}}}]}''', '''                 "then": {"properties": {"admission": {"required": ["source", "remaining_reasoning", "rejected_cheaper", "decomposition"]}}}},
                {"if": {"properties": {"proposed_worker": {"type": "object", "properties": {
                    "model": {"enum": ["gpt-6-astra", "claude-fable-5-1"]}}}}}, "then": {"properties": {
                    "admission": {"properties": {"kind": {"enum": ["official-task-priority", "high-workhorse-inadequacy", "explicit-user-selection"]}}}}}}]}''')
replace('admission always needs kind and nonempty evidence. When proposing', 'admission always needs kind and nonempty evidence. Exceptional models cannot use ordinary admission. When proposing')
p.write_bytes(raw)
print('Final same-scope shape audit includes existing exceptional admission prohibition and whitespace-only evidence refusal.')
