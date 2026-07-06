# Alaa Golang Topic Map

Use this file after `alaa-golang` triggers. Read only the smallest reference that matches the task.

## Start here

- Read `full-guide.md` for the production Go baseline.
- Read `11-orchestration-and-overlap-guide.md` when a task spans multiple Go concerns or the right public skill is unclear.

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

- Load `alaa-golang-clean-code-principles` ( `$alaa-golang-clean-code-principles` ) first for any `alaa-go-chi` service — it owns the mandatory P1–P13 platform discipline.
- Read `62-clean-code-and-patterns.md` for the generic Go clean-code and pattern layer beneath it.
- Route generic Go style to `golang-code-style` ( `$golang-code-style` ) and the pattern catalog to `golang-design-patterns` ( `$golang-design-patterns` ).

## If the task is about reading, navigating, or refactoring existing code

- Load `golang-gopls` ( `$golang-gopls` ) for semantic navigation and diagnostics (`go_search`, `go_file_context`, `go_symbol_references`, safe rename) instead of grep-and-guess.
- Load `golang-refactoring` ( `$golang-refactoring` ) for the safe, staged process of restructuring at scale, together with the target-shape skill and `golang-gopls` as the actuator.
- Read `11-orchestration-and-overlap-guide.md` for the gopls-vs-godig-vs-govulncheck boundary and the refactoring-vs-target-shape split.

## If the task is about the latest Go language and toolchain

- Read `70-go-1.26-and-modern-language.md` for the Go 1.26 baseline, the features to adopt by default, and the adoption rules.
- Route the mechanical rewrite to `golang-modernize` ( `$golang-modernize` ) and confirm live release facts from `SOURCES.md`.

## If the task changes behavior

- Read `63-tdd-and-testing-discipline.md`.
- Use it before implementation so tests drive the change.

## If the task is about choosing packages

- Read `40-production-ready-package-catalog.md`.
- Use `golang-popular-libraries` ( `$golang-popular-libraries` ) for broad ecosystem discovery.
- Use `golang-pkg-go-dev` ( `$golang-pkg-go-dev` ) to check a specific path's versions, symbols, importers, licenses, or CVEs before adopting it.
- Use the local package catalog when the choice must fit this stack.
- Read `30-enterprise-shortlist.md` only when stdlib, public skills, and the package catalog still leave a gap.

## If the task is about routing to other skills

- Read `11-orchestration-and-overlap-guide.md` for primary plus secondary skill bundles.
- Read `10-installed-golang-skills.md` for public Go skills.
- Read `20-sohrab-companions.md` for Sohrab companion skills.

## If the task is version-sensitive or needs fresh facts

- Read `SOURCES.md` and verify live state from official sources.

## Reading policy

- Do not load every reference by default.
- Prefer `full-guide.md` plus one focused reference.
- Keep `SKILL.md` compact by moving details into references.
