# Official-source check

Read-only researcher lane, 2026-11-17. Dated evidence. Items marked unverified or open stay so until a later fetch.

## Researcher return

STATUS: COMPLETE. Four questions answered from official sources fetched 2026-11-17 (system date; `date -u` read 2026-11-16). Items marked "page-text unverified" came through WebFetch summarisation and are not exact quotes.
AGENT: alaa-researcher. CONFIGURED: not inspected. REQUESTED: Sonnet 5.5 (`sonnet`), effort medium. OBSERVED: model claude-sonnet-5-5; effort unknown.
Checkout: skills/sohrab/alaa-prompting-guide/references (files 41, 50, 90, 12).
Fetch notes:
- code.claude.com/docs/en/advisor failed twice in WebFetch. I read it through the same URL with `.md` appended (curl, HTTP 200).
- The advisor-tool page was read to char 100000 of 124522, then 100000 onward. The Fable-specific text in the middle part is covered only by the summariser's report of "no guidance".
- The model-selection page text has no matrix (it is JS-rendered). The cited asset `ModelSelection.react.DJkmSLnH.js` now returns 404. I used the current asset `ModelSelection.react.BKCv-TnC.js` (reviewedAt 2026-09-17), downloaded from the guide's HTML.

## Q1 Advisor in prompts
Table: A = Claude Code session or subagent. B = API or Agent SDK caller writing the executor system prompt.
| Executor | A (Code page) | B (platform page) |
|---|---|---|
| Haiku 5.5 | write nothing by default. The Code page says only: "You can ask for a consultation in your prompt ... if you want Claude to consult more or less often ... say so" | Haiku coding block replaces timing+weight blocks, for coding/write-task loads only (it cost about 4 points on a browse benchmark). Quote: "Hard rule: your first write_file, edit_file, or state-changing bash call on a task must be preceded by an advisor call". Optional second-turn nudge: "You have not consulted the advisor yet." (page-text unverified) |
| Sonnet 5.5 | write nothing | copy the timing block ("Call advisor BEFORE substantive work") then the weight block ("Give the advice serious weight"). Nudge: "no measurable effect" |
| Opus 5.5 | write nothing | "Calls at a reasonable rate without extra prompting"; the timing and weight blocks are the page's default for coding prompts. Optional checkpoint only if under-calling is observed. Do not nudge. |
| Fable 5.2 | write nothing | page gives no guidance beyond rejecting `tool_choice` types `tool` and `any` (page-text unverified) |
Contradicted or extended statements in `41` (URLs: Code=code.claude.com/docs/en/advisor, Plat=platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool):
- 41:46 "needs the Anthropic API or Claude Platform on AWS": EXTENDS. Code page: "or Claude Models on Google Cloud (Anthropic managed)"; v2.1.300+ on the two cloud providers; "isn't available on Amazon Bedrock, Google Cloud's Agent Platform, or Microsoft Foundry"; needs a feature flag fetch (`DISABLE_TELEMETRY` breaks it). Plat: the same three platforms.
- 41:44 Start: EXTENDS. Code page: `/advisor` also works with `-p`, in the Agent SDK and the desktop app from v2.1.260; `/advisor off` exists; `--advisor` is "not in claude --help" and exits at launch on an invalid pair; a background session starts without the advisor instead.
- 41:52-55 pair rows: MATCH (Haiku 5.5 / Sonnet 5.5 / Opus 5.5 / Fable 5.2). Code page also has "Haiku 4.5 can call the advisor but can't act as one" and Haiku 5.5 needs v2.1.293+.
- 41:57 "runs no consultation and raises no error": EXTENDS. Code page: "The /advisor command output and a notification show this", and "Subagents whose own model satisfies the pairing may still use the advisor."
- 41:63 subagent inheritance: MATCH ("Subagents inherit the configured advisor and apply the same pairing check").
- 41:78 "For a Haiku coding executor the platform page gives a hard-rule block and a second-turn nudge; its stated evidence is Haiku 4.5": DIFFERS in part. The page now labels the block "Haiku 5.5" ("raised Haiku pass rates about 7.5 points"). Only the nudge cites Haiku 4.5 (about 7 points). Page-text unverified.
- 41:78 Opus/Sonnet: MATCH. The Opus checkpoint text exists on the page and 41 does not mention it (EXTENDS).
- 41:79 `tool_choice` rejection for Fable 5.2, Opus 5.5, Sonnet 5.5: MATCH. The page also lists Mythos 5.2, Fable 5.1 and Mythos 5.1.
- 41:81 length line: EXTENDS. Plat: tool `max_tokens` minimum 1024, "recommended starting point: 2048"; the line "(Advisor: please keep your guidance under 80 words. I need a focused starting point, not a comprehensive plan.)". 41:81 gives no starting value. The Managed Agents advisor takes no `max_tokens`.
- 41:80 "Claude Code has no setting that caps or forces calls": MATCH. Code: "There is no setting to cap or force advisor calls".
- 41:71 "page disagrees with itself on executor reasoning": MATCH (core section lists text only; Haiku block says "your reasoning").
- 41:83-85 surface split: MATCH. The Code page gives no timing or weight block. "Observed in 2.1.307" is not on any page.
- Advisor must be "at least as capable as the executor" (Plat): extends 41:48-57.

## Q2 Claude model and effort (platform.claude.com: about-claude/models/choosing-a-model, models/overview, build-with-claude/effort)
- 90:73-76 "Effort evidence: Unspecified": DIFFERS. Choosing-a-model: "On Claude Fable 5.2 ... and Claude Sonnet 5.5, start with the default (`high`) ... On Claude Opus 5.5 and Claude Haiku 5.5, the default is `medium`". Overview "Default effort" row matches: Fable high, Opus medium, Sonnet high, Haiku medium. These are Messages API defaults. For Managed Agents "fills in the model's default". For Claude Code the three pages give no default for the 5.5 models: open (code.claude.com/docs/en/model-config was not in scope).
- 90:79 "No selected Fable effort": EXTENDS. Effort page: "Start with `high`", `xhigh` for hardest long-running work "where you've measured a gain", "Step down to `medium` or `low` where your evals show quality holds", reserve `max` ("often for only a small gain").
- 90:77 Haiku "No task-specific effort": DIFFERS. Effort page: "Start with `medium`", `low` for "chat, short tool tasks, and simple, high-volume requests", but at `low` "more likely to skip a search, stop early, or skip a check" in long agent prompts. `high` for "knowledge work, longer agent tasks, and strict instruction following". `xhigh` or `max` only where evals show a gain, compared against Sonnet 5.5.
- 90:83 "Sonnet prompting page, not the selection guide, gives medium/high": DIFFERS. The effort page now says it: "For agentic coding and multistep tool use, start with `medium` for well-specified tasks and move to `high` for harder or longer ones. For chat ... `medium` or `low`. Use `xhigh` or `max` only where your evals show a quality gain". Sonnet's `high` default applies unless "agentic or latency-sensitive".
- 90:74 Opus: EXTENDS. Effort page: Opus 5.5 default `medium`; "A request that omits effort runs one level lower" than Opus 5. Overview: Opus 5.5 is "start with Opus 5.5 for most workloads".
- 90:70-82 workload rows: MATCH. Extensions: Opus adds "vision-heavy workflows"; Haiku overview adds "classification, extraction, and routing". Choosing-a-model: "Tuning effort is often a better lever than switching models."
- 50 lacks lowering guidance (EXTENDS), all from the effort page:
  - Lower effort means "fewer and terser tool calls" and "Combine multiple operations into fewer tool calls".
  - Step down only where evals hold quality (Fable). `low` suits "Simpler tasks ... such as subagents".
  - Haiku `low` risk of skipped checks in long agent prompts.
  - Changing top-level effort between requests "can invalidate" the prompt cache. Per-message effort preserves it on supported platforms. With Sonnet 5.5 `between_tools` or Haiku 5.5 disabled thinking, a mid-conversation effort change returns 400.
  - Sonnet 5.5 `thinking: disabled` is unsupported; use `between_tools` (low, medium, high only).
- 50:9, 50:14, 50:16, 50:21: MATCH (effort does not shorten replies; lower effort to cut thinking; Haiku 5.5 disabled thinking only at `high` or below).

## Q3 Codex (learn.chatgpt.com/docs/models; developers.openai.com/api/docs/guides/model-selection; learn.chatgpt.com/docs/agent-configuration/subagents)
Differences:
- 90:49-50 computer use rows: DIFFERS. Asset: "Find visible controls in an app" and "Update specified records in an app" are `usage Sol low | balanced Terra medium | quality Sol high` (Oct 21 editorial update). 90 shows Sol medium in the balanced cell.
- 90:28 "Adapt existing content": EXTENDS. Asset adds the alternative `terra61 medium`, with Sol kept as primary.
- 90:88 asset URL: STALE. DJkmSLnH returns 404; current is `BKCv-TnC`. All other matrix rows (90:26-48, 51-52) match cell for cell.
- 90:62-67 guide prose: MATCH (seven model/effort pairings; Astra default when cost and latency are not concerns).
- 90:69 Terra guidance cites `learn.chatgpt.com/docs/model-selection`. The Terra text I verified is on the developers.openai.com guide (concise writing from supplied material, computer use with defined outcome, scoped code fixes). The cited URL was not fetched: open.
- 12:15 models page: "defaults Luna high and Astra low": MATCH ("High for Luna, Light for Astra. Astra's Light is `low`"). The 16 November date and the exact quote are not on the page (fetch tool paraphrase): unverified.
- 12:39-41: EXTENDS. Models page: "Max ... Ultra: uses subagents ... Luna supports Max but not Ultra." Desktop/web presets still list "GPT-6 Sol Light" and "GPT-6 Sol Medium" (summariser text, unverified). 90:14 says never fall back to old Sol.
- Subagents page, absent from 90 and 12: unset subagent model or effort "inherits the parent agent's model and reasoning effort". A model set without effort "uses that model's default reasoning effort". Resolution order: spawn value, then `[agents]` default, then parent. `gpt-6.1-sol` "Start here for demanding agents". `gpt-6-luna` for "fast, narrowly scoped agents". Effort: "start with `high` for GPT-6 Luna or `low` for GPT-6 Astra". `high` "for tracing complex logic or edge cases, such as reviewer or security agents". A file that sets only `model` keeps the previously resolved effort.
Lanes, official matrix (columns: lower latency/cost | balanced | higher quality):
- (a) Rename over many files with a cheap check: "Make small edits to existing files": Luna low | Luna medium | Luna high.
- (b) Comparison of sources against four files: closest "Research decisions and verify facts": Sol low | Sol medium | Sol xhigh. The row is a judgement call (nearer rows: "Organize information"; "Search documents").
- (c) Everyday feature, known patterns, explicit acceptance: "Build application features": Sol low | Sol medium | Sol xhigh.
- (d) Refactor across services, unresolved contracts: no matching row. Nearest is "Update or debug existing software" (Luna medium | Sol medium | Sol xhigh).
- (e) Judgment-dense instruction rewrite: no matching row. "Adapt existing content" (Sol low | Sol medium | Sol high) is an analogy only, and the "Other" rows are editorial fallbacks.
- (f) Unattended migration lasting hours: "Migrate an app or service": Sol medium | Sol high | Astra xhigh. The matrix does not express "unattended".
- (g) Second review of a broad change: no matching row. The subagents page says `high` for reviewer agents, which is prose, not the matrix.

## Q4 Beads v1.3.2 (raw.githubusercontent.com/steveyegge/beads/v1.3.2, plus the tag tarball in the scratchpad)
- `bd update X --claim` by B on an `in_progress` issue held by A with an expired lease FAILS (ErrAlreadyClaimed refusal). The lease is never read by the claim path.
  - internal/storage/issueops/claim.go:60-65: "claimable from "open" plus any configured custom status whose category is "active" ... WIP/done/frozen customs are excluded so the anti-steal protection ... is preserved." `in_progress` is not in the set.
  - claim.go:117 and :126: `WHERE id = ? AND row_lock = ? AND status IN (%s)` matches 0 rows. `assigneeOK` is true only for an empty assignee, the same actor or a `claim.pools` alias.
  - claim.go:138 `if rowsAffected == 0`, then :185-186 `default: refusal = fmt.Errorf("%w%s%s", storage.ErrAlreadyClaimed, storage.ClaimedByFragment, assignee)`, returned as `ClaimConflictError`. Same-actor re-claim is the only idempotent success.
  - `lease_expires_at` appears in claim.go only in comments (:177-184) and in the lease grant (:202). The lease check is in lease.go:624-691 (reclaim only).
  - cmd/bd/update.go:496-499: "the claim CAS is itself the anti-steal gate (a foreign live claim fails it ...)". update.go:993 flag text confirms.
- `bd ready` never lists such an issue.
  - internal/workapi/ready.go:44-47: "Open only, not in_progress", `Status: types.StatusOpen`.
  - cmd/bd/ready.go:25: "Excludes in_progress, blocked, deferred, and hooked issues."
  - `bd ready --claim` (ready.go:127-137): `claimer.ClaimNext`, whose `ClaimReadyIssueInTx` sets `claimFilter.Status = types.StatusOpen; claimFilter.Unassigned = true` (claim.go:255-256).
  - Caveat: sqlbuild/ready.go:113 has `status IN ('open', 'in_progress')` for a filter with no Status. `bd ready` always pins Status, so I did not follow that path.
- Other commands that move such an issue to another actor, beyond `bd reclaim`, `bd unclaim --force` and `bd update --force`:
  - YES: `bd update X --if-assignee A -a B` (and `bd assign` with the same guard) needs no `--force`. update.go:502 fences only when `ifAssignee == nil`. The code comments call it "how sanctioned X to Y transfers (park) stay possible without --force". cmd/bd/assign.go:23 names `bd update <id> --if-assignee <holder> -a <new>`. The guard compares only the assignee name, never the lease.
  - `bd assign --force` and `bd update --force` are the `--force` variants (assign.go:119). The plain fence is internal/validation/issue.go:206-220 `AssigneeNotStolen`. It never reads the lease: "pass --force only if their claim is abandoned (crashed agent, expired lease), or use bd reclaim".
  - Lease expiry changes nothing on its own. The only caller of `ReclaimExpiredLeases` in cmd/bd is reclaim.go:107 (plus the proxied unclaim path, unclaim_proxied_server.go:132). It reverts to open with the assignee cleared (lease.go:624-632), after which `--claim` succeeds.
  - Not checked: a plain `bd update X -s open` by B on a foreign `in_progress` issue. internal/storage/issueops/update.go:192-203 discusses lease handling on status changes, but I did not read it through. Open.

Decision impact: for the Phase 0 plan, a prompt-author rule set can rely on a fixed advisor surface split (Code page: write nothing). For Beads, an expired lease alone never lets another actor claim: B needs `bd reclaim` or `--if-assignee A -a B`, and the latter is a transfer path that ignores the lease.

Scratchpad copies (untrusted downloads): <session scratchpad>/{adv,oa,bd,src}

## Lead decisions from this evidence

- Heartbeat removal is confirmed: the claim path never reads the lease, a claim by another actor
  on an in-progress issue fails, and `bd ready` lists open issues only.
- A new session takes over its own earlier claim with one guarded transfer,
  `bd update <id> --if-assignee <old-actor> --if-status in_progress --assignee <new-actor>`,
  after stopped-writer recovery. This replaces the `bd reclaim` step of plan Workstream 1 item 4:
  the transfer needs no force flag, ignores the lease, and uses a command the allow-list covers.
- Advisor table: on the Claude Code surface every executor cell is "write nothing"; the API and
  SDK cells come from the platform page as reported above.
