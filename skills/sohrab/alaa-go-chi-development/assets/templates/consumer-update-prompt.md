<!--
Propagation prompt: the kit owner or auditor hands this to the agent that owns ONE consumer service.
Writing it is the `consumer-prompt-authoring` capability and issuing it is `propagation` — look both up in the
capability matrix in references/05-phase-and-source-truth.md before you start, and note that propagation also
requires an actual kit release, since there is nothing to propagate before a tag exists.
Author WITH /alaa-prompting-guide ($alaa-prompting-guide) loaded — it owns model-specific phrasing and trigger
syntax (Claude Code: /skill-name; Codex: $skill-name — pick per target runtime, never mix).
Save as: <kit-repo>/docs/change-requests/YYYY-MM-DD-<slug>-update-<consumer>.md
(audit-originated: YYYY-MM-DD-audit-fix-<consumer>-<slug>.md beside the audit report).
One prompt per consumer. Must be executable by an agent with ZERO context from your session.
Replace every <...> and delete these comments before handing over.
-->

You are updating the `<consumer>` service (repo: `<repo path/URL>`) to follow a released change in the shared
`alaa-go-chi` kit. Work only inside that repository, plus the one authorized kit-repo edit in step 7.

Before any code: load `<trigger>alaa-go-chi-development` and follow its consumer-mode rules — including its
session-start phase read, which governs what you may touch — then `<trigger>alaa-golang`,
`<trigger>alaa-golang-clean-code-principles`, and the companion skills the changed surfaces require.

## Released kit change

<2–6 sentences: the change, the motivating request or bug, the immutable version/tag that ships it, and the
classification (patch/minor/major/deprecation). Cite the decision record docs/change-requests/<file> and the
relevant CONTRACTS.md delta.>

## Your task

1. Pin `git.alaatv.com/vk/alaa-go-chi` to `<released version>` in `go.mod`; no committed local `replace`.
2. Adapt these surfaces — before → after contract shapes, with this consumer's known call sites:
   - <surface 1: exact symbol / env key / DDL, old shape → new shape>
   - <surface 2 …>
3. Regenerate every generated artifact with the matching kit binary (`alaa-go-chi gen`, the scaffold and API
   generators), and resolve every `.kitnew` file an upgrade emits. Never hand-edit a generated file.
4. Remove every `KIT-WRAP` this version resolves: <list, or "none known — search for KIT-WRAP and judge each
   against the decision record">. Do not re-implement or fork kit behaviour.
5. Change no other behaviour. If the upgrade reveals an unrelated bug, file it separately.
6. Validate: `go build ./...`, `go test -race ./...`, `contracttest`, `make api-contract`, the repository lint
   gates, and the real-dependency and deploy-render gates the change touches. A failing `contracttest` you cannot
   resolve by following this prompt means the kit broke contract — stop and file a `blocking` kit change request
   rather than working around it. Never claim remote CI without a runner-executed job.
7. Update only this service's row in the kit's `docs/CONSUMERS.md`: `kit_version`, `contracttest`, `updated`,
   from verified results.

## Report back

Changed files; contract impact; the exact validation commands with their outcomes and blockers; the proof level
reached and the production evidence still missing; any `NEEDS_CONFIRMATION` items; and explicit confirmation that
no kit surface was re-implemented or forked.
