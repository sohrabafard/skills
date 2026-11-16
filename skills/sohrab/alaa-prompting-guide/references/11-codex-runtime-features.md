# Codex Runtime Features

These are features of the Codex app and CLI, not model behavior. Read only the section you need. `references/12-gpt-6.md` holds model and API guidance.

## Rejected tool input or patch context

Grounded in active host schemas inspected 18 October 2026. Recheck the executing host; never copy a remembered tool signature.

- **Before you repair a rejected call, read the active host's tool schema.** JavaScript orchestration, shell-command arguments, structured objects and patch text are different input contracts. Keep each language in its declared input. An API example does not establish the host's schema.
- **Patch-context mismatch:** inspect the current target region and the scoped diff, including other owners' edits. Rebuild the smallest patch that matches that state.
- **Duplicate-operation error:** combine or split operations only as the active patch contract permits.
- **A mutation may have occurred:** reconcile the actual state before you retry. Never blindly replay an uncertain write.
- **Process, shell, path or sandbox failure:** route it to `/alaa-codex-runtime-ops`. This section owns only schema and context mistakes.
- Neither diagnosis authorizes a settings change or broader writes. Use the active repair and retry budget. When the required contract or the safe resulting state stays unknown, report the exact blocker and stop the dependent operation.

## `/goal` — persistent objective mode

A Goal is durable, thread-scoped state that keeps a Codex thread working toward one outcome across turns. Codex stops when evidence makes it fairly confident that the stop condition is met, when it hits its budget, or when it is blocked. A budget limit is not completion.

**Activation.** Use the goal tool or command of the current host only when the user explicitly requests an objective loop; ordinary implementation work activates none. Read that host's goal tool schema for lifecycle, budget and blocked-state rules. Report an unavailable capability; write no remembered feature flag or version gate into configuration.

**A strong Goal defines seven things:** the outcome, the verification surface, the constraints that must not regress, the boundaries, the iteration policy, the blocked stop condition with what would unblock it, and an explicit turn or time cap.

```text
/goal <desired end state> verified by <specific command, test, or artifact>, while preserving <what must not regress>.
Use only <allowed files, tools, or boundaries>. Between iterations, <how Codex should pick the next action>.
If blocked or no valid path remains, report exactly what is blocking progress and what would unblock it.
Stop after <turn or time cap> even if incomplete, reporting progress, evidence so far, and the next step.
```

Write one objective, one stop condition and one validation loop. Size a goal larger than one prompt and smaller than an open-ended backlog.

**CLI composer and objective storage.** Verified 3 November 2026 against installed `codex-cli 0.163.0` and its tagged source:

- The TUI accepts a leading `/goal` with a multiline objective in one composer message ([test](https://github.com/openai/codex/blob/rust-v0.163.0/codex-rs/tui/src/chatwidget/tests/goal_validation.rs#L78)).
- The protocol caps the stored objective at **4,000 Rust characters**, `str::chars().count()` ([source](https://github.com/openai/codex/blob/rust-v0.163.0/codex-rs/protocol/src/protocol.rs#L4207)).
- Above the cap, the TUI writes the full objective to `goal-objective.md` and stores a short file reference ([source](https://github.com/openai/codex/blob/rust-v0.163.0/codex-rs/tui/src/goal_files.rs#L121)).
- The CLI source establishes neither Desktop composer behavior nor the limits of the active goal tool. Verify the target host and input path before you depend on the file route.

**This is not Claude Code's `/goal`.** Never carry a `/goal` block between the runtimes unedited. `references/41-claude-code-runtime-features.md` states how the two differ in what proves completion, how each is enabled and what each costs.

## Subagents

**Authority.** Delegate only within authorization granted by the user or an applicable instruction. A prompt can authorize concrete independent lanes; it cannot enable an unavailable runtime feature. The host's current collaboration tools define roles, nesting, concurrency, inheritance and waiting. Copy no default or tool name from another Codex surface.

**Definitions.** To write a custom agent TOML, read `references/80-subagent-authoring.md`; it owns the directories and keys. A definition created in the repository does not prove that the current session loaded it.

**Pin precedence** (verified 9 October 2026):

1. A model or effort pin in the custom TOML wins over spawn arguments.
2. With both pins omitted, explicit spawn controls precede global agent defaults and parent settings.

Managed authority roles omit both pins, so supply BOTH task controls on a verified compatible spawn surface. An inherited value is not a task decision. A full-history fork can forbid overrides in the active host. Neither prose nor a disk edit changes a stale loaded pin: use an available exact verified realization or block the affected lane. The policy JSON records a dated supported-effort snapshot; verify availability on the dispatch host.

**Concurrency.** `agents.max_concurrent_threads_per_session` caps the spawned-agent threads open at once, excluding the primary thread. `agents.max_threads` is its legacy alias. When the key is unset, Codex chooses the default; neither source states a number. Verified 14 November 2026 against [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) and the [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference).

**Sandbox.** A subagent inherits the parent sandbox policy and runtime overrides.

- A `read-only` TOML value does not prove that every capability is read-only. The server-side effects of an MCP tool are outside native sandbox enforcement.
- Before you claim a read-only boundary, inspect the effective native permissions, the parent overrides and the MCP tool grants, and restrict or withhold mutation-capable tools.
- Change no installed configuration without authority.
- In `workspace-write`, these paths stay read-only inside a writable root, recursively: `.git`, whether it is a directory or a pointer file, together with the Git directory a pointer file names; and the directories `.agents`, `.codex` and `.aws` when they exist. The page does not say how `git commit` is handled. Verified 14 November 2026 against [Sandbox and approvals](https://learn.chatgpt.com/docs/agent-approvals-security).

**Identity.** To report a subagent's model and effort, read `references/80-subagent-authoring.md` *Configuration and observed identity*.

## `spawn_agents_on_csv` — background batch jobs

An experimental tool that spawns one worker per CSV row from an instruction template with `{column_name}` placeholders, and exports the combined results to an output CSV. Parameters: `csv_path`, `instruction`, `id_column`, `output_schema`, `output_csv_path`, `max_concurrency`, and `max_runtime_seconds`, which overrides `agents.job_max_runtime_seconds` per call.

Each worker **must call `report_agent_job_result` exactly once**; a worker that exits without it produces an error row. Make that call an explicit, unconditional final step of every instruction template, on the failure path too.

## `AGENTS.md`

For the resolution order, the `project_doc_max_bytes` limit, the fallback filenames and the write-back rule, read `references/70-agent-instruction-files.md` *Nesting and precedence*. For authoring, read the rest of that file.

## Agent Skills

To write a Codex skill, its install instructions or its description, read `references/61-skill-platform-mechanics.md`; it owns the discovery scopes, the install default, the listing budget and the frontmatter keys. `references/06-invocation-and-composition.md` owns the invocation paths.

## Session-shaping slash commands

Name the command in a generated operating prompt; do not leave it to the operator: `/plan`, `/review`, `/experimental` (toggles optional features, including subagents and goals), `/fork`, `/side` or `/btw`, `/personality`, `/compact`, `/model`, `/permissions`, `/status`, `/approve`, `/new`, `/resume`. A `/plan` gate followed by a `/goal` is the Codex plan-then-autonomy pattern: approve the approach, then hand the thread a bounded objective.

## Automations

Put two cautions in a prompt that sets up a scheduled Codex task:

- On a Git repository an automation runs in the local project or on a dedicated background worktree, and a frequent schedule accumulates worktrees.
- In read-only sandbox mode, a tool call fails when it must modify files, use the network or work with apps.

## Caveats

- Goal lifecycle and subagent guidance were refreshed 25 September 2026. Sections with no later date were verified 24 July 2026 and need a live refresh before use.
- Historical defaults, not dispatch authority; re-check each before you depend on it: `agents.max_depth` (1), `agents.job_max_runtime_seconds` (1800), and the `codex-cli` 0.128.0 requirement for goals. The former `agents.max_threads` default (6) is superseded; see Subagents.
- Goals, `spawn_agents_on_csv` and the batch flow are experimental.
- The `features.goals` key did not appear in the visible, truncated portion of the configuration reference; the enabling paths come from the Goals use-case page.
- `features.memories` exists and is off by default. How memories interact with `AGENTS.md` is unverified.

## Sources

- [Follow a goal | Codex use cases](https://learn.chatgpt.com/use-cases/follow-goals)
- [Using Goals in Codex (Cookbook)](https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex)
- [Subagents – Codex](https://developers.openai.com/codex/subagents)
- [Agent Skills – Codex](https://learn.chatgpt.com/docs/build-skills)
- [Custom instructions with AGENTS.md – Codex](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Configuration Reference – Codex](https://developers.openai.com/codex/config-reference)
- [Slash commands – Codex CLI](https://developers.openai.com/codex/cli/slash-commands)
- [Automations – Codex app](https://developers.openai.com/codex/app/automations)

## Managed task-selected authority roles

- The orchestrator renders model-neutral definitions that preserve role authority, grants and contracts. Its `scripts/render_agents.py --check` checks projection consistency, not serving identity.
- The capability policy registers the roles and supports explicit task controls. An existing ID that names a model or an effort is a compatibility label only.
- The orchestrator selects every task pair, and it verifies the loaded definitions, the controls and the effective permissions. Main-session configuration stays external.
- A planner draft stays advisory, and the parent owns the durable plan.
- No source check proves installation, loaded registration or model obedience.
