# Model Selection and Companion Routing

## Capability evidence and allocation ownership

- **Capability.** `assets/codex-model-policy.json` and `assets/claude-model-policy.json` own capability snapshots, ordinary eligibility, and the registrations of neutral roles and artifacts. The Codex policy also owns the supported-effort snapshots; the Claude policy owns Claude capabilities and model availability conditions. They define no role default and choose no task pair. A supported effort is separate from `selection_enabled`: a retained effort history never enables a disabled model.
- **Allocation.** The runtime orchestrator owns task allocation, priority, admission and deliberate source departures for every managed role, including research, review, verification, documentation and rule-writer. Read `/alaa-codex-orchestrator` or `/alaa-cc-orchestrator` `references/routing-matrix.md`. `/alaa-workflow` records the allocation when durable state is admitted.
- **Standalone delegation.** The parent uses that allocation procedure and records a compact dispatch. It need not start the full pipeline or create a plan only for selection.
- **Normalization.** Before an explicit dispatch, `alaa-codex-orchestrator references/model-effort-policy.md` or its `alaa-cc-orchestrator` mirror normalizes omitted fields; its resolved defaults count as task selection.
- **Realization and checks.** To realize an explicit model AND effort, use `references/11-codex-runtime-features.md` or `references/41-claude-code-runtime-features.md`. For capability and uncertainty checks, use `references/50-effort-and-thinking.md`.
- **What selects no task pair:** a registered role name, a retained compatibility ID that names a model or an effort, an inherited control, a vendor ranking, model availability, a file count, a planning effort. A role name selects authority only.
- Main-session controls stay externally configured; an allocation does not change them.
- The tables below are evidence inputs, not executable defaults. No source claim proves host availability, quality or local superiority.

**Codex.** Ordinary selection excludes GPT-6 Sol and keeps its effort snapshot as history. GPT-6.1 Sol is the current Sol candidate. Use the newest member of the selected family that is verified, supported and eligible; a suitable Luna stays eligible. If current Sol is unavailable, require an exact eligible realization or block the affected lane. Never fall back to old Sol.

**Legacy request.** Record an explicit user request for a legacy model separately. It neither restores ordinary eligibility nor passes ordinary task-control validation.

**Claude.** The active set is Haiku 5.5, Sonnet 5.5, Opus 5.5 and Fable 5.2 (since 14 November 2026). Mythos is excluded from active selection and custom profiles. A historical model supplies reference evidence only. Verify availability and the loaded registry separately.

## Official task guidance

OpenAI matrix refreshed 9 October 2026; Claude rows refreshed 14 November 2026. Each current model reference holds that model's defaults per surface. The complete served selector asset was read as text, without execution or browser interaction; the supplied screenshots match its cells. L = GPT-6 Luna, S = GPT-6.1 Sol, A = GPT-6 Astra.

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

Limits of the matrix:

- It is a dated editorial starting point. Some rationale metadata keeps an older Sol generation; use the served recommendations, not that label.
- Well-scoped bug: the medium and high cells are editorial checking choices with no demonstrated gain over low.
- Search: the medium and high cells lack direct benchmark proof; only xhigh was tested.
- The animation choices and the rows marked editorial fallback are editorial.
- No general reliability rate or saving follows.

The guide's prose adds:

- Luna low for precise or bounded work; Luna xhigh for cross-app prioritization.
- Sol medium for complex revisable technical work; Sol xhigh for polished, connected or conflicting-evidence work.
- Astra low for concise nuanced writing; Astra medium for broad ambitious projects; Astra xhigh for demanding analysis.
- With no effort assigned: compare Sol on cost-conscious complex work, and optionally default to Astra when cost and latency are unconstrained.

The [Codex Terra guidance](https://learn.chatgpt.com/docs/model-selection#when-to-consider-gpt-61-terra) (3 November 2026) names concise writing from supplied material, computer use with a defined outcome, and scoped code fixes with explicit inputs, requirements and a check. Read `references/12-gpt-6.md` for Terra controls.

| Claude workload/path | Source recommendation | Effort evidence |
|---|---|---|
| Everyday coding, analysis, content, vision, agent tools | Sonnet | Unspecified in selection guide |
| Complex autonomous coding, broad refactors, systems, computer use | Opus | Unspecified in model matrix |
| Highest capability, agent sessions that run for hours, multistep deep research, finished documents | Fable 5.2 | Unspecified in model matrix |
| Real-time, bulk, cost-sensitive processing/subagents | Haiku | Unspecified in model matrix |
| Efficiency-first prototypes, latency or straightforward bulk | Start Haiku; move up for a demonstrated capability gap | No task-specific effort |
| Capability-first complex reasoning, accuracy or advanced autonomous coding | Start Opus; optimize downward after adequate quality | Opus medium starting effort |
| Demanding reasoning or long-horizon work that falls short on Opus at `xhigh` or `max` | Move to Fable 5.2 (selection guide, 14 November 2026) | No selected Fable effort; `references/43-fable-5-2.md` holds the vendor starting point |
| Bulk execution with difficult decisions | Cheaper executor plus frontier advisor, or a frontier orchestrator that delegates bulk work to lower-cost workers. For native Code candidates and preflight, read `references/41-claude-code-runtime-features.md`. | No default pair or effort |

- The guide recommends Opus as the starting point for most workloads. Keep both the capability-first path and the efficiency-first path.
- The Sonnet prompting page, not the selection guide, gives `medium` for well-specified agentic coding and `high` for harder or longer work. Its examples of regressions at higher effort rule out automatic maximization.
- A local Fable admission belongs to the runtime orchestrator and stays distinct from the vendor's `xhigh` and `max` advice.

Sources (refresh the current page and asset before reuse):

- [OpenAI model selection](https://developers.openai.com/api/docs/guides/model-selection) and its [served selector asset](https://developers.openai.com/_astro/ModelSelection.react.DJkmSLnH.js)
- [Claude model selection](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model)
- [Sonnet prompting](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5)

## Companion routing

- `/alaa-codex-orchestrator` (Codex) and `/alaa-cc-orchestrator` (Claude Code): production multi-agent orchestration. Prefer them over a hand-written fan-out. Each owns its role catalog, role triggers, task selection, parallel scheduling and gates; this file sets no spawn-count default.
- Role identity and neutral controls are checked against the policy JSON of each runtime. Executable frontmatter preserves authority and selects no task pair. The standard and deep reviewer scopes share one reviewer profile; scope breadth alone creates no second executable identity.
- `/alaa-workflow`: durable multi-phase plans, phase prompts and resumable state.
- `/openai-docs`: the freshest GPT-6 and Codex guidance when this skill is stale. Use the official Anthropic documentation for Claude gaps.
- `/alaa-low-noise`: broad prompt research, validation, or a long tool-heavy session.

## Caveats

Benchmark claims, relative pricing, effort defaults and the capability order among current models are vendor-stated and time-sensitive. Before you treat a ranking here as current, re-check `references/00-source-map.md` and the live model pages.
