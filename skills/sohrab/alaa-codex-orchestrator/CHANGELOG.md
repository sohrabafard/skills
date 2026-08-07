# Changelog

## 3.5.1

- The installers replace a differing agent TOML outright and keep no backup. Both platform installers previously copied any differing same-named file into `.alaa-codex-orchestrator-backups/<timestamp>/`, which left an unmanaged second copy of a definition that is already under version control. The atomic temp-file-and-replace path, the hash verification, and the install lock are unchanged; only the retained copy is gone, and `BackupDirectory` has left the installer's JSON result.
- Fixed the Windows agent installer, which threw on every file it had to update. `[System.IO.File]::Replace` requires a backup filename and PowerShell binds a `$null` argument to an empty string, so the call failed with "The path is empty" the moment a differing same-named file existed — leaving the backup directory it had just created as the only trace. Reproduced against the committed 3.5.0 tree before the fix. The staging copy, its hash check, and the post-install hash check are unchanged; the replace itself is now `Move-Item -Force`.
- The skill installers no longer retain the directory they replaced. They still move it aside so a failed swap can be undone, and now remove it once the swap succeeds; `PreviousSkillBackup` has left their JSON result.

## 3.5.0

- Phase A is now a planning phase rather than an evidence phase, and it never skips. It sets up the workspace, chooses the solution and names the alternatives it rejected, decides the data representation and the complexity bound where either exists, then writes the plan through `$alaa-workflow` as one checklist with a box per subtask. A decomposition written before the solution is chosen decomposes the wrong solution, and every lane afterwards inherits that mistake.
- Added execution profiles. `lean`, `standard`, and `hardened` size the pipeline to the finished plan, so a bounded one-lane change no longer pays the full dispatch cost. `lean` drops the reviewer dispatch, never the review: the main thread did not write the diff, so it remains an independent authority over it. Escalation is one-way, and `references/verification-and-gates.md` carries the profile-to-gate mapping.
- Verification is now tiered by what changed. Lanes run the focused tier only, the verifier runs the affected tier once per phase, and the exhaustive tier — full suite, race, end-to-end, highest proof levels — runs exactly once, on the final candidate, after documentation lands. A result stays citable while the tree, the tool versions, the environment, and the flags are unchanged; `$alaa-testing-strategy` owns the tiers and the four validity conditions. The previous shape let several agents re-run the same heavy suites against an unchanged tree, which cost the most and proved the least.
- A failure is classified before it is repaired. `references/failure-taxonomy.md` gained host-environment sub-classes — shell parsing, container runtime, permission and lock, absent executable, stale cache — each with its discriminator, so a product edit is never made against an environment block.
- Replaced "never commit unless requested" with a commit protocol. Each run works on its own branch off a recorded base, refuses to start on a tree dirty with someone else's changes, commits at every completed subtask, and merges into the base only after the user confirms. New Phase F owns that handshake, including base-into-branch conflict resolution, the re-run the merged tree requires, and worktree removal. `alaa-workflow references/workspace-and-integration.md` owns the rules.
- Documentation now carries a size grade. The documenter reaches green, accepts yellow or orange only for the stated reasons, and never leaves a red document behind; `alaa-repo-docs references/15-document-size-and-clustering.md` owns the thresholds.
- Every dispatch now carries a return contract with a line bound, and bulky output goes to the artifact directory as a path rather than into the conversation. An unbounded child return is the most common way a main thread's context is flooded, and that cost is charged on every remaining turn.
- Scoped plan writing to orchestrator mode. Advisor mode answers a plan, critique, or review request in the reply and creates no branch, commit, or plan file unless the user asks, because a request to think about the work is not authorization to change the tree.
- Stopped the `lean` profile from naming which specialists it excludes. Its exclusion list did not cover every Phase D trigger — a one-lane retry or background-job change qualified as `lean` while still needing the observability reviewer — and any such list is a second copy of the routing matrix that goes stale. The profile now decides how gate 4 is performed and how much ceremony the phases carry; gate 5 stays conditional at every profile, on the triggers `references/routing-matrix.md` owns and nowhere else.
- Moved base integration ahead of the exhaustive tier. The tier ran on the final candidate and the base was merged in afterwards, so a base that advanced conflict-free reached the merge with evidence that described a different tree. Phase E now integrates first and records the base commit it observed, and Phase F reruns only when the base advanced past that commit. `$alaa-testing-strategy` owns the invariant: the exhaustive tier runs on the tree that will land, and a clean integration invalidates it exactly as a conflicted one does, because no conflict means no edit was needed rather than that the combination was observed.
- Replaced six copies of the document size ladder — both skill bodies, both documenter agents, both dispatch templates — with a route to `alaa-repo-docs references/15-document-size-and-clustering.md`. The copies also said never leave a red document behind while the owner permits one with explicit human approval, so the duplicate was already deciding something it does not own. The documentation gate now consumes that skill's measuring command and its exit codes instead of restating its thresholds.
- Added a run-accounting line to the final report: agents dispatched and distinct roles among them, checks run versus cited, and the branch span from the plan's creation to the last commit. Every figure already exists in the roster, the evidence table, or the git reconciliation that step 6 performs anyway, so the accounting adds no command and no bookkeeping — a run that measures its own slowness by being slower has answered nothing. No budget is stated for any of the three, because a threshold invented here would be enforced everywhere and grounded nowhere; they are diagnostic together, and the previous shape left a slow run with no evidence at all about why.
- Restructured both bodies. Phase detail, the intake list, and the cross-phase curation step moved into `references/verification-and-gates.md`, which now owns the pipeline as well as the gates — the phases are the gate order, and the separate ten-item gate list it used to carry was a second ordering of the same pipeline. The body keeps the phase table, the profiles, the report shape, and the authority boundaries. `SKILL.md` went from 223 lines to 163, below the 182 it started this batch at, so the capabilities added here cost less always-loaded context than what preceded them.
- Folded the specialist trigger list out of the body and named each agent in its own `references/routing-matrix.md` section instead, which is where the trigger already lived. Pruned the anti-pattern list from 24 entries to 19 by merging pairs and dropping those that only restated a rule stated above them.
- Routed every specialist condition to `references/routing-matrix.md` and left none behind. The pipeline named the moment and the agent but also restated the trigger, and each restatement was narrower than the owner: security had become "trust-boundary changes" against twelve named conditions, and the dependency auditor had lost replacement, lockfile drift, and transitive shift. A shorter local copy of a trigger list does not read as a summary at dispatch time — it reads as the list, and the conditions it dropped become gates nobody ran. Five further copies were found in the same class and removed with it.
- Stated that every profile runs all six phases. The profile table had implied `lean` skips phases while the text said the six-phase shape was not mandatory, leaving no way to determine which phases `lean` actually runs. A phase skipped is a gate skipped and no profile holds that authority: `lean` removes dispatches, not phases.
- Removed a second copy of the dispatch return contract from section 3; `Bound every return` in section 2 owns it.
- Closed five contract defects a second review found, three of them introduced by the restructure above. The pipeline heading had lost the word that scoped it to orchestrator mode, so Phases A, B, and F read as instructions in advisor mode, where creating a branch and committing are forbidden. Phase C's exit condition read "`PASS` or classified", which let a classified `PRODUCT-FAILURE` satisfy it and Phase D begin on known-failing verification; it now requires `PASS` or a phase that ended blocked with the failure's owner named. And the anti-pattern list still called running the full pipeline under `lean` a defect while the profile section said every profile runs all six phases — `lean` removes dispatches, never phases, and all three statements now say that.
- Reduced the agent catalog's `Trigger` column to a `Subject` column that decides nothing. It was a second, shorter trigger list — security lost sessions, downloads, command construction, serialization, and privileged operations against the matrix's twelve conditions — and a roster line read as a trigger under-fires, because the conditions it leaves out are still conditions.
- Split the adversarial reviewer's two trigger arms, which are not interchangeable. The blast-radius arm is known in Phase A and selects the `hardened` profile; the conflicting-verdict arm is discovered in Phase D and fires the reviewer inside the profile already running. Treating them as one made a Phase D discovery reselect the profile retroactively and demand a Phase A gate the run had already passed.

## 3.4.1

- Removed the routing-owned Laravel Boost hardening rule. Read-only lanes retain exact question-scoped Boost allowlists, while implementation lanes inherit Boost's native surface; this orchestrator no longer denies `tinker` or `record-rule` or claims they must be switched off at the server.

## 3.4.0

- Replaced partial per-server MCP tables with marked transport-neutral templates. Partial tables had no transport and were rejected by Codex as malformed, while omission and empty maps inherit the parent configuration.
- Made both installers resolve the live parent inventory, preserve each server's transport discriminator, materialize the catalog's exact per-role grant, disable unassigned servers, validate the resolved files, and record an inventory fingerprint.
- Changed the grant checker to distinguish portable templates from resolved roles and added omission, missing-server, enabled-server, and partial-transport red fixtures.
- Updated status and bootstrap checks for materialized files and live inventory drift, and removed the installer bootstrap's count-only fallback when Python is unavailable.
- Wired the grant checker into pack validation and documented its exact command and exit-code contract in the skill body.

## 3.3.0

- Every agent file now fixes the code-intelligence servers its role may reach. A role that cannot ask a server's question no longer holds it, and the tool descriptions it never used stop arriving in that role's window on every dispatch. `references/agent-catalog.md` records the assignment; `$alaa-code-intelligence-routing` owns the grant classes behind it.
- Read-only review lanes receive Serena tools by exact name rather than the whole server. An MCP server is a separate process, so `sandbox_mode = "read-only"` never constrained it — a lane declared read-only could still rename or delete a symbol repository-wide. The allow list is the only form of that boundary that holds.
- Removed Serena's shell tool from the implementation lanes. They already run commands under the sandbox and approval policy, and a second path to the shell that bypasses those rules is a hole rather than a capability.
- A lane's grant is now an anti-pattern to widen inside a dispatch. It belongs in the agent file, which is also what a reinstall restores.
- Gave `alaa-documenter` a real tool allow list instead of a deny list. It previously inherited every tool in the session; it now holds exactly what a documentation lane needs.
- Framework-context access is scoped per role in composable classes — documentation and versions, live schema, URL resolution, application errors, browser surfaces — rather than one bundle, so a migration lane holds no browser logs and a browser lane holds no connection inventory. `tinker` and `record-rule` are denied in every lane and switched off at the server.
- Every lane granted a code-intelligence server keeps the ability to invoke the routing skill. A grant without the contract that chooses among the granted servers recreates the problem the grant was meant to solve, and a lane whose allow list omits the skill surface cannot act on the repository binding that tells it to.
- Added `scripts/check_agent_grants.py`. It resolves each definition the way the runtime does and fails on a read-only lane holding a mutating tool, a forbidden framework tool left reachable, a granted lane that cannot reach the routing contract, and an allow list that could refuse to launch. A parse alone never proved any of those.
- Narrowed the cross-runtime sweep exemption in `scripts/validate_pack.py` from the whole "When NOT to use" section to the single negative-routing line, so the section stays covered for anything else placed in it.

## 3.2.0

- Wired three doctrine skills into the roles that were already gated on their subjects but had no standard behind them. `alaa-architecture-critic` now reviews against `$alaa-system-design`, `alaa-test-strategist` applies `$alaa-testing-strategy`, and `alaa-performance-profiler` measures against the complexity budget `$alaa-algorithms-data-structures` owns. Each is loaded through the agent's developer instructions and named in its dispatch template, so the standard arrives with the lane rather than depending on the lead remembering it.
- Phase A now runs a design pass before implementation on three conditions the architecture critic's gate never covered — a change of data owner, a dependency added or removed between components, and a new deployable unit — so the critic reviews a design record with its decisions made instead of a plan that can only be accepted or rejected whole.
- `alaa-verifier` now names the proof level each `PASS` reached. A check run against an embedded substitute and the same check against the real engine are indistinguishable from the command line, and the level is what tells a reader whether the result needs re-running.
- Replaced the test strategist's restatement of layer placement, failure-mode ordering, and the broken-implementation challenge with a pointer to the skill that owns them, so the two cannot drift apart.

## 3.1.1

- Extended the authoring escalation criterion: the wording of these artifacts carries as much judgment as their structure. In a skill the prose is the executable logic — nothing underneath enforces what a sentence failed to say — so drafting the text is the judgment rather than the write-up of it.

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
