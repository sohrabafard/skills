from pathlib import Path
import json

root = Path.cwd()
out = root / 'outputs/20261010-go-routing-ownership'
draft_root = out / 'authoring-drafts'
finals = {p.relative_to(draft_root): p.read_text(encoding='utf-8') for p in draft_root.rglob('*') if p.is_file()}
changes = []

def compress(path, old, new):
    path = Path(path)
    assert old in finals[path], (path, old)
    finals[path] = finals[path].replace(old, new)
    changes.append({'path': path.as_posix(), 'draft': old, 'final': new,
                    'classification': 'wording only; same trigger, obligation and scope'})

base = 'skills/sohrab/'
g = base + 'alaa-golang/'
r = base + 'alaa-code-intelligence-routing/'
# Restore baseline source preflight explicitly before compression; first drafts remain intact.
preflight = Path(g+'SKILL.md')
finals[preflight] = finals[preflight].replace(
    'Read applicable repository instructions,',
    "Read applicable repository instructions, including `AGENTS.md` and `CLAUDE.md` when present,")
finals[preflight] = finals[preflight].replace(
    'For HTTP changes, inspect route registration.',
    'For source changes, inspect route registration.')
revision = out/'authoring-drafts-revision-1'/preflight
revision.parent.mkdir(parents=True, exist_ok=True)
revision.write_text(finals[preflight], encoding='utf-8', newline='\n')
changes.append({'path': preflight.as_posix(), 'classification': 'baseline preflight restoration before compression',
                'change': 'Name both existing instruction files and retain route-registration read for source changes; dependency-only exception is ratified A4.'})
compress(g+'SKILL.md',
    'Act as the Go engineering front door for the Ala platform. Select the applicable Go mechanics,\nhouse companions and doctrine owners; hold the Go decisions none of them owns. Finish the\nauthorized task with repository evidence, required native proof and the four completion answers.',
    'Own Go decisions no routed skill covers; select Go mechanics, house companions and doctrine\nowners for Ala platform work. Complete the authorized task with repository evidence, required\nnative proof and the four completion answers.')
compress(g+'SKILL.md',
    'Existing repository truth overrides this skill;\n   report discrepancies instead of silently deciding between conflicting statements.',
    'Repository truth overrides this skill; report discrepancies.')
compress(g+'SKILL.md',
    'follow it without restating\n   its rules.', 'follow it without restating its rules.')
compress(g+'SKILL.md',
    'Route model, effort, thinking-budget, runtime-capability and invocation questions\n   through /alaa-prompting-guide and its `references/50-effort-and-thinking.md`; state none here.',
    'Take model, effort, thinking-budget, runtime-capability and invocation answers from\n   /alaa-prompting-guide and its `references/50-effort-and-thinking.md`, never this skill.')
compress(g+'SKILL.md',
    'Loading this skill alone\n   does not write files or authorize effects.',
    'Activation writes nothing and grants no additional authority.')
compress(g+'SKILL.md',
    'Report each actual command and outcome using /alaa-go-chi-development',
    'Report commands and outcomes using /alaa-go-chi-development')
compress(g+'SKILL.md',
    'Before calling Go work done, report all four:', 'Report all four before calling Go work done:')
compress(g+'references/00-topic-map.md',
    'for selection of evidence and any required semantic operation; this row delegates the decision rather than selecting a provider',
    'for evidence and required semantic-operation selection')
compress(g+'references/10-installed-golang-skills.md',
    'it selects the eligible surface and records its limits, so this catalogue names capabilities only.',
    'it selects the surface and its limits. This catalogue names capabilities only.')
compress(g+'references/11-orchestration-and-overlap-guide.md',
    'it alone decides provider selection and degraded operation.',
    'it owns provider selection and degraded operation.')
compress(g+'references/40-production-ready-package-catalog.md',
    'load /alaa-code-intelligence-routing to select its eligible surface; this list prescribes no provider.',
    'load /alaa-code-intelligence-routing for surface selection.')
compress(g+'agents/openai.yaml',
    'use $alaa-code-intelligence-routing and follow its sole provider-selection and degraded-operation contract.',
    'use $alaa-code-intelligence-routing for provider selection and degraded operation.')
compress(r+'references/10-routing-contract.md',
    '''An authorized bounded local edit does not require Serena, gopls or another semantic provider to be
configured. When supported provider evidence is missing, first name the exact behavior and scope
to change. Use adequate fresh source or already returned evidence, inspect applicable contracts,
callers and tests, verify the target worktree, preserve unrelated changes and inspect the resulting
diff. Execute every mandatory native gate under the stack/repository/task's proof policy. A source
read alone is not proof of complete references, binding-safe rename or refactor safety. If a required
property still needs unavailable semantic evidence and cannot be established by authorized equivalent
proof, stop only its dependent action or claim. Do not require installation to continue a bounded edit
whose evidence and required proof are sufficient.''',
    '''Authorized bounded local edits need no configured Serena, gopls or other semantic provider.
When provider evidence is missing, name the behavior and scope; use adequate fresh source or
returned evidence, inspect applicable contracts/callers/tests, verify the target worktree, preserve
unrelated changes and inspect the resulting diff. Run every mandatory native gate under the
stack/repository/task proof policy. Source reads alone prove neither complete references,
binding-safe rename nor refactor safety. Block only the dependent action or claim if its required
semantic property lacks authorized equivalent proof. Sufficient evidence and required proof permit
the bounded edit without installation.''')
compress(r+'references/10-routing-contract.md',
    '''Provider diagnostics are supplemental unless a repository rule or acceptance criterion requires a
specific semantic property beyond native proof. Absence of an optional diagnostic does not block
authorized edits or completion after mandatory native gates pass. Record that gap and its lost
guarantee; do not call native output equivalent without evidence. A specifically required uncovered
property remains blocked, and native gates still execute for unrelated safe work.''',
    '''Provider diagnostics are supplemental unless repository rules or acceptance require a specific
semantic property beyond native proof. Missing optional diagnostics do not block authorized edits
or completion after mandatory native gates pass. Record the gap and lost guarantee; do not claim
native output equivalent without evidence. Required uncovered properties remain blocked; execute
native gates for unrelated safe work.''')
compress(r+'references/40-stack-bindings.md',
    'That contract\nalso owns bounded native editing and supplemental diagnostics.',
    'That contract also owns bounded native edits and supplemental diagnostics.')
compress(r+'references/45-native-tools.md',
    'Do not survey symbols or call\npaths unless a separately named compatibility, API-use or impact fact requires that evidence.',
    'Survey symbols/call paths only for a separately named compatibility, API-use or impact fact.')

for path, text in finals.items():
    (root/path).write_text(text, encoding='utf-8', newline='\n')
(out/'authoring-compression.json').write_text(json.dumps(changes, indent=2)+'\n', encoding='utf-8', newline='\n')
print(f'Wrote {len(finals)} final files; {len(changes)} explicit wording cuts recorded.')
