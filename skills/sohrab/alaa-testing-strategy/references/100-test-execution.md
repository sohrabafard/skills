# Test Execution

Repository validation policy takes precedence. This procedure grants no role authority, observer independence, allocation or scheduling. Under orchestration, take the executor and observer mapping from /alaa-codex-orchestrator or /alaa-cc-orchestrator `references/verification-and-gates.md`. Direct work keeps its caller's declared authority and required independent observer.

## Existing doctrine owners

Before you select breadth, apply `SKILL.md` **Scope tiers: how much of the suite runs, and when** and **A result stays valid until something named invalidates it**. Before you repair, apply **A failing tier is classified before it is repaired**, which also bans every change that conceals a failure.

## Prepare the check list

Before execution, record one check list in the admitted plan, or without a plan in the repository's existing result record. It holds:

- the required gates, with each exact command, its scoped inputs, cwd, timeout, environment and resource limits;
- the expected cases, declared case dependencies, aggregate-to-child coverage and eligible citations;
- each command's machine-readable reporter, with its output retained; without one, the raw exit status and output;
- the tested content snapshot, relevant untracked inputs and tool versions.

Keep check inputs stable during the pass: a conflicting change invalidates the affected evidence.

For a new or changed test command, or one with a recorded harness failure, confirm selection before citing its result. When the runner has a list-only or collect-only mode, run that as a separate selection check before the first execution; otherwise compare the first run's selected cases with the recorded expected cases. Preserve selected and executed counts, case identities and skip and setup reasons, including every covered child of an aggregate. A valid collect-only result proves selection alone. A lint, type-check, build or render command that runs no tests needs no case selection check: record its scope, exit status and output.

Inspect what an aggregate command actually executes: its name proves no coverage. Replace children with an aggregate only when their inputs, environment, flags and required observer match demonstrably; the caller's constraint on observer authority still applies. Count underlying checks once and run uncovered gates separately. Reuse builds and reset-safe setup under `90-test-economy.md`.

Before CPU-heavy checks or timing, read `110-execution-resources.md`. Before you interpret an outcome or repair a failure, read `120-result-classification.md`; it also decides empty, mismatched and selected-but-unexecuted selections. Report proof and evidence through `80-evidence-and-reporting.md`.

## Collect, repair, retest

1. **Collect before repair.** Run every required runnable check once, and cite eligible evidence. One failure never cancels independent remaining checks. Record each command's exit status and result, and each unrun check's blocker. Record each failure as a finding under /alaa-workflow `references/review-mode.md` `## Finding triage`. A dependent case whose precondition failed is skipped with that precondition named. A fail-fast aggregate proves only executed coverage: use its supported keep-going mode, or run the exact uncovered child commands, while preserving each failure exit status. Stop unsafe or contaminated cases and name them. Collection is incomplete while a required check is unresolved.
2. **Batch repair.** Combine the collection's failures verbatim, classify their causes first, and repair the batch within explicit ownership and authority. A clear owner or cheap fix does not bypass collection. Only an obstruction blocking all or most remaining checks permits minimal early repair: record the cause and blocked checks, repair only that obstruction, then resume the full collection, including previously blocked checks. Review waits for checks required before it. Acceptance waits for all required checks and retests.
3. **Freeze and retest.** Rerun failed or invalidated checks on the frozen repaired snapshot, including invalidated citations. Run any remaining checks whose preconditions are now satisfied. Cite valid passing evidence unless fresh proof is required. Repeat the whole list only when all its evidence is invalidated or the governing gate requires a fresh whole-list run. Extend coverage only for shared behavior, a newly reachable surface or a required uncovered claim. Preserve the original result, repair and retest separately. Collect new failures within the existing budget.

Environment recovery changes require their own authority and evidence. Unresolved required checks block acceptance; continue only safe independent checks. The caller's retry and stop budget still applies and is not reset by collection or a new agent.
