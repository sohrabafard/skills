<!--
Template for a propagation prompt: the kit owner (or auditor) hands this to the agent that owns ONE consumer
service. Author it WITH the alaa-prompting-guide skill loaded — it owns model-specific phrasing and trigger
syntax (Claude Code: /skill-name; Codex: $skill-name — pick per target runtime, do not mix).
Save as: <kit-repo>/docs/change-requests/YYYY-MM-DD-<slug>-update-<consumer>.md
        (audit-originated: YYYY-MM-DD-audit-fix-<consumer>-<slug>.md beside the audit report)
One prompt per consumer. Must be executable by an agent with ZERO context from your session.
Replace every <...> and delete these comments before handing over.
-->

You are updating the `<consumer>` service (repo: `<repo path/URL>`) to follow a change in the shared
`alaa-go-chi` kit. Work only inside this repository, plus the one allowed kit-repo edit named in step 6.

Before any code: load `/alaa-go-chi-development` (kit↔consumer governance — follow its consumer-mode rules),
`/alaa-golang`, and `/alaa-golang-clean-code-principles`.

## What changed in the kit, and why

<2–6 sentences: the change, the motivating request/bug, kit version that ships it, classification
(patch/minor/major/deprecation). Link/cite the decision record: docs/change-requests/<file> in the kit repo,
and the relevant CONTRACTS.md entry.>

## Your task

1. Pin `git.alaatv.com/vk/alaa-go-chi` to `<version>` in `go.mod`.
2. Adapt these surfaces (before → after contract shapes):
   - <surface 1: exact symbol/env key/DDL, old shape → new shape, where this consumer uses it if known>
   - <surface 2 …>
3. Remove any `KIT-WRAP` marker whose need this version ships: <list, or "none known — search for KIT-WRAP and
   judge each against the decision record">.
4. Do NOT change any other behavior; if the upgrade reveals an unrelated bug, report it separately — do not fix
   it in this change.
5. Validate: `go build ./...`, `go test -race ./...`, `contracttest`, the repo's lint gates. A failing
   contracttest you cannot resolve by following this prompt means the kit broke contract — stop and file a
   `blocking` kit change request per the governance skill instead of working around it.
6. Update this service's row in the kit repo's `docs/CONSUMERS.md`: `kit_version`, `contracttest`, `updated`.

## Report back

Changed files; validation commands run with outcomes; any `NEEDS_CONFIRMATION` items; explicit confirmation
that no kit surface was re-implemented or forked locally.
