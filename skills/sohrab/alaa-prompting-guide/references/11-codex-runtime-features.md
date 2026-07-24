# Codex Runtime Features (the environment GPT-5.6 runs inside)

These are Codex app/CLI features, not raw model behavior. Read `references/10-gpt-5-6.md` first, then only the feature section the task needs.

## `/goal` — persistent objective mode

A Goal is durable, thread-scoped state that keeps a Codex thread working toward one defined outcome across many turns instead of stopping after a single reply. Codex keeps working across turns toward a verifiable stopping condition, works in checkpoints, keeps a short progress log, and can run independently for hours. **Evidence, not speculation, determines completion**: it stops when it is fairly confident the stopping condition is met, when it hits its budget, or when it is genuinely blocked. Reaching a budget limit is explicitly not the same as completing the objective — in that case Codex stops substantive work, summarizes progress and blockers, and names the next useful step rather than claiming success.

A strong Goal defines seven things: **outcome** (what should be true when work concludes), **verification surface** (the test, benchmark, artifact, or log that proves it), **constraints** (what must not regress), **boundaries** (which files, tools, or resources are in play), **iteration policy** (how Codex picks the next action after each attempt), **blocked stop condition** (when to halt and what would unblock it), and **bounded budget** (an explicit turn or time cap so a stalled or non-converging goal cannot run unbounded).

**Must be enabled first.** Goals are an experimental feature, off by default. Turn them on from the CLI with `/experimental`, or set `goals = true` under `[features]` in `~/.codex/config.toml`. The feature requires `codex-cli` 0.128.0 or later. Manage the lifecycle with `/goal <objective>` (set), bare `/goal` (view current objective and status), `/goal pause`, `/goal resume`, and `/goal clear`.

### Ready-to-use `/goal` template

```text
/goal <desired end state> verified by <specific command, test, or artifact>, while preserving <what must not regress>.
Use only <allowed files, tools, or boundaries>. Between iterations, <how Codex should pick the next action>.
If blocked or no valid path remains, report exactly what is blocking progress and what would unblock it.
Stop after <turn or time cap> even if incomplete, reporting progress, evidence so far, and the next step.
```

Build worked examples from `references/10-gpt-5-6.md` plus the template above: one objective, one stopping condition, one validation loop. A goal should be larger than one prompt but smaller than an open-ended backlog. Documented fits are migrations, large refactors, experiments, and any long-running coding work with a clear success condition and a validation loop.

**This is not Claude Code's `/goal`.** Same command name, different mechanism: Codex runs a durable thread-scoped objective loop with its own budget accounting, while Claude Code wraps a session-scoped Stop hook whose completion check is a separate small evaluator model reading the transcript. The two differ in what proves completion, in how they are enabled, and in what they cost. Never carry a `/goal` block between the runtimes unedited — see `references/41-claude-code-runtime-features.md`.

## Subagents — explicit delegation and parallel spawning

**Codex only spawns a new agent when you explicitly ask it to.** It never fans out on its own, and there is no dedicated slash command for spawning — delegation is requested in natural language. This is the single most important prompt-side fact about the runtime: delegation language for Codex must authorize positively, not merely restrict. See `references/06-invocation-and-composition.md` for the polarity rule.

Built-in roles: `default` (general fallback), `worker` (execution-focused implementation and fixes), `explorer` (read-heavy codebase exploration). Custom agents are standalone TOML files in `~/.codex/agents/` (personal) or `.codex/agents/` (project). Required fields: `name`, `description`, `developer_instructions`. Optional: `nickname_candidates`, `model`, `model_reasoning_effort`, `sandbox_mode`, `mcp_servers`, `skills.config`. Each subagent inherits the parent session's sandbox policy and runtime overrides. When several agents run concurrently, the parent orchestrates, waits for all requested results, and consolidates them into one summary.

Global configuration under `[agents]` in `~/.codex/config.toml`:

| Key | Default | Meaning |
|---|---|---|
| `agents.max_threads` | `6` | Maximum agent threads open concurrently |
| `agents.max_depth` | `1` | Maximum nesting depth for spawned agent threads; root sessions start at depth 0 |
| `agents.job_max_runtime_seconds` | `1800` when unset | Default per-worker timeout for `spawn_agents_on_csv` jobs |

The underlying collaboration tools — `spawn_agent`, `send_input`, `resume_agent`, `wait_agent`, `close_agent` — are gated behind `features.multi_agent`, which is stable and on by default.

```text
Explicit authorization: you may use subagents and run independent work in parallel for this task without asking
again. Spawn one agent per independent file/module/lane, wait for all of them, and reconcile the results yourself
before moving on. Give every subagent the same constraints and a clearly scoped slice so nothing is duplicated
or dropped.
```

## `spawn_agents_on_csv` — background batch jobs

An experimental tool for many similar tasks that map one-to-one to rows. Codex reads a CSV, applies an instruction template with `{column_name}` placeholders per row, spawns one worker per row, waits for the batch, and exports combined results to an output CSV carrying the original row data plus `job_id`, `item_id`, `status`, `last_error`, and `result_json`.

Parameters: `csv_path`, `instruction`, `id_column` (optional stable item identifier), `output_schema` (the JSON structure each worker returns), `output_csv_path`, `max_concurrency`, and `max_runtime_seconds` (per-call override of `agents.job_max_runtime_seconds`).

Each worker **must call `report_agent_job_result` exactly once**. A worker that exits without reporting produces an error row rather than hanging the batch — so any instruction template you generate must make that call an explicit, unconditional final step, including on the failure path.

```text
spawn_agents_on_csv with csv_path="tickets.csv", instruction="Investigate ticket {ticket_id} about {summary}
and propose a fix; report your finding.", output_csv_path="ticket_results.csv", id_column="ticket_id",
max_concurrency=4
```

## `AGENTS.md` — durable project instructions

Codex rebuilds a resolved `AGENTS.md` chain on every run and at the start of each TUI session, so there is no cache to clear. Resolution order: global scope (`~/.codex` by default, checking `AGENTS.override.md` first, then `AGENTS.md`), then project scope walked from the Git root down to the current directory, checking `AGENTS.override.md`, `AGENTS.md`, then any configured fallback filenames at each level. Files are concatenated root-first and joined with blank lines, so files closer to the working directory override earlier guidance by appearing later in the combined prompt. Override files take precedence at their own level; `~/.codex/AGENTS.override.md` is the documented way to apply a temporary global override without deleting the base file.

`project_doc_max_bytes` caps the combined size (32 KiB default, configurable up to 65536 bytes); Codex stops adding files once the limit is reached, which means a deep chain can silently drop the outermost files. `project_doc_fallback_filenames` in `~/.codex/config.toml` adds alternative filenames. `CODEX_HOME` relocates the global profile used for discovery.

No manual invocation is needed. Codex does **not** update these files on its own, so a prompt must explicitly instruct it to write a correction back into `AGENTS.md` when the correction should persist. For authoring guidance, read `references/70-agent-instruction-files.md`.

## Agent Skills

Skills package instructions, references, scripts, and assets into a directory so Codex can follow a workflow reliably — this skill is one. Structure: required `SKILL.md` (frontmatter with `name` and `description`, plus the body), optional `scripts/`, `references/`, `assets/`, and `agents/openai.yaml`.

Discovery runs across these scopes, highest priority first:

| Scope | Path | Status |
|---|---|---|
| Repo (cwd) | `.agents/skills` | documented |
| Repo (parent) | `../.agents/skills` | documented |
| Repo (root) | `$REPO_ROOT/.agents/skills` | documented |
| User | `$HOME/.agents/skills` | documented |
| User | `$HOME/.codex/skills` | **field-verified, undocumented** |
| System | Bundled by OpenAI | documented |

The `$HOME/.codex/skills` row is not in the official page but works: skills installed there are discovered and trigger normally, verified on Windows where the path is `Join-Path $HOME ".codex\skills"`. Treat the official list as incomplete rather than treating this path as broken. Note that it sits next to `~/.codex/agents/`, which is where agent TOMLs live — so a Codex user who keeps both under `~/.codex/` has one coherent tree, which is likely why this location is in use even though the docs point elsewhere.

When generating install instructions, name `$HOME/.codex/skills` for personal skills unless the user has said otherwise, and `.agents/skills` for repository-scoped skills that travel with a project.

For context efficiency Codex first loads only each skill's name and description. That listing is capped at 2% of the model's context window, or 8,000 characters when the context window is unknown; the full `SKILL.md` loads only once a skill is selected, regardless of that budget. Three invocation paths: `/skills` or a `$name` mention in the CLI and IDE, direct selection in the app, and implicit matching of the prompt against the skill's `description`. That last path is why a skill's `description` must state a clear, assertive trigger scope. `agents/openai.yaml` carries presentation metadata and `allow_implicit_invocation` (default `true`) for skills that should never fire on their own.

Codex documents no skill frontmatter keys beyond `name` and `description`. Treat Claude-side keys as inert here. See `references/60-skill-authoring.md`.

## Session-shaping slash commands

These change how a thread runs and are worth naming explicitly in a generated operating prompt rather than leaving to the operator:

| Command | Effect |
|---|---|
| `/plan` | Switch to plan mode so Codex proposes an execution strategy before implementing |
| `/review` | Request a working-tree review of local changes |
| `/experimental` | Toggle optional features, including subagents and goals |
| `/fork` | Clone the current conversation into a new thread to explore an alternative in parallel |
| `/side` (alias `/btw`) | Start an ephemeral side conversation without disturbing the main thread |
| `/personality` | Set communication style without rewriting the prompt |
| `/compact` | Summarize the conversation to reclaim context |
| `/model`, `/permissions`, `/status`, `/approve`, `/new`, `/resume` | Model selection, approval requirements, session configuration and token usage, retry of an auto-review denial, and thread lifecycle |

A `/plan` gate followed by a `/goal` is the Codex analogue of the plan-then-autonomy pattern: approve the approach first, then hand the thread a bounded objective.

## Automations — scheduled recurring tasks

Codex can schedule recurring background tasks that add findings to the inbox, or archive themselves when there is nothing to report. Three shapes: standalone automations that start fresh runs on a schedule and report into Triage; project automations, which require the app to be running and the selected project to be available on disk; and thread automations, heartbeat-style recurring wake-ups attached to the current thread. Scheduling accepts predefined daily and weekly slots, custom cron syntax, and minute-based intervals for active follow-up loops.

Two operational cautions belong in any prompt that sets one up: on a Git repository an automation runs either in the local project or on a dedicated background worktree, and frequent schedules accumulate worktrees over time; and in read-only sandbox mode, tool calls fail when they need to modify files, use the network, or work with apps.

## Caveats

Verified against live documentation on 24 July 2026. Time-sensitive: the `agents.max_threads` (6), `agents.max_depth` (1), and `agents.job_max_runtime_seconds` (1800) defaults; the 32 KiB / 65536-byte `project_doc_max_bytes` bounds; the 2%-or-8,000-character skill listing budget; and the `codex-cli` 0.128.0 requirement for goals are current published values and should be re-checked before being depended on.

Goals, `spawn_agents_on_csv`, and the agent-team-style batch flow are all marked experimental and may change. The `features.goals` key did not appear in the visible portion of the configuration reference, which is truncated on fetch; the two enabling paths cited above come from the Goals use-case page. `features.memories` exists and is off by default, but Codex's memory documentation redirects off the developer docs domain, so this pack makes no claim about how memories interact with `AGENTS.md` — treat that as unverified.

## Sources

- [Follow a goal | Codex use cases](https://developers.openai.com/codex/use-cases/follow-goals)
- [Using Goals in Codex (Cookbook)](https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex)
- [Subagents – Codex](https://developers.openai.com/codex/subagents)
- [Agent Skills – Codex](https://developers.openai.com/codex/skills)
- [Custom instructions with AGENTS.md – Codex](https://developers.openai.com/codex/guides/agents-md)
- [Configuration Reference – Codex](https://developers.openai.com/codex/config-reference)
- [Slash commands – Codex CLI](https://developers.openai.com/codex/cli/slash-commands)
- [Automations – Codex app](https://developers.openai.com/codex/app/automations)
