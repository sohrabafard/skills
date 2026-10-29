# Redis Key Registry

This file binds the fleet values into the Redis key shape, sets the per-service ACL key pattern, and holds the
registry of key templates. A service that must read, clear, or avoid another service's keys reads this
registry instead of that service's code.

What this file does not own:
- **The key shape and cache design** - the shape `{app}:{env}:{tenant}:{resource}:{id}:{version}`, tenant
  isolation, TTL choice, invalidation, stampede control, locks, limiters, and behaviour while Redis is down -
  are `/alaa-data-layer` (`$alaa-data-layer` in Codex) `references/40-redis-verification-and-anti-patterns.md`;
  connection and logical-database separation is its `references/50-redis-laravel-octane.md`.
- **The `project_id` value form** - `25-end-to-end-flow-and-boundaries.md`, `Canonical project_id form`.
- **The Redis endpoint** - `15-deployment-and-runtime-contract.md`; **the Redis command timeout** -
  `22-failure-load-and-deprecation-contract.md`; **creating ACL users, TLS, and memory policy** - the deploy
  repository.

## Fleet bindings of the shape

```text
{app}:{env}:{tenant}:{resource}:{id}:{version}
```

- `{app}` is the canonical service identity from `10-core-service-contract.md`, byte for byte (`comment`, not
  the repository name `comment-service`; `projector`, not `entitlement-projector`). A hyphen stays a hyphen.
- `{env}` is the service's `APP_ENV` value (`15-deployment-and-runtime-contract.md`), unchanged.
- `{tenant}` is the canonical `project_id`. A key not scoped to a project omits the segment.
- `{id}` may span several `:`-separated segments; `{version}` is `v<major>` and comes last.
- Literal segments are lowercase; words inside one segment join with `-` (`explain-object`). No `{}` hash tag, except as the next bullet allows.
- **Hash-tag exception (owner-approved).** Keys that one multi-key atomic operation (a Lua script or `MULTI`) uses
  together, including a key the script derives from a declared one, share one Redis Cluster hash tag such as
  `{magfa}`. Redis Cluster runs a multi-key script only when all its keys hash to one slot; without the tag the script
  fails with `CROSSSLOT`, the limiter becomes unreadable and SMS sending stops. A key no multi-key operation touches
  with another carries no `{}`.
- A template writes each variable segment as a `<snake_case>` placeholder.

Cache entries live in database 0 of the shared Redis. Sessions, queues, locks, and limiters use a separate
logical database or instance, per `/alaa-data-layer` `50-redis-laravel-octane.md`.

Register templates, not keys:

```text
key written:         content:production:<a project_id>:course:12:v1
template registered: content:<env>:<project_id>:course:<course_id>:v1
```

## Key rules

- **No PII or secret.** A key never holds a value the never-log list in
  `21-alaa-platform-observability-directive.md` names, a session identifier, or PII such as a mobile
  number or email address, in clear or as a digest an attacker can reverse by enumerating inputs. Keys
  appear in `MONITOR`, slow logs, and memory dumps.
- **Explicit TTL.** Every key is written with a positive TTL, and its registry row states it.
- **Register before use.** Add the template to the registry in the same change that first writes it. A key
  whose template is not registered is a defect in the writing service.
- **ACL.** When the Redis requires AUTH, each service connects as its own Redis ACL user whose key pattern is
  exactly `~<app>:*`; without AUTH no credentials are sent. No service user holds `~*` or `allkeys`. The trailing `:` is required: `~auth*` would also match `authz-sidecar:` keys.

Observable that decides compliance: every Redis client call site writes a key built from a registered
template, under `<app>:<env>:`, with a TTL argument; cache keys sit in database 0.


## Registry

Status: `live` is in code and conforms; `planned` is an accepted design not yet in code; `gap` is live and
non-conforming, with the conforming target. Only the `authz-sidecar` keys conform. Inventory read from working
trees on 2026-10-10; `authz-sidecar` rows re-read at `ac89ce0` (CACHE-1 P5) and at `c7f5286` (kid segment); the `auth:sms:v1:` and
`auth:totp:` rows re-read at `auth` `8fa95e7` on 2026-10-21 (Phases 5 to 8 are merged into `auth` `main`).

### Effective prefix per Laravel service

Laravel writes `<REDIS_PREFIX><cache prefix><key>` with no separator added (`RedisStore::setPrefix`). Target
for every row: the cache store on database 0 with an effective prefix of `<app>:<env>:`; other concerns on
their own logical database or instance.

| Service | Cache DB default | `REDIS_PREFIX` | Cache prefix | Prometheus storage prefix |
|---|---|---|---|---|
| `auth` | 1 (`config/database.php:147`) | `auth_database_` (`:126`) | `auth_cache_` (`config/cache.php:138`); store `file` in `.env.example:205` | `prometheus_auth_`, DB 1 (`config/observability.php:70-71`) |
| `content` | 1 (`config/database.php:194`) | `content_` (`.env.example:280`) | `content` (`.env.example:258`) | `PROMETHEUS_content_` (`config/observability.php:72`) |
| `comment` | 1 (`config/database.php:216`) | `comment_` (`.env.example:300`) | `comment` (`.env.example:277`) | `comment_prometheus_` (`config/observability.php:66`) |
| `notification` | 1 (`config/database.php:178`) | `notification-database-` (`.env.example:64`) | `notification-cache-` (`.env.example:38`) | `<service_name>:prometheus:` (`config/observability.php:56`) |
| `vod` | not read | empty (`.env.example:62`) | `vod_cache` (`.env.example:55`); sessions on Redis (`:49`) | `vod_prometheus_` (`config/observability.php:36`) |
| `assessment-service` | 1 (`config/database.php:100`) | `assessment-service-database-` (`:79`) | store `array` (`.env.example:23`) | not read |

### Key templates

| Current template | Source | Purpose | TTL | Invalidation | Status and target |
|---|---|---|---|---|---|
| `entitlement:explain-object:v1:<project_id>:<project_version>:<request_hash>` | entitlement-api `internal/domain/explain/service.go:29,102` | Explain-object result | `EXPLAIN_CACHE_TTL` 60 s; empty result `EXPLAIN_NEGATIVE_CACHE_TTL` 15 s (`internal/config/config.go:24-25`) | None in code; keys embed the project version | gap: `entitlement-api:<env>:<project_id>:explain-object:<project_version>:<request_hash>:v1` |
| `entitlement:explain-user:v1:<project_id>:<project_version>:<request_hash>` | same file `:30,151` | Explain-user result | as above | as above | gap: `entitlement-api:<env>:<project_id>:explain-user:<project_version>:<request_hash>:v1` |
| `entitlement:effective:v1:<project_id>:<project_version>:<scope>:<subject_hash>:<registry_version>:<enumeration_basis>:<filter_hash>:<limit>:<cursor_part>` | entitlement-api `internal/effectiveaccess/service.go:349-358` | Effective-access page | min(`EFFECTIVE_ACCESS_CACHE_TTL` 60 s, cursor expiry, next validity boundary) (`:360-373`) | As above | gap: `entitlement-api:<env>:<project_id>:effective:<project_version>:...:v1` |
| `news:corpus:v2:<project_id>:<corpus_version>` | news `internal/infrastructure/rediscache/corpus.go:183-184` | Published corpus | `NEWS_CORPUS_CACHE_TTL`, default 15 s (`corpus.go:69-70`) | Version shard bump | gap: `news:<env>:<project_id>:corpus:<corpus_version>:v2` |
| `news:corpus:s<shard>:version` | news `internal/application/port/ports.go:51-60` | Corpus version counter, 16 shards | none: persistent by kit design | `INCR` post-commit on every write | gap: no TTL; target `news:<env>:corpus:s<shard>:version` (the kit requires the `:version` suffix, alaa-go-chi `rediskit/invalidator.go:23`) |
| `news:unread:<project_id>:<user_id>` | news `internal/application/port/ports.go:22-27` | Viewer unread count | 30 s | Deleted on the viewer's read (`command/view.go:64`) | gap: `news:<env>:<project_id>:unread:<user_id>:v1` |
| `verify-sms-<project_int>:<mobile>` and its sibling `verify-sms-<project_int>:<mobile>:generation` | auth `app/Services/Auth/OtpKeyspace.php:16-24` (prefix `auth.tokens.otp_cache_prefix`, `:26-29`) | OTP code (the bare code, kept readable by the previous release during a rolling deploy) and the generation that identifies the challenge for its SMS delivery | `otp_ttl_seconds`, default 120 s, minimum 10 (`OtpKeyspace.php:38-41`); both keys share it | `OtpService::forget()` deletes both (`app/Services/Auth/OtpService.php:244-247`); `discard()` deletes both only while the generation still matches (`:122`) | gap: mobile in clear, integer project id; target `auth:<env>:<project_id>:otp-code:<mobile_digest>:v1` and `...:otp-generation:<mobile_digest>:v1` |
| `auth:sms:v1:{magfa}:rate:<unix_second>` | auth `app/Services/Messaging/Sms/SmsLimiterScripts.php` (derived inside the admission script from the declared `{magfa}:rate` base); prefix `SMS_REDIS_KEY_PREFIX` | Per-second provider request counter of the Magfa account | 2 s (`PEXPIRE` in the script) | TTL | gap: no `<env>`; the `{magfa}` account hash tag is the owner-approved exception in `Fleet bindings of the shape`, because the script derives this key and must stay in one Cluster slot; Bale's keys are the same with `{bale}`; `33-outbound-messaging-provider-contract.md` owns the semantics |
| `auth:sms:v1:{magfa}:inflight` | same script | Sorted set of in-flight capacity leases (account concurrency) | Lease: the adapter's call bound plus 5 s; the set expires one second after its newest lease | `ZREM` on release, `ZREMRANGEBYSCORE` of expired leases | gap, as above |
| `auth:sms:v1:{magfa}:aimd` | same script; `app/Services/Messaging/Sms/RedisSmsAccountLimiter.php` | AIMD state of the account: `rate`, `anchor_ms`, `last_cut_ms` | Refreshed on every write; long enough to climb from the floor back to the ceiling | TTL; a missing hash means the ceiling | gap, as above |
| `auth:sms:v1:{magfa}:cooldown` | `SmsLimiterScripts.php:115-148` (the THROTTLE script writes it); read by `RedisSmsAccountLimiter.php:164-168` | Account-wide pause set by a throttle that carried a readable `Retry-After` hint (Magfa and Bale HTTP 429, Bale body code 3); admission defers while it runs | The hint, clamped to `SMS_RETRY_AFTER_MAX_SECONDS` (default 60, read clamped to 1..3600) (`SmsRetryTiming.php:84-87,165-172`). Extend-only: `PSETEX` when the key is absent or has less time left, never shortened (`SmsLimiterScripts.php:126-136`); a key without expiry is left alone | TTL, or an operator `DEL` | gap, as above |
| `auth:sms:v1:{magfa}:breaker` | `RedisSmsAccountLimiter.php` | Account breaker (account-class answers, operator) | `SMS_MAGFA_BREAKER_OPEN_SECONDS`, default 300 s | TTL, or an operator `DEL` | gap, as above |
| `auth:sms:v1:{magfa}:line:<line>:breaker` | `RedisSmsAccountLimiter.php` | One sender line's breaker (Magfa 20 and 34) | `SMS_MAGFA_BREAKER_OPEN_SECONDS`, default 300 s | TTL, or an operator `DEL` | gap, as above |
| `auth:sms:v1:{magfa}:degraded` | `RedisSmsAccountLimiter.php`, written by a worker's transport breaker | Advisory: at least one worker sees the provider as unreachable; nothing reads it to decide | The breaker's open period | TTL | gap, as above |
| `auth:sms:v1:{all}:pause` | `RedisSmsAccountLimiter.php`; written by an operator (`auth` `docs/ops/sms-magfa-cutover.md`, Pause and rollback) | Operator pause of every provider | The expiry the operator sets; without one it holds until deleted | Operator `DEL` or TTL | gap: no `<env>`; `{all}` hash tag, though no multi-key operation touches it with another key (it is read alone, `RedisSmsAccountLimiter.php:219-223`) |
| `auth:sms:v1:bale:not_user:<sha256(project id:mobile)>` | auth `app/Services/Messaging/Sms/RedisNotBaleUserMemo.php` | Memo that a recipient has no Bale account; the Bale lane skips that recipient. The key holds a hash, never the number; a Redis failure is logged and reads as not remembered | 7 days (`TTL_SECONDS`, owner decision 2026-10-20) | TTL | gap: no `<env>`, as the other `auth:sms:v1:` keys |
| `auth:sensitive-attempts:v1:auth:otp:verify:<ip>:<sha256_16>`, `...:v1:auth:refresh:<ip>:<sha256_16>` | auth `app/Providers/AppServiceProvider.php:58`; `app/Http/Controllers/Api/Auth/AuthController.php:267-301` | OTP-verify and refresh attempt limiter | Window: OTP verify 300 s, refresh 60 s (`PEXPIREAT`) | Window expiry; release by owner | gap: no `<env>`; raw IP (see Open decisions); truncated unkeyed hash of a mobile number; a limiter belongs off the cache database |
| `auth:otp:request:<ip>:<sha256_16>` | auth `AuthController.php:112-123,267-271` | OTP-request limiter (Laravel `RateLimiter`) | 300 s | Window expiry | gap, as above; on Redis only where `CACHE_STORE=redis` |
| `auth:totp:step-up:<user_id>:<project_int>:<purpose>` | auth `app/Support/Auth/TotpStepUpProofStore.php:130-133,145-148` (prefix `AUTH_TOTP_STEP_UP_CACHE_PREFIX`, `config/auth.php:105`) | Local step-up proof that `require_totp` reads; the value is the id of the credential that issued it | `AUTH_TOTP_STEP_UP_TTL_SECONDS`, default 300 s, minimum 30 (`config/auth.php:104`; `app/Services/Security/TotpStepUpService.php:55`) | TTL, or `forgetAllForUser` after a disable or reset (`TotpService.php:199`; `TotpResetService.php:90-92`) | gap: integer project id; target `auth:<env>:<project_id>:totp-step-up:<user_id>:<purpose>:v1` |
| `auth:totp:step-up:proof:<jti>` | `TotpStepUpProofStore.php:38-58,135-138` | Binds a gateway proof token (`<jti>`, a random lowercase UUID, which the gateway injects as `X-TOTP-PROOF-ID`) to the credential that issued it; the value is the credential id; written only when proof-token issuance is on | The proof's expiry, as above | TTL, or `forgetAllForUser` | gap: no `<env>`; target `auth:<env>:totp-step-up-proof:<jti>:v1` |
| `auth:totp:step-up-index:<user_id>` | `TotpStepUpProofStore.php:53-54,140-143` | The user's list of the two proof key kinds above, so a disable or reset forgets all of them in every project and purpose | The newest proof's expiry, refreshed by each issue | `forgetAllForUser` removes it with the keys it lists; otherwise TTL | gap: no `<env>`; raw numeric user id (see Open decisions); target `auth:<env>:totp-step-up-index:<user_id>:v1` |
| `auth:totp:attempts:quota:enroll:<user_id>`, `auth:totp:attempts:quota:admin_reset:<user_id>` (`<user_id>` of the admin for the reset) | auth `app/Support/Auth/TotpAttemptLimiter.php:22,64-71,120-126` (prefix `AUTH_TOTP_ATTEMPT_RATE_LIMIT_PREFIX`, `config/auth.php:114`) | Hourly quota of enrolment calls (all outcomes) and of admin TOTP reset calls, counted by Laravel `RateLimiter` with its `:timer` sibling | 3600 s window; limit `AUTH_TOTP_ENROLL_MAX_PER_HOUR` default 5 (clamped 1..100) and `AUTH_TOTP_ADMIN_RESET_MAX_PER_HOUR` default 10 (clamped 1..1000) (`TotpAttemptLimiter.php:131-138`) | Window expiry | gap: no `<env>`; raw numeric user id; a limiter belongs off the cache database; target `auth:<env>:totp-quota:<action>:<user_id>:v1` |
| `auth:totp:attempts:<project_id>:<user_id>:<action>:<sha256_16>` (`<sha256_16>` is the first 16 hex characters of the client IP's SHA-256) | `TotpAttemptLimiter.php:95-104` | Failed TOTP attempt limiter per user, action and client address | `AUTH_TOTP_ATTEMPT_RATE_LIMIT_DECAY_SECONDS`, default 300 s; `AUTH_TOTP_ATTEMPT_RATE_LIMIT_MAX_ATTEMPTS`, default 5 (`config/auth.php:112-113`) | Window expiry; cleared on success (`TotpAttemptLimiter.php:49-52`) | gap: no `<env>`; unkeyed truncated IP hash; a limiter belongs off the cache database |
| `auth.profile.catalogs.v3`, `available-bank-gateway-urls` | auth `app/Repositories/Profile/EloquentAcademicProfileReadRepository.php:46`; `app/Helpers/helpers.php:189` | Catalog and gateway lists | `CACHE_600`, `CACHE_1`, both default 0 (`config/constants.php:550,556`) | TTL | gap: `auth:<env>:profile-catalogs:v3`, `auth:<env>:bank-gateway-urls:v1` |
| `content:rating-aggregation:active` | content `app/Support/Content/Ratings/RatingAggregationDispatcher.php:35` | Aggregation lease | `ratings.aggregation.lease_seconds`, default 120 s (`:105-108`) | Owner forgets it (`:100-101`) | gap: `content:<env>:rating-aggregation-lease:v1`, off the cache database (a lock) |
| `comment-service:settings` | comment-service `app/Services/SettingsService.php:11` | Settings | none (`rememberForever`, `app/Repositories/CachedSettingsRepository.php:19`) | Forget on save (`app/Models/Setting.php:39`) | gap: no TTL; target `comment:<env>:settings:v<major>`, global |
| `show:lang:<locale>:id:<user_id>`, tag `users` | notification `app/Models/Base/BaseModel.php:55`; `app/Repositories/Base/BaseCacheRepository.php:21-27` | User by id | 86400 s (`BaseModel.php:35`) | Tag flush on write (`app/Services/User/UserService.php:37,43,58`) | gap: `notification:<env>:user:<user_id>:<locale>:v1` |
| Laravel named limiters `md5(<name><by>)` plus `:timer` | content `AppServiceProvider.php:129-137`; comment-service `AppServiceProvider.php:128-147` | API and commenting rate limits | Limiter window, 60 s | Window expiry | gap: prefix `<app>:<env>:` and off the cache database; the hashed part is framework-generated |
| Not enumerated | vod `app/`; auth `app/Classes/EloquentBuilderWithCache.php` | Legacy `Cache::` call sites and model-binding cache | `CACHE_*` constants | Not inventoried | gap: inventory owed by each owner |
| `authz-sidecar:<env>:<project_id>:decision:<store_id>:<model_id>:g<generation>:<pins12>:<cmode>:<kid>:<canon_hmac>:v1` (`<kid>` is the lowercase hex of the first 8 bytes of `HMAC-SHA256(K_mac, "kid")`, so a new `K_mac` is a new keyspace; authz-sidecar `c7f5286`) | RFC 0007 §5 `:174-188` (kid segment aligned in authz-openfga `6f6f31b`); `authz-sidecar: internal/decisioncache/keys.go:20,121,128-134` | Whole authorization decision | Allow 15 m, deny 15 s; bundle maxima 30 m, 45 s | Token rotation, then TTL | live (mode `redis` only; cache database 0) |
| `authz-sidecar:<env>:<project_id>:project-token:v1` | RFC 0007 §5; `keys.go:21,137-142` | Project clear token (random 128-bit) | Created with a short TTL (the write-back cutoff `Q + E + skew` rounded up to 15 s); an entry write extends it to 60 m (`2 * hard_ceiling_ms`) (`authz-sidecar: internal/decisioncache/cache.go:46-56`) | Rotated by a project clear | live |
| `authz-sidecar:<env>:<project_id>:subject-token:<subject_hmac>:v1` | RFC 0007 §5; `keys.go:22,145-150` | Subject-in-project clear token | as the project token | Rotated by a subject clear | live |
| `authz-sidecar:<env>:global-token:v1` | RFC 0007 §5; `keys.go:23,153-155` | Global epoch token (no global clear: the user accepted "no cross-project clear") | 60 m | Rotated by a replica that finds the redis-mode lease absent (an off period, a full restart or a lapsed lease), not by a clear (`internal/decisioncache/cache.go:20-33,538-579`) | live |
| `authz-sidecar:<env>:redis-mode-lease:v1` | `authz-sidecar: internal/decisioncache/keys.go:24,180-182`; `cache.go:20-33,507-530` | Marker that a redis-mode replica ran; an absent marker triggers the global-token rotation | 30 s, refreshed every 10 s | TTL | live (cache database 0) |
| `authz-sidecar:<env>:<project_id>:clear-cooldown:project:v1`, `authz-sidecar:<env>:<project_id>:clear-cooldown:<scope>:<subject_hmac>:v1` (`<scope>` is `subject` or `decision`) | RFC 0007 §6.6 `:243`; `authz-sidecar: internal/decisioncache/keys.go:25-26,160-178`; `clear.go:53-54,187-212` | Project or subject clear cooldown (a limiter: limiter database, not the cache database; RFC 0007 §8 Eviction), `SET NX PX`; unlinked early when a clear is shed | 60 s project, 5 s subject and decision | TTL, or early release | live (limiter database `AUTHZ_SIDECAR_DECISION_CACHE_REDIS_LIMITER_DB`, default 1, never 0: `internal/config/decision_cache_clear.go:28-29,72`; `redis.go:71-79`) |

Services with no Redis key found: `entitlement-projector`, `entitlement-spoa`, `gateway`, `wa`, `notif`,
`tusd`. `ticket` has an emptied working tree at `dfbe181` ("remove all to migrate to golang ticket service").

## Owner decisions

Register `292b831` (`entitlement-api: docs/decisions/mesh-145d79be-decision-register.md`), owner, 2026-10-10:

- **D-CA-12, Redis AUTH is selected by env in every environment.** The Redis a service is given may or may
  not require AUTH, locally and in production alike, and the choice never depends on `APP_ENV`. With AUTH the
  service uses its own ACL user (`~<app>:*`); the ACL user applies only when the Redis requires AUTH. Without
  AUTH no credentials are sent. An unauthenticated connection is not reported in logs or readiness.
  Cache safety does not depend on AUTH, because every `authz-sidecar` value is MAC-authenticated.
- **D-CA-13, break-glass flush by tag.** A tag is the service name plus the tenant (`project_id`); flushing a
  tag invalidates every entry under it. In `authz-sidecar` the per-project token is the (service, tenant) tag,
  so a tenant flush is the existing project-scope clear. The global token is the whole-service tag, and a
  whole-service flush is an operator runbook action that rotates it. The clear API has no global scope.

## Open decisions

- Persistent keys (rediskit version counters, promphp metric storage) contradict the explicit-TTL rule.
- Whether a numeric `user_id` or a raw IP address is PII in a key is unresolved; RFC 0007 Section 5 keeps
  the user inside an HMAC.
- Redis topology: one shared instance today. If a cluster is adopted, a service needing multi-key reads raises a
  co-location request here; RFC 0007 reads switch to pipelined GETs. Until then no `{}` hash tag is allowed beyond the
  exception in `Fleet bindings of the shape`.
- No ACL user with a `~<app>:*` pattern exists in the deploy repository yet.
