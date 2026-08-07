# Platform Audit

An audit reports evidence-backed defects and drift. By default it observes and files documents; it does not fix.
When the user explicitly authorizes fixes, follow fix → validate → re-review until no actionable finding remains.
Every finding that matters maps to exactly one filed action; a finding not worth an action does not belong in the
report.

**Capability required: `consumer-repo-read` for any consumer surface, `consumer-impact-claim` for any per-consumer
verdict, `consumer-prompt-authoring` for a remediation prompt.** Look each up in the matrix in
[05-phase-and-source-truth](05-phase-and-source-truth.md) before scoping. Where a cell blocks you, audit the kit
only, and record in the report's coverage table that the consumer was not inspected and why.

## Scope

**Kit surfaces, always:** code, generators, generated goldens, the consistency of `CONTRACTS.md`, the `.rules/`
files, `docs/INDEX.md` and the package documentation, this skill package, and kit-local infrastructure
and CI evidence. Follow-up actions are kit-local change requests, baseline proposals, drift notes, or authorized
fixes.

**Consumer surfaces, when the capability cells allow:** iterate every accessible `docs/CONSUMERS.md` row; audit
inaccessible consumers from their architecture documents and registry rows only, and say so per consumer. An
audit that silently skipped a consumer is worse than no audit. In Claude Code, fan per-repository sweeps out to
Explore or general-purpose subagents, one repository or one dimension per lane, under `/alaa-low-noise`
(`$alaa-low-noise`) discipline; in Codex, run the lanes sequentially.

## Dimensions

1. **Correctness and data loss:** transactions, outbox/receipt/ack ordering, migration reversibility
   (up-down-up), retries and terminal states, run-twice idempotency proof.
2. **Security and privacy:** the trust boundary, authorization and TOTP, tenant isolation, secrets, PII in logs
   or labels, SSRF and provider or webhook exposure. Route verdicts to `/alaa-security-review`
   (`$alaa-security-review`).
3. **Concurrency and reliability:** owned bounded workers, cancellation, shutdown ordering, retry storms, pool
   budgets, deadlines. Doctrine is `/alaa-reliability-sla` (`$alaa-reliability-sla`).
4. **Contracts and governance:** drift among code, docs, tests and generators; error, metric, env, API and
   migration vocabulary drift; capability-matrix violations; `contracttest` holes, meaning a `CONTRACTS.md` shape
   with no assertion; and decisions promised but unshipped.
5. **Observability:** correlation and trace propagation, low-cardinality metrics, readiness severities, audit
   trails.
6. **Performance and SLA evidence:** allocation and contention, database, query and index behaviour, broker and
   cache pressure, and the honest gaps in load, HA, chaos and capacity proof.
7. **Generated, deploy and CI truth:** regeneration-only changes, bidirectional API coverage, rendered manifests,
   real runner status.
8. **Clean code**, citing P-numbers from `/alaa-golang-clean-code-principles`
   (`$alaa-golang-clean-code-principles`).

**Per consumer**, when permitted: kit-surface re-implementation — hand-built envelopes, raw trusted-header reads,
local readiness rendering, diverging outbox/job/receipt DDL, `gen_random_uuid()` defaults, scattered `os.Getenv`,
re-prefixed metric names; `KIT-WRAP` hygiene against the contract in `10-`, where wrapper-shaped code with no
marker is a hidden fork and the highest severity; the registry row against the actual `go.mod` pin; whether
`contracttest` is wired and honest; deprecated APIs still in use; and seam bugs such as ack-before-commit, an
outbox write outside the business transaction, unowned goroutines, pooled-lane DDL, missing snake_case tags,
high-cardinality labels, and PII in logs.

**Cross-consumer**, when permitted — the audit's unique value: the same behaviour shape in two or more services
is a baseline-proposal candidate; in one service but present in another's architecture document, it is
`emerging`. Respect recorded negative decisions at the granularity they were made — the `rediskit` precedent
promoted the shared transport and left the domain cache shapes local, so do not re-propose the settled shape, and
do flag a hand-rolled transport. Also look for behavioural divergence on shared contracts: different error codes
for the same failure, different lane usage, different readiness severities for the same dependency class.

## Verification bar

Report only findings verified in this session, with `file:line` evidence or a command you ran. A finding you
could not verify ships as `suspected`, with what would confirm it. Severity: `critical` for data loss, a security
hole, or a silent contract break; `high` for a fork, drift, or a blocking bug; `normal` for debt, docs, and
hygiene. Distinguish deterministic repository defects from host and network friction. "Bug-free" and "99.99%
ready" are not provable from static review — name the proof level reached and the evidence missing, per `05-`.

## Outputs

1. **Audit report** at `docs/audits/YYYY-MM-DD-<scope>-audit.md` in the kit repository, per
   `assets/templates/audit-report.md`: honest coverage, findings with evidence and severity, the duplication
   matrix where cross-consumer analysis was permitted, the validation and readiness boundary, and a follow-up
   ledger in which every finding maps to exactly one action — kit change request, baseline proposal, drift note,
   authorized fix, or a remediation prompt named
   `YYYY-MM-DD-audit-fix-<consumer>-<slug>.md` beside the report and authored with `/alaa-prompting-guide`
   (`$alaa-prompting-guide`).
2. **Registry corrections** where the audit proved a row stale, within the capabilities you hold.
