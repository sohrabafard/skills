# Whole-skill low-noise STE-inspired pilot: static comparison

Date: 2026-10-24. Task authority and acceptance: Beads issue `alaa-okil`.

## Scope and method

The candidate changes `skills/sohrab/alaa-low-noise/SKILL.md` and all four Markdown files in its `references/` directory. Each now has a purpose-oriented introduction and short, direct rules with explicit conditions and stable terms. This is STE-inspired writing, not a claim of full ASD-STE100 dictionary compliance.

The first pass covered only the entry point. The user clarified that the intended outcome covers the whole skill. Issue `alaa-okil` was reopened with that acceptance scope. The entry-point comparison below remains valid; the reference comparisons and final evidence now cover the complete skill.

Baseline: `69eadc60dc969acf7356737f22fe1a31453bb73f` on `main`. The initial worktree was clean. The whole skill was read, including its four references and interface metadata. No skill-local scripts or additional nested instruction files were present in its file inventory.

The author compared each original paragraph and list item with the final text, then walked the scenarios below. This is a static semantic review, not independent review or a live agent A/B evaluation. Structural gates cannot prove model compliance or performance improvements.

The requested restructuring adds an Introduction to each Markdown file and separates rules within their original owning files. It moves no rule across a file or loading boundary. Existing headings, reference loading, frontmatter, source priority, source URLs, code examples, and interface metadata remain unchanged. No new decision procedure, stop rule, permission, or model policy was introduced. The two legacy `$alaa-codex-runtime-ops` calls in the edited patterns reference use the repository-required `/alaa-codex-runtime-ops` form.

Each rewrite received a second compression pass. Review preserved preference verbs for fallback artifact paths and explicit child/writer subjects for delegated-lane restrictions. The entry-point review also clarified an ambiguous reference to the Codex-only recovery skill. Final source gates ran after the last source correction.

## Entry-point clause preservation

Baseline locations refer to sections in the baseline commit. Candidate locations refer to line numbers in the final `SKILL.md`.

| Original clause or group | Candidate lines | Static finding |
|---|---|---|
| Frontmatter: both runtimes, all activation triggers, exclusions, quality safeguards, workflow owner | 1-4 | Byte-identical |
| Opening: distinct context and output controls, recurring context cost, context priority, unchanged effort/evidence/validation/reviewability | 10 | Preserved; introductory purpose comes from these existing aims |
| Companion scope, domain implementation, workflow planning/state, no planning advice, runtime parity and exceptions, frontmatter ownership | 14 | Preserved |
| Contract: real task, repository truth | 20 | Preserved |
| Required facts, decisions, caveats, validation, blockers, next steps | 21 | Every item retained |
| Trim introductions, repetition, proof-of-work narration, raw dumps, optional background first | 22 | Every item and priority retained |
| Explicit full-log, full-diff and full-file requests override trimming | 23 | Preserved |
| Repository conventions and active workflow artifact family, no competitor | 24 | Condition and owner retained |
| Long-run observability, bounded calls, host-required concise updates | 25 | Preserved |
| Safe independent batching; sequential dependent operations and mutations | 26 | Safety condition and ordering retained |
| No universal watchdog assumption; no per-command narration; stricter repository invocation rules | 27-29 | Preserved |
| Context bullet 1: recurring-cost retrieval decisions | 33 | Preserved |
| Context bullet 2: search/inventory, bounded slice, whole-file safe-edit exception | 34 | Sequence and exception retained |
| Context bullet 3: new reason to reread; own edits, failed checks and changed hypotheses qualify; reassurance does not | 35 | Preserved; examples remain non-exhaustive |
| Context bullet 4: prefer targeted searches, changed paths and counts to raw dumps | 36 | Preference remains a preference |
| Context bullet 5: batch independent reads/searches in one supported turn; prefer one chosen query | 37 | Runtime condition and preference retained |
| Context bullet 6: capture bulk, inspect relevant/failing slice, keep path | 38 | Preserved |
| Output medium: every listed working-material category and reusable state belongs in files; report paths | 42 | Categories, future consumers and terminal-cost rationale retained |
| Requested reviews, assessments, explanations and advice belong in replies | 44 | Preserved |
| Read workflow admission owner before choosing plan medium; preserve exceptions; save admitted plan/checkpoint and report outcome/paths | 44 | Trigger, owner, destination and reporting retained |
| No unrequested files for advisory/read-only requests outside admission; document owner | 44 | Both conditions and owner retained |
| Brevity cannot remove required checklists, resume context or phase/task skill bindings | 44 | Every protected item retained |
| Only milestones, blockers, scope changes, validation outcomes and useful paths; no harness-status duplication | 46 | Preserved |
| Bounded terminal output; file/tree/manifest/log exclusions; preferred tools and diff shapes | 47 | Preserved |
| Default 12 prose lines / 20 excerpt lines; progress only; deliverable/findings exclusions; excess required content survives; authorized artifact for bulk | 48 | Exact numbers and all exceptions retained |
| Artifact retention helps inspection/resume; outcome/path; safe throwaway cleanup; implementation in ordinary repo files, never temp/history/off-repo | 49 | Conditions and prohibited locations retained |
| Final changed paths, reasons, validation, risks/blockers instead of large diff | 50 | Preserved, subject to the shared explicit-output exception |
| Sandbox/refresh/locking/quoting/command-length failures: essential failed work only, serial bounded retry; Codex recovery first, no Claude equivalent | 51 | All failure classes, sequence and runtime limit retained |
| Leak 1: plan narration only for a prior user decision; otherwise execute and report | 57 | Condition and rationale retained |
| Leak 2: result, meaningful line and path rather than transcript as proof | 58 | Preserved |
| Leak 3: path and change instead of restating an openable deliverable | 59 | Preserved |
| Calibration trigger, response/artifact/progress separation, prompting owner, no local model/effort policy | 63 | Preserved |
| Four negative-use cases and their reasons/owners | 67-70 | Preserved |
| Four reference routes, destinations and triggers, needed-only loading | 72-79 | Byte-identical router |
| Final check: quality/evidence, justified bounded input, output budget, durable state, reviewability and no duplicate ownership | 83-90 | Preserved; budget exceptions remain those already defined above |

## Reference clause preservation

Each row maps a complete original paragraph, list or procedure to the final section in the same file. Rationale moved only within its original file to provide the requested introduction. These are author static findings.

| File and original clause | Final location | Finding |
|---|---|---|
| `model-output-profiles.md`: output/context ownership; prompting read before model claims or model/effort choice; conditional router; no local profiles/policy | Ownership | All boundaries and read conditions retained |
| Same: separately calibrate long responses, written artifacts and progress; required content, useful cadence and protected detail | Calibration rules | Trigger, three output surfaces and every protected item retained |
| Same: no effort-as-verbosity control and no inference that lower effort meets length target | Calibration rules | Both prohibitions retained as prohibitions |
| Same: tool output dominates context; bound retrieval, retain useful full evidence path, no reassurance discovery | Calibration rules | Condition, action and prohibition retained |
| Same: shorter reports and fewer calls prove neither reasoning nor coverage | Introduction | Both limitations retained without a new obligation |
| Same: distinguish focused checks, independent acceptance and repetition before removal; preserve first two | Validation rules | Preserved |
| Same: remove repetition only without new change, failure or unresolved concern | Validation rules | All three disqualifying conditions retained |
| Same: representative tasks, identical required content/acceptance, retain change only if coverage and authority survive; no universal guarantee | Validation rules; Ownership | Evaluation contract and limitation retained |
| `workflow-integration.md`: read only for active workflow or delegated execution | Introduction | Exact trigger retained |
| Same: low-noise owns context/output; workflow owns modes, artifacts/naming, continuity and lane ownership | Ownership rule | Every owner and item retained |
| Same: workflow decides overlapping artifact structure; low-noise decides read/print volume; no phase/plan/state layout decisions | Ownership rule | Preserved |
| Same: existing artifacts retain durable reasoning; no competing notes; logs use existing repo/workflow locations | Artifact routing | Shared condition and all actions retained |
| Same: inactive workflow but useful bulky artifact; prefer repository convention, then small local fallback | Artifact routing | Preference remains a preference; useful-artifact condition retained |
| Same: context economy before parallelism, child bears discovery context, only return reaches parent | Introduction | Rationale retained |
| Same: parent synthesis/report; child result-only return, prohibited raw forms; discovery conclusions/evidence; writer scope/changed paths | Delegated lanes | All subjects and return boundaries retained |
| Same: explicit child return shape/length; flooding rationale; no summary-only lane obtainable with a couple of bounded parent reads | Delegated lanes | Threshold, rationale and prohibition retained |
| Same: prompting owner for delegation authority/capability; identical runtime return contract | Delegated lanes | Preserved |
| Same: workflow artifact admission; compact discovery/validation/reporting; domain code/runtime/architecture | Good pairing pattern | Preserved |
| Same: polarity differs by family/generation; read calibration reference before cap/authorization assumption; fallback paths rank below conventions/workflow | Caveats | Trigger, precedence and caveats retained |
| `90-source-map.md`: current runtime/shell/model-policy read trigger | Introduction | Exact trigger retained |
| Same: seven ranked source classes and all endpoints | Source priority | Byte-identical ordered section |
| Same: latest runtime/new shell or tool behavior; large logs/new runners/caps; fan-out; context/compaction/caching | Freshness triggers | Every trigger and cost rationale retained |
| Same: model-change dimensions; read calibration reference first; re-verify against vendor docs for model newer than file | Freshness triggers | All dimensions, order and conditional re-verification retained |
| Same: smallest adequate instruction set; add rule only for demonstrated gap; repetition cost | Standing policy | Preserved |
| Same: prioritize required facts/evidence/caveats/validation/blockers/next steps before trimming; generic brevity danger | Standing policy | Complete protected list and rationale retained |
| Same: token/call/turn reduction is improvement only above quality bar; positive explicit output shape; no rituals/repeated phrasing | Standing policy | Condition and prohibitions retained |
| Same: newer capability does not remove bounded reads, reviewability or validation | Standing policy | Preserved |
| Same: 2,000-line log and six-file anti-patterns with useful capture, failing slice, command/result/path, bounded read and stop | Domain-bounded anti-patterns | Examples and replacement actions retained |
| Same: documentation endpoints can move; HTTP 404 routes to vendor root, no guessing | Caveats | Same condition and fallback; `404s` became `returns 404` |
| Same: no cross-runtime verification inference; prompting owns model/runtime claims; calibration reference copies no policy | Caveats | Preserved |
| Same: source links | Sources | Byte-identical URLs and order |
| `noise-control-patterns.md`: context versus output/storage split; runtime-neutral except named sections | Introduction | Preserved |
| Same: search/read/full-file/summarize sequence, stop when answered, safe-edit whole-file exception | Discovery and bounded reads | Procedure unchanged |
| Same: scoped search/context/count/path/query preferences and default avoidance of full dumps, generated trees, unjustified rereads and large results | Discovery and bounded reads | Every preference, default and qualifying reason retained |
| Same: Claude native-tool preference and cost rationale; bounded ranges; concurrent independent search; wide-sweep delegation returning findings/paths | Runtime notes | Conditions, outputs and rationale retained |
| Same: Codex shell bounds, real paths, small context and output filters; five failure classes, recovery owner, essential serial bounded retry | Runtime notes | All controls and runtime boundary retained |
| Same: preferred diff command shapes; default final fields; full repository diff only on user request | Diff and reporting patterns | Commands, default and exception retained |
| Same: long log capture directory/full output/tail or failure/result path; useful durable retention and safe cleanup before finishing | Large-log capture patterns | Procedure and both cleanup/retention conditions unchanged |
| Same: PowerShell examples, all streams, selective reads, status/stat before detailed diff | PowerShell notes | Code fences and notes unchanged |
| Same: Bash examples, bounded tools and scoped diff before larger output | Bash notes | Code fences and notes unchanged |
| Same: explicit full-output request, output scope, relevant section first, no unrelated mixing | When the user wants raw output | All conditions and handoff obligations retained |
| Same: command portability caveat; installed-shell/version verification before scripting; changing Claude tool parameters; no Claude recovery counterpart | Caveats | Preserved |

## Scenario walkthrough

For each row, the baseline and candidate select the same action on textual inspection. These are static walkthroughs, not observed executions by another agent.

| Scenario | Action under both versions | Candidate evidence |
|---|---|---|
| A narrow symbol question after broad inventory | Read the relevant bounded slice | 34, 36 |
| Safe editing requires the whole file | Read the whole file | 34 |
| The agent wants to reread unchanged evidence for reassurance | Do not reread | 35 |
| An edit, failed check or changed hypothesis makes evidence stale | A reread has a qualifying new reason | 35 |
| Independent reads are safe and supported in one turn | Batch them | 26, 37 |
| A mutation depends on an earlier read | Keep dependent work and mutations sequential | 26 |
| A long validation log contains a small failure | Save the full log, inspect the failing slice, retain/report its path | 38, 42, 58 |
| The user explicitly requests a full diff | Deliver the requested raw output; do not apply trimming as a substitute | 23, 68 |
| Required progress content exceeds the default budget | Preserve required content; place bulky working material in an authorized artifact | 48 |
| A requested assessment has no admitted plan or requested file | Put advice in the reply; create no file | 44 |
| An execution plan is admitted by workflow | Save plan/checkpoint, preserve required bindings and resume content, report paths | 24, 44 |
| The active host requires progress updates during a long call sequence | Keep work observable with bounded calls and concise host-required updates | 25, 27 |
| Codex experiences a quoting or lock failure | Invoke the recovery owner first; retry only essential failed work serially with bounded output | 51 |
| Claude Code experiences the same failure class | Follow the serial bounded retry rule without invoking a Codex-only owner | 51 |
| The harness already displays status | Do not repeat it | 46 |
| A proposed plan requires a user decision before execution | State the plan before running it | 57 |
| A throwaway artifact cannot safely be removed | The safe-cleanup condition does not authorize removal | 49 |
| A model-specific verbosity decision is needed | Read the calibration reference and follow its prompting-owner route | 63, 76 |
| The entire task fits in one read and one edit | Do not activate this skill for that task | 67 |

Reference scenarios use final section names instead of entry-point lines:

| Scenario | Action under both versions | Reference evidence |
|---|---|---|
| Only progress is verbose while the requested artifact needs detail | Calibrate progress separately and preserve requested artifact detail | Calibration rules |
| A shorter report is proposed as evidence of better reasoning | Do not treat length as that evidence | Calibration Introduction |
| An effort reduction is proposed merely to meet a word target | Do not use effort as verbosity control or infer the target will be met | Calibration rules |
| Repeated checks have no new input, failure or unresolved concern | They may be removed; focused checks and independent acceptance remain | Calibration Validation rules |
| A new change, failure or unresolved concern justifies repetition | Retain the justified repeated check | Calibration Validation rules |
| Calibration saves tokens but loses required coverage or authority compliance | Do not retain that calibration change | Calibration Validation rules |
| Workflow artifacts already exist | Reuse them for durable reasoning and use existing log paths | Workflow Artifact routing |
| Workflow is inactive and a bulky artifact is useful | Prefer repository conventions before a small local fallback | Workflow Artifact routing |
| A child offers a full transcript | Require bounded findings/counts/verdicts/paths instead | Workflow Delegated lanes |
| A writer lane completes an owned change | Report its changed paths within its scope, not a diff | Workflow Delegated lanes |
| A parent can obtain a proposed summary with two bounded reads | Do not spawn a summary-only lane | Workflow Delegated lanes |
| A new model affects verbosity or delegation | Read calibration routing first; re-verify vendor guidance if newer than the reference | Source map Freshness triggers |
| A source URL returns HTTP 404 | Navigate from the vendor documentation root, not a guessed path | Source map Caveats |
| A rule was verified only on Claude Code | Do not infer it is verified for Codex | Source map Caveats |
| A community answer is available without a concrete tool/shell failure | It does not qualify for the seventh source tier | Source map Source priority |
| A symbol search answers the question before a full-file read | Stop discovery at the answering step | Patterns Discovery and bounded reads |
| Claude needs a wide sweep across many files | Delegate the sweep and require findings or paths instead of excerpts | Patterns Runtime notes |
| Codex uses shell search | Scope real paths, bound context and filter output | Patterns Runtime notes |
| A full log is explicitly requested | Deliver it with scope and relevant section identified; keep unrelated outputs separate | Patterns When the user wants raw output |
| A command example will become a script on another shell/version | Verify actual installed syntax first | Patterns Caveats |

## Evidence and limits

- The whole six-file skill changed from 3,222 to 2,996 whitespace-delimited words and from 21,920 to 21,041 bytes. Five Markdown files changed; interface metadata did not. Counts for each file are in the JSON evidence. Added headings and separated rules can increase line counts without increasing total content size.
- [validation.json](validation.json) records the snapshot, counts and structural invariants. [scope.sha256](scope.sha256) records all six skill files. The final scoped digest is `7c48f6f93facb6600a986f3e3d032bfeec842cd07995096d9a122430ef96a769`.
- Snapshot method: sort relative POSIX paths; write each file's SHA-256, two spaces, path and LF; SHA-256 those manifest bytes. Source writes were frozen for final validation.
- All checks use the local Linux Python toolchain. The `-B` option avoids creating bytecode caches.
- No live model comparison, installed-skill activation, package installation, commit, push, remote synchronization, release or publication was performed.
- This report, manifest and JSON evidence are untracked local artifacts; logs are ignored. The source edit remains uncommitted. No full ASD-STE100 compliance or live behavior guarantee is claimed.
- The supplementary numeric-extraction check failed twice: the first pattern omitted baseline `404s`; its one corrected retry included the comma in candidate `404,`. No further retry was made, and the failed result remains in the JSON evidence. Direct source review confirms the unchanged HTTP 404 fallback. Source numbering and command examples are byte-identical; the 2,000-line and six-file examples and the 12/20 progress bounds also survive. This manual evidence supports numeric preservation; the automated numeric check does not.

| Command | Observed result | Evidence |
|---|---|---|
| `python3 -B scripts/validate_sohrab_skill_pack.py` | Exit 0; unrelated body-length warnings, none for alaa-low-noise | [Log](validate_sohrab_skill_pack.log) |
| `python3 -B scripts/check_skill_index.py` | Exit 0; no findings | [Log](check_skill_index.log) |
| `python3 -B scripts/check_fleet_references.py` | Exit 0; no blocking findings; informational legacy paths remain | [Log](check_fleet_references.log) |
| `python3 -B scripts/check_lifecycle_contract.py` | Exit 0; no findings | [Log](check_lifecycle_contract.log) |
| `git diff --check` | Exit 0 | Whitespace validation of the final source diff |

Changed checker self-tests were not applicable: no checker changed. No skill-local validator exists. No workflow plan or checkpoint was admitted for this bounded, issue-only edit.
