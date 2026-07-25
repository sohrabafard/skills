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

Fifty-one skills remain in `skills/sohrab/`: 43 `alaa-*` plus 8 others in the same namespace. Nothing under `vendor/` is in scope. Group them by shared context so one session's research serves every skill in it.

**Run Batch 1 first and alone.** It defines the doctrine every later batch references. Running a domain batch before it means each domain invents its own version of the quality bar, which is exactly the inconsistency to avoid.

### Batch 1 — Doctrine and cross-cutting standards *(do first)*
`alaa-project-constitution`, `alaa-services-contract`, `alaa-security-review`, `alaa-observability-soc`, `alaa-controlled-ops`, `service-runtime-kit-governance`
Plus: decide and build the section 4 candidates.
Deliverable beyond the skills themselves: a single named owner for the section 2 quality bar that every other skill can point at instead of restating.

### Batch 2 — PHP and Laravel
`alaa-php-clean-code`, `alaa-laravel-architecture`, `alaa-octane-performance`, `alaa-laravel-job-rabbitmq`, `alaa-laravel-public-api-contract-pack`, `alaa-laravel-upgrade-all-packages`, `alaa-cicd-laravel-postgres`, `alaa-permission-generator`

### Batch 3 — Go
`alaa-golang`, `alaa-golang-clean-code-principles`, `alaa-golang-fiber`, `alaa-go-chi-development`
The 46 vendored `golang-*` skills are out of scope — see section 4b. Define the delegation boundary instead of restating what upstream already covers.

### Batch 4 — Data and storage
`alaa-data-layer`, `alaa-mongodb-patterns`, `alaa-partitioned-table-fk-audit`, `alaa-crockford-base32-codecs`, `clickhouse-performance-schema-ops`

### Batch 5 — Frontend
`alaa-frontend-developer`, `alaa-vue-typescript-clean-code`, `alaa-quasar-app-vite-v3`, `alaa-ui-ux-design-system`, `alaa-frontend-devops`, `alaa-frontend-doc-annotations`, `alaa-mono-package`, `alaa-indexeddb-browser-storage`, `alaa-shaka-player`

### Batch 6 — Infrastructure and delivery
`alaa-docker-production`, `alaa-k8s-helm`, `alaa-gitlab-ci-cd`, `alaa-haproxy`, `alaa-makefile`, `caas-arvan-kuber`, `ansible-generator`, `ansible-validator`

### Batch 7 — Messaging, integrations, and trust
`alaa-async-messaging`, `alaa-trust-gateway-auth`, `alaa-bale-provider`, `alaa-sms-provider-mediana`, `tusd-upload-platform`, `jitsi-platform-architect`

### Batch 8 — Observability, documentation, and knowledge
`alaa-signoz-clickhouse-docs`, `vector-rust-observability-pipelines`, `alaa-docs-farsi`, `alaa-postman-collections`, `alaa-basic-memory-os`
Plus the repository-level cleanup in section 6.

---

## 6. Known repository-level defects

**`skills/sohrab/README.md` does not match the directory.** Its skill map lists roughly twenty skills that are not on disk — `azure-pipelines-*`, `fluentbit-*`, `github-actions-*`, `jenkinsfile-*`, `terraform-*`, `terragrunt-*`, `promql-*`, `logql-generator`, `loki-config-generator` — and omits at least thirteen that are: `alaa-project-constitution`, `alaa-basic-memory-os`, `alaa-controlled-ops`, `alaa-indexeddb-browser-storage`, `alaa-ui-ux-design-system`, `alaa-sms-provider-mediana`, `alaa-bale-provider`, `alaa-partitioned-table-fk-audit`, `alaa-signoz-clickhouse-docs`, `alaa-laravel-upgrade-all-packages`, `alaa-go-chi-development`, `alaa-golang-clean-code-principles`, `alaa-golang-fiber`. An index that lies is worse than no index, because agents route from it. Fix it in Batch 8, once the real inventory is settled.

**`agents/openai.yaml` coverage.** The README states every shipped skill has one. Verify per batch rather than assuming.

**Root `AGENTS.md` and `CLAUDE.md` are byte-identical duplicates.** One runtime reads each, so two files are legitimate, but keeping two copies in sync by hand guarantees they drift. Decide on a single source with a generation or link step, and cover it when Batch 1 reaches instruction-file doctrine. `alaa-prompting-guide/references/70-agent-instruction-files.md` discusses the trade-offs.

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
- Its bundled scripts run, and any test suite passes from a fresh checkout.
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

BATCH: 1 — Doctrine and cross-cutting standards

READ FIRST, before anything else:
1. D:\Sohrab\Project\skills\skills\sohrab\UPGRADE-CARRYOVER.md — the working contract.
   Section 2 is the quality bar, section 3 the upgrade standard, section 4 the candidate
   new skills, section 4b the vendored packs, section 5 this batch's membership,
   section 7 the definition of done.
2. Project memory — model and effort decisions, the Codex skill install path, the
   recurring defect classes, and the vendored-pack rule.

PHASE 1 — analyse, then stop.
Read every skill in this batch in full: SKILL.md, all references, all scripts. Then give me
one table for the whole batch showing, per skill: which of the ten criteria in section 2 it
already satisfies, which it fails, and which it should not own because another skill does.
Add the defect classes from section 3 that you actually found. Then say, in one short
paragraph each, whether the section 4 candidate skills are genuinely missing or already
covered — grounded in what you read, not in what the names suggest.
Change no file in this phase. End your turn and wait for my approval.

PHASE 2 — execute, after I approve.
Rewrite skill by skill against the definition of done in section 7.

HARD RULES
- Never edit anything under vendor/. Those are upstream git subtrees. Wrap them from the
  owning alaa-* skill instead. See section 4b.
- Never hardcode a model name. Route model and effort questions to /alaa-prompting-guide
  and its references/50-effort-and-thinking.md.
- Every instruction appears exactly once across a skill. The body holds only what is always
  needed; detail lives one hop away in references/.
- Trigger syntax: $name for Codex, /name for Claude Code. Cross-runtime skills give both.
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

FINISH WITH
What each skill gained, what gaps remain and why, any decision that is mine to make, and
what the next batch inherits from this one.
```
