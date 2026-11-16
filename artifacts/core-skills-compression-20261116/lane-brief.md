# Lane brief — core skill compression

Every Phase 1 lane follows this brief. The dispatch adds the lane's scope, moves and commands.
Where the dispatch and this brief disagree, report the conflict and follow the dispatch.

## Outcome

The owned skill text keeps its behaviour in far fewer words. The owner expects a large
reduction. Pursue every reduction source that the mapping report lists for your scope. A light
edit is an incomplete result. Never cut a rule to reach a number.

## Read first

1. `skills/sohrab/AGENTS.md` in your worktree: the binding contract for every skill file.
2. `skills/sohrab/alaa-prompting-guide/references/60-skill-authoring.md`: sections *The
   draft-then-compress loop*, *ASD-STE100 style* and *The wording is the mechanism*. They define
   what may never be cut and the done-test.
3. Your whole owned skill: `SKILL.md`, every reference, every asset, and every script as code.
4. The plan, the mapping report for your scope and the appendices, in the directory that holds
   this brief. Read them from that absolute path; they are not in your worktree. Line numbers in
   a mapping report are dated: verify a line before you rely on it.

## Change classes — one commit per class

1. **Compress.** Fewer words in the same file and place. The executing agent's behaviour is
   unchanged. Never remove or weaken a rule, condition, trigger, exception, threshold, scope,
   the alternative a prohibition names, a reason clause, a stop condition, an authority limit,
   a source or a verification date. Shorten a reason clause; do not drop it. History and
   incident narrative that states no rule and no reason is the only freely removable prose.
2. **Relocate or retire, inside your scope only.** Give a rule stated in several of your files
   one owner. The other site keeps a pointer that names the situation that triggers the read
   and what the owner file decides. The pointer's trigger covers every situation the removed
   copy served. Retire a file with `git mv` into
   `_to_delete/20261116-core-skills-compression/<skill>/`, then confirm with `ls -la` that it
   arrived at its original size. Never delete a file. State the reason for each move in the
   commit body.

Do not make a deliberate behaviour change. When you find a rule that looks wrong, stale or
contradictory, leave it and list it in your return.

## Loading condition is behaviour

A `SKILL.md` body loads on every activation, and some bodies preload into agents. Moving a rule
from a body into a reference changes when it applies. For a rule that applies on every run,
keep one compressed line in the body and cut the copy in the reference. Move only lookup
detail, catalogues and worked examples behind a pointer. A rule restated inside an agent
definition or a contract asset stays there in compressed form, because a subagent does not
load the owning reference.

## Checker-bound text

- Before you reword a sentence, search the clause checkers for it:
  `skills/sohrab/alaa-testing-strategy/scripts/check_execution_contracts.py` and both
  `skills/sohrab/alaa-*-orchestrator/scripts/check_agent_contracts.py`.
- When the checker is inside your scope, change the sentence and its literal in the same
  commit. Keep the mapping one-to-one: delete, merge or loosen no clause, and change no checker
  logic. Keep a literal that is matched with a raw `in` on one line.
- When the checker is outside your scope, leave the sentence verbatim and list it in your
  return under "left for Phase 2".
- Keep every heading in Appendix A of the plan verbatim. Keep file and directory names.
- Keep each skill's `When NOT to use` heading, its `agents/openai.yaml` fields, and every
  backticked `references/`, `assets/` and `scripts/` path resolvable.

## Style

Write ASD-STE100-style English: one idea per sentence, complete sentences, active voice,
command form for an action, one term per concept. Put the rule before its reason. Keep
technical names, paths, commands and numbers exact. Write a single `/name` at a cross-skill
call site. Write no emoji. English only.

## Work rules

- Edit only your owned paths, inside your own worktree. Never write to another checkout: the
  main checkout is live for every running session through symlinks.
- Run each command from your worktree with `PYTHONDONTWRITEBYTECODE=1` and `python3 -B`, so no
  `__pycache__` is created. Run no fixture, self-test or comparison evaluation.
- This lane designs no test. The verification commands in the dispatch are the complete list.
- Each gate exits `0` clean, `1` findings, `2` could not run. Either nonzero blocks your
  commit. Repair the cause in your scope. A failure caused outside your scope goes in your
  return with its output line.
- Commit on the branch that is checked out in your worktree. Stage and commit by path:
  `git add -- <owned paths>`, then `git commit -m "<message>" -- <owned paths>`. Use one
  Conventional Commit per change class and topic, with no attribution trailer. Never run
  `git add -A`, `switch`, `reset`, `stash`, `rebase`, `merge`, `tag` or `push`.
- Finish the whole owned scope. Diagnose an ordinary error and work through it. Do not end the
  run with a list of remaining files or an offer to continue; return `STATUS: INCOMPLETE` only
  when a named blocker stops the work.

## Return

Default length: about 40 lines; exceed it only for required list items. No diff, no file dump.

1. `STATUS` line and the outcome in one sentence.
2. Branch name, worktree path, and each commit with short hash and subject.
3. Before and after words for your scope, from `python3 -B <brief directory>/measure.py .`
   run in your worktree.
4. Relocations: rule, old site, owner, pointer site. Retired files with sizes.
5. Checker literals changed: count per tuple, and confirmation that no tuple lost a clause.
6. Left for Phase 2: sentences bound by a checker outside your scope, and rules also stated in
   another skill.
7. Rules that make an agent re-review, re-test or re-confirm, with file and line. List only;
   change none.
8. Rules that look wrong, stale or contradictory, with file and line. List only.
9. Gate commands with their exit codes.
