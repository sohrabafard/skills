# Consumer surfaces and prerequisites

This is one portable Agent Skill with only `name` and `description` frontmatter.
`agents/openai.yaml` supplies optional OpenAI interface metadata. It is neither a subagent definition nor a permission grant.
No model, effort, host tool grant, MCP server, or private Alaa dependency is pinned.

## Surface-specific use

| Surface | Consumer behavior |
| --- | --- |
| Codex CLI / IDE | Use a supported skill location under existing installation authorization. Invoke `$alaa-ent-go-orm-db` or select it in the picker. |
| Claude Code, including Desktop Code | Use the installed registered command, normally `/alaa-ent-go-orm-db` for a personal/project skill. Plugin installation may add a namespace. |
| ChatGPT with Skills support | Use the host's import/installation flow and picker or registered `@` mention. Support depends on the host. |
| Claude chat / API with Skills support | Import through that surface's supported mechanism. Do not assume Claude Code commands, filesystem discovery, or shell access. |
| Agent without Skills support | Read `SKILL.md` and triggered references explicitly. This is manual application, not automatic discovery. |

Resolve the host before writing installation commands or invocation examples.
Do not assume a local skill is installed in ChatGPT or Claude chat.
Keep automatic discovery enabled unless the user changes that policy.
Automatic selection does not authorize sensitive execution.

Sources verified 2026-11-05: [Agent Skills specification](https://agentskills.io/specification), [OpenAI skills](https://learn.chatgpt.com/docs/build-skills), [Claude Code skills](https://code.claude.com/docs/en/skills).

## Execution prerequisites

- Design/review needs readable schemas and query context; changed volatile facts require browsing.
- Compilation/generation needs the supported installed Go toolchain, module dependencies, and project source.
- Database checks need authorized PostgreSQL matching the target major version and representative synthetic fixtures.
- Atlas operations need the installed edition's verified capabilities. Paid features are optional, never assumed.
- The optional baseline helper needs Python 3.10 or newer; equivalent manual inspection is supported.

The package installs no tools and provisions no database. It contains no DSNs, credentials, or production configuration.
Format validation proves neither discovery nor invocation. Report only exercised surfaces.
