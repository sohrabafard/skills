# Backend modernization evidence

> Citation notation: `<repo>/` denotes this repository root; resolve it before invoking a command. Path lists use this display prefix only; strip it when reproducing a recorded hash manifest. [Original exact evidence](./backend-evidence.raw.txt.gz) preserves the pre-normalization text.

Status: scoped implementation complete; independent review remains with the parent.
Agent: alaa-implementer-sol; configured gpt-6-astra/high; requested override none; observed model/effort unknown.
Date: 2026-09-29. Cwd for all commands: repository root. Scope: alaa-golang,
alaa-golang-fiber, alaa-async-messaging, alaa-laravel-job-rabbitmq only, plus this authorized evidence directory.
Workspace-write sandbox was declared; narrower lane ownership was enforced by scope. No deployment, consumer
upgrade, package installation, broker access, commit or private-kit phase change occurred.

## Read and change coverage

All SKILL.md, references, agents metadata, scripts, fixtures, examples/assets, evals and pinned snapshots
in the four owned directories were read before authoring; full-read inventory is `backend-read-coverage.txt`.
Large-file reads were chunked and truncated reads resumed. Applicable root/sohrab instructions, prompting
compression owner, routing, low-noise, workflow, orchestrator, repo-docs, services-contract and gateway-trust
owners were read, as were the parent plan/state, backend-research.json and validation-strategy.md.
Historical installed-package and private-kit observations retain their original dates; no live revalidation is claimed.
Drafts were rewritten through the compression done-test and all scoped diffs inspected. Load-bearing
version/capability conditions, authority boundaries, failure paths, source dates and required proof survived.
Touched Markdown is an atomic agent execution contract, not repository narrative; no document split was introduced.

## Decisions and acceptance

- Go: current upstream 1.27.1 is separate from consumer go.mod/toolchain/build-tag constraints. Stable JSON v2
  needs wire-compatibility tests; stable goroutineleak removes the old experiment flag without promising all leaks.
- Fiber: 3.5.0 proxy policy, source-order binding and unmatched-route behavior are version-qualified. Tagged
  proxy source overrides conflicting rolling prose docs for that release. Cached pre-guard HostClients and
  caller-owned custom LB dialers prevent a universal DNS-rebinding guarantee. Global policy stays boot-scoped.
  Three new eval scenarios discriminate trust precedence, shared proxy state and skipped middleware contracts.
- Messaging: canonical broker rules own acquired/delivery counter differences and consumer-cancel semantics.
  Non-counting returns require a proven application bound; existing counted reject/crash paths remain counted.
  Laravel points to those rules and preserves Horizon prohibition, historical driver facts and installed-source
  uncertainty. Signature/class-load verification replaces the false method-count compatibility shortcut.
- Alternatives rejected: blanket consumer version bumps, universal delivery-limit promises, duplicated broker
  doctrine in Laravel, and a blanket runtime-helper DNS vulnerability claim contradicted by the tagged source.

## Official sources checked on 2026-09-29

- https://go.dev/doc/devel/release and https://go.dev/doc/go1.27
- https://github.com/gofiber/fiber/releases/tag/v3.5.0
- https://raw.githubusercontent.com/gofiber/fiber/v3.5.0/go.mod
- https://raw.githubusercontent.com/gofiber/fiber/v3.5.0/middleware/proxy/security.go
- https://docs.gofiber.io/middleware/proxy/#security (disagreement recorded, not silently merged)
- https://docs.gofiber.io/api/bind/#custom-precedence
- https://www.rabbitmq.com/blog/2026/04/23/rabbitmq-4.3-release
- https://www.rabbitmq.com/docs/quorum-queues#poison-message-handling

## Focused verification

Six gate executions across five distinct checks; final outcomes all pass. Exact argv, timestamps,
exit codes and output paths are in `backend-focused-checks.json`. No heavy command, behavioral model eval,
Go/PHP consumer test, live broker test, full suite or independent review was run by this lane.

1. Scoped `git diff --check --` four owned directories: exit 0 (only existing CRLF normalization warning).
2. `sh skills/sohrab/alaa-async-messaging/scripts/check-consumer-bounds.sh --self-test`: sandbox attempt
   failed before fixtures with Win32 error 5 creating the Git Bash signal pipe (exit 3221225794).
   One cause-specific retry of the unchanged command outside sandbox: exit 0, all eight assertions pass.
3. `python -B <repo>/scripts/check_fleet_references.py --skill alaa-golang --skill alaa-golang-fiber
   --skill alaa-async-messaging --skill alaa-laravel-job-rabbitmq`: exit 0; 46 Markdown files,
   144 citations, no findings. Nine informational target-repository paths are pre-existing, non-gating.
4. `python -B skills/sohrab/alaa-repo-docs/scripts/check_markdown_links.py . --files <18 changed Markdown paths>`:
   exit 0; exact expanded argv in the JSON record.
5. Inline `python -B` JSON integrity check: parsed Fiber eval JSON, exact skill name, IDs 0..7,
   unique eval names, exact keys, nonempty prompt/expected strings and files lists: pass. This proves
   fixture integrity, not agent performance.

The edit pass had one precondition assertion on an unchanged heading after earlier files were written;
remaining edits were applied once with that no-op removed. One inspection command had a PowerShell
brace-expansion parse error and was replaced by explicit scoped reads. Neither was a verification pass.
No verification was repeated after success; source files did not change after those passes.

## Snapshot and residual limits

Snapshot selection uses `git diff HEAD --name-only -- <four owned dirs>` plus untracked files under those
same dirs. Nothing in that source scope was excluded. Workflow evidence is outside the owned source scope.
`backend-source.sha256` contains content hashes for all actual changed/untracked source paths.
No new untracked source file or script was added. Rollback is a scoped source revert after preserving any
later user edits; no runtime migration or persisted-data rollback is involved.

Changed source count: 19. Full-read inventory count: 69.
Manifest SHA-256: `e511624bdd2c1076dae25cd7ae40c939ae694727b4deedd652d0afff50c644aa`.

### Actual changed files

- `skills/sohrab/alaa-async-messaging/SKILL.md`
- `<repo>/skills/sohrab/alaa-async-messaging/references/10-transport-and-topology.md`
- `<repo>/skills/sohrab/alaa-async-messaging/references/30-consuming-ack-and-prefetch.md`
- `<repo>/skills/sohrab/alaa-async-messaging/references/40-dead-letter-and-replay.md`
- `<repo>/skills/sohrab/alaa-async-messaging/references/50-failure-classes.md`
- `<repo>/skills/sohrab/alaa-async-messaging/references/60-telemetry-and-proof.md`
- `<repo>/skills/sohrab/alaa-async-messaging/references/90-source-map.md`
- `skills/sohrab/alaa-golang-fiber/SKILL.md`
- `<repo>/skills/sohrab/alaa-golang-fiber/evals/evals.json`
- `<repo>/skills/sohrab/alaa-golang-fiber/references/10-fiber-v3-core.md`
- `<repo>/skills/sohrab/alaa-golang-fiber/references/20-routing-middleware-errors.md`
- `<repo>/skills/sohrab/alaa-golang-fiber/references/30-validation-testing.md`
- `<repo>/skills/sohrab/alaa-golang-fiber/references/45-v2-to-v3-migration.md`
- `<repo>/skills/sohrab/alaa-golang-fiber/references/SOURCES.md`
- `<repo>/skills/sohrab/alaa-golang/references/70-modern-go-baseline.md`
- `skills/sohrab/alaa-laravel-job-rabbitmq/SKILL.md`
- `<repo>/skills/sohrab/alaa-laravel-job-rabbitmq/references/driver-facts.md`
- `<repo>/skills/sohrab/alaa-laravel-job-rabbitmq/references/failure-classes.md`
- `<repo>/skills/sohrab/alaa-laravel-job-rabbitmq/references/source-map.md`
