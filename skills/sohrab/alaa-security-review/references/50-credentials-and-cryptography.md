# Credentials, Sessions, And Cryptography

Read when the change touches a token, session, refresh credential, step-up proof, password, signature, HMAC, key, or random value.

Every rule here is written to bind **any** credential system, including one built by a service that has never read this platform's own contracts. What this platform's tokens and trusted headers actually contain, and how its gateway issues, verifies, projects, and strips them, is owned by `/alaa-trust-gateway-auth`.

## Credential verification

- **Algorithm allowlist first.** The accepted algorithm set is a configured allowlist, and a credential whose algorithm is outside it is rejected before any other processing - before the signature check, before claim parsing, before a key lookup. An empty or absent allowlist stops the process at boot. The algorithm is never read from the credential to decide how to verify it.
- **Key family matches algorithm.** A symmetric credential presented to an asymmetric verifier, or the reverse, is rejected by the allowlist. Discovering the mismatch in the key loader is too late and stack-dependent.
- **Issuer resolves through a configured map.** The verifier holds a map from issuer to key source. A credential whose issuer is not a key in that map is rejected before its signature is checked, and the issuer is never used to *locate* a key source at request time.
- **Audience** must name this service, or the credential is rejected.
- **Subject** is present and resolves to a live, enabled principal in this service's own store. A credential for a deleted, disabled, or removed subject fails while its signature is still valid.
- **Expiry** in the past is rejected. **Not-before** and **issued-at** in the future beyond the configured skew are rejected. The skew is one configured number with a stated maximum, used at every verification site.
- **Tenancy assertions** in a credential are subject to the derivation rule in `40-authorization-and-tenancy.md`: whatever a credential says about a tenant is a selection among verified memberships, never a grant.
- **Key identifier** is an opaque value that resolves against a pre-configured key set. Never a URL, a path, a filename, or anything that can trigger a fetch or a filesystem read. An unknown identifier fails closed and makes no outbound request.
- **Key set retrieval**, where a key set is fetched at all: only from pre-configured issuer metadata, cached with a bounded TTL and a bounded refresh rate, and an unexpected change in the key set fails closed rather than adopting the new keys.
- **Rotation** supports overlap: two keys verify during the rotation window, one of which signs. Keys live outside the repository, in the platform's secret mechanism.
- **Failure is uniform.** Every verification failure returns one response shape and one code; the cause goes to the structured log with the request id. `25-browser-trust-and-output.md` owns the response rule.

## Access credential

- **Lifetime** is minutes, configured per environment, and no longer than the revocation staleness bound below.
- **Contents** are the minimum the resource server needs to decide. No personal data, no secret, no free text.
- An access credential whose lifetime exceeds the session it serves, with neither rotation nor a revocation path, is stop-the-line item 12.

## Session continuity

A service whose access credential is shorter than the session it must support issues a refresh credential. A service with none marks this section N/A - and its access-credential lifetime then equals its session lifetime, which fails the lifetime item above unless that session is measured in minutes.

Every rule below applies to every refresh credential that exists.

- **Rotation**: each refresh issues a new credential and invalidates the presented one, in one atomic operation (`40-authorization-and-tenancy.md` owns the atomicity and the concurrent-refresh decision).
- **Server-side storage**: hashed under the high-entropy rule below, keyed by its own identifier, with `replaced_by`, `revoked_at`, `expires_at`, and a family or session identifier recorded.
- **Client-side storage**: never in any store readable by page script. A host-only `Secure`, `HttpOnly`, `SameSite` cookie, or the platform's native secure storage on a device.
- **Reuse of an already-rotated credential is a compromise signal**, not an error: revoke the entire family, require re-authentication, and emit a security event. `/alaa-observability-soc` owns the event's shape.
- Privacy-aware session metadata - a hashed address, a hashed user agent, a device identifier - is retained only where the repository documents the purpose and the retention.

## Revocation

Revocation is the control that bounds a stolen credential's blast radius, so it exists in every service that issues credentials.

Two properties both hold:

1. A **durable** record of the revocation that survives the restart of every cache.
2. A **check on the request path** whose worst-case staleness is a configured number the review reads from configuration and reports.

Where a cache fronts the durable record: a cache miss consults the record, and a cache outage means consulting the record on every request. It never means skipping the check.

Events that revoke: logout, password or credential change, detected reuse, permission or membership change, tenant removal, account disable, and an operator action.

## Public-client flows

A **public client** is a browser application, a mobile application, a desktop application, or anything whose deployed artifact contains no secret its own user cannot read.

- A public client uses Authorization Code with PKCE, method `S256`. `plain` is not accepted. The implicit flow and the resource-owner-password flow are used by no client of any kind.
- Redirect URIs match **exactly** against a registered set: no wildcard, no prefix match, no path-suffix tolerance, no tolerance of an added query parameter.
- `state` is required on every authorization request and bound to the initiating session. `nonce` is required wherever an identity token is issued, and is verified against the value the client sent.
- A resource server enforces scope as least privilege: a scope that admits more than the route needs is a finding at the severity of what the excess reaches.

## Step-up proof mechanics

Purpose scoping, the no-renewal rule, and the relationship to permission checks are owned by `40-authorization-and-tenancy.md`. This section owns the credential handling.

- The proof binds at least: the subject; the tenant or project context where applicable; the purpose; a proof identifier; the issue time; the expiry; the issuer. It is opaque to public clients, and public documentation uses placeholders only.
- The raw second factor - the shared secret, the provisioning URI, a user-entered code, a recovery code - is never logged, persisted outside its intended secure store, cached, serialised into client state, sent to analytics, or included in a crash report.
- Recovery codes are displayed exactly once, stored under the high-entropy hashing rule below, and rejected after use.
- The verification endpoint is rate-limited and lockout-protected, and its limiter store is fail-closed (`40-`).

## Sender-constrained credentials

A pure bearer credential is replayable by anyone who obtains it, which is why short lifetime and revocation above are mandatory rather than advisory: they bound the replay window instead of removing it. Sender-constraining - mTLS-bound credentials or DPoP-style proof of possession - removes it.

Adopt it when one of two preconditions already holds: the platform terminates mTLS at the trust boundary, or the client stack already implements DPoP. Where neither holds, record it as a named future-hardening item together with the precondition that would make it available, and do not report its absence as a finding.

## Constant-time comparison

**Every comparison of a secret-bearing value against an expected value uses the platform's constant-time comparison.** There is no case where the byte-by-byte comparison is needed: the constant-time call costs nothing measurable, and the fast one leaks the matching prefix length to a caller who can time it.

Applies to: session and API credentials, refresh credentials, HMAC and webhook signatures, one-time codes, password-reset and invitation tokens, CSRF tokens, signed-URL signatures, preshared keys, and licence keys.

Per stack: Go `hmac.Equal` or `crypto/subtle.ConstantTimeCompare` - **`bytes.Equal` and `==` are not constant time**; PHP `hash_equals`; Node `crypto.timingSafeEqual`, with lengths checked first because it throws on a mismatch; Python `hmac.compare_digest`; Java `MessageDigest.isEqual`.

Flag: `==`, `!=`, `===`, `strcmp`, `bytes.Equal`, `String.equals`, `Arrays.equals`, a loop that returns on the first differing byte, a comparison of a truncated prefix, and a comparison performed after `trim` or case-folding - which also silently widens the set of accepted values.

**Lookup is part of this rule.** Look a credential up by the full digest of the presented value, which is an indexed single-row read, never by a prefix of the secret and never by a scan. Treat "no row" and "row found but digest mismatch" identically, in the same code path, so the two are indistinguishable in timing and in response.

## Hashing: two different problems

Conflating these two is the most common cryptography defect in this class of service, and the instruction "store refresh tokens hashed like passwords" is the specific error.

**A user-chosen password** has low entropy, so the defence is cost:

- A memory-hard KDF. Argon2id where the stack offers it; bcrypt or scrypt where the repository already uses one.
- Parameters live in configuration and are validated at boot, never hardcoded.
- Parameters are chosen against two numbers the review names: a target verification time band on production hardware, and the peak login rate - verification cost multiplies by login QPS, so a parameter copied from an article either provides too little cost or removes the service at peak.
- A per-record salt from the library's CSPRNG. Never hand-rolled, never global.
- Re-hash on the next successful verification when a stored record's parameters are below the current configuration.
- The accepted password length is bounded so the KDF's work is bounded, and the bound is generous (64 bytes or more). Where bcrypt is in use, its input truncation is handled deliberately rather than discovered.

**A server-generated credential** - refresh credential, API key, invitation or reset token, webhook secret - is not a password:

- At least 128 bits from a CSPRNG.
- Stored as a plain cryptographic digest (SHA-256), or as HMAC-SHA-256 under a server-held pepper key from the secret manager.
- **Not** under a memory-hard KDF. The KDF's cost buys nothing against 128 bits of entropy, and it puts a memory-hard computation on the hot path of every authenticated request - a latency and CPU regression that reads as a security measure.

Never: MD5 or SHA-1 where collision or preimage resistance matters; a fast hash for a user-chosen password; an unsalted password hash; a memory-hard KDF on a per-request verification path; hashing parameters hardcoded in code.

## Signing algorithm ladder

Pick the lowest rung whose condition your deployment actually meets.

1. **One process both signs and verifies, and no other process needs to verify** - HMAC-SHA-256 with a key of at least 256 bits from a CSPRNG. The asymmetric distinction buys nothing when there is one holder.
2. **Verification happens in more than one process, or in a process that must not be able to mint** - asymmetric signing. Ed25519 (EdDSA) first; ECDSA P-256 where a dependency requires it; RSA of at least 2048 bits with PSS where a dependency requires that. **Never distribute a symmetric key to verifiers**: a holder that can verify can mint, so every verifier becomes an issuer.
3. **Never** - `none`; RSA below 2048 bits; MD5- or SHA-1-based signatures; an algorithm selected from the credential; a library default that is not pinned in configuration.

## Randomness

Every credential, salt, nonce, initialisation vector, and unguessable identifier comes from a CSPRNG, with at least 128 bits of entropy for anything that must be unguessable, encoded without shortening.

Per stack: Go `crypto/rand`; PHP `random_bytes` and `random_int`; Node `crypto.randomBytes` and `crypto.randomUUID`; Python `secrets`.

Flag: `rand()`, `mt_rand()`, `math/rand`, `Math.random()`, `random.random()`, `uniqid()`, a timestamp, an incrementing counter used where a value must be unguessable, a UUIDv1, a UUIDv4 from a non-CSPRNG source, and a digest of a timestamp.

## Encryption of data the application holds

- AEAD only: AES-GCM, AES-GCM-SIV, or XChaCha20-Poly1305. Never ECB. Never CBC without a separately verified MAC. Never a mode whose tag the code does not check before using the plaintext.
- A unique nonce per encryption under a given key, from a CSPRNG or from a counter that cannot repeat. Nonce reuse under AES-GCM discloses the authentication key, not merely one plaintext, so it converts a confidentiality bug into a forgery capability.
- Keys come from the secret manager, are versioned, and the version is stored beside the ciphertext so rotation is possible without a full re-encryption outage.
- A key derived from a password uses a KDF with configured parameters, never a bare digest.

## Secrets

- No secret in the repository, in a committed configuration file, in an image layer, in a build argument, or in a CI log. Secrets arrive at runtime from the platform's secret mechanism.
- Every secret has a documented rotation procedure that supports **overlap** - two values valid at once - so rotation needs no downtime. A secret that cannot be rotated without an outage will not be rotated after an incident, which is when it matters.
- **No credential, secret, or token is written to a log, a metric label, a trace attribute, a URL, an error message, a crash report, or an analytics event.** Where correlation is needed, log a stable non-reversible reference: the credential's own identifier claim, its database row id, or a digest under a server-held pepper. Never a truncation of the credential itself - a prefix of a secret is a partial secret.
- A secret found in git history is **rotated**. Deleting the line does not un-disclose it, and the review says so rather than accepting a removal commit as the fix.

## Review checklist for a credential or step-up change

Flag the change when any of these appears. Each is a detection trigger, not a topic to consider.

1. A public client sends a header, field, or claim that the trust boundary is documented to strip from client input.
2. A public client sends a raw second-factor code to any service other than the one that owns the credential.
3. A downstream service accepts step-up metadata without the repository documenting which component strips and verifies it.
4. A step-up proof is renewed, extended, or refreshed without a fresh presentation of the credential.
5. A proof's purpose is absent, generic, derived from a route path, or supplied by the client rather than bound at issue.
6. A proof is accepted for an action other than the one its purpose names.
7. A step-up requirement stands in place of a permission or business authorization check rather than in addition to it.
8. A route gains a forced step-up requirement with no client-visible challenge-and-retry contract, so the client's only signal is an opaque failure.
9. A second-factor secret, provisioning URI, entered code, or recovery code appears in a log, a metric label, a trace attribute, an analytics event, a cached response, a serialised client state, or a crash report.
10. Recovery codes are shown more than once, stored reversibly, or accepted after use.
11. The limiter or lockout store for a credential-verification endpoint is unreachable and the request proceeds.
12. Documentation, an API description, a collection, an SDK, or a test describes a credential flow the route code does not implement - including a feature flag whose documented state differs from the deployed one.
13. A flag that disables a credential feature makes its routes answer as an ordinary missing route, so a client cannot distinguish "disabled" from "wrong URL" and degrades silently.

## Minimum negative tests

Each must fail against the broken implementation it names, and the review lists the ones that apply in the report's `Validation:` section. A test suite that only exercises the success path proves nothing about a verifier.

1. A credential with a bit-flipped signature is rejected.
2. An algorithm outside the allowlist is rejected, including `none` and a symmetric credential presented to an asymmetric verifier.
3. An unknown key identifier is rejected **and the test asserts zero outbound requests were made**.
4. A wrong issuer is rejected; a wrong audience is rejected; each asserted independently.
5. An expiry in the past is rejected; a not-before in the future is rejected; both tested at exactly the configured skew boundary, with the test asserting which side of the boundary passes.
6. A credential valid for tenant A is rejected on a tenant B resource, asserted separately at every layer that claims to enforce it - route middleware, data layer, and the object read. One passing assertion hides two missing layers.
7. A reused refresh credential fails, and the reuse revokes the family; a concurrent double refresh produces the outcome the service decided on.
8. A revoked credential fails within the configured staleness bound, with the cache warm.
9. A credential for a deleted or disabled subject fails.
10. The response for every case above is identical except for the request identifier.
