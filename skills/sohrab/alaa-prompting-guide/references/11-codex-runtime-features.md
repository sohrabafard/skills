# Codex Runtime Features

These are Codex app/CLI features, not raw model behavior. Read only the feature section needed; model/API guidance lives in `references/12-gpt-6.md`.

## `/goal` — persistent objective mode

A Goal is durable, thread-scoped state that keeps a Codex thread working toward one defined outcome across many turns instead of stopping after a single reply. Codex keeps working across turns toward a verifiable stopping condition, works in checkpoints, keeps a short progress log, and can run independently for hours. **Evidence, not speculation, determines completion**: it stops when it is fairly confident the stopping condition is met, when it hits its budget, or when it is genuinely blocked. Reaching a budget limit is explicitly not the same as completing the objective — in that case Codex stops substantive work, summarizes progress and blockers, and names the next useful step rather than claiming success.

A strong Goal defines seven things: **outcome** (what should be true when work concludes), **verification surface** (the test, benchmark, artifact, or log that proves it), **constraints** (what must not regress), **boundaries** (which files, tools, or resources are in play), **iteration policy** (how Codex picks the next action after each attempt), **blocked stop condition** (when to halt and what would unblock it), and **bounded budget** (an explicit turn or time cap so a stalled or non-converging goal cannot run unbounded).

Codex documents no fixed cap on goal length, but a bloated objective dulls both the directive and the completion check.

Use the goal tools or command exposed by the current host only when the user explicitly requests
an objective loop. Do not infer goal activation from ordinary implementation work. Read that
host's current goal tool schema for lifecycle, budget, and blocked-state rules; report unavailable
capabilities instead of writing remembered feature flags or a version gate into configuration.

### Ready-to-use `/goal` template

```text
/goal <desired end state> verified by <specific command, test, or artifact>, while preserving <what must not regress>.
Use only <allowed files, tools, or boundaries>. Between iterations, <how Codex should pick the next action>.
If blocked or no valid path remains, report exactly what is blocking progress and what would unblock it.
Stop after <turn or time cap> even if incomplete, reporting progress, evidence so far, and the next step.
```

Build worked examples from `references/12-gpt-6.md` plus the template above: one objective, one stopping condition, one validation loop. A goal should be larger than one prompt but smaller than an open-ended backlog. Documented fits are migrations, large refactors, experiments, and any long-running coding work with a clear success condition and a validation loop.

**This is not Claude Code's `/goal`.** Same command name, different mechanism — never carry a `/goal` block between the runtimes unedited. Read `references/41-claude-code-runtime-features.md` for how Claude Code's version differs and what that changes about what proves completion, how it's enabled, and what it costs.

## Subagents — explicit delegation and parallel spawning

Delegate only within authorization granted by the user or an applicable instruction. The host's
current collaboration tools define roles, nesting, concurrency, inheritance, and waiting; do not
copy defaults or tool names from another Codex surface. Prompts may authorize concrete independent
lanes, but cannot enable unavailable runtime features.

Custom agents are standalone TOML files in the active Codex home `agents/` directory or the
project's `.codex/agents/`. Required fields are `name`, `description`, and
`developer_instructions`. The official subagent page documents optional model and effort pins,
sandbox, MCP, and skill configuration; use only keys supported by the target host.

**Custom TOML model and effort pins win over spawn arguments.** Omitted settings inherit from
the parent. Changing a dispatch argument does not upgrade a pinned agent; select another registered
profile such as the deep reviewer. If unavailable, report the limit without claiming an override.
A definition created in the repository does not prove the current session has loaded it.

A subagent inherits parent sandbox policy and runtime overrides. A `read-only` TOML value is not
proof that every capability is read-only: inspect effective native permissions, parent overrides,
and MCP tool grants, whose server-side effects are outside native sandbox enforcement. Restrict
or withhold mutation-capable tools before claiming a read-only boundary. Do not change installed
configuration without authority.

Keep requested profile/model/effort separate from observed runtime identity. Use `unknown` for
values the host does not expose; copied pins are not observations. Verdict-bearing reports put
the verdict first and metadata afterward. Replacement-only agents keep their output contract;
the caller records their requested configuration externally.

The sources below were verified on 25 September 2026. The policy JSON records a dated
supported-effort snapshot; verify availability again on the actual dispatch host.

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

Goal and subagent guidance refreshed on 25 September 2026. Remaining historical sections were verified on 24 July 2026 and require live refresh before use. Historical defaults are not current dispatch authority: the `agents.max_threads` (6), `agents.max_depth` (1), and `agents.job_max_runtime_seconds` (1800) defaults; the 32 KiB / 65536-byte `project_doc_max_bytes` bounds; the 2%-or-8,000-character skill listing budget; and the `codex-cli` 0.128.0 requirement for goals are current published values and should be re-checked before being depended on.

Goals, `spawn_agents_on_csv`, and the agent-team-style batch flow are all marked experimental and may change. The `features.goals` key did not appear in the visible portion of the configuration reference, which is truncated on fetch; the two enabling paths cited above come from the Goals use-case page. `features.memories` exists and is off by default, but Codex's memory documentation redirects off the developer docs domain, so this pack makes no claim about how memories interact with `AGENTS.md` — treat that as unverified.

## Sources

- [Follow a goal | Codex use cases](https://developers.openai.com/codex/use-cases/follow-goals)
- [Using Goals in Codex (Cookbook)](https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex)
- [Subagents – Codex](https://developers.openai.com/codex/subagents)
- [Agent Skills – Codex](https://learn.chatgpt.com/docs/build-skills)
- [Custom instructions with AGENTS.md – Codex](https://developers.openai.com/codex/guides/agents-md)
- [Configuration Reference – Codex](https://developers.openai.com/codex/config-reference)
- [Slash commands – Codex CLI](https://developers.openai.com/codex/cli/slash-commands)
- [Automations – Codex app](https://developers.openai.com/codex/app/automations)
