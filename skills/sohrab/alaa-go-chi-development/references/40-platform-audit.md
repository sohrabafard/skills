# Platform Audit — Kit (and, after reactivation, Consumers)

An audit reports evidence-backed defects and drift. By default it observes and files documents; it does not fix.
If the user explicitly authorizes fixes, follow fix → validate → re-review until no actionable finding remains.
Every finding that matters maps to exactly one filed action; a finding not worth an action does not belong in the
report.

## Scope by phase

**During `KIT_FIRST_STABILIZATION`:** audit only the kit repo — code, generators, generated goldens, maintained
docs (`CONTRACTS.md`/`GOVERNANCE.md`/`docs/INDEX.md` consistency), the skill package, and kit-local infra/CI
evidence. Do not inspect consumer repos, create consumer prompts, or perform cross-consumer duplication analysis.
Registry rows remain `NOT_ASSESSED_KIT_FIRST`; follow-up actions are kit-local change requests, baseline
proposals, docs, or authorized fixes only.

**After explicit reactivation:** iterate every `docs/CONSUMERS.md` row that is accessible; audit inaccessible
consumers from their architecture docs and registry rows only — and say so per consumer. An audit that silently
skipped a consumer is worse than no audit. In Claude Code, fan per-repo sweeps out to Explore/general-purpose
subagents (one repo or dimension per lane) with `alaa-low-noise` discipline; in Codex, run lanes sequentially.

## Dimensions (kit-local always; per-consumer and cross-consumer after reactivation)

1. **Correctness/data loss:** transactions, outbox/receipt/ack ordering, migration reversibility (up-down-up),
   retries and terminal states, idempotency run-twice proof.
2. **Security/privacy:** trust boundary, authz/TOTP, tenant isolation, secrets, PII in logs/labels, SSRF/provider/
   webhook exposure.
3. **Concurrency/reliability:** owned bounded workers, cancellation, shutdown ordering, retry storms, pool budgets,
   deadlines.
4. **Contracts/governance:** code↔docs↔tests↔generators drift; error/metric/env/API/migration vocabulary drift;
   phase-policy violations; contracttest holes (a `CONTRACTS.md` shape with no assertion); promised-but-unshipped
   decisions.
5. **Observability:** correlation and trace propagation, low-cardinality metrics, readiness severities, audit
   trails.
6. **Performance/SLA evidence:** allocation/contention, DB/query/index, broker/cache pressure, and the honest gaps
   in load/HA/chaos/capacity proof.
7. **Generated/deploy/CI truth:** regeneration-only changes, bidirectional API coverage, rendered manifests, real
   runner status.
8. **Clean code P1–P13**, citing P-numbers.

**Per consumer (reactivated):** kit-surface re-implementation (hand-built envelopes, raw trusted-header reads,
local readiness rendering, diverging outbox/job/receipt DDL, `gen_random_uuid()` defaults, scattered `os.Getenv`,
re-prefixed metric names); `KIT-WRAP` hygiene (marker → filed request, ≤2 releases; unmarked wrapper-shaped code is
a hidden fork — highest severity); registry row vs actual `go.mod` pin; contracttest wired and honest; deprecated
APIs still in use; seam bugs (ack-before-commit, outbox outside the business transaction, unowned goroutines,
pooled-lane DDL, missing snake_case tags, high-cardinality labels, PII in logs).

**Cross-consumer (reactivated — the audit's unique value):** the rule of two — the same logic shape in ≥2 services
→ baseline proposal; in one service but predicted by a designed-service doc → `emerging`. Respect recorded negative
decisions at the right granularity (the Redis precedent: shared transport was promoted to `rediskit`; the distinct
domain cache shapes stayed local — do not re-propose the settled shape, do flag hand-rolled transports). Also:
behavioral divergence on shared contracts (different error codes for the same failure, different lane usage,
different readiness severities for the same dependency class).

## Verification bar

Report only findings verified in this session — file:line evidence or a command you ran. Unverifiable findings
ship as `suspected` with what would confirm them. Severity: `critical` (data loss / security / silent contract
break), `high` (fork, drift, blocking bug), `normal` (debt, docs, hygiene). Distinguish deterministic repo defects
from host/network friction. "Bug-free" and "99.99% ready" are not provable from static review — state the missing
production evidence explicitly.

## Outputs

1. **Audit report** — `docs/audits/YYYY-MM-DD-<scope>-audit.md` in the kit repo, per
   `assets/templates/audit-report.md`: honest coverage, findings with evidence and severity, the duplication matrix
   (reactivated audits), validation/readiness boundary, and a follow-up ledger where every finding maps to exactly
   one action: kit change request, baseline proposal, docs/drift note, authorized fix — or, after reactivation, a
   propagation prompt (`YYYY-MM-DD-audit-fix-<consumer>-<slug>.md` beside the report, authored with
   `alaa-prompting-guide`).
2. **Registry corrections** where the audit proved a row stale — within what the active phase allows.
