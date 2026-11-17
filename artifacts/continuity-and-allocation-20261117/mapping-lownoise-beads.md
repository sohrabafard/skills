# Mapping: low-noise reach, measurement tooling and the Beads binding

Read-only mapping report, 2026-11-17. Dated evidence: verify a line number before relying on it.

# Facts for the three planned changes: low-noise reach, transcript measurement, Beads binding

The main findings:
- **Part A:** no agent definition in either pack preloads `alaa-low-noise`. The skill reaches a lane only if the lead follows one sentence in each `SKILL.md` and one `<return>` pointer. The only rule inside any agent body is a return-length rule, and only implementers and planners carry it.
- **Part B:** none of the measurement scripts sizes Bash or Read results. Only CodeGraph results are sized.
- **Part C:** the only template for the Beads block is an old one in `artifacts/`. It has drifted from the live block, and no live checker reads the block.

All paths are relative to `<repository root>`. Word counts are `wc -w`.

## A1 — Agent definitions and asset contracts

**Preload.** None of the 33 cc agents lists `alaa-low-noise` under `skills:` (frontmatter lines 4 onward). The 37 codex `.toml` files have only `name`, `description`, `sandbox_mode` and `developer_instructions`, so there is no skills key. Their equivalent is a "load /alaa-…" sentence inside `developer_instructions`, and no codex file names low-noise. There are no rules about bounding command output while running commands (no tail, redirect, quiet or terminal rules) in any agent or asset file. The only rules found are about the length of the return.

**Wording 1** (one sentence, two parts):
```
Return findings, evidence lines and paths, never a transcript, a full diff or a raw log: write bulky output to the permitted artifact directory and return its path. Default length: about 40 lines; exceed it only for required items.
```
- cc, line 76: `alaa-implementer.md`, `-fable`, `-haiku`, `-haiku-high`, `-opus`, `-opus-high`, `-sonnet-high`
- cc, other lines: `-infra.md:78`, `-go.md:80`, `-laravel.md:80`, `-frontend.md:81`
- codex, line 7 (inside the one-line `developer_instructions`): all 14 `alaa-implementer*.toml`
- assets: cc `assets/implementation-contract.md:63`, codex `assets/implementation-contract.md:61`

**Wording 2:**
```
Return a bounded report with evidence paths, never a transcript or a raw log. Default length: about 40 lines; exceed it only for required items.
```
- cc `alaa-planner.md:40` and `alaa-planner-high.md:40`
- codex `alaa-planner.toml:7` and `alaa-planner-high.toml:7`
- cc `assets/planner-contract.md:30`, codex `assets/planner-contract.md:28`

**No rule at all** in the remaining 20 cc and 21 codex agents (explorer, researcher, spec-analyst, verifier, failure-analyst, all reviewers and guardians, documenter, browser-qa, and so on). Codex `assets/reviewer-contract.md` (40 lines, output contract at line 32) has none either. One rule points the opposite way, at `alaa-cc-orchestrator/agents/alaa-reviewer.md:33`:
```
- Report every issue you find, ordered by severity, including uncertain and low-severity ones. Do not filter by importance or confidence: a later step ranks and filters, and it never sees a finding you withhold.
```

## A2 — Orchestrator `SKILL.md` and delegation prompts

The two packs' `delegation-prompts.md` files are identical (`diff` is empty). Each quote below appears in both packs at the line shown.

The lead is told to attach low-noise to every dispatch at cc `SKILL.md:74` / codex `SKILL.md:72`:
```
- **Keep dispatches lean.** Word each dispatch under /alaa-prompting-guide. Carry lane facts only: outcome, owned files, exclusions, acceptance, commands, dependencies, resolved skills and return contract. Do not restate the native role definition. State each instruction once. Every dispatch carries `/alaa-low-noise`.
```

`references/delegation-prompts.md`:
- line 21: `<progress>report meaningful progress under the active host contract; use bounded invocations per package or target</progress>`
- line 22: `<return>the shape of the return and its line bound; findings, verdicts, counts, and artifact paths only, never transcripts, full diffs, or raw logs</return>`
- line 26: ``Every dispatch, in every role template below, carries `<task_controls>` and `<return>`.``
- line 33: ``- **`<return>`**: for its shape and length bound, read `alaa-low-noise references/workflow-integration.md` section `Delegated lanes`.``

Child files:
- `delegation-prompts/30-implementation.md:34` re-sends `<return>` on a continuation: ``send this repair content with `<cadence>`, `<beads_identity>` and `<return>` as the continuation message``
- `10-discovery.md:14`: `<output>Use the planner's bounded native output contract; include decisions, evidence, independent consolidated checks and unknowns.</output>`
- `50-correctness-review.md:25`: `Then exactly one line per item ID: CONFIRMED | REFUTED | NEEDS-EVIDENCE, with evidence.`

All other child `<output>` tags just say "Use the role's native output contract…". No child template contains its own `<return>` tag.

## A3 — `alaa-workflow`

- `SKILL.md:16`: ``5. Before planning, apply Mandatory Ponytail binding in `references/companion-routing.md`, including its user opt-out. Load `/alaa-low-noise` and the narrowest domain skill for each technical decision.``
- `references/companion-routing.md:11` assigns ownership only: ``| What enters the context window and what gets printed | `/alaa-low-noise`. This skill owns what is written down durably |``. The per-child-lane binding at lines 17–23 exists for Ponytail only. There is no matching low-noise binding.
- `references/context-continuity.md:112`: ``- Set the return shape under /alaa-low-noise `references/workflow-integration.md` *Delegated lanes*. Record the return's evidence in the parent's artifacts, because a finding that lives only in a return is lost when the parent compacts.``
- `references/context-continuity.md:119`: `- **Raw logs and full command output.** Record the command, the outcome and the one line that mattered.`
- `assets/phase-prompts-template.md` does not mention low-noise or any output bound.

## A4 — Repository instruction files

Neither root `AGENTS.md` (`CLAUDE.md` is a symlink to it) nor `skills/sohrab/AGENTS.md` has an output-length or terminal-noise rule. `skills/sohrab/CLAUDE.md` is an `@AGENTS.md` import bridge. The only length rules in `skills/sohrab/AGENTS.md` (lines 66 and 106) cover skill description length.

## A5 — Low-noise references in full

`skills/sohrab/alaa-low-noise/references/noise-control-patterns.md`:
```
1	# Noise Control Patterns
2	
3	These commands express the rules of `SKILL.md` *Part 1* and *Part 2*. They are common cases: verify a flag against the installed tool before you script it.
4	
5	## Discovery and bounded reads
6	
7	- `rg -n "pattern" <paths>` to locate before you read.
8	- `rg -n -C 3 "pattern" <paths>` when the surrounding lines decide the answer.
9	- `rg -c "pattern" <paths>` or a file list when the question is how widespread something is.
10	- `sed -n '1,120p' path/file.txt` or `tail -n 80 path/file.txt` for a bounded slice where the runtime reads files through the shell.
11	
12	**Codex.** Discovery mostly uses the shell, so put the bounds in each command: scope every search to real paths, keep `-C` context small, and pipe through `head` or `tail` instead of printing a whole file.
13	
14	**Claude Code.** Delegate a wide sweep across many files to a subagent, and require findings or paths, not excerpts. The sweep then consumes the child's context instead of the parent's.
15	
16	## Diffs
17	
18	Use `git status --short`, `git diff --stat` and `git diff --name-only`, then `git diff -- <path>` for the one file that matters.
19	
20	## Large logs
21	
22	Redirect the full output to a repo-local artifact directory, then read back only the tail or the failing slice:
23	
24	```bash
25	mkdir -p artifacts
26	pnpm test > artifacts/test.log 2>&1
27	tail -n 80 artifacts/test.log
28	```
```

`references/workflow-integration.md`:
```
1	# Workflow Integration
2	
3	## Ownership rule
4	
5	`/alaa-workflow` owns plan versus execution mode, durable artifact families and naming, resume and handoff continuity, and lane ownership. Follow it for artifact structure, and this skill for how much is read and printed. This skill never decides phases, plans or state layout.
6	
7	## Artifact routing
8	
9	- With admitted workflow state: keep durable reasoning in its workflow owner, and cite the canonical plan reference, which is a Beads address for a Beads-native plan. Duplicate nothing in alternate notes. Keep long logs in the repo-local paths that the repository or the workflow run already uses.
10	- With no active workflow: put a useful bulky artifact where the repository convention says. Without a convention, use a small repo-local path such as `artifacts/` or `reports/`.
11	
12	## Delegated lanes
13	
14	The return of a lane enters the parent's context. Keeping discovery out of the parent therefore takes priority over parallelism.
15	
16	- Give each child an explicit return shape and a length bound in its dispatch: an unbounded return most often floods the parent's context.
17	- A child returns findings, counts, verdicts or artifact paths. It never returns a transcript, full file contents, a full diff or a raw log.
18	- A discovery lane reports conclusions and evidence locations, not what it read.
19	- A writer lane keeps its output inside its owned surfaces and reports changed paths, not diffs.
20	- The parent owns the concise synthesis and the user-facing report.
21	- Spawn no summary-only lane when the parent can get that summary in a couple of bounded reads.
22	
23	Both runtimes share this return contract. Delegation polarity differs by model family and generation: before you assume that a cap or an authorization is the right correction, read `alaa-prompting-guide references/06-invocation-and-composition.md`. That skill also owns runtime-specific delegation authorization and capability.
```

`references/model-output-profiles.md`:
```
1	# Output calibration routing
2	
3	Calibration changes output length and cadence, never required content. A shorter report does not prove better reasoning, and fewer calls do not prove equal coverage. This skill defines no model profile and no effort policy: before a model-specific claim or a model and effort selection, read `/alaa-prompting-guide` and follow its topic router.
4	
5	- Calibrate responses, artifacts and progress updates separately. For each, state the required content and the useful cadence.
6	- Preserve evidence, caveats, findings, blockers and the detail that the user requested.
7	- Do not control verbosity through reasoning effort, and do not infer that lower effort meets an output-length target.
8	- When tool output dominates context, bound retrieval at its source, and keep a path to the full evidence.
9	- Shortening never removes a focused implementer check or an independent acceptance gate. Before you remove a repeated check, read `alaa-prompting-guide references/80-subagent-authoring.md`; it decides which repetition is redundant.
10	- Before you keep a calibration change, apply `alaa-prompting-guide references/60-skill-authoring.md`: required content, coverage and authority compliance must survive.
```

For reference: the skill's `SKILL.md:31` sets "Default progress budget: 12 lines of prose and excerpts up to 20 lines", and `SKILL.md:24` holds the save-bulky-output rule.

## B — Measurement tooling (`outputs/20261115-code-intelligence-usage/`)

| Script | Input | What it measures | How it is invoked |
|---|---|---|---|
| `tool_usage.py` (139 lines) | `~/.claude/projects/**/*.jsonl` changed in the last N days (`:4-6`, `:62-63`); subagent `.meta.json` for `agentType` and `spawnedWithWorktree` (`:69-73`) | tool calls by scope, agent type, worktree and project; Bash split into categories and target type using the first real command (`:41-60`); CodeGraph result size (`:92-94`, `:138`) | `python3 -I …/tool_usage.py [days]` from the repo root (README:8) |
| `availability_and_nudge.py` (72 lines) | same files, fixed 7 days (`:4`) | tools available in subagents (from `api-request-shape`), deferred tools, dispatch wording, nudge follow-through, prompt-hook `<codegraph_context>` size (`:34`, `:72`) | `python3 -I …` |
| `reachability.py` (66 lines) | same files, fixed 7 days (`:4`) | whether routing text reaches subagents (`api-request` lines, `:21-26`), re-reads after a CodeGraph call (`:54-58`), deduplicated hook size | `python3 -I …` |

- **No script reads Codex sessions.** The README's Codex row (line 30, "coarse") has no script behind it.
- **No script sizes Bash or Read results.** The only result-size measure is for CodeGraph: `tool_usage.py` collects CodeGraph tool-use ids at `:101` and sizes their matching `tool_result` at `:92-94`. That is the pattern to generalise.
- **Closest base to extend:** `tool_usage.py`. It already pairs each `tool_use` with its `tool_result`, classifies Bash commands, and groups by scope and agent.

**Transcript fields that carry result size** (checked read-only on local transcripts):
- `message.content[].type=="tool_result"` → `.content`, which is either a string or a list of `{type:"text",text}`. This is what entered the context.
- Main-session `user` entries also carry a top-level `toolUseResult`:
  - Bash: `stdout`, `stderr`, `interrupted`, `isImage`, `noOutputExpected`, plus `persistedOutputPath` and `persistedOutputSize` when the output was moved to a file.
  - Read: `file.{content, filePath, numLines, startLine, totalLines}`.
- In one persisted Bash sample, the block content was 1,903 characters (a `<persisted-output>` preview), `toolUseResult.stdout` was 29,992 and `persistedOutputSize` was 48,684. So `toolUseResult` overstates context cost; the block content is the true measure.
- In the one subagent transcript I sampled, `tool_result` lines had no `toolUseResult`. Only the block content is safe to rely on across main and subagent files. I checked one file, so this is unverified in general.
- Side note: `tool_usage.py:80` and `availability_and_nudge.py:35` match the nudge text "is CodeGraph-indexed. For locating". The current hook text reads "For a named symbol call…", so nudge counts may come out zero on new transcripts.

**README key numbers** (lines 16–33):
```
| Subagent tool calls that were shell | 26,538 of 33,387 |
| Shell search and read calls, main plus subagents | 20,251 |
| `codegraph_explore` result size, median characters | 24,799 |
| Prompt-hook injections, deduplicated; median characters | 552; 9,535 |
| Codex `exec` calls with shell search or read, against CodeGraph (coarse) | about 5,800 against about 350 |
Operation sizes for one symbol in one Laravel repository, CodeGraph 1.6.2: `explore` 24,952 characters,
`explore --max-files 3` 24,478, `query --limit 5` 674, `callers --limit 10` 1,287, `node` 1,825.
```
Scope (README:3-4): 1,083 Claude Code transcripts from the seven days before 2026-11-15.

## C1 — Root `AGENTS.md` Beads block

The block runs from `<!-- BEGIN ALAA BEADS BINDING -->` at line 7 to `<!-- END … -->` at line 91.
- With both markers: **1,220** words.
- From `## Beads` (line 9) through the end of the code fence (line 89): **1,208** words.

| Section (lines) | Words |
|---|---|
| `## Beads` preamble: label, workspace, authority, Codex note (9–20) | 105 |
| `### Start and resume` (21–32) | 266 |
| `### Scope and issue lifecycle` (33–41) | 197 |
| `### Issue conventions` (42–51) | 124 |
| `### Continuity and handoff` (52–57) | 95 |
| `### Ownership and authority` (58–65) | 252 |
| `### Quick Reference` (66–89) | 169 (175 including the END marker) |

## C2 — Template, copies and checkers

| File | Role | Words |
|---|---|---|
| `artifacts/agent-control-defaults-20261018/binding-template.md` | The canonical template: markers at lines 1 and 82, `Project label: repo:__PROJECT__` at line 5 | 983 whole file; 971 from `## Beads` to the fence |
| `artifacts/agent-control-defaults-20261018/binding-proposal.md` | Earlier amendment proposal: sections Start, Scope, Issue conventions, Quick Reference, `bd prime` at line 54 | 431 |
| `binding-a.md` to `binding-d.md` (same dir) | Receipts from the batch rollout (`binding-d.md:18` mentions the `Project label` whitespace) | 1,319 / 339 / 341 / 242 |
| `artifacts/agent-control-defaults-20261018/audit_bindings.py` and `.ps1` | Checkers that compare blocks to the template | 673 / 1,086 |
| `docs/_agent_plans/20261013-140219_beads-workflow-memory-ownership.md` | Plan that cites `bd prime` (lines 40, 57, 66, 104); not a copy of the block | 3,624 |
| `.agents/skills/beads/SKILL.md` | Upstream Beads skill; `bd prime` at lines 15 and 79; not the block | 345 |

- **The live block has drifted from the template.** A `diff` shows the template lacks the authority paragraph (live lines 17–18), the `bd ping` step, the batch-script rule (line 31), the native-plan `spec-id` rule, the pre-authorised local commits and the Beads classification rule (lines 63–64), and `--sandbox` in the Quick Reference.
- **The only checker of the block's content** is `audit_bindings.py:88`:
  ```
  assert block == template.replace(b'__PROJECT__', name.encode()), f'{path}: template mismatch'
  ```
  The `.ps1` equivalent is at line 115. Both are pinned to old commit SHAs (`audit_bindings.py:9-27`) and assert `HEAD == base` at `:74`. They are one-off artifacts and would fail now. `commit_bindings.py` only commits `AGENTS.md`/`CLAUDE.md` (`:38`).
- **Nothing generates the block.** No live script writes it.
- **`scripts/check_skill_index.py` checks nothing inside the block.** It has no match for beads, binding, label, workspace, Quick Reference or `bd prime`. Its X6 check (`check_agents_claude_pair`, `:311-357`) only confirms that root `CLAUDE.md` is an `@AGENTS.md` bridge (`:329-342`) or equal to `AGENTS.md` after newline normalisation (`:345`). Root `CLAUDE.md` is a symlink to `AGENTS.md`, so this passes trivially.

## C3 — What agents write into Beads for continuity, and the hooks

**`alaa-workflow/references/context-continuity.md`:**
- `:12`: `| Beads-native plan | Root `notes` | Six-field handoff in the root description |`
- `:13`: `| Issue-only work | Issue `notes` | Issue comments |`
- `:19`: `The root notes name the exact IDs of the current phase, task and subtask (or `none`), the last verified evidence address, blockers, the next action, touched surfaces, and any pending review or commit. For concurrent lanes, the parent keeps the aggregate cursor and links to each lane's leaf notes. … Clear a finished cursor before you advance.`
- `:35-44`: the six-field handoff package (Confirmed facts, Open assumptions, Ruled out, Read first on resume, Environment notes, Traps).
- `:54`: `Learned knowledge about a task goes to its issue comments for native or issue-only work, and to the plan handoff for Markdown. The native root handoff links to task findings when needed. Issue notes hold position only.`
- `:58`: the cross-PC handoff ("Record it in the task notes or the native root notes, or in the Markdown checkpoint or direct cursor").
- `:62-69`: when to write. Line 69: `Write the knowledge down while it is still verbatim. Do not wait for a compaction warning.`
- `:85`: native-plan resume reads the root's notes and handoff, then the phase, task and subtask comments.
- `:89`: `**The bound issue**, when Beads is selected: task state, notes, comments and prerequisites. Hook guidance is no substitute for this read.`
- `:92`: ``When it holds a `Pending Beads reconciliation` list and Beads is available, register each entry in Beads and clear the list before other work.``
- `:113`: leaf notes record a lane's done and remaining items and its last evidence address.

**`alaa-workflow/references/task-tracking.md`:**
- `:57`: the root `description` carries "…the six-field handoff under `references/context-continuity.md`".
- `:59`: `| Root `notes` | The aggregate cursor, the last verified evidence address, blockers and the next action |`
- `:60-61`: phase and task comments hold results, verdicts and evidence.
- `:135-136`: `notes` hold position, blockers and next step; comments hold events, interim validation, learned knowledge and curation outcomes.
- `:140`: durable knowledge goes through memory-os.
- `:181`: `Events go in `bd comments add`, position in `--append-notes``
- `:206`: the dated `Pending Beads reconciliation` list during an outage.

**Elsewhere:**
- `alaa-workflow/references/context-curation.md:31`: the curation outcome goes in issue comments for issue-only work.
- `alaa-memory-os/SKILL.md:175`: a task's position and next step belong in issue `notes`.
- `alaa-memory-os/SKILL.md:181-191`: `bd remember` rules, including `:183` "`bd prime` injects every memory by default, with no label or project filter".
- Root `AGENTS.md:55` restates the notes rule.
- The workflow `.py` and `.json` files have no matching text.

**Hooks:**

| File | Hook | What it injects |
|---|---|---|
| `.claude/settings.json:32-44` | `SessionStart` → `bd prime --hook-json` | Output of `bd prime`: workflow reference plus all memories. Its `--help` says "~1-2k tokens" in CLI mode. A read-only run here returned 7,858 bytes. |
| `.codex/hooks.json:3-49` | `SessionStart` (startup, resume, clear), `UserPromptSubmit`, `PreCompact` (manual, auto), `PostCompact` → `bd codex-hook <event>` | Status messages say "Loading / Refreshing / Checking Beads context" and "Scheduling … refresh". The content is not determinable from the repo; `bd codex-hook --help` only says "Run an internal Codex lifecycle hook". |
| `alaa-memory-os/scripts/session_start_context.sh` | SessionStart script, not registered in either config | Lines 96–99: owner pointers plus the drift-record count |
| `alaa-memory-os/scripts/precompact_checkpoint.sh` | PreCompact script, not registered | Line 23: `{"systemMessage":"Before active-task compaction, use /alaa-workflow for its checkpoint and handoff.","continue":true}`. `references/checkers-and-hooks.md:64,68-71` says Claude Code discards this, so it injects nothing. |

Root `AGENTS.md:27` says "Reuse current hook-injected `bd prime` context". Allow-lists are in `.claude/settings.json:16` and `.codex/rules/beads.rules`. `scripts/` and `docs/` contain no hooks; `.githooks/` holds only post-merge and post-rewrite. The other matches are vendor or curated plugins unrelated to Beads.

## C4 — Citations of `task-tracking.md` headings

The headings did not change in the last three commits. The rewrite in `854c74bb` removed `## Division of labor` and `## Where task information lives`.

| Cited heading | Citing file:line |
|---|---|
| `## Select before tracking-dependent work` | `AGENTS.md:17, 25`; `alaa-workflow/references/artifact-lifecycle.md:57`; `alaa-repo-docs/references/80-implementation-gap-backlog.md:15` |
| `## Agent identity and ownership` | `AGENTS.md:28, 38, 49, 68`; cc and codex `references/delegation-prompts.md:30`; cc and codex `scripts/check_agent_contracts.py:108` (enforced string); `alaa-workflow/references/context-continuity.md:52`, `phase-prompts.md:43`, `workspace-and-integration.md:43`; `alaa-workflow/assets/phase-prompts-template.md:19` |
| `## Beads capabilities in use` | `AGENTS.md:31, 44, 49, 50`; cc and codex `delegation-prompts.md:30`; `phase-prompts.md:43`; `phase-prompts-template.md:19` |
| `## Acceptance and evidence by level` | `AGENTS.md:61`; `context-continuity.md:66`; `workspace-and-integration.md:57` |
| `## Close reason` | `AGENTS.md:39` |
| `## Issue fields` | `alaa-memory-os/SKILL.md:175` |
| `## Outage and uncertain writes` | `alaa-memory-os/SKILL.md:186`; `80-implementation-gap-backlog.md:13` |
| phase-task-subtask hierarchy (lowercase prose) | cc `agents/alaa-planner.md:19`, `alaa-planner-high.md:19`, `assets/planner-contract.md:9`; codex `alaa-planner.toml:7`, `alaa-planner-high.toml:7`, `assets/planner-contract.md:7`; enforced by `check_agent_contracts.py` (cc `:393`, codex `:390`) |
| `## Issue fields`, `## Close reason`, `## Acceptance…`, `## Beads capabilities…`, `## Cross-project delivery` | `docs/_agent_plans/20261013-140219_beads-workflow-memory-ownership.md:37-42` |
| **Stale (removed) headings** | same plan `:36` cites `## Where task information lives`; `:44` cites `## Division of labor` |

Another 34 lines cite the file with no heading: `alaa-workflow/SKILL.md:17, 24, 31, 61`, `artifact-lifecycle.md:15, 69, 88`, `review-mode.md:27`, both packs' `verification-and-gates.md`, and others. `alaa-workflow/scripts/init_workflow_files.py:340` cites the file in a generated string.

## Could not determine
- What `bd codex-hook` injects for each event.
- Whether `toolUseResult` is missing from subagent transcripts in general (one file checked).
- Codex session transcript format; no script or repo file describes it.
