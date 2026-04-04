---
name: alaa-golang
description: "Use this skill as the main entrypoint for Golang work, including services, libraries, CLIs, Fiber applications, concurrency, testing, performance, observability, and production delivery. It routes to the right installed Go and Sohrab companion skills while enforcing a current, official-source-aware Go baseline."
---

# Alaa Golang

## Purpose

Use this skill as the main entrypoint for Go work in this pack.

It does not replace the installed Go skills. It selects and combines them, adds Sohrab-specific companion routing, and
enforces a merged baseline for current Go and Fiber work.

## Live version policy

- Go does not publish an official `LTS` branch.
- Check `https://go.dev/doc/devel/release` first.
- Treat the latest stable release and the previous still-supported major release as the supported target set.
- At the time of this refresh:
    - `go1.26.1` was released on `2026-03-05`
    - `go1.25.8` was released on `2026-03-05`
- Do not describe Go as "LTS" unless the upstream project changes its release policy.
- If the project uses Fiber, verify framework compatibility before raising the Go toolchain. Fiber v3 explicitly warns
  that its `unsafe` usage may not always be compatible with the latest Go version.

## Merge policy

`alaa-golang` merges the requested external guidance as:

- lifecycle-safe concurrency from `effect-concurrency-fibers`, translated into Go with `context`, `errgroup`, channels,
  worker pools, and explicit shutdown ownership
- clarity-first Go style from the Uber guide, reinforced by the installed Go style, naming, safety, and error-handling
  skills
- Fiber production structure from the Fiber best-practices skill, aligned with official Go module layout and
  thin-handler server design

## Default engineering stance

- start with official Go module layout; do not cargo-cult a large service skeleton
- keep binaries in `cmd/`, private app code in `internal/`, and publish reusable packages only on purpose
- prefer thin HTTP or Fiber handlers, explicit service boundaries, typed config, and graceful shutdown
- every goroutine needs an owner, a cancellation path, and a shutdown story
- bound concurrency intentionally; do not create unbounded fan-out
- use the standard library first unless `golang-popular-libraries` gives a better justified choice
- validate with the smallest meaningful Go-native checks before widening to CI or infra validation

## When to use

- any Go feature, refactor, review, bug fix, architecture, or production-hardening task
- Fiber APIs, middleware, request lifecycle, and service structure
- situations where one top-level Go skill should decide which more specific installed skills to load next

## When NOT to use

- non-Go tasks where Go is not the decision surface
- pure infra work with no Go code, Go runtime behavior, or Go delivery implications

## Quick start

1. Confirm whether the task is a CLI, library, standard HTTP service, Fiber service, gRPC service, or mixed repo.
2. Read `references/full-guide.md` for the merged baseline.
3. Read `references/10-installed-golang-skills.md` and load only the specific Go skills the task actually needs.
4. Read `references/20-sohrab-companions.md` when the task touches observability, security, Docker, Kubernetes, data,
   docs, or workflow coordination.
5. Validate with the narrowest relevant Go checks before scaling out to CI or infra validation.

## Routing rules

- For current-language idioms and release-aware refactors, start with `golang-modernize`.
- For style, naming, defensive coding, and errors, route to `golang-code-style`, `golang-naming`, `golang-safety`, and
  `golang-error-handling`.
- For concurrency or cancellation, route to `golang-concurrency` and `golang-context` together.
- For Fiber or server layout, route to `golang-project-layout`, `golang-design-patterns`, `golang-observability`, and
  `golang-testing`; add the relevant Sohrab companion skills when delivery or trust boundaries matter.
- For performance, measure first with `golang-benchmark`, then optimize with `golang-performance`.

## Reference navigation

- Topic map and fast router:
    - `references/00-topic-map.md`
- Merged Go, Uber-style, concurrency, and Fiber baseline:
    - `references/full-guide.md`
- Installed public Go skill routing:
    - `references/10-installed-golang-skills.md`
- Sohrab companion skill routing:
    - `references/20-sohrab-companions.md`
- Live and external sources:
    - `references/SOURCES.md`

## Maintenance rules

- Keep this file routing-first and compact.
- Move dense detail into `references/`.
- Re-check `go.dev/doc/devel/release` whenever version-sensitive wording changes.
- Re-check Fiber compatibility wording whenever the supported Go baseline or Fiber major version changes.
- Update the routing references when new public Go or relevant Sohrab skills are added.
