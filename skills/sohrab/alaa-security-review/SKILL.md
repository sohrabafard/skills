---
name: alaa-security-review
description: "Security review gate for production multi-tenant services: trust boundaries, authentication and authorization, tenant isolation, injection, output encoding and XSS, SSRF and outbound fetching, file upload and serving, secrets and cryptography, race conditions, and fail-closed behaviour. Use when reviewing or writing an authn/authz change, a new endpoint, webhook, or queue consumer, a raw-HTML or sanitisation path, a query that can cross tenants, a request-influenced outbound URL, an upload or download path, a token, session, or step-up change, or a security-relevant configuration default - and before merging any change that moves a trust boundary. Emits a per-item PASS/FAIL/N-A verdict, a stop-the-line list, and a prioritized remediation plan. Do not use for style cleanup, docs-only work, or performance tuning with no trust impact. Route availability-side degradation, timeouts, retries, and circuit breaking to /alaa-reliability-sla; how this platform's own tokens and trusted headers are issued and verified to /alaa-trust-gateway-auth; security-event and telemetry design to /alaa-observability-soc."
---

# Alaa Security Review

Review a change against the rules in this skill and emit a verdict per item. The verdict is the deliverable: a named set of items, each with a named result. Orchestrators and platform contracts gate on this verdict, so a verdict emitted on ground the reviewer never examined is worse than no verdict - it launders an unexamined change as reviewed.

Companion skills are written `/name` here; under Codex the same skill is `$name`.

## Modes

**Fast Gate** is the default and runs on every change in scope. It is bounded by the surface inventory in `references/10-fast-gate.md`, not by a clock. When the inventory is larger than the time available, report the items you determined and report the remainder as FAIL / not determined. Never shorten the gate by dropping items.

**Deep Review** adds threat modelling, configuration and deployment hardening, and a prioritized remediation plan. Escalate when any trigger in `10-fast-gate.md` fires. That test is mechanical; it is not a judgment about how risky the change feels.

## Evidence discipline

Three verdicts exist per item, and only three:

- **PASS** - you read the code that implements the control and it satisfies the rule. Name the file and the symbol.
- **FAIL** - you read the code and it violates the rule, **or** you could not determine the answer from actual code. The second kind carries the reason `not determined`, what you examined, and what would settle it.
- **N/A** - the change contains nothing the item applies to. Name why in one clause.

An item you could not verify is FAIL with reason `not determined`. It is never omitted and never PASS. Absence of evidence is not evidence of a control, and silence about an item reads to every consumer of this verdict as a PASS on it.

A FAIL of the `not determined` kind is ranked at the severity the item would carry if the control were absent, not at the severity of an unknown. Leaving an item undetermined therefore costs the same as failing it, which is the point.

A PASS verdict on the change enumerates every item marked PASS and every item marked N/A, and closes with the line `Items not listed above were not examined.` An item absent from that enumeration is not covered by the verdict.

## Fail-closed doctrine

**A control that decides whether a caller may act denies when it cannot reach a decision.**

"Cannot reach a decision" is the whole set, not only an explicit deny: the authorization service timed out, returned a non-success status, or returned a body the caller could not parse; the policy, permission map, or model version failed to load or is unpinned; the key material needed to verify a credential is unavailable; a required piece of verified context is absent, empty, or malformed; the rate-limit or lockout store is unreachable; the flag that gates the control cannot be read. In every one of those states the request is refused with the control's own error, the protected work does not run, and the failure is emitted as a distinct event rather than folded into a generic 500.

Two consequences that reviews miss most often. A cache in front of a decision may absorb a *cache* outage by consulting the authoritative source, and must never absorb an *authoritative-source* outage by serving a stale allow. And a control skipped because its dependency was down has not degraded - it has been removed for the duration of the outage.

`/alaa-services-contract` records this platform's own instance of the doctrine at its request-time authorization layer; that file owns the wire behaviour, and the general rule above binds a new service that has never read it.

### Fail-closed versus fail-open, and which doctrine applies

The two doctrines contradict each other by design. The deciding question is what the component's failure lets through, not how important the component is.

- A component that answers "may this actor do this?" **fails closed**. Denying costs availability; allowing costs a breach. This skill owns those components.
- A component that only observes, records, or reports **fails open** - a telemetry exporter, a metrics sink, a trace pipeline, the *shipping* of an audit record to a SOC. Dropping its output costs visibility; blocking the request costs availability and buys no security. `/alaa-reliability-sla` owns those, together with timeouts, retries, backpressure, shedding, and the error budget.
- The line runs through the audit trail rather than around it: the *write* of an audit record for a privileged action is part of the control and fails closed where the repository states non-repudiation is required; the *forwarding* of that record downstream fails open, buffers, and counts what it dropped.

An agent implementing a control states which doctrine it chose, in the code or in its test. A component whose failure behaviour is undecided will have it decided by its library default, and library defaults are fail-open.

## Constraints on the review itself

- Read the repository's own `AGENTS.md` / `CLAUDE.md` and its existing security and error contracts before judging a change against these rules. Where the repository states a stricter rule, the stricter rule wins and the report says which rule it applied.
- Map every finding to a reachable entry point, an actor, the failing control, the file, and a check that proves the fix. A finding that names a standard but no route is not a finding.
- Propose the smallest auditable fix that preserves the repository's existing architecture and error contract. Never propose a broad refactor as a remediation.
- Never propose adding a third-party security product, scanner, or service. Name the command or mechanism the repository's stack already has; where none exists, that absence is itself a finding at the severity `60-deep-review-and-hardening.md` assigns it.
- Never write a secret, credential, token, or personal datum into a finding, a reproduction step, or a test fixture. Reproduce with a placeholder.
- Route every model and effort question to `/alaa-prompting-guide`. Never state a model name in a review.

## Stop-the-line findings

Each of these blocks merge. Stop-the-line and P0 are the same set: an item here is P0 by definition, and the scale below ranks the remainder.

**Access control**

1. A path that reads or writes another tenant's data, or an object read authorized only by possession of its identifier.
2. A privileged action with no permission check, or with a check that is not the exact permission the action requires.
3. A permission, access level, or choice of query, route, response field, validation, or branch derived from a role name or a role-derived tier - including a broad role such as `admin` short-circuiting an exact permission or a per-object decision.
4. A component treating metadata that *describes* an already-made allow decision as an input to a further authorization decision.
5. An authentication or authorization control that proceeds when it cannot reach a decision.
6. A step-up or re-authentication proof accepted for an action other than the one its purpose names, or renewed without a fresh presentation of the credential.
7. A downstream service accepting a boundary-verified credential, or the boundary's verified-metadata form of it, from a public client.

**Credentials, secrets, cryptography**

8. A credential, secret, token, or recovery code in a log, response body, metric label, trace attribute, URL, or committed file.
9. A verifier that accepts `none`, selects its algorithm from the credential itself, or has no configured algorithm allowlist.
10. Missing issuer or audience validation on a credential accepted from more than one issuer, or valid for more than one audience.
11. A key identifier taken from a credential and used to locate key material by URL, path, or remote fetch.
12. An access credential whose lifetime exceeds the session it serves, with no rotation and no revocation path.
13. A refresh credential recoverable at rest, or readable by page script, or without rotation, or without a defined response to reuse.
14. A secret-bearing value compared with a comparison that returns on the first differing byte.
15. A user-chosen password stored under a fast hash, or without a per-record salt.

**Untrusted input and output**

16. Request-derived text spliced into SQL, a document filter, a shell command line, a template body, or a filesystem path.
17. Untrusted bytes deserialized by a mechanism that can instantiate types named in the input.
18. Untrusted HTML rendered without the platform's sanctioned sanitiser, or a second raw-HTML path added alongside it.
19. An outbound request whose destination is influenced by request data, without an allowlist, or connecting to a name rather than to the address the guard checked.
20. An upload accepted without byte-level type verification, or written where a web server or interpreter can reach it, or served with a client-supplied content type.
21. A webhook or queue payload treated as trusted without verifying its origin.

**Configuration and concurrency**

22. A security control whose missing configuration produces a permissive default.
23. A single-use credential, quota, or balance consumed by a read followed by a separate write that a concurrent request can interleave.
24. Certificate or hostname verification disabled anywhere outside a test-only build.

## Severity scale for everything else

- **P0** - every stop-the-line item, plus any finding statable as a concrete exploit path: the actor, the request, the result. Blocks merge.
- **P1** - a control that exists but is weaker than the rule, with no exploit path reachable in the current deployment. Fixed in this change, or in a follow-up whose owner and date the report records.
- **P2** - hardening whose absence creates no reachable path. Recorded and tracked; no date required.

## Output contract

Always in this order:

1. `Scope:` the five-column surface inventory from `10-fast-gate.md`, one line per column, plus the mode run and the trigger that selected it.
2. `Checked:` every item examined with its verdict - PASS with file and symbol, FAIL with file and line or with `not determined` plus what would settle it, N/A with why. Close with `Items not listed above were not examined.`
3. `Stop-the-line:` list, or `None`.
4. `Required fixes:` P0/P1/P2, each with impact, exact file(s), the remediation, and the check that proves it fixed.
5. `Validation:` exact commands or tests with the expected result of each, including the applicable negative tests from `50-credentials-and-cryptography.md`.
6. `PASS` only when all three hold: no FAIL of either kind, no stop-the-line item, and section 2 enumerates every item in every trigger row the inventory hit.

## Reference routing

Read the smallest set the surface inventory hits.

- `references/10-fast-gate.md` - always. The inventory procedure, the trigger table that selects the rest of these files, and the Deep Review escalation test.
- `references/20-untrusted-input.md` - when request-derived data reaches SQL, a document filter, a shell, a template, a deserializer, a document parser, a path, a response header, or a redirect target.
- `references/25-browser-trust-and-output.md` - when the change puts user-supplied content in a browser, touches a raw-HTML or sanitiser path, changes a cookie, CSP, or CSRF control, or newly returns identifiers, error detail, or personal data to a client.
- `references/30-outbound-fetch-and-files.md` - when the change makes an outbound request whose destination is influenced by request data, or accepts, stores, or serves a file.
- `references/40-authorization-and-tenancy.md` - when the change touches an authentication or authorization decision, tenant derivation, a cache key, a background job, an export, a search index, a rate limit or lockout, or a check-then-act sequence.
- `references/50-credentials-and-cryptography.md` - when the change touches a token, session, refresh credential, step-up proof, password, signature, HMAC, key, or random value.
- `references/60-deep-review-and-hardening.md` - on Deep Review, or when a security-relevant configuration value, default, dependency, container, or network exposure changes.
- `references/90-source-map.md` - before relying on any version-sensitive claim, advisory, or standard.

## What this skill does not own

- `/alaa-trust-gateway-auth` owns how *this platform's* tokens and trusted headers are issued, verified, projected, and stripped: the claim set, the header names, the gateway configuration, key distribution. This skill owns the review questions that apply to *any* token system, plus the negative tests in `50-credentials-and-cryptography.md`. Read that skill to learn what this platform's credentials contain; the rules for judging a credential system live here, and every one of them binds a service that has never read it.
- `/alaa-reliability-sla` owns availability-side failure behaviour, as split under the fail-closed doctrine above.
- `/alaa-services-contract` owns the wire contracts these invariants instantiate - header names, decision codes, endpoint categories, route registration, permission catalogs. Where a rule here and a contract there describe the same control, that file owns the wire and this file owns the invariant.
- `/alaa-observability-soc` owns what a security event contains and how it reaches a SOC. This skill names *that* an event is required at a decision point; its shape is owned there.
- `/alaa-prompting-guide` owns every model and effort question.
- Report length and noise discipline belong to `/alaa-low-noise`; they are not security decisions and never justify dropping an item.
