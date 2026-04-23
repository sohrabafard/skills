# Source Map

Use this file when workflow guidance depends on current agent/runtime behavior, model selection, subagent availability, or execution-memory policy.

## Source priority

1. Explicit user instructions for the current task.
2. Repo-local `AGENTS.md`, active plan/state files, and current worktree state.
3. This skill's `SKILL.md`, `references/00-topic-map.md`, templates, and validators.
4. System/developer instructions for the active Codex surface and sandbox.
5. Official or primary documentation for the tool involved, such as:
   - OpenAI/Codex product instructions in the active environment.
   - Microsoft PowerShell docs: https://learn.microsoft.com/powershell/
   - Git docs: https://git-scm.com/docs
6. Community posts, StackOverflow answers, or forum threads only for troubleshooting a concrete error after the primary sources above are exhausted.

## Freshness triggers

Re-check the active environment or official docs when the task mentions:

- latest, current, today, GPT-5.5, new Codex surface behavior, model routing, or subagent behavior
- changed sandbox, approval, tool, shell, or browser-automation rules
- changed plan/state file layout or execution-memory conventions
- resuming after a long interruption, compaction, or parallel lane handoff

## GPT-5.5-ready use guidance

- Do not invent GPT-5.5-specific commands, syntax, file formats, or hidden capabilities.
- Treat newer model labels as a reason to preserve stronger planning discipline, not as a reason to skip durable state.
- For broad work, use higher reasoning to design cleaner phases and lane boundaries, then record the decisions in the same repo-local artifacts this skill already requires.
- When subagents are allowed, pass them bounded source artifacts and scope, not the parent agent's conclusions.

## Domain-bounded example

Good: a parent agent creates one parent plan, assigns read-only API/docs/runtime lanes, merges findings centrally, validates, and updates the state file before handoff.

Bad: each lane edits `docs/BIG_PICTURE.md` directly and the parent chooses the largest diff without reconciling source truth.
