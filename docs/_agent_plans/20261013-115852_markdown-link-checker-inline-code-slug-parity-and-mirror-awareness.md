# Workflow Plan - markdown link checker: inline-code slug parity and mirror awareness

- Task ID: `20261013-115852_markdown-link-checker-inline-code-slug-parity-and-mirror-awareness`
- Mode: `plan`
- Profile: `resumable`
- Task store: `local`
- Task binding: not applicable
- Status: executing
- Created: `2026-10-13T11:58:52Z`
- Parent plan: not created
- Prompt pack: not created
- Checkpoint: `docs/agents/20261013-115852_markdown-link-checker-inline-code-slug-parity-and-mirror-awareness-state.md`
- Machine state: not created
- Base branch and commit: skills `main` @ `daaa3694c` (clean before this plan); consumer repository `client` `main` @ `ddb2510` (clean)
- Work branch: `main` in place (no commit authority; see decision D4)
- Worktree: none

## Summary and Outcome

- Current repository truth: `skills/sohrab/alaa-repo-docs/scripts/check_markdown_links.py` (461 lines) builds heading slugs from `iter_body()` output, which replaces every inline code span with a space before `HEADING_RE` runs, so the code text inside a heading is lost before `slugify_heading()` sees it. Links that leave a copied contract pack resolve against the consumer tree and report `LINK-MISSING`. No mirror concept exists. Exit contract: 0 clean, 1 findings, 2 could not run.
- Outcome: (1) heading slugs keep inline-code text and drop only the backticks, matching GitHub; (2) declared mirror directories have their outbound and locally-broken links re-checked at the origin path, labelled `healthy in origin` (not counted), `upstream error` (counted separately, exit 1), or `origin unavailable` (never a pass).
- Strategy: one slug function and one mirror-resolution function, both covered by new fixtures in `assets/fixtures` and `--self-test` cases; then align references 10 and 15; then add one mirror declaration file to the consumer repository only if D1 selects a file.

## Scope

- In scope: `skills/sohrab/alaa-repo-docs/scripts/check_markdown_links.py`; new fixture directories under `skills/sohrab/alaa-repo-docs/assets/fixtures/`; `skills/sohrab/alaa-repo-docs/references/10-language-and-links.md`; `skills/sohrab/alaa-repo-docs/references/15-document-size-and-clustering.md`; the `SKILL.md` invocation line only if the command shape it states changes; one mirror declaration file at the consumer repository root (conditional on D1).
- Out of scope: the sibling origin repositories `entitlement-api`, `auth`, `content`, `comment-service`, `wa`, `tusd`, `news` (read only); fixing the tusd upstream anchor; any other consumer file; MCP configuration; other skills; `vendor/`; commit, push, `bd dolt push`, publication.
- Constraints and assumptions: preserve every current finding code and exit code for runs without a mirror declaration; no new third-party dependency (stdlib only, so JSON not YAML); no machine path in a committed file (origin paths are relative to the declaration file); state each instruction once (reference 10 owns link-checker usage, reference 15 points to it).

## Decisions (user set the /goal on 2026-10-13 naming "the approved plan"; recommendations D1-D5 adopted)

- D1 - Mirror declaration form. Recommended: both, sharing one parser: repeatable `--mirror LOCAL ORIGIN` and `--mirror-config PATH` pointing at a JSON file; no auto-discovery, because the tool's existing convention is explicit scope (`--localized-pair`, `--allow-red`) and acceptance needs a run "without declaration" on the same tree. Alternatives: CLI only (nothing in the consumer repository; every caller must repeat seven pairs); config auto-discovered at repo root (silent behavior change for any repository holding the file, and the no-declaration acceptance run then needs an opt-out flag).
- D2 - Exit code when an origin is not on disk. Recommended: print every finding, report each unverified link as `MIRROR-ORIGIN-UNAVAILABLE`, and exit 2, since nothing was proven for those links and 2 already means "not proven". Alternative: count them as ordinary findings and exit 1 (hides the difference between "broken" and "unchecked").
- D3 - Links that stay inside the mirror but fail locally (the tusd `README.md#auth-model` case is one). Recommended: re-check at the origin; broken there too gives `MIRROR-UPSTREAM` (counted separately); healthy there gives `MIRROR-DRIFT` (counted as a local finding, because the copy diverged). Without this the tusd case stays an ordinary `LINK-ANCHOR`, and acceptance criterion 3 fails.
- D4 - Installation. Verified: `~/.claude/skills/alaa-repo-docs` and `~/.codex/skills/alaa-repo-docs` are symlinks into this checkout, so every source edit is live in both runtimes the moment it is written. Recommended: edit in place (the change is backward compatible by design) and make the install step a read-only verification that both links still resolve to the source; no copy runs. Alternative: develop in a separate worktree, which keeps the live copy unchanged but cannot reach the symlinked path without a commit or merge that this run may not perform.
- D5 - GitHub slug divergences found while reading, outside the requested change: the current slug removes `_` and collapses repeated hyphens, while GitHub keeps `_` and does not collapse. Recommended: record them, do not change them in this run (would alter findings in other repositories); open a follow-up.

## Handoff Package

Knowledge held only in the current agent's head disappears on compaction. Fill a field when knowledge is learned, not on a schedule; leave unused fields empty. Field semantics are in the skill's `alaa-workflow references/context-continuity.md`, not in this repository.

- Confirmed facts (verified, each with how it was verified):
  - Baseline: `python skills/sohrab/alaa-repo-docs/scripts/check_markdown_links.py <client-root>` exits 1 with 43 issues in 759 files: 1 RFP `LINK-ANCHOR`, 41 `LINK-MISSING` under `packages/sdk-{auth,comment,content,entitlement,wa}/docs/contracts/**`, 1 tusd `LINK-ANCHOR` (`packages/sdk-tusd/docs/contracts/tusd/api-reference.md:27`, `README.md#auth-model`). Observed 2026-10-13.
  - RFP line 41 targets `#16-alaa-go-chi-consumer-architecture` for a heading containing `` `alaa-go-chi` ``; observed by reading the line.
  - Mirror map (local under client -> origin under the shared parent): `packages/sdk-auth/docs/contracts/auth` -> `auth/docs/contracts/auth`; `packages/sdk-comment/docs/contracts/comment` -> `comment-service/docs/contracts/comment`; `packages/sdk-content/docs/contracts/content` -> `content/docs/contracts/content`; `packages/sdk-entitlement/docs/contracts/entitlement-api` -> `entitlement-api/docs/contracts/entitlement-api`; `packages/sdk-wa/docs/contracts/wa` -> `wa/docs/contracts/wa`; `packages/sdk-tusd/docs/contracts/tusd` -> `tusd/docs/contracts/tusd`; `packages/sdk-news/docs/contracts/news` -> `news/api`. Verified with `diff -rq --strip-trailing-cr`: same file set, no `Only in` lines for all seven.
  - Mirrors are not byte-identical: content diffs per pack (auth 46, wa 18, tusd 17, comment 15, content 65, entitlement 72, news 3). Sampled tusd diff is formatting only (client `oxfmt` reflowed JSON in Markdown). Mapping must therefore be by relative path, never by content or line number.
  - `sdk-news` contributes zero findings; its origin is `news/api`, not `news/docs/contracts`.
  - Installed copies are symlinks to this checkout (see D4); observed with `ls -la` on both skill directories.
  - `DEFAULT_EXCLUDES` already contains `fixtures`, so new fixture trees do not affect repository-wide runs.
- Open assumptions (believed but unverified, each with what would verify it):
  - The 41 outbound links all resolve at the origin; verified only by the user's earlier comparison. Acceptance run 3 verifies it.
- Ruled out (approach, reason, evidence):
  - Content-hash or line-based mirror matching: mirrors are reformatted copies (fact above).
  - Changing `iter_body()` globally to keep code spans: it would make link extraction see links inside code spans, changing existing findings. The heading path alone must keep code text.
- Read first on resume (ordered exact paths): this plan; the checkpoint; `skills/sohrab/alaa-repo-docs/scripts/check_markdown_links.py`; `skills/sohrab/alaa-repo-docs/references/10-language-and-links.md`; `skills/sohrab/alaa-repo-docs/references/15-document-size-and-clustering.md`.
- Environment notes (command shapes that work here, and ones that look right but fail): run the checker with the consumer root as the positional argument from the skills root; `diff -rq` without `--strip-trailing-cr` overstates mirror drift.
- Review outcomes: code review (alaa-reviewer) REQUEST_CHANGES -> APPROVE_WITH_FINDINGS after fix cycles 1-2; remaining nits recorded: `_` stripped outside code spans and hyphen collapse are known GitHub-parity gaps (D5). Instruction review (alaa-instruction-reviewer) REQUEST_CHANGES x2 -> APPROVE_WITH_FINDINGS; stale slug comment fixed; line-wrap nits accepted. Deferred: 11 newly-correct LINK-ANCHOR findings in alaa-docker-production (out of scope; follow-up task raised); client AGENTS.md does not name markdown-links.mirrors.json (client change out of scope); optional split of reference 10's checker section into its own reference.
- Traps (looks correct, is not): editing the source script is an installation on this machine (D4). An origin outside the consumer root must not be reported as `LINK-OUTSIDE-ROOT` once a mirror maps it.

## Skill Bindings

| Skill | Source | Load before | When | If unavailable |
|---|---|---|---|---|
| alaa-repo-docs | `skills/sohrab/alaa-repo-docs/SKILL.md` | Phase 1, Phase 2 | always (owns the tool and its references) | block |
| alaa-testing-strategy | `skills/sohrab/alaa-testing-strategy/SKILL.md` | T2 fixture design | always | block |
| alaa-low-noise | `skills/sohrab/alaa-low-noise/SKILL.md` | every dispatch | always | proceed with bounded output, record gap |
| alaa-prompting-guide | `skills/sohrab/alaa-prompting-guide/SKILL.md` | T5 wording; every model/effort record | always for instruction text and allocation | block |
| alaa-code-intelligence-routing | `skills/sohrab/alaa-code-intelligence-routing/SKILL.md` | review lanes' evidence choice | when a lane needs code relationships | use Read/Grep, record gap |
| alaa-cc-orchestrator | `skills/sohrab/alaa-cc-orchestrator/SKILL.md` | every dispatch | always | block |

## Ordered Work

Keep only phases with a distinct decision, authority or integration barrier. Merge compatible work while retaining each acceptance outcome and evidence mapping.

### Phase 1 - Implement checker capabilities

- Status: pending (waits for user approval of D1-D5)
- Depends on: none
- Reasoning and selection reason: ordinary engineering judgment; design settled once D1-D5 are answered; local causal path known for the slug defect.
- Settled/open decisions and invariants: invariants: no new finding code fires without a mirror declaration; existing self-test cases keep their expected codes; exit contract 0/1/2 unchanged; one slug function; one mirror-resolution function; stdlib only.
- Risk and required observers: medium (live-installed tool, D4); observers: alaa-verifier, alaa-reviewer.
- Owned scope: the script and new fixture directories.
- Excluded from this phase: references, `SKILL.md`, consumer repository.
- Required skills: alaa-repo-docs, alaa-testing-strategy, alaa-low-noise
- Work:
  - [x] T1: Ground baseline on the consumer repository and map mirrors to origins. [depends: none] [skills: inherit]
  - [x] T2: Implement inline-code slug parity and mirror resolution with fixtures and self-test cases (clean inline-code anchor; healthy-in-origin; upstream error; drift; origin unavailable; no-declaration regression). [depends: T1] [skills: inherit]
- Acceptance criteria: `--self-test` passes all old and new cases; a run without declaration on the consumer repository no longer reports the RFP finding and still reports the other 42 unchanged.
- Validation commands: `python skills/sohrab/alaa-repo-docs/scripts/check_markdown_links.py --self-test`; `python skills/sohrab/alaa-repo-docs/scripts/check_markdown_links.py <client-root>`.
- Evidence observed: T1 baseline above.
- Snapshot: not captured yet

### Phase 2 - Align references and consumer declaration

- Status: pending
- Depends on: Phase 1
- Reasoning and selection reason: instruction text controlling other agents; separate authority (instruction reviewer) and a different repository write.
- Settled/open decisions and invariants: reference 10 owns usage and labels; reference 15 points to it without restating; consumer change limited to one declaration file (D1).
- Risk and required observers: low; observers: alaa-instruction-reviewer.
- Owned scope: references 10 and 15; `SKILL.md` invocation line if needed; consumer declaration file.
- Excluded from this phase: script.
- Required skills: alaa-repo-docs, alaa-prompting-guide, alaa-low-noise
- Work:
  - [x] T3: Update references 10 and 15 for the slug rule, mirror declaration, labels and exit semantics. [depends: T2] [skills: inherit]
  - [x] T4: Add the mirror declaration file for seven packs at the consumer root (only if D1 selects a file). [depends: T2] [skills: alaa-repo-docs, alaa-low-noise]
- Acceptance criteria: references match implemented flags and labels exactly; consumer diff is exactly one new file.
- Validation commands: checker run on the skills pack docs touched (`--files` both references); `git -C <client-root> status --short`.
- Evidence observed: not run
- Snapshot: not captured yet

### Phase 3 - Verify, review, install check

- Status: pending
- Depends on: Phase 2
- Reasoning and selection reason: independent verification and review authority.
- Settled/open decisions and invariants: reviewers never edit; fixes return to the owning lane.
- Risk and required observers: alaa-verifier, alaa-reviewer, alaa-instruction-reviewer.
- Owned scope: none (read only); fixes reopen T2 or T3.
- Excluded from this phase: any commit or publication.
- Required skills: alaa-cc-orchestrator, alaa-low-noise
- Work:
  - [x] T5: Run acceptance and repository gates. [depends: T3, T4] [skills: inherit]
  - [x] T6: Independent reviews of code and references; resolve or disposition findings. [depends: T5] [skills: inherit]
  - [ ] T7: Installation step per D4, only after explicit user approval at that point. [depends: T6] [skills: inherit]
- Acceptance criteria: self-test passes; no-declaration run has no RFP finding; declared run exits 1 with exactly one counted finding (tusd upstream) and 41 `healthy in origin`; the four repository checkers exit 0; review findings resolved or dispositioned.
- Validation commands: `python scripts/validate_sohrab_skill_pack.py`; `python scripts/check_skill_index.py`; `python scripts/check_fleet_references.py`; `python scripts/check_lifecycle_contract.py`; self-test; two consumer runs.
- Evidence observed: not run
- Snapshot: not captured yet

## Task Allocation

After finalizing tasks, dependencies and consolidation, record the runtime orchestrator's all-role allocation.
In Codex, `/alaa-codex-orchestrator` owns `references/routing-matrix.md`.
In Claude Code, `/alaa-cc-orchestrator` owns `references/routing-matrix.md`.
Prompting-guide supplies capability/mechanics evidence; workflow stores decisions. Unresolved controls or availability block the affected dispatch. Material changes reassess only affected remaining tasks.

| Task/scope/complexity | Role authority | Priority/reason | Model | Effort | Selection/admission evidence and source date | Invocation/requested/effective controls | Availability/limits |
|---|---|---|---|---|---|---|---|
Pair support source: `alaa-prompting-guide assets/claude-model-policy.json` (verified_on 2026-10-09; all three models list low..max). Invocation: Agent tool `model` + `effort` parameters.

| Task/scope/complexity | Role authority | Priority/reason | Model | Effort | Selection/admission evidence and source date | Invocation/requested/effective controls | Availability/limits |
|---|---|---|---|---|---|---|---|
| T1 evidence, retrieval | lead inline | done | session model | session | inline grounding, 2026-10-13 | n/a | done |
| T2 script + fixtures, ordinary judgment, bounded | alaa-implementer | high; grounded work, explicit acceptance | claude-sonnet-5-5 | high | routing-matrix All-role allocation | requested sonnet/high; effective unobservable | available |
| T3 references, instruction text | alaa-documenter | medium | claude-sonnet-5-5 | high | instruction text with exact flag names from T2 | requested sonnet/high | available |
| T4 one JSON file, mechanical | alaa-implementer-haiku (mechanical branch) | low; exact content enumerated in dispatch | claude-haiku-5-5 | low | exact content, one new file, discriminating check = checker run | requested haiku/low | available |
| T5 gates | alaa-verifier | required | claude-sonnet-5-5 | medium | independent observer | requested sonnet/medium | available |
| T6 code review | alaa-reviewer (standard) | required | claude-opus-5-5 | high | standard depth; no deep trigger | requested opus/high | available |
| T6 references review | alaa-instruction-reviewer | required (instruction trigger) | claude-opus-5-5 | high | instruction-change trigger | requested opus/high | available |

## Delegation

- Keep shared-context work in the main conversation.
- Independent lane ownership, if admitted: T2 owns the script and new fixtures; T3 owns references 10/15 and `SKILL.md`; T4 owns one consumer file.
- Dependency edges and ready sets: Local task prerequisites above own dependency edges; derive readiness before dispatch.
- Disjoint writes and shared-resource conflicts: T3 and T4 are disjoint and may run in parallel after T2; both read the T2 flag names, so T2 must be final first. The live symlinked install is a shared resource touched by T2 and T3.
- Integration barriers and parallel/serialized rationale: T2 before T3/T4 (flag and label names); T5 after both; T6 after T5.
- Consolidated tasks/checks and preserved outcome/evidence mappings: acceptance runs 2 and 3 run once in T5; the implementer runs only self-test and the no-declaration run.
- Reusable evidence and invalidation conditions: T1 baseline remains valid until the consumer repository or any origin pack changes.
- Dispatches assume zero shared context: copy the relevant handoff-package facts into the dispatch text rather than referring to this conversation.
- Lanes report changed paths; this plan's owner records the validated snapshot and handles any explicitly authorized commit.

## Execution Position

- Position owner: `docs/agents/20261013-115852_markdown-link-checker-inline-code-slug-parity-and-mirror-awareness-state.md` (current phase, blockers, next action).

## Review follow-up evidence

- The user authorized both review repairs, a failing-first regression, relevant checks, and a local commit.
- Added `mirror-locally-added-links` before changing production behavior. The exact-case suite exited 1: local defects were incorrectly classified as three upstream errors, an origin-boundary error, and an extra healthy-origin result.
- Origin classification now requires the extracted link target to occur in the origin document. Locally introduced links use ordinary local checks; per-run caching avoids rereading origin documents for each link. The regression covers missing files, missing anchors, consumer-root escape, an origin-only healthy target, and shared links with different Markdown formatting.
- Corrected the fixture's root-escape depth without changing its assertions. Disabling the provenance guard in memory reproduced the failure; the actual implementation passed every exact case. The complete `check_markdown_links.py --self-test` then exited 0 with all 45 cases passing, using the verified outside-sandbox workaround for Windows temporary-directory permissions.
- `validate_sohrab_skill_pack.py`, `check_skill_index.py`, `check_fleet_references.py`, and `check_lifecycle_contract.py` each exited 0. Link validation passed for the 20 changed non-fixture Markdown files; `git diff --check HEAD` passed.
