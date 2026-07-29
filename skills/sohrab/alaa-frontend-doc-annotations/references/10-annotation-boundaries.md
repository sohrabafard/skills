# Annotation boundaries

Read this before the first edit of the pass.

## The documentation-only rule

A documentation-only diff is one where the build output is byte-identical before and after. That is the
test, not an intention.

**Allowed:** JSDoc blocks, file-level headers, inline comments, and the deletion of a comment this file
declares dead.

**Not allowed:** logic changes, template structure changes, CSS or style changes, import reordering,
formatter runs over untouched lines, and any behavior change carried inside a comment edit.

If a repair is needed, the pass does not make it. Report it as a finding naming
`/alaa-vue-typescript-clean-code` (`$alaa-vue-typescript-clean-code`) as the skill that makes it, and leave
the code as it stands. **This skill never repairs code.** That is the single mandate the two skills cannot
both hold, and it is why they are separate skills.

## When a comment and its code disagree

This is the failure mode a documentation pass actually meets, and it has one rule per case. A comment
disagrees with its code when the comment names a symbol that no longer exists, states a branch that no
longer runs, states a value that differs from the value in the code, or asserts a behavior the code beneath
it does not perform.

| What you found | What the pass does |
|---|---|
| The comment describes code that was deleted or renamed | Delete the comment in the same diff. A comment about absent code is not documentation. |
| The comment states a fact the code contradicts, and the code is right | Rewrite the comment to the code's behavior. |
| The comment states a fact the code contradicts, and the *comment* is right — the code has a bug | **Do not touch either.** Report it as a defect, name the file and line, and stop. A documentation pass that silently rewrites the comment hides a bug; a documentation pass that fixes the code is not a documentation pass. |
| The comment is an `AUTH NOTE:` or `SECURITY NOTE:` and its `verified:` date is older than the file's last commit | `references/60-staleness-and-verification.md`. Re-verify against the owner named in the note, or escalate. Never refresh the date without re-verifying. |
| The comment is a `TODO` with no owner, no reason and no boundary | Delete it, or rewrite it as `TODO(<owner>): <reason>; remove when <observable condition>`. |
| The comment is a commented-out implementation | Delete it. Git holds it. |

## Where an annotation is required, and where it is noise

**Required.** Every exported function, exported arrow-const, store action, composable and fetch wrapper in
a module imported by two or more other modules carries a leading `/** ... */`. The checker asserts this as
`ANN101`. Boot files, router guards, SSR data-loading paths and auth or hydration bridges are in this set
whenever they export anything.

**Required regardless of export count** when the code's correctness depends on a fact not visible inside
the function: the render phase it may run in, the auth state it assumes, the store that must already be
hydrated, or a unit, timezone or encoding assumption.

**Noise.** A comment restating the statement below it. A comment on a one-line assignment. A block of
repeated comments over a list of similar declarations. Long paragraphs inside a function body — an inline
comment is at most two lines, and a comment needing more than two lines becomes a function-level or
file-level block.

**Templates.** Do not add comments inside `<template>` unless the repo's `AGENTS.md` names template
comments as a convention or the existing template already contains them.

## Wording that survives a refactor

Do not name a local variable, a file path or a line number inside a comment. Refer to the exported symbol
or the module's public name, which survive a rename. A comment that says "see line 214" is false as soon as
someone inserts a line above it; a comment that says "see `decodeUnverifiedUiAuthorization`" is not.

Re-open the target file immediately before editing it. If the file is being changed for unrelated reasons
in the same branch, annotate it in a separate commit — the change-control rule is
`/alaa-workflow` (`$alaa-workflow`) and `/alaa-controlled-ops` (`$alaa-controlled-ops`), not this skill.

## Owners of ground a comment may describe

A comment may *state* any of these facts. This skill never decides what the fact is; it decides the shape
of the sentence and whether it is still true. When a comment asserts one of these, cite the owner in the
comment or in the pass report.

| Ground | Owner |
|---|---|
| Comment-versus-extract, SOLID, the `any` policy, abort, race and double-fire correctness | `/alaa-vue-typescript-clean-code` (`$alaa-vue-typescript-clean-code`) |
| Threat classes; what counts as a security assumption; the sanctioned sanitiser | `/alaa-security-review` (`$alaa-security-review`) |
| The trust boundary; gateway and trusted-header facts | `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`) |
| The permission bitmap contract and its canonical TypeScript decoder | `/alaa-permission-generator` (`$alaa-permission-generator`) |
| SSR, hydration, lifecycle and reactivity behavior | `/alaa-frontend-developer` (`$alaa-frontend-developer`) |
| Quasar API, boot files, SSR discriminators, config | `/alaa-quasar-app-vite-v3` (`$alaa-quasar-app-vite-v3`) |
| Every name and value a comment quotes: header names, route names, storage keys, status strings | `/alaa-services-contract` (`$alaa-services-contract`) |
| What a log line, metric or trace attribute means; correlation ids | `/alaa-observability-soc` (`$alaa-observability-soc`) |
| A complexity bound a comment states, and the growth dimension it names | `/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`) |
| Digit and text normalization, fleet-wide | `/alaa-input-normalization` (`$alaa-input-normalization`) |
| Test design, proof levels, what a test-intent comment may claim | `/alaa-testing-strategy` (`$alaa-testing-strategy`) |
| Browser storage quota, eviction and persistence semantics | `/alaa-indexeddb-browser-storage` (`$alaa-indexeddb-browser-storage`) |
| Persian-language deliverables. Never Persian inside a source file | `/alaa-docs-farsi` (`$alaa-docs-farsi`) |
| The quality bar itself | `/alaa-project-constitution` (`$alaa-project-constitution`) |
| Output discipline in the pass report | `/alaa-low-noise` (`$alaa-low-noise`) |
| Model and effort | `/alaa-prompting-guide` (`$alaa-prompting-guide`), `references/50-effort-and-thinking.md` |
