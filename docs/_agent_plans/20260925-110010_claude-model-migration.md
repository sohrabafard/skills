# Workflow Plan - Claude model and prompting migration

- Task ID: `20260925-110010_claude-model-migration`
- Mode: `execute`
- Profile: `resumable`
- Status: completed
- Created: `2026-09-25T11:00:10Z`
- Parent plan: not created
- Prompt pack: not created
- Checkpoint: `docs/agents/20260925-110010_claude-model-migration-state.md`
- Machine state: not created
- Base branch and commit: `codex/gpt6-agent-migration`, `4fdd8b709a745314a0575c25c06d0a390847bde6`
- Work branch: current checkout, `codex/gpt6-agent-migration`; no integration or commit authorized.
- Worktree: repository root; use the existing checkout because ownership is clear and writes will be disjoint.

## Summary and Outcome

- Initial repository truth: the GPT migration was present; Claude profiles used rolling aliases and older generation guidance. Installed Codex pack was 3.6.0 versus repository 4.0.0. Initial Claude CLI was 2.1.221; after the user's independent upgrade, a fresh check reported 2.1.282.
- Outcome: migrate Claude policy, prompting references and executable profiles using current official evidence while preserving GPT policy and shared authority contracts.
- Strategy: research first, ratify one structured Claude policy, delegate disjoint implementation, then independently verify and review the candidate. Standard execution profile, subject to escalation if a routing trigger is observed. No live comparisons are authorized.

## Scope

- In scope: prompting-guide Claude references, structured policy and checkers; Claude orchestrator agents and contracts; affected packaging and documentation; shared behavioral corrections mirrored to Codex.
- Out of scope: vendor sources, installed copies, credentials, global configuration, installation, upgrades, commits, merges, publication, destructive operations, GPT policy changes.
- Constraints and assumptions: lead writes workflow decisions and evidence only, never implementation. At most two disjoint writing lanes and one heavy verification command at a time. Shell priority BelowNormal. Runtime identity unknown unless observed. Unavailable sources block only dependent claims.

## Handoff Package

Knowledge that lives only in the current agent's head and disappears on compaction. Fill a field when something is learned, not on a schedule; leave a field empty rather than padding it. Field semantics are in `alaa-workflow references/context-continuity.md`, which is in the skill, not in this repository.

- Confirmed facts (verified, each with how it was verified): native Git inspection returned the branch/HEAD above and no initial changes; archived scratch directories raised access warnings. Installed role files and callable roles use GPT-5.6 and lack instruction-reviewer/deep-review profiles. `claude --version` returned 2.1.221. Official model overview lists Opus 5.5, Fable 5.1, Sonnet 5 and Haiku 4.5. Claude Code documentation requires 2.1.280 for Opus 5.5 and 2.1.257 for Fable 5.1.
- Open assumptions (believed but unverified, each with what would verify it): actual Claude account model availability and serving identity require authorized runtime evidence; role quality/latency/cost requires separately authorized evaluation. None is inferred from source consistency.
- Ruled out (approach, reason, evidence): no silent legacy or generic-role substitution; execution question submitted to user. No installation or CLI upgrade. No inferred superiority from vendor benchmark or model name.
- Read first on resume (ordered exact paths): this plan; its checkpoint; `docs/gpt6-agent-migration.md`; `skills/sohrab/alaa-prompting-guide/assets/codex-model-policy.json`.
- Environment notes (command shapes that work here, and ones that look right but fail): native PowerShell with process priority BelowNormal works. Native text/config evidence is selected under code-intelligence routing. Hindsight recall tools are unavailable; recall fails open; current repository truth governs.
- Traps (looks correct, is not): an alias depends on provider, environment, version and fallback; configured pins never prove serving identity. Historical GPT evidence uses an older HEAD and is not current validation. No memory writes authorized.
- Intermediate curation: user-authorized temporary GPT-6 roles are a task-local decision, retained here only. Source facts belong in their updated owners; no additional durable memory candidate admitted.
- Final curation: no separate durable candidate remains. Calibration and instruction-scope corrections are now maintained by their source owners. Temporary-role authority, host capacity/setup failures and unexplained index provenance stay task-local; no memory publication is authorized or performed.

## Ordered Work

### Phase 1 - Research, baseline and ratified plan

- Status: completed
- Depends on: none
- Owned scope: read-only official research and repository inventory; workflow and evidence artifacts.
- Excluded from this phase: implementation and live model comparisons.
- Work:
  - [x] Read the named sources and verify current behavior.
  - [x] Inventory Claude assignments and owners; capture baseline, with plugin build path explicitly unresolved.
  - [x] Record official model/provider/effort/runtime evidence and a complete before/after role table.
  - [x] Resolve execution-role drift, choose the policy, and ratify disjoint lanes before implementation.
- Acceptance criteria: every requested role has a sourced starting hypothesis, availability condition and escalation criterion; unknowns remain explicit.
- Validation commands: repository structural/index/reference/lifecycle checks; both orchestrator pack, grant and contract checks; prompting rule-writer/policy/evaluation checks; affected packaging and workflow checks. Exact lane command list follows inventory.
- Evidence observed: eleven independent baseline commands exited 0; static proof. No baseline failures. `artifacts/claude-model-migration/baseline/` carries exact records and logs. Full system cards unavailable after bounded retrieval; release summaries and model/migration/runtime docs available. Architecture verdict SOUND after resolving schema/coverage and metadata ownership findings; see docs/design/0001-claude-policy-projections.md.
- Snapshot: HEAD 4fdd8b709a745314a0575c25c06d0a390847bde6; SHA-256 56a22ef8a1ff79edc0d28feb1faedc7b4a76e05c50e8c78fcc00fc3d430c93d5; paths scripts/, skills/sohrab/alaa-prompting-guide/, skills/sohrab/alaa-cc-orchestrator/, skills/sohrab/alaa-codex-orchestrator/; exact 466-path/content manifest artifacts/claude-model-migration/baseline/sha256-manifest-initial.txt, excluding bytecode. Initial/end identical; observed 2026-09-25.

### Phase 2 - Delegated implementation

- Status: completed
- Depends on: Phase 1
- Owned scope: policy/reference lane; executable-agent/checker/packaging lane, serialized where policy schema or generated artifacts overlap.
- Excluded from this phase: lead implementation, vendor or installed edits, GPT policy changes.
- Work:
  - [x] Implement canonical Claude policy and current references, preserving historical routing.
  - [x] Project profiles into agents and validate drift; preserve rule-writer replacement-only output.
  - [x] Add discriminating fixtures for invalid pairs, aliases, identity, precedence, grants, side effects and generated drift.
- Acceptance criteria: scoped changes match the ratified plan and focused proof passes.
- Validation commands: lane-specific focused checks, recorded before dispatch.
- Evidence observed: see Phase 3 integrated verification and lane focused-check records.
- Snapshot: HEAD 4fdd8b709a745314a0575c25c06d0a390847bde6; SHA-256 f93a0f4c937d19e1403e898489de74b76a2872d8a225276eafa0ed9661a8961c; paths scripts/, skills/sohrab/alaa-prompting-guide/, skills/sohrab/alaa-cc-orchestrator/, skills/sohrab/alaa-codex-orchestrator/; 482-path manifest artifacts/claude-model-migration/verification/source-manifest-final.txt.

### Phase 3 - Independent verification, review and documentation

- Status: completed
- Depends on: Phase 2
- Owned scope: integrated evidence, independent artifact/instruction/security/release review, documentation and final reconciliation.
- Excluded from this phase: live quality claims, installation or publication.
- Work:
  - [x] Freeze a scoped content snapshot and run applicable local gates through an independent verifier.
  - [x] Obtain independent correctness, instruction, security and release verdicts; resolve blocker/major findings within two fix cycles.
  - [x] Document full before/after routing, official sources, limitations and unrun comparison design.
  - [x] Validate workflow and documentation; report all four lifecycle states and final curation outcome.
- Acceptance criteria: local gates and required verdicts agree; runtime activation and comparisons remain separately reported.
- Validation commands: exact integrated command list is finalized from the inventory and changed paths.
- Evidence observed: all 19 affected-tier commands exited 0 on the unchanged initial candidate, static proof; exact records in artifacts/claude-model-migration/verification/command-summary.txt. One runner setup failure launched no Python; one cause-specific repair completed the commands. Cycle 1 resolved two correctness findings; cycle 2 restored excluded Codex behavior in one reference only. Correctness APPROVED; instruction text APPROVED and independently bound to disk by literal/delta proof; security PASS; release source condition resolved, package/runtime readiness unproven and publication not requested. Final delta verifier confirmed only 90-model-selection.md changed, with structural and fleet gates both exit 0; artifacts/claude-model-migration/verification/final/ carries proof. Unchanged source inputs retain the earlier gate evidence.
- Snapshot: HEAD 4fdd8b709a745314a0575c25c06d0a390847bde6; SHA-256 9ac7145a6048d35118ba78f2d80d32ab2280a27b1b2181533815ef8d32a767e5; paths scripts/, skills/sohrab/alaa-prompting-guide/, skills/sohrab/alaa-cc-orchestrator/, skills/sohrab/alaa-codex-orchestrator/; 482-path manifest artifacts/claude-model-migration/verification/final/source-manifest-final.txt.

## Delegation

### Ratified routing hypothesis

Official evidence: `artifacts/claude-model-migration/research-summary.md`, checked 2026-09-25. All profiles remain `unrun`; confidence is medium for documented compatibility and low for comparative advantage. Exact IDs replace rolling aliases. Every profile requires provider/account eligibility, applicable CLI version, effective override/cap inspection and separately observed identity; Opus requires CLI 2.1.280, Sonnet 5 requires 2.1.197. Source validation never claims activation.

| Role | Before model / effort | Proposed model / effort | Local reason and escalation criterion |
|---|---|---|---|
| Main lead | Opus 5 / xhigh | claude-opus-5-5 / medium | Documented starting effort; raise to high for interacting unresolved design decisions |
| spec-analyst | opus / high | claude-opus-5-5 / medium | Acceptance judgment at current default; escalate when material ambiguity survives adequate context |
| explorer | sonnet / medium | claude-sonnet-5 / medium | Current supported lower-cost line for bounded inventory; escalate on missed required relationships |
| researcher | sonnet / medium | claude-sonnet-5 / medium | Source extraction; escalate on unresolved source conflicts |
| implementer | sonnet / high | claude-sonnet-5 / high | Current engineering starting point for decided scope; difficult design goes to difficult implementation |
| implementer-opus | opus / xhigh | claude-opus-5-5 / high | Interacting design decisions; evaluate xhigh only after diagnosed quality gap |
| failure-analyst | opus / high | claude-opus-5-5 / high | Interacting failure evidence; escalate after tool/context/spec causes are excluded |
| verifier | sonnet / low | claude-sonnet-5 / low | Exact commands and evidence, no design; ambiguous failure goes to analyst |
| test-strategist | sonnet / high | claude-sonnet-5 / high | Discriminating failure matrix; escalate for unresolved cross-system semantics |
| reviewer, standard and deep scopes | opus / xhigh | claude-opus-5-5 / high | Same independent contract; deep scope changes coverage, no second executable profile without evidence |
| adversarial-reviewer | opus / xhigh | claude-opus-5-5 / high | Load-bearing assumption challenge; use only existing blast-radius/conflict trigger |
| architecture-critic | opus / xhigh | claude-opus-5-5 / high | Ownership and consistency judgment; evaluate xhigh after demonstrated reasoning shortfall |
| security-reviewer | opus / xhigh | claude-opus-5-5 / high | Trust-boundary judgment; safeguards/fallback must be disclosed, never bypassed |
| migration-guardian | opus / high | claude-opus-5-5 / high | Multi-state rollout/recovery judgment; escalate for unresolved interactions |
| api-contract-reviewer | opus / high | claude-opus-5-5 / high | Consumer compatibility judgment; escalate for unresolved transition states |
| dependency-auditor | sonnet / high | claude-sonnet-5 / high | Bounded manifest and advisory evidence; escalate unresolved compatibility reasoning |
| accessibility-reviewer | sonnet / high | claude-sonnet-5 / high | Declared source/rendered criteria; missing rendered proof is an evidence gap |
| browser-qa | sonnet / medium | claude-sonnet-5 / medium | Declared browser scenarios; tooling failure is not model failure |
| performance-profiler | sonnet / high | claude-sonnet-5 / high | Controlled measurements and interpretation; no unsolicited benchmarks |
| observability-reviewer | sonnet / high | claude-sonnet-5 / high | Failure-to-signal mapping; escalate interacting operational ambiguity |
| release-guardian | sonnet / high | claude-sonnet-5 / high | Packaging and rollout evidence; unavailable runtime remains a blocker to activation claims |
| documenter | sonnet / medium | claude-sonnet-5 / medium | Verified behavior synthesis; unresolved behavior returns to owner |
| instruction-reviewer | opus / xhigh | claude-opus-5-5 / high | Behavioral equivalence and authority judgment; evaluate xhigh for demonstrated misses |
| rule-writer | opus / high | claude-opus-5-5 / high | Per-sentence equivalence; keep replacement-only output and no authorship/edits |

Sonnet 5 is retained for these role-specific bounded engineering/evidence duties because it remains current, supports the needed tools/effort, and has a lower published API rate; this is not measured superiority. Haiku 4.5 is a viable comparison candidate for exact verification/exploration, with no effort parameter; no default pin is introduced without evidence of sufficient contract fidelity. Fable 5.1 is a viable explicit comparison/escalation candidate for long-horizon unresolved reasoning after Opus effort/context/tool diagnosis; it has no default role or automatic fallback. Mythos is restricted and has no local profile. Future Sonnet/Haiku 5.5 announcements are not released defaults. No blanket effort ceiling remains; supported max/xhigh are not recommended defaults merely because available.

### Implementation lanes and dependencies

1. Policy/reference lane (temporary difficult implementer, GPT-6 Astra/high): owns `alaa-prompting-guide` except existing Codex policy/checker/fixtures and Claude rule-writer wrapper/checker. Create Claude policy/checker/evaluation corpus, refresh current/historical Claude routing, preserve GPT behavior. Freeze the JSON schema before projection work; full model IDs in policy.
2. Agent/package lane (temporary difficult implementer, GPT-6 Astra/high): owns `alaa-cc-orchestrator`, Claude rule-writer wrapper and its grant checker, affected shared Codex orchestrator contracts, and directly affected packaging/manifest/install paths. Consume the frozen policy, never duplicate it. Keep existing role IDs and grant scope. No new default agent without a demonstrated gap.
3. Both lanes read their complete affected skill contracts, apply draft-then-compress, add focused discriminating fixtures, and return reviewed-file candidates with focused evidence. They are not alone and must preserve other changes. Shared files are serialized by declared ownership.
4. Independent verifier runs integrated static/unit checks after source freeze. Correctness reviewer plus instruction, security and release gates inspect actual artifacts; no lane approves itself. Documentation follows verified behavior and gets link/size checks.

### Gate ownership

- Correctness: temporary alaa-reviewer-deep, GPT-6 Astra/high, because policy, checker, agent and packaging interactions cross skill boundaries. One correctness profile for the complete scope.
- Instruction contracts: temporary alaa-instruction-reviewer, GPT-6 Astra/high, source-only inspection of preserved authority, independent gates, generation-specific rules and compression.
- Security: temporary alaa-security-reviewer, GPT-6 Astra/high, covering model overrides, grants, untrusted evidence/input, side-effect boundaries and safeguard/fallback handling. No offensive or live actions.
- Release: temporary alaa-release-guardian, GPT-6 Sol/medium, covering source packaging, version/activation prerequisites, known absent plugin builder and installation separation.
- Verification: temporary alaa-verifier, GPT-6 Luna/low, exact commands and content hashes; no fixes. All current expected gates are local static/unit work. No benchmark, model comparison or target-account probe.
- Documentation: temporary alaa-documenter, GPT-6 Luna/high, after source review, for dated migration record/full role table, authoritative links and README route; do not duplicate live policy.
- No frontend, data/schema migration, operational service, or dependency-version change is currently planned. Their additional specialist gates fire only if implementation introduces a matching change. Adversarial gate fires only for an unresolved reviewer/specialist conflict or newly discovered qualifying blast radius.

Workflow focused validation: initial exit 1 rejected Markdown-backticked snapshot identifiers; one format-only correction to the required `HEAD <sha>; SHA-256 <digest>; paths <scope>` representation produced exit 0. The underlying manifest did not change. No verifier command or assertion was weakened.

Test design rejects `ultra`, `adaptive` as effort, and any effort for Haiku. Sonnet xhigh/max are valid capabilities. Synthetic precedence/identity/fallback fixtures validate our records/contracts only; live behavior remains unrun. Existing GPT fixtures remain unchanged regression evidence.

- Keep shared-context work in the main conversation.
- Independent lane ownership: `anthropic_research` (temporary researcher, GPT-6 Sol/medium), `claude_inventory` (temporary explorer, GPT-6 Luna/high), and `claude_test_design` (temporary test strategist, GPT-6 Sol/medium). Observed identities unknown. Each owns read-only questions and its evidence subdirectory only. User explicitly approved temporary GPT-6 agents with repository role contracts, without installed-file changes.
- Dispatches assume zero shared context: copy the relevant handoff-package facts into the dispatch text rather than referring to this conversation.
- Lanes report changed paths; this plan's owner records the validated snapshot and handles any explicitly authorized commit.

## Blockers and Next Action

- Blockers: account availability, serving identity, plugin packaging and comparative results remain unproven. Initial CLI version blocker is resolved: after the user's independent upgrade, `claude --version` returned `2.1.282 (Claude Code)`. Claude Desktop update is user-reported, not independently observed. No activation or evaluation was run.
- Next action: none within the authorized source migration. No installation, evaluation, commit, merge or publication is authorized. Unexplained staging of task artifacts and policy source was observed; both implementation lanes deny index mutations. The index was preserved.

## Completion evidence

- Completion audit: artifacts/claude-model-migration/goal-completion-audit.md maps every goal requirement to current evidence. The independent researcher approved the dated provider-alias supplement; rehashing all 482 source files found zero mismatches. This evidence-only supplement did not reopen implementation or change controlled source.
- Report: docs/claude-model-migration.md; complete 24-profile before/after snapshot, sources and limitations. README route added.
- Documentation: scoped link/line-budget gate exit 0; profile-table checker exit 0 for all 24 pairs; whitespace proof passed. README is YELLOW at 53 lines (one navigation hub); report is YELLOW at 61 lines (one migration table and evidence record). Plan/checkpoint/design and structured policy are exempt named artifacts; agent instructions remain atomic contracts.
- Workflow: `python -B skills/sohrab/alaa-workflow/scripts/validate_workflow_files.py --plan docs/_agent_plans/20260925-110010_claude-model-migration.md` exited 0 before completion-state reconciliation; final-state result is recorded under artifacts/claude-model-migration/final-workflow.log.
- IMPLEMENTED: proven on the final source snapshot above; no task commit was created, so recovery depends on retaining the worktree and evidence.
- MERGE_CANDIDATE: proven for the scoped local source by affected gates and independent verdicts, including instruction-text judgment bound to disk by a separate verifier. No merge is authorized or performed.
- RELEASE_CANDIDATE: not requested. Plugin build and actual target activation remain unproven.
- PUBLISHED: not requested; no publication occurred.
- Curation: no separate durable candidate admitted; no memory write performed.
