# Model and Runtime Compatibility

Use this file only when creating/updating skills, prompts, runtime harness instructions, or model-selection guidance. Do not load it for ordinary observability design.

## Portable skill contract

- Keep each skill as a directory containing `SKILL.md`.
- Use YAML frontmatter with portable fields: `name` and `description` only unless a specific runtime requires a platform-specific fork.
- Keep `name` lowercase hyphenated and matching the directory name.
- Front-load the `description` with the main trigger terms because Codex and Claude may decide invocation from the description alone.
- Keep `SKILL.md` under 500 lines and move long details to `references/`.
- Reference files by relative path; do not assume external files are loaded unless the skill tells the agent when to load them.
- Put machine-checkable rules, boundaries, and output contracts in the skill. Put long examples, schema notes, and source maps in references.

## GPT-5.5 / Codex guidance

- Prefer outcome-first instructions: goal, success criteria, constraints, evidence rules, validation, output contract, and stop rules.
- Avoid process-heavy step stacks unless the exact order is a true product requirement.
- Reserve `must`, `always`, and `never` for platform invariants, safety rules, required output fields, or irreversible side effects.
- Add retrieval budgets for current/domain facts: one broad official search first; search again only when core evidence is missing, exhaustive coverage is requested, or a specific artifact must be read.
- For multi-step/tool-heavy work, start with a short user-visible preamble/update when the runtime supports it.
- Validate work when possible; if validation cannot run, state why and the next best check.
- Default reasoning can start at medium; evaluate lower effort for latency-sensitive workflows and escalate only when task difficulty/evals justify it.
- Use concise `agents/openai.yaml` metadata. Keep `short_description` tight because skill catalogs can truncate.

## Claude Opus 4.8 / Sonnet 5 / Fable 5 guidance

- Claude Code skills can be invoked explicitly or loaded automatically from descriptions; descriptions must clearly state both what the skill does and when to use it.
- Keep portable shared skills free of Claude-only frontmatter such as `context: fork` unless the skill is explicitly a Claude-only fork and the task justifies subagent isolation.
- Opus 4.8 is appropriate for complex agentic/coding work; use high or xhigh effort only when workload importance and latency/cost permit it.
- Sonnet 5 is a strong speed/intelligence option. Recount prompt/output budgets when migrating because tokenization and adaptive thinking behavior can differ from earlier Sonnet versions.
- Fable 5 is for long autonomous sessions and very high capability needs. The harness, not the skill, must check data-retention/ZDR eligibility, safety-classifier behavior, and fallback policy before routing sensitive work to Fable.
- Do not request hidden chain-of-thought. Ask for concise findings, assumptions, validation evidence, and uncertainty instead.

## Cross-model writing rules

- State the safest assumption instead of asking broad questions when the task can progress safely.
- Ask only the smallest question when missing information would materially change security, privacy, production side effects, or schema compatibility.
- Separate source-backed facts from recommendations. Use placeholders instead of invented customers, metrics, dates, table names, or retention commitments.
- Require official-source freshness checks for current/niche facts, especially model capabilities, SigNoz schemas, OpenTelemetry semantic conventions, Sentry OTLP behavior, and Vector sink maturity.
- Never authorize destructive production changes, secret exposure, data deletion, `git push`, deploy, or external SOC/SIEM egress without explicit user/operator permission.

## Compatibility smoke tests

Use these prompts after editing a skill:

1. “Which skill should handle a p99 latency dashboard query in SigNoz ClickHouse?” Expected: `alaa-signoz-clickhouse-docs`, with `alaa-observability-soc` only for signal design.
2. “Review this service’s observability for production readiness.” Expected: `alaa-observability-soc`, security-sensitive checklist loaded.
3. “Can I add `user_id` as a metric label?” Expected: reject as high-cardinality/sensitive; suggest trace/log attribute with redaction policy.
4. “Update this skill for GPT-5.5 and Claude Sonnet 5.” Expected: load this compatibility reference and preserve portable skill format.
