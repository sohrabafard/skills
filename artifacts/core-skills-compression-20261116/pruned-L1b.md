# Pruned rules — lane L1b, `alaa-prompting-guide`

Second-pass ledger under `lane-brief-2.md`. Paths are relative to `skills/sohrab/alaa-prompting-guide/`. The text before the pass is at commit `b8a00eb8`. No checker clause binds text in this skill, so the checker column is empty for every row.

## Pruned rules

| # | File | Rule removed, in one line | Code | Checker clause |
|---|---|---|---|---|
| 1 | `references/12-gpt-6.md`, `21-opus-5-5.md`, `31-sonnet-5-5.md`, `36-haiku-5-5.md` | "Calibration is unrun", "no live role run or account entitlement check is claimed", "a selected task effort is an unrun workload hypothesis", "no local calibration ran". Kept once in `90-model-selection.md`, `43-fable-5-2.md` and the `SKILL.md` gate text | P6 | none |
| 2 | `references/21-opus-5-5.md`, `31-sonnet-5-5.md`, `36-haiku-5-5.md`, `41-claude-code-runtime-features.md` | Opening line "`assets/claude-model-policy.json` owns model-neutral role identity and capabilities". `90-model-selection.md` states policy ownership | P5 | none |
| 3 | `references/31-sonnet-5-5.md` | "Keep durable state through `/alaa-workflow`" | P5 | none |
| 4 | `references/31-sonnet-5-5.md` | "This skill performs no API calls" | P3 | none |
| 5 | `references/36-haiku-5-5.md`, `12-gpt-6.md` | "Vendor claims prove no local quality, latency or GPT equivalence"; "Terra execution and local calibration were unrun"; "No workload-specific superiority, cost saving or live installed-agent activation is claimed" | P6 | none |
| 6 | `references/50-effort-and-thinking.md` | "Source consistency does not prove installed activation or observed serving identity" (kept in the `SKILL.md` gate text) | P6 | none |
| 7 | `references/50-effort-and-thinking.md` | "This skill validates controls and allocates no work" and the per-section ownership restatements | P5 | none |
| 8 | `references/90-model-selection.md` | The role catalog of the orchestrator packs: the list of core lanes and gated specialists, and "Dispatch only triggered roles" | P5 | none |
| 9 | `references/90-model-selection.md` | "The lead never implements or runs heavy suites itself", "The verifier executes commands under a low-priority resource policy", "The lead is always the session's own model". The orchestrator pair owns them; `90` keeps a pointer | P5 | none |
| 10 | `references/90-model-selection.md` | "No live run is implied"; "These recommendations establish no measured local quality, cost or speed" (Terra) | P6 | none |
| 11 | `references/41-claude-code-runtime-features.md` | Plan mode: what it is, the three ways to enter it (`Shift+Tab`, a `/plan` prefix, `claude --permission-mode plan`), that shell commands outside the read-only set still prompt, and that approval switches the permission mode | P4 | none |
| 12 | `references/41-claude-code-runtime-features.md` | Ultraplan: that it drafts the plan in a web session, its three launch forms (`/ultraplan <task>`, the bare keyword, the approval dialog), and "`/ultrareview` is its review-side counterpart" | P4 | none |
| 13 | `references/41-claude-code-runtime-features.md` | Workflow tool: "Claude writes it", "the script for every run is saved under `~/.claude/projects/`", "`/deep-research` is a bundled workflow", "`/workflows` manages runs and `s` saves a script as a `/<name>` command in `.claude/workflows/` or `~/.claude/workflows/`", "a saved workflow takes input through an `args` global" | P4 | none |
| 14 | `references/41-claude-code-runtime-features.md` | Subagents: the built-in list (`Explore`, `Plan`, `general-purpose`); "subagents run in the background by default", "a background subagent surfaces its permission prompts in the main session, and its result arrives as a completion notification"; "`/subtask` starts a fork" and "`/fork` copies the whole session" | P4 | none |
| 15 | `references/41-claude-code-runtime-features.md` | "These compose: a workflow's `agent()` calls are subagents, a `/goal` can supervise a session that uses `/loop`, and an approved `/ultraplan` plan is often what a later `/goal` or `/loop` executes" | P4 | none |
| 16 | `references/41-claude-code-runtime-features.md` | Advisor prompts, API caller: the summary of what the platform's timing and weight blocks tell the executor. The rule "copy both from the page; never paraphrase them" stays | P4 | none |
| 17 | `references/11-codex-runtime-features.md` | `/goal`: "Codex then stops substantive work, summarizes progress and blockers, and names the next useful step"; "Documented fits are migrations, large refactors, experiments and long-running coding work"; the parenthetical definitions of the seven Goal elements, which the template states | P4 | none |
| 18 | `references/11-codex-runtime-features.md` | Slash commands: the meaning of `/plan`, `/review`, `/fork`, `/side` and `/btw`. The command names and the rule "name them in a generated operating prompt" stay | P4 | none |
| 19 | `references/11-codex-runtime-features.md` | Automations: the three kinds (standalone into Triage, project, thread). The two cautions stay | P4 | none |
| 20 | `references/11-codex-runtime-features.md` | "Build worked examples from `references/12-gpt-6.md` and this template" | P2 | none |
| 21 | `references/06-invocation-and-composition.md` | The plugin-build explanation of why `/name` is the one repository form (`$name` and `/name` are both rewritten to `/<plugin-namespace>:name`). `skills/sohrab/AGENTS.md` owns it; `06` keeps the rule and a pointer | P5 | none |
| 22 | `references/00-source-map.md` | "`references/00-topic-map.md` decides which reference answers a question" | P5 | none |
| 23 | `references/70-agent-instruction-files.md` | "It is neither documentation nor a skill" and the definition of an instruction file as standing context | P1 | none |
| 24 | `references/60-skill-authoring.md` | "Claude Code implements the Agent Skills open standard and Codex reads the same `SKILL.md` shape" (the rule "one package serves both runtimes" stays) | P4 | none |
| 25 | `SKILL.md` | "Deliver a usable artifact unless the user changes the role" | P1 | none |
| 26 | `references/80-subagent-authoring.md` | "A subagent is ... not a second opinion from the same agent" | P1 | none |

## Corrections from `freshness.md`

| # | File | Before | After | Source |
|---|---|---|---|---|
| A | `references/11-codex-runtime-features.md`, `references/70-agent-instruction-files.md` | `11`: a deep chain "can silently drop the outermost files"; "configurable up to 65536 bytes". `70`: "silently truncates the tail" | The fact is stated once, in `70` *Nesting and precedence*: Codex adds files from the root down and "stops adding files once the combined size reaches the limit", so the files nearest the working directory are left out; 65536 is the page's example value, not a stated maximum; the page does not say whether a crossing file is cut or skipped. `11` points to `70`. The stale `developers.openai.com/codex/guides/agents-md` URL is replaced by its destination | https://learn.chatgpt.com/docs/agent-configuration/agents-md , 16 November 2026 |
| B | `references/41-claude-code-runtime-features.md`, `references/80-subagent-authoring.md` | `41` carried a second, incomplete frontmatter list (no `autoCompactWindow`, `omitClaudeMd`, `experimental`) | One list, in `80`; `41` points to it | https://code.claude.com/docs/en/sub-agents , 16 November 2026 |
| C | `references/12-gpt-6.md` | Official Codex guidance "recommends GPT-6.1 Sol for complex coding and demanding agents" | The models page describes Astra as "for the most demanding work across code, apps, and research" and GPT-6.1 Sol as "near-Astra performance at lower cost, suited to repeated, long-running work". The Luna and Sol selector cells keep their dates of 8 and 9 October 2026 | https://learn.chatgpt.com/docs/models , 16 November 2026 |
| D | `references/60-skill-authoring.md` | "Write all three parts" above a list of four | "Write all four parts" | internal |
| E | `references/90-model-selection.md` | "Claude rows and defaults refreshed 14 November 2026" | "Claude rows refreshed 14 November 2026. Each current model reference holds that model's defaults per surface" | internal |

## Additions with a reason

| File | Addition | Source |
|---|---|---|
| `references/60-skill-authoring.md` | Two carry-over rows, "Default-behaviour instruction" and "Step-by-step itinerary", and the rule "record each removal: the rule removed and the reason" | https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra , 16 November 2026 |
| `references/12-gpt-6.md` | One line that states the blog guidance, so that the carry-over gate ("apply a check only when the target model's reference documents the behavior") can apply the two rows | same |
| `references/61-skill-platform-mechanics.md` | Section *Official structure guidance*: six one-line facts | https://code.claude.com/docs/en/skills and https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices , 16 November 2026 |

## Removed as a duplicate of a rule that stays in this skill (no code)

Listed so that the owner can restore a second statement. Each rule still exists at the named place.

| Removed from | What | Stays in |
|---|---|---|
| `06` *Pre-send checklist* (8 items) | Every item restated a rule of the same file | `06` sections *Writing a call site*, *Role consistency*, *Kickoff and completion condition*, *Delegation polarity* |
| `06` *The failure shape to recognize* | The bad and fixed example | One sentence in `06` *Role consistency* |
| `60` *Checklist* (10 items) | Every item restated a rule | `60` sections; `SKILL.md` *Principles for every artifact* |
| `60` *Defects and fixes* | 7 of 14 rows restated the prose | The 7 rows that carry a rule or a symptom the prose lacks stay |
| `60` *Lean prompts must preserve behavior* | The vendor guidance and the keep-list restatement | `12` *Prompt design*; `60` never-remove list |
| `70` *Defects and fixes*, *Checklist* | 7 of 9 rows and all 10 items | `70` prose; 2 rows stay as *Symptoms of a chain defect* |
| `80` *Defects and fixes*, *Checklist* | All 12 rows and 9 of 10 items | `80` prose, except "Untested escalation", which stays in `50` *Raising effort*, and "Wrong delegation polarity", which stays in `06` *Delegation polarity*; checklist item 5 (the description states when to delegate) moved into *The four things every definition pins* |
| `80` *When a subagent is the right tool* | Pointer section | One line under the title |
| `50` *Anti-patterns* | 8 of 11 items restated the prose | `50` prose; 3 items stay under *Raising effort* |
| `50` *Capability registries and realized controls* | Restated procedure steps | `50` procedure steps 3 to 5 |
| `31` | The bounded-implementation example contract | `31` *Prompting* rules for `low` and `high` |
| `21` | "Give the desired outcome, complete task context, scope, authority, acceptance criteria and stop conditions" | `SKILL.md` *Complete contract* |
| `21` | "Release summaries are weaker evidence and do not justify relaxing authority or safety gates" | `00-source-map.md` *Interpretation contract* |
| `36` | "Historical Haiku 4.5 has no effort parameter" | `50` *Thinking* |
| `41` | Agent definition directories and the frontmatter list | `80` *Definition files* |
| `80` | Nesting default and the inherited `Agent` tool | `41` *Agent tool and subagents* |
| `11` | `CODEX_HOME`, `project_doc_fallback_filenames`, the byte limit, and "Codex does not update these files on its own" | `70` |
| `12` | "Give explicit delegation scope when delegation is authorized" | `06` *Delegation polarity*, Codex row |
