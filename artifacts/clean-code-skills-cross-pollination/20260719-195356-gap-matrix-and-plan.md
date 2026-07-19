# Cross-pollination gap matrix — alaa-vue-typescript-clean-code / alaa-php-clean-code / alaa-golang-clean-code-principles

Date: 2026-07-19. Basis: full read of all three SKILL.md files and every reference file (27 files, ~3,700 lines).

## Skill shapes (context for every decision below)

- **Vue skill**: enforced contract + numeric budgets + project-proven observed patterns (65-alaa-observed-patterns). Pattern catalog in `references/40-patterns-vue-quasar.md`.
- **PHP skill**: mode-aware refactor discipline + mandatory repository gate + Octane statelessness + rich pattern catalog (`references/design-patterns.md`, 17 patterns) + companion routing.
- **Go skill**: thirteen kit-era principles (P1–P13); deliberately non-duplicative — naming/style/patterns-catalog depth routes to the `alaa-golang` tree (`references/50-skill-boundaries.md`). New principles append, never renumber.

## Phase 1 — concepts present in one skill, missing and meaningful in another

### Into PHP (from Vue / Go)

| # | Concept | Source | Target placement |
|---|---------|--------|------------------|
| P-1 | Numeric size/complexity budgets as hard gates (file/class/method line caps, one primary unit per file, split-seam guidance) | Vue "Size and complexity budgets" | SKILL.md new section + consistency ref |
| P-2 | Presence-detection vs truthiness on merges/partial updates (`??`/`?:` discard legitimate `0`/`false`/`''`; PATCH uses key-presence) | Vue observed pattern #5 | laravel-best-practices (requests) + SKILL non-negotiables |
| P-3 | Failure classification before retry/fallback (definitive 4xx denials never retried; transient transport/5xx retried with backoff) + outbound-HTTP hygiene (explicit timeout, bounded retry, idempotency-aware) | Vue observed pattern #6 + Go P4 retryability | Error-handling baseline + adapter pattern section |
| P-4 | `env()` only in config files; vocabulary (event names, error codes, metric names) as enums/constants, never inline strings | Go P10 | Laravel defaults + non-negotiables |
| P-5 | Idempotency proven by a run-twice test (jobs, listeners, seeders, consumers) | Go P7 | laravel-best-practices (jobs + testing) |
| P-6 | Route posture visible at route registration (auth/permission middleware declared on the route, never buried in controller bodies) | Go P2 | Laravel defaults |
| P-7 | Unknown external facts marked (`NEEDS_<X>_CONFIRMATION`), never invented | Go P13 | SKILL.md small bullet |
| P-8 | Consolidated validation checklist with exact commands (Pint, PHPStan, Pest/PHPUnit) before "done" | Vue 60-validation-checklists | SKILL.md validation section |

### Into Vue (from PHP / Go)

| # | Concept | Source | Target placement |
|---|---------|--------|------------------|
| V-1 | Public-contract inventory before refactors (published props/emits/slots, store public APIs, URL/query params, storage keys, event names, SDK surfaces) | PHP refactor-modes | SKILL.md operating model + 60-checklists |
| V-2 | Boundary naming alignment: one domain term per concept across DTO → mapper → store → composable → component → test; ban vague buckets | PHP consistency-and-naming | 30-clean-code-solid-vue |
| V-3 | Idempotent/double-fire-safe UI mutations (disable while pending, in-flight dedupe, idempotency keys when backend supports) | Go P7 | 20-ts contract async discipline + checklists |
| V-4 | Route auth/permission posture declared in route `meta`, guards read meta (never scattered per-component checks) | Go P2 | 50-quasar router section |
| V-5 | Large-list discipline: server-side pagination / QVirtualScroll; never render unbounded lists | PHP large-dataset section | 50-quasar contract |
| V-6 | Time discipline: immutable date handling, UTC/ISO at boundaries, format at edges | PHP DateTimeImmutable rule | 20-ts contract |
| V-7 | Exhaustiveness checking for discriminated unions (`assertNever` / `satisfies never`) | PHP enums+match | 20-ts contract |
| V-8 | Caching discipline: cache at service/adapter layer with explicit keys incl. user/tenant; never ad-hoc component caches | PHP cache-decorator gate | 40-patterns (Decorator/Facade) |
| V-9 | Vocabulary constants: event names, storage keys, query-param names as `as const` registries | Go P10 | 20-ts contract |

### Into Go (from Vue / PHP)

| # | Concept | Source | Target placement |
|---|---------|--------|------------------|
| G-1 | Partial updates distinguish absent vs zero (pointer fields / presence flags on PATCH wire structs) — presence-detection twin of V/P rule | Vue observed pattern #5 | P8 in `20-domain-...` + `full-guide.md` (extension, no renumber) |
| G-2 | 15-pattern kit-era decision map (Phase 3) as a routing-first reference — maps each GoF pattern to its kit idiom, routes depth to `golang-design-patterns` | user request | new `references/60-design-patterns-kit-era.md` |

Deliberately **not** ported into Go (boundary respect, `50-skill-boundaries.md`): numeric size budgets (golang-code-style), naming families (golang-naming), pattern mechanics (golang-design-patterns), iterator/idiom depth (golang-modernize).

## Phase 2 — web-refresh targets

1. PHP 8.5 final feature set + PER-CS current version (php.net / php-fig) — verify pipe operator, clone-with, `#[\NoDiscard]`, `array_first/last`, Uri ext; PHP 8.4 lazy objects for Proxy pattern.
2. Laravel 13 current release notes — verify skill's upgrade list still accurate; new conveniences worth teaching.
3. Vue 3.5/3.6 status — Vapor mode, `useTemplateRef`, `useId`, `onWatcherCleanup`, watcher pause/resume, reactive props destructure stability.
4. Pinia current major (v3?) — breaking changes affecting the store contract.
5. TypeScript current stable — features relevant to app-level typing discipline.
6. Go: skipped by design — version-sensitive Go idioms are owned by `golang-modernize`/`alaa-golang` (verified durable per Go skill's own 90-source-map).

## Phase 3 — the 15 patterns (screenshot list) per skill

| Pattern | Vue today | PHP today | Go today | Action |
|---|---|---|---|---|
| Singleton | ✓ | ✓ | boot-time composition root (implicit) | map in Go ref |
| Factory Method | ✓ | ✓ | `NewX` constructors (implicit) | map in Go ref |
| Builder | ✗ | ✗ | functional options (owned by golang-design-patterns) | ADD Vue + PHP; map in Go ref |
| Adapter | ✓ | ✓ | P5 ✓ | — |
| Decorator | ✓ | ✓ (cache decorator) | middleware (implicit) | map in Go ref |
| Facade | ✓ | Laravel-facade only — GoF-facade (service facade) distinction missing | kit packages (implicit) | CLARIFY PHP; map in Go ref |
| Proxy | ✓ | ✗ (add PHP 8.4 lazy objects, API proxies) | — | ADD PHP; map in Go ref |
| Composite | ✗ | ✗ | ✗ | ADD Vue (recursive components) + PHP (trees, rule composition); map in Go ref |
| Observer | ✓ | ✓ | outbox/events P6 | map in Go ref |
| Strategy | ✓ | ✓ | strategies-as-data P5 | map in Go ref |
| Command | ✓ | ✓ (jobs) | outbox commands/workers | map in Go ref |
| Iterator | ✗ | ✗ (generators / LazyCollection) | range-over-func (owned by golang tree) | ADD Vue + PHP; map in Go ref |
| State | FSM ✓ (name the alias) | ✗ (enum+match transitions) | typed status vocab (P10) | ALIAS Vue; ADD PHP; map in Go ref |
| Template Method | ✗ | ✗ | no inheritance — composition | ADD Vue (renderless/slots) + PHP (cautious); map in Go ref |
| Chain of Responsibility | ✗ (interceptors/guards) | Pipeline ✓ (name the linkage) | chi middleware | ADD Vue; LINK PHP; map in Go ref |

## Execution order

1. Phase 2 searches first (so pattern/practice additions are version-accurate).
2. PHP skill edits (SKILL.md + design-patterns.md + laravel-best-practices.md + php-modern-and-psr.md).
3. Vue skill edits (SKILL.md + 20/30/40/50/60 references).
4. Go skill edits (P8 extension in two files + new 60-design-patterns-kit-era.md + SKILL.md navigation).
