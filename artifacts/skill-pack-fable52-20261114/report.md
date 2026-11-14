# Skill pack upgrade for Claude Fable 5.2 (2026-11-14)

This record covers one engagement: the first-party pack under `skills/sohrab/` was reviewed and repaired for Claude Fable 5.2 and the current Codex models, and the managed specialist agents received a uniform return contract. The plan is `beads:alaa-2uo9j`. This is a dated maintenance record, not an installed skill instruction. Verify current repository and upstream facts before you reuse a conclusion.

## Outcome

- `alaa-prompting-guide` registers `claude-fable-5-2` as the active Fable member, owns a Fable 5.2 reference, and carries a carry-over review for a new model generation.
- Three stale Claude Code runtime facts are corrected: subagent nesting is on by default, the per-invocation model accepts a family alias only, and a Fable 5.2 main model accepts only a Fable 5.2 advisor.
- Every managed role in both orchestrators returns a fixed first line (`VERDICT:` or `STATUS:`), states its completion condition, reports a missing dispatch input as `STATUS: BLOCKED`, and lists unassessed scope. The agent catalog owns the lead's routing on that line.
- Claude implementer profiles deny `Agent`, so a lane cannot spawn subagents outside the lead's allocation.
- Two always-preloaded bodies are smaller with no text lost: `alaa-testing-strategy` (32 KB to 27 KB) and `alaa-services-contract` (13 KB to 8.5 KB).
- Every other first-party skill was audited under a closed rubric by nine edit lanes. Section *Lane results* lists what changed and what was only audited.

## Evidence

Official pages fetched on 2026-11-14:

| Source | Used for |
|---|---|
| `https://www.anthropic.com/claude-fable-and-mythos-5-2` | Launch facts, pricing, advisor and orchestrator roles |
| `https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-2` | Effort calibration, early stop, approvals, code ownership, progress text, subagents, accumulated caution, carried-over prompts, final reports, refusals |
| `https://platform.claude.com/docs/en/models/fable-5-2/migration-guide` | Model ID, prefix check, thinking-block compatibility, advisor pairing, data retention |
| `https://platform.claude.com/docs/en/models/overview` | IDs, API default effort, thinking mode |
| `https://platform.claude.com/docs/en/build-with-claude/effort` | Supported levels and per-model guidance |
| `https://platform.claude.com/docs/en/about-claude/models/choosing-a-model` | Selection matrix |
| `https://code.claude.com/docs/en/model-config` | Claude Code default effort, minimum version 2.1.321, `fable` alias (first 100,000 characters read) |
| `https://code.claude.com/docs/en/sub-agents` | Frontmatter fields, model and effort precedence, nesting default (first 100,000 characters read) |
| `https://code.claude.com/docs/en/advisor` | Accepted pairs, subagent inheritance |
| `https://developers.openai.com/api/docs/guides/latest-model`, `https://learn.chatgpt.com/docs/model-selection` | No Codex model newer than the 2026-11-03 record; the Codex policy is unchanged |

Limits: the Fable 5.2 behaviour statements are vendor test results. No local calibration ran. The system card was not read. No installed agent or skill copy was changed, so nothing in this record is activated on any machine.

## Decisions

| Decision | Reason |
|---|---|
| Fable 5.1 moves to history; Fable 5.2 is the active Fable member | The policy uses the newest verified member of a family; the `fable` alias now resolves to Fable 5.2 |
| The Claude dispatch default stays `claude-opus-5-5` at `medium` | The selection guide still starts most workloads on Opus 5.5; Fable 5.2 is for work that falls short there |
| The 20-word procedure-sentence rule becomes a default with an exception | The Fable 5.2 prompting page reports that a hard sentence cap makes prose choppy; a split must not separate a rule from its condition |
| Unobservable task controls are recorded as unknown and do not block a lane | A subagent cannot observe its invocation controls; the owner files already treat unknown identity as a reporting limit; the Fable 5.2 page reports needless approval stops when cautions pile up across agents |
| Implementers deny `Agent` | Nesting is on by default; the lead owns every dispatch and its task allocation |
| One `STATUS:` vocabulary (`COMPLETE`, `INCOMPLETE`, `BLOCKED`) for non-gate roles | It reuses the vocabulary the Ent specialist contract already used |
| No role was renamed, added or removed; both packs move to version 5.6.0 | The output contract of every role changed, and the version lets an installed copy be recognised as older than the source |
| Lane edits were limited to a closed rubric | The pack forbids growth without a capability and forbids editing a domain fact that the lane cannot verify |

## Closed rubric used by the edit lanes

R1 stale model or runtime fact. R2 standing delegation with no cost, criteria or inline case. R3 "never" on an action the agent must keep through approval. R4 thinking control in prose. R5 token budget shown to the agent. R6 wording-test failure. R7 expired or unscoped caution. R8 description defect. R9 router row that is not a condition. R10 duplicate owner inside a skill. The first seven are owned by `alaa-prompting-guide references/60-skill-authoring.md` *Carry-over review for a new model generation*.

A deterministic scan before dispatch found no R4, R5 or R7 signal outside the prompting guide, and one R1 signal (item 1 under *Proposals*).

## Lane results

Nine edit lanes ran as general-purpose subagents on Opus 5.5 at medium effort. Each lane held Beads ownership action `none` and made no commit. The lead reviewed each report and committed each lane.

| Lane | Skills | Edited | Audited only |
|---|---|---|---|
| C1 | alaa-workflow, alaa-low-noise, alaa-extract-agent-lessons | all three | none |
| C2 | alaa-testing-strategy, alaa-code-intelligence-routing, alaa-ponytail | all three | none |
| C3 | alaa-memory-os, alaa-repo-docs, alaa-project-constitution | all three | none |
| L1 | PHP and Laravel (11) | alaa-php-clean-code, alaa-octane-performance, alaa-phpantom, alaa-permission-generator, alaa-controlled-ops, alaa-mono-package | alaa-laravel-architecture, alaa-laravel-job-rabbitmq, alaa-laravel-public-api-contract-pack, alaa-laravel-upgrade-all-packages, alaa-cicd-laravel-postgres |
| L2 | Go and data (11) | alaa-golang, alaa-golang-clean-code-principles, alaa-golang-fiber, alaa-go-chi-development, alaa-partitioned-table-fk-audit | alaa-ent-go-orm-db, alaa-data-layer, alaa-mongodb-patterns, alaa-keyset-pagination, clickhouse-performance-schema-ops, alaa-crockford-base32-codecs |
| L3 | Frontend (9) | alaa-frontend-developer, alaa-frontend-devops, alaa-frontend-doc-annotations, alaa-vue-typescript-clean-code, alaa-ui-ux-design-system, alaa-indexeddb-browser-storage, alaa-input-normalization | alaa-quasar-app-vite-v3, alaa-shaka-player |
| L4 | Platform (12) | alaa-docker-production, alaa-k8s-helm, caas-arvan-kuber, alaa-gitlab-ci-cd, alaa-haproxy, alaa-haproxy-lua, alaa-bash-shell, alaa-makefile, ansible-generator, ansible-validator, service-runtime-kit-governance | jitsi-platform-architect |
| L5 | Contracts and doctrine (9) | alaa-services-contract, alaa-reliability-sla, alaa-observability-soc, alaa-system-design, alaa-algorithms-data-structures, vector-rust-observability-pipelines | alaa-security-review, alaa-trust-gateway-auth, alaa-signoz-clickhouse-docs |
| L6 | Storage, messaging, providers, tooling (11) | alaa-async-messaging, alaa-sms-provider-magfa, alaa-postman-collections, repository-tooling-capability-check | alaa-minio-object-storage, alaa-arvan-object-storage, tusd-upload-platform, alaa-bale-provider, alaa-sms-provider-mediana, alaa-legacy-path-map, alaa-codex-runtime-ops |

The lead edited `alaa-prompting-guide`, `alaa-cc-orchestrator` and `alaa-codex-orchestrator` directly, and relocated the two preloaded bodies. Most lane hits were description defects (R8), router rows that were not conditions (R9), and wording-test failures (R6). The lanes found three standing-delegation hits (R2) and six approval-rule hits (R3).

New capabilities that justify growth:

- `alaa-memory-os` and `alaa-extract-agent-lessons`: the shape of a stored caution and the rule for retiring one whose reason expired. `alaa-memory-os references/knowledge-shape.md` owns the shape.
- `alaa-low-noise`: progress text for an attended run and a final report a reader with no context can follow.
- Both orchestrators: the return header, completion conditions and `NOT ASSESSED` coverage for every role.
- `alaa-prompting-guide`: the Fable 5.2 reference and the carry-over review.

## Independent review

`alaa-instruction-reviewer` (Opus 5.5, medium, read-only) reviewed the prompting-guide change and the orchestrator change with the two relocations. Both first passes returned `CHANGES-REQUESTED`: nine findings and fourteen findings. Commits `82d22fa3` and `42ee52c5` repair them. The same reviewers ran a confirmation pass, and a third reviewer read the nine lane commits. Section *Review outcome* records the final verdicts.

## Proposals: reported, not changed

These need the owner's decision. No lane edited them.

1. `alaa-services-contract/SKILL.md` names a model and effort pair (`gpt-6.1-terra` at `high`, `opus` at `medium`) and requires delegation for `docs/PRODUCT_OVERVIEW.fa.md`. The same file says it names no model, and the pack assigns task allocation to the orchestrators. The paragraph also has no trigger, so it reads as an every-task obligation in a body that every implementer preloads.
2. `/alaa-controlled-ops` is cited as the owner of hook registration, shared configuration and commands that touch a shared system (`alaa-memory-os/SKILL.md`, two memory-os references, `alaa-golang/references/20-sohrab-companions.md`). That skill governs the `alaa/controlled-ops` Composer package.
3. `alaa-phpantom` holds machine paths (`SKILL.md`, `references/troubleshooting.md`, `README.md`, `.lsp.json`) against the no-machine-path rule. The `.lsp.json` command is functional, so a repair needs a tested replacement.
4. `alaa-project-constitution`: the template calls the 12 KiB and 160-line thin-charter figures targets, while `scripts/validate_constitution.py` rejects above them. The adapter text emitted into bound repositories tells agents to surface any conflict with repository truth before proceeding, which can stop every task on an obligation the code does not implement yet.
5. `alaa-php-clean-code`: the English-output rule is stated four times and conflicts with the `alaa-repo-docs` rule to preserve a document's language. Its `vendor/` reason describes this pack's subtrees, not a Laravel repository's Composer directory.
6. `alaa-keyset-pagination`: the body applies the skill to "any export or background traversal" and its *When NOT to use* excludes "an internal export or backfill".
7. `vector-rust-observability-pipelines`: the body allows an environment-variable credential under three conditions; `references/85-security-and-secrets.md` adds a fourth.
8. Stale citations and status: `alaa-bale-provider` and `alaa-sms-provider-mediana` cite line ranges in `alaa-services-contract` that moved; the registry marks Mediana inactive after the Magfa cutover; the Bale skill says the client "ships shortly". `alaa-haproxy/SKILL.md` hard-codes "3.4 is the current LTS". `alaa-makefile` says the Arvan Kubernetes version is pinned, and `caas-arvan-kuber` says no current server version is established. Arvan object-storage facts are past the skill's own 90-day re-read rule.
9. `caas-arvan-kuber`: `scripts/summarize-openapi.sh --check` exits 1 on a capability-matrix row that predates this work.
10. `service-runtime-kit-governance` routes generic Kubernetes and Helm work to `/caas-arvan-kuber`; the skills' own deciding test points to `/alaa-k8s-helm`.
11. `alaa-codex-runtime-ops`: three statements of the approval rule name different approvers.
12. `alaa-quasar-app-vite-v3` uses emoji markers in its Do and Don't pairs against the no-emoji rule, and states the package-manager rule in seven files.
13. Body-size candidates left in place: `alaa-testing-strategy` proof-level definitions and the exhaustive-tier rationale (checker-bound); `alaa-services-contract` product-overview paragraph and companion list; `alaa-trust-gateway-auth` ownership table; `alaa-sms-provider-magfa` tables (16 KB body with no references); `alaa-php-clean-code`, `alaa-laravel-job-rabbitmq`, `alaa-gitlab-ci-cd`, `alaa-memory-os` and `alaa-project-constitution` bodies above the validator's line target.
14. `alaa-code-intelligence-routing` and `alaa-ent-go-orm-db` use dense slash-joined noun stacks. The lanes found no ambiguous case beyond the ones they repaired; a full wording pass needs its own review.
15. Legacy dual-form call sites remain in files no lane edited. The pack converts them only in a file edited for another reason.
16. `docs/claude-model-migration.md` at the repository root still lists Fable 5.1; it is outside this engagement's scope.

## Pending actions that need authorization

- Install. The installed agent definitions and any non-symlinked skill copy are unchanged. `install-skills.md` owns the commands. Until an authorized install, sessions keep the previous agent definitions, including the old first-line labels.
- Push. The lane branch is merged locally only.
- Activation skew. After the merge the skills are live through the symlinked install, while the installed agent copies still hold version 5.5.0 text with the old first-line labels. An orchestrator run reports those roles as stale until the install.

## Validation observed

Run from the worktree with `PYTHONDONTWRITEBYTECODE=1`; section *Review outcome* records the final-candidate run.

- Root: `validate_sohrab_skill_pack.py`, `check_skill_index.py`, `check_fleet_references.py`, `check_lifecycle_contract.py`.
- `alaa-prompting-guide`: `check_claude_model_policy.py`, `check_codex_model_policy.py`, `check_rule_writer_grants.py`.
- Each orchestrator: `render_agents.py --check`, `validate_pack.py`, `check_agent_grants.py`, `check_agent_contracts.py`.
- `alaa-testing-strategy`: `check_execution_contracts.py`.
- Lane-run skill validators: permission-generator bitmap conformance, tusd `validate_pack.py`, indexeddb gates, signoz SQL checker, haproxy defaults-scope check, constitution template validator, repo-docs link checker on edited files, memory-os `sha256sum -c`.
- Not run: checkers that need a binary, a container, a network, a cluster or a target repository. `vector` config check exited 2 (no `vector` binary) and is not a pass.

No fixture, self-test or comparison run was created. Static checks prove source agreement only; they prove no live agent behaviour.

## Review outcome

| Review | First pass | After repair |
|---|---|---|
| Prompting-guide change (commit `6726f57e`) | `CHANGES-REQUESTED`, nine findings | `APPROVED-WITH-NITS`; all nine resolved; two new items repaired in the final commit |
| Orchestrator change and the two relocations (`41a0fb81`, `6c408780`, `9e12a460`) | `CHANGES-REQUESTED`, fourteen findings | `APPROVED-WITH-NITS`; twelve resolved, two accepted as declared lane repairs; two new items repaired in the final commit |
| Nine lane commits | `CHANGES-REQUESTED`, six minor and five nit, no blocker or major | Ten repaired in the final commit; one kept as a declared change (the capability check asks for approval before a dependency install) |

The final commit's repairs to the last review's findings were not re-reviewed. They restore earlier wording or narrow a claim, and every gate below ran after them.

Final-candidate gates, all exit 0: the four root checkers; the three prompting-guide policy checkers (the Codex one over both agent roots); `render_agents.py --check`, `validate_pack.py`, `check_agent_grants.py` and `check_agent_contracts.py` in each orchestrator; `check_execution_contracts.py`; the constitution template validator; `sha256sum -c` for `alaa-memory-os`.
