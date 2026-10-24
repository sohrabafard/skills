# Source Map

## Introduction

Source priority and freshness guide context and output policy. Runtime, shell, and model behavior can change.

Read this file when context or output policy depends on current runtime behavior, shell behavior, or model guidance.

## Source priority

1. The user's requested output shape, especially any explicit request for raw logs, full diffs, or full file contents.
2. Repo-local instruction files (`AGENTS.md`, `CLAUDE.md`), active plan or state artifacts, and the current worktree.
3. This skill: `SKILL.md`, then `references/noise-control-patterns.md`, `references/model-output-profiles.md`, and `references/workflow-integration.md`.
4. Official documentation for the runtime in use:
   - Claude Code: https://code.claude.com/docs/
   - Codex: https://developers.openai.com/codex/
5. Official documentation for the command surface in use:
   - PowerShell: https://learn.microsoft.com/powershell/
   - Git: https://git-scm.com/docs
   - ripgrep: https://github.com/BurntSushi/ripgrep
6. Official prompting and skill guidance when model behavior affects output policy:
   - Anthropic prompting: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
   - Anthropic skill authoring: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
   - OpenAI model guidance: https://developers.openai.com/api/docs/guides/latest-model
   - OpenAI skills: https://developers.openai.com/codex/skills/
7. Community posts, StackOverflow answers, and issue comments only for troubleshooting a concrete shell or tool failure.

## Freshness triggers

Re-check current behavior when the task mentions:

- The latest Claude Code or Codex release, or new tool, terminal, PowerShell, Bash, or Windows behavior.
- Very large generated logs, new validation runners, or new output caps.
- A model change affecting reasoning, verbosity, narration, tool eagerness, or delegation polarity. First read `references/model-output-profiles.md`. For a model newer than that file, re-verify it against vendor documentation.
- Subagent fan-out that could flood the parent's context.
- Context-window, compaction, or caching behavior. These change the actual cost of a long tool result.

## Standing policy

- Start with the smallest instruction set that reliably preserves task quality. Add a rule only for a demonstrated gap.
- Repetition costs context without raising compliance.
- Prioritize required facts, evidence, caveats, validation, blockers, and next steps before trimming repetition or optional background. Generic brevity instructions suppress required artifacts first.
- Treat fewer tokens, calls, or turns as improvements only when final output still meets its quality bar.
- State the desired output shape positively and explicitly. Avoid model-specific rituals and repeated phrasing.
- Keep bounded reads, reviewable edits, and validation evidence with newer models. Greater capability does not remove this discipline.

## Domain-bounded anti-patterns

**Pasting a 2,000-line validation log to prove a command ran:** Capture it in a repo-local artifact when useful. Read the failing slice. Report the command, result, and path.

**Reading six full files to answer a question about one function:** Search for the symbol. Read the bounded range around it, then stop.

## Caveats

- The URLs above are current documentation entry points and can change. If one returns 404, navigate from the vendor's documentation root instead of guessing a path.
- Claude Code and Codex behavior diverges between releases. Verification on one runtime does not automatically apply to the other.
- `/alaa-prompting-guide` owns model and runtime claims. The `references/model-output-profiles.md` file routes there and defines no copied model policy.

## Sources

- [Claude Code documentation](https://code.claude.com/docs/)
- [Codex documentation](https://developers.openai.com/codex/)
- [Prompting best practices (Claude family)](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [Agent Skills best practices (Anthropic)](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Using the latest model (OpenAI)](https://developers.openai.com/api/docs/guides/latest-model)
- [Skills (Codex)](https://developers.openai.com/codex/skills)
