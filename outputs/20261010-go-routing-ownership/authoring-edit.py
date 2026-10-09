from pathlib import Path
import re
import hashlib
import json

root = Path.cwd()
out = root / 'outputs/20261010-go-routing-ownership'
go = root / 'skills/sohrab/alaa-golang'
route = root / 'skills/sohrab/alaa-code-intelligence-routing'
before = {p: p.read_text(encoding='utf-8') for d in (go, route) for p in d.rglob('*') if p.is_file()}
drafts = {}

def replace(path, old, new):
    text = drafts.get(path, before[path])
    assert old in text, (path, old)
    drafts[path] = text.replace(old, new)

body = '''# Alaa Golang

Act as the Go engineering front door for the Ala platform. Select the applicable Go mechanics,
house companions and doctrine owners; hold the Go decisions none of them owns. Finish the
authorized task with repository evidence, required native proof and the four completion answers.
If a routed owner disagrees with this skill, follow that owner and report both files as drift.

## When NOT to use

- Kit-conformance-only review of an existing `alaa-go-chi` consumer: load
  /alaa-golang-clean-code-principles directly.
- Kit governance, change requests or active scope phase alone: load /alaa-go-chi-development.
- A task with no Go source or module/toolchain change, such as a Dockerfile, chart, pipeline,
  edge configuration or a document merely mentioning a Go service: use its domain owner.

## Procedure

Read `references/00-topic-map.md` before a Go decision; open only rows matching the next action.

1. Establish repository truth before proposing a change. Read applicable repository instructions,
   `go.mod` (module path and `go` directive), and the imports and existing tests of every package
   to change. For HTTP changes, inspect route registration. For dependency-only work, inspect
   module/workspace metadata and the native dependency recipe; source discovery applies only
   when a source or impact question needs it. Existing repository truth overrides this skill;
   report discrepancies instead of silently deciding between conflicting statements.
2. When `go.mod` requires `git.alaatv.com/vk/alaa-go-chi`, establish the active phase from the kit
   repository through /alaa-go-chi-development before writing or reviewing a line. Read its
   `references/05-phase-and-source-truth.md`. If the phase forbids consumer work, stop and report
   the phase and decision-record filename. A consumer-shaped request, local consumer repository,
   registry row or older record does not reactivate it; only a project-owner instruction naming
   that consumer does. Load /alaa-golang-clean-code-principles before the first edit or review
   comment; P1-P13 bind and this skill adds or overrides no principle.
3. Before choosing evidence, an editing surface or supplemental diagnostics, load
   /alaa-code-intelligence-routing. It alone selects providers, order, eligibility and fallback.
   Follow its rules for native continuation, missing guarantees and mutation reconciliation;
   this skill supplies Go doctrine and native proof, not a provider sequence.
4. Load each triggered domain owner before the governed action and follow it without restating
   its rules. For an uncovered decision, apply the gap test reached through the topic map, then
   report the decision, why no owner covered it and where it was recorded. Never decide a gap
   silently. Route model, effort, thinking-budget, runtime-capability and invocation questions
   through /alaa-prompting-guide and its `references/50-effort-and-thinking.md`; state none here.
5. Change behavior through the test-first sequence selected by the topic map. Inspect the full
   resulting diff and callers, then execute the validation gate below. Loading this skill alone
   does not write files or authorize effects.

## Authority and failure

Read accessible sources and make authorized local edits within the requested scope. Preserve
existing behavior, contracts, user changes and repository conventions unless the task authorizes
a change. Get explicit permission for installation, integration configuration, commits, publication,
deployment, external mutation or destructive effects. A skill or tool being available grants none.
When a required owner, fact, phase authorization or proof is missing, stop the dependent action
and report the exact blocker; unrelated safe work may continue. Use the routing owner's finite
failure budget for evidence and native gates; do not loop or claim an unrun gate passed.

## Validation gate

After any Go edit, run in order: `go build ./...`; `go vet ./...`; tests of the changed packages;
`go test ./...`. Supplemental provider diagnostics and any required uncovered semantic property
are governed by /alaa-code-intelligence-routing; they do not replace these native gates.
Add `go test -race ./...` when the change touches a goroutine, channel, mutex, cache, worker pool
or package-level variable. Run `govulncheck ./...` when `go.mod` or `go.sum` changed.
Report each actual command and outcome using /alaa-go-chi-development
`references/05-phase-and-source-truth.md`: `passed`, `failed`, `blocked`, `skipped`, `not run`.
Never report an outcome for a command you did not execute. Stop successfully only when the
requested behavior, required gates and completion answers are established in the target repository.

## Completion answers

Before calling Go work done, report all four:

1. Each validation command and its observed outcome.
2. What shipped: externally visible routes, request/response fields and types, error codes and
   event-payload changes. Write `no contract change` when there is none.
3. How it is operated: every environment key added, changed or removed, its default and accepted
   range, and each dashboard panel or alert required to make the change visible in production.
4. How it fails: each new failure mode and its exact operator signal, including metric, log event
   or degraded readiness check.

/alaa-services-contract owns contract-entry shape; /alaa-observability-soc owns dashboard/alert
shape. This skill requires the four answers without restating either owner's contract.
'''
drafts[go / 'SKILL.md'] = before[go / 'SKILL.md'].split('# Alaa Golang')[0] + body

replace(go / 'references/00-topic-map.md',
    'only those, and act. When several rows match, open all of them. Trigger forms are given for both runtimes: Claude Code\n`/name`, Codex `$name`.',
    'only those, and act. When several rows match, open all of them. Each call site names its owning skill.')
replace(go / 'references/00-topic-map.md',
    '`/alaa-code-intelligence-routing` (`$alaa-code-intelligence-routing`): Serena for the known Go symbol; direct `/golang-gopls` (`$golang-gopls`) only for one recorded unavailable, unhealthy, or missing-operation fallback',
    '`/alaa-code-intelligence-routing` for selection of evidence and any required semantic operation; this row delegates the decision rather than selecting a provider')

replace(go / 'references/10-installed-golang-skills.md',
    '**Rule:** load a skill by naming it in the trigger form of the runtime you are in — Claude Code `/golang-testing`,\nCodex `$golang-testing`. **Forbidden:** mentioning a vendor directory path in an answer to a user.',
    '**Rule:** load the named skill when its condition applies. **Forbidden:** mentioning a vendor directory path in an answer to a user.')
old = before[go / 'references/10-installed-golang-skills.md'].split('Direct access to Go\'s `gopls`')[1].split('\n\n### golang-refactoring')[0]
replace(go / 'references/10-installed-golang-skills.md', "Direct access to Go's `gopls`" + old,
    "Go's `gopls` language-server mechanics: build-aware definitions, references, package API discovery,\n" 
    'diagnostics, rename and code actions against the locally resolved build, including `replace`d forks.\n'
    'When the task needs a local code-intelligence operation, load /alaa-code-intelligence-routing;\n'
    'it selects the eligible surface and records its limits, so this catalogue names capabilities only.')

replace(go / 'references/11-orchestration-and-overlap-guide.md', 'Trigger forms: Claude Code `/name`, Codex `$name`.\n\n', '')
replace(go / 'references/11-orchestration-and-overlap-guide.md',
    '`/golang-project-layout` (`$golang-project-layout`); CodeGraph maps unknown structure and Serena answers the exact known symbol',
    '`/golang-project-layout` (`$golang-project-layout`) for package-layout decisions')
replace(go / 'references/11-orchestration-and-overlap-guide.md',
    'the semantic diagnostics selected by `/alaa-code-intelligence-routing` (`$alaa-code-intelligence-routing`)',
    '`/alaa-code-intelligence-routing` (`$alaa-code-intelligence-routing`) when a local code-intelligence question needs answering')
replace(go / 'references/11-orchestration-and-overlap-guide.md',
    '- `/alaa-code-intelligence-routing` (`$alaa-code-intelligence-routing`) — this repository: CodeGraph for unknown\n  structure, Serena for known Go symbols and semantic edits, and direct `/golang-gopls` (`$golang-gopls`) only for one\n  recorded unavailable, unhealthy, or missing build-aware operation. Serena\'s Go backend itself uses `gopls`.',
    '- /alaa-code-intelligence-routing — evidence and editing surfaces for this repository;\n  it alone decides provider selection and degraded operation.')
replace(go / 'references/11-orchestration-and-overlap-guide.md',
    '**Rule:** read and reshape through the selected semantic owner, learn ecosystem facts with godig, and gate releases with `govulncheck`.',
    '**Rule:** route local evidence and editing-surface choices through /alaa-code-intelligence-routing,\nlearn ecosystem facts with godig, and gate releases with `govulncheck`.')
replace(go / 'references/11-orchestration-and-overlap-guide.md',
    '**Rule:** load the process skill and the destination skill together, with the semantic actuator selected by\n`/alaa-code-intelligence-routing` (`$alaa-code-intelligence-routing`); Serena is the default Go surface and direct\n`/golang-gopls` (`$golang-gopls`) is one recorded fallback.',
    '**Rule:** load the process skill and the destination skill together; use /alaa-code-intelligence-routing\nfor the editing surface and any missing semantic guarantee before the dependent operation.')

replace(go / 'references/40-production-ready-package-catalog.md',
    "`gopls` — **required backend** for Serena's Go semantic surface and the direct fallback reached through `/golang-gopls` (`$golang-gopls`); it is not the default agent-facing route.",
    '`gopls` — Go language server. For a task requiring a local semantic operation,\nload /alaa-code-intelligence-routing to select its eligible surface; this list prescribes no provider.')
replace(go / 'references/62-import-direction-and-boundaries.md',
    '- `/alaa-code-intelligence-routing` (`$alaa-code-intelligence-routing`) selects the semantic surface: Serena shows\n  the package\'s known symbols and references before a move; invoke `/golang-gopls` (`$golang-gopls`) directly only\n  for one recorded package-API or build-aware guarantee that Serena does not expose.',
    '- Before a move requiring package-API or reference evidence, load /alaa-code-intelligence-routing\n  for the evidence and editing surfaces; retain any coverage limits it establishes.')
replace(go / 'agents/openai.yaml',
    'Route code intelligence through $alaa-code-intelligence-routing: CodeGraph owns unknown structure, Serena owns known Go symbols and semantic edits, and $golang-gopls is a recorded direct fallback rather than a duplicate discovery path.',
    'Before selecting evidence, an editing surface or supplemental diagnostics, use $alaa-code-intelligence-routing and follow its sole provider-selection and degraded-operation contract.')

replace(route / 'references/10-routing-contract.md',
    '| Known-symbol declaration, references, implementations, hierarchy, diagnostics or semantic edit | Stack-declared semantic owner, otherwise supported Serena backend | Equivalent configured native semantic operation; targeted source for partial read evidence only |',
    '| Known-symbol declaration, references, implementations, hierarchy, diagnostics or semantic edit | Stack-declared semantic owner, otherwise supported Serena backend | Equivalent configured native semantic operation; targeted source for partial read evidence; bounded native edit under the continuation rule below |\n'
    '| Dependency metadata, resolved module/workspace versions or an authorized dependency upgrade | Applicable native manifest/parser and inspected stack dependency recipe | Eligible equivalent proving the named metadata property; discover source or semantics only for a separate missing impact/API fact |')
replace(route / 'references/10-routing-contract.md', '## Mutation uncertainty',
    '''## Authorized native continuation

An authorized bounded local edit does not require Serena, gopls or another semantic provider to be
configured. When supported provider evidence is missing, first name the exact behavior and scope
to change. Use adequate fresh source or already returned evidence, inspect applicable contracts,
callers and tests, verify the target worktree, preserve unrelated changes and inspect the resulting
diff. Execute every mandatory native gate under the stack/repository/task's proof policy. A source
read alone is not proof of complete references, binding-safe rename or refactor safety. If a required
property still needs unavailable semantic evidence and cannot be established by authorized equivalent
proof, stop only its dependent action or claim. Do not require installation to continue a bounded edit
whose evidence and required proof are sufficient.

Provider diagnostics are supplemental unless a repository rule or acceptance criterion requires a
specific semantic property beyond native proof. Absence of an optional diagnostic does not block
authorized edits or completion after mandatory native gates pass. Record that gap and its lost
guarantee; do not call native output equivalent without evidence. A specifically required uncovered
property remains blocked, and native gates still execute for unrelated safe work.

## Mutation uncertainty''')
replace(route / 'references/40-stack-bindings.md',
    'Native Go recipes own build/vet/test proof. /alaa-golang owns implementation doctrine; routing does not authorize backend activation.',
    'For dependency metadata or an authorized upgrade, use the native recipes in `references/45-native-tools.md`;\nsource/impact/API questions trigger their own selection under `references/10-routing-contract.md`. That contract\nalso owns bounded native editing and supplemental diagnostics. Native Go recipes own build/vet/test proof.\n/alaa-golang owns implementation doctrine; routing does not authorize backend activation.')
replace(route / 'references/45-native-tools.md',
    "Direct gopls is a semantic fallback only for the stack owner's recorded gap, with build context and the required operation verified. Go tests/builds can launch processes, dependencies and generated work; select the authorized scoped recipe and resource policy rather than assuming pure reads.",
    '''For a dependency-metadata or upgrade question, inspect `go.mod`, `go.sum`, applicable `go.work`,
replacements, toolchain/directive constraints and the repository's dependency-management recipe.
Use /golang-dependency-management for Go dependency-change mechanics. Inspect the installed Go
help and recipe before executing version queries or upgrade/tidy commands: they can download modules,
write manifests or execute tooling. Execute only authorized effects. Do not survey symbols or call
paths unless a separately named compatibility, API-use or impact fact requires that evidence.

Direct configured gopls follows the routing contract's recorded capability gap, with build context
and the operation verified. Bounded native edits and missing diagnostics follow
`references/10-routing-contract.md`; semantic-provider absence alone does not require setup.
Go tests/builds can launch processes, dependencies and generated work; select the authorized scoped
recipe and resource policy rather than assuming pure reads.''')

# Draft first: store the complete revised artifacts before shortening any new text.
for path, text in list(drafts.items()):
    if path.suffix == '.md':
        text = re.sub(r'\s*\(`\$[a-z][a-z0-9-]*`\)', '', text)
        text = re.sub(r' · `\$[a-z][a-z0-9-]*`', '', text)
    drafts[path] = text
    target = out / 'authoring-drafts' / path.relative_to(root)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding='utf-8', newline='\n')

(out / 'authoring-progress.md').write_text('''# Authoring progress

- Completed: complete target-package reads, owner/instruction reads, verified neutral installed implementer definition, ratified scope and draft preservation.
- Completed: full revised drafts saved under authoring-drafts before compression.
- Remaining: behavior-preserving wording pass, focused checks, rule/scenario evidence and frozen manifest.
- Last evidence: target packages had no existing tracked/staged changes; parent-owned plan artifacts are preserved.
- Controls: configured definition neutral (no model/effort pins); requested gpt-6.1-sol/medium; serving identity and narrower MCP enforcement unknown. Workspace-write with narrower declared two-package/artifact scope; no children or external effects.
''', encoding='utf-8', newline='\n')

print(f'Saved {len(drafts)} complete revised drafts; product files unchanged.')
