# Runtime evidence for task-specific selection

Researcher: alaa-researcher, configured Sol/medium, observed identity unknown. Retrieved2026-10-09; no model calls.

- [Codex custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents): custom-file model/effort pins win over spawn arguments. Omitting both permits explicit spawn values before global agent defaults and parent settings. Therefore reusable role authority can be model-neutral. Current chat role schema still fixes all named roles; editing disk cannot reload that registry. Full-history forks prohibit explicit overrides in this host.
- [Claude subagents](https://code.claude.com/docs/en/sub-agents): invocation model overrides YAML except effective force/environment/hook/provider rules. Since2.1.292, non-fork per-invocation effort overrides YAML and persists on resume; CLAUDE_CODE_EFFORT_LEVEL supersedes both. Existing local no-per-call-effort assumption is stale.
- [Claude CLI](https://code.claude.com/docs/en/cli-reference): --agent, --model, --effort and --agents are session controls. Separate sessions need context/permission handling and are not an automatic substitute for in-process specialist dispatch.

Permissions remain separate: parent sandbox/permission overrides and MCP/shell capability can affect effective enforcement. Removing model pins neither establishes read-only enforcement nor changes the role contract. Source compatibility, registration, actual controls, account access and observed serving identity are different claims.

Inference adopted: model-neutral roles plus mandatory explicit task controls avoid role-by-model duplication. If the actual host lacks compatible controls, exact registered realization or a blocked affected lane is required; no silent fallback. Official selector and model capability evidence from the earlier same-day archive remain reference inputs, not role-specific defaults.
