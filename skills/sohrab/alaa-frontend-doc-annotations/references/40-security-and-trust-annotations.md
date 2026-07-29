# Security and trust annotations

Read this when a comment names who is authorized, what the gateway sends, where a secret lives, or what the
server re-checks.

**A stale security annotation is worse than none.** An absent comment leaves the next agent to read the
code. A comment that says "the server re-checks every mutation" and is no longer true tells the next agent
to stop reading, and they stop reading at exactly the place where reading mattered. This is the whole reason
this class of annotation carries a machine-checked date and no other class does.

## What may be asserted, and who owns it

This skill owns the *shape* of the sentence and its *expiry*. It owns none of the facts.

| The comment asserts | The owner of that fact |
|---|---|
| A threat class, a sanitiser, a fail-closed rule, CSP, cookie policy | `/alaa-security-review` (`$alaa-security-review`) |
| What the gateway strips, injects or verifies; which header is trusted and where trust begins | `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`) |
| The permission bitmap encoding, its ids, and the canonical decoder | `/alaa-permission-generator` (`$alaa-permission-generator`) |
| That a client-side permission check is a UI hint and never an authorization decision | `/alaa-vue-typescript-clean-code` (`$alaa-vue-typescript-clean-code`), `references/72-frontend-security-binding.md` |
| A header name, claim key, route or status string | `/alaa-services-contract` (`$alaa-services-contract`) |

An annotation asserting a fact from this table without naming its owner is a finding of the pass. The owner
name is what a future agent uses to re-verify; a claim with no owner cannot be re-verified, only believed.

## The two prefixes and their required fields

- `AUTH NOTE:` — who is authenticated, what identity is assumed, which auth flow produced it.
- `SECURITY NOTE:` — what is trusted, what is not, what the server re-checks, where a secret lives.

**Both carry `verified:<ISO-date>` in the same block.** The date is the day a human or an agent checked the
assertion against the owner named in it. It is not the day the comment was written, and it is never
advanced without re-verification. The checker asserts the field as `ANN301` and its staleness as `ANN302`.

The full shape:

```
<PREFIX> <the assertion, one sentence, stating what is NOT guaranteed as well as what is>
owner: <the skill that owns the fact>
verified:<YYYY-MM-DD>
```

## A comment never restates a cross-service value

**A comment asserting a cross-service fact cites `/alaa-services-contract` (`$alaa-services-contract`) as
the source of that value rather than restating the value inline.**

This closes the invalidation problem that otherwise has no owner. A comment in the frontend that says "the
gateway sends `X-Alaa-Tenant`" can become false without the annotated file changing at all — the header is
renamed in a different repository, `ANN302` never fires because git never touched this file, and the comment
outlives the fact. Citing the contract instead of the value converts the invalidation into an existing
owner's existing responsibility: when the contract changes, the contract owner's consumers are already the
thing that must be reviewed.

Not this:

```ts
// AUTH NOTE: the gateway injects X-Alaa-Tenant and strips any client copy. verified:2026-07-28
```

This:

```ts
// AUTH NOTE: tenant identity comes from the gateway's injected header, never from a client-supplied
// value; the header name and strip rule are the contract's, not this file's.
// owner: /alaa-services-contract ($alaa-services-contract) and
// /alaa-trust-gateway-auth ($alaa-trust-gateway-auth)
// verified:2026-07-28
```

The second survives a header rename. The first is a lie the moment the rename lands, and nothing detects it.

## Worked example: the `client` permission bitmap

This is the live case that motivates the whole class, verified in the repository on 2026-07-28.

`packages/sdk-auth/src/authorization/decode-unverified-ui-authorization.ts` decodes a permission bitmap
from an access token, capped at `MAX_BITMAP_BYTES = 512` (4096 ids). Its docblock says, in prose:

```
 * SECURITY: this function never verifies the token signature and must never
 * gate a security decision. It reads only `prm`, `prv`, and `av`, returns no
 * raw token and no raw claims, logs nothing, and fails closed [...]
```

`src/stores/authPermissions.ts` repeats the assertion in its own words: "every value here is an
**unverified UI hint** [...] The gateway and the owning service remain authoritative, and a deny response is
the only authoritative answer."

**Both are correct today, and both are unprotected.** The prefix is `SECURITY:`, not `SECURITY NOTE:`, so
it is outside the closed set and `grep -rn "SECURITY NOTE:"` does not find it. Neither carries a
`verified:` field, so `ANN301` has nothing to check and `ANN302` cannot compare a date to the file's last
commit — which was `2026-07-19T13:51:46+03:30` for the decoder and `2026-07-19T18:43:51+03:30` for the
store. If the Laravel side ever stopped re-checking a mutation, both comments would keep reading as
reassurance, indefinitely, and no tool in the repository would say a word.

The annotation the pass writes:

```ts
/**
 * SECURITY NOTE: the permission bitmap decoded here is an unverified UI hint, never an authorization
 * decision. The signature is not checked; the owning service re-checks every mutation and a deny response
 * is the only authoritative answer. Malformed input fails closed to zero permissions, and an empty bitmap
 * on a valid token is a legitimate ready state.
 * owner: /alaa-permission-generator ($alaa-permission-generator) for the encoding;
 *        /alaa-trust-gateway-auth ($alaa-trust-gateway-auth) for the re-check guarantee
 * verified:2026-07-28
 */
```

What changed: the prefix joins the closed set so the assertion is greppable; the guarantee names the party
that provides it; and the date makes the next commit to this file fail `ANN302` until someone re-verifies
that the server still re-checks. The `512` cap stays where it already is — a `/** ... */` on
`MAX_BITMAP_BYTES` — because it is a local constant, not a cross-service value.

## What an annotation must never contain

- A secret, a token, a key, a sample JWT, or an example value that would be valid if pasted.
- A path to a secret store that is not already public in the repository's configuration.
- A description of a bypass, a disabled check, or a known-vulnerable path. That is a defect report to the
  owner, not a comment in the file that would tell an attacker where to look.
- A claim that something "is secure". State what is checked, by whom, and what is not checked.
