# Consumer surfaces and prerequisites

Read this for host import, registration, invocation, or discovery.
Refresh the cited host documentation when versions or mechanisms differ.
Portable `SKILL.md` uses only `name` and `description` frontmatter.
`agents/openai.yaml` is OpenAI interface metadata, not an executable specialist or permission grant.
Extracting these native templates installs nothing.

## Locations and invocation

Use these destinations only for explicitly authorized setup; preserve unrelated configuration and resolve name conflicts before writes.
Templates are under `assets/specialist/`.

| Host | Skill directory | Agent template → destination |
| --- | --- | --- |
| Local Codex | `.agents/skills/alaa-ent-go-orm-db/` or `~/.agents/skills/alaa-ent-go-orm-db/` | `codex/alaa-ent-specialist.toml` → `.codex/agents/alaa-ent-specialist.toml` or `~/.codex/agents/alaa-ent-specialist.toml` |
| Claude Code | `.claude/skills/alaa-ent-go-orm-db/` or `~/.claude/skills/alaa-ent-go-orm-db/` | `claude/alaa-ent-specialist.md` → `.claude/agents/alaa-ent-specialist.md` or `~/.claude/agents/alaa-ent-specialist.md` |

Invoke the skill through the supported Codex picker or `$alaa-ent-go-orm-db`, or the observed Claude Code command, ordinarily `/alaa-ent-go-orm-db` for this layout.
Keep automatic discovery enabled unless the user changes it.
ChatGPT and Claude chat/API require their own supported skill import and invocation mechanisms; these local agent files do not establish hosted agent registration.
Without Skills support, explicitly reading `SKILL.md` and triggered references permits manual application, not native-agent claims.

## Codex

Current standalone agent TOML requires `name`, `description`, and `developer_instructions`; no extra `[agents.<name>]` registration is needed for that mechanism.
The configuration reference also documents `agents.<name>.config_file` role layers: verify the target schema before adapting to that mechanism; do not assume identical file formats.
There is no documented Claude-style preload here; `skills.config` is not a preload.
The wrapper explicitly reads canonical sources.

Custom agents inherit parent permissions, provider, and MCP servers.
Agent-local `sandbox_mode` does not enforce a separate read-only sandbox.
Inspect effective tools and use approved parent controls; prose cannot enforce an unavailable restriction.

## Claude Code

The Markdown adapter preloads `alaa-ent-go-orm-db` through `skills`, then verifies its readable canonical source.
The scoped tool list supports local implementation, checks, and documentation retrieval and omits Agent.
Model, effort, permission mode, memory, hooks, and MCP configuration remain unset; effective host permissions and user authority still apply.
A missing or disabled preload may be skipped, so successful creation alone does not verify loading.

The supplied preload targets personal/project installation.
A plugin conversion must resolve actual scoped agent and skill IDs; skill commands use `/plugin-name:skill-name`.
Verify the accepted preload identifier and effective load before changing it; do not guess namespaces or rely on colliding short aliases.
This package supplies no plugin manifest.

## Verify discovery

Read the active host/version, role definition, effective tools, and canonical source without writes.
Inspect the host's exposed role roster and loaded definition; use its skill picker for skill discovery.
Claude Code `/agents` behavior varies by version and may show instructions rather than a role list.
Dispatch to the exact observed `alaa-ent-specialist` identity or verified scoped ID with [85-specialist-delegation.md](85-specialist-delegation.md)'s lane facts.
Verify the specialist loaded the expected canonical source and triggered references before dependent work.
Missing roles, disabled skills, unreadable references, or stale definitions block that dispatch; report the gap without auto-installation, permission changes, or a disguised generic fallback.

Existing Alaa orchestrators may additionally require role catalog, capability policy, and installer admission.
Read their accessible current contracts when invoked; host discovery alone does not satisfy those gates, and this package changes none.

## Prerequisites and evidence limits

Readable schema/query context and current source access support design and review.
Generation needs Go, modules, and project source; database checks need an authorized target matching the PostgreSQL major version and representative synthetic fixtures.
Verify Atlas capabilities before use; paid features are optional.
The optional baseline helper needs Python 3.10+; manual inspection remains supported.
Delegation requires an exposed native role and required tools.
Static parsing verifies structure only; claim discovery or invocation only after observing it on the target host.

Host sources checked 2026-11-05: [OpenAI subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), [configuration](https://learn.chatgpt.com/docs/config-file/config-reference), [skills](https://learn.chatgpt.com/docs/build-skills), [Claude Code subagents](https://code.claude.com/docs/en/sub-agents), [skills](https://code.claude.com/docs/en/skills).
