---
name: alaa-golang
description: "Front door and router for Go work on the Ala platform. Selects the right Go skill, holds the Go rules no other skill owns, and reaches the whole Go surface — the vendor golang-* pack, the house companions, and the doctrine owners for reliability, contracts, observability, security and data — so a project can load only this skill plus alaa-golang-clean-code-principles. Owns the HTTP framework decision (the alaa-go-chi kit is chi and is the default for every new Ala Go service), deadline propagation and server bounds at the call site, request-decoding limits, repository and cache boundaries, TDD, the modern-Go baseline, and package choice. Use it before writing, reviewing, refactoring, or debugging any Go code. Do not use it for kit-conformance-only review of an existing kit service — that is alaa-golang-clean-code-principles — or for kit governance, change requests, and the active scope phase — that is alaa-go-chi-development."
---

# Alaa Golang

The front door for every Go task on this platform, with three jobs of equal weight. It **selects** the right vendor
`golang-*` skill, house companion, or doctrine owner for the situation in front of you. It **holds** the Ala platform
policy those skills do not know about. And it **owns every Go decision that no vendor skill and no doctrine owner
covers** — filling that gap is this skill's own work, not an overflow from routing, and the test that decides what
belongs here is in `references/05-what-this-skill-does-not-own.md`. A project that loads this skill and
`alaa-golang-clean-code-principles` therefore reaches the whole Go surface. It restates nothing it routes to. When
this skill and a skill it routes to disagree, follow the routed skill and report the disagreement as drift; do not
pick a side silently.

## When NOT to use

Do not enter through this skill when the whole task belongs to another owner:

- **The task is kit-conformance review of an existing `alaa-go-chi` consumer and nothing else** —
  load `/alaa-golang-clean-code-principles` (`$alaa-golang-clean-code-principles`) directly.
- **The task is kit governance rather than service work** — load `/alaa-go-chi-development`
  (`$alaa-go-chi-development`) directly. Its row in `references/05-what-this-skill-does-not-own.md`
  lists which requests those are.
- **The task contains no Go source.** A Dockerfile, a pipeline, a chart, an edge configuration, or a
  document that merely mentions a Go service belongs to its own owner, named in
  `references/20-sohrab-companions.md`.

Handing one topic inside a Go task to another owner is a different question, answered topic by topic
in `references/05-what-this-skill-does-not-own.md`.

## Router

Read `references/00-topic-map.md` and open only the rows whose situation matches what you are about to do.

## Rules that hold on every Go task

**Evidence before decision.** Before proposing any Go change, read the repo's `go.mod` (module path and `go`
directive), the imports of every package you will touch, the route-registration site, the existing tests for the code
you will change, and the repo's `AGENTS.md` and `CLAUDE.md` when those files exist. Repository truth outranks every
statement in this skill; where they differ, follow the repository and report the difference.

**Phase gate on kit services.** When `go.mod` requires `git.alaatv.com/vk/alaa-go-chi`, read
`alaa-go-chi-development` `references/05-phase-and-source-truth.md` and establish the active scope phase from the kit
repository before writing or reviewing a single line. If that phase forbids consumer work, stop and report the phase
and its decision-record filename instead of doing the work. A consumer-shaped request, a consumer repository on disk,
a registry row, or an older decision record does not reactivate consumer work; only a project-owner instruction naming
the consumer does.

**Clean-code layer on kit services.** On the same trigger, load `/alaa-golang-clean-code-principles`
(`$alaa-golang-clean-code-principles`) before the first edit or the first review comment. Its P1–P13 are the
conformance bar; this skill adds no principle of its own and overrides none of them.

**Route Go code intelligence through `/alaa-code-intelligence-routing` (`$alaa-code-intelligence-routing`).**
CodeGraph owns unknown package location, source flow, callers, callees, relationships, likely impact, and the files or
regions to inspect. Serena owns a known Go file or symbol: outline, declaration, references, implementation hierarchy,
diagnostics, semantic rename, and symbol-scoped edits. Serena's Go backend uses `gopls`; that backend is not a second
evidence owner. Invoke `/golang-gopls` (`$golang-gopls`) directly only when Serena is unavailable or unhealthy, or
after recording one required build-aware operation that Serena does not expose. Use `grep` only for text that is not
a Go symbol: struct tags, SQL strings, template names, config keys, and generated-file markers.

**Route, do not restate — and record what nothing covers.** When another skill owns a topic, load it and follow it;
do not paraphrase its content into your answer or into this repository.
`references/05-what-this-skill-does-not-own.md` names every owner and the observable condition that hands the topic to
it. When a decision the task needs is covered by no vendor skill and no owner, apply the gap test in that same file,
decide, and state in your final report which decision you had to make and where you recorded it — a gap decided
silently is re-decided differently by the next agent.

**Never state a model, a reasoning effort, or a runtime capability.** When the task needs a model choice, an effort or
thinking budget, a subagent or plan-mode capability, or trigger-syntax guidance, load `/alaa-prompting-guide`
(`$alaa-prompting-guide`) and its `references/50-effort-and-thinking.md`, and take the answer from there.

**Validation gate.** After any Go edit, run in this order: `go build ./...`; Serena diagnostics on every changed Go
file; `go vet ./...`; the tests of the changed packages; `go test ./...`. If Serena is unavailable or unhealthy, or
does not expose the required diagnostic, record that one gap and invoke `/golang-gopls` (`$golang-gopls`)
`go_diagnostics` once as the fallback. Add `go test -race ./...` when the change
touches a goroutine, a channel, a mutex, a cache, a worker pool, or a package-level variable. Run `govulncheck ./...`
when `go.mod` or `go.sum` changed. Report every command with the evidence vocabulary in
`alaa-go-chi-development` `references/05-phase-and-source-truth.md` — `passed`, `failed`, `blocked`, `skipped`,
`not run` — and never report an outcome for a command you did not execute.

**Completion check.** Before calling Go work done, produce four answers in the final report:

1. Each validation command above and its outcome.
2. **What shipped** — the diff to the service's externally visible contract: routes added or removed, request and
   response fields added, removed or retyped, error codes, event payload fields. Write `no contract change` when
   there is none.
3. **How it is operated** — every environment key added, changed, or removed with its default and its accepted range,
   and every dashboard panel or alert rule that must exist for this change to be visible in production.
4. **How it fails** — each new failure mode the change introduces and the exact signal an operator sees when it
   occurs: which metric moves, which log event fires, which readiness check degrades.

The shape of a contract entry belongs to `/alaa-services-contract` (`$alaa-services-contract`) and the shape of a
dashboard or alert to `/alaa-observability-soc` (`$alaa-observability-soc`). This rule fixes only that all four
answers appear.
