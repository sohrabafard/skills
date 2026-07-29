---
name: alaa-vue-typescript-clean-code
description: Mandatory Vue 3, Quasar, Vite, and TypeScript clean-code contract for writing, reviewing, and refactoring frontend code - Vue style-guide gates, script-setup with type-only props and emits, composable and Pinia shape, SOLID and code-smell repair, design-pattern selection, TypeScript depth (discriminated unions, generics, satisfies, branded types, strict flags), hard size budgets, and the Vue-shaped bindings for async failure, security, observability, load, and testing. Use before changing any .vue or .ts file, composable, store, boot file, or route, and when code is duplicated, weakly typed, monolithic, or already over budget. Do not use for backend, database, infrastructure, CI/CD, or deployment work with no frontend contract impact; for Quasar API lookup or app-vite line detection, which is /alaa-quasar-app-vite-v3; for SSR auth, PWA policy, or Web Vitals, which is /alaa-frontend-developer; or for design tokens, theming, and motion, which is /alaa-ui-ux-design-system.
---

# Alaa Vue TypeScript Clean Code

## Purpose

Make Vue 3 + Quasar + Vite + TypeScript code production-grade: correct, typed, testable, and consistent with the official Vue style guide. This is an enforced contract, not advice. Repair violations inside the task scope; report what cannot be repaired safely as a blocker naming file and symbol.

## Portability and model routing

This skill uses the core Agent Skills format so Claude Code and Codex both load it, and it names no model: a model name written into a skill goes stale silently and is copied forward because it looks authoritative. Take every model and reasoning-effort choice from `/alaa-prompting-guide` (`$alaa-prompting-guide`), `references/50-effort-and-thinking.md`. Keep frontmatter to `name` and `description`; `agents/openai.yaml` is Codex-only UI metadata. Output discipline follows `/alaa-low-noise` (`$alaa-low-noise`) — this skill defines no response format.

## When to use

Before writing, reviewing, or refactoring `.vue`, `.ts`, `quasar.config.*`, `vite.config.*`, `src/boot/*`, `src/stores/*`, `src/router/*`, composables, API clients, or component-library sources; and for any task named as clean code, SOLID, design patterns, technical debt, duplication, or type safety.

## When NOT to use

- Backend, database, infrastructure, CI/CD, or deployment work that changes no frontend contract, state, route, component, or type.
- Documentation, product planning, UI copy, or design-only tasks that change no Vue/TypeScript code.
- A pure API lookup with no code being written — that is `/alaa-quasar-app-vite-v3` (`$alaa-quasar-app-vite-v3`).

## Where the rules live

`references/00-topic-map.md` is the only router in this skill. Match your diff against its conditions and load just the rows that match. No reference file is unconditionally required.

## Source priority

Repo-local instructions (`AGENTS.md`, `CLAUDE.md`, package scripts, lint and `tsconfig` config, existing tests) beat current official Vue, Quasar, Vite, Pinia, and TypeScript docs, which beat this skill. Keep a working repo convention unless it breaks correctness, safety, a Vue Priority A rule, or TypeScript soundness. `references/05-sources-and-freshness.md` owns provenance and freshness.

## What this skill does not own

This skill owns the **Vue-shaped expression** of a rule: where the code lives, what a component may emit, which file holds the seam. It owns no doctrine, no value, and no name another skill owns. When a row applies, state the binding and route the rule — a rule written twice drifts in one copy and the reader cannot tell which.

| The moment it comes up | Owner |
|---|---|
| Retry count, backoff shape, timeout, deadline, idempotency, degradation | `/alaa-reliability-sla` (`$alaa-reliability-sla`) |
| Test layer, doubles, flake, the six proof levels | `/alaa-testing-strategy` (`$alaa-testing-strategy`) |
| Threat class, sanitiser choice, fail-closed rule, secrets, CSP | `/alaa-security-review` (`$alaa-security-review`) |
| Trust boundary, route trust posture, gateway headers | `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`) |
| Permission bitmap contract and the canonical TypeScript decoder | `/alaa-permission-generator` (`$alaa-permission-generator`) |
| Log, metric, trace, and exception requirement levels and gates | `/alaa-observability-soc` (`$alaa-observability-soc`) |
| Every name and value: event names, storage keys, query params, page sizes, timeout values, timestamp format | `/alaa-services-contract` (`$alaa-services-contract`) |
| Paging any list endpoint; cursor format | `/alaa-keyset-pagination` (`$alaa-keyset-pagination`) |
| Complexity bounds, the bound on a list, N+1 resolution | `/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`) |
| Identifier encode/decode, and `scripts/codec-conformance.sh` | `/alaa-crockford-base32-codecs` (`$alaa-crockford-base32-codecs`) |
| Folding non-ASCII digits; text normalization form and its corpus | `/alaa-input-normalization` (`$alaa-input-normalization`) |
| `quasar.config` semantics, app-vite line detection, service-worker depth, browser permissions | `/alaa-quasar-app-vite-v3` (`$alaa-quasar-app-vite-v3`) |
| SSR auth/session, PWA and offline policy, Web Vitals, browser debugging (hydration mismatch, lost reactivity, stale closure) | `/alaa-frontend-developer` (`$alaa-frontend-developer`) |
| Design tokens, theming, motion, `prefers-reduced-motion` | `/alaa-ui-ux-design-system` (`$alaa-ui-ux-design-system`) |
| IndexedDB schema, quota, eviction, persistence, browser outbox | `/alaa-indexeddb-browser-storage` (`$alaa-indexeddb-browser-storage`) |
| Published package `dist` boundary, peer deps, rebuild-before-check | `/alaa-mono-package` (`$alaa-mono-package`) |
| Comment and JSDoc policy: what earns a comment | `/alaa-frontend-doc-annotations` (`$alaa-frontend-doc-annotations`) |
| Pre-implementation subsystem design | `/alaa-system-design` (`$alaa-system-design`) |
| The quality bar itself | `/alaa-project-constitution` (`$alaa-project-constitution`) |

## Non-negotiable invariants

- Component APIs are explicit: typed props, typed emits, and a documented slot wherever the slot name does not say what fills it. A child never reads or writes a parent's internals.
- State has one owner. A component does not hold domain state that a store, composable, or service owns.
- Every side effect registered in a component or composable is disposed in the same file: listeners, timers, observers, subscriptions, object URLs, in-flight requests, watchers.
- Every user-visible async surface exposes loading, error, success, and cancellation. `references/70-async-and-failure-binding.md` states where each one lives.
- `any` does not appear in touched code. An untyped third-party boundary is isolated in one adapter module that returns a declared domain type; that adapter file is the only file permitted an `any`, and it carries a one-line comment naming the library and its installed version.
- A user-triggered mutation cannot fire twice: the trigger is disabled, or the request deduped by action key, for the whole in-flight window, and re-enabled only in `finally`. Whether the request also carries an idempotency key, and what that key contains, comes from `/alaa-reliability-sla` (`$alaa-reliability-sla`).
- Untrusted content reaching a template, a permission read in a component, and any `VITE_*` value are governed by `references/72-frontend-security-binding.md`. A component does not invent its own answer to any of the three.
- Accessibility is written with the component, not after it: label, role, keyboard path, and focus target for every interactive element the change adds.

## Size and complexity budgets (hard gates)

Repo-local rules may set stricter numbers; stricter wins.

- A composable, store, service, or util `.ts`/`.js` file: **at most 400 lines**.
- An SFC: **at most 300 lines** of template plus script.
- A single function: **at most 60 lines**.
- One exported primary unit per file. Its own types and private helpers ride along; unrelated exports do not.
- A `useX` returns one responsibility. A composable returning filters and transport verbs and drafts and lifecycle sync is at least three composables plus a thin orchestrator.

Cross a budget and split before declaring the work done, along these seams: pure policy, classification, and formatting into modules with no Vue imports; view/filter/selection state into one `useX`; draft and dialog state into one `useX`; transport verbs into one `useX` receiving those narrow surfaces; one thin orchestrator composing them. Deliberate data registries — mock rows, static option tables — are the exception: data rows are not logic.

**A file already over budget before your change does not grow by even one line.** Extract the touched responsibility into a new file that is under budget. If that is impossible, stop and report the blocker naming the file and its current line count; do not ship the growth with a note attached.

## Task mode and the public-contract inventory

Classify the task first: **new feature slice** (design boundaries, state ownership, error and empty states, and tests before coding), **local refactor** (preserve public behaviour, keep the diff focused), **review** (rank findings by severity, one repair each), or **repo-wide normalization** (staged plan, explicit approval first).

Before any refactor beyond a single local slice, inventory what the change can break, and preserve it unless the task allows a break: published props, emits, and slots, especially in a package consumed from `dist`; store public state, getters, and actions used across features; route names, paths, and query params; storage and cache keys; emitted event names; i18n keys; SDK adapter surfaces. A contract change smuggled into a cleanup is a blocking finding.

## Validation gate

Before the final response, run the project's typecheck and lint scripts as named in `package.json`, plus the tests covering the changed behaviour. If a script is absent or the runtime rejects it, report the exact command and its exact failure text; an unrun check is reported as unrun, never as passed. `references/60-validation-gates.md` owns the checklists and the command set; `references/78-testing-binding.md` owns which proof level each claim needs.

## Stop rules

Ask one narrow question and stop only when the missing information would change a public API, the architecture, data ownership, a side effect, a destructive operation, or what counts as validated.

If the requested change conflicts with these rules, implement the safest compliant version and name the conflict. If compliance needs a refactor outside scope, record it as a blocker with file-level evidence rather than doing it silently.
