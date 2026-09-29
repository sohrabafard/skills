# 0001 - Review repair boundaries

Status: not-required
Trigger condition: consistency/concurrency and failure-path wording triggered a design triage.
Owner: goal lead   Reviewer: independent correctness/security/migration gates   Date: 2026-09-29
Supersedes: none   Superseded by: none

## 1. Frame

Restore existing promised atomic account purge, single-player lifecycle, least-authority tool reuse and secret-output confidentiality. The reviews found implementation gaps, not a requested replacement subsystem.
Journeys: logout, source switch/disposal, cached validation and local rendering.
Constitution discovery is not applicable to this closed triage: no new service or platform-policy design is proposed; existing skill contracts supply the invariants.

## 2. Scope and boundary

Only first-party skill examples, scripts and their instructions may change. Browser engines, consumer applications, providers and clusters remain external and untouched. No data-writer boundary moves; extend the existing examples/helpers.
Boundary evidence: review-correctness.json, review-security.json and review-migration.json in the parent artifact directory. Runtime proof remains pending.

## 3. Contract

Existing local helper APIs and CLI purposes remain. Preserve data-row purge count, other accounts, existing-file refusal, operator installation authority and truthful failure exits. No HTTP/event/message or platform identity contract changes.
The versioned example schema may add an index; migration safety conditions and consumer compatibility are owned by the migration review, not inferred from this triage.

## 4. Data and consistency

Existing owners retain their data. Purge already promises one transaction; lifecycle already promises safe disposal; rendering already promises private output. Repairs must implement those promises, including orphan metadata and concurrent execution cases. No second stored copy is added.

## 5. Failure and load

Use the existing indexed account-range complexity and journal guidance for large purges. Do not invent deployment load or timeout numbers. Interrupted upgrade retains old data; failed purge must abort; unavailable secure descriptor checks must fail before writing secrets. No live performance or security claim follows from mocked tests.

## 6. Alternatives

No distinct boundary, ownership or consistency decision survives the existing contracts. Full-store scans violate the indexed purge contract; data-only metadata cleanup misses orphans; pathname reopen violates the secret-output invariant. These are invalid implementations, not competing subsystem designs. The design trigger therefore misfired; implementation is a bounded defect repair.

## 7. Rollout and reversal

Local example updates only. Consumers must coordinate a versioned upgrade and test blocked/abort behavior before adoption. After a v4 upgrade commits, a v3 opener cannot roll back the schema; use v4-compatible code or roll forward. Preserve model policy/projection coherence and new safety gates. Installation and external release remain unauthorized.

## 8. Open questions

The migration guardian's values-owner naming condition needs clarification because the platform contract has no registry of these example index names. Do not invent a global registry; obtain the exact owner requirement before widening the source scope. Other findings have explicit owners in review-fix1-brief.json.
