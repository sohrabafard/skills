# Fast Gate

The default instrument, read on every review. Build the inventory, read the rows it hits, emit the verdict shape `SKILL.md` defines.

## Step 1 - Build the surface inventory

Write all five columns. A column with nothing in it is written as `none`. An unwritten column means the step was skipped, and a skipped step is FAIL / not determined on every item that column would have selected.

1. **Entry points added or changed.** Each HTTP route as method plus path, queue or topic consumer, webhook receiver, scheduled job, CLI command, gRPC method, admin action, and public SDK operation. For each, name what authenticates the caller and the file and symbol where that happens. An entry point whose authenticating code you cannot locate is stop-the-line item 5, not a note.
2. **Sinks reached.** Each database write; each database read that returns data to a caller; each outbound network call; each file write and read; each subprocess; each template render; each response that carries user-supplied content to a browser; each log line, metric label, or trace attribute that carries a request-derived value.
3. **Trusted inputs claimed.** Every value the code treats as already verified - an identity, a tenant or project id, a permission set, a role list, a step-up purpose, a signature verdict, a webhook origin - and for each, the exact component that verified it and the file where that verification happens. **A value whose verifier you cannot name is an untrusted value**, and every rule for untrusted input applies to it.
4. **Tenant-scoped data touched.** Every table, collection, search index, cache key namespace, object-store prefix, queue payload shape, and generated export that holds more than one tenant's data.
5. **Security-relevant configuration read.** Every configuration key that enables, disables, or parameterises a control. `60-deep-review-and-hardening.md` enumerates what counts.

The inventory is the `Scope:` section of the report. It is what makes "not examined" a checkable claim rather than an absence.

If all five columns are `none`, the change is out of scope for this skill: say so in one line, name what you inspected to conclude it, and stop.

## Step 2 - Read the rows the inventory hit

Read only these rows' files, and only the named section within each.

| The inventory contains | Read | Note |
|---|---|---|
| an entry point whose authenticating code you cannot locate | `40-authorization-and-tenancy.md` | stop-the-line 5 |
| an entry point reachable without an authenticated session | `40-`, `20-`, `60-` | escalates to Deep Review |
| a permission check, policy, gate, middleware, or per-object decision | `40-` | |
| tenant or project derivation, or a query predicate carrying a tenant | `40-` | |
| a cache key, memoised value, or process-level shared state | `40-` | tenant leak site 1 |
| a background job, queue consumer, or scheduled task | `40-` | tenant leak site 2 |
| an export, report, or bulk-read endpoint | `40-` | tenant leak site 3 |
| a search-index write or query | `40-` | tenant leak site 4 |
| a cross-tenant or admin aggregation path | `40-` | tenant leak site 5 |
| a read followed by a dependent write: single-use credential, quota, balance, idempotency key, counter | `40-` | |
| a rate limit, lockout, or per-tenant quota | `40-` | |
| a request-derived value reaching SQL, a document filter, or an ORM raw escape hatch | `20-untrusted-input.md` | |
| a request-derived value reaching a shell, a subprocess, or a child process environment | `20-` | |
| a request-derived value reaching a template body or a template path | `20-` | |
| a deserializer, or a decode of a cookie, cache entry, queue payload, or webhook body | `20-` | |
| an XML, YAML, SVG, office-document, or archive parser | `20-`, `30-` | |
| a request-derived value reaching a filesystem path or an object-store key | `20-`, `30-` | |
| a request-derived value reaching a response header, a redirect target, or an email header | `20-` | |
| a response that renders user-supplied content, or any raw-HTML path | `25-browser-trust-and-output.md` | |
| a change to a cookie attribute, a CSP, or a CSRF control | `25-` | |
| an identifier, error detail, stack trace, or personal datum newly present in a response | `25-` | |
| an outbound request whose host, port, path, or scheme is influenced by request data | `30-outbound-fetch-and-files.md` | |
| an upload, download, or file-serving path | `30-` | |
| a token, session, refresh credential, or step-up proof | `50-credentials-and-cryptography.md` | |
| a password, signature, HMAC, key, salt, nonce, or random value used in a decision | `50-` | |
| a security-relevant configuration key, default, or boot-time check | `60-` | |
| a new or upgraded third-party dependency | `60-` | |
| a container image, network exposure, TLS termination, or trusted-proxy setting | `60-` | |

## Step 3 - Universal items

These six apply to every change in scope, because each one's failure mode is the *absence* of something the inventory therefore cannot list. Every review reports a verdict on all six.

1. **Two decisions per entry point.** Every entry point in column 1 makes an authentication decision and an authorization decision, and they are separate pieces of code. An entry point that is authorized by the fact that it authenticated has no authorization. Rules in `40-`.
2. **Schema before logic.** Every entry point validates its input against a declared schema before any business logic reads it. Rules in `20-`.
3. **Named verifier per trusted value.** Every value in column 3 has a verifier you named. Any that does not is reclassified as untrusted for the rest of the review, and every item it feeds is re-judged on that basis.
4. **Decided failure behaviour.** Every control the change adds or touches has a failure behaviour that the code or its test states, and it matches the doctrine in `SKILL.md`.
5. **Nothing secret leaves.** No credential, secret, token, recovery code, or personal datum reaches a log, metric label, trace attribute, response body, URL, or committed file. Rules in `50-` and `25-`.
6. **No permissive default.** Every configuration value in column 5 is validated at process start, and its absence stops the process rather than producing a permissive fallback. Rules in `60-`.

## Step 4 - Escalate to Deep Review

Escalate when any one of these is true. The test is mechanical and does not depend on how risky the change feels.

- The change adds or modifies a control that decides access: authentication, authorization, tenant derivation, step-up, rate limiting, revocation, or session lifetime.
- The change adds an entry point reachable without an authenticated session.
- The change adds or changes an outbound destination influenced by request data, or a file upload, download, or serving path.
- The change alters what a trust boundary verifies, strips, projects, or forwards.
- The change touches payment, entitlement, quota, credit, or balance state.
- The change adds a third-party dependency that parses untrusted input, executes a subprocess, or opens a network connection.
- The change is a remediation for a security finding or an incident.
- A Fast Gate item resolved to FAIL / not determined and that item is on the stop-the-line list.

Deep Review does not replace the Fast Gate. It runs after it, against the same inventory, and adds the sections in `60-deep-review-and-hardening.md`.

## What the Fast Gate is not

- **Not a clock.** The gate ends when every row and every universal item has a verdict. Time pressure changes which verdict an item gets - `not determined` instead of PASS - and never changes how many items appear.
- **Not a filter on what gets reported.** Every item the trigger table selected appears in `Checked:`, including the ones that passed and the ones you could not settle.
- **Not a substitute for the repository's own contract.** Where the repository, its `AGENTS.md`, or `/alaa-services-contract` states a stricter rule for the same control, apply the stricter one and name it in the report.
