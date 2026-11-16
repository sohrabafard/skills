# Lane brief — continuity, allocation fit, advisor handling, output reach

Every write lane of this work follows this brief. The dispatch adds the lane's scope and
commands. Where the dispatch and this brief disagree, report the conflict and follow the
dispatch.

## Outcome

`plan.md` in this directory is the approved design. Implement the workstream items that your
dispatch assigns, exactly as the plan states them. This is a deliberate behaviour change that
the owner approved. It is not a compression pass: change the rules that the plan names, and
leave every other rule as it is.

## Start

1. Run `git merge --ff-only work/continuity-and-allocation` in your worktree, then confirm that
   `git log --oneline -1` shows the commit your dispatch names. This is the only merge you run.
2. Read `skills/sohrab/AGENTS.md`, then `plan.md`, `sources.md` and the mapping report for your
   scope, all in `artifacts/continuity-and-allocation-20261117/` inside your worktree.
3. Read every file you will edit in full, and the checkers that bind it.

## Interface texts

Section *Fixed interface texts* of `plan.md` defines I1 (checkpoint), I2 (knowledge comments),
I3 (resume commands) and I5 (output rule). Other lanes write the same texts into other files at
the same time. Keep their field names, tags, commands and meaning exactly; you may shorten
surrounding prose only.

## Writing rules

- Write ASD-STE100-style English: one idea per sentence, command form, rule before reason, one
  term per concept, exact names and numbers. Keep one short reason clause per new rule.
- A new rule states its scope and its trigger. A prohibition names what to do instead.
- Growth needs a reason: add only what a plan item names. Where a plan item replaces a rule,
  remove the old rule in the same edit, so that no file states both.
- State each rule once, in its owner file. Another file gets a pointer that names the trigger,
  the owner file and what it decides. An agent definition or a contract asset is the exception:
  a subagent does not load references, so a rule it must follow is stated in its definition.
- Never remove or weaken, unless a plan item says so: an independent-gate floor; an authority
  limit or an action that needs approval; a secret, security, tenancy or data-loss rule; a stop
  condition; a verdict or status token; a number, version gate, or a source with its date.
- Keep every heading that the plan lists as kept, and every file name.
- Write English only, a single `/name` at a cross-skill call site, and no emoji.

## Ledger

Write `artifacts/continuity-and-allocation-20261117/changes-<lane>.md` and commit it. One row
per rule you changed, added or removed: file, the old rule in one line (or "new"), the new rule
in one line (or "removed"), the plan item, and the checker clause you reworded or deleted with
it, if any.

## Checker literals

Three clause checkers bind sentences: `alaa-testing-strategy/scripts/check_execution_contracts.py`
and both `alaa-*-orchestrator/scripts/check_agent_contracts.py`.

- Before you change a sentence, search the checkers for it. Reword a bound sentence and its
  literal in the same commit. Delete a clause only with the sentence it binds, and record it in
  the ledger. Change no checker logic.
- Edit a clause only when it binds one of your owned files. Other lanes edit the same checker
  files in other entries at the same time, so keep each edit inside the entry it concerns.
- A pair literal changes in both packs in the same commit. Keep a literal that is matched with
  a raw `in` on one line.
- `NORMATIVE_DUPLICATES`, its SHA-256 and `CONTRADICTIONS` in the testing checker stay as they
  are. When your new text collides with one of them, report it; do not edit them.

## Work rules

- Edit only your owned paths, inside your own worktree. The main checkout is live for every
  running session; never write to it.
- Run each command with `PYTHONDONTWRITEBYTECODE=1 python3 -B`. Run no fixture, self-test or
  comparison evaluation. Run the gates when the work is done, not after each file.
- Each gate exits `0` clean, `1` findings, `2` could not run. Either nonzero blocks your commit.
  Repair the cause in your scope. Report a failure whose cause is outside your scope with its
  output line.
- Commit by path on the branch checked out in your worktree: `git add -- <paths>`, then
  `git commit -m "<message>" -- <paths>`. Use Conventional Commits with no attribution trailer.
  Run no `git add -A`, `switch`, `reset`, `stash`, `rebase`, `tag` or `push`.
- Run no `bd` command that writes. The lead holds the Beads claims of this work.
- Finish the whole scope. Work through an ordinary error. Return `STATUS: INCOMPLETE` only when
  a named blocker stops the work.

## Return

About 40 lines by default; exceed it for required items. No diff and no file dump.

1. `STATUS` line and the outcome in one sentence.
2. Branch, worktree path, and each commit with short hash and subject.
3. Per plan item assigned to you: done, and where (file and section), or not done and why.
4. Words before and after for each file you changed (`wc -w`).
5. Checker clauses: reworded and deleted counts per tuple.
6. Anything in the plan that the source text or `sources.md` made impossible or unwise, with
   the evidence. Do not silently deviate.
7. Rules you kept but doubt, at most ten, with file and line.
8. Gate commands with their exit codes.
