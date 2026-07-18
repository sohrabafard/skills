# Mode A — Platform Audit: Kit + Consumers Surveillance

Periodically (or on request) an agent inspects the kit **and every registered consumer** as one system, hunting
for what per-repo work cannot see: bugs, contract drift, and — most valuable — logic that has quietly been
written twice. The audit exists because "baseline" is discovered, not just designed: some abstractions only
become visible after two consumers have independently solved the same problem.

When no explicit request sets the cadence, these events warrant an audit: a consumer reaches `active`; a kit
minor/major ships and propagation completes; a migration (entitlement-api, tusd) finishes a surface; or two kit
releases pass with no audit. Between audits, any agent that notices an audit-class smell in passing files the
single finding through the normal mode CR channel instead of waiting.

An audit **observes and files documents; it does not fix.** Every finding becomes a change request, baseline
proposal, propagation prompt, or drift note — fixes then flow through the normal mode C/K workflows where they
get proper review and impact analysis. (The one exception: the kit owner may fold a kit-side finding directly
into mode K in the same session, since that path has its own gates.)

## 1. Scope and inputs

- The kit repo: code, `CONTRACTS.md`, `GOVERNANCE.md`, `docs/change-requests/`, open decision records.
- Every repo listed in `docs/CONSUMERS.md` that is accessible from the session. Inaccessible consumers are
  audited from their architecture docs and registry rows only — and the report says so per consumer; an audit
  that silently skipped a consumer is worse than no audit.
- In Claude Code, fan the per-repo sweeps out to Explore/general-purpose subagents (one repo or one dimension
  per lane) and keep synthesis in the main context; in Codex, run lanes sequentially. Use `/alaa-low-noise`
  discipline — bounded greps, no full-file dumps.

## 2. The audit checklist (run each dimension per consumer, then cross-consumer)

**Per consumer:**

1. **Kit-surface re-implementation (P1 violations).** Grep for local versions of kit-owned behavior: hand-built
   envelopes/JSON binding, raw trusted-header reads outside trustkit, local readiness/health rendering, local
   outbox/job/receipt DDL diverging from canonical, `gen_random_uuid()` defaults, scattered `os.Getenv`,
   re-prefixed kit metric names, shadowed kit env keys.
2. **Wrap hygiene.** Find `KIT-WRAP` markers; each must reference a filed change request/baseline proposal and
   be younger than two kit releases. Unmarked wrapper-shaped code (thin adapters around kit calls that alter
   behavior) counts as a hidden fork — highest severity.
3. **Version and contract currency.** Registry row vs actual `go.mod` pin; contracttest present in CI and
   green (or honestly reported `runner_contract_pending`); deprecated kit APIs still in use.
4. **Bugs on kit seams.** The historical hot spots: ack-before-commit paths, outbox rows written outside the
   business transaction, idempotency without a run-twice test, unowned goroutines, pooled-lane DDL/advisory
   locks, missing snake_case tags on nested wire structs, high-cardinality metric labels, PII in logs.
   Judge against P1–P13 (`/alaa-golang-clean-code-principles`) and cite P-numbers.
5. **Registration integrity.** Service consumes the kit but has no registry row, or a stale row.

**Cross-consumer (the audit's unique value):**

6. **Duplication → abstraction candidates.** Compare consumers pairwise for logic that is the *same shape* in
   ≥2 places: helpers, middlewares, retry/backoff policies, cache adapters, provider plumbing, validation
   idioms, test harness code, deploy/CI snippets. The rule of two: same shape in two consumers → baseline
   proposal; in one consumer but predicted by a designed-service doc for another → note it as `emerging`.
   Respect recorded negative decisions, but read them at the right granularity, and do not re-propose settled
   non-abstractions without new evidence — the framework ruled the two latent Redis *domain shapes* different and
   service-local, yet the generic Redis *transport* they share was promoted to `rediskit` (§12 decision 6, resolved
   2026-07-18). The negative decision covers the domain policy, not the mechanics: do not re-propose the settled
   shape-level non-abstraction, but do flag any consumer that hand-rolls a go-redis client/cache adapter instead of
   importing `rediskit`.
7. **Behavioral divergence on shared contracts.** Same kit surface used with different semantics (different
   error-code choices for the same failure, different lane usage, different readiness severities for the same
   dependency class) — this is drift in consumer space even when no kit code was copied.
8. **Kit-side gaps.** Requests/decisions promised but unshipped; contracttest holes (a `CONTRACTS.md` shape with
   no assertion); docs that lag shipped behavior.

## 3. Verification bar

Report only findings you verified against current code in this session — file:line evidence, or a command you
actually ran. An audit finding that turns out to be a misread costs the platform two agent cycles. When you
cannot verify (inaccessible repo, ambiguous intent), the finding ships as `suspected` with what would confirm
it. Severity: `critical` (data loss / security / silent contract break), `high` (fork, drift, blocking bug),
`normal` (debt, docs, hygiene).

## 4. Outputs

1. **The audit report** — `docs/audits/YYYY-MM-DD-platform-audit.md` in the kit repo, per
   `assets/templates/audit-report.md`: scope actually covered, findings with evidence and severity, the
   duplication matrix, and a follow-up ledger where every finding maps to exactly one action:
   - kit bug/change → change-request file (write it yourself, same rules as mode CR; audit-originated
     requests/proposals live in the kit repo's `docs/change-requests/` directly)
   - abstraction candidate → baseline-proposal file (same location rule)
   - consumer-side fix → propagation prompt via `/alaa-prompting-guide` + `assets/templates/consumer-update-prompt.md`,
     saved beside the report as `YYYY-MM-DD-audit-fix-<consumer>-<slug>.md`
   - doc/source-of-truth disagreement → drift note (Basic Memory drift workflow when available, else a
     timestamped doc), continuing on the safest verified behavior
2. **Updated registry** rows where the audit corrected reality (stale versions, missing consumers).

No finding may end as prose only — if it mattered enough to report, it maps to a filed action; if it doesn't
merit an action, it doesn't belong in the report.
