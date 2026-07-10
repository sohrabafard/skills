# Intent and Risk Discovery

Read this reference for every CREATE or UPDATE. Repository inventory shows what exists;
intent discovery identifies material obligations, failure modes, and owner decisions that
the current files may not yet express.

## Build the project-intent model

Synthesize, in this order:

1. explicit user context and owner decisions from the current request;
2. the complete prior constitution, including preserved principles, TODOs, proposals,
   exceptions, canonical-source pointers, and status/version evidence;
3. repository identity, owned user journeys, runtime surfaces, data flows, trust boundaries,
   deployment model, consumers, and operational expectations;
4. current externally verified domain knowledge relevant to those evidenced surfaces.

Treat an existing constitution as a durable prior-decision source. Preserve its semantic
intent unless current truth contradicts it or the owner approves a normative change. Do not
claim to reconstruct a prior chat message that was not retained in the constitution or a
named repository source; ask only when the missing provenance changes policy.

Write a one-paragraph internal intent statement covering who the project serves, what
outcome it owns, which failure classes matter, and which qualities appear load-bearing.
Separate `OBSERVED`, `INHERITED`, `INFERRED_CANDIDATE`, and `OWNER_DECIDED` claims.

## Expand the risk horizon

For each evidenced surface, test the applicable horizons below. This is a discovery lens,
not a requirement to add every topic to the constitution.

| Horizon | Questions to investigate |
|---|---|
| Correctness and concurrency | What races, duplicate work, ordering, idempotency, isolation, consistency, or cache-coordination failures could violate the owned outcome? |
| Availability and overload | What needs timeouts, bounded retries, backoff/jitter, admission control, backpressure, degraded modes, or recovery objectives? |
| Connectivity and client continuity | What happens during intermittent networks, refresh/token loss, partial responses, offline use, stale caches, resynchronization, or storage pressure? |
| Data lifecycle | What governs schema evolution, retention, deletion, backup/restore, reconciliation, corruption recovery, and auditability? |
| Security, privacy, and abuse | Which trust boundaries, identities, permissions, sensitive data, supply-chain risks, misuse cases, and regulatory duties apply? |
| Performance, scale, and cost | Which latency, throughput, fan-out, resource, bandwidth, storage, or third-party-cost risks can become architectural constraints? |
| User experience and inclusion | Which accessibility, localization, device/browser, error-recovery, and user-control guarantees are material? |
| Operations and change safety | What observability, rollout, rollback, compatibility, incident response, dependency upgrade, and ownership rules prevent unsafe change? |
| Domain-specific continuity | What specialized lifecycle or entitlement questions arise from evidenced capabilities such as media playback/downloads, payments, realtime sessions, search, or external providers? |

Use counterfactuals: peak load, dependency outage, process restart, duplicate delivery,
concurrent writes, stale cache, network interruption, partial rollout, expired credentials,
storage exhaustion, and rollback. Keep only scenarios that plausibly affect an owned surface.

## Research candidate practices

Research only after the intent model identifies a material gap. Prefer, in order:

1. current standards, specifications, and regulator or security-body guidance;
2. official framework, database, browser/platform, protocol, and vendor documentation;
3. maintained upstream repositories, reference implementations, and primary research;
4. reputable engineering articles only when primary sources do not answer the question.

Use narrow queries tied to the project surface and failure mode. Verify version-sensitive
claims live when tools are available. Record source, date, applicability, and limitations.
External knowledge may reveal a candidate obligation or option; it does not prove that the
project currently implements it or that the owner wants it.

Do not turn generic best practices into constitutional law. For every discovered candidate,
choose exactly one disposition:

- `REQUIRED_BY_EVIDENCE`: repository or already-ratified governance proves it; retain or add
  the minimum durable rule.
- `OWNER_DECISION_REQUIRED`: the choice changes product promise, security/privacy posture,
  compatibility, cost, data lifecycle, or operational risk; ask interactively.
- `DELEGATE_TO_CANONICAL_SOURCE`: important technical detail belongs in a named architecture,
  contract, runbook, standard, or generated owner.
- `NON_CONSTITUTIONAL_FOLLOW_UP`: useful implementation improvement but not durable law;
  report it outside CONSTITUTION.md.
- `NOT_APPLICABLE`: positive evidence excludes it; record the reason internally.
- `UNKNOWN`: evidence remains insufficient; use a structured TODO when material.

## Coverage gate

Before writing, verify that:

- each owned user journey and high-risk runtime/data surface was tested against the relevant
  horizons;
- every material candidate has a disposition and provenance;
- owner questions express decisions, not research trivia or presumed implementation details;
- external sources did not overwrite repository truth or prior ratified governance;
- irrelevant stack/domain content was removed;
- the final constitution keeps only durable, project-specific rules and closed delegations.

If broad discovery yields many implementation ideas but no constitutional decisions, keep
them out of CONSTITUTION.md and summarize the highest-value follow-ups separately.
