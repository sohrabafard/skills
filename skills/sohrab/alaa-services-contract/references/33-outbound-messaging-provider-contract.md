# Outbound Messaging Provider Contract

Use this file when a service calls an external messaging provider (an SMS gateway such as Magfa, a messenger such
as Bale Safir) directly: the adapter port, the outcome and failure classes, sender lines, admission order, the AIMD
rate and breaker values with their worked examples, and the Redis keys. Today only `auth` does this; its canonical
design is `docs/notification-latest-plan.md` in the `auth` repository.

What this file does not own:
- **Vendor wire facts** (endpoints, codes, idempotency mechanism, status model) - `/alaa-sms-provider-magfa`,
  `/alaa-bale-provider`, `/alaa-sms-provider-mediana`.
- **Why** a breaker, a rate limit or a deferral exists and how to choose one - `/alaa-reliability-sla`.
- **Internal service-to-service timeouts and retry budget** - `22-failure-load-and-deprecation-contract.md`. A
  provider hop follows this file instead.
- **Redis key rows** - `29-redis-key-registry.md` registers the keys below; this file explains them.
- **Whether a signal is required, and alerts** - `/alaa-observability-soc`.

## Source priority

Every path is relative to the root of the `auth` repository checkout. Trust code first, then docs; report drift.

1. `app/Contracts/Messaging/Sms/SmsProvider.php`, `app/Services/Messaging/Sms/MessageProviderRegistry.php`,
   `app/Services/Messaging/Sms/SmsSenderLineRegistry.php`
2. `app/Services/Messaging/Sms/SmsProviderAdmission.php`, `RedisSmsAccountLimiter.php`, `SmsLimiterScripts.php`,
   `SmsTransportBreaker.php`, `SmsTransportCircuit.php`, `SmsResilienceSettings.php`
3. `config/sms.php`, `.env.example`
4. `docs/data-architecture/85-message-provider-resilience.md`, `docs/ops/sms-magfa-cutover.md`

Facts here were read on 2026-10-20 from `auth` branch `feat/followups-p5-resilience` (D4 of
`docs/_agent_plans/20261020-103000_sms-milestone-followups-design.md`), now merged into `auth` `main`. The Bale
registration, the Bale timeouts and everything about `Retry-After` and the cooldown were re-read at `8fa95e7` on
2026-10-21.

## Adapter port

- One adapter per provider behind one channel-neutral port. A provider registry maps the provider name to its
  adapter; shared code never binds the port to one adapter and never reads a provider's own configuration.
- Registry names: `magfa`, `bale` (both registered: `app/Providers/AppServiceProvider.php:84-86`). Metric `dependency`
  label values: `magfa`, `bale_safir` (`app/Services/Messaging/Sms/Bale/BaleCallObserver.php:24`).
- The adapter only translates: it builds the request, authenticates, parses and classifies. It never retries,
  schedules, picks a line or suppresses, and it never throws for a classified answer or a transport failure.
- Every message carries a durable idempotency key the caller persisted before the first call and reuses on every
  retry. Magfa: the numeric `uid` (delivery id plus the adapter's uid offset). The adapter supplies its own offset
  and its call bound (connect plus read timeout), which sizes the capacity lease (call bound plus 5 s).
- Every result carries an outcome, an error class, the vendor code, a transport signal, a line scope and, per item,
  an opt-out flag.

| Outcome | Meaning | Caller action |
|---|---|---|
| `completed` | A parsed answer with a success status; read the items | Record each item |
| `rejected` | The provider answered and refused the whole request | Act on the error class |
| `not_sent` | The request was never written (DNS, connect, TLS) or was throttled before processing | Retry with the same key inside the attempt budget |
| `ambiguous` | It may have executed: a timeout after the write, a broken or unreadable body, a 5xx | Look the key up; never resend blind |

| Error class | Caller action |
|---|---|
| `transient` | Retry with the same key; for a possibly executed send, look up first (OTP same-code exception: `/alaa-sms-provider-magfa`) |
| `recipient_terminal` | Fail this recipient on this line; an opt-out (Magfa 33) records a suppression for the line |
| `account` | Open the account breaker and alert; never retry |
| `caller_defect` | Fail and alert; never retry |
| `window` | Defer to the allowed window without spending an attempt (at most 3 times) |
| `unknown` | Terminal for the item and alerted; never guessed into a retryable class |

| Transport signal | Set when | Transport breaker | AIMD rate |
|---|---|---|---|
| `answered` | Any HTTP status below 500 except a throttle | success sample | none |
| `throttled` | The provider refused for rate (Magfa and Bale HTTP 429, Bale body code 3) | not counted | halve |
| `failed` | Connect refused or unreachable, DNS or TLS failure, connect or read timeout, broken transfer, HTTP 5xx | failure sample | none |
| `not_called` | A local refusal, or nothing to send | not counted | none |

Line scope marks a rejection that concerns only the sender line (Magfa 20 and 34): the caller opens that line's
breaker, never the account's.

## Sender lines

- Each lane lists its lines in order as `provider:line`: `SMS_OTP_SENDER_LINES` (OTP and security notices),
  `SMS_BULK_SENDER_LINES` (campaigns). An entry without a provider means `magfa`; an entry of an unknown provider
  or a non-numeric line is left out and logged once per process. When a list is empty, the single
  `SMS_OTP_SENDER_LINE` or `SMS_BULK_SENDER_LINE` means `magfa:<line>`.
- A delivery is recorded with its lane's first line. A send tries the recorded line first, then the lane's other
  lines. A line refused by its own breaker leaves the account's other lines in the race; an account that refused is
  not asked again for its other lines. A send moved to another line goes out from it and the delivery records it.
- A line-scoped rejection (Magfa `20` or `34`) on a single-delivery send gives the attempt back and moves the delivery
  to another admitted line of the same provider, once per delivery, and logs `auth.sms.delivery.line_switch_scheduled`.
  With no other admitted line, or after the one switch, the delivery fails as before.
- A line is sent only through its own provider account's credentials.

## Admission order

Before every call: (1) operator pause `{all}:pause`, every provider; (2) the process's transport breaker for the
provider; (3) the account breaker; (4) the line breaker; (5) the account's `Retry-After` cooldown; (6) the account's
AIMD rate and concurrency. A refusal defers the work durably for the remaining lifetime of what refused (a capacity
shortage: at most `SMS_CAPACITY_DEFER_MS`; an unreadable Redis: at least 5 s), never spends an attempt and never fails
the work. An unreadable store admits nothing.

## Values

| Value | Ala value | Key |
|---|---|---|
| Magfa connect / total timeout per call | 3 s / 15 s | `MAGFA_SMS_CONNECT_TIMEOUT_SECONDS`, `MAGFA_SMS_TIMEOUT_SECONDS` |
| Bale connect / total timeout per call | 2 s / 5 s | `BALE_SAFIR_CONNECT_TIMEOUT_SECONDS`, `BALE_SAFIR_TIMEOUT_SECONDS` |
| Attempts per delivery, same key | 3 in total; full-jitter backoff `min(100 ms * 2^(n-1), 2000 ms)` | `sms.delivery.max_attempts` |
| Throttled retry | at least 5 s plus jitter, the rate is halved, and a readable `Retry-After` raises the wait (see `Retry-After on a throttle`) | code |
| `Retry-After` clamp | a hint is clamped to 1 through this maximum, default 60 s; the maximum is read clamped to 1 through 3600 | `SMS_RETRY_AFTER_MAX_SECONDS` |
| AIMD ceiling (starting rate) | 5 req/s for Magfa (`NEEDS_MAGFA_CONFIRMATION`) | `SMS_MAGFA_REQUESTS_PER_SECOND` |
| AIMD floor | 1 req/s | `SMS_AIMD_FLOOR_REQUESTS_PER_SECOND` |
| AIMD decrease | x0.5, at most once per 2 s window | `SMS_AIMD_DECREASE_FACTOR`, `SMS_AIMD_DECREASE_WINDOW_MS` |
| AIMD increase | +1 req/s per 10 s without a throttle, up to the ceiling, computed lazily | `SMS_AIMD_INCREASE_STEP`, `SMS_AIMD_INCREASE_INTERVAL_MS` |
| OTP reserve | `min(configured, max(1, floor(rate / 2)))`; configured 2 | `SMS_MAGFA_OTP_RESERVED_REQUESTS_PER_SECOND` |
| Lane shares per Redis second | OTP `floor(rate)`; campaigns and notices `floor(rate) - reserve` | code |
| Concurrency | 4 per account, 1 reserved for OTP | `SMS_MAGFA_MAX_CONCURRENCY`, `SMS_MAGFA_OTP_RESERVED_CONCURRENCY` |
| Transport breaker window | 30 s, one-second buckets | `SMS_TRANSPORT_BREAKER_WINDOW_SECONDS` |
| Transport breaker trip | at least 10 failures and at least 50% of counted calls | `SMS_TRANSPORT_BREAKER_MIN_FAILURES`, `SMS_TRANSPORT_BREAKER_FAILURE_RATIO` |
| Transport breaker open | 30 s, doubled per failed probe to at most 300 s, each period shortened by up to 20% jitter | `SMS_TRANSPORT_BREAKER_OPEN_SECONDS`, `SMS_TRANSPORT_BREAKER_MAX_OPEN_SECONDS`, `SMS_TRANSPORT_BREAKER_JITTER_RATIO` |
| Half-open probe | 1 call per process; a probe that never reports frees its slot after one first open period | code |
| Account breaker | 300 s, operator-terminal: account-class answers (Magfa 14, 16-19, 22, 29; HTTP 401 or 403) | `SMS_MAGFA_BREAKER_OPEN_SECONDS` |
| Line breaker | 300 s: line-scoped answers (Magfa 20, 34) | `SMS_MAGFA_BREAKER_OPEN_SECONDS` |

Every value is read and clamped at call time; a bad value never throws, at boot or later. Magfa documents no
throttle error code; HTTP 429 is the only throttle signal (`NEEDS_MAGFA_CONFIRMATION`), and codes 15 and 23 stay
transient rejections.

The transport breaker lives in each worker process and is never shared through Redis: one worker's broken egress
must not switch a provider off fleet-wide. On opening it writes only the advisory `{<provider>}:degraded` key for
the open period; nothing reads that key to decide. The rate, the in-flight set and the OTP reserve are scoped to the
provider account, never to a line, because per-line limits would remove the account limit and the reserve.

## Retry-After on a throttle

A provider's `Retry-After` header (delay seconds or an HTTP date) is read only on a throttle: Magfa and Bale HTTP 429,
and Bale body code 3. A header on any other answer, a 503 included, is ignored. A throttle with a readable hint:

1. Clamps the hint to `SMS_RETRY_AFTER_MAX_SECONDS`. A longer wait is an outage and belongs to the account breaker or
   the operator pause.
2. Sets the account-wide cooldown `{<provider>}:cooldown` for the clamped hint, extend-only: concurrent workers can
   lengthen the pause, never shorten it. Admission defers every call of that provider account, after the breakers
   and before the lease, spending no attempt. A cooldown never blocks another provider.
3. Moves the AIMD anchor to the pause end (`anchor_ms` = now plus the pause) and lets the AIMD state live that much
   longer, so the pause is never credited as recovery and the halved rate survives it.
4. Holds the row's retry gate to at least the hint, bounded by the message deadline: `max(backoff, outage floor,
   min(now + clamped hint, deadline))`. The rows of one call share one gate.

An OTP or notice whose cooldown outlasts its deadline falls back to the next provider when it can: its channel ends as
`channel_unavailable`, logged with reason `retry_after_cooldown`. Without a fallback it waits and closes at its
deadline. A pause, a capacity shortage or an unreadable cooldown never ends a channel this way.

### Worked example: rate

Ceiling 5, floor 1, configured OTP reserve 2.

| Time | Event | Rate | Calls/s | Reserve | OTP | Campaigns and notices |
|---|---|---|---|---|---|---|
| before 10:00:00 | none | 5 | 5 | 2 | 5 | 3 |
| 10:00:00 | 429 | 2.5 | 2 | 1 | 2 | 1 |
| 10:00:01 | 429 inside the 2 s window: ignored | 2.5 | 2 | 1 | 2 | 1 |
| 10:00:03 | 429 | 1.25 | 1 | 1 | 1 | 0 |
| 10:00:05 | 429; 0.625 is below the floor | 1 | 1 | 1 | 1 | 0 |
| 10:00:15 / :25 / :35 | 10 s each without a 429 | 2 / 3 / 4 | 2 / 3 / 4 | 1 / 1 / 2 | 2 / 3 / 4 | 1 / 2 / 2 |
| 10:00:45 | back at the ceiling | 5 | 5 | 2 | 5 | 3 |

Proof in `auth`: `tests/Feature/Sms/SmsResilienceLiveTest.php` (live Redis, every step),
`tests/Feature/Sms/SmsRedisLiveTest.php` (the shares at the ceiling).

### Worked example: breaker

Worker W1 loses its route to the provider; W2 and W3 are healthy. Jitter is left out.

| Time | W1 sees | W1's breaker |
|---|---|---|
| 10:01:00-10:01:20 | 6 answers, then 10 read timeouts (10 of 16 calls, 62.5%) | opens 30 s; `{magfa}:degraded` for 30 s; W1 defers its work |
| 10:01:50 | the probe times out | reopens 60 s |
| 10:02:50, 10:04:50, 10:08:50 | each probe fails | 120 s, 240 s, then 300 s (the cap) |
| next probe | an answer | closes; a later opening starts at 30 s |

W2 and W3 count only their own calls and keep sending. Proof in `auth`: `tests/Unit/Sms/SmsTransportBreakerTest.php`,
`tests/Feature/Sms/SmsResilienceEngineTest.php`, `tests/Feature/Sms/SmsResilienceLiveTest.php`.

## Redis keys

All keys start with the service's SMS key prefix (`auth`: `SMS_REDIS_KEY_PREFIX`, default `auth:sms:v1:`) on a
connection no cache store flushes. The braced segment is the provider account's Redis Cluster hash tag.

| Key | Holds | Lifetime |
|---|---|---|
| `{<provider>}:rate:<unix_second>` | per-second request counter | 2 s |
| `{<provider>}:inflight` | sorted set of capacity leases | lease |
| `{<provider>}:aimd` | hash `rate`, `anchor_ms`, `last_cut_ms` | refreshed on write; long enough to climb back to the ceiling |
| `{<provider>}:cooldown` | account `Retry-After` pause, written by the throttle script | the clamped hint, extend-only |
| `{<provider>}:breaker` | account breaker | breaker period |
| `{<provider>}:line:<line>:breaker` | one line's breaker | breaker period |
| `{<provider>}:degraded` | advisory transport-degraded flag | the open period |
| `{all}:pause` | operator pause of every provider | the expiry the operator sets |

## Signals

- Metrics: only the registered `alaa_dependency_requests_total`, `alaa_dependency_request_failures_total`,
  `alaa_dependency_request_duration_seconds` and `alaa_dependency_timeouts_total`, with `dependency=<provider>` and
  `operation` (`send`, `mid`, `statuses`). `outcome=refused` is a call the adapter refused to make. No recipient,
  key, uid or message id is ever a label.
- `auth` log events (`event` plus `code`): `auth.sms.provider.throttled` (`SMS_PROVIDER_THROTTLED`; warning; fires when
  the rate was cut or a hint set or lengthened the cooldown, and stays silent when neither changed; fields `provider`,
  `requests_per_second`, `rate_decreased`, `cooldown` of `set`, `extended` or `unchanged`, and `retry_after_seconds`,
  the whole seconds left of the clamped cooldown, never the raw header),
  `auth.sms.provider.transport_breaker_opened` (`SMS_PROVIDER_TRANSPORT_DEGRADED`),
  `auth.sms.provider.transport_breaker_closed` (`SMS_PROVIDER_TRANSPORT_RECOVERED`), `auth.sms.provider.account_error`
  (`SMS_PROVIDER_ACCOUNT_ERROR`), `auth.sms.provider.line_error` (`SMS_PROVIDER_LINE_ERROR`),
  `auth.sms.lines.entry_ignored` (`SMS_SENDER_LINE_IGNORED`), `auth.sms.lines.unusable` (`SMS_SENDER_LINE_UNUSABLE`),
  `auth.sms.delivery.line_switch_scheduled` (`SMS_DELIVERY_LINE_SWITCH_SCHEDULED`; warning; fields `sms_delivery_id`,
  `kind`, `provider`, `provider_code`, `error_class`), `auth.sms.delivery.queued_expired`
  (`SMS_DELIVERY_QUEUED_EXPIRED`; warning; fields `sms_delivery_id`, `kind`, `provider`),
  `auth.sms.delivery.unclaimed_expired` (`SMS_DELIVERY_UNCLAIMED_EXPIRED`; now also closes fanout and last-in-chain
  deliveries), `auth.sms.delivery.unknown_kind` (`SMS_DELIVERY_UNKNOWN_KIND`; now also written by the claim step and
  by lease recovery), `auth.sms.due_work.stage_failed` (`SMS_DUE_WORK_STAGE_FAILED`; error; fields `stage` of
  `recover_expired_leases`, `never_claimed`, `dispatch_queued`, `dispatch_unknown` or `dispatch_accepted`, and the
  exception class name), `auth.sms.relay.stage_failed` (`SMS_RELAY_STAGE_FAILED`; error; `stage` is
  `campaign_schedule`), `auth.sms.attempt_partitions.ensured` (`SMS_ATTEMPT_PARTITIONS_ENSURED`; info, or warning when
  rows moved or a month failed; fields `created`, `partitions`, `moved_rows`, `failed_months`) and
  `auth.sms.attempt_partitions.ensure_failed` (`SMS_ATTEMPT_PARTITIONS_ENSURE_FAILED`; error; fields `reason`,
  `partition`, `rows`). Every log line written during an OTP, notice or Bale lane job also carries `sms_delivery_id`.
- `auth` TOTP denial events: `auth.totp.admin_reset.denied` (warning; `code` is `TOTP_ADMIN_RESET_FORBIDDEN` for the
  guard reasons `self`, `target_holds_reset_permission`, `multi_project_scope` and `privilege_superset`, and
  `TOTP_RATE_LIMITED` for `quota`; fields `reason`, `actor_user_id`, and `retry_after_seconds` on quota) and
  `auth.totp.enroll.denied` (warning; `TOTP_RATE_LIMITED`, `reason=quota`). Neither carries the target of a reset or
  free text, and `http.path` is the route template. The admin reset audit line keeps the reason, operator and ticket
  out of the application log; they live in the audit row only.

## Conformance check

An adapter conforms when its provider contract suite passes: every documented code to its class, opt-out and line
scope; each wire answer (accepted, throttled, read timeout, connect refused, server error, malformed body, account
and line codes for the whole request) to an outcome, a class and a transport signal; the idempotency key on the
wire; and no phone number, code, key or credential in logs or labels. In `auth` the suite is
`tests/Unit/Sms/Contract/MessageProviderContractTestCase.php`, extended by the Magfa adapter and by the fake the
engine tests use.
