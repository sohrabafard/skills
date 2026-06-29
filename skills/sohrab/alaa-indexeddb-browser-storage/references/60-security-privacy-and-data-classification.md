# Security, privacy, and data classification

## Security model

IndexedDB is same-origin browser storage. Any JavaScript that runs in the origin can generally access that origin's IndexedDB unless the application has created a stronger isolation boundary.

Therefore:

- IndexedDB is not a secure secret store.
- XSS can read/modify IndexedDB.
- Malicious or compromised third-party scripts running in the origin can access it.
- Browser extensions, devtools, local malware, or shared-device users may expose data depending on environment.
- Client-side encryption only helps if keys are not available to attacker-controlled JavaScript.

## Never store

Do not store in IndexedDB:

- access tokens
- refresh tokens
- session secrets
- password-equivalent values
- payment credentials
- private keys that unlock server resources
- entitlement authority or grant truth
- unredacted high-risk PII unless specifically approved
- server signing secrets or API keys

Use server-side sessions, token-mediating backends, HttpOnly/Secure/SameSite cookies, short-lived server-issued URLs, and gateway-side authorization instead.

## Data classification

| Class | Examples | IndexedDB policy |
|---|---|---|
| Public cache | public course list, thumbnails metadata, static config | Allowed with TTL and versioning |
| User-private low risk | UI preferences, last-opened lesson, local filters | Allowed; purge on logout/account switch |
| User-generated unsynced | drafts, pending answers, comments before submit | Allowed with user-visible recovery and sync |
| Analytics/outbox | watch events, UX events, retry queue | Allowed if minimized, bounded, and idempotent |
| PII moderate/high | names, contact info, school info, support content | Minimize, encrypt only with meaningful key model, TTL, purge controls, security review |
| Secrets/credentials | tokens, passwords, session authority | Forbidden |
| Authorization truth | entitlements, paid access grants | Cache display hints only; never authoritative |

## Alaa auth boundary

For Alaa-style architecture:

- Authentication and profile truth belong to server/auth services.
- Gateway/trusted backend path verifies tokens and injects trusted context.
- Client storage may cache display state, but backend remains authoritative.
- Entitlement decisions must be revalidated server-side.
- IndexedDB may store `entitlementSnapshot` only as non-authoritative UX cache with TTL and server revision.

## Token-storage rule

If a task asks “can we put token in IndexedDB?” answer:

```text
No for access/refresh/session tokens. IndexedDB is readable by JavaScript in the origin; XSS turns it into token exfiltration. Use HttpOnly Secure SameSite cookies or a token-mediating backend/session design. Store only non-secret session display metadata if needed.
```

## Logout and account switch

On logout/account switch:

1. Stop sync loops.
2. Flush or discard according to data class.
3. Purge user-scoped stores or records by `accountKey`.
4. Clear in-memory caches.
5. Broadcast `logout-purge` to other tabs.
6. Close/reopen storage connections if needed.
7. Confirm no user-private records remain for the previous account.

Do not delete unsynced drafts silently unless the user explicitly chooses discard or policy says guest data is ephemeral.

## Shared devices

For students, schools, labs, family devices, or public computers:

- Provide “clear local data” controls.
- Purge on logout by default for user-private data.
- Avoid storing sensitive PII offline.
- Keep local previews minimal.
- Consider separate “remember on this device” consent for durable local data.
- Show warning in private/incognito or unmanaged shared-device flows only when user action matters.

## Local encryption

Client-side encryption can help for some local-at-rest threats, but not for XSS if the decryption key is available to JavaScript.

Use encryption only after answering:

- Where is the key generated?
- Where is the key stored?
- Can XSS read the key?
- Can the server recover data?
- What happens on password reset/device loss?
- Is encryption solving a real threat or just adding complexity?

Acceptable patterns:

- User-supplied passphrase not stored locally, for optional private notes.
- Platform-bound credentials/WebAuthn-derived flows after security review.
- Server-encrypted payloads cached locally where client cannot decrypt until authorized.

Do not claim local encryption makes token storage safe.

## Third-party scripts

Because scripts in the origin can access storage:

- Minimize third-party scripts on pages that access sensitive local data.
- Use CSP and Trusted Types where possible.
- Audit analytics/tag managers.
- Avoid giving untrusted scripts same-origin execution.
- Isolate untrusted content in sandboxed/cross-origin iframes.
- Validate all records read from IndexedDB; treat local storage as attacker-modifiable.

## Storage poisoning

IndexedDB data can be stale or maliciously modified.

Protect by:

- Schema-validating records before use.
- Treating cache records as untrusted input.
- Verifying server revisions/signatures when used for important UI.
- Expiring sensitive caches.
- Avoiding direct HTML injection from cached records.
- Keeping a `schema` field in records.

## Privacy and compliance

For user data stored locally:

- Minimize fields.
- Set retention/TTL.
- Provide local deletion controls.
- Include storage in privacy documentation.
- Ensure logout/account deletion clears local data on next app open where feasible.
- Do not log raw local payloads.
- Use bucketed telemetry for sizes and counts.

## Security review checklist

Before approving a new IndexedDB store:

- [ ] Data class identified.
- [ ] Source of truth identified.
- [ ] No tokens/secrets/authority stored.
- [ ] Record schema validated on read.
- [ ] TTL/retention defined.
- [ ] Logout/account-switch purge defined.
- [ ] Quota cleanup policy defined.
- [ ] XSS/third-party script exposure considered.
- [ ] User-visible recovery for unsynced data.
- [ ] Tests cover malicious/stale/old schema records.
