# Lane brief, second pass — rewrite and prune

Owner decision, 2026-11-17: the first pass removed duplicates only and cut 3 to 15 percent. The
owner chose a second pass that rewrites every sentence and prunes rules that buy no behaviour,
written by Fable 5.2. This brief replaces `lane-brief.md` for second-pass lanes. Where the
dispatch and this brief disagree, report the conflict and follow the dispatch.

## Outcome

The owned text does the same job in far fewer words. Rewrite it; do not trim it. Every file
is in scope. For each file that ends above four fifths of its starting word count, state in
your return what kept it there.

## Start

1. Run `git merge --ff-only work/core-skills-compression` in your worktree, then confirm that
   `git log --oneline -1` shows the commit your dispatch names. This is the only merge you run.
2. Read `skills/sohrab/AGENTS.md`, then your whole owned scope, then the checkers that bind it.
3. Read `plan.md` (Appendices A to C), `freshness.md` and the first-pass return for your scope
   in `lane-returns.md`. They sit in the directory that holds this brief, inside your worktree.

## Method: one pass per file, three moves

**1. Find the decisions.** For each section, list what an agent must decide or do differently
because the section exists. That list is the section's job.

**2. Prune.** Remove a sentence that carries no item on that list. A sentence qualifies under
exactly one of these criteria:

| Code | Criterion |
|---|---|
| P1 | Default behaviour. Every in-scope model does this without being told when it works in a coding harness. Judge it for the weakest model that loads the file (Haiku 5.5, Luna low): if that model would plausibly act differently in a case that matters, keep the sentence. |
| P2 | Itinerary. A step that states only the obvious order of work. Keep a step whose order affects correctness, or that an agent would not take unprompted. |
| P3 | Ceremony. A record, label or report item that no later step, gate, checker or reader consumes. |
| P4 | Restated platform fact. The runtime's own system prompt, tool description or official documentation states it, and the file adds no house decision to it. |
| P5 | Ownership noise. "X owns Y" where no decision at that site depends on knowing it. Keep a pointer that routes a real decision. |
| P6 | Repeated disclaimer. An evidence limit ("source checks prove no live behaviour", "uncalibrated", "unrun") stated again; keep it once per skill, where it binds a claim. |

**Never prune**, whatever the criterion: an independent-gate floor; an authority limit or an
action that needs approval; a secret, security, tenancy or data-loss rule; a stop condition; a
verdict or status token; an output-contract field that the lead or a checker reads; a number,
threshold, limit, version gate, or the source and date beside it; an exception to a rule that
stays; a recorded owner decision; a heading in Appendix A; a fact in Appendix C.

When you cannot tell whether a sentence changes behaviour, keep it and compress it.

**3. Rewrite what stays.** State each remaining rule in the fewest words that an agent cannot
misread: one idea per sentence, command form, rule before reason, one term per concept, exact
names and numbers. Merge rules that share a condition into one list. Keep one short reason
clause per rule that has a non-obvious reason; drop a reason that only restates the rule. Turn
prose that enumerates cases into a table or a list.

Worked example, no rule pruned, 311 words to 215:

Before (excerpt): "For each unchanged question, keep the established evidence and every
attempted owner-and-operation pair. Before each transition, record the missing fact, the failed
capability and its cause, the next eligible operation and the lost guarantee. Mark each attempt
before its call. Skip a candidate known to be unavailable or unsupported. Never cycle. For a
failed operation, allow at most one cause-specific, non-mutating repair of health or capability
and one materially different retry, when the cause supports them; otherwise advance
immediately."

After: "Per question, keep the established evidence and the owner-operation pairs you tried.
Try no pair twice, and skip one known to be unavailable. Before each fallback, record the
missing fact, the failed capability and the guarantee you lose. A failed operation gets at most
one cause-specific, non-mutating repair and one materially different retry; otherwise move on."

## Ledger

Write `artifacts/core-skills-compression-20261116/pruned-<lane>.md` in your worktree and commit
it. One row per pruned rule: file, the rule in one line, the criterion code, and the checker
clause you deleted with it, if any. A sentence removed as a duplicate of a rule that stays in
the same skill needs no row. The owner reads this ledger to restore a rule.

## One owner per rule across skills

When your file restates a rule that another skill owns, replace the restatement with a pointer
that names the trigger, the owner file and what it decides. When your skill is the owner, keep
the rule. A rule inside an agent definition or a contract asset stays there, compressed,
because a subagent does not load the owner.

| Rule family | Owner |
|---|---|
| Lane branches, lane commits, checkpoint is not acceptance, plan header fields, `REVIEW_PENDING` closure, one writer per file | `alaa-workflow` |
| Agent-tool model alias, invocation effort and its precedence, advisor pairing, concurrency-limit error | `alaa-prompting-guide references/41-claude-code-runtime-features.md` |
| Codex pin precedence, sandbox and `AGENTS.md` chain facts | `alaa-prompting-guide references/11-codex-runtime-features.md` |
| Test tiers, evidence validity, the fresh exhaustive run, never weaken an assertion, result classification | `alaa-testing-strategy` |
| Return shape of a delegated lane, output budgets, no universal watchdog timeout | `alaa-low-noise` |
| Provider grant scoping, read-only MCP enforcement | `alaa-code-intelligence-routing references/80-agent-scoping.md` |
| Model and effort capability, delegation polarity | `alaa-prompting-guide` |
| Task model and effort allocation, review cadence and scheduling, role triggers | the orchestrator pair |

## Checker literals

Three clause checkers bind sentences: `alaa-testing-strategy/scripts/check_execution_contracts.py`
and both `alaa-*-orchestrator/scripts/check_agent_contracts.py`.

- Reword a bound sentence and its literal in the same commit. Delete a clause only with the
  sentence it binds, and record it in the ledger. Change no checker logic.
- You may edit a clause in any of the three checkers when it binds one of your owned files.
  Touch no other clause. Other lanes edit the same checker files in other tuples at the same
  time, so keep each edit inside the tuple entry it concerns.
- A clause that one tuple requires in files of two lanes: keep the sentence verbatim and list it.
- `NORMATIVE_DUPLICATES` and its SHA-256, and `CONTRADICTIONS`, belong to the testing-strategy
  lane. When that lane rewords an owned normative sentence, it updates the entry and the hash.
- Keep a literal that is matched with a raw `in` on one line.
- Fixed everywhere: file and directory names; Appendix A headings; each skill's
  `When NOT to use` heading; `agents/openai.yaml` field limits; the completion-state names and
  their definition rows; the `Final report` heading of each orchestrator `SKILL.md`; every
  `{{token}}` and script-read string in `alaa-workflow/assets/`.

## Work rules

- Edit only your owned paths, inside your own worktree. The main checkout is live for every
  running session; never write to it.
- Retire a file with `git mv` into `_to_delete/20261116-core-skills-compression/<skill>/`, then
  confirm its size with `ls -la`. Never delete a file.
- Run each command with `PYTHONDONTWRITEBYTECODE=1 python3 -B`. Run no fixture, self-test or
  comparison evaluation. Run the gates when the work is done, not after each file.
- Each gate exits `0` clean, `1` findings, `2` could not run. Either nonzero blocks your commit.
  Repair the cause in your scope. Report a failure whose cause is outside your scope with its
  output line.
- Commit by path on the branch checked out in your worktree: `git add -- <paths>`, then
  `git commit -m "<message>" -- <paths>`. One Conventional Commit per skill, no attribution
  trailer. Run no `git add -A`, `switch`, `reset`, `stash`, `rebase`, `tag` or `push`.
- Write English only, a single `/name` at a cross-skill call site, and no emoji.
- Finish the whole scope. Work through an ordinary error. Return `STATUS: INCOMPLETE` only when
  a named blocker stops the work.

## Return

About 40 lines by default; exceed it for required items. No diff and no file dump.

1. `STATUS` line and the outcome in one sentence.
2. Branch, worktree path, and each commit with short hash and subject.
3. Before and after words per load class, from
   `python3 -B artifacts/core-skills-compression-20261116/measure.py .`
4. Per file that ended above four fifths of its start: what kept it there.
5. Pruned rules: count per criterion, and the ledger path.
6. Checker clauses: reworded and deleted counts per tuple.
7. Cross-skill restatements replaced by pointers, and those you left, with the reason.
8. Rules you kept but doubt, with file and line. At most ten.
9. Gate commands with their exit codes.
