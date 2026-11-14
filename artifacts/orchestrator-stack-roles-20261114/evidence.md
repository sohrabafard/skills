# Session evidence for the orchestrator role review (2026-11-14)

Two read-only subagents mined the session transcripts of the seven days before 2026-11-14, one per runtime. Each inspected the record schema, wrote an extractor, and read only its aggregate output. This file carries counts, role names, skill names and failure classes in the miners' own words. It carries no prompt body, tool output or transcript text. The extractors and aggregates stayed in the session scratchpad and are not archived.

Every rate below has its denominator. A missing measurement is recorded as unknown.

## Scope of the two samples

| | Claude Code | Codex |
|---|---|---|
| Session files in the window | 79, plus 893 lane transcripts | 262 rollouts: 46 root sessions, 111 child lanes, 105 auto-review threads excluded |
| Sessions that activated the orchestrator skill | 7 | 10 |
| Dispatches | 909 (709 Agent-tool, 5 nested, 195 Workflow-tool lanes) | 152 |
| Implementation dispatches | 265, of which 209 in orchestrator sessions | 28, of which 22 have a transcript |

The Claude Code sample excludes the pack-maintenance session from every behaviour metric. The Codex format stores dispatch prompts as opaque blobs, so no Codex metric that needs the prompt text was measured. All 32 lanes of the Codex infrastructure project have no child transcript.

Both samples ran on the installed agent definitions of pack version 5.5.0, before the uniform return header of 5.6.0.

## Stack of implementation lanes

Claude Code, orchestrator sessions, family taken from the dispatch prompt (n=209 with fallbacks): PHP and Laravel 103, Vue, Quasar and TypeScript 55, infrastructure 18, instructions and documents 13, Go 4, others in the remainder.

Codex, by project manifest (n=28): PHP and Laravel 11, Vue, Quasar and TypeScript 10, infrastructure 7, Go 0.

## Did a lane load the skill that owns its stack

| Stack | Claude Code: loaded a stack-matched skill | Claude Code: zero explicit skill loads | Codex: loaded a stack-owner skill |
|---|---|---|---|
| PHP and Laravel | 60 of 103 | 22 of 103 | 5 of 11 |
| Vue, Quasar and TypeScript | 10 of 55 | 37 of 55 | 3 of 10 |
| Infrastructure | 4 of 18 | 10 of 18 | unknown (6 of 7 lanes have no transcript) |
| Go | 1 of 4 | 2 of 4 | no dispatch |

Claude Code implementer definitions preloaded three general skills and no stack skill, so an explicit load was the only way a lane reached its stack doctrine.

How the dispatch named the skill decided the outcome. In Claude Code, PHP lanes had a stack skill named as a call in 47 of 103 dispatches and loaded one in 60. Vue lanes had one named as a call in 1 of 55 dispatches (53 of 55 as a bare mention) and loaded one in 10.

Lanes with at least one dispatch-named skill that was never loaded: 173 of 275 in Claude Code orchestrator sessions, 110 of 180 among implementation lanes. Most often missed: the low-noise, testing-strategy, ponytail, Vue TypeScript clean-code, security-review, PHP clean-code and frontend-developer skills.

In Codex every implementation lane loaded the process skills (workflow, testing strategy, the orchestrator itself) and 80 of 119 lanes read orchestrator files.

## Start-up and lane cost

- Tool calls before the first edit, implementation lanes: Claude Code median 32, p90 60 (n=86, first Edit or Write); Codex median 26, p90 32 (n=19).
- Claude Code median input tokens per lane (cumulative, including cache reads): `alaa-implementer` 3.95M (n=113), `alaa-implementer-sonnet-high` 4.43M (n=55), `alaa-implementer-opus` 13.7M (n=22).
- Codex: the verifier is the costliest gate role (median 114 tool calls, n=9).

## Hand-backs and repair

- Claude Code: 130 of 209 implementation finals were free text with no status token. Codex: 0 of 139 implementer hand-backs opened with a `VERDICT:` or `STATUS:` line. Pack version 5.6.0 requires that first line; the sample predates it.
- Claude Code: 16 non-pass review hand-backs in orchestrator sessions, 13 followed by a new implementation dispatch. 41 of 195 Workflow-tool lanes were repair-like phases.
- Codex: 122 follow-ups to implementer roles against 28 implementation spawns; the most frequent verdict token was `CHANGES-REQUESTED` (29).

## Failure classes in non-pass results (60 excerpts per runtime, classified by the miner)

- Contract artifacts out of step with code (OpenAPI, Postman, error codes, documents): Claude Code 5, Codex 7.
- Environment, tool, registry or dependency blocks rather than code defects: Codex 14; Claude Code 6 (4 token-selected, 2 keyword-selected).
- Failures that existed before the lane started: Claude Code 6.
- A fix that needed a file or test outside the lane's scope: Claude Code 5.
- Correctness defects found by review: Codex 9, Claude Code 4.

## Controls

- Claude Code Agent-tool dispatches (n=714): model omitted in 508, effort omitted in 591. When the model was omitted, the lane ran on the session's model: Opus 45 times and Fable 4 times among implementer lanes. When a model was given, the lane matched it in 145 of 145 cases.
- Workflow-tool lanes never carried a requested effort (195 of 195).
- Codex: the effective model and effort matched the request in all 146 dispatches that set a model. Only 3 of the 10 implementer identities were dispatched.

## Other observations

- Claude Code: 145 of 209 implementation lanes in orchestrator sessions ran `git commit` (detected from the command text), although the implementer contract says a lane never commits.
- Codex: "agent thread limit reached" stopped 11 follow-ups and 1 spawn; 3 lanes ended on a usage limit.
- Routing inside orchestrated Claude Code runs was already role-based: 7 of 221 Agent-tool dispatches used a generic agent.

## Limits

- Work class and stack family in Claude Code come from keyword and extension classifiers; the work classifier agreed with the role's own work in 283 of 522 managed-role dispatches.
- Skill loads are explicit loads only (a skill call, or a read of a skill file). A preload leaves no record.
- "Followed by" in the repair counts is order in the transcript, not proven cause.
- One week of one owner's sessions is a small sample. The Go and infrastructure rows rest on few lanes.
