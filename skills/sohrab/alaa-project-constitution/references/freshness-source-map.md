# Freshness Source Map

Use live authoritative sources when a constitution or generation prompt makes concrete,
version-sensitive claims. Repository truth remains authoritative for the project's current
behavior; external docs establish current vendor/runtime capabilities and standards.

## OpenAI and Codex

- GPT-5.6 model and prompting guidance:
  <https://developers.openai.com/api/docs/guides/latest-model>
- Codex prompting:
  <https://developers.openai.com/codex/prompting>
- Codex AGENTS.md discovery and precedence:
  <https://learn.chatgpt.com/docs/agent-configuration/agents-md>
- Codex skills:
  <https://learn.chatgpt.com/docs/build-skills>

Current durable implications:

- Start with an outcome, useful context, output needs, and material boundaries.
- Prefer the smallest prompt and tool set that reliably meets evaluated success criteria.
- State autonomy/permission boundaries and required evidence explicitly.
- Codex automatically loads applicable AGENTS.md; a separate constitution needs an explicit
  AGENTS.md read rule.
- Skills use progressive disclosure; keep SKILL.md procedural and move detail to references.

## Anthropic and Claude Code

- Prompting best practices:
  <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices>
- Claude Opus 4.8:
  <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-4-8>
- Claude Sonnet 5:
  <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5>
- Claude Fable 5:
  <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5>
- Claude Code memory/CLAUDE.md imports:
  <https://code.claude.com/docs/en/memory>
- Claude Code skills:
  <https://code.claude.com/docs/en/skills>

Current durable implications:

- Use clear, explicit instructions and explain context that changes the decision.
- Use structured steps only when order/completeness matters; avoid unnecessary scaffolding.
- CLAUDE.md can import the constitution via `@relative/path`.
- Keep CLAUDE.md concise and conflict-free; imported content consumes startup context.
- Claude Code skills and Codex skills share the open Agent Skills structure but have
  runtime-specific invocation and metadata behavior.

## Freshness rule for generated constitutions

Do not copy volatile model names, prices, token limits, version gates, framework versions,
browser thresholds, security standards, or vendor behavior into binding policy from memory.
Verify the current official page when the fact materially affects a rule. Cite or record the
source path and verification date. If live verification is unavailable, preserve bounded
uncertainty or a TODO rather than presenting the claim as current.

