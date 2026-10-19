from pathlib import Path
import json

BASE = Path('skills/sohrab')
EVIDENCE = Path('artifacts/skill-pack-optimization-20261018/lanes')
draft = {
    'intent': 'Resolve I1 without changing review triggers, authorities or model selection.',
    'design': 'The parent completes the required design record before implementation. The critic independently judges that record and the implemented candidate only at the inherited phase or final boundary. Preserve the complete boundary candidate, including earlier pending phases for final. A nested invocation cannot reset the boundary or candidate scope. Return missing, inconsistent or premature review dispatch to the parent. Planning and research remain available before implementation.',
    'contract': 'Keep trigger registration, consumer impact, compatibility and deprecation decisions in Stage A. Dispatch independent contract judgment only at the inherited declared phase or final review boundary. Carry the complete boundary candidate and parent cadence into the review template. Existing stricter repository gate conflicts still return to the canonical plan owner.',
    'compression': 'Replace repetitive timing explanations with the canonical gate pointer and one shared template boundary clause. Preserve the pre-implementation record, scope, missing/premature-dispatch stop, independent verdict and all existing specialist duties.',
    'alternatives_rejected': ['Keep early independent review: contradicts the canonical inherited cadence.', 'Drop the critic or contract gate: weakens independent acceptance.', 'Reset each nested scope to a local final candidate: excludes pending engagement phases.'],
    'limits': 'Source contract and structural regressions only; no live model compliance or installed activation claim.',
}
(EVIDENCE / 'ORCH-FINAL-draft.json').write_text(json.dumps(draft, indent=2) + '\n', encoding='utf-8', newline='\n')

boundary = '<review_boundary>Consume the inherited <cadence> through references/verification-and-gates.md. Judge only at its declared phase|final boundary: the complete phase candidate for phase, or whole-engagement candidate including pending earlier phases for final. Nested invocations never reset that scope. Return missing, conflicting or premature cadence to the parent without judgment.</review_boundary>'
for name, suffix in [('alaa-codex-orchestrator', '.toml'), ('alaa-cc-orchestrator', '.md')]:
    root = BASE / name
    path = root / 'references/delegation-prompts/20-design.md'
    text = path.read_text(encoding='utf-8')
    text = text.replace('<task>Pressure-test this proposed architecture before implementation: <plan>.</task>', '<task>Pressure-test this architecture and its implemented candidate: <plan and candidate>.</task>\n' + boundary)
    text = text.replace('<design_record><path to the design record under review, or a statement that no design pass was run and which of the six conditions fired></design_record>', '<design_record><pre-implementation design record; if absent, state which design-pass condition fired and report the missing record></design_record>')
    path.write_text(text, encoding='utf-8', newline='\n')
    path = root / 'references/delegation-prompts/60-contract-review.md'
    text = path.read_text(encoding='utf-8')
    text = text.replace('Dispatch in Stage A before code exists; dispatch in Stage D instead only when the contract change emerged during implementation.', 'Record known triggers and decide consumer impact, compatibility and deprecation in Stage A; a newly discovered trigger reopens the affected plan and gate.')
    text = text.replace('</trigger>\n<surfaces>', '</trigger>\n' + boundary + '\n<surfaces>', 1)
    path.write_text(text, encoding='utf-8', newline='\n')
    path = root / ('agents/alaa-architecture-critic' + suffix)
    text = path.read_text(encoding='utf-8')
    text = text.replace('Spawn before implementation for public-contract, service-boundary, distributed workflow, consistency, caching, concurrency, or cross-cutting design changes.', 'Judge public-contract, service-boundary, distributed workflow, consistency, caching, concurrency, or cross-cutting design changes at the inherited declared review boundary.')
    old = 'Pressure-test a proposed plan against repository reality before expensive implementation begins.'
    new = ('Pressure-test the pre-implementation design record and implemented candidate against repository reality. '
           f'Consume the inherited parent cadence through /{name} references/verification-and-gates.md: '
           'judge only at its declared phase|final boundary, covering the complete phase candidate for phase or whole-engagement candidate including pending earlier phases for final. '
           'Nested invocations never reset that scope. Return missing, conflicting or premature cadence to the parent without judgment. '
           'The design record remains due before implementation.')
    assert old in text
    text = text.replace(old, new).replace('6. Questions that must be answered before implementation.', '6. Unresolved questions and conditions that block acceptance.')
    path.write_text(text, encoding='utf-8', newline='\n')
print('I1 compressed source repair written in both runtimes')
