# Request documentation block

Copy this into a request item's `request.description`. Keep all eight headings, in
this order, spelled exactly as written — `scripts/validate_postman_artifacts.py
--require-doc-section` matches the heading line, so a renamed heading reads as a
missing section.

Delete no heading. When a heading has nothing to say for this route, write one
sentence saying so and why (`No permission is required; this route is public at the
gateway.`). An absent heading is indistinguishable from an unanswered question; a
one-line answer is an answer.

Two readers must finish this block able to work without opening the backend
repository: a frontend developer implementing the call, and a security engineer
testing it. The last two headings exist for them and are not optional.

---

## Purpose

One or two sentences: what this route does, and the user-visible or business outcome
it produces. Name the resource in the platform's own words, not the table name.

## Flow position

- What must have happened before this request succeeds, as request names in this
  collection.
- Which variables this request consumes, and which request populates each one.
- Which variables this request's post-response script writes, and which later
  requests read them.
- Whether the effect is synchronous or queued, and where the caller observes
  completion when it is queued.

## Request

- Method and the full public path, with each path parameter's meaning.
- Required headers, and which of them the caller must not send because the gateway
  injects them.
- Every query parameter: type, required or optional, default, allowed values, bounds.
- Every body field: type, required / optional / nullable, format, bounds, enum
  values, and any conditional or mutually exclusive rule.
- Content type, and the request body size limit when one applies.

## Response

- The success status, and any second success status this route can return.
- The response envelope and the fields inside it that the caller reads, with types.
- Response headers the caller must read, such as location, retry, idempotency, ETag,
  or rate-limit headers.
- Pagination fields and cursor semantics for a collection response.
- What an empty result looks like, distinguished from an error.

## Access

- Auth mode at the boundary the caller actually uses.
- The exact permission or scope name required, or an explicit statement that none is.
- The tenancy or project scoping applied, and which identifier decides it.
- Whether a step-up or second factor is required.

## Errors

One row per status this route can actually return. Enumerate them from the
validation rules, the authorization gates, the dependency calls, and the platform's
documented code list — never from a generic 4xx guess.

| Status | Code | When it happens | Caller does |
|---|---|---|---|
| `422` | `EXAMPLE_FIELD_INVALID` | one named validation rule failed | fix the field and resend |
| `403` | `EXAMPLE_FORBIDDEN` | caller lacks the named permission | do not retry |
| `503` | `DEPENDENCY_UNAVAILABLE` | a named dependency is down | retry per the retry rule |

Every row here has a matching saved example on this request. A row without one is an
unproven claim.

## Frontend notes

- The loading, empty, and error states this response forces the UI to have.
- Which field to key a list on, and which field to render as the label.
- Idempotency: whether a double submit is safe, and which key makes it safe.
- Caching and invalidation: what a successful write makes stale.
- Anything about this route that would otherwise be discovered by trial and error.

## Security notes

- The isolation this route depends on, and the identifier that enforces it, so a
  cross-tenant or cross-project attempt can be constructed.
- Which headers are trusted and stripped at the gateway, so spoofing them is a test
  case rather than a surprise.
- IDOR / BOLA surface: which identifiers in the request address another actor's data.
- Rate limits and lockouts that apply, and the observable that proves they fired.
- Values that must never appear in a log, a screenshot, or a bug report.
- Replay and expiry behaviour for any token, code, or signed URL this route accepts.
