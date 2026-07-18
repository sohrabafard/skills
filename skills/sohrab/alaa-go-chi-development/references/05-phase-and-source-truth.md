# Phase and Source Truth

Read this reference in every session, in every mode. It owns two things: the authority order for facts, and the
scope-phase gate that decides whether consumer work is allowed at all.

## Authority order

For any factual or permission question, trust in this order — and verify before acting:

1. System/developer/current user authority and safety rules.
2. Nearest repository `AGENTS.md`, then `CONSTITUTION.md` within its binding scope.
3. Current executable repository truth: code, tests, generators, generated artifacts, manifests, runtime evidence.
4. Maintained `GOVERNANCE.md`, `CONTRACTS.md`, `docs/RUNBOOK.md`, `docs/CONSUMERS.md`, `README.md`, `docs/INDEX.md`.
5. This skill and its references.
6. Memory, handoffs, old plans, historical architecture docs, and consumer-origin claims.

When sources disagree, that is drift: do not silently pick a side. Record it (Basic Memory drift note when available,
otherwise a timestamped doc) and continue on the safest verified behavior. A skill statement is never proof that the
current kit implements a feature — the capability map is navigation, not an alternate contract.

## Determining the active phase (do this, don't assume)

The kit's execution scope is set by owner-ratified decision records in the kit repo — not by this skill. At session
start, establish the active phase from repo truth: the scope banner in `docs/CONSUMERS.md`, the phase section in the
kit `AGENTS.md`/`CONSTITUTION.md`, and the newest scope decision in `docs/change-requests/`.

As of this skill revision the active phase is **`KIT_FIRST_STABILIZATION`**, ratified in
`docs/change-requests/2026-07-14-kit-first-stabilization-scope.md`. It ends **only** through a new explicit
project-owner instruction naming which consumer(s) reactivate and their new baseline. Never infer reactivation from a
consumer-shaped request, the presence of a consumer repo, a registry row, or an old decision record. If the repo shows
a newer scope decision than this skill describes, the repo wins — follow it and flag this skill for update.

## While KIT_FIRST_STABILIZATION is active

- Scope is kit-only: work in the kit repo and kit-owned skill/doc surfaces the task authorizes.
- Do not inspect, edit, survey, validate, audit, or prompt consumer repositories — including `news`.
- Consumer implementations are not design constraints and not compatibility evidence; historical consumer context may
  explain a request's origin but creates no execution scope.
- `docs/CONSUMERS.md` is inventory only; every row stays `paused` with impact exactly `NOT_ASSESSED_KIT_FIRST`
  (never `none`, `additive`, or "compatible").
- No consumer prompts, no propagation, no consumer release gates. A stable kit release does not require consumer proof.
- Release evidence is kit-local: kit tests, contract tests, generated goldens, truth-tier tests, governance checks,
  and the accepted local CI smoke path. Remote CI stays `runner_contract_pending` until a real runner job passes.
- Change-request decisions may be accepted and implemented without a release: use `implemented-unreleased` and fill
  `shipped_in` only after an actual tag exists.
- If a task names a consumer, treat it as historical context or a kit-improvement request — not authority to open
  that repository.

## After explicit reactivation

The full two-way governance in references 10/15/20/30/40/50 applies: consumers build on the released kit, file
change requests, and register; the kit owner surveys the live registry prospectively, propagates with per-consumer
prompts, and tracks impact with verified evidence. Baseline from the then-current kit; no pre-reactivation
implementation acquires compatibility rights unless the owner grants them.

## Evidence vocabulary

Use exactly: `passed`, `failed`, `blocked`, `skipped`, `not run`, and `NOT_ASSESSED_KIT_FIRST`. Keep deterministic
repo defects separate from host/runtime/network friction. A claim such as "production ready" must name its evidence
boundary — unit/contract/race/static, real Postgres/RabbitMQ/Redis truth tiers, rendered deployment, load/capacity,
chaos/failover, real remote CI, and live SLO evidence are distinct tiers; never let a lower tier impersonate a higher
one.
