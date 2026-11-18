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

**Codex.** The active set is GPT-6.2 Astra, GPT-6.2 Sol, GPT-6.1 Terra and GPT-6 Luna (since 18 November 2026). Ordinary selection excludes GPT-6 Sol, GPT-6.1 Sol and GPT-6 Astra and keeps their effort snapshots as history. Use the newest member of the selected family that is verified, supported and eligible; a suitable Luna or Terra pair stays eligible. If the current Sol or Astra is unavailable, require an exact eligible realization or block the affected lane. Never fall back to a historical model.

**Legacy request.** Record an explicit user request for a legacy model separately. It neither restores ordinary eligibility nor passes ordinary task-control validation.

**Claude.** The active set is Haiku 5.5, Sonnet 5.5, Opus 5.5 and Fable 5.2 (since 14 November 2026). Mythos is excluded from active selection and custom profiles. A historical model supplies reference evidence only. Verify availability and the loaded registry separately.

## Official task guidance

OpenAI matrix refreshed 18 November 2026; Claude rows refreshed 14 November 2026. Each current model reference holds that model's defaults per surface. The complete served selector asset was read as text, without execution or browser interaction. L = GPT-6 Luna, T = GPT-6.1 Terra, S = GPT-6.2 Sol, A = GPT-6.2 Astra. The asset also lists T medium as an alternative for "Adapt existing content", with Sol kept as primary.

| Category | Task | More usage | Balanced | Higher quality |
|---|---|---|---|---|
| Deliverables | Make small edits to existing files | L low | L medium | L high |
| Deliverables | Create slides or spreadsheets | L high | S high | A high |
| Deliverables | Adapt existing content | T medium | S medium | S high |
| Deliverables | Create a coordinated set of files from input data | T high | S high | A high |
| Deliverables | Turn source material into a final output | S medium | S high | A high |
| Deliverables | Create a high-quality, complex deliverable | S high | A high | A xhigh |
| Deliverables | Other (editorial fallback) | T medium | S medium | A medium |
| Software engineering | Fix a well-scoped bug | L low | T low | S low |
| Software engineering | Update or debug existing software | T medium | S medium | S xhigh |
| Software engineering | Build application features | S low | S medium | S xhigh |
| Software engineering | Migrate an app or service | S medium | S high | A xhigh |
| Software engineering | Build polished applications | S medium | A medium | A xhigh |
| Software engineering | Other (editorial fallback) | S medium | S medium | A xhigh |
| 3D/design | Design a page or interface (editorial fallback) | S medium | S high | A medium |
| 3D/design | Create editable 3D models | S high | A medium | A xhigh |
| 3D/design | Animate a 3D model | S high | S xhigh | A xhigh |
| 3D/design | Build interactive 3D experiences | S medium | S high | A xhigh |
| 3D/design | Other (editorial fallback) | S medium | S high | A xhigh |
| Research/analysis | Organize information and prioritize work | L medium | T medium | T high |
| Research/analysis | Search documents, messages, and emails | L medium | L high | L xhigh |
| Research/analysis | Research decisions and verify facts | S medium | S high | S xhigh |
| Research/analysis | Analyze data and solve problems | L high | T high | S xhigh |
| Research/analysis | Other (editorial fallback) | T medium | S medium | S xhigh |
| Computer use | Find visible controls in an app | T low | T medium | S high |
| Computer use | Update specified records in an app | T low | T medium | S high |
| Computer use | Test an app or website | T medium | T high | S high |
| Computer use | Other (editorial fallback) | T low | T medium | S high |

Limits of the matrix:

- It is a dated editorial starting point. The asset says that its 13 November editorial review set all three positions for each task, that the task scores in each rationale keep their original model identities, and that the shared-task results cover GPT-6 Luna, GPT-6.1 Terra, GPT-6.1 Sol and GPT-6 Astra. No cell is a measured GPT-6.2 result.
- Fix a well-scoped bug: all three cells are `low`, and the priority changes the model. The rationale still supports Luna for simple fixes and names Sol for a change that needs more repository context.
- Research decisions and verify facts: the rationale says that higher effort is not required for every fact check.
- Search: only xhigh was tested; the medium and high cells are editorial.
- The animation choices and the rows marked editorial fallback are editorial.
- No general reliability rate or saving follows.

`references/12-gpt-6.md` holds the eight model and effort pairs of the guide's prose.

The [Codex models page](https://learn.chatgpt.com/docs/models) (18 November 2026) names Terra for "everyday writing and visual work": clear communication, images and screens, and tasks across supported apps. Read `references/12-gpt-6.md` for the Terra pair of the guide and for Terra controls.

| Claude workload/path | Source recommendation | Effort evidence |
|---|---|---|
| Everyday coding, analysis, content, vision, agent tools | Sonnet | API default `high` (17 November 2026). Effort page: `medium` for well-specified agentic coding and multistep tool use, `high` for harder or longer work, `medium` or `low` for chat; `xhigh` or `max` only where evals show a gain |
| Complex autonomous coding, broad refactors, systems, computer use | Opus | API default `medium`; an omitted effort runs one level lower than on Opus 5 (17 November 2026) |
| Highest capability, agent sessions that run for hours, multistep deep research, finished documents | Fable 5.2 | API default `high` (17 November 2026) |
| Real-time, bulk, cost-sensitive processing/subagents | Haiku | API default `medium` (17 November 2026) |
| Efficiency-first prototypes, latency or straightforward bulk | Start Haiku; move up for a demonstrated capability gap | Effort page (17 November 2026): start with `medium`; `low` for chat, short tool tasks and simple high-volume requests, but a long agent prompt at `low` is more likely to skip a search, stop early or skip a check; `high` for knowledge work, longer agent tasks and strict instruction following; `xhigh` or `max` only where evals show a gain over Sonnet 5.5 |
| Capability-first complex reasoning, accuracy or advanced autonomous coding | Start Opus; optimize downward after adequate quality | Opus medium starting effort |
| Demanding reasoning or long-horizon work that falls short on Opus at `xhigh` or `max` | Move to Fable 5.2 (selection guide, 14 November 2026) | Effort page (17 November 2026): start with `high`; `xhigh` for the hardest long-running work where a gain was measured; step down to `medium` or `low` where evals show that quality holds; reserve `max`, often for only a small gain |
| Bulk execution with difficult decisions | Cheaper executor plus frontier advisor, or a frontier orchestrator that delegates bulk work to lower-cost workers. For native Code candidates and preflight, read `references/41-claude-code-runtime-features.md`. | No default pair or effort |

- The guide recommends Opus as the starting point for most workloads. Keep both the capability-first path and the efficiency-first path.
- The API defaults above are Messages API defaults. The choosing-a-model, models overview and effort pages checked on 17 November 2026 state no Claude Code default for the 5.5 models; model-config was not re-read. Each model reference holds its Claude Code default.
- The Sonnet prompting page gives regression examples at higher effort, which rule out automatic maximization.
- A local Fable admission belongs to the runtime orchestrator and stays distinct from the vendor's `xhigh` and `max` advice.

Sources (refresh the current page and asset before reuse):

- [OpenAI model selection](https://developers.openai.com/api/docs/guides/model-selection) and its [served selector asset](https://developers.openai.com/_astro/ModelSelection.react.DJwdUSJM.js) (18 November 2026; the asset name changes with each site build, so take the current one from the guide page)
- [Claude model selection](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model)
- [Claude models overview](https://platform.claude.com/docs/en/about-claude/models/overview) (default effort row, 17 November 2026)
- [Claude effort](https://platform.claude.com/docs/en/build-with-claude/effort)
- [Sonnet prompting](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5)

## Companion routing

- `/alaa-codex-orchestrator` (Codex) and `/alaa-cc-orchestrator` (Claude Code): production multi-agent orchestration. Prefer them over a hand-written fan-out. Each owns its role catalog, role triggers, task selection, parallel scheduling and gates; this file sets no spawn-count default.
- Role identity and neutral controls are checked against the policy JSON of each runtime. Executable frontmatter preserves authority and selects no task pair. The standard and deep reviewer scopes share one reviewer profile; scope breadth alone creates no second executable identity.
- `/alaa-workflow`: durable multi-phase plans, phase prompts and resumable state.
- `/openai-docs`: the freshest GPT-6 and Codex guidance when this skill is stale. Use the official Anthropic documentation for Claude gaps.
- `/alaa-low-noise`: broad prompt research, validation, or a long tool-heavy session.

## Caveats

Benchmark claims, relative pricing, effort defaults and the capability order among current models are vendor-stated and time-sensitive. Before you treat a ranking here as current, re-check `references/00-source-map.md` and the live model pages.
