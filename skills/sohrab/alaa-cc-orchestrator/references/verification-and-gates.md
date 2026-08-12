# Execution Pipeline and Gate Policy

`SKILL.md` carries the phase table, the execution profiles, and the authority boundaries. This file
owns what each phase actually does and what each gate requires. Read it before dispatching Phase A,
and again whenever a gate's requirement is in question.

The phases are the gate order. There is no second numbered list of gates, because two orderings of
the same pipeline drift and the agent follows whichever it read first.

## Before any dispatch

1. Inspect relevant repository guidance (`CLAUDE.md`/`AGENTS.md`, local instructions, architecture docs, package manifests, CI, tests, and affected code paths).
2. Restate internally: desired outcome; checkable acceptance criteria; constraints and preserved behavior; out-of-scope work; irreversible or externally visible actions.
3. Split work into the smallest practical lanes with disjoint write scopes. Each lane gets: one concrete outcome; owned files and modules; explicit exclusions; acceptance criteria; focused-tier verification commands; dependencies on other lanes; the name of its matching clean-code skill; and its return contract — the shape of the return and its line bound.
4. Serialize lanes that overlap in files, data contracts, generated output, migrations, or runtime state — or run them under worktree isolation and merge deliberately.

`references/routing-matrix.md` owns every specialist trigger; `references/delegation-prompts.md` owns
the dispatch contracts.

## Cross-phase reusable-context curation

At the end of Phases A through D, invoke `/alaa-extract-agent-lessons` for an intermediate scan only when the
phase produced an explicit user or team judgment, an accepted tradeoff, a verified surprise, a costly detour,
a validation-driven method change, a coordination bottleneck, or non-obvious reusable knowledge. This is a
lead-session curation step, not a subagent lane. When a workflow parent exists, put admitted candidates in its
handoff package; otherwise keep the compact candidates in the lead session. Never publish active phase state.

## Phase A — Plan

Always first, never skipped, at any profile. Everything after it inherits its decisions, so a decomposition written before the solution is chosen decomposes the wrong solution and every lane then carries that mistake into its own diff.

1. Set up the workspace before the first write: record the base branch and its commit, refuse to start on a tree carrying changes this run did not make, and create the run's work branch. `alaa-workflow references/workspace-and-integration.md` owns the base capture, the dirty-tree refusal, worktree mode, and the commit protocol.
2. Dispatch the specification, exploration, and research lanes whose conditions in `references/routing-matrix.md` hold, in parallel only when their questions are independent. Spending on `alaa-spec-analyst` here is the cheapest correctness lever in the pipeline and is wasted on a request that is already concrete.
3. Reconcile observed facts and label unresolved assumptions.
4. Decide the solution before decomposing it. Name the chosen approach and each rejected alternative with the reason it was rejected. Where the goal stores, indexes, caches, or moves data, decide the representation and the access path with `/alaa-data-layer` (`$alaa-data-layer`). Where a path grows with tenants, rows, history, or events, state its complexity bound with `/alaa-algorithms-data-structures` (`$alaa-algorithms-data-structures`). Run the design pass under `/alaa-system-design` (`$alaa-system-design`) when that skill's conditions hold; `references/routing-matrix.md` names the three conditions it adds beyond the architecture critic's own triggers.
5. Trigger `alaa-architecture-critic` before implementation whenever its condition in `references/routing-matrix.md` holds, and whenever step 4 required a design pass. The critic reviews a design record with its decisions already made; a critic handed an undecided plan can only accept or reject the whole proposal. A specialist running here is pressure-testing the plan rather than gating the change, and that is the one place a specialist runs early.
6. Trigger `alaa-api-contract-reviewer` here rather than in Phase D whenever its condition in `references/routing-matrix.md` already holds, so consumer impact and the deprecation path are decided before code is written rather than discovered after.
7. Use `alaa-test-strategist` before implementation, not after, whenever its condition in `references/routing-matrix.md` holds: a test matrix designed after the code exists is written against what was built rather than against what the change had to prove.
8. Write the plan down through `/alaa-workflow` (`$alaa-workflow`) at the `resumable` profile, or adopt the parent plan when a workflow parent already exists. That plan is the run's single checklist — ordered phases, one checkbox per subtask, acceptance criteria, per-phase validation commands, and the handoff package — and it is where the lead reads its own position back after compaction. Tick a box once its outcome has been observed and never ahead of the evidence — several at once when one change satisfied several, and at the start for a subtask that turns out to be already done and was verified rather than assumed. `/alaa-workflow` owns the plan and state machinery; this skill consumes it and does not recreate it.
9. Choose the execution profile from the finished plan, then present the plan and the profile in one compact message and continue without waiting, unless an irreversible decision, destructive action, external side effect, or genuine product choice belongs to the user.

## Phase B — Implementation

1. Dispatch one `alaa-implementer` per routine lane.
2. Dispatch `alaa-implementer-opus` instead only when the lane meets a named escalation criterion from `references/routing-matrix.md` and must itself make non-obvious design decisions rather than apply already-decided ones; record the criterion in the dispatch and the roster.
3. Concurrency policy: at most two workspace-writing implementation agents at once; never parallelize overlapping write scopes; reserve remaining capacity for read-only agents; only one CPU-heavy verification or profiling command at a time.
4. Each lane runs the focused tier only — the tests naming its own failure modes, plus lint, type, and build checks scoped to the files it touched — and returns that evidence. A lane never runs the affected or exhaustive tier: it is the wrong authority and the wrong moment for both. `/alaa-testing-strategy` (`$alaa-testing-strategy`) owns the tiers.
5. Wait for all required lanes. A blocked lane is blocked; do not pad it into success.
6. Reconcile actual diffs and lane evidence, not summaries alone. Detect scope violations, accidental generated changes, contract mismatches, and cross-lane breakage. Commit each completed subtask on the work branch as it lands, and tick its box in the plan.

## Phase C — Independent verification

1. Build one integrated verification plan for the affected tier: every suite reachable from the changed surfaces, plus the acceptance criteria this phase claims. The exhaustive tier is not dispatched here — it runs once in Phase E, on the final candidate.
2. Dispatch only the gates the delta's changed paths actually reach — a delta earns re-verification of what it touches, not the complete gate set. Do not re-dispatch a check whose recorded result is still valid: the tracked tree at the paths it reads, the tool and dependency versions, the environment and service state, and the flags, seed, and working directory all unchanged since it ran. Cite that result with its command, its timestamp, and the lane that observed it. When you do re-run, name which of the four conditions changed.
3. Dispatch `alaa-verifier` with exact commands, working directory, timeout, allowed artifact directory, and resource policy.
4. On Windows, CPU-heavy commands must use `scripts/Invoke-AlaaLowPriority.ps1` with `BelowNormal` by default; `Idle` only for explicitly background-grade benchmark, fuzz, or very heavy diagnostics. On Unix-like systems use `scripts/run-low-priority.sh`.
5. Do not proceed as if verification passed when status is `PRODUCT-FAILURE`, `TEST-INFRA-FAILURE`, `ENVIRONMENT-BLOCKED`, `TIMEOUT`, `FLAKY`, or `CONTAMINATED`. Classify the failure before any repair: `references/failure-taxonomy.md` separates a product defect from a test-infrastructure defect, a host-environment block — shell parsing, container runtime, permission, missing executable — and a contaminated tree, including stale build or test cache. A product edit made against any of the last three is a change with no defect behind it.
6. Use `alaa-failure-analyst` whenever step 5's classification does not by itself name the owning lane; `references/routing-matrix.md` owns that routing. Send a grounded fix request to the owning implementer afterward — the analyst diagnoses and never fixes.
7. Re-run the affected checks after fixes, followed by the integrated gate when shared behavior changed.

## Phase D — Independent review and specialist gates

1. Spawn `alaa-reviewer` against the complete diff and lane plan after integrated verification is clean enough to review. Under the `lean` profile the lead performs this review itself against a diff it did not write; the authority boundary holds because the reviewer is not the author, and the moment the diff leaves the lane plan the profile becomes `standard` and `alaa-reviewer` is dispatched.
2. Trigger a specialist only when its own condition in `references/routing-matrix.md` holds. That file owns every trigger; this one names no condition and narrows none, because a shorter local copy of a trigger list does not read as a summary at dispatch time — it reads as the list, and the conditions it dropped become gates nobody ran. The triggers are identical at every profile.
3. Spawn `alaa-adversarial-reviewer` only when its condition in `references/routing-matrix.md` holds. That condition has two arms and they are not interchangeable: the blast-radius arm is known in Phase A and is what selects the `hardened` profile, while the conflicting-verdict arm is discovered here and fires the reviewer inside whatever profile is already running. A discovery made in Phase D never reselects the profile, because a profile chosen retroactively would demand a Phase A gate the run has already passed. It is a second independent lens, not a second opinion on a routine change, and its findings are reported to the user rather than fed into another fix cycle.
4. Reviewer verdict handling: `APPROVED` proceeds; `APPROVED-WITH-NITS` proceeds while reporting nits, fixing only in-scope low-risk ones; `CHANGES-REQUESTED` routes blocker and major findings verbatim to the owning lane.
5. Specialist blocker and major findings are gates equal to reviewer findings. Conflicting specialist opinions are reconciled by the lead using repository evidence; unresolved high-risk conflicts are surfaced to the user.
6. Present every finding this phase leaves open — reported to the user rather than routed to a lane — as one decision set: each item with its severity per lens, the smallest fix that closes it, and what closing it costs. Ask once. Answered one at a time, each answer moves the tree again and buys another Phase E exhaustive run, and that one is never citable.

## Phase E — Documentation and final validation

1. Spawn `alaa-documenter` when its condition in `references/routing-matrix.md` holds. It is the final write lane, which is why every check below runs after it and not before.
2. Documentation is graded, not merely written. `alaa-repo-docs references/15-document-size-and-clustering.md` owns the size ladder, its thresholds, the measuring command, and the one condition under which the largest grade may stand; `/alaa-repo-docs` (`$alaa-repo-docs`) applies it. This skill decides only that the grade is measured and reported, never what the ladder says — a local copy of it goes stale the moment that skill retunes a threshold.
3. After documentation edits, run the documentation gate below. Documentation is the final write lane and must not bypass validation.
4. Bring the base branch into the work branch before verifying, so the tree about to be judged is the tree that will land. Then dispatch the exhaustive tier once, on that tree: the whole suite under its normal configuration, then the race, end-to-end, and highest-level proofs the claims require. This result is always fresh and is never cited from an earlier run. Run it after documentation lands, so nothing writes to the tree afterwards, and record the base commit it observed — Phase F compares against that commit to decide whether the evidence still describes the tree being merged.
5. Invoke `/alaa-extract-agent-lessons` for the final full-engagement gate after the evidence is stable. Reconcile intermediate candidates, publish only authorized durable knowledge through `/alaa-memory-os`, and accept an empty retained set as a valid result. If it returns `pipeline reopen required`, follow the gate-reopen rule below before rerunning this final gate.
6. Re-check final git status and diff against declared scopes, confirm every plan checkbox matches what actually landed, and read the last commit's timestamp out of that same inspection.
7. Report in the order `SKILL.md` states, and audit every claim against an actual tool result from this session before reporting it.

## Phase F — Integration handshake

The goal is not finished when the gates pass; it is finished when the work is on the base branch or the user has decided it should not be. Present the work branch, its commits, the diffstat against the base, every gate verdict, and the residual risks, then ask for confirmation and wait without merging. On confirmation, integrate exactly as `alaa-workflow references/workspace-and-integration.md` specifies: if the base has advanced past the commit Phase E recorded, bring it into the work branch, resolve any conflict there against the plan's decisions, and re-run the exhaustive tier — a clean merge invalidates that evidence exactly as a conflicted one does, because no conflict means no edit was needed to combine the two sides, not that the combination was observed. When the base has not moved, the Phase E evidence still describes the tree and no rerun is owed. Then merge into the base locally. Push, tag, branch deletion, and any remote action each need a further explicit request. In worktree mode, remove the worktree and detach only after the merge is confirmed clean, then report the branch that still holds the work. A declined or unanswered confirmation ends the goal with the work branch intact and the base untouched, which is a complete outcome and is reported as one.

## Evidence quality

Accept evidence only when it includes the exact command, working directory, relevant environment/resource limits, exit/result, and observed output. A lane summary saying "tests pass" is insufficient.

A cited result — one carried forward instead of re-run — additionally names the timestamp of the run and the tree it ran against, and the lane that observed it. `/alaa-testing-strategy` (`$alaa-testing-strategy`) owns the four conditions under which a result stays citable and the rule that the exhaustive tier is never among them.

## Gate reopen rule

A repository promotion discovered after evidence was declared stable reopens the owning write lane and every
affected verification, review, documentation, and documentation-check gate. After those gates pass, rerun final
reusable-context curation. Durable memory publication alone does not reopen repository gates.

## Finding ownership

- Findings are routed verbatim to the lane that owns the behavior.
- Cross-cutting findings become a new serialized lane with an explicit scope.
- Security, migration, or architecture blockers default to an `alaa-implementer-opus` dispatch.
- The reviewer/specialist never fixes its own finding.

## Maximum cycles

Two fix-review cycles are the default, unless the user explicitly authorizes more. Verification reruns necessary to evaluate those fixes do not count as extra review cycles. After two unresolved cycles, stop and report options rather than oscillating.

## Documentation gate

Because the documenter writes after code review, documentation changes require at least:

- final diff scope check;
- repository docs formatter/linter when available;
- touched-link validation when available;
- example/config snippet validation when safely supported;
- spot-check against verified behavior;
- the size grade `alaa-repo-docs references/15-document-size-and-clustering.md` requires, measured with `alaa-repo-docs scripts/check_markdown_links.py` in its line-budget mode. Consume that result rather than judging the grade here: its exit `1` on an unapproved document at the largest grade is a failed gate, and its exit `2` proves nothing.

## Final success criteria

The orchestrator may report completion only when:

- every acceptance criterion maps to evidence, each marked run or cited and carrying its tier;
- the exhaustive tier ran once, fresh, on the tree that is being merged, with no integration after it;
- no mandatory command is failed, flaky, timed out, blocked, or contaminated;
- reviewer and triggered specialist blockers/majors are resolved or explicitly accepted by the user;
- final touched files match authorized scopes;
- documentation ran or was explicitly skipped for a grounded reason;
- the final reusable-context pass reported persisted, deferred, rejected, or no admitted candidates;
- no `pipeline reopen required` result remains unresolved;
- every plan checkbox matches what actually landed, and every subtask this run changed carries its commit;
- the integration handshake was presented and the user's answer recorded;
- no destructive/external action was performed without authorization.
