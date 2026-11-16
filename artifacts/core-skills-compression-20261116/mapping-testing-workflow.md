# Mapping testing workflow

Read-only mapping report, 2026-11-16. Dated evidence: verify a line number before relying on it.

I mapped every question below. Five things go beyond what you asked or correct an assumption:

- **Two checkers you did not list bind these skills hardest.** `alaa-cc-orchestrator/scripts/check_agent_contracts.py` and its codex twin read workflow files and run `check_execution_contracts.py` themselves.
- **Clause matching is a substring test.** It ignores case and whitespace, so re-wrapping lines is free. Any change to a word, punctuation mark, backtick or `**…** |` table-cell marker breaks a match.
- **The workflow scripts read none of the skill's prose.** `init_workflow_files.py` and `validate_workflow_files.py` bind only the asset templates and the plan files they generate.
- **The testing body's `body` and `doctrine` clauses must stay in `SKILL.md`.** The checker reads them from that file only (`check_execution_contracts.py:391`), so they cannot move to a reference unless the checker changes in the same commit.
- **No checker validates heading citations.** I found no heading or anchor handling in `check_fleet_references.py` (grep for "heading" and "anchor"). Inbound heading citations are protected only by people.

## 1. Checker-bound literals

### `alaa-testing-strategy/scripts/check_execution_contracts.py`
Matching (376–386): a clause matches as a substring after whitespace is normalized and case is folded. A clause that is a bare file name must appear as a whole token. The verbatim lists are at the checker lines below.

| Key | Must appear in | Checker lines | Clauses | Where they sit now |
|---|---|---|---|---|
| body | testing `SKILL.md` | 25–33 | 7 | SKILL.md 158, 160 |
| doctrine | testing `SKILL.md` | 79–107 | 27 | SKILL.md 81, 86, 115–154, 196 (tier table cells 115–118 verbatim, with `**Focused** \|` etc.) |
| router | `references/00-topic-map.md` | 34 | 3 file names | 00-topic-map 16–18 |
| execution | `100-test-execution.md` | 35–78 | 42 | almost every sentence, 3–25; includes the three SKILL.md heading strings, which sit at 100:7 |
| resources | `110-execution-resources.md` | 108–168 | 59 | almost all of 3–91, including the `bash "<TESTING_SKILL_ROOT>/scripts/run-low-priority.sh"` line |
| classification | `120-result-classification.md` | 169–203 | about 40 | all 8 `## STATUS` headings (5–33), the table rows 43–48, the diagnostic steps 56–64 |
| flake | `50-flake.md` | 204–209 | 4 | 38, 40, 55 |
| economy | `90-test-economy.md` | 210 | 2 | 23, and the heading `## Existing tests on a touched topic` at 25 |
| workspace | workflow `workspace-and-integration.md` | 211–230 | 17 + 2 file names | 9, 31, 37–41, 55 |
| continuity | workflow `context-continuity.md` | 231 | 2 | 128 |
| cc_/codex_ body, gates, resources, taxonomy | orchestrator `SKILL.md`, `verification-and-gates.md`, `resource-policy.md`, `failure-taxonomy.md` | 425–432 | `/alaa-testing-strategy` plus the three reference paths | fixes the names `100-test-execution.md`, `110-execution-resources.md`, `120-result-classification.md` |

Two clauses that looked missing are present. They wrap differently in the file:
- "never treat `2` as a pass" appears as "Never treat `2`…" at SKILL.md:160.
- "separate files permit concurrent writers…" appears as "Separate files…" at workspace-and-integration.md:31.

Other mechanics:
- **Frozen hash.** `NORMATIVE_DUPLICATES` (236–346) is pinned by a SHA-256 at 349. Editing any of those strings requires a new hash. Those clauses are also forbidden in every `cc_*` and `codex_*` source (457–463).
- **One frozen clause appears in no skill file.** Line 340, "a check outside the list runs only when the repair changes shared behaviour…", is in the frozen set but in no `REQUIREMENTS` tuple. My grep found it in no skill file.
- **Forbidden strings.** `CONTRADICTIONS` (353–373) are checked in every loaded file, including the workflow files.
- **Files it reads outside the testing skill** (389–417), all of which must exist or the run exits 2:
  - workflow `SKILL.md`, `references/artifact-lifecycle.md`, `assets/plan-template.md`, `assets/phase-template.md`, `references/phase-prompts.md`, `assets/phase-prompts-template.md` (contradiction scan only);
  - workflow `workspace-and-integration.md` and `context-continuity.md`;
  - for both orchestrators: `SKILL.md`, `verification-and-gates.md`, `resource-policy.md`, `failure-taxonomy.md`, `routing-matrix.md`, `delegation-prompts/40-verification.md`, `delegation-prompts/30-implementation.md`.

### `check_agent_contracts.py` (cc and codex, nearly identical)
- 15–20 and 677–678: runs `check_execution_contracts.failures()`.
- `COLLECTION_SEAMS` (cc 524–529) requires these exact sentences in workflow files:

| Workflow file | Required clause | Current line |
|---|---|---|
| `SKILL.md` | "Record phase test-collection, repair/retest and review barriers" | 35 |
| `artifact-lifecycle.md` | "Record each phase's post-reconciliation test collection, combined repair/retest and declared review barriers" and "Workflow records barriers without redefining them" | 85 |
| `plan-template.md` | "Phase collection, repair/retest and review barriers, owners and resume evidence" | 77 |
| `phase-template.md` | "Collection/repair/retest barrier and evidence owner" | 15 |
| `phase-prompts.md` | "Carry the plan's phase collection and repair/retest barriers and their evidence owner" | 46 |
| `phase-prompts-template.md` | "Run only assigned focused or bounded task-owner checks" and "centralized phase collection, repair/retest barriers and any review…" | 29 |

- `COLLECTION_CONTRADICTIONS` (531–543) are forbidden in those same files.
- It loads testing `SKILL.md` and `90-test-economy.md` (624–625) but attaches no clauses to them. They must only exist.
- It requires orchestrator text that names workflow files and headings, so renaming them breaks it:
  - `alaa-workflow references/artifact-lifecycle.md` (75)
  - `…companion-routing.md` (104, 126)
  - `…task-tracking.md` and "Agent identity and ownership" (110, 341)
  - "Its `## Lane branches and commits` owns…" (367)
  - `…workspace-and-integration.md` (502)

### `scripts/check_lifecycle_contract.py`
- Owner file is `alaa-workflow references/workspace-and-integration.md` (59–61).
- L1 needs a table row whose first cell is exactly the backticked state (`DEFINITION_ROW_RE`, 72). Those rows are at w&i 67–70.
- L4: `IMPLEMENTED`, `MERGE_CANDIDATE`, `RELEASE_CANDIDATE`, `PUBLISHED` may appear only in that file and workflow `SKILL.md` (current uses: SKILL.md:39, w&i 23, 67–74). Any other workflow or testing reference that names them fails.
- L5: no definition row outside the owner.
- It also needs a `Final report` heading in both orchestrator `SKILL.md` files that cites the owner (63–64, 241).

### `scripts/check_fleet_references.py`
Generic. It requires every cited `references/…`, `scripts/…` or `assets/…` path to resolve (R1–R6, 163–170). R6 applies to `00-topic-map.md`. A target-repo path on a line that names another skill must use the `<repo>/` marker. No literal sentences or headings.

### `scripts/check_skill_index.py`
Binds only the directory names (README maps, X1–X4) and the existence of `agents/openai.yaml` (X8, 90). Nothing inside the skill text.

### `scripts/validate_sohrab_skill_pack.py`
- V1: frontmatter `name` and `description` (825–828).
- V2: packaged description ≤1024 characters, warning above 975. Each `/name` call adds 3 characters (99–113, 836).
- V3: a heading matching `^#+\s+.*(when not to use|do not use)`, case-insensitive (856). Currently testing SKILL.md:206 and workflow SKILL.md:73.
- V4: warns when the body exceeds 120 lines (860). Testing `SKILL.md` is 216 lines and already warns. Workflow is 90.
- V5: backticked bundled paths in `SKILL.md` must exist.
- V7: `short_description` must be 25–64 characters.
- V8: `default_prompt` must contain `$alaa-testing-strategy` or `$alaa-workflow` (879).
- V9: paths in `00-topic-map.md` must exist (886–893).

### `alaa-workflow/scripts/init_workflow_files.py`
Reads only `assets/` and imports helpers from the validator.
- Template file names (84, 319, 454, 455, 466, 473, 483, 485).
- Every `{{token}}` must be filled, or the run fails (75–76).
- `<!-- design-body -->` marker (22, 97).
- Profile names `direct|resumable|orchestrated|legacy` (18).
- Literal strings it emits:
  - "local commits pre-authorized (main instruction file)" (399)
  - task line syntax (306–311)
  - the `Execution Position` and `Blockers and Next Action` sections (314)
  - "`alaa-workflow references/task-tracking.md`" (340)

### `alaa-workflow/scripts/validate_workflow_files.py`
Reads only target-repository plan artifacts, not the skill's prose. It binds the templates and the formats the references document:
- Handoff heading and its six fields (38–46).
- Phase fields (47) and `### Phase N` headings (642–652).
- Skill Bindings table columns `Skill | Source | Load before | When | If unavailable` (50–51).
- Local task syntax (57) and the hierarchy indentation of 0, 2 and 4 spaces (58, 329).
- Design sections and the `Date | Owner | Decision | Reason` columns (195, 201).
- Approval fields (128–129), the delegated fields (96), and the `## Approved Design`, `<!-- approved-design:start -->` and `## Execution Design` headings (94–97).
- Commit-authority strings (412–413).
- Review verdicts `APPROVED`, `APPROVED-WITH-NITS`, `REVIEW_PENDING`, `CHANGES-REQUESTED` (418–422).
- `Work branch` and `Base branch and commit` (728, 746).
- Checkpoint fields (170, 1248–1255).
- The prompt pack must contain "verify BOTH effective model and effort" (1287). It is at phase-prompts-template.md:15.
- Rules `plan.local-dependency` and "exactly one subtask rejected" are cited by name at task-tracking.md:92 and :244.

Prose that restates these formats (artifact-lifecycle.md:19–27, :50–58; task-tracking.md:62, :88–115, :244; companion-routing.md:44) is kept in step with the scripts by hand. No checker reads it.

## 2. Inbound heading citations (headings that must survive)

| Cited heading | Citing file:line |
|---|---|
| task-tracking `## Select before tracking-dependent work` | root AGENTS.md 17, 25; alaa-repo-docs/references/80-implementation-gap-backlog.md:15 |
| task-tracking `## Agent identity and ownership` | root AGENTS.md 28, 38, 49, 68; cc and codex `references/delegation-prompts.md:30`; cc and codex `check_agent_contracts.py:110` |
| task-tracking `## Beads capabilities in use` | root AGENTS.md 31, 44, 49 |
| task-tracking `## Close reason` | root AGENTS.md 39 |
| task-tracking `## Acceptance and evidence by level` | root AGENTS.md 61 |
| task-tracking `## Issue fields` | alaa-memory-os/SKILL.md:175 |
| task-tracking `## Outage and uncertain writes` | alaa-memory-os/SKILL.md:186; repo-docs 80-…:13 |
| context-continuity `## Task resume and phase resume`, `## Cross-PC handoff record` | root AGENTS.md 55 |
| workspace-and-integration `## Lane branches and commits` | cc and codex `SKILL.md` (143 and 141); cc and codex `verification-and-gates.md:87`; cc `assets/implementation-contract.md:37`, codex :35; 12 cc agent `.md` files (implementer variants at 50/52/54/55, documenter :28); 15 codex agent `.toml` files (`:7`, documenter `:9`); cc and codex `check_agent_contracts.py` (367 and 364) |
| workspace-and-integration `## Before the first write` | cc `verification-and-gates.md:122`, codex :124 |
| workspace-and-integration `## The integration handshake` | cc :180, codex :182 |
| review-mode `## Finding triage` | cc and codex `verification-and-gates.md:48`, `delegation-prompts.md:48`, `delegation-prompts/50-correctness-review.md:18`, `delegation-prompts/90-completion/20-review-followup.md:5` |
| companion-routing `## Mandatory Ponytail binding` | cc and codex `SKILL.md:18`, `delegation-prompts.md:34`, `delegation-prompts/30-implementation.md:30` |
| testing `100-test-execution.md` *Prepare the check list*, *Collect, repair, retest* | alaa-laravel-upgrade-all-packages/references/30-final-gates-and-repair.md:3 |
| testing SKILL headings `Scope tiers…`, `A result stays valid…`, `A failing tier is classified…` | 100-test-execution.md:7; checker 38–40 |
| testing 90 `## Existing tests on a touched topic` | checker 210 |

These are citations by file only, so file names must survive but headings are free:
- quasar `75-testing-ci-playbook.md:5` cites testing 10, 20, 40, 70 and 80.
- haproxy-lua `SKILL.md:47` cites testing 40.
- codex implementer `.toml:7` cites testing 100, 110 and 120.

Headings cited only inside the two skills:
- **Workflow:** `## Shared-file ownership…`, `## Record the tested state`, `## What not to write`, `## Delegate selectively`, `## Plan kinds and approval`, `## Decisions` / `## Open Questions`. These are citations at task-tracking 43, 160, 188; artifact-lifecycle 19, 102, 116; context-continuity 128.
- **Testing:** `*Setup once*`, `*Whether a test is owed*`, `*Reachable failure*`, `*Owned by another skill*`, `*Anti-patterns*`, `*No shipped surface is exempt*`.

Not covered: `docs/`, `artifacts/` and `CHANGELOG` files. These also cite task-tracking headings, for example `docs/_agent_plans/20261013-…:36–44` and `artifacts/agent-control-defaults-20261018/binding-template.md`.

## 3. Duplication inside each skill

### Testing `SKILL.md` inventory (wc -w total 4100; per-section counts by awk)

| Section (line) | Words | Already covered by a reference? |
|---|---|---|
| frontmatter + intro (1–10) | 236 | description vs 00-topic-map:20–30 (negative routing) |
| When this applies (12) | 237 | none; floor rule restated at 90:17 |
| The core rule (27) | 486 | 10:3–7 (derivation), 10:30 (absence of effect), 20:40–45 (triplication discriminator, about 60 words twice) |
| Whether a test is owed (45) | 428 | 90:5–23 table restates the conditions (about 300 words); 60:25 (always-owed) |
| Non-negotiables (70) | 751 | #2→20:40; #3/#4→30-doubles; #5→40; #6→50:38; #7→60:3, 11; #8→70:3, 48; #9→80:3, 15; #10→90:37–55; #11→50:61; #13→90:29–35; #14→90:56–64; #15→120:33, 100:21 |
| Designing the tests (88) | 259 | each step names its reference; partly a second router |
| Proof levels (103) | 72 | 40:3, 7 |
| Scope tiers (107) | 474 | checker-bound; 90:34 and cc and codex verification-and-gates 76–77 restate the tiers |
| Result stays valid (126) | 230 | checker-bound; 80:29–41 and 110:43 restate the reuse conditions |
| Failing tier classified (143) | 131 | checker-bound; 120:37–52 |
| Executing checks (156) | 105 | checker-bound |
| Output contract (162) | 262 | 80:78–80 points to it |
| Stop conditions (186) | 210 | none |
| When NOT to use (206) | 77 | 00-topic-map:20 |
| Reference routing (214) | 58 | 00-topic-map |

### Rules repeated inside the testing skill

| Rule | Locations | Owner | Approx. copy words |
|---|---|---|---|
| Blanket retry forbidden; classify a flake first | SKILL 77, 50:38, 10:61 | 50 | 60 |
| Report unrun checks as not run | SKILL 80, 80:3, 80:15, 120:35 | 80 | 50 |
| Happy path written last | SKILL 79, 100; 10:47–49; 70:3, 48–55 | 70 | 150 |
| Never weaken or delete assertions to pass | SKILL 141, 154; 100:25; 80:65; 10:69 | 100 (checker-bound in both) | 80 |
| Percentage coverage forbidden | SKILL 78; 60:3, 11–21; 10:63 | 60 | 60 |
| Triplication discriminator | SKILL 43; 20:40–44; 10:57 | 20 | 70 |
| Validity conditions and evidence reuse | SKILL 126–141; 80:31–41; 110:43 | SKILL (checker) | 120 |
| Setup once, hermetic tests | SKILL 81; 90:37–55 | 90 | 100 |
| Not-owed kinds | SKILL 49–62; 90:7–15 | 90 | 150 |

### Rules repeated inside the workflow skill

| Rule | Locations | Owner |
|---|---|---|
| Follow the resume protocol | SKILL 13, 25, 31 | context-continuity |
| Cadence belongs to orchestrators' `verification-and-gates.md` | SKILL 34, 36; task-tracking 111; w&i 14, 49; artifact-lifecycle 85; companion-routing 3 | (pointer, repeated 7 times) |
| Push, tag, merge and rewrite need explicit permission | w&i 27, 59, 85; task-tracking 111 | w&i `## What still needs the user` |
| A commit is a checkpoint, not acceptance; one Conventional Commit, no attribution | w&i 20, 22, 49 | w&i |
| A claim locks no file or resource | w&i 31 (checker-bound); task-tracking 62, 186, 214 | w&i |
| Failed heartbeat → ping → outage | task-tracking 39, 222 | task-tracking |
| Never use `--force` or a bare reclaim | task-tracking 39, 189, 188 | capability table |
| Guard exit 13, then re-read | task-tracking 41, 186 | capability table |
| `--sandbox` and Dolt sync authority | task-tracking 21, 199, 203, 214 | 199 |
| Exactly one subtask is invalid | task-tracking 70, 92 | 92 |
| A design plan is always local | task-tracking 19; artifact-lifecycle 19 | artifact-lifecycle |
| A dispatch is a context wall | SKILL 53; context-continuity 15, 146–148 | context-continuity |
| Ponytail, code-intelligence and memory pointers | SKILL 14–16; companion-routing 10, 12, 17 | companion-routing |
| Keep the command, result and the one line that mattered | context-continuity 160; task-tracking 138 | context-continuity |
| Evidence reuse survives a new session or PC | context-continuity 128; w&i 83 | w&i |

## 4. Rules repeated across skills

| Rule | One side | Other side |
|---|---|---|
| Never weaken assertions or lower standards | workflow SKILL:37 | testing SKILL:141, 100:25 |
| Tier definitions | testing SKILL 113–120 | cc and codex `verification-and-gates.md` 76–77 (table rows) |
| Exhaustive tier runs once, fresh, on the final candidate | testing SKILL 118, 137 | cc v&g:172, codex :174 |
| Final-only cadence keeps `REVIEW_PENDING`; closing a tested issue advances readiness | task-tracking 162 | cc and codex v&g:83 |
| Lane commits; commit is a checkpoint; push/tag permission | w&i 16–27, 49, 59 | cc and codex v&g 89, 91, 99 |
| One writer per file; no automatic worktree | w&i 9, 31 | cc v&g 112, codex 114 (pointer plus a short restatement) |
| Where task information lives | task-tracking 117–129 | alaa-memory-os SKILL 171–176 (overlapping table, cross-pointing) |
| Command, result, one line that mattered | context-continuity 160 | alaa-low-noise SKILL:61 |
| "Ample context, don't stop" | context-continuity 142 | alaa-prompting-guide 40-fable-5.md:94 |
| Task allocation owned by orchestrator, capability by the prompting guide | artifact-lifecycle 72, 79; companion-routing 7–8 | testing 00-topic-map 29–30; skills/sohrab/AGENTS.md:43 |
| Mandatory Ponytail | companion-routing 15–21 | cc and codex SKILL:18 (pointer only) |

## 5. Heading inventories (words; what each controls)

**task-tracking.md** (5782 words total):
- preamble 38: scope.
- Select before… 454: the Beads availability test, 4 conditions.
- Division of labor 32: store owns versus workflow owns.
- Agent identity… 651: actor form, claim, lease, guards, transfer, close sequence.
- One task authority 227: local versus beads entries.
- Beads-native plan 627: root, phase and task field content, registration.
- Hierarchy 631: Markdown mapping, review and commit headers.
- Where info lives 99: field owners.
- Acceptance and evidence 203: one owner per level.
- Issue fields 157: field table.
- Close reason 136: verdict, version, address.
- Record prerequisites 133: blocking edges.
- Beads capabilities 1379: adopt or reject per command.
- Cross-project 78: delivery task.
- Ready and gates 165: readiness versus scope; sync authority.
- Outage 335: what to do when Beads fails.
- Helper boundary 177: offline validator scope.
- Migrating 182: local → beads steps.

**context-continuity.md** (2939 words total):
- preamble 37.
- Four ways lost 223: rationale only.
- Two things lost 281: position versus knowledge, artifact split.
- Status and position 510: cursor, checkpoint and JSON projection.
- Handoff package 293: the six fields.
- Task/phase resume 114: what to read.
- Cross-PC 51: the device record.
- When to write 254: five triggers.
- Cold-start test 169: the recovery check.
- Resume protocol 434: read order.
- After compaction 154: re-read, no budget numbers.
- Delegation boundary 184: dispatch content.
- What not to write 122: exclusions.
- Caveats 45: runtime variance.

**workspace-and-integration.md** (2501 words total):
- preamble 33.
- Before the first write 238: base, checkout, isolation.
- Lane branches 909: lane branch, commit, merge.
- Shared-file ownership 297: one writer, stopped-writer recovery.
- Tested state 244: snapshot digest, commits.
- Reconcile evidence 77: route to testing.
- Needs the user 72: the authority list.
- Completion lifecycle 322: the four states.
- Integration handshake 215: requested merge.
- Does not own 41.

**artifact-lifecycle.md** (1874 words total):
- Admission 245: compact versus durable, plan-only.
- Plan kinds 415: design and execution approval.
- Markdown profiles 184.
- Helpers 178: script usage and exit codes.
- Size/consolidate 274: phase classes, allocation routing.
- Dependency/concurrency 210: lanes and barriers.
- Paths 48.
- Permitted contents 71, Update events 49, Resume 22, Delegation 41: all pointers only.
- Compatibility 79: aliases.

**Testing 10** (1606 words total): preamble 52; catalogue 527 (break per code shape); assertion rules 272; auditing 191 (survivor procedure); happy path 56; anti-patterns 478 (largely restates SKILL and 20, 30, 50, 60, 90).

**Testing 80** (1386 words total): five facts 143; reruns 84; scoping 123; reuse 263; changed command 88 (plus routing to 100, 110, 120); removal experiment 127; cannot run 246; reviewing others 166; report field 50.

**Testing 90** (1459 words total): preamble 81; not-owed 434; existing tests 78 (checker-bound); selectors 193; setup once 313; build once 192; review checks 133.

**Testing 110** (1104 words total): preamble 67 (four control layers); runner 77; Go 148; Node 51; PHP 36; services 24; browser 33; artifacts 34; host and container 327; timing 199; runner compatibility 73. Nearly all of it is checker-bound.

**Testing 120** (842 words total): the 8 status sections, 327 words together; host sub-classes 334; diagnostic sequence 123. Nearly all checker-bound.

**Narrative, history and dated text.** No batch numbers, incident stories or "this was added because" text in these files. Dated version provenance appears only in task-tracking:
- :33 (about 10 words)
- :53 (41 words)
- :172 (92 words)
- :177, :181, :195, :201 (about 8 words each)

The skills/sohrab `AGENTS.md` rule to record source and date beside version-sensitive values requires this provenance, so it is not free to delete.

Rationale rather than rules, in context-continuity:
- :5–17 (223 words)
- :19–25 (about 150 words)
- :111 (23 words)
- :142 (63 words)
- :166–168 (47 words)

## 6. Assets

All eight are rendered by `init_workflow_files.py`. None is free prose.

| Asset | Rendered at init line | Other binding |
|---|---|---|
| `plan-template.md` | 473 | 24 tokens; validator headings and fields; `check_agent_contracts` clause at 77; contradiction scan |
| `phase-template.md` | 319 | 5 tokens; phase fields; `check_agent_contracts` clause at 15 |
| `phase-prompts-template.md` | 483 | 14 tokens; validator literal at :15; `check_agent_contracts` clauses at 29; cites task-tracking headings at :19 |
| `continuation-state-template.md` | 485 | checkpoint fields, `Plan:` line |
| `design-plan-template.md` | 454 | 6 required design sections, Decisions columns, Handoff Package |
| `design-checkpoint-template.md` | 455 | 8 header fields |
| `approved-design-section-template.md` | 466 | `## Approved Design` and its start marker |
| `state-template.json` | 84 | the `ADAPTIVE_STATE_KEYS` |

The tokens left unfilled at init raise an error (75–76). Free prose inside them, such as the NEEDS_FILL guidance lines, is bound only where the scripts above name it.

## 7. Routers

**Testing has two overlapping routers.** `00-topic-map.md` is the one router. `SKILL.md` *Reference routing* (214–216) points at it, but the body also routes inline to references 10–90:
- *Designing the tests* steps 92–101 name a reference per step;
- non-negotiables 73, 81;
- the Proof levels section at 105;
- the tier sections at 139, 152, 154.

That is a second, step-ordered routing surface. Its conditions overlap with the topic-map rows.

**Workflow has one router.** `SKILL.md` `## Direct references` (77–90) is the only reference router, with one row per reference. `companion-routing.md` routes to other skills and owns Ponytail and skill bindings; it does not route to references. The body sections at 10–71 still repeat one-line pointers to the same references (for example `context-continuity.md` at 13, 25, 31 and 53).

## Not determined
- I did not check `review-mode.md`, `phase-prompts.md` or `context-curation.md` for repeated rules (word counts only: 864, 970 and 419). `## Finding triage` in `review-mode.md` is the most-cited inbound heading.
- I compared the cc and codex `check_agent_contracts.py` only by diff. The codex line numbers above that I did not grep directly are the cc number minus about 3.
- I could not run a script to map every one of the roughly 230 checker clauses to a line, because the permission system blocked it. Line positions in section 1 came from grep spot-checks, and the per-key clause counts were tallied by hand.
