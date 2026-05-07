# Alaa Golang Topic Map

Use this file after `alaa-golang` triggers. Read only the smallest reference that matches the task.

## Start here

- Read `full-guide.md` for the production Go baseline.

## If the task is about HTTP APIs

- Read `30-http-api-framework-choice.md` first.
- Read `31-chi-api-guide.md` when chi is chosen, the repo already uses chi, or the raw service is small/simple.
- Load `alaa-golang-fiber` ( `$alaa-golang-fiber` ) when Fiber is chosen, the repo already uses Fiber, or the raw service is large/high-concurrency/SLA-heavy.

## If the task is about service architecture

- Read `60-service-architecture-patterns.md`.
- Use it for repository pattern, service/use case boundaries, handler boundaries, and dependency construction.

## If the task is about Redis cache

- Read `61-redis-cache-layer.md`.
- Use it for cache-aside, keys, TTLs, invalidation, stampede protection, fallback policy, and cache tests.

## If the task is about clean code or design patterns

- Read `62-clean-code-and-patterns.md`.
- Route generic Go style to `golang-code-style` ( `$golang-code-style` ) and local production rules to this reference.

## If the task changes behavior

- Read `63-tdd-and-testing-discipline.md`.
- Use it before implementation so tests drive the change.

## If the task is about choosing packages

- Read `40-production-ready-package-catalog.md`.
- Use `golang-popular-libraries` ( `$golang-popular-libraries` ) for broad ecosystem discovery.
- Use the local package catalog when the choice must fit this stack.
- Read `30-enterprise-shortlist.md` only when stdlib, public skills, and the package catalog still leave a gap.

## If the task is about routing to other skills

- Read `10-installed-golang-skills.md` for public Go skills.
- Read `20-sohrab-companions.md` for Sohrab companion skills.

## If the task is version-sensitive or needs fresh facts

- Read `SOURCES.md` and verify live state from official sources.

## Reading policy

- Do not load every reference by default.
- Prefer `full-guide.md` plus one focused reference.
- Keep `SKILL.md` compact by moving details into references.
