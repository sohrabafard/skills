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
- Literal segments are lowercase; words inside one segment join with `-` (`explain-object`). No `{}` hash tag.
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
trees on 2026-10-10; `authz-sidecar` rows re-read at `ac89ce0` (CACHE-1 P5).

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
| `verify-sms-<project_int>:<mobile>` | auth `app/Services/Auth/OtpService.php:195-203` | OTP code | `otp_ttl_seconds`, default 120 s, minimum 10 (`:205-209`) | `forget()` deletes it (`:190-192`) | gap: mobile in clear, integer project id; target `auth:<env>:<project_id>:otp-code:<mobile_digest>:v1` |
| `auth:sensitive-attempts:v1:auth:otp:verify:<ip>:<sha256_16>`, `...:v1:auth:refresh:<ip>:<sha256_16>` | auth `app/Providers/AppServiceProvider.php:58`; `app/Http/Controllers/Api/Auth/AuthController.php:267-301` | OTP-verify and refresh attempt limiter | Window: OTP verify 300 s, refresh 60 s (`PEXPIREAT`) | Window expiry; release by owner | gap: no `<env>`; raw IP (see Open decisions); truncated unkeyed hash of a mobile number; a limiter belongs off the cache database |
| `auth:otp:request:<ip>:<sha256_16>` | auth `AuthController.php:112-123,267-271` | OTP-request limiter (Laravel `RateLimiter`) | 300 s | Window expiry | gap, as above; on Redis only where `CACHE_STORE=redis` |
| `auth:totp:step-up:<user_id>:<project_int>:<purpose>` | auth `app/Services/Security/TotpService.php:217,443-449` | TOTP step-up proof | Until proof expiry | TTL | gap: integer project id; target `auth:<env>:<project_id>:totp-step-up:<user_id>:<purpose>:v1` |
| `auth.profile.catalogs.v3`, `available-bank-gateway-urls` | auth `app/Repositories/Profile/EloquentAcademicProfileReadRepository.php:46`; `app/Helpers/helpers.php:189` | Catalog and gateway lists | `CACHE_600`, `CACHE_1`, both default 0 (`config/constants.php:550,556`) | TTL | gap: `auth:<env>:profile-catalogs:v3`, `auth:<env>:bank-gateway-urls:v1` |
| `content:rating-aggregation:active` | content `app/Support/Content/Ratings/RatingAggregationDispatcher.php:35` | Aggregation lease | `ratings.aggregation.lease_seconds`, default 120 s (`:105-108`) | Owner forgets it (`:100-101`) | gap: `content:<env>:rating-aggregation-lease:v1`, off the cache database (a lock) |
| `comment-service:settings` | comment-service `app/Services/SettingsService.php:11` | Settings | none (`rememberForever`, `app/Repositories/CachedSettingsRepository.php:19`) | Forget on save (`app/Models/Setting.php:39`) | gap: no TTL; target `comment:<env>:settings:v<major>`, global |
| `show:lang:<locale>:id:<user_id>`, tag `users` | notification `app/Models/Base/BaseModel.php:55`; `app/Repositories/Base/BaseCacheRepository.php:21-27` | User by id | 86400 s (`BaseModel.php:35`) | Tag flush on write (`app/Services/User/UserService.php:37,43,58`) | gap: `notification:<env>:user:<user_id>:<locale>:v1` |
| Laravel named limiters `md5(<name><by>)` plus `:timer` | content `AppServiceProvider.php:129-137`; comment-service `AppServiceProvider.php:128-147` | API and commenting rate limits | Limiter window, 60 s | Window expiry | gap: prefix `<app>:<env>:` and off the cache database; the hashed part is framework-generated |
| Not enumerated | vod `app/`; auth `app/Classes/EloquentBuilderWithCache.php` | Legacy `Cache::` call sites and model-binding cache | `CACHE_*` constants | Not inventoried | gap: inventory owed by each owner |
| `authz-sidecar:<env>:<project_id>:decision:<store_id>:<model_id>:g<generation>:<pins12>:<cmode>:<canon_hmac>:v1` | RFC 0007 §5 `:156-171`; `authz-sidecar: internal/decisioncache/keys.go:20,115-121` | Whole authorization decision | Allow 15 m, deny 15 s; bundle maxima 30 m, 45 s | Token rotation, then TTL | live (mode `redis` only; cache database 0) |
| `authz-sidecar:<env>:<project_id>:project-token:v1` | RFC 0007 §5; `keys.go:21,124-129` | Project clear token (random 128-bit) | Created with a short TTL (the write-back cutoff `Q + E + skew` rounded up to 15 s); an entry write extends it to 60 m (`2 * hard_ceiling_ms`) (`authz-sidecar: internal/decisioncache/cache.go:46-56`) | Rotated by a project clear | live |
| `authz-sidecar:<env>:<project_id>:subject-token:<subject_hmac>:v1` | RFC 0007 §5; `keys.go:22,132-137` | Subject-in-project clear token | as the project token | Rotated by a subject clear | live |
| `authz-sidecar:<env>:global-token:v1` | RFC 0007 §5; `keys.go:23,140-142` | Global epoch token (no global clear: the user accepted "no cross-project clear") | 60 m | Rotated by a replica that finds the redis-mode lease absent (an off period, a full restart or a lapsed lease), not by a clear (`internal/decisioncache/cache.go:20-33,538-579`) | live |
| `authz-sidecar:<env>:redis-mode-lease:v1` | `authz-sidecar: internal/decisioncache/keys.go:24,166-169`; `cache.go:20-33,507-530` | Marker that a redis-mode replica ran; an absent marker triggers the global-token rotation | 30 s, refreshed every 10 s | TTL | live (cache database 0) |
| `authz-sidecar:<env>:<project_id>:clear-cooldown:project:v1`, `authz-sidecar:<env>:<project_id>:clear-cooldown:<scope>:<subject_hmac>:v1` (`<scope>` is `subject` or `decision`) | RFC 0007 §6.6 `:221`; `authz-sidecar: internal/decisioncache/keys.go:25-26,147-163`; `clear.go:53-54,187-212` | Project or subject clear cooldown (a limiter: limiter database, not the cache database; RFC 0007 §8 Eviction), `SET NX PX`; unlinked early when a clear is shed | 60 s project, 5 s subject and decision | TTL, or early release | live (limiter database `AUTHZ_SIDECAR_DECISION_CACHE_REDIS_LIMITER_DB`, default 1, never 0: `internal/config/decision_cache_clear.go:28-29,72`; `redis.go:71-79`) |

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
  co-location request here; RFC 0007 reads switch to pipelined GETs. No `{}` hash tag is allowed until then.
- No ACL user with a `~<app>:*` pattern exists in the deploy repository yet.
