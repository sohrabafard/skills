# Ledger — lane LC

Lane LC of `plan.md`: Workstream 3 items 1 to 3 and Workstream 4 item 3, with the `sources.md`
corrections to `41`, `50`, `90` and `12`. Paths are relative to `skills/sohrab/`. No clause checker
binds these files, so no checker clause was reworded or deleted.

| File | Old rule | New rule | Plan item | Checker clause |
|---|---|---|---|---|
| alaa-prompting-guide/SKILL.md | new | Decision procedure step 6: for a Claude target, apply `41` *Prompts for a session that may have an advisor* before you ship a prompt, system prompt or dispatch | W3.1 | none |
| alaa-prompting-guide/references/41 | Rules 1, 2, 4 and the decision-in-visible-text sentence, spread over a nine-rule list | The four things every Claude prompt does: goal, constraints, acceptance; visible decision; save before the completion consultation; never depend on the advisor | W3.2 | none |
| alaa-prompting-guide/references/41 | Rule 6 "Fit the executor model" and the two surface paragraphs | One table, surface by executor model: Claude Code cells "write nothing by default"; API cells per `sources.md` Q1 (Haiku 5.5 hard-rule block and optional nudge, page-text unverified; Sonnet timing then weight, no nudge; Opus timing and weight, no nudge, checkpoint only on observed under-calling; Fable no guidance, page-text unverified), 17 November 2026; Sonnet and Opus API cells scoped to coding executors | W3.2 | none |
| alaa-prompting-guide/references/41 | Rule 6: hard-rule block's stated evidence is Haiku 4.5 | Block labelled Haiku 5.5 (page-text unverified); only the nudge cites Haiku 4.5 | W3.2, Q1 41:78 | none |
| alaa-prompting-guide/references/41 | new | Opus API cell: optional checkpoint only when under-calling is observed | W3.2, Q1 41:78 | none |
| alaa-prompting-guide/references/41 | Rule 3: consultation points only on a long multi-step task | Kept, moved to the *Claude Code surface* bullet under the table | W3.2 | none |
| alaa-prompting-guide/references/41 | "A dispatch to a subagent ... Apply rules 1 to 9" | A dispatch uses the Claude Code column | W3.2 | none |
| alaa-prompting-guide/references/41 | Rules 5, 7, 8, 9; harness-text paragraph; block placement | Kept unchanged as "Rules the table does not carry" and bullets | W3.2 | none |
| alaa-prompting-guide/references/41 | Start: `/advisor` and `--advisor` only | Adds v2.1.260 `-p`, Agent SDK and desktop; `/advisor off`; invalid pair exits at launch, background session starts without advisor (17 November 2026) | W3.3, Q1 41:44 | none |
| alaa-prompting-guide/references/41 | Preflight: Anthropic API or Claude Platform on AWS (14 November 2026) | Adds Claude Models on Google Cloud (Anthropic managed), v2.1.300+ on the cloud providers, not on Bedrock, Agent Platform or Foundry, feature-flag fetch broken by `DISABLE_TELEMETRY` (17 November 2026) | W3.3, Q1 41:46 | none |
| alaa-prompting-guide/references/41 | new | Haiku 5.5 main model needs v2.1.293+; advisor at least as capable as executor (17 November 2026) | W3.3, Q1 41:52-55 | none |
| alaa-prompting-guide/references/41 | Unaccepted pair: no consultation, no error | Adds `/advisor` output and a notification show it; a subagent whose model satisfies the pairing can still use the advisor (17 November 2026) | W3.3, Q1 41:57 | none |
| alaa-prompting-guide/references/41 | new | `max_tokens`: minimum 1024, recommended start 2048; Managed Agents advisor takes none (17 November 2026) | W3.3, Q1 41:81 | none |
| alaa-prompting-guide/references/06 | new | *Kickoff and completion condition*: for a goal that will run long on a Claude model, apply the `41` advisor section to the kickoff | W3.3 (plan) / dispatch item 4 | none |
| alaa-prompting-guide/references/50 | new | *Lowering effort*: lower for short, fully specified or high-volume tasks; low level in a long agent prompt risks skipped search, early stop, skipped check; step down only where evals hold quality; effort often a better lever than a model switch (17 November 2026, each linked) | W2 (lowering rule), Q2 | none |
| alaa-prompting-guide/references/90 | Claude effort evidence "Unspecified" (four workload rows) | Messages API defaults per model; Sonnet effort-page guidance (17 November 2026) | Q2 90:73-76, 90:83 | none |
| alaa-prompting-guide/references/90 | Haiku efficiency row "No task-specific effort" | Effort-page Haiku guidance (17 November 2026) | Q2 90:77 | none |
| alaa-prompting-guide/references/90 | Fable row "No selected Fable effort" | Effort-page Fable guidance (17 November 2026) | Q2 90:79 | none |
| alaa-prompting-guide/references/90 | Sonnet prompting page, not the selection guide, gives medium/high | API defaults are Messages API defaults; the three platform pages checked state no Claude Code default and model-config was not re-read, so each model reference keeps its Code default; Sonnet regression examples still rule out maximization | Q2 90:83 | none |
| alaa-prompting-guide/references/90 | Two computer-use rows, balanced S medium | Balanced T medium (17 November 2026); legend adds T = GPT-6.1 Terra | Q3 90:49-50 | none |
| alaa-prompting-guide/references/90 | Adapt existing content balanced S medium | Matrix cell unchanged; a note under the legend records the asset's alternative T medium, Sol primary, with no column assigned (17 November 2026) | Q3 90:28 | none |
| alaa-prompting-guide/references/90 | Asset URL `DJkmSLnH` | `BKCv-TnC` (17 November 2026); old asset returns 404 | Q3 90:88 | none |
| alaa-prompting-guide/references/12 | new | Subagent inheritance: unset model or effort inherits the parent's; model without effort uses its default; order spawn, `[agents]`, parent (17 November 2026) | Q3 subagents | none |
| alaa-prompting-guide/references/00-source-map | new | 17 November 2026 row in *Latest verification dates* | dates of the corrections | none |
| alaa-low-noise/SKILL.md | Four rules spread over Part 1 and Part 2 | Moved to a new *First rules* section at the top; wording kept, bound-output rule stated as rule 1 | W4.3 | none |
| alaa-low-noise/SKILL.md | new | Default command-output budget: about 40 lines per command that enters the context; larger output to a file; required evidence stays | W4.3 | none |
| alaa-low-noise/SKILL.md | new | A dispatched lane carries its own output rule in its definition; the lead names this skill only for a discovery-heavy or log-heavy lane | W4.2/W4.3 | none |
| alaa-low-noise/references/workflow-integration.md | `## Delegated lanes` | Unchanged | W4.3 | none |

Kept, not changed: `90:69` Terra guidance URL (open), `12:15` models-page defaults and date
(unverified), every matching matrix row, and the progress budget.

Notes: `41` keeps its 14 November 2026 verification stamp for the unchanged rules. In `50`, the
skipped-check risk at a low level is stated generally, as the dispatch words it; `sources.md` ties
it to Haiku 5.5 at `low`.
| alaa-prompting-guide/assets/codex-model-policy.json | Selector source `ModelSelection.react.DJkmSLnH.js`, verified 2026-10-09 | `ModelSelection.react.BKCv-TnC.js`, verified 2026-11-17; the scope says the asset name changes with each site build (the owner added this repair to the scope on 2026-11-17, commit c3f8438d) | Q3 90:88 | none |
