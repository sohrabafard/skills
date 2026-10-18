# Skill pack review 02: optimization

Scope: the 69 skills under `skills/sohrab/`. Date of review: 2026-10-18.
Companion files: `01-contradictions-and-overlaps.md`, `03-new-skill-proposals.md`.

## Purpose and method

This file lists skill content that makes an agent do unnecessary work or repeat work in the develop, debug and publish loop. It does not list style. Each item states the cost, where it sits, and the change that removes it.

- Status tags follow file 01: `[V]` checked by the parent, `[R]` reported by a reviewer lane and not re-read by the parent.
- Sizes below come from `wc -c` on each `SKILL.md`. Body size is paid on every load of a skill; a reference is paid only when read (AGENTS.md "Structure").
- The repository validator warns when a top-level body is long (21 skills, by line count). Its warnings are repeated here as evidence, not as a rule.

## A. Always-paid body size

**O-01 [V] Largest skill bodies.** Sizes in bytes of `SKILL.md`:

| Skill | Bytes | Validator body warning |
|---|---|---|
| `alaa-testing-strategy` | 30,726 | yes (205 lines) |
| `alaa-php-clean-code` | 25,808 | yes (206 lines in the body; the warning reads "206 lines") |
| `alaa-system-design` | 19,422 | yes (166 lines) |
| `alaa-algorithms-data-structures` | 19,058 | yes (153 lines) |
| `alaa-reliability-sla` | 17,856 | yes (140 lines) |
| `alaa-cc-orchestrator` | 17,686 | yes (168 lines) |
| `alaa-codex-orchestrator` | 18,356 | yes (169 lines) |
| `alaa-security-review` | 15,823 | yes (144 lines) |
| `alaa-project-constitution` | 15,022 | yes (210 lines) |
| `alaa-memory-os` | 14,443 | yes (207 lines) |

- Cost: each of these bodies is read whenever the skill is triggered, even when the task needs one section.
- Change: move the sections that are consulted rather than followed into `references/`, leaving the role, trigger, decision procedure, stop conditions and one-line pointers in the body. This is the rule AGENTS.md already states under "Structure". Start with `alaa-testing-strategy` and `alaa-php-clean-code`, which are the two largest.
- Caution: the validator warnings are line-based. Byte size is the better signal. Do not shorten a body that carries a behaviour rule; move the consulted material instead.

**O-02 [R] Duplicated routers in the always-paid body.** Each duplicate router costs body tokens on every load and drifts (file 01, M1-14 and M1-15).
- `alaa-frontend-developer/SKILL.md:69-85` duplicates `references/00-topic-map.md:10-29`.
- `alaa-quasar-app-vite-v3/SKILL.md:36-47`.
- `alaa-reliability-sla/SKILL.md:107-119` duplicates its topic map.
- `alaa-services-contract/SKILL.md:53-73` duplicates its topic map, and has already drifted.
- Change: reduce each body to one pointer line, as AGENTS.md requires for skills with 9 or more references.

**O-03 [R] Dated environmental observation in an always-paid body.** `alaa-minio-object-storage/SKILL.md:71-82` ("What the fleet does today") records dated, unverifiable observations about another repository. It sits in the body that every load pays for. It conflicts with the grounding rule on volatile facts. Change: move it to a dated reference that is read on demand, and reconcile the source name (the body cites "tusd-upload-platform repository", while the tusd skill names "Ala tusd repository").

**O-04 [R] Routing over-sized in the workflow start sequence.** `alaa-workflow/SKILL.md` "Start" section, steps 3 to 6, asks the agent to invoke or read up to four owners before any repository work: `alaa-memory-os` when triggered, `alaa-code-intelligence-routing` once, `alaa-low-noise` and a domain skill, and three reference reads (`task-tracking.md`, `artifact-lifecycle.md`, `companion-routing.md`). The file's own rule says a small bounded task creates no workflow artifact, but the start sequence has no matching exemption for a small task that still loads these owners. Confidence medium on the size of the effect; the sequence is real.
- Change: add a fast path for a bounded single-phase task that names which of these steps may be skipped.

## B. Mandatory scaffolds that apply to every change

**O-05 [R] Shaka Player forces the whole pipeline on any change.** `alaa-shaka-player/SKILL.md:58-65` lists six mandatory steps, including reading `references/80` for every task. Line 69 says every player change must ship a configure block, error classes, telemetry and QA evidence. A one-line config edit runs all of it.
- Change: scope each step by change size or trigger. The configure block and error classes apply when the change adds or alters a player option or error path.

**O-06 [R] TUS design returns ten items for every design or review.** `alaa-tusd-upload-platform` (`tusd-upload-platform/SKILL.md:64-66`) requires every design or review to return ten items. A review of one hook returns the same ten.
- Change: make the ten items conditional on the scope of the design, or list the items each change type needs.

**O-07 [R] Frontend QA runs SSR and service-worker checks with no scope.** `alaa-frontend-developer/references/50-qa-and-verification.md:27-47` makes "mandatory SSR and hydration checks" and the service-worker runbook apply without a trigger. A CSS-only change, or a repository with no PWA mode, is told to run them. The Quasar playbook (`alaa-quasar-app-vite-v3/references/75-testing-ci-playbook.md:22-31`) already has an "Applies when" column; the frontend file lacks one.
- Change: add the same column to file 50.

**O-08 [V] Partitioned FK audit writes permanent repository files on every audit.** `alaa-partitioned-table-fk-audit/SKILL.md:3, 19, 49-56` requires a durable regression test in the repository, CI wiring and a synthetic broken fixture for each audit, "even when the request is only an audit". This creates a repository change, a CI change and a second test run in the audit loop, when the request asked for a read.
- Change: make the installation conditional on an explicit request, and report the missing regression test as a finding.

**O-09 [R] Go: the whole-suite race run is required in several triggers.** `alaa-golang-fiber/references/40-production-readiness.md:150` requires `go test -race ./...` unconditionally at pre-ship. `alaa-golang-fiber/SKILL.md:88-91` and `references/30-validation-testing.md:122-126, 168-169` add further triggers, and `alaa-golang/SKILL.md:66-72` gives a different list. An agent that follows several of these runs the full race suite repeatedly.
- Change: one trigger list, owned by `alaa-golang`. Fiber keeps only its own triggers (file 01, C-18).

**O-10 [R] Go: fixed TDD sequence repeated.** `alaa-golang-fiber/references/30-validation-testing.md:117-121` and `clean-code/references/40-testing-and-contracts.md:20` repeat the TDD steps. The owner, `alaa-golang/references/63-tdd-and-testing-discipline.md:15-29`, adds the failure-reason check that the copies omit. Agents follow the shorter copy and skip the check, then debug the failure later.
- Change: point both copies at file 63.

**O-11 [R] Audit of an OpenAPI or Postman contract re-derives the owner's rules.** `alaa-laravel-public-api-contract-pack` restates the Postman rules owned by `alaa-postman-collections` (file 01, M1-05). The audit reads both, then decides which set governs. Change: the pack points to the Postman owner and runs only the parity audit.

## C. Loop-level rework

**O-12 [R] Upgrade sweep with an undefined apply set.** `alaa-laravel-upgrade-all-packages/SKILL.md:23-24` and step 3 (file 01, C-03). An agent that applies all moves, then splits majors, redoes the lock diff. Change: define the allowed set and the command that applies only it, so the first run is the final run.

**O-13 [R] Ansible gate run and rerun.** `ansible-generator/SKILL.md:42-46` omits the currency check, and `playbook.md:230-243` includes it (file 01, C-02). An agent that follows the SKILL gate passes a playbook that the second gate would fail, then reruns it after a user report. Change: a single gate.

**O-14 [R] Frontend verification runbook has two homes.** `alaa-frontend-developer/references/50-qa-and-verification.md:33-36` and `alaa-quasar-app-vite-v3/references/75-testing-ci-playbook.md:35-52` list the service-worker checks. The lists differ. An agent running one list misses items in the other (file 01, M1-13). Change: one list, in file 75.

**O-15 [R] Object storage: two part-size defaults for one upload plane.** `alaa-minio-object-storage/references/05-environment-contract.md:60` (16 MiB, estimate) and `tusd-upload-platform/references/25-upstream-library.md:62` (50 MiB) (file 01, C-29). An agent sizing one plane from the other reruns the capacity estimate after the first load test. Change: name which setting governs the tus plane, and map the two.

**O-16 [R] Permission generator: apply step ahead of authorization.** `alaa-permission-generator/SKILL.md:72-73` requires the consumer map in the same change as the seed, while lines 36-48 say applying needs explicit words (file 01, C-36). The agent either asks mid-change or applies unauthorized. Change: make the same-change rule conditional on the seed being authorized.

**O-17 [R] Ansible validator: history carried into the rule.** `ansible-generator/references/best-practices.md:91-92, 94-96, 105-107, 218-219` and `ansible-validator/references/playbook.md:33-36` describe past behaviour. `ansible-validator/references/failure-classes.md:350` says corrections were "carried over from the retired common_errors.md". These lines change no action, cost reads, and can revive a retired rule. Change: move the narratives to an outputs or changelog record. Do not delete (AGENTS.md "Nothing is deleted").

**O-18 [R] Docker version table stamped with a date that expires soon.** `alaa-docker-production/references/10-dockerfile-authorship.md:188-197` says the table is "current as of 2026-07-29", with Node 24 Active LTS "to 2026-10-20". The review date is 2026-10-18. An agent that copies the Node row writes an expiring default. Change: re-run `check-image-pinning.mjs --versions` before any Node default is written, and re-date the table.

## D. Duplicated reading cost

These items are not wrong on their own. Each adds a file an agent reads to confirm a rule that another file states.

**O-19 [R] Keyset restates the envelope and limits.** `alaa-keyset-pagination/references/40-wire-contract-limits-and-errors.md:9-36` restates the `meta` envelope and the `has_more` exclusion, which services-contract owns (file 01, M1-09). The file says it states "only what keyset adds". Change: keep only the algorithmic rationale.

**O-20 [R] Fiber restates many owners.** `alaa-golang-fiber/references/40-production-readiness.md` restates singleflight, TTL jitter, negative TTL, measure-first, cardinality and the signal list (file 01, M1-18). Change: a pointer per rule.

**O-21 [R] Orchestrator "keep focused checks" rule repeated five times.** File 01, M1-31. Change: one owner, the orchestrator's verification-and-gates reference.

**O-22 [R] Dispatch return contract split across three owners.** File 01, M1-29. Change: one owner per clause, so an agent reads each clause once.

**O-23 [R] ClickHouse boundary and worked instance.** `alaa-signoz-clickhouse-docs/SKILL.md:50-54` and `clickhouse-performance-schema-ops/SKILL.md:47-52` carry the same text. `clickhouse-performance-schema-ops/references/15-fleet-clickhouse-boundary.md:83-110` embeds a commit hash and line numbers in a worked instance. The worked instance goes stale, and the duplicate text is read twice. Change: keep the boundary in one file, and move the instance to a dated, re-derivable note.

**O-24 [R] Bale and Mediana restate reliability and security rules.** File 01, M1-23 and M1-24. Change: keep only the vendor-specific column and point to the owners.

## E. Maintenance-driven rework

**O-25 [R] Dated facts without a refresh trigger.** `alaa-golang-fiber/SKILL.md:24-28`, `alaa-golang-clean-code-principles/references/30-runtime-and-observability.md:101-105`, `alaa-golang-fiber/references/40-production-readiness.md:69-76` and `50:41-47` state "verified" facts with dates. They age without a trigger. The next reviewer re-derives them. Change: attach the source and a re-check trigger, or cite a live source.

**O-26 [V] Date bound in a durable rule.** `alaa-mongodb-patterns/SKILL.md:14-16`: "On 2026-07-26 no service … runs MongoDB". Change: cite a live source or drop the date.

**O-27 [R] Phase gate duplicated with its dated facts.** File 01, C-19. Each copy must be updated when the phase changes. Change: delete the restated gate.

**O-28 [R] Shaka and IndexedDB verbatim copy.** File 01, M1-26. A change to one copy is not made to the other. Change: pointer.

## F. Not reported

- Skills with no optimization finding in the lanes' reads: the lanes did not read most reference files, so a clean result there is unknown.
- `alaa-shaka-player/assets/templates/offlineDownload.ts` is referenced by no file in the skill. This is cleanup, not an agent cost, and it belongs in a separate tidy-up change.
- Cost of loading the global owners at the start of every task is outside this pack and is not reported.
