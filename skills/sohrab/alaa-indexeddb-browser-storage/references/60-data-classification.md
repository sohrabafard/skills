# Data classification and shared devices

The question this file answers: **may this specific field be written to a browser database at all?**

The security model is one sentence and it drives every row: **any script executing in the origin reads this
database** — including an injected script, a compromised third-party tag, and an extension with host
access. Encryption helps only when the key is not reachable by that same script.

## The class table

`assets/data-classification-policy.yaml` is the machine-readable form and is what
`scripts/validate_skill_pack.py` checks. This table and that file must agree; the check fails if they do
not.

| Class | Examples | May it be written to IndexedDB | Owner of the harder question |
|---|---|---|---|
| `public_cache` | public course list, thumbnail metadata, static config | yes, with a TTL and a schema version | — |
| `user_private_low_risk` | UI preferences, last-opened lesson, local filters | yes; purged on logout and account switch | — |
| `user_generated_unsynced` | draft comment, draft ticket, unsubmitted answers | yes, with a user-visible recovery path; never silently deleted | — |
| `analytics_outbox` | watch events, UX telemetry awaiting flush | yes, minimised, bounded by count and bytes, idempotent | `71-browser-outbox.md` |
| `pii_moderate_high` | names, contact details, school identifiers, support content | **not by default.** A feature requiring it obtains a review under `/alaa-security-review` (`$alaa-security-review`) and records in its ADR where the key is generated, where it is stored, and whether JavaScript in the origin can read it | `/alaa-security-review` |
| `secret_or_credential` | access token, refresh token, session secret, decoded JWT claim, payment credential, private key | **never** | `/alaa-trust-gateway-auth` |
| `trusted_gateway_context` | `X-Project-Id`, `X-User-Id`, `X-Access`, `X-Authz-*` and every other trusted internal header | **never as client-authored data**; a value that arrived in a server response body may be cached as a display hint with a TTL | `/alaa-trust-gateway-auth` |
| `authorization_truth` | permission bitmap, entitlement, paid-access grant, authorization decision | **never as authority**; the bitmap rules are `61-authority-boundary.md` | `/alaa-permission-generator`, `/alaa-trust-gateway-auth` |

This file decides *whether*. `61-authority-boundary.md` decides *what a stored value may be used for*.
`62-poisoning-and-purge.md` decides *what happens on the way in and on the way out*.

## The one-line answer to "can we put the token in IndexedDB?"

> No. Not the access token, not the refresh token, not the session token, not a decoded JWT claim.
> IndexedDB is readable by every script in the origin, so storing one there turns a single XSS into token
> exfiltration and account takeover. Token attachment and refresh belong to the SDK and the gateway —
> `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`). Store only non-secret session display metadata,
> such as a display name, if the UI needs it before the first API response.

## Shared devices

Students, schools, labs, family devices, public computers. The device is shared; the storage is not
partitioned by human.

- **Purge user-private data on logout by default.** The user does not opt in to a purge; they opt in to
  retention. `62-poisoning-and-purge.md`.
- **A "keep my work on this device" affordance is separate consent**, per feature, recorded in a record the
  purge respects. Absent that consent, the purge takes the data.
- **Do not store `pii_moderate_high` offline on a device the product knows is shared.** If the product
  cannot know, treat every device as shared and the rule holds everywhere.
- **Keep local previews minimal.** A cached thumbnail of another student's submission is that student's
  data on a stranger's device.
- **Show a notice only where the user is about to rely on persistence** — before a download, before offline
  mode. A notice on every page trains the user to ignore it.

## Local encryption

Encryption at rest in the browser defends against a reader of the disk, not against script in the origin.
Answer all six in the feature's ADR before proposing it: where is the key generated; where is it stored;
**can script in this origin read it** — if yes the encryption defends against nothing this product faces;
can the server recover the data if the key is lost; what happens on password reset and device loss; which
named threat does this close.

Two shapes are acceptable: a user-supplied passphrase never stored on the device, for optional private
notes; and a payload the server encrypted, cached locally, undecryptable by the client until authorized.
Anything else needs the review above. **Encryption never makes token storage acceptable** — the key is
reachable by the same script that would read the token.

## Privacy and retention

Store the minimum field set; a cached DTO with fields no view reads is retained risk for no benefit. Every
record carries a retention rule — a TTL, a count cap, or an explicit "until the user deletes it". Local
storage is part of the product's privacy documentation. Never log a raw record payload; sizes and counts go
to telemetry bucketed, at the level `/alaa-observability-soc` (`$alaa-observability-soc`) sets.
