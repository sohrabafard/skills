# Codex Runtime Features (the environment GPT-5.5 runs inside)

These are product/harness features of the Codex app and CLI, not raw model behavior — they matter whenever a prompt targets GPT-5.5 running in Codex rather than the bare API. Read `references/10-gpt-5-5.md` first for model-level tuning, then use this file for the feature the task actually needs.

## `/goal` — persistent objective mode

A Goal is durable, thread-scoped state that keeps a Codex thread working toward one defined outcome across many turns instead of stopping after a single reply. Continuation only happens when the thread is idle, the goal is active, budget remains, and no user input is queued; **evidence, not speculation, determines completion.** Codex works in checkpoints, keeps a short progress log, and can run independently for hours. It stops when it is confident the stopping condition is verifiably met, when it hits a budget limit, or when it is genuinely blocked — in the last two cases it reports progress and blockers instead of claiming success.

A strong Goal defines six things: **outcome** (what should be true when work concludes), **verification surface** (the test/benchmark/artifact/log that proves it), **constraints** (what must not regress), **boundaries** (which files/tools/resources are in play), **iteration policy** (how Codex picks the next action after each attempt), and **blocked stop condition** (when to halt and what would unblock it).

**Must be enabled first**: Goals are disabled by default. Enable with `[features]\ngoals = true` in `~/.codex/config.toml`, or `codex features enable goals` from the CLI. Manage the lifecycle with `/goal` (view current objective/status), `/goal pause`, `/goal resume`, `/goal clear`.

### Ready-to-use `/goal` template

```text
/goal <desired end state> verified by <specific command, test, or artifact>, while preserving <what must not regress>.
Use only <allowed files, tools, or boundaries>. Between iterations, <how Codex should pick the next action>.
If blocked or no valid path remains, report exactly what is blocking progress and what would unblock it.
```

For a full worked example (package clean-code pass, explicit subagent/parallel/background authorization, mandatory self-review before declaring done, step-by-step Conventional Commits with no co-author trailer) see this pack's own prior art in a running Codex session, or build one fresh from `references/10-gpt-5-5.md` plus the template above — state one objective, one stopping condition, and a validation loop; a good goal is bigger than one prompt but smaller than an open-ended backlog.

## Subagents — explicit delegation and parallel spawning

Codex only spawns subagents when explicitly asked — it never fans out on its own. Built-in roles: `default` (general fallback), `worker` (execution-focused), `explorer` (read-heavy codebase search). Custom agents can be defined as TOML files in `~/.codex/agents/` (personal) or `.codex/agents/` (project), with required `name`, `description`, `developer_instructions`, and optional `model`, `sandbox_mode`, `mcp_servers`. When several agents run concurrently, the parent orchestrates, waits for all requested results, and consolidates them into one summary.

Config lives under `[agents]` in `~/.codex/config.toml`: `max_threads` (concurrent open agent threads, default 6), `max_depth` (nesting depth, default 1 — one level of direct child spawning, no deep recursive fan-out).

```text
Explicit authorization: you may use subagents and run independent work in parallel for this task without asking
again. Spawn one agent per independent file/module/lane, wait for all of them, and reconcile the results yourself
before moving on. Give every subagent the same constraints and a clearly scoped slice so nothing is duplicated
or dropped.
```

## `spawn_agents_on_csv` — background batch jobs

An experimental tool for many similar tasks that map one-to-one to rows: Codex reads a CSV, applies an instruction template with `{column_name}` placeholders per row, spawns one worker per row, waits for the batch, and exports combined results (including `job_id`, `status`, `result_json`, `errors`) to an output CSV. Each worker must call `report_agent_job_result` exactly once; a worker that exits without reporting gets an error row instead of hanging the batch. Per-worker timeout defaults to `job_max_runtime_seconds` (config, falls back to 1800s) unless overridden per call.

```text
spawn_agents_on_csv with csv_path="tickets.csv", instruction="Investigate ticket {ticket_id} about {summary}
and propose a fix; report your finding.", output_csv_path="ticket_results.csv", id_column="ticket_id",
max_concurrency=4
```

## `AGENTS.md` — durable project instructions

Codex reads a resolved `AGENTS.md` chain automatically at session start: global (`~/.codex/AGENTS.override.md` or `~/.codex/AGENTS.md`) plus project-scoped files walked from the project root down to the current working directory, closer files overriding/adding to more global ones. `project_doc_max_bytes` caps total size read (32 KiB default). No manual invocation is needed — but a prompt can still explicitly tell Codex to *update* `AGENTS.md` when a correction should persist, since Codex does not do that unprompted.

## Agent Skills

Skills package instructions/resources/scripts into a directory (`SKILL.md` + optional `scripts/`, `references/`, `assets/`, `agents/openai.yaml`) so Codex can follow a workflow reliably — this skill is one. Codex discovers skills in `.agents/skills` (cwd), the repo root, `~/.agents/skills`, and system locations. For context efficiency it first loads only each skill's name+description (capped at 8,000 characters or 2% of context) and loads the full body only once a skill is actually selected. Trigger explicitly with `/skills` or a `$name` mention, or implicitly by describing a task that matches a skill's description — which is why a skill's `description` field should state a clear, assertive trigger scope.

## Caveats

The `codex-cli >= 0.128.0` version number attached to the goals feature flag came from a secondary/unofficial source and was not confirmed on an official page — verify against `codex features list` or current docs before depending on it. No dedicated ad hoc slash command for single-subagent spawning was found beyond natural-language delegation and the CSV batch tool.

## Sources

- [Follow a goal | Codex use cases](https://developers.openai.com/codex/use-cases/follow-goals)
- [Using Goals in Codex (Cookbook)](https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex)
- [Subagents – Codex](https://developers.openai.com/codex/subagents)
- [Agent Skills – Codex](https://developers.openai.com/codex/skills)
- [Custom instructions with AGENTS.md – Codex](https://developers.openai.com/codex/guides/agents-md)
- [Configuration Reference – Codex](https://developers.openai.com/codex/config-reference)
