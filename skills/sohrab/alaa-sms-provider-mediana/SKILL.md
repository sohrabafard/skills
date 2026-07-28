---
name: alaa-sms-provider-mediana
description: "Mediana/IPPanel Edge SMS provider contract for Alaa services: the wire shapes, the canonical +989xxxxxxxxx recipient rendering, and what to do when a send does not come back. Use when implementing, reviewing, debugging or testing an Alaa SMS integration against Mediana/IPPanel — Authorization auth, environment-driven endpoints, webservice and pattern sends, mapping the notification envelope's pattern_values array onto Mediana's params object, voice OTP, peer-to-peer and multipart sends, phonebook, keyword, postal-code, country, geolocation and job targeting, scheduling, cancellation, price calculation, the GET URL send, meta.status and message_code parsing, timeout and ambiguous-send handling, and provider client code. Do not use for Bale Safir sends (alaa-bale-provider), Telegram, email, WhatsApp or push; not for broker, outbox or queue design (alaa-async-messaging); not for retry legality or backoff doctrine (alaa-reliability-sla)."
---

# Alaa SMS Provider — Mediana / IPPanel Edge

## What this skill owns

One vendor: the Mediana/IPPanel Edge send API — its wire shapes, its recipient rendering, its absence of an idempotency key, its own failure classes. Every rule here is scoped to code that builds, sends, parses, or tests a Mediana request. Route the rest; a rule restated here becomes a second strength for a rule that already has an owner.

- Retry legality, backoff, idempotency mechanics, ambiguity doctrine → `/alaa-reliability-sla` (`$alaa-reliability-sla`)
- Timeout and retry-budget values, metric and event names, the notification envelope → `/alaa-services-contract` (`$alaa-services-contract`)
- Queues, workers, outbox rows, DLQ topology, replay → `/alaa-async-messaging` (`$alaa-async-messaging`)
- Secret storage, threat classes, fail-closed doctrine → `/alaa-security-review` (`$alaa-security-review`)
- Bale Safir sends and the Bale wire form → `/alaa-bale-provider` (`$alaa-bale-provider`)
- Log field names, telemetry requirement levels → `/alaa-observability-soc` (`$alaa-observability-soc`)
- Go client structure and context plumbing → `/alaa-golang` (`$alaa-golang`)
- PHP and Laravel provider class shape → `/alaa-php-clean-code` (`$alaa-php-clean-code`)
- Which layer a behaviour is tested at → `/alaa-testing-strategy` (`$alaa-testing-strategy`)
- Model, effort, runtime capability → `/alaa-prompting-guide` (`$alaa-prompting-guide`)

## Router

Every send mode this vendor offers is documented at field level behind one of these rows.

| You are about to | Read |
|---|---|
| Send one SMS to a number list, one approved pattern, a voice OTP, or a different message per recipient group | `references/10-send-contract.md` |
| Let a CSV or XLSX supply the recipients or the per-recipient text | `references/12-multipart-and-file-sends.md` |
| Send to a phonebook, postal-code area, province, operator range, or job category | `references/15-targeting-and-bulk-sends.md` |
| Cancel a scheduled message, quote a price, or call the GET URL send endpoint | `references/18-cancel-price-and-url-send.md` |
| Write a fixture, a curl, a Postman request, or a test that must reject a payload | `references/20-examples-and-rejects.md` |
| Handle a timeout, a refused connection, a non-2xx, or a 200 with `meta.status: false` | `references/30-failure-and-ambiguity.md` |
| Write or review Go here, or reconcile a `/v1` base URL with a `/v1/api` one | `references/40-vendor-contract-clues.md` |
| Turn a user-entered number into a recipient string, or change either normaliser | `references/50-phone-and-conformance.md` |

## The two send modes the fleet commands today

`alaa-services-contract references/27-notification-service-contract.md:88-90` defines two SMS command families: `…sms.send_message.v1` becomes a `webservice` send, `…sms.send_pattern.v1` becomes a `pattern` send. Field lists are in `references/10-send-contract.md`. A mode outside these two needs a product decision before it needs a payload.

Drop `users[].id` and `user.id` when building a payload, because Mediana has no field for them and an unknown key is a payload defect. Correlate outbox ids back to users in your own delivery table.

### Mapping `pattern_values[]` onto `params{}`

The envelope carries `pattern_values` as an **array of `{key, value}` pairs**; Mediana's `params` is a **JSON object**. This is the most defect-prone step in the integration, so it is stated in the body rather than a reference.

- Insert each element into `params` under its own `key`, in array order.
- Reject the command when two elements share a `key`, naming the second index, because object insertion keeps the last write silently and sends text nobody chose.
- Render every `value` as a string first, because Mediana substitutes values as text and a JSON number drops a leading zero, delivering `0458` as `458`.
- Reject the command when local pattern metadata exists and an element names a variable the pattern does not declare. Mediana ignores an undeclared key, so the send succeeds and the intended text never arrives.
- Reject the command when local pattern metadata exists and a declared variable has no element. Mediana renders a missing placeholder as empty, so the recipient gets a message with a hole in it rather than an error.
- Stop and mark `NEEDS_MEDIANA_PATTERN_CONFIRMATION` when no local pattern metadata exists, because a guessed variable name produces a send that is accepted and wrong.
- Array order carries no wire meaning; the vendor substitutes by name. Preserve it only so duplicate reporting can name an index.

## Non-negotiables

- Send `Authorization: <token>` with no scheme prefix. Add `Bearer` only when a committed request fixture in the target repository shows it, and cite that fixture's path and line in the change.
- Read every endpoint from configuration and ship the vendor URL only as a documented default constant, because a hardcoded host cannot be pointed at a sandbox account.
- Decide the base-URL boundary once and assert the final URL in a test. A `/v1` base takes the path `/api/send`, a `/v1/api` base takes `/send`, and mixing the two builds `…/v1/api/api/send`, which 404s in production and nowhere else.
- Produce every recipient string from exactly one normaliser, and pass that normaliser the target channel. Mediana's wire form is `+989xxxxxxxxx` and Bale's is `989xxxxxxxxx`; both render one platform input form, so a shared normaliser that does not take the channel is a defect. An OTP rendered for the wrong channel is rejected by the vendor at best and delivered to the wrong subscriber at worst. The canonical implementation is `scripts/validate_mediana_payload.py --normalize`.
- Keep the token, recipient numbers, OTP values, pattern variable values, and message text out of **logs, traces, exception payloads, screenshots, and final reports** — all five egresses, not logs alone. Mask a recipient as `+9891****0000` and a token as its first four characters followed by `****`, so an engineer can correlate a delivery without holding the subscriber's number.
- Use `POST /api/send` with the token in the `Authorization` header for all authenticated production traffic, never the GET URL send endpoint, because a GET query string writes the credential into access logs, proxy logs, and shell history where nothing rotates it.
- Run a live send only against a dedicated test account, a test sender, and a recipient the user named in this session, because an accepted send cannot be recalled.
- Deduplicate at the envelope's `idempotency_key` and add no second mechanism beside it (`alaa-services-contract references/22-failure-load-and-deprecation-contract.md:152-153`), because the Mediana send API defines no idempotency key of its own.

## The ambiguous send

A timeout after the request bytes were written proves nothing about whether the SMS was sent. A connect refusal proves the opposite — that nothing executed. **Never let those two outcomes share a code path**, because collapsing them is what double-sends an OTP.

This route records `idempotent: false`, so every caller sets its HTTP retry budget to `0` and resolves an ambiguous attempt at the envelope's `idempotency_key` rather than re-issuing the request (`alaa-services-contract references/22-failure-load-and-deprecation-contract.md:149-151`). The four-class table and per-symptom recovery are in `references/30-failure-and-ambiguity.md`; the doctrine is `/alaa-reliability-sla` (`$alaa-reliability-sla`), at `alaa-reliability-sla references/20-retries.md:24,33`.

Emit the `alaa_dependency_*` families from `alaa-services-contract references/24-metric-registry.md:107-110` on every Mediana call, invent no provider-specific family, and label no series with a recipient number or a `message_outbox_id`, because both are unbounded.

## The validator and the required checks

```bash
python3 scripts/validate_mediana_payload.py <payload.json> [--strict]
python3 scripts/validate_mediana_payload.py --normalize '<raw-number>' [--channel mediana|bale]
python3 scripts/validate_mediana_payload.py --self-test
```

| Exit | Meaning | What you must do |
|---|---|---|
| 0 | The requested check passed | Continue |
| 1 | The payload is invalid, `--normalize` rejected the input, or `--self-test` disagreed with the corpus | Fix the payload or the normaliser; do not send |
| 2 | The invocation is wrong | Fix the arguments |
| 3 | The payload file is unreadable or is not JSON | Fix the fixture path or its contents |
| 4 | `scripts/phone-conformance-corpus.json` is missing or its `corpus_sha256` does not match its cases | Reconcile with the `alaa-bale-provider` copy; never edit one copy alone |

Exit 0 proves payload shape and normalisation only; it cannot check a sender approval, a pattern code, a phonebook id, or a geographic id.

Before finishing, run `--self-test`, run the validator over every committed fixture, and add a `pattern_values[] → params{}` test covering a duplicate key, a missing variable, an undeclared variable, and a leading-zero value. The full required-test list is in `references/20-examples-and-rejects.md`.

## When NOT to use this skill

- Not for Bale Safir, Telegram, email, WhatsApp, or push sends; Bale is `/alaa-bale-provider` (`$alaa-bale-provider`).
- Not for IPPanel account management, package purchase, number assignment, or panel reporting. Read a panel value here only when a send payload takes it as a field.
- Not for retry, backoff, breaker, or timeout **values**; this skill names the vendor's failure classes and routes every number to its owner.
