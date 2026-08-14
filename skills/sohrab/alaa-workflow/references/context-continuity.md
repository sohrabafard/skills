# Context Continuity

This file owns the question "will the work survive losing the conversation?" Everything else in this skill is ordering and artifact hygiene; this is the part that decides whether a long task can be picked up again.

## The four ways context is lost

Long work loses context in four ways, and only one of them is dramatic enough that anyone plans for it.

**Compaction.** The session hits its context limit and older turns are summarized away. The agent continues in the same conversation and often does not announce it. What survives is a compressed summary; what disappears is the detail — the exact error text, the path that was tried and abandoned, the reason a decision went the way it did.

**A new session.** The user comes back tomorrow, or a run is resumed after an interruption. The agent starts with nothing but the repository and whatever files exist in it.

**A different agent.** A subagent takes a lane, or the work moves between runtimes, or a fresh agent inherits an unfinished task. It has no memory of the conversation at all and no way to ask.

**A subagent boundary.** Every dispatch is a one-way context wall. The child sees only its dispatch text; the parent sees only the child's return. Anything the parent knew and did not write down never reaches the child.

Treat all four as the same problem. The design target is a task that any competent agent can resume from the repository alone, with no conversation history, and that target is testable — see the cold-start test below.

## Two different things get lost, and they need different homes

**Position** is where the work currently stands: which phase is finished, what the last verification actually returned, what is blocking right now, what the next executable action is. Position changes constantly and is cheap to write.

**Knowledge** is what the work learned along the way: which approach was tried and abandoned and why, which facts are verified versus still assumed, which command shape actually works in this environment, which plausible-looking path is a trap. Knowledge accumulates slowly, is expensive to rediscover, and is the first thing compaction destroys — precisely because it lives in the middle of the conversation rather than at the end.

Most workflow tooling records position and forgets knowledge. That is why a resumed task so often repeats a failed experiment: the agent knows where it is, but not what the last agent already ruled out.

The three artifacts divide the work accordingly:

| Artifact | Owns | Answers |
|---|---|---|
| Plan | Destination and route | Where are we going, and in what order |
| Checkpoint | Position | Where are we right now |
| Handoff package | Knowledge | What has this work already learned |

The handoff package is a section inside the plan rather than a separate file, because knowledge is only useful next to the route it belongs to, and because a fourth file is a fourth thing to keep honest.

## The handoff package

Six fields. Each exists because a real resume fails without it.

**Confirmed facts.** Things verified by inspection or execution, each with how it was verified. "The session table has no index on `user_id` — checked with `\d sessions`." A fact without its verification method decays into an assumption the moment someone doubts it.

**Open assumptions.** Things currently believed but not verified, each with what would verify it. Keeping these explicitly separate from confirmed facts is the single highest-value line in the package, because a resumed agent that cannot tell the two apart will either re-verify everything or trust something it should not.

**Ruled out.** Approaches tried and abandoned, each with the reason and the evidence. This is what stops a fresh agent from spending an hour rediscovering that the obvious approach does not work. Record the reason, not just the outcome: "rejected — the ORM strips the CTE" is reusable, "did not work" is not.

**Read first on resume.** An ordered, minimal list of exact paths a resuming agent must read before touching anything. Not every file the task touches; the two or three whose content is load-bearing for the remaining work.

**Environment notes.** Command shapes that actually work here, and ones that look right but fail. Exact invocations, not descriptions. This is the knowledge that is most annoying to rediscover and least likely to be in any documentation.

**Traps.** Anything that looks correct and is not. A test that passes for the wrong reason, a config that is overridden elsewhere, a name that appears twice with different meanings.

Write a field when you learn something that belongs in it, not on a schedule. An empty field stays empty; do not pad it.

## When to write

Writing continuously is a tax; writing only at the end is a bet that nothing goes wrong. Write at these moments and no others:

1. **A phase completes or fails.** Update the checkpoint. This is the routine case and it is cheap.
2. **A decision is made or scope changes.** Update the checkpoint and, if the decision closed off an alternative, add it to *ruled out*.
3. **A validation runs.** Record the actual result in the checkpoint — the command, and what it returned. Not a paraphrase. Freeze the tree before the validation is dispatched: commit the work first, so the reference the validation resolves cannot move under it, and record that commit beside the result. A result recorded without the tree identity it observed cannot be cited on resume, because nobody can then check what has changed since — so the resuming agent re-runs a pass this run already paid for.
4. **Something is learned that would be expensive to rediscover.** Add it to the matching handoff field immediately, while the detail is still exact.
5. **Before handing off, and before any long autonomous stretch.** Bring both files fully current, then verify with the cold-start test.

There is one more trigger worth naming because it is easy to miss: **when the conversation is getting long.** Do not wait for a compaction warning. If the work has run for many turns, or has just finished an expensive investigation, write the knowledge down while it is still verbatim. After compaction the same information is available only as a summary of a summary.

## The cold-start test

Before a handoff, and periodically during long work, apply one question to the artifacts as they currently exist:

> If a competent agent with no conversation history read only these files, could it take the next action correctly, without re-deriving anything expensive and without repeating anything already ruled out?

If the answer is no, the missing piece names its own home. It does not know where we are — the checkpoint is stale. It does not know what to do next — the plan's phase breakdown is too coarse. It would retry something that already failed — the *ruled out* field is incomplete. It would trust something unverified — *confirmed facts* and *open assumptions* are not properly separated.

This test is worth running mentally before any long unattended stretch, because that is exactly when nobody is watching to catch the gap.

## The resume protocol

A resuming agent reads in this order, and stops as soon as it has what it needs:

1. **The plan**, for destination, scope, ordered phases, acceptance criteria, and validation commands. Always read this first — it is the only authoritative source for what the work is.
2. **The handoff package** inside the plan, for what the work already knows. Read this before touching code, because it is what stops wasted effort.
3. **The checkpoint**, for current position, last verified result, blockers, and next action.
4. **The files named in "read first on resume."**
5. **JSON state**, only when an automated consumer needs it. A human or an agent resuming interactively does not.

Then verify position against reality before continuing: check `git status` and the diff against the checkpoint's touched surfaces. If the repository and the checkpoint disagree, the repository is the truth and the checkpoint is stale — reconcile it before acting, and record what was out of date.

## After compaction, specifically

Compaction is the one case where the agent continues in the same conversation and may not realise anything was lost. Two rules.

**Re-read the plan.** Do not continue from what the summary says the plan contained. The summary is lossy in exactly the direction that matters — it keeps the shape and drops the specifics.

**Trust the files over your own recollection.** After compaction, a remembered detail and a written one are not equally reliable. Where they conflict, the file wins, and the discrepancy is worth a line in the checkpoint.

Do not surface raw context-budget numbers to the model as a way of managing this; that tends to produce premature stopping rather than better prioritisation. Where a model needs reassurance to keep going on a long run, state it plainly instead — that ample context remains, and that it should not stop, summarise, or suggest a new session on account of context limits.

## Delegation is a context boundary

A dispatch is a one-way wall. The child cannot ask, and the parent cannot see what the child saw.

Write dispatches assuming zero shared context: the outcome, the owned scope, the exclusions, the acceptance criteria, the verification commands, and any handoff-package facts that bear on this lane. Copy the relevant facts into the dispatch rather than pointing at a conversation the child never had.

Require the child to return a compact structured result rather than a narrative, and record its evidence in the parent's artifacts. A finding that exists only inside a subagent's return has already been lost — the parent's context will compact too.

Keep the parent responsible for synthesis. Children return findings and artifact paths; the parent decides what those mean and writes the outcome down.

## What not to write

The failure mode opposite to losing context is drowning in it. These do not belong in any workflow artifact:

- **Raw logs and full command output.** Record the command, the outcome, and the one line that mattered.
- **Anything the plan already owns.** Scope, acceptance criteria, and phase definitions live in the plan and nowhere else. A duplicated section becomes a contradicting section.
- **A transcript of what happened.** The artifacts describe state, not history. "Phase 2 complete, tests pass" is state; three paragraphs about how Phase 2 went is history.
- **Speculation recorded as fact.** If it is not verified, it belongs in *open assumptions* with what would verify it.
- **Secrets, tokens, credentials, or private data**, in any artifact, ever.

## Caveats

Compaction behavior, context window sizes, and whether a runtime signals compaction to the agent are all runtime- and model-specific and change between versions. The rules here are written to hold regardless, but re-check `$alaa-prompting-guide` / `/alaa-prompting-guide` and its runtime references before depending on any specific harness behavior.
