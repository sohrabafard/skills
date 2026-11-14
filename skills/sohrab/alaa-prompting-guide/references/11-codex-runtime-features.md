# Codex Runtime Features

These are features of the Codex app and CLI, not raw model behavior. Read only the feature section you need. Model and API guidance lives in `references/12-gpt-6.md`.

## Rejected tool input or patch context

Before you repair a rejected call, read the active host's tool schema. JavaScript orchestration, shell-command arguments, structured objects and patch text are different input contracts. Keep each language in its declared input. An API example does not establish the host's schema.

For a patch-context mismatch, inspect the current target region and the scoped diff, including other owners' edits. Then rebuild the smallest patch that matches that state. For a duplicate-operation error, combine or split operations only as the active patch contract permits. If a mutation may have occurred, reconcile the actual state before you retry. Never blindly replay an uncertain write.

This section owns schema and context mistakes. Route process, shell, path or sandbox failures to
`/alaa-codex-runtime-ops`. Neither diagnosis authorizes a settings change or broader writes.
Use the active repair and retry budget. When the required contract or the safe resulting state remains unknown, report the exact blocker and stop the dependent operation. This procedure is grounded in active host schemas inspected 18 October 2026. Recheck the executing host rather than copying a remembered tool signature.

## `/goal` — persistent objective mode

A Goal is durable, thread-scoped state that keeps a Codex thread working toward one defined outcome across many turns instead of stopping after a single reply. Codex keeps working across turns toward a verifiable stopping condition, works in checkpoints, keeps a short progress log, and can run independently for hours. **Evidence, not speculation, determines completion**: it stops when it is fairly confident the stopping condition is met, when it hits its budget, or when it is genuinely blocked. Reaching a budget limit is explicitly not the same as completing the objective — in that case Codex stops substantive work, summarizes progress and blockers, and names the next useful step rather than claiming success.

A strong Goal defines seven things: **outcome** (what should be true when work concludes), **verification surface** (the test, benchmark, artifact, or log that proves it), **constraints** (what must not regress), **boundaries** (which files, tools, or resources are in play), **iteration policy** (how Codex picks the next action after each attempt), **blocked stop condition** (when to halt and what would unblock it), and **bounded budget** (an explicit turn or time cap so a stalled or non-converging goal cannot run unbounded).

### CLI composer and objective storage

Verified 3 November 2026 against installed `codex-cli 0.163.0` and its tagged source. The TUI accepts a leading `/goal` with a multiline objective in one composer message. The protocol caps the stored objective at **4,000 Rust characters** (`str::chars().count()`). Above that cap, the TUI writes the full objective to `goal-objective.md` and stores a short file reference. The CLI source does not establish Desktop composer behavior or the active goal tool's limits. Verify the target host and input path before depending on the file route.

- [Multiline composer input](https://github.com/openai/codex/blob/rust-v0.163.0/codex-rs/tui/src/chatwidget/tests/goal_validation.rs#L78)
- [Stored objective limit](https://github.com/openai/codex/blob/rust-v0.163.0/codex-rs/protocol/src/protocol.rs#L4207)
- [TUI file route](https://github.com/openai/codex/blob/rust-v0.163.0/codex-rs/tui/src/goal_files.rs#L121)

### Activation

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

Delegate only within authorization granted by the user or an applicable instruction. The host's current collaboration tools define roles, nesting, concurrency, inheritance and waiting. Do not copy defaults or tool names from another Codex surface. A prompt may authorize concrete independent lanes, but it cannot enable an unavailable runtime feature.

Custom agents are standalone TOML files in the active Codex home `agents/` directory or the
project's `.codex/agents/`. Required fields are `name`, `description`, and
`developer_instructions`. The official subagent page documents optional model and effort pins,
sandbox, MCP, and skill configuration; use only keys supported by the target host.

**Custom TOML model and effort pins win over spawn arguments.** Verified 9 October 2026: when both pins are omitted, explicit spawn controls precede global agent defaults and parent settings. Managed authority roles omit both pins. Supply BOTH task controls on a verified compatible spawn surface. An inherited value is not a task decision. In the active host, a full-history fork can forbid overrides. Neither prose nor a disk edit can change a stale loaded pin; use an available exact verified realization or block the affected lane.
A definition created in the repository does not prove that the current session has loaded it.

`agents.max_concurrent_threads_per_session` caps the spawned-agent threads open at once, excluding the primary thread. `agents.max_threads` is its legacy alias. When the key is unset, Codex chooses the default; neither source states a number. Verified 14 November 2026 against [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) and the [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference).

A subagent inherits the parent sandbox policy and runtime overrides. A `read-only` TOML value does not prove that every capability is read-only. Inspect the effective native permissions, the parent overrides and the MCP tool grants; the server-side effects of an MCP tool are outside native sandbox enforcement. Before you claim a read-only boundary, restrict or withhold mutation-capable tools. Do not change installed configuration without authority.

In `workspace-write`, these paths stay read-only inside a writable root, recursively: `.git`, whether it is a directory or a pointer file, together with the Git directory a pointer file names; and the directories `.agents`, `.codex` and `.aws` when they exist. The page does not say how `git commit` is handled. Verified 14 November 2026 against [Sandbox and approvals](https://learn.chatgpt.com/docs/agent-approvals-security).

Keep the requested profile, model and effort separate from the observed runtime identity. Use `unknown` for a value the host does not expose; a copied pin is not an observation. A report that carries a verdict puts the verdict first and the metadata after it. A replacement-only agent keeps its output contract, and the caller records its requested configuration externally.

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

Skills package instructions, references, scripts, and assets into a directory so Codex can follow a workflow reliably — this skill is one. A skill requires `SKILL.md` (frontmatter with `name` and `description`, plus the body). `scripts/`, `references/`, `assets/`, and `agents/openai.yaml` are optional.

Discovery runs across these scopes, highest priority first:

| Scope | Path | Status |
|---|---|---|
| Repo (cwd) | `.agents/skills` | documented |
| Repo (parent) | `../.agents/skills` | documented |
| Repo (root) | `$REPO_ROOT/.agents/skills` | documented |
| User | `$HOME/.agents/skills` | documented |
| User | `$HOME/.codex/skills` | **undocumented; WSL discovery unverified** |
| System | Bundled by OpenAI | documented |

The `$HOME/.codex/skills` row is absent from the official page but earlier evidence for its discovery came from a retired Windows host. Discovery on WSL is unverified. Express the path as `$HOME/.codex/skills`, and check it in the target runtime before relying on it. Treat the official list as incomplete evidence, not as grounds to reject this path. It sits next to `~/.codex/agents/`, where agent TOMLs live, so a Codex user who keeps both under `~/.codex/` has one coherent tree.

When generating install instructions, name `$HOME/.codex/skills` for personal skills unless the user has said otherwise, and `.agents/skills` for repository-scoped skills that travel with a project.

For context efficiency Codex first loads only each skill's name and description. That listing is capped at 2% of the model's context window, or 8,000 characters when the context window is unknown; the full `SKILL.md` loads only once a skill is selected, regardless of that budget. A skill has three invocation paths: `/skills` or a `$name` mention in the CLI and IDE, direct selection in the app, and implicit matching of the prompt against the skill's `description`. That last path is why a skill's `description` must state a clear, assertive trigger scope. `agents/openai.yaml` carries presentation metadata and `allow_implicit_invocation` (default `true`) for skills that should never fire on their own.

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

Codex can schedule recurring background tasks that add findings to the inbox, or archive themselves when there is nothing to report. Automations take three shapes: standalone automations that start fresh runs on a schedule and report into Triage; project automations, which require the app to be running and the selected project to be available on disk; and thread automations, heartbeat-style recurring wake-ups attached to the current thread. Scheduling accepts predefined daily and weekly slots, custom cron syntax, and minute-based intervals for active follow-up loops.

Two operational cautions belong in any prompt that sets one up: on a Git repository an automation runs either in the local project or on a dedicated background worktree, and frequent schedules accumulate worktrees over time; and in read-only sandbox mode, tool calls fail when they need to modify files, use the network, or work with apps.

## Caveats

Goal lifecycle and subagent guidance refreshed on 25 September 2026. CLI composer evidence has its own date above. Remaining historical sections were verified on 24 July 2026 and require live refresh before use. Historical defaults are not current dispatch authority: the `agents.max_depth` (1) and `agents.job_max_runtime_seconds` (1800) defaults (the former `agents.max_threads` (6) default is superseded; see Subagents); the 32 KiB / 65536-byte `project_doc_max_bytes` bounds; the 2%-or-8,000-character skill listing budget; and the `codex-cli` 0.128.0 requirement for goals are current published values and should be re-checked before being depended on.

Goals, `spawn_agents_on_csv`, and the agent-team-style batch flow are all marked experimental and may change. The `features.goals` key did not appear in the visible portion of the configuration reference, which is truncated on fetch; the two enabling paths cited above come from the Goals use-case page. `features.memories` exists and is off by default, but Codex's memory documentation redirects off the developer docs domain, so this pack makes no claim about how memories interact with `AGENTS.md` — treat that as unverified.

## Sources

- [Follow a goal | Codex use cases](https://learn.chatgpt.com/use-cases/follow-goals)
- [Using Goals in Codex (Cookbook)](https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex)
- [Subagents – Codex](https://developers.openai.com/codex/subagents)
- [Agent Skills – Codex](https://learn.chatgpt.com/docs/build-skills)
- [Custom instructions with AGENTS.md – Codex](https://developers.openai.com/codex/guides/agents-md)
- [Configuration Reference – Codex](https://developers.openai.com/codex/config-reference)
- [Slash commands – Codex CLI](https://developers.openai.com/codex/cli/slash-commands)
- [Automations – Codex app](https://developers.openai.com/codex/app/automations)

## Managed task-selected authority roles

The orchestrator renders model-neutral definitions that preserve role authority, grants and contracts. Its `scripts/render_agents.py --check` checks projection consistency, not serving identity. The canonical capability policy registers the roles and supports explicit task controls. An existing ID that names a model or an effort is a compatibility label only. The orchestrator selects every actual task pair, and it verifies the loaded definitions, the controls and the effective permissions. Main-session configuration remains external. A planner draft stays advisory, and the parent owns the durable plan. No source check proves installation, loaded registration or model obedience.
