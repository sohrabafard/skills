# Skill Trigger Syntax by Agent Family

Choose the trigger from the runtime that will execute the prompt, not from the authoring environment.

## The rule

| Runtime | Models in scope | Pack syntax |
|---|---|---|
| Codex app/CLI | GPT-5.6 | `$skill-name` |
| Claude Code | Opus 4.8, Sonnet 5, Fable 5 | `/skill-name` |

## Why both exist, and the one nuance worth knowing

Codex may also register skills as slash commands, but this pack keeps `$name` for Codex consistency and mixed-runtime readability. Do not rewrite existing Codex-facing `$name` references to `/name`.

## Practical checklist when writing a prompt for another agent

1. Identify the target runtime; ask if it cannot be inferred safely.
2. Apply one syntax consistently within each runtime-specific section.
3. In mixed prompt packs, switch syntax section by section.
4. Read the target skill's `name:` frontmatter instead of guessing its registered name.
