# Model Selection and Companion Routing

## Active model routing

For Codex, read `references/12-gpt-6.md` and the exact role profile in
`assets/codex-model-policy.json`. That file alone owns executable Codex pins and rationales;
this page does not reproduce them. Use `references/50-effort-and-thinking.md` before changing
one. A historical GPT-5.6 comparison does not authorize a production exception.

For Claude Code, `assets/claude-model-policy.json` alone owns role pins, rationales,
escalation criteria and calibration status. Apply its legacy-replacement rule in `notes` before selection; historical capability snapshots cannot override it. Use current model references for prompting and
`references/41-claude-code-runtime-features.md` for activation limits. Historical references never select current profiles.

The active Claude set is Haiku 5.5, Sonnet 5.5, Opus 5.5 and Fable 5.1. Mythos is explicitly excluded from active selection and custom profiles; a joint launch page supplies no admission.

## Decision helper

1. Resolve runtime, surface and available registered profiles. Historical or announced models authorize no active fallback.
2. Finalize scope, dependencies and task consolidation before model allocation. Then allocate every finalized plan task in one batch through the procedure below. Runtime matrices own admission; canonical policies own exact registered pins. Planning effort does not determine worker effort; do not impose a trial ladder.
3. For Codex distinguish exact mechanical work, bounded semantic work, reproduced local bugs, ordinary engineering and demanding coupled reasoning. For Claude, exact mechanical or settled bounded semantic work can fit Haiku medium/high; everyday engineering with interacting local decisions fits Sonnet, and materially coupled unresolved system design fits Opus. A settled architecture need not prescribe every line of an implementation.
4. Apply `references/50-effort-and-thinking.md` for effort, planning and exceptional admission. Selection is an unrun hypothesis until compared; no task requires a calibration experiment.
5. Verify actual controls and availability. Pinned profiles can override caller values; prose cannot change them. Inline planning needs verified compatible controls, otherwise a registered read-only planner. Its draft stays advisory; the parent ratifies the durable plan.
6. Before delegation wording read `references/06-invocation-and-composition.md`. For a requested goal loop read that runtime's feature reference; `/goal` mechanisms differ. `/alaa-workflow` owns durable multi-phase artifacts.

## One allocation pass over the finalized plan

1. Choose the task's authority role first. Research, review, verification and documentation retain their registered role restrictions and canonical pins; an implementation row never turns them into implementers. Match each actual task/lane to an applicable source row from its scope and remaining decisions; record `not applicable` with the role reason when no row fits. A goal-level label does not describe every child task. Read recommendations once for the batch and reuse them; do not repeat discovery per task.
2. Default priority to **Balanced**. Use **Lower latency/cost** when the user explicitly prefers it. Use **Higher quality** for an explicit user high/quality request, documented inability of the current route to meet acceptance after excluding missing context/tool/specification problems, or a demonstrably consequential task whose concrete failure consequence is recorded in the plan. Vague importance or a production label is insufficient. Importance can select priority; it does not establish complexity or waive gates.
3. For OpenAI implementation lanes, look up the row's actual model/effort cell. Higher-quality preference does not mean effort `high`: the cell can select medium, high or xhigh. Select its registered implementation profile only when lane admission holds. Other roles retain canonical role pins; record recommendations as guidance or a deliberate departure, never a prose override. A source-matched Astra branch records why decomposition or cheaper admitted work cannot satisfy that lane's acceptance; it requires no artificial failed trial. Outside a matching source branch, existing inadequacy/explicit-user exceptional admission remains available.
4. Claude's guide is a capability/workload matrix, without the OpenAI slider. Match admitted settled bounded work to Haiku, everyday work to Sonnet and materially coupled unresolved work to Opus; apply supported medium/high guidance and priority with an explicit reason. Longer or stricter bounded Haiku work can use high; complexity needing interacting design decisions selects Sonnet. Do not infer a Fable route from every long session or deep-research label: the pack retains inadequate-workhorse/explicit-model admission. Vendor xhigh/max escalation advice and local Opus-high admission remain distinct.
5. Write all selections together into the workflow plan before dispatch: task, source row/date, priority and trigger, exact registered role/model/effort, deciding scope/acceptance evidence, admission or deliberate departure, calibration status and target availability. Unsupported or unavailable pairs stay blocked; never silently substitute. A documented deliberate source departure does not manufacture a missing profile or grant configuration authority.
6. At an existing material-scope or fix-follow-up boundary, reallocate only affected remaining tasks. Preserve completed work and still-valid evidence. No rediscovery, replay or new calibration experiment is required by allocation alone.

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

Sol-low feature work and Luna-high scoped bugs have official selector support; their narrow admission contracts remain uncalibrated local policy. Source-matched Astra medium/xhigh routes are admitted through the batch procedure. The existing Astra-high inadequacy/explicit-selection profile remains a compatibility route outside matching table cells. No recommendation guarantees local superiority.

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

The guide recommends Opus as a most-workloads starting point. Qualify defaults by surface: Opus medium; Haiku medium; Sonnet Code/apps medium versus Platform/API high; Fable Code/API high versus Cowork/claude.ai medium. Preserve capability-first and efficiency-first paths. Separate Sonnet prompting guidance recommends medium for well-specified agentic coding and high for harder/longer work; source examples of higher-effort regressions rule out automatic maximization. Local Fable implementation remains inadequacy/explicit-selection after context/tool/spec correction and decomposition; its Opus-high boundary is local policy, distinct from vendor xhigh/max advice. No live comparison is implied.

- [OpenAI model selection](https://developers.openai.com/api/docs/guides/model-selection) and its [served selector asset](https://developers.openai.com/_astro/ModelSelection.react.DJkmSLnH.js) (refresh the current page/asset before reuse)
- [Claude model selection](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model)
- [Sonnet prompting](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5)

## Companion routing

`/alaa-codex-orchestrator` (Codex) and `/alaa-cc-orchestrator` (Claude Code) are the production multi-agent orchestration packs, each carrying a conditionally routed role catalog for its runtime: core lanes (spec analyst, explorer, researcher, test strategist, implementer with a separate escalated implementer, independent verifier, failure analyst, reviewer, documenter) plus conditionally gated specialists (adversarial review, architecture, security, migration, API contract, dependency audit, accessibility, browser QA, performance, observability, release).

The catalog is a menu: dispatch only triggered roles. The orchestrator owns parallel scheduling and gate economics; this reference imposes no spawn-count default.

Claude pins are read from `assets/claude-model-policy.json`; executable frontmatter is a checked projection, never a second policy. Standard and deep reviewer scopes share the existing reviewer profile; scope breadth alone does not create a second executable identity.

Codex pins and calibration status are read from `assets/codex-model-policy.json`; the catalog owns role triggers, not a second model policy.

In both packs the lead never implements or runs heavy suites itself, the verifier executes commands under a low-priority resource policy, and no lane approves its own change. Prefer these packs over hand-writing a fan-out; the lead is always the session's own model.

Other companions:

- `/alaa-workflow`: durable multi-phase plans, phase prompts, resumable state, and the implementation-plus-review cadence.
- `/openai-docs`: freshest GPT-6 and Codex guidance when this skill is stale. Use official Anthropic docs for Claude gaps.
- `/alaa-low-noise`: broad prompt research, validation, or long tool-heavy sessions.

## Caveats

Benchmark claims, relative pricing, effort defaults, and the capability ordering among current models are vendor-stated and time-sensitive — a single release can invalidate any ranking here. Re-check `references/00-source-map.md` and the live model pages before treating any ranking here as current.
