# Model Selection and Companion Routing

## Capability evidence and allocation ownership

`assets/codex-model-policy.json` and `assets/claude-model-policy.json` own capability snapshots, ordinary eligibility, and the registrations of neutral roles and artifacts. The Codex policy owns supported-effort snapshots. The Claude policy owns Claude capabilities and model availability conditions. Supported efforts are separate from selection_enabled: a retained effort history never enables a disabled model. The policies define no role default and choose no task pair. Main-session controls remain externally configured, and an allocation does not change them.

For every managed role, including research, review, verification, documentation and rule-writer, the runtime orchestrator owns task allocation, priority, admission and deliberate source departures. Read `/alaa-codex-orchestrator` or `/alaa-cc-orchestrator` `references/routing-matrix.md` for that decision. For bounded standalone delegation, the parent uses that allocation procedure and records a compact dispatch; it need not start the full pipeline or create a plan solely for selection. `/alaa-workflow` records allocation when durable state is admitted. The tables below are evidence inputs, not executable defaults.

To realize an explicit task model AND effort, use `references/11-codex-runtime-features.md` or `references/41-claude-code-runtime-features.md`. For capability and uncertainty checks, use `references/50-effort-and-thinking.md`. A registered role name selects authority only, and so does a retained compatibility ID that names a model or an effort. Neither a name nor an inherited control counts as task selection. Before explicit dispatch, `alaa-codex-orchestrator references/model-effort-policy.md` or its `alaa-cc-orchestrator` mirror normalizes omitted fields; its resolved defaults count as task selection.

Ordinary Codex selection excludes GPT-6 Sol and retains its effort snapshot as history. GPT-6.1 Sol is the current Sol candidate. Use the newest member of the selected family that is verified, supported and eligible; a suitable Luna stays eligible. If current Sol is unavailable, require an exact eligible realization or block the affected lane. Never fall back to old Sol. Record an explicit user request for a legacy model separately. It neither restores ordinary eligibility nor passes ordinary task-control validation.

The active Claude set is Haiku 5.5, Sonnet 5.5, Opus 5.5 and Fable 5.2 (Fable 5.1 became history on 14 November 2026). Mythos is excluded from active selection and custom profiles. Historical models supply reference evidence only; availability and loaded registry remain separately verified.

## Official task guidance and local policy

Refreshed 9 October 2026; Claude rows and defaults refreshed 14 November 2026. These source recommendations are not executable local pins, and they prove neither host availability nor quality. The complete served selector asset was read as text, without execution; browser interaction was not run. The supplied screenshots match its cells. L = GPT-6 Luna, S = GPT-6.1 Sol, A = GPT-6 Astra.

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

The matrix is a dated editorial starting point. Some rationale metadata retains an older Sol generation; use the served recommendations, not that historical label. In the well-scoped bug row, the medium and high cells are editorial checking choices with no demonstrated gain over low. In the search row, the medium and high cells lack direct benchmark proof; only xhigh was tested. The animation choices and the rows marked editorial fallback are editorial. No general reliability rate or saving follows.

The guide's explicit prose also recommends Luna low for precise or bounded work, Luna xhigh for cross-app prioritization, Sol medium for complex revisable technical work, and Sol xhigh for polished, connected or conflicting-evidence work. It fits Astra low to concise nuanced writing, Astra medium to broad ambitious projects and Astra xhigh to demanding analysis. It suggests comparing Sol on cost-conscious complex work, and optionally defaulting to Astra when cost and latency are unconstrained. It assigns no effort to those two suggestions.

Sol low for feature work and Luna high for scoped bugs have official selector support. Workload admission and exceptional selection belong to the runtime orchestrator. Source guidance proves no local superiority or availability.

The [Codex Terra guidance](https://learn.chatgpt.com/docs/model-selection#when-to-consider-gpt-61-terra),
verified 3 November 2026, names concise writing from supplied material, computer use
with a defined outcome, and scoped code fixes with explicit inputs, requirements and a check.
These recommendations establish no measured local quality, cost or speed. Read
`references/12-gpt-6.md` for Terra controls and the Codex routing matrix for admission.

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

The guide recommends Opus as the starting point for most workloads. Qualify each default effort by surface:

- Opus: medium.
- Haiku: medium.
- Sonnet: medium in Claude Code and the Claude apps; high on the Platform and the API.
- Fable 5.2: medium in Claude Code; high on the Claude API.

Preserve both the capability-first path and the efficiency-first path. The separate Sonnet prompting guidance recommends medium for well-specified agentic coding and high for harder or longer work. The source's examples of regressions at higher effort rule out automatic maximization. Any local Fable admission belongs to the runtime orchestrator and remains distinct from the vendor's xhigh and max advice. No live run is implied.

- [OpenAI model selection](https://developers.openai.com/api/docs/guides/model-selection) and its [served selector asset](https://developers.openai.com/_astro/ModelSelection.react.DJkmSLnH.js) (refresh the current page/asset before reuse)
- [Claude model selection](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model)
- [Sonnet prompting](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5)

## Companion routing

`/alaa-codex-orchestrator` (Codex) and `/alaa-cc-orchestrator` (Claude Code) are the production multi-agent orchestration packs, each carrying a conditionally routed role catalog for its runtime: core lanes (spec analyst, explorer, researcher, test strategist, implementer with a separate escalated implementer, independent verifier, failure analyst, reviewer, documenter) plus conditionally gated specialists (adversarial review, architecture, security, migration, API contract, dependency audit, accessibility, browser QA, performance, observability, release).

The catalog is a menu: dispatch only triggered roles. The orchestrator owns parallel scheduling and gate economics; this reference imposes no spawn-count default.

Claude role identity and neutral controls are checked against `assets/claude-model-policy.json`. Executable frontmatter preserves authority and selects no task pair. The standard and deep reviewer scopes share the existing reviewer profile. Scope breadth alone does not create a second executable identity.

Codex capabilities and neutral role identities are checked against `assets/codex-model-policy.json`. The orchestrator owns role triggers and actual task selection.

In both packs the lead never implements or runs heavy suites itself. The verifier executes commands under a low-priority resource policy. No lane approves its own change. Prefer these packs over hand-writing a fan-out. The lead is always the session's own model.

Other companions:

- `/alaa-workflow`: durable multi-phase plans, phase prompts, resumable state, and the implementation-plus-review cadence.
- `/openai-docs`: freshest GPT-6 and Codex guidance when this skill is stale. Use official Anthropic docs for Claude gaps.
- `/alaa-low-noise`: broad prompt research, validation, or long tool-heavy sessions.

## Caveats

Benchmark claims, relative pricing, effort defaults, and the capability ordering among current models are vendor-stated and time-sensitive — a single release can invalidate any ranking here. Re-check `references/00-source-map.md` and the live model pages before treating any ranking here as current.
