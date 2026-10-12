# Model Selection and Companion Routing

## Capability evidence and allocation ownership

`assets/codex-model-policy.json` and `assets/claude-model-policy.json` own capability snapshots, active model/effort support and model-neutral role/artifact registrations. They define no role-default or task choice. Main-session controls remain externally configured; an allocation does not change them.

For every managed role, including research, review, verification, documentation and rule-writer, the runtime orchestrator owns task allocation, priority, admission and deliberate source departures. Read `/alaa-codex-orchestrator` or `/alaa-cc-orchestrator` `references/routing-matrix.md` for that decision. For bounded standalone delegation, the parent uses that allocation procedure and records a compact dispatch; it need not start the full pipeline or create a plan solely for selection. `/alaa-workflow` records allocation when durable state is admitted. The tables below are evidence inputs, not executable defaults.

Use `references/11-codex-runtime-features.md` or `references/41-claude-code-runtime-features.md` to realize explicit task model AND effort, and `references/50-effort-and-thinking.md` for capability/uncertainty checks. Registered role names, including retained model/effort-named compatibility IDs, select authority only. Neither names nor inherited controls count as task selection.

The active Claude set is Haiku 5.5, Sonnet 5.5, Opus 5.5 and Fable 5.1. Mythos is excluded from active selection and custom profiles. Historical models supply comparison evidence only; availability and loaded registry remain separately verified.

## Official task guidance and local policy

Refreshed 9 October 2026. These source recommendations are neither executable local pins, host availability nor comparative-quality proof. The complete served selector asset was read as text, without execution; browser interaction was not run. The supplied screenshots match its cells. L = GPT-6 Luna, S = GPT-6.1 Sol, A = GPT-6 Astra.

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

The matrix is a dated editorial starting point. Some rationale metadata retains an older Sol generation; use the served recommendations, not that historical label. Scoped-bug medium/high are editorial checking choices without demonstrated gains over low. Search medium/high lack direct benchmark proof; only xhigh was tested. Animation choices and marked fallback rows are editorial. No general reliability rate or savings follows.

Explicit prose also recommends Luna low for precise/bounded work, Luna xhigh for cross-app prioritization, Sol medium for complex revisable technical work and Sol xhigh for polished/connected/conflicting-evidence work. Astra low fits concise nuanced writing, medium broad ambitious projects and xhigh demanding analysis. It suggests comparing Sol on cost-conscious complex work and optionally defaulting to Astra with unconstrained cost/latency, without assigning effort to those two suggestions.

Sol-low feature work and Luna-high scoped bugs have official selector support. Workload admission and exceptional selection belong to the runtime orchestrator; source guidance proves no local superiority or availability.

| Claude workload/path | Source recommendation | Effort evidence |
|---|---|---|
| Everyday coding, analysis, content, vision, agent tools | Sonnet | Unspecified in selection guide |
| Complex autonomous coding, broad refactors, systems, computer use | Opus | Unspecified in model matrix |
| Highest capability, long sessions, deep research, finished documents | Fable | Unspecified in model matrix |
| Real-time, bulk, cost-sensitive processing/subagents | Haiku | Unspecified in model matrix |
| Efficiency-first prototypes, latency or straightforward bulk | Start Haiku; move up for a demonstrated capability gap | No task-specific effort |
| Capability-first complex reasoning, accuracy or advanced autonomous coding | Start Opus; optimize downward after adequate quality | Opus medium starting effort |
| Demanding long-horizon work inadequate at Opus xhigh/max | Consider Fable | No selected Fable effort |
| Bulk execution with difficult decisions | Cheaper workers plus frontier advisor | No selected pair |

The guide recommends Opus as a most-workloads starting point. Qualify defaults by surface: Opus medium; Haiku medium; Sonnet Code/apps medium versus Platform/API high; Fable Code/API high versus Cowork/claude.ai medium. Preserve capability-first and efficiency-first paths. Separate Sonnet prompting guidance recommends medium for well-specified agentic coding and high for harder/longer work; source examples of higher-effort regressions rule out automatic maximization. Any local Fable admission belongs to the runtime orchestrator and remains distinct from vendor xhigh/max advice. No live comparison is implied.

- [OpenAI model selection](https://developers.openai.com/api/docs/guides/model-selection) and its [served selector asset](https://developers.openai.com/_astro/ModelSelection.react.DJkmSLnH.js) (refresh the current page/asset before reuse)
- [Claude model selection](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model)
- [Sonnet prompting](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5)

## Companion routing

`/alaa-codex-orchestrator` (Codex) and `/alaa-cc-orchestrator` (Claude Code) are the production multi-agent orchestration packs, each carrying a conditionally routed role catalog for its runtime: core lanes (spec analyst, explorer, researcher, test strategist, implementer with a separate escalated implementer, independent verifier, failure analyst, reviewer, documenter) plus conditionally gated specialists (adversarial review, architecture, security, migration, API contract, dependency audit, accessibility, browser QA, performance, observability, release).

The catalog is a menu: dispatch only triggered roles. The orchestrator owns parallel scheduling and gate economics; this reference imposes no spawn-count default.

Claude role identity and neutral controls are checked against `assets/claude-model-policy.json`; executable frontmatter preserves authority without selecting a task pair. Standard and deep reviewer scopes share the existing reviewer profile; scope breadth alone does not create a second executable identity.

Codex capabilities and neutral role identities are checked against `assets/codex-model-policy.json`; the orchestrator owns role triggers and actual task selection.

In both packs the lead never implements or runs heavy suites itself, the verifier executes commands under a low-priority resource policy, and no lane approves its own change. Prefer these packs over hand-writing a fan-out; the lead is always the session's own model.

Other companions:

- `/alaa-workflow`: durable multi-phase plans, phase prompts, resumable state, and the implementation-plus-review cadence.
- `/openai-docs`: freshest GPT-6 and Codex guidance when this skill is stale. Use official Anthropic docs for Claude gaps.
- `/alaa-low-noise`: broad prompt research, validation, or long tool-heavy sessions.

## Caveats

Benchmark claims, relative pricing, effort defaults, and the capability ordering among current models are vendor-stated and time-sensitive — a single release can invalidate any ranking here. Re-check `references/00-source-map.md` and the live model pages before treating any ranking here as current.
