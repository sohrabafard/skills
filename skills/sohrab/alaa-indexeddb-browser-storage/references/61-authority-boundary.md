# The authority boundary

Read this before storing, reading back, or branching on anything touching identity, session, permission or
entitlement.

**One property governs the file: a value read out of browser storage carries no trust.** It was writable by
any script in the origin — including one the attacker injected — and by the user with DevTools open. That
property is `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`) ground; this file states what it means
for a database.

## What is never written here, and what replaces it

| Never written | Positive replacement | Owner |
|---|---|---|
| access, refresh or session token | the SDK attaches the bearer and performs single-flight refresh through the gateway; storage code never sees the token | `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`) |
| decoded JWT claims | re-derive from the current session at the point of use; nothing persists them | `/alaa-trust-gateway-auth` |
| any trusted internal gateway header | the browser sends only the public request headers the SDK and gateway contract allows; the trusted set is injected server-side and its exact composition is the gateway skill's ground, not restated here | `/alaa-trust-gateway-auth` |
| an authorization decision, an entitlement grant, a paid-access truth | ask the server at the point of decision; a `403` is the only authoritative answer | `/alaa-trust-gateway-auth` |
| a permission bitmap, encoded or decoded | see below | `/alaa-permission-generator` (`$alaa-permission-generator`) |
| a payment credential or a private key unlocking a server resource | never client-side | `/alaa-security-review` (`$alaa-security-review`) |

## The permission bitmap

The bitmap's contract and its canonical TypeScript decoder belong to `/alaa-permission-generator`
(`$alaa-permission-generator`); its trust property belongs to `/alaa-trust-gateway-auth`
(`$alaa-trust-gateway-auth`). This skill states three things and no more.

1. **A decoded bitmap is a UI hint and is never an authorization decision.** That is how the `client`
   repository frames it: the snapshot shapes the interface — hide a control, skip a request — and the
   gateway and owning service remain authoritative. A deny response is the only authoritative answer.
2. **Neither the encoded bitmap nor the decoded snapshot is written to IndexedDB.** Persisting it creates a
   value that outlives the session that justified it, on a possibly shared device, readable by any script —
   and one an attacker with write access to the origin's storage can edit to reveal controls that should be
   hidden. The revealed control still fails at the gateway, but the product has disclosed what exists.
3. **Never decode a bitmap in storage code.** A storage path that needs a capability takes the
   already-decoded snapshot as a parameter. A second decoder in this layer is a second implementation of a
   fleet contract, and it will drift.

An example in this pack that persisted or decoded a bitmap would be a boundary violation. None does, and
`scripts/validate_skill_pack.py` fails the pack if one appears.

## What a cached server response may be used for

A value that arrived in a server response body may be cached with a TTL and a server revision, and used
**only to render**. It may not be used to decide.

| Use | Allowed |
|---|---|
| render a cached title while the request is in flight | yes |
| hide a control because a cached snapshot says the capability is absent | yes — it is a hint, and the request still fails closed at the gateway if the hint was wrong |
| **show** protected content because a cached entitlement says the user paid | **no.** Ask the server. |
| skip a call a cached decision says would be denied | yes as an optimisation; the call is still made whenever the user acts on the outcome |
| treat a cached `403` as permanent | no. Revalidate; entitlements change. |

The distinguishing question: **if an attacker replaced this cached value with the opposite one, would the
user gain access to something?** If yes, it is authority and it may not be cached.

## `accountKey`

A storage namespace for cleanup and cache isolation, and nothing else. Its composition in the `client`
repository is in `95-alaa-integration-playbook.md`, and the composed string is a value owned by
`/alaa-services-contract` (`$alaa-services-contract`). Two rules follow: **never read `accountKey` off a
record and use it as the actor for a request** — the actor comes from the session; and **a record whose
`accountKey` does not match the current session is another account's data**, so it is purged, not read
(`62-poisoning-and-purge.md`).

## When a task asks for an exception

There is no self-granted exception on this file. A feature that believes it needs one obtains a review
under `/alaa-security-review` (`$alaa-security-review`) and records in its ADR: what is stored, which
threat the reviewer accepted, and what detects it if that acceptance turns out to be wrong. "Reviewed"
without those three is not a review.
