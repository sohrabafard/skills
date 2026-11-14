---
name: alaa-golang
description: "Front door and router for Go work on the Ala platform. Selects the right Go skill, holds the Go rules no other skill owns, and reaches the whole Go surface — the vendor golang-* pack, the house companions, and the doctrine owners for reliability, contracts, observability, security and data — so a project can load only this skill plus alaa-golang-clean-code-principles. Owns the HTTP framework decision (the alaa-go-chi kit is chi and is the default for every new Ala Go service), deadline propagation and server bounds at the call site, request-decoding limits, repository and cache boundaries, TDD, the modern-Go baseline, and package choice. Use it before writing, reviewing, refactoring, or debugging any Go code. Do not use it for kit-conformance-only review of an existing kit service (alaa-golang-clean-code-principles) or for kit governance, change requests, and the active scope phase (alaa-go-chi-development)."
---

# Alaa Golang

Own the Go decisions that no routed skill covers. Select Go mechanics, house companions and doctrine
owners for Ala platform work. Complete the authorized task with repository evidence, required native
proof and the four completion answers.
If a routed owner disagrees with this skill, follow that owner and report both files as drift.

## When NOT to use

- Kit-conformance-only review of an existing `alaa-go-chi` consumer: load
  /alaa-golang-clean-code-principles directly.
- Kit governance, change requests or active scope phase alone: load /alaa-go-chi-development.
- A task with no Go source, module or toolchain change, such as a Dockerfile, chart, pipeline,
  edge configuration or a document merely mentioning a Go service: use its domain owner.

## Procedure

Read `references/00-topic-map.md` before a Go decision. Open only the rows that match the next action.

1. Establish repository truth before you propose a change.
   - Read the applicable repository instructions, including `AGENTS.md` and `CLAUDE.md` when present.
   - Read `go.mod` (module path and `go` directive).
   - Read the imports and existing tests of every package to change.
   - For a source change, inspect route registration.
   - For dependency-only work, inspect the module and workspace metadata and the native dependency recipe. Run source discovery for that work only when a source or impact question needs it.
   - Repository truth overrides this skill. Report discrepancies.
2. When `go.mod` requires `git.alaatv.com/vk/alaa-go-chi`, resolve the active phase through
   /alaa-go-chi-development before you write or review a line. Run its
   `../alaa-go-chi-development/scripts/phase-check.sh <kit-repo-root>`. Apply the action-specific matrix in
   `../alaa-go-chi-development/references/05-phase-and-source-truth.md`, including its evidence-required,
   forbidden, manual-read and nonzero-exit rules. A consumer request is not reactivation.
   Load /alaa-golang-clean-code-principles before the first edit or review comment.
   P1-P13 bind. This skill adds or overrides no principle.
3. Before you choose evidence, an editing surface or supplemental diagnostics, load
   /alaa-code-intelligence-routing. It alone selects providers, order, eligibility and fallback.
   Follow its rules for native continuation, missing guarantees and mutation reconciliation.
   This skill supplies Go doctrine and native proof, not a provider sequence.
4. Load each triggered domain owner before the governed action. Follow it without restating its rules.
   For an uncovered decision, apply the gap test reached through the topic map.
   Then report the decision, why no owner covered it and where it was recorded.
   Never decide a gap silently.
   Take model, effort, thinking-budget, runtime-capability and invocation answers from
   /alaa-prompting-guide and its `references/50-effort-and-thinking.md`, never this skill.
5. Change behavior through the test-first sequence that the topic map selects.
   Inspect the full resulting diff and callers. Then execute the validation gate below.
   Activation writes nothing and grants no additional authority.

## Authority and failure

Read accessible sources. Make authorized local edits within the requested scope.
Preserve existing behavior, contracts, user changes and repository conventions unless the task authorizes
a change. Get explicit permission for installation, integration configuration, commits, publication,
deployment, external mutation or destructive effects. A skill or tool being available grants none.
When a required owner, fact, phase authorization or proof is missing, stop the dependent action
and report the exact blocker. Unrelated safe work may continue.
Use the routing owner's finite failure budget for evidence and native gates.
Do not loop.

## Validation gate

After any Go edit, the authoring lane runs in order:

1. `go vet` on the changed packages.
2. `go test` on the changed packages, narrowed with `-run` to the changed topic when the package is large.
3. Verify that each shipped entrypoint links, with `go build` or a matching artifact from the same tree,
   environment and build configuration.

A test compile does not prove that the production entrypoint links.
/alaa-code-intelligence-routing governs supplemental provider diagnostics and any required uncovered
semantic property. They do not replace these native gates.
Run `govulncheck ./...` in the authoring lane when `go.mod` or `go.sum` changed.
The whole-suite run is an affected- and exhaustive-tier gate. /alaa-testing-strategy assigns it to an
authority other than the authoring lane. When the session has no such authority, run it on the final tree
before you report completion.
Add the repository's configured real-store build tag when a required test carries it.
Combine tagged and untagged selections only when reference 63's build-constraint and test-configuration
check proves normal behavior remains covered. Otherwise run both.
Add `-race` to each required run when the change touches a goroutine, channel, mutex, cache,
worker pool or package-level variable.
Report commands and outcomes using /alaa-go-chi-development
`../alaa-go-chi-development/references/05-phase-and-source-truth.md`: `passed`, `failed`, `blocked`,
`skipped`, `not run`.
Never report an outcome for a command you did not execute.
Stop successfully only when the requested behavior, required gates and completion answers are established
in the target repository.

## Completion answers

Report all four before you call Go work done:

1. Each validation command and its observed outcome.
2. What shipped: externally visible routes, request and response fields with types, error codes and
   event-payload changes. Write `no contract change` when there is none.
3. How it is operated: every environment key added, changed or removed, its default and accepted
   range, and each dashboard panel or alert required to make the change visible in production.
4. How it fails: each new failure mode and its exact operator signal, including metric, log event
   or degraded readiness check.

/alaa-services-contract owns contract-entry shape. /alaa-observability-soc owns dashboard and alert
shape. This skill requires the four answers without restating either owner's contract.
