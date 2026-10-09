---
name: alaa-golang
description: "Front door and router for Go work on the Ala platform. Selects the right Go skill, holds the Go rules no other skill owns, and reaches the whole Go surface — the vendor golang-* pack, the house companions, and the doctrine owners for reliability, contracts, observability, security and data — so a project can load only this skill plus alaa-golang-clean-code-principles. Owns the HTTP framework decision (the alaa-go-chi kit is chi and is the default for every new Ala Go service), deadline propagation and server bounds at the call site, request-decoding limits, repository and cache boundaries, TDD, the modern-Go baseline, and package choice. Use it before writing, reviewing, refactoring, or debugging any Go code. Do not use it for kit-conformance-only review of an existing kit service — that is alaa-golang-clean-code-principles — or for kit governance, change requests, and the active scope phase — that is alaa-go-chi-development."
---

# Alaa Golang

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

1. Establish repository truth before proposing a change. Read applicable repository instructions, including `AGENTS.md` and `CLAUDE.md` when present,
   `go.mod` (module path and `go` directive), and the imports and existing tests of every package
   to change. For source changes, inspect route registration. For dependency-only work, inspect
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
