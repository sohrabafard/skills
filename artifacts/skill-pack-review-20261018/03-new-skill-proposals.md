# Skill pack review 03: new skill proposals from chat evidence

Scope: local agent transcripts from 2026-10-08 to 2026-10-18 (today 2026-10-18), read to find repeated work, repeated errors and learning cost. Companion files: `01-contradictions-and-overlaps.md`, `02-optimization.md`.

## Sources and limits

- Claude Code: 89 transcript files in the window (14 top-level, 75 subagent) across four projects: `alaa-go-chi`, `client`, `deploy`, `skills`.
- Codex: 1,173 session files under `~/.codex/sessions/2026/10/08` to `18`. About 1,100 are subagent threads and about 80 are main threads. Logs, SQLite files and caches were not used.
- Not available: ChatGPT web chats. No local copy exists. The ChatGPT side of the evidence is absent.
- Codex inter-agent message bodies are encrypted. Orchestrator-to-subagent corrections cannot be counted. Human corrections in Codex main threads are sparse because most "user" lines are injected context.
- Some Claude sessions look like forks. Sessions `03ea0831` and `194ed3fa` share an identical first prompt, so repeat counts may be inflated.
- Counts come from regex and grep. They are approximate.

## Verification status

The chat-mining lane made coverage claims about the pack. The parent checked each claim by grep. Corrections are marked **corrected**.

| Claim from the lane | Parent check | Result |
|---|---|---|
| Sentry appears in only 5 skill files | grep finds about 20 files, including `alaa-observability-soc/references/60-sentry-and-profiling.md` and `alaa-quasar-app-vite-v3/references/36-client-observability-contract.md` | **corrected** |
| Sentry SDK setup for the browser or Quasar SPA is not covered | `observability-soc/60` covers the role split, gates and reasons, and defers package sets to services-contract. Quasar `36` covers the scrub-before-transport rule. Neither covers SDK initialisation, DSN exposure, or SSR setup | confirmed as partial gap |
| Git Bash `signal pipe` error has coverage in `alaa-codex-runtime-ops` | `SKILL.md:51` and `references/20-command-and-path-discipline.md:48` | confirmed |
| PowerShell `InitializeDefaultDrives` warning has no coverage | grep finds nothing | confirmed |
| `apply_patch` failures have no coverage | `alaa-prompting-guide/references/10-gpt-5-6.md:60` mentions `apply_patch` only as a tool type in a list. No failure guidance | confirmed, with a minor correction |
| No skill covers Stop-hook goal conditions | `alaa-prompting-guide/references/41-claude-code-runtime-features.md:133-135` covers `/goal` and the Stop-hook evaluator | **corrected** |
| No skill covers the GitLab runner Compose bootstrap | grep for `compose`, `bootstrap`, `docker run` in `alaa-gitlab-ci-cd/SKILL.md` finds nothing | confirmed |
| Commit `4d5f295aa` exists (test-economy doctrine) | `git log` shows it, dated 2026-10-18 | confirmed |
| Persian-language rule is an issue for a skill | 51 pack files mention Persian. The rule itself lives in the global `000-working-style` rule and the auto-memory entry | the lane agrees a skill is the wrong fix |

## Recommendation summary

Most of the chat evidence is already covered by an owner, or belongs to a tool or harness rather than a skill. Only one item justifies a new skill, and even that one is conditional.

| # | Topic | Type | Recommendation |
|---|---|---|---|
| N-1 | GitLab runner Compose bootstrap | LEARNING-COST | Conditional new skill. Wait for a second occurrence |
| N-2 | Browser Sentry SDK wiring for Quasar SPA and SSR | REPEATED-DERIVATION | Extend `alaa-quasar-app-vite-v3` with a reference. No new skill |
| N-3 | Codex patch failures and JS exec-wrapper syntax | REPEATED-ERROR-THEN-FIX | Extend `alaa-codex-runtime-ops`. No new skill |
| N-4 | Windows shell and process failures (Codex) | REPEATED-ERROR-THEN-FIX | Extend `alaa-codex-runtime-ops` with the `InitializeDefaultDrives` case. No new skill |
| N-5 | Premature completion against goal and Stop-hook gates | REPEATED-ERROR-THEN-FIX | No new skill. Point `alaa-workflow` at the existing `/goal` section |
| N-6 | Central-delivery gate re-runs and re-reads | REPEATED-ERROR-THEN-FIX | No new skill now. Re-check after the test-economy doctrine has a full window |
| N-7 | Subagent re-reads of global rules and skills | REPEATED-DERIVATION | No new skill. Fix the brief in the orchestrator's delegation prompts |
| N-8 | Multi-session commit scope | REPEATED-ERROR-THEN-FIX | No skill. A global rule change, outside this pack |
| N-9 | Persian-language drift | REPEATED-ERROR-THEN-FIX | No skill. A hook or pre-question checklist, outside this pack |

## N-1. GitLab runner Compose bootstrap

**Type:** LEARNING-COST. **Confidence:** medium. Evidence is one session.

- **Evidence.** Session `1f770ca3`, about 553 minutes and about $26.8 (lane estimate). Issues: token entry; three TLS verify modes, where the user had to name `insecure`, `verified` and `unverified` in turn; `RUNNER_COMPOSE_DIR` must contain no spaces; `sed` and `pwsh` errors; parity between the `.sh` and `.ps1` bootstrap scripts.
- **Coverage gap.** `alaa-gitlab-ci-cd` covers `config.toml`, executors and pipeline authoring. It has no reference to a runner Compose bootstrap. Grep finds nothing.
- **Why conditional.** One session is thin evidence. The lane itself rated confidence medium. The pattern (a shell and PowerShell parity script for a runner) could be a one-off.
- **Proposed skill.** Name: `alaa-gitlab-runner-compose-bootstrap`. Scope: a Compose-based GitLab Runner install on a Windows host and a Linux host, with both scripts kept in parity, a TLS verify mode chosen once and recorded, and a path check that rejects spaces.
- **Trigger to build it.** A second session with the same bootstrap work. Build it then, with that second session as evidence.
- **Owner boundary.** Runner `config.toml` stays with `alaa-gitlab-ci-cd`. The new skill covers only the Compose bootstrap, and points to it for config.

## N-2. Browser Sentry SDK wiring for Quasar SPA and SSR

**Type:** REPEATED-DERIVATION and LEARNING-COST. **Confidence:** medium.

- **Evidence.** Three client sessions on 2026-10-16 (`03ea0831`, `194ed3fa`, `2fc5e610`) open with the same question: is Sentry set up? The lane counts about 2,100, 950 and 155 mentions in those files. Forks may inflate the count. The Stop-hook conditions in those sessions include "dev test Sentry acceptance".
- **Coverage.** Partial, not absent (correction). `alaa-observability-soc/references/60-sentry-and-profiling.md` owns the role split and gates. `alaa-quasar-app-vite-v3/references/36-client-observability-contract.md:37` owns the scrub-before-transport rule and names `src/observability/sentryEventScrub.ts`. Neither file explains SDK initialisation, DSN exposure in a client bundle, the SSR and PWA split, or which env variables the client reads.
- **Why not a new skill.** The owner already exists for the client. The missing part is a reference section on SDK wiring. Adding a skill would split one client contract across two owners.
- **Proposed change.** Add `alaa-quasar-app-vite-v3/references/` with a Sentry browser-SDK reference: initialisation point, DSN handling as a public value, SSR and client split, and the env contract (names from services-contract, `21-alaa-platform-observability-directive.md`). Link it from `36`.
- **Owner boundary.** Event and env names stay with `alaa-services-contract`. Gates stay with `alaa-observability-soc`.

## N-3. Codex patch failures and JS exec-wrapper syntax

**Type:** REPEATED-ERROR-THEN-FIX. **Confidence:** high on counts, medium on cause.

- **Evidence.** `apply_patch verification failed` appears in 81 outputs across 46 sessions. Of these, `Failed to find expected lines` is 67 outputs across 39 sessions and `multiple operations target` is 10. A `SyntaxError` from the JS exec wrapper (for example `Unexpected identifier`) appears in 21 outputs across 14 sessions. `Failed to write file` appears in 5 sessions.
- **Wasted.** Retries of a patch on a stale context. Shell syntax written into the JS exec wrapper.
- **Coverage.** None for patch failure. `alaa-prompting-guide/references/10-gpt-5-6.md:60` names `apply_patch` only as a tool type.
- **Proposed change.** Add a section to `alaa-codex-runtime-ops`: re-read the target lines before every patch, rebuild the patch from the current file on a context mismatch, and never mix shell syntax into the JS exec wrapper. Runtime failures are that skill's family (its description says so).
- **Why not a new skill.** The trigger is the same environment-failure family that `alaa-codex-runtime-ops` already owns.

## N-4. Windows shell and process failures in Codex

**Type:** REPEATED-ERROR-THEN-FIX. **Confidence:** high on recurrence.

- **Evidence.** Git Bash `couldn't create signal pipe, Win32 error 5` in 35 outputs across 27 sessions. The PowerShell profile warning `InitializeDefaultDrives` in 87 outputs across 9 sessions, mostly on 10-11. The exec tool returned `CreateProcess ... rejected` 23 times.
- **Coverage.** The signal-pipe case is covered (`alaa-codex-runtime-ops/SKILL.md:51`). Its `references/20-command-and-path-discipline.md:48` repeats it. `InitializeDefaultDrives` has no coverage (grep). `CreateProcess … rejected` is not checked.
- **Failure despite coverage.** Eleven of the 27 signal-pipe sessions read the skill. Whether they read it before the error is not verified.
- **Proposed change.** Extend `alaa-codex-runtime-ops` with the `InitializeDefaultDrives` case and its safe response. Check the `CreateProcess` case before writing guidance.
- **Scope note.** The skill is Codex-only. Claude Code sessions do not load it, and their Bash errors differ (quoting errors, 7 times).

## N-5. Premature completion against goal and Stop-hook gates

**Type:** REPEATED-ERROR-THEN-FIX. **Confidence:** medium-low.

- **Evidence.** 12 Stop-hook feedback events in Claude sessions (client 4, deploy 8; 7 of the deploy events in `4261078e` on 10-17). Nine `/goal` invocations. Codex shows 213 injected "continue working toward the goal" messages, 81 on 10-16 alone.
- **Coverage.** Present, but in a different place than the lane reported. `alaa-prompting-guide/references/41-claude-code-runtime-features.md:133-135` states that Claude Code's `/goal` is evaluated after each turn and that Codex's `/goal` is a different mechanism. The lane missed this.
- **Why no new skill.** The pattern is an agent declaring a sub-goal done before its gate condition holds. The existing reference covers the mechanism. What is missing is a rule in the workflow owner: check the gate condition before claiming a sub-goal complete.
- **Proposed change.** Point `alaa-workflow`'s goal-loop text at the `/goal` section of `prompting-guide/41`, with the trigger "a goal or Stop-hook condition is set". Do not restate the mechanism.

## N-6. Central-delivery gate re-runs and re-reads

**Type:** REPEATED-ERROR-THEN-FIX. **Confidence:** medium.

- **Evidence.** Deploy sessions `5ec61786` (about $27.9, 338 minutes), `b69fb467` (about $60.1, 159 minutes) and `4261078e`. The user asked "why does it take so long now?" on 10-18 and said the full gate is "too long" on 10-17. The user also asked "why do you verify again and again?" on 10-18. Central files were read 16 to 18 times across sessions (`central_release_manifest.py`, `central_openfga_initializer.py`, `central-release.py`).
- **Coverage.** `alaa-testing-strategy` gained a test-economy doctrine in commit `4d5f295aa` on 2026-10-18, the same day. The failures came before it.
- **Why no new skill now.** The delivery modules are specific to the deploy repository, not to the pack. A skill for them belongs in that repository. The general test-economy rule is already in the pack.
- **Proposed check.** Re-measure the next window. If the re-runs continue after the doctrine, write the gate-selection rule into the deploy repository, not into this pack.

## N-7. Subagent re-reads of global rules and skills

**Type:** REPEATED-DERIVATION. **Confidence:** medium.

- **Evidence.** 506 of 1,175 Codex sessions read at least one `SKILL.md` through exec, averaging 5.8 skills each. `alaa-code-intelligence-routing` is read in 394 sessions, `alaa-low-noise` in 393, `alaa-memory-os` in 229, `alaa-codex-runtime-ops` in 216. Global agent-rule files are read in 508 sessions.
- **Cause.** Unknown. Whether the parent told each subagent to read these files is encrypted in the transcript.
- **Why no new skill.** The fix is the dispatch brief. The orchestrator owns brief design (`alaa-codex-orchestrator` and `alaa-cc-orchestrator`, `references/delegation-prompts.md`). The brief should carry only the facts a lane needs, not a list of rules to re-read.
- **Proposed change.** Add to the orchestrator's delegation prompts: a subagent receives a compact brief and reads a rule file only when its trigger holds. The change is in both orchestrators, per AGENTS.md ownership.

## N-8. Multi-session commit scope

**Type:** REPEATED-ERROR-THEN-FIX. **Confidence:** low-medium.

- **Evidence.** On 10-17 the user said a commit for another agent also swept in this agent's changes (sessions `4261078e` and `5ec61786`). The deploy project shows 74 cross-session agent messages. The user asked for a push twice on 10-16.
- **Coverage.** The global dirty-tree rule (`050-coding-discipline`) and `alaa-workflow` cover this in general terms. No skill states commit-scope isolation for parallel agents.
- **Why no skill.** The rule belongs in the global dirty-tree rule, outside this pack, and in the orchestrator's lane boundary, which already requires disjoint write scopes. The gap is enforcement, not missing guidance.

## N-9. Persian-language drift

**Type:** REPEATED-ERROR-THEN-FIX. **Confidence:** high on recurrence.

- **Evidence.** User corrections to answer in Persian on 2026-10-15 (`1f770ca3`), 10-16 (`03ea0831`, `194ed3fa`), 10-17 (`dfa8dcd1`) and 10-18 (`6ebf694d`). The user's correction is roughly "answer in Persian".
- **Coverage.** The global `000-working-style` rule and an auto-memory entry both cover it. The failure happened despite both.
- **Why no skill.** A skill does not fix instruction adherence. The lane's suggestion is a hook or a pre-question checklist, which is outside this pack. Note: the global rules are not part of this repository, so this proposal goes to the user's own configuration, and only if the user asks for it.

## Harness-side items (not skills)

- `mcp__ccd_turn__update_plan` returned a `scope` error about 13 times in the window, including in this review. The harness requires `scope` on every call. Report to the user; no skill change.
- Plan and checkpoint validator errors (about 6) and generated-agent drift (about 4) are thin. No skill proposal.
- CodeGraph appears in 15 `codegraph_explore` calls against 579 `Read` and 168 `Grep` calls in Claude sessions. Whether the tool was loaded at all is unverified. Low confidence; no proposal.

## Not assessed

- ChatGPT web chats. No local copy.
- Costs in dollars come from the lane's estimates and were not checked against billing.
- Fork detection. Identical first prompts were noted, not fully resolved.
- Whether the N-1 bootstrap pattern recurs. This is the reason N-1 stays conditional.
