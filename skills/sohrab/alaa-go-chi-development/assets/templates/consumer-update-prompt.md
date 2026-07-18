<!--
Propagation prompt: the kit owner (or auditor) hands this to the agent that owns ONE consumer service.
Use only after explicit consumer reactivation AND an actual kit release. Author WITH alaa-prompting-guide loaded —
it owns model-specific phrasing and trigger syntax (Claude Code: /skill-name; Codex: $skill-name — pick per target
runtime, never mix). Save as: <kit-repo>/docs/change-requests/YYYY-MM-DD-<slug>-update-<consumer>.md
(audit-originated: YYYY-MM-DD-audit-fix-<consumer>-<slug>.md beside the audit report).
One prompt per consumer. Must be executable by an agent with ZERO context from your session.
Replace every <...> and delete these comments before handing over.
-->

You are updating the `<consumer>` service (repo: `<repo path/URL>`) to follow a released change in the shared
`alaa-go-chi` kit. Work only inside that repository, plus the one authorized kit-repo edit in step 7.

Before any code: load `<trigger>alaa-go-chi-development` (follow its consumer-mode rules),
`<trigger>alaa-golang`, `<trigger>alaa-golang-clean-code-principles`, and the domain companion skills the changed
surfaces require.

## Released kit change

<2–6 sentences: the change, motivating request/bug, the immutable version/tag that ships it, classification
(patch/minor/major/deprecation). Cite the decision record docs/change-requests/<file> and the relevant
CONTRACTS.md delta.>

## Your task

1. Pin `git.alaatv.com/vk/alaa-go-chi` to `<released version>` in `go.mod`; no committed local `replace`.
2. Adapt these surfaces (before → after contract shapes, with this consumer's known call sites):
   - <surface 1: exact symbol/env key/DDL, old shape → new shape>
   - <surface 2 …>
3. Regenerate all generated artifacts with the matching kit binary (`alaa-go-chi gen`, scaffold/API generators);
   never hand-edit generated files.
4. Remove every `KIT-WRAP` this version resolves: <list, or "none known — search for KIT-WRAP and judge each
   against the decision record">. Do not re-implement or fork kit behavior.
5. Change no other behavior; if the upgrade reveals an unrelated bug, file it separately.
6. Validate: `go build ./...`, `go test -race ./...`, `contracttest`, `make api-contract`, the repo lint gates, and
   the truth-tier/deploy-render gates the change touches. A failing contracttest you cannot resolve by following
   this prompt means the kit broke contract — stop and file a `blocking` kit change request instead of working
   around it. Never claim remote CI without a real runner job.
7. Update only this service's row in kit `docs/CONSUMERS.md`: `kit_version`, `contracttest`, `updated` — from
   verified results.

## Report back

Changed files; contract impact; exact validation commands with outcomes and blockers; remaining production-evidence
gaps; any `NEEDS_CONFIRMATION` items; explicit confirmation that no kit surface was re-implemented or forked.
