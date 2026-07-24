# Changelog

## 3.1.0

- Closed a routing gap found in use: the escalation criteria were all software-shaped, so a judgment-dense lane that touched no API, boundary, migration or concurrency surface matched nothing and fell to the default implementer. Authoring or rewriting a skill, prompt, agent definition, instruction file, architecture document, or any standard other agents follow is now a named escalation criterion in its own right. The policy did not change — the criteria list now matches the policy it was always meant to serve.

## 3.0.0

Breaking revision. Re-read `references/model-effort-policy.md` before relying on any prior pin.

- New effort ladder with explicit tier ceilings: Terra is capped at `high` and Luna at `medium`; above a ceiling the correct move is to change the variant, never to raise the effort. `max` is no longer a legal pin anywhere — it survives only as a named per-invocation retry after a documented failure at `xhigh`.
- Seven lanes stepped down one effort level on the documented finding that this model generation holds quality with fewer tokens: browser QA, migration guardian, observability, release, research, test strategy, and the verifier.
- Added `references/model-effort-policy.md` as the single owner of every model and effort decision, including the lean-prompt discipline, Programmatic Tool Calling, persisted reasoning, prompt caching and Pro mode guidance.
- Five new roles, each conditionally gated: `alaa-spec-analyst` (checkable acceptance contract before dispatch), `alaa-adversarial-reviewer` (red-team lens, irreversible and high-blast-radius changes only), `alaa-api-contract-reviewer` (consumer-safe contract transitions), `alaa-dependency-auditor` (supply-chain risk), `alaa-accessibility-reviewer` (interface usability including RTL). Catalog is now 21 roles.
- Dispatch discipline: one agent per lane, never several; no subagent whose job is to double-check another subagent; dispatch text carries lane facts only, because the role already lives in the agent TOML and restating it dilutes both.
- Verification reframed explicitly as an authority boundary rather than redundancy, so gates are never skipped on the grounds that a lane already checked itself.
- Reviewer now reports every finding including uncertain and low-severity ones, leaving ranking to a downstream step, and no longer carries the adversarial lens that `alaa-adversarial-reviewer` now owns.
- Verifier hardened at `low` effort: executes exactly, never diagnoses, never adapts a command, reports blocked rather than reasoning around a failure.
- `scripts/validate_pack.py` extended: validates model and effort pins, rejects `max` pins, requires the new roles and the policy reference, and sweeps the whole pack for cross-runtime leaks.
- Manifest regenerated over all 21 agents.

## 2.1.4

- Implementers and reviewer now always apply $alaa-services-contract and $alaa-trust-gateway-auth in Ala-style repositories (cross-service posture and auth/trust-context handling), in both worlds.
- Manifest hashes refreshed over the enriched agent skill baselines.

## 2.1.3

- Escalation discipline: default down; escalation earned by decision density, never surface sensitivity or goal importance; named criterion required in dispatch and roster; when uncertain, do not escalate.
- Anti-patterns extended for habitual top-tier implementation dispatches.

## 2.1.2

- Bootstrap redesigned: one sentinel-file check per activation (.alaa-codex-orchestrator.version vs VERSION); installer runs only on first install or version change, one attempt, never blocks dispatch.
- Fixed installer empty-path failure when $PSScriptRoot is unset (robust script-root resolution with explicit -SourceDirectory fallback error).
- Both installers now write the version sentinel after installing.

## 2.1.1

- Every agent now begins its final report with a mandatory AGENT | MODEL | EFFORT identity line and flags pin mismatches.
- The orchestrator final report gained an agent roster section listing each dispatched subagent with pinned and self-reported model/effort.

## 2.1.0

- Wired the Alaa skill ecosystem into role agents: security ($alaa-security-review, $alaa-trust-gateway-auth), observability ($alaa-observability-soc), migration ($alaa-data-layer, $alaa-partitioned-table-fk-audit), release ($alaa-docker-production, $alaa-gitlab-ci-cd, $alaa-cicd-laravel-postgres, $alaa-k8s-helm), browser QA ($playwright), performance ($alaa-octane-performance, $golang-performance), test strategy ($golang-testing), architecture ($alaa-services-contract, $alaa-project-constitution).
- Added routing of durable multi-phase plan/state engagements to $alaa-workflow, with single-phase execution through this skill allowed under workflow ownership.
- Corrected the Codex concurrency config key to the documented [agents] max_threads with a freshness caveat.
- Refreshed manifest hashes.

## 2.0.0

- Added mandatory idempotent auto-install/update into `~/.codex/agents` with backups.
- Added repository explorer and split external research from repository mapping.
- Added independent verifier using low-priority resource runners.
- Added failure analyst and pre-implementation test strategist.
- Added architecture, security, migration, browser QA, performance, observability, and release specialist gates.
- Added final documentation validation gate.
- Added current `max_concurrent_threads_per_session` guidance without modifying global config.
- Added Windows and Unix low-priority runners, status checks, validation, routing, failure taxonomy, and complete dispatch templates.
- Reduced Luna documenter effort to medium and preserved `--browser chromium` as a hard user constraint.
