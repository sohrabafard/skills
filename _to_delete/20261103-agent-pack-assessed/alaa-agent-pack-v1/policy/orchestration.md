# Coordination policy

## Risk and routing

| Tier | Shape | Initial route | Gate |
|---|---|---|---|
| R0 | Mechanical, local, easily verified | Luna medium | Deterministic check |
| R1 | Bounded code/UI/doc task with clear oracle | Sol medium; Terra medium for visual/scoped fixes | Relevant regression or inspection |
| R2 | Multi-file behavior, integration, framework judgment | Sol medium/high | Integration/contract check + independent review when material |
| R3 | Auth/tenant integrity, irreversible data, ambiguous distributed consistency | Astra high for design/review; Sol high can implement the accepted plan | Specialist evidence + required human/project authority |

File count alone is not risk: a one-line authorization change can be R3.
The routes are provisional engineering defaults, not measured model leaderboards.

## Escalation

1. Identify whether the gap is missing evidence, unclear requirements, insufficient
   tools, context overload, or reasoning difficulty. A stronger model does not fix all of these.
2. Collect the missing discriminating evidence or ask a focused material question.
3. Allow one targeted recovery using new evidence. Do not loop on the same guess.
4. Transfer a small packet: goal, exact failure, reproduction, relevant paths,
   tested hypotheses, evidence, remaining decision. Transfer Terra/Luna to Sol;
   transfer unresolved high-risk Sol tasks to Astra.
5. Increase effort to high before considering xhigh/max when there is a specific
   reasoning bottleneck. Evaluate rather than assuming a universal benefit.

## Shared worktree protocol

- The lead alone updates the task/path ownership register. Reserve directories or
  explicit files before dispatch; treat nested/overlapping paths as conflicts.
- Never let two workers change the same file concurrently. Do not rely on different
  function names in the same file as isolation.
- Shared generated output, lockfiles and migrations have a single owner even when
  source changes are independent. Serialize regeneration and final formatting.
- Reserve a separate temp/output directory per worker. Namespace test databases,
  queues, ports and tenants; concurrent tests can conflict without shared code edits.
- Only the integrator stages or commits shared work when authorized. Avoid reset,
  clean, stash, rebase and broad formatting while workers are active.
- Pause writes, capture revision plus diff hash, then run final review/tests. Resume
  review if the captured files change. A commit alone does not identify uncommitted state.
- Reservations are a coordination convention, not a lock implementation. If agents
  cannot reliably comply, serialize their writes. Independent branches/worktrees
  remain an option when isolation outweighs integration cost.

## Context and durable state

Load common policy + one role + one task. Fetch specialized references on demand.
Keep current task facts and acceptance evidence in the existing task tracker
(for example Beads if actually installed); keep architecture decisions in ADRs.
Use Hindsight or other memory as a pointer to evidence, not as an authority over
current source/lockfiles. Keep secrets and raw user payloads out of memory.

Recommended checkpoint: objective; current revision/diff hash; completed evidence;
remaining work; owners/reservations; decisions; blockers; next exact action.
Refresh before handoff or context compaction, rather than storing full chat history.

## Tool routing

Use the actual alaa-code-intelligence-routing skill when available. Otherwise:
rg for exact paths/identifiers; a semantic tool for definitions/references;
dependency graph for cross-module impact; framework tooling for runtime facts;
browser tools for user-visible behavior; docs for version-specific claims.
Do not start a new MCP instance per role without an actual requirement.

## Done definition

Requested behavior satisfied; authorized scope preserved; required checks passed
or explicit blockers reported; independent findings resolved or clearly accepted;
contracts/docs updated where changed; residual risks and rollout requirements
visible. A model's declaration of success is not the acceptance oracle.
