# Lifecycle, Hashing, And Validation Semantics

## Canonical hashing

This skill owns canonicalisation for every digest the package computes: dry-run hash, payload hash, idempotency fingerprint. Apply it as written; an implementation that differs is a defect to report, not a precedent to preserve.

- **Function** — SHA-256, lower-case hex, all 64 characters. Not MD5, SHA-1, or `crc32`. If the storage column is narrower, widen the column; a truncated digest is a defect, not a fit.
- **Encoding** — hash the UTF-8 bytes of canonical JSON: map keys sorted byte-wise ascending at every depth, no insignificant whitespace, no trailing newline. In PHP, `json_encode($v, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE | JSON_THROW_ON_ERROR)` over an array whose keys were recursively `ksort`ed.
- **Lists** — element order in a list is data. Sort map keys only, never list elements. When two orderings of one set must yield one digest, sort that list in the planner before hashing and say so in the field's doc comment.
- **Numbers** — integers serialise with no decimal point and no exponent. Floats must not reach the canonicaliser: convert fractional and monetary values upstream to an integer in the smallest unit, or to a decimal string. `1`, `1.0`, and `"1"` are three different inputs and must not both occur for one field.
- **Null and absent are one value** — drop every key whose value is `null` before serialising, so an omitted key and an explicit `null` yield the same digest.
- **Booleans** — `true`/`false`, never `1`, `0`, or `"true"`.
- **Unicode** — normalise every string to NFC. Do not case-fold and do not strip inner whitespace: a difference an operator can see must change the digest.
- **Exclusions** — exclude current time, request ID, trace ID, correlation ID, actor ID, client IP, user agent, and attempt counter; that is, exclude every value the same caller could not reproduce by replaying the same request. Include everything the outcome depends on. An included field failing that test is a defect to report.
- **Stability** — a digest is a compatibility surface. Changing the function, key order, exclusion list, or any normalisation above invalidates every stored digest and every in-flight dry-run review, so it is a major version bump of `alaa/controlled-ops` whose release notes state that reviews are invalidated. Never ship it as a minor or patch release.

## Reviewed-hash comparison

Dry-run must precede approval and execution when the operation is approval-based. Both paths must recompute the canonical hash from current operation state and compare it with the digest recorded at dry-run review. A repository implementing "latest payload wins" for an approval-based operation is a defect to report, not a policy to preserve.

On mismatch, fail closed: reject the request, leave the operation in the status it held before it, write one audit record carrying both digests, and require a fresh dry-run before approval is possible again. Never execute against current state, never auto-approve the recomputed digest, never overwrite the reviewed digest. An absent reviewed digest is a mismatch and takes the same path.

## Idempotency: this skill's part only

`/alaa-reliability-sla` ($alaa-reliability-sla) owns the general contract in its `references/60-idempotency.md` — key supply, scope, retention, the uniqueness constraint, the concurrent-duplicate case, and store-unavailable behaviour. Read it there; do not restate it here.

ControlledOps owns two pieces. The fingerprint is the canonical hash above, computed over the operation request payload. And: distinguish same-key/same-fingerprint replay from same-key/different-fingerprint conflict — return the stored result for a replay without re-executing, reject a conflict through the mismatch path above, and never start a second execution under one key.

## Lifecycle helpers

Package helpers for cancel, retry-failed, fatal recovery, worker claim, or completion aggregation are admission and classification surfaces. The service still owns locks, state writes, queue dispatch, domain mutations, sibling-drift checks, and outbox safety.

## Validation gate

Lifecycle work is not done until tests exist that would fail against a plausible broken implementation and prove all five:

- invalid status transitions fail closed
- reviewed hash mismatches fail closed
- duplicate or conflicting idempotency attempts are classified correctly
- service-owned domain writes do not move into the package
- public docs and Postman examples still match implemented behavior

Name in the report, with its reason, any of the five this task could not test; never describe an untested property as covered. A canonicalisation change also needs a deterministic digest test — fixed input, expected hex asserted literally — so a future normalisation change fails a test instead of silently re-hashing production data.
