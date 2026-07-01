# Phase Prompt Packs

Every parent plan created by `$alaa-workflow` requires a same-stem phase prompt pack:

- plan: `<stem>.md`
- phase prompts: `<stem>__phase-prompts.md`

The planning agent writes this file as a senior prompt engineer for coding agents. It is not a generic appendix. It is the ready-to-run execution and review interface for the plan.

# Purpose

The phase prompt pack lets a user run each phase with the right agent pairing:

- GPT-5.5/Codex implements by default, using `/goal` or pursue-goal execution when available.
- Claude Opus 4.8 reviews by default, using explicit, structured review prompts.
- Review findings feed back into focused implementation fix loops.

# Required reading before writing

Before writing a phase prompt pack, read:

1. the main plan
2. relevant `AGENTS.md` files
3. the current continuation and machine state when available
4. the user's requested agent split if any
5. `$alaa-prompting-guide` (Codex) or `/alaa-prompting-guide` (Claude Code) for current per-model tuning, trigger syntax, and runtime-feature templates before writing the GPT-5.5 implementation prompt or the Opus/Sonnet/Fable review prompt; fall back to official/current docs directly only if that skill is unavailable, and say so

# Required sections

The file must include:

- `# Phase Prompt Pack - <task>`
- `## Summary`
- `## How to run this cadence`
- `## Standing rules for every phase prompt`
- `## Phase prompts`
- one phase block per plan phase
- `## Cross-phase review cadence`
- `## Draft-to-final rewrite record`

# Per-phase implementation prompt rules

Each Codex/GPT implementation prompt must be outcome-first and evidence-checked.

It must include:

- one durable phase objective
- verifiable end state
- exact read-first files
- mandatory skills for that phase
- scope boundaries and non-goals
- test-first requirement
- validation commands
- state update requirements
- compact checkpoint reporting
- permission to use subagents, parallel jobs, background jobs, or worktrees when lanes are independent and write scopes are disjoint
- blocked stop condition with exact evidence required

Use this shape:

```text
/goal Complete Phase <ID> - <name> from <plan-path> without stopping until <verifiable end state>.

Read first: <AGENTS.md, plan, phase prompts, state files, source files>.
Use mandatory skills: <skills>.
Scope: <allowed surfaces>. Do not change <non-goals>.
Implementation contract: <tests, architecture, state, parallelism>.
Validation: <commands>.
Done means: <all checks>.
If blocked: <exact blocker report>.
```

Do not write a vague prompt like "implement phase 2". The prompt must be sufficient for a fresh agent to run the phase without hidden chat context.

# Per-phase Opus review prompt rules

Each Opus review prompt must be explicit and structured. Use XML-style sections when the prompt is complex.

It must include:

- role
- context/read-first files
- phase scope
- must-check list
- production readiness requirements
- security and observability requirements
- clean-code, architecture, abstraction, and design-pattern requirements
- validation/gate evidence expectations
- output format with verdict, blockers, nits, out-of-scope recommendations, what's good, and gate evidence

Review prompts must allow wider recommendations when architecture, refactor quality, or design quality materially affects production readiness. Wider recommendations should be labeled out-of-scope unless they are severe enough to block the phase.

# Fix-loop prompt rules

Every phase must have or inherit a fix-loop prompt.

The fix-loop prompt must:

- include the review findings verbatim
- resolve blockers first
- avoid scope expansion beyond findings unless the finding requires it
- update state and checklists
- re-run gates
- return for re-review when blockers are fixed

# Parallel worktree rules

When a plan has parallel implementation branches:

- fix branch names in the plan and prompt pack
- do not fix worktree directory names
- require each branch to be green in isolation before integration
- keep shared-file wiring for the integration phase
- give the user suggested git commands and commit messages
- never instruct the agent to commit, push, reset, delete, or force-push without explicit user permission

Example guidance:

```text
BRANCH: `feat/example-lane-a`. Develop in a user-chosen isolated worktree off the reviewed base commit. Do not edit shared integration files. Return suggested commit message and exact files changed; the user performs the commit if desired.
```

# Standing state rule

Every phase prompt must tell the agent to update:

- `.codex/state/<stem>.json` when writable
- `docs/agents/<stem>-state.md`
- relevant checklist items in the main plan or continuation state

If `.codex/state` is blocked, the agent records the blocker and continues with the continuation state file as fallback.

# Draft-to-final rewrite rule

The planning agent drafts the phase prompt pack first, then rewrites it into a final polished version. The rewrite must preserve every phase objective, mandatory skill, validation command, state rule, branch/worktree assumption, and review criterion from the draft.
