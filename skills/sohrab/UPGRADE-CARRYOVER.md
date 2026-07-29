# Alaa Skills — Upgrade Carry-Over

Written 2026-07-24. This document exists so the remaining skill upgrades can run in fresh sessions without re-deriving anything. Read it fully before starting a batch.

---

## 1. What is already done

Seven skills were rebuilt and are installed at `D:\Sohrab\Project\skills\skills\sohrab\`. Treat them as the reference standard for everything that follows — when in doubt about shape, register, or structure, open one of these rather than inventing.

| Skill | Version | What it now owns |
|---|---|---|
| `alaa-prompting-guide` | — | Prompts, skills, agent definitions, `AGENTS.md`/`CLAUDE.md`, model and effort selection. **The authority for every model question.** |
| `alaa-cc-orchestrator` | 3.0.0 | Claude Code multi-agent orchestration, 21 roles |
| `alaa-codex-orchestrator` | 3.0.0 | Codex multi-agent orchestration, 21 roles |
| `alaa-workflow` | — | Long-task planning, phasing, state, and continuity across compaction and handoff |
| `alaa-low-noise` | — | Context economy and output discipline, cross-runtime |
| `alaa-codex-runtime-ops` | — | Codex/Windows runtime failure recovery |
| `alaa-bash-shell` | — | Shell lifecycle |

Both orchestrator packs ship `scripts/validate_pack.py`, which enforces pins mechanically and fails on cross-runtime leaks. Run it after touching either pack.

**Model landscape as of this writing.** Opus 5 is the Claude top tier; Opus 4.8 is retired and Fable 5 is an opt-in specialist only. Sonnet 5 is the balanced tier, capped at `high` effort. GPT-5.6 runs `sol`/`terra`/`luna`. Never restate a pin from memory — `alaa-prompting-guide/references/90-model-selection.md` and `references/50-effort-and-thinking.md` own it.

**Codex skill install path.** Personal Codex skills live in `~/.codex/skills` (`Join-Path $HOME ".codex\skills"` on Windows). They are discovered and trigger correctly there even though the official docs omit that location. Reserve `.agents/skills` for skills that travel with a repository.

---

## 2. The quality bar these skills must produce

Every remaining skill is judged by one question: **does an agent using this skill produce work fit for a service that must not fail?** The services in question are production, security-sensitive, high-concurrency, and carry an SLA above 99.99%.

Translate that into checkable requirements. A skill that cannot answer these for its own domain is incomplete:

1. **Correctness and testability.** Test-driven where the domain allows it. Tests that would fail against a plausible broken implementation, not tests that merely execute the happy path.
2. **Failure behavior.** Timeouts, retries with backoff, idempotency, partial failure, degraded dependencies, and what the system does when a dependency is gone. An SLA is a statement about failure, not about success.
3. **Security.** Trust boundaries, authentication and authorization, untrusted input, secrets, and tenant isolation, expressed as rules rather than reminders.
4. **Observability.** New failure modes must be diagnosable in production. Logs, metrics, traces, and their contracts — not "add logging".
5. **Concurrency and load.** Behavior under many simultaneous requests: connection pools, lock contention, N+1 access, cache semantics, backpressure, and load shedding.
6. **Clean code, SOLID, and appropriate design patterns.** Applied where they earn their place, never as decoration.
7. **Algorithm and data-structure choice.** Stated complexity budgets, and a deliberate choice rather than the first structure that came to mind.
8. **Configurability.** Behavior that varies by environment or scale is configurable, with safe defaults and validation at the boundary — not hardcoded, and not configurable for its own sake either.
9. **Speed of development and debuggability.** The guidance must make an agent fast, not merely careful. A skill that makes correct work slow will be bypassed.
10. **Documentation.** What shipped, how it is operated, and how it fails.

**Two standing preferences that cut across all of the above.** First, prefer official capabilities of a tool or framework and wrap them, rather than reimplementing them; a wrapper around an official mechanism survives upgrades, a reimplementation does not. Second, uniformity matters more than local optimality: all agents should develop in one recognisable style, because inconsistency across services costs more than any single clever local choice saves.

---

## 3. The upgrade standard

Every skill gets the same treatment. The first eight items are defect classes that appeared in nearly every one of the seven already done — check all of them every time.

1. **Stale model pins.** Any hardcoded model name goes stale silently and gets copied forward because it looks authoritative. Replace with a pointer to `alaa-prompting-guide` and describe lanes by the kind of judgment they need.
2. **Wrong trigger syntax.** Codex is `$name`, Claude Code is `/name`. Cross-runtime skills give both forms. `$alaa-cc-orchestrator` is the specific error to grep for.
3. **Duplication between the body and references.** State each instruction exactly once. This is measurable, not stylistic: on the current GPT generation leaner prompts scored 10–15% higher while cutting tokens 41–66%.
4. **Project-specific content in an always-loaded body.** Move it to a reference that loads only when that stack is involved. Preserve it completely — operational detail from real sessions is expensive to rediscover.
5. **Long numbered procedures nobody reads in order.** Restructure recovery-style content by failure class: symptom, diagnosis, smallest retry, escalation.
6. **Descriptions that only say when to use.** A description without a "do not use for" clause over-triggers.
7. **Fragile tooling.** `Path(__file__).parents[N]` breaks when a skill moves; temp directories created inside the repository fail on read-only mounts.
8. **Shipped `__pycache__`.** Delete before packaging.

Then, new in this round:

9. **Measure the skill against section 2.** Name the gaps explicitly in your report rather than quietly filling some and skipping others.
10. **Shrink where possible.** If the same or better outcome can be had from a shorter body, shorten it. Buy space by moving detail into references, not by deleting rules.
11. **Check the companion boundary.** Every skill should name what it does *not* own and which skill does. Overlap between skills is where agents get inconsistent.

---

## 4. Candidate new skills — verify before building

The goals in section 2 imply capabilities that may not exist yet. **These are candidates, not conclusions.** Before creating any of them, read `alaa-project-constitution`, `alaa-controlled-ops`, `alaa-services-contract`, and `service-runtime-kit-governance` — some of this ground may already be covered, and extending an existing skill beats adding a competing one.

| Candidate | Fills | Check first whether it already lives in |
|---|---|---|
| `alaa-design-patterns` | Which pattern fits a situation, how to apply it, and — equally important — when not to. Over-patterning is a real failure mode. | `alaa-project-constitution`, the per-language clean-code skills |
| `alaa-algorithms-data-structures` | Choosing and implementing the right algorithm and structure, with stated complexity budgets and configurable tuning points | nothing obvious; likely a genuine gap |
| `alaa-system-design` | Designing and planning a service, subsystem, or class set *before* implementation, to the bar in section 2 | `alaa-services-contract`, `alaa-workflow`, `alaa-project-constitution` |
| `alaa-reliability-sla` | Error budgets, timeouts, retries, circuit breaking, backpressure, graceful degradation, idempotency | `alaa-controlled-ops`, `alaa-observability-soc` |
| `alaa-testing-strategy` | Cross-stack test design: layers, doubles, flake control, what must be covered for an SLA service | per-language skills, `golang-testing` |

If a candidate turns out to be genuinely missing, build it to the same standard as the seven already done, and add it to the relevant cluster's routing.

---

## 4b. Vendored packs — read, route to, never edit

`D:\Sohrab\Project\skills` is a git repository, and `vendor/` holds **git subtrees pulled from upstream projects**, listed in `vendor/subtrees.json`:

| Subtree | Upstream | Skills |
|---|---|---|
| `cc-skills-golang` | `github.com/samber/cc-skills-golang` | 46 (`golang-*`) |
| `basic-memory` | upstream | 19 |
| `openfga-agent-skills` | `github.com/openfga/agent-skills` | 1 |
| `skill-temporal-developer` | upstream | 1 |
| `claude-plugins-official` | Anthropic, pinned commit | — |
| `knowledge-work-plugins` | Anthropic, pinned commit | — |

**Do not upgrade or edit anything under `vendor/`.** A subtree is periodically re-pulled from its upstream; local edits either collide on the next pull or are silently overwritten. Work spent there is work you will lose.

The correct pattern is to wrap rather than fork. Your own `alaa-*` skill owns the opinion — the quality bar from section 2, the house conventions, the routing — and points into the vendored skill as reference material for mechanics the upstream already documents well. That is the same "use the official capability and wrap it" preference stated in section 2, applied one level up.

Two consequences for the batch plan:

- **Batch 3 is resolved.** Upgrade only `alaa-golang`, `alaa-golang-clean-code-principles`, `alaa-golang-fiber`, and `alaa-go-chi-development`. The 46 vendored `golang-*` skills stay untouched; your four route into them. The most valuable work in that batch is deciding which decisions your skills own versus which they delegate upstream, and making the boundary explicit — the upstream pack has skills for design patterns, data structures, concurrency, performance, testing and observability that your skills should route to rather than restate.
- **`alaa-basic-memory-os` in Batch 8** sits over the vendored `basic-memory` pack and follows the same rule.

## 5. Batch plan

Sixty-three skill directories now sit in `skills/sohrab/`: fifty-one assigned to the eight batches below, seven rebuilt before the programme started (section 1), and five created by the programme itself and therefore already at standard — `alaa-reliability-sla`, `alaa-testing-strategy`, `alaa-system-design`, `alaa-algorithms-data-structures`, and `alaa-keyset-pagination`. Nothing under `vendor/` is in scope. Group them by shared context so one session's research serves every skill in it.

### Execution model: one batch at a time, in the numbered order

This programme is being run sequentially — one chat per batch, the next started only after the previous is committed. The numbers below **are** the running order. An earlier draft of this document described five parallel waves; that framing is retired, because it never matched how the work is actually done and it invited a reader to start two batches that share a rule.

### What has already run

| Batch | Status |
|---|---|
| 1 — Doctrine and cross-cutting standards | completed 2026-07-25 |
| 2 — PHP and Laravel | completed 2026-07-26 |
| 3 — Go | in flight as of 2026-07-26 |

### Renumbering, 2026-07-26

Batches 4 through 8 were reordered after Batch 2 finished, because the original wave plan put the platform contracts before the language batches and that ordering had already been overtaken by events. Batches 1, 2 and 3 keep their numbers and memberships; only the three below move.

| Was | Is now | Subject | Why it moved |
|---|---|---|---|
| 4 | **4** | Data and storage | unchanged |
| 7 | **5** | Messaging, integrations, and trust | a platform contract; must be settled before the frontend batch consumes its trust boundary |
| 5 | **6** | Frontend | a stack batch; consumes the two platform contracts above |
| 6 | **7** | Infrastructure and delivery | consumes build and runtime conventions from every stack batch, so it goes after all of them |
| 8 | **8** | Observability, documentation, knowledge | unchanged; still last |

A note for anyone reading older material: the memory topic files are named for the batch that wrote them, and batches 1–3 are unaffected, so no existing name collides with this renumbering.

### Why this order

Three rules produce it, and each is a dependency rather than a preference.

**Platform contracts before the stacks that obey them.** `alaa-data-layer` carries a repository-pattern gate and `alaa-trust-gateway-auth` a trust boundary that stack skills point at rather than restate. Batch 6 (Frontend) has not run yet, so it can still consume them in the intended order.

**Stacks before infrastructure.** Batch 7 owns how a gate is *expressed* on a runner and in a container; the stack batches own *what* the gate is. The boundary settled in Batch 2 — a stack skill owns gates and predicates and emits no provider YAML, the platform skill owns the YAML and decides no gate — only works if the stack side is written first. This is also why Frontend and Infrastructure must never run at the same time: `alaa-frontend-devops` and `alaa-gitlab-ci-cd` plus `alaa-docker-production` would otherwise decide the same ownership question independently.

**Documentation last.** Batch 8 owns `README.md` and the repository-level cleanup, so it must see the final inventory.

**One consequence to carry into Batches 4 and 5.** They are being rewritten *after* two batches that already point into them. Batch 2 cites `alaa-data-layer references/50-redis-laravel-octane.md` "Step 0" and `alaa-trust-gateway-auth` by name. Before renaming or restructuring a reference file, grep `skills/sohrab/` for inbound pointers to it; keep the filename where that is possible, and where it is not, list every pointer the change breaks in the final report rather than editing a file outside the batch. Batch 8 runs a link check over the whole tree at the end as the backstop.

### If two batches are ever run at once

Not recommended while the order above holds, but if it happens: 4 and 5 are disjoint from each other and from 6; 6 and 7 are **not** disjoint and must never overlap; 8 runs alone. Inside any concurrent run the four rules below are what keep it safe.

### Rules that hold whether batches run one at a time or not

- **Disjoint folders only.** Do not let a session edit a skill outside its batch — if it finds a defect elsewhere, it reports it rather than fixing it.
- **Nobody but the coordinator edits shared files.** `README.md`, `AGENTS.md` and this document belong to the human between batches, and to Batch 8 at the end.
- **Commit between batches, not during.** Concurrent sessions writing the same git repository is how a file silently reverts. Committing from the host is faster and more reliable than committing through a mounted device bridge, where `git` on this repository regularly exceeds a 45-second tool ceiling and can leave a stale `index.lock` it has no permission to remove.
- **Learnings travel through project memory, not through this file.** Each batch writes its own topic file named for its batch and adds one line to the memory index.

### Batch 1 — Doctrine and cross-cutting standards *(done)*
`alaa-project-constitution`, `alaa-services-contract`, `alaa-security-review`, `alaa-observability-soc`, `alaa-controlled-ops`, `service-runtime-kit-governance`
Plus: decide and build the section 4 candidates.
Deliverable beyond the skills themselves: a single named owner for the section 2 quality bar that every other skill can point at instead of restating.

### Batch 2 — PHP and Laravel *(done)*
`alaa-php-clean-code`, `alaa-laravel-architecture`, `alaa-octane-performance`, `alaa-laravel-job-rabbitmq`, `alaa-laravel-public-api-contract-pack`, `alaa-laravel-upgrade-all-packages`, `alaa-cicd-laravel-postgres`, `alaa-permission-generator`

### Batch 3 — Go *(in flight)*
`alaa-golang`, `alaa-golang-clean-code-principles`, `alaa-golang-fiber`, `alaa-go-chi-development`
The 46 vendored `golang-*` skills are out of scope — see section 4b. Define the delegation boundary instead of restating what upstream already covers.

### Batch 4 — Data and storage
`alaa-data-layer`, `alaa-mongodb-patterns`, `alaa-partitioned-table-fk-audit`, `alaa-crockford-base32-codecs`, `clickhouse-performance-schema-ops`
Keep the repository-pattern gate in `alaa-data-layer references/50-redis-laravel-octane.md`: Batch 2 points at it by path and by section name.

### Batch 5 — Messaging, integrations, and trust *(was Batch 7)*
`alaa-async-messaging`, `alaa-trust-gateway-auth`, `alaa-bale-provider`, `alaa-sms-provider-mediana`, `tusd-upload-platform`, `jitsi-platform-architect`
`alaa-async-messaging` is named by `alaa-services-contract` as the owner of prefetch values, acknowledgement mechanics, publisher confirms and DLQ replay, and its four reference files contain none of those words. It also restates retry and idempotency doctrine without citing `alaa-reliability-sla`. Nominally the owner, factually empty — fix that first.

### Batch 6 — Frontend *(was Batch 5)*
`alaa-frontend-developer`, `alaa-vue-typescript-clean-code`, `alaa-quasar-app-vite-v3`, `alaa-ui-ux-design-system`, `alaa-frontend-devops`, `alaa-frontend-doc-annotations`, `alaa-mono-package`, `alaa-indexeddb-browser-storage`, `alaa-shaka-player`
`alaa-vue-typescript-clean-code` carries a stale hardcoded model name.

### Batch 7 — Infrastructure and delivery *(was Batch 6)*
`alaa-docker-production`, `alaa-k8s-helm`, `alaa-gitlab-ci-cd`, `alaa-haproxy`, `alaa-makefile`, `caas-arvan-kuber`, `ansible-generator`, `ansible-validator`
Three stale hardcoded model names live here: `alaa-gitlab-ci-cd`, `alaa-k8s-helm`, `caas-arvan-kuber`. `alaa-gitlab-ci-cd` must also absorb the stack-versus-platform boundary Batch 2 settled: it owns YAML expression and decides no gate.

**Added at the close of Batch 6, 2026-07-28 — decision D8.** The stack-versus-platform boundary is no longer a plan to be settled; it is written and binding, and Batch 7 writes only the reciprocal half. `alaa-frontend-devops` owns the frontend delivery gate register — for each gate, the predicate it asserts, the command that evaluates it, and the artifact it inspects — and writes no provider YAML and no Dockerfile. Against that, `alaa-gitlab-ci-cd` owns how a gate is expressed on a runner and decides no gate; `alaa-docker-production` owns how the build and runtime images and any Compose file are expressed and decides no gate; and `alaa-haproxy` owns how a cache or routing decision is expressed as a directive and decides no policy. Batch 6 wrote its side into `alaa-frontend-devops/SKILL.md`; each of the three platform skills must now state its own half in its own words, because a boundary asserted from one side only is a boundary the other side has not agreed to. **The line-by-line disposition of what moved out of `alaa-frontend-devops/references/20-ci-docker-and-cache.md` is in Appendix F §A of `UPGRADE-BATCH-6-ANALYSIS.md`, at the root of this directory, and that file is the input Batch 7 must read before touching any of the three skills.**

What routes to whom is already decided, so no Batch 7 session needs to re-derive it. Cache-key syntax, the job graph, `rules:` and `needs:`, artifact retention and the runner image reference go to `alaa-gitlab-ci-cd`. Dockerfile layer ordering, multi-stage separation and image minimisation go to `alaa-docker-production`, which also owns Compose authorship. Proxy and cache directives go to `alaa-haproxy`, while the caching *policy* stays with the frontend skill because the policy follows from content hashing and the build owns that. CDN origin bucket, lifecycle and invalidation go to `alaa-minio-object-storage` and `alaa-arvan-object-storage`.

Two live findings are waiting for this batch. First, `entekhabat-front/docker-compose.yml` uses the service-level `env_file:` key, which Compose interpolation never reads, and declares no `${VAR:?}` at all — a live instance of the fail-closed interpolation invariant ratified 2026-07-28, and the fix belongs to `alaa-docker-production`. Second, `alaa-frontend-devops` now ships `scripts/verify-artifact-contract.mjs`, and its findings on the live `client` — no client-prefix convention, and no build provenance in any emitted tree — are the concrete gap this batch's container and pipeline work has to close.

### Batch 8 — Observability, documentation, and knowledge
`alaa-signoz-clickhouse-docs`, `vector-rust-observability-pipelines`, `alaa-docs-farsi`, `alaa-postman-collections`, `alaa-basic-memory-os`
Plus the repository-level cleanup in section 6, and a link check that every cross-skill path in `skills/sohrab/` resolves.

**Added at the close of Batch 6, 2026-07-28 — decision D8.** Five obligations beyond the membership above.

**Count deterministic checkers per skill, alongside the link check.** Batch 6 shipped nine new ones — `check-upstream-versions.mjs`, `check-frontend-versions.mjs`, `query-installed-quasar-api.mjs`, `check-design-system.mjs`, `verify-artifact-contract.mjs`, `check-annotations.mjs`, `verify-package-entrypoints.mjs`, `check-shaka-api.mjs` and `normalization-conformance.sh` — and every one of them found a real defect on its first execution against the live `client`. A skill whose rules have no tool that reports a violation is shipping preferences, not rules. Run this as a survey across the whole tree: per skill, how many executable checks it ships, and what each of them asserts.

**The router convention is inconsistent fleet-wide, and Batch 6 could not fix it outside its own membership.** Twenty-eight of the sixty-eight skill directories carry a `references/00-topic-map.md` and forty do not. Among the ones this programme has touched, `alaa-observability-soc`, `alaa-reliability-sla`, `alaa-services-contract`, `alaa-permission-generator` and eight of the nine Batch 6 skills have one; `alaa-testing-strategy`, `alaa-security-review`, `alaa-keyset-pagination`, `alaa-trust-gateway-auth`, `alaa-low-noise`, `alaa-crockford-base32-codecs`, `alaa-algorithms-data-structures`, `alaa-frontend-doc-annotations` and the new `alaa-input-normalization` do not. Two corrections against the list as it was first drafted, both verified on disk on 2026-07-28: `alaa-algorithms-data-structures` does **not** carry one, and the ninth Batch 6 skill, `alaa-frontend-doc-annotations`, does not either. Decide whether the convention is mandatory or optional and make the tree say the same thing either way.

**A new skill exists that both READMEs and the repository index must gain**: `alaa-input-normalization`. Neither `README.md` nor `README.fa.md` mentions it — verified on 2026-07-28 — and section 6 already assigns both files to this batch.

**Batch 6 filed 21 RFCs across 15 repositories, all deliberately uncommitted.** They sit under each repository's `docs/requests-for-change/` (or `docs/change-requests/` in `alaa-go-chi` and `client`), timestamped `20260728-221605` apart from the `alaa-go-chi` one. Seven of them are in `client` — build provenance and workspace integrity, design-system tokens and RTL, the IndexedDB foundation, input-normalization adoption, the open phone-grammar divergence, the permission-bitmap assumption with no expiry, and Shaka API drift — and they name defects a later batch should read rather than re-derive.

**`alaa-frontend-developer` was to retire its duplicate `scripts/check-upstream-versions.mjs`** in favour of the `alaa-quasar-app-vite-v3` copy, which now has `--help`, `--self-test`, a per-request timeout and `HTTPS_PROXY`/`NO_PROXY` handling — the pattern every other version-checking script in the tree should adopt. The retirement did not land: on 2026-07-28 the duplicate was still at `alaa-frontend-developer/scripts/check-upstream-versions.mjs`, `alaa-frontend-developer/SKILL.md` and its `references/90-upstream-deltas-and-maintenance.md` still invoke it locally, and `alaa-quasar-app-vite-v3/references/91-agent-authoring-and-dual-runtime.md` already asserts that its copy is the fleet's only one. Finish the retirement and make the two statements agree.

---

## 6. Known repository-level defects

**`skills/sohrab/README.md` does not match the directory.** Its skill map lists roughly twenty skills that are not on disk — `azure-pipelines-*`, `fluentbit-*`, `github-actions-*`, `jenkinsfile-*`, `terraform-*`, `terragrunt-*`, `promql-*`, `logql-generator`, `loki-config-generator` — and omits at least thirteen that are: `alaa-project-constitution`, `alaa-basic-memory-os`, `alaa-controlled-ops`, `alaa-indexeddb-browser-storage`, `alaa-ui-ux-design-system`, `alaa-sms-provider-mediana`, `alaa-bale-provider`, `alaa-partitioned-table-fk-audit`, `alaa-signoz-clickhouse-docs`, `alaa-laravel-upgrade-all-packages`, `alaa-go-chi-development`, `alaa-golang-clean-code-principles`, `alaa-golang-fiber`. An index that lies is worse than no index, because agents route from it. Fix it in Batch 8, once the real inventory is settled.

**`agents/openai.yaml` coverage.** The README states every shipped skill has one. Verify per batch rather than assuming.

**Root `AGENTS.md` and `CLAUDE.md` are byte-identical duplicates.** One runtime reads each, so two files are legitimate, but keeping two copies in sync by hand guarantees they drift. Decide on a single source with a generation or link step. Batch 1 did not cover it, so it falls to Batch 8 with the rest of the repository-level cleanup. `alaa-prompting-guide/references/70-agent-instruction-files.md` discusses the trade-offs.

**`install-skills.md` is correct and worth treating as authoritative** for install paths — it already targets `~/.codex/skills`, which is the field-verified location. If any skill's own installation docs disagree with it, the skill is wrong, not this file.

---

## 7. Definition of done, per skill

A skill is finished when all of these hold:

- The frontmatter description says what it does, when to use it, and when not to.
- The body holds only what is always needed; everything else is one hop away in `references/`.
- Every instruction appears exactly once across the whole skill.
- No hardcoded model name, no wrong trigger syntax, no stale tool version.
- It answers the section 2 questions for its own domain, or explicitly names which it does not own and which skill does.
- Every rule survives the wording test: could a competent agent follow this sentence exactly and still do the wrong thing? No preference verbs where a constraint was meant, no rule without a stated scope, no abstract noun standing in for an observable condition, no prohibition without its positive replacement. The prose in these files is the executable logic, so phrasing defects become behaviour defects on every future run. `alaa-prompting-guide/references/60-skill-authoring.md` has the full treatment.
- Its bundled scripts run on **Windows**, not only in the cloud container, and any test suite passes from a fresh checkout. Two Windows-only defect classes have already shipped from this programme: `new URL(import.meta.url).pathname` yields `/D:/...`, which Node cannot spawn as a path — use `fileURLToPath(import.meta.url)` — and a shell driver writing CRLF leaves a carriage return on the last field of every parsed line, so every comparison fails while the rendered bytes look identical.
- **The repository's plugin validation passes on the batch's own output, run before the batch is declared closed.** Two rules it enforces are not in the Agent Skills specification and are not discoverable by reading a skill: a `description` may contain no angle brackets at all — `<video>` written as prose is rejected as an XML tag, so write "a plain HTML video element" instead — and its character count for the 1024 limit exceeds a YAML-parsed count by at least thirty, by a rule nobody has established yet. **Keep every description at or below 900 characters** until someone measures the real rule from a second data point.
- It is not larger than it was, unless it gained a genuinely new capability — and if it did, say so.

---

## 8. Working method

Deliver by writing files into the skill directories on disk. The device mount forbids `unlink`, so `unzip -o` fails; extract with a Python loop that truncates in place, or commit files individually. Delete nothing on the user's disk — move retired files into the existing `_to_delete/` folder at the repository root and say so.

**The repository is under git.** That is the rollback path, and it is also a hazard worth naming: during the first upgrade round a single file reverted to its pre-upgrade state between sessions, almost certainly from a `git restore` or an editor undo. Verify what actually landed rather than trusting a successful write, and at the end of a batch confirm the tree state before declaring the batch done.

The user's preferences: no `Co-Authored-By` tags in commits, ever. Replies in fluent English prose with a clear through-line unless the user writes otherwise. When a decision is genuinely the user's, give a short Persian block stating the situation, the problem, what is being asked of them, your own recommendation with its reasoning, and the trade-offs of each option.

---

## 9. Session prompt

Paste this into a fresh session, changing only the `BATCH` line.

```text
/alaa-cc-orchestrator  Advisor mode first. Orchestrator mode only after I approve the analysis.

GOAL: upgrade one batch of my skills under D:\Sohrab\Project\skills\skills\sohrab\
Batch 5 — Messaging, integrations, and trust
READ FIRST, before anything else:
1. D:\Sohrab\Project\skills\skills\sohrab\UPGRADE-CARRYOVER.md — the working contract.
   Section 2 is the quality bar, section 3 the upgrade standard, section 4 the candidate
   new skills, section 4b the vendored packs, section 5 the running order and this batch's
   membership, section 7 the definition of done.
2. Project memory — model and effort decisions, the Codex skill install path, the recurring
   defect classes, the vendored-pack rule, and why a skill's prose is its executable logic.
   
PHASE 1 — analyse, then stop.
Read every skill in this batch in full: SKILL.md, all references, all scripts.
Write the full analysis to a single draft file in English, at the root of the skills
directory above, as the working input Phase 2 will execute from. Name it
UPGRADE-BATCH-<N>-ANALYSIS.md, where <N> is the batch number declared at the top of this
prompt. That file — not the terminal — holds: one table for
the whole batch showing, per skill, which of the ten criteria in section 2 it already
satisfies, which it fails, and which it should not own because another skill does; the defect
classes from section 3 that you actually found; and one short paragraph per section 4
candidate skill saying whether it is genuinely missing or already covered — grounded in what
you read, not in what the names suggest.
Also decide whether any new skill is genuinely required to close a gap you actually observed.
Propose a new skill only when an existing skill cannot own the gap without violating its own
boundary. Name the gap and the evidence for it. Inventing a skill to look thorough is a
failure of this step; concluding that no new skill is needed is a valid and welcome outcome.
In the terminal, do not reprint the analysis. Give me instead a short, readable Persian
briefing — concise, but written in complete, connected sentences I can follow — with exactly
three sections:
1. In-scope work you have decided on yourself and will carry out.
2. In-scope proposals that wait on my decision — each with your own recommendation and the
   reason for it.
3. Out-of-scope items that will need my follow-up or my decision later.
Create no file other than that draft, and change no skill file in this phase. End your turn
and wait for my approval.

PHASE 2 — execute, after I approve.
Rewrite skill by skill against the definition of done in section 7, working from the draft
file you produced in Phase 1 and from whatever I approved or corrected in my reply.

HARD RULES
- Speak to me in the terminal in fluent, natural Persian. Everything you write into a file —
  skills, prompts, references, scripts, commit messages, the Phase 1 draft — is in fluent,
  natural English. This split is absolute: no Persian inside artifacts, no English-only
  reporting to me.
- Never edit anything under vendor/. Those are upstream git subtrees. Wrap them from the
  owning alaa-* skill instead. See section 4b.
- Never edit a skill outside this batch, and never edit README.md or UPGRADE-CARRYOVER.md.
  Other batches may be running against the same repository. If you find a defect outside
  your batch, report it to me instead of fixing it.
- Never hardcode a model name. Route model and effort questions to /alaa-prompting-guide
  and its references/50-effort-and-thinking.md.
- Every instruction appears exactly once across a skill. The body holds only what is always
  needed; detail lives one hop away in references/.
- Trigger syntax: $name for Codex, /name for Claude Code. Cross-runtime skills give both.
- Apply the wording test to every rule you write: could a competent agent follow this
  sentence exactly and still do the wrong thing? No preference verbs where a constraint was
  meant, no rule without a stated scope, no abstract noun standing in for an observable
  condition, no prohibition without its positive replacement. In these files the prose is
  the executable logic. See /alaa-prompting-guide references/60-skill-authoring.md.
- A skill body must not grow unless it gained a genuinely new capability. If it did, say which.
- Delete nothing on my disk. Move retired files to the repository's _to_delete/ folder and
  tell me what you moved.
- Commit messages carry no Co-Authored-By tag.

DELEGATION
Skill authoring is a judgment lane, not a routine one — every writing lane in this programme
runs on the escalated implementer, and the named criterion is "authoring an artifact whose
deliverable is judgment itself". Do not dispatch skill rewrites to the default implementer.
Spawn one agent per skill or per lane, never several for the same one, and never a subagent
whose only job is to re-check another subagent. Independent lanes go out together.
DELIVERY
Write files directly into the skill directories. My mount forbids unlink, so `unzip -o` fails —
extract with a Python loop that truncates each target in place. The repository is under git;
verify what actually landed rather than trusting a successful write, and confirm the tree
state before declaring the batch done.
FINISH WITH — in Persian, in the same three-section shape as Phase 1
1. What each skill gained, and what gaps remain and why.
2. Any decision that is mine to make.
3. A project-memory topic file named for this batch, holding what a later wave needs from
   it: ownership boundaries you settled, conventions you established, and anything you
   found that contradicts the carry-over document. Write this file in English. Do not
   rewrite the memory index while other batches may be running.
```
