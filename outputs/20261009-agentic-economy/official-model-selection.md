# Official model-selection recommendations

Retrieved 2026-10-09 by the research subagent. Labels are paraphrased. This is a dated source snapshot, not the pack's model policy or local calibration.

## OpenAI: complete served selector matrix

Source: [selection guide](https://developers.openai.com/api/docs/guides/model-selection) and its directly referenced [selector asset](https://developers.openai.com/_astro/ModelSelection.react.DJkmSLnH.js?dpl=dpl_7iHSYrJ5jPyHvJgcWEVxZrsjhkmE). Standard TLS retrieval succeeded outside the sandbox after sandbox Schannel failures. JavaScript was read as text, never executed. Browser interaction was not run.

The asset contains 27 tasks and exactly three positions (81 cells). Its default is deliverables, small edits, balanced; the component selects recommendations by priority. L = GPT-6 Luna; S = GPT-6.1 Sol; A = GPT-6 Astra. Each cell is model plus effort.

| Category | Task | Lower latency/cost | Balanced | Higher quality |
|---|---|---|---|---|
| Deliverables | Small existing-file edits | L low | L medium | L high |
| Deliverables | Slides or spreadsheets | L medium | S medium | A xhigh |
| Deliverables | Adapt existing content | S low | S medium | S high |
| Deliverables | Coordinated files from input data | S medium | S high | S xhigh |
| Deliverables | Source material to finished output | S medium | S medium | A xhigh |
| Deliverables | Complex polished deliverable | S medium | A high | A xhigh |
| Deliverables | Other (editorial fallback) | S low | S medium | A xhigh |
| Software engineering | Well-scoped bug | L low | L medium | L high |
| Software engineering | Update/debug existing software | L medium | S medium | S xhigh |
| Software engineering | Application features | S low | S medium | S xhigh |
| Software engineering | App/service migration | S medium | S high | A xhigh |
| Software engineering | Polished application | S medium | A medium | A xhigh |
| Software engineering | Other (editorial fallback) | S medium | S medium | A xhigh |
| 3D/design | Page/interface design (editorial fallback) | S medium | S medium | S high |
| 3D/design | Editable 3D models | S low | S medium | S high |
| 3D/design | 3D animation | S medium | S high | S xhigh |
| 3D/design | Interactive 3D experience | S medium | S high | A xhigh |
| 3D/design | Other (editorial fallback) | S medium | S high | A xhigh |
| Research/analysis | Organize information/priorities | L low | L medium | S high |
| Research/analysis | Search documents/messages/email | L medium | L high | L xhigh |
| Research/analysis | Research decisions/fact verification | S low | S medium | S xhigh |
| Research/analysis | Data analysis/problem solving | L medium | S high | A xhigh |
| Research/analysis | Other (editorial fallback) | S medium | S medium | S xhigh |
| Computer use | Find app information/controls | S low | S medium | S high |
| Computer use | Complete app workflow | S low | S medium | S high |
| Computer use | App/website testing | S medium | S high | S xhigh |
| Computer use | Other (editorial fallback) | S low | S medium | S xhigh |

These are editorial starting points, not guarantees. Rows marked editorial fallback differ from the remaining user-directed basis. Dataset benchmark metadata is dated 2026-09-17 and covers 48 of 56 tasks; current recommendations substitute GPT-6.1 Sol while some historical rationales retain earlier Sol. Scoped-bug medium/high are editorial checking options, not demonstrated gains over low. Search medium/high lack direct benchmark proof; only xhigh was tested. Animation effort choices are editorial. Do not infer a general reliability rate or local superiority.

## Anthropic

Source: [Choosing the right model](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model). The guide presents both efficiency-first and capability-first selection; its most-workloads Opus starting advice coexists with Sonnet everyday-work guidance.

| Workload | Selection path | Model | Effort in this guide |
|---|---|---|---|
| Highest capability, long sessions, deep research, finished documents | Model matrix | Fable 5.1 | Unspecified |
| Complex autonomous code, broad refactors, systems, computer use | Model matrix | Opus 5.5 | Unspecified |
| Everyday code, analysis, content, vision, agent tools | Model matrix | Sonnet 5.5 | Unspecified |
| Real-time, bulk, cost-sensitive processing and subagents | Model matrix | Haiku 5.5 | Unspecified |
| Prototypes, latency-sensitive or straightforward bulk work | Efficiency-first | Haiku 5.5 | Unspecified |
| Specific tested capability gap | Efficiency-first escalation | Stronger model, unspecified | Unspecified |
| Complex reasoning, accuracy-critical or advanced autonomous code | Capability-first | Opus 5.5 | Starting effort below |
| Adequate capability; optimize efficiency | Capability-first optimization | Lower effort/model | Unspecified |
| Demanding long-horizon work inadequate at Opus xhigh/max | Capability-first escalation | Fable 5.1 | Unspecified |
| Bulk execution with difficult decisions | Mixed strategy | Cheaper workers plus frontier advisor | Unspecified |

The selection guide's starting efforts are Opus 5.5 medium, Haiku 5.5 medium and Fable 5.1 high; Sonnet is unspecified there. Later launch/effort inspection qualifies surface defaults: Sonnet Code/apps medium versus API high, and Fable Code/API high versus Cowork/claude.ai medium. Historical rows (Opus 5 high and Opus 4.8/4.7 extra high) do not select current profiles. Sonnet's separate [prompting guide](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5) recommends medium for well-specified agentic coding and high for harder/longer work. See [source evidence](source-evidence.md) for all four user-requested launch pages and caveats.

## Interpretation for this change

The recovered selector explicitly supports Sol-low feature work; this supersedes the initial incomplete extraction. The three supplied screenshots agree with recovered cells. Stronger direct vendor routes also exist (for example polished applications and quality-prioritized migration). The final pack admits source-matched Codex exceptional routes with actual-lane, priority and cheaper-route insufficiency reasons; it requires no synthetic failed trial. Other exceptional routes retain inadequacy/explicit-selection admission. Claude Fable retains the conservative local admission and never inherits the OpenAI slider rule.

API support, official starting recommendations, local admission and measured local performance are separate evidence classes. All new local routes remain uncalibrated. No table row proves runtime availability, serving identity or savings.
