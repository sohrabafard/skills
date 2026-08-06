# Skill Trigger Syntax by Agent Family

Choose the trigger from the runtime that will execute the prompt, not from the authoring environment.

## The rule

| Runtime | Models in scope | Pack syntax |
|---|---|---|
| Codex app/CLI | GPT-5.6 (`sol`, `terra`, `luna`) | `$skill-name` |
| Claude Code | Opus 5, Sonnet 5, Fable 5 | `/skill-name` |

Opus 4.8 is retired from this pack's scope. A session still running it takes the Claude Code column unchanged — trigger syntax is a harness property, not a model property.

## Why both exist, and the one nuance worth knowing

Codex registers skills on both surfaces: `$name` in a prompt and `/skills` for the browser. This pack keeps `$name` for Codex for consistency and mixed-runtime readability. Do not rewrite existing Codex-facing `$name` references to `/name`.

Claude Code merged custom commands into skills, so `.claude/commands/deploy.md` and `.claude/skills/deploy/SKILL.md` both produce `/deploy`. Either form is a valid target for a `/name` trigger.

## Practical checklist when writing a prompt for another agent

1. Identify the target runtime; ask if it cannot be inferred safely.
2. Apply one syntax consistently within each runtime-specific section.
3. In mixed prompt packs, switch syntax section by section.
4. Read the target skill's registered name instead of guessing it. In Claude Code the command name comes from the skill's directory or file name for personal and project skills, while plugin skills resolve under their namespaced form (`/plugin-name:skill-name`), where the frontmatter `name` sets only the last segment. In Codex, read the `name:` frontmatter field.
5. Prefer the namespaced form for plugin skills even where a bare alias also resolves. The bare alias is conditional — it works only while no other command claims that name — so it is the wrong thing to hard-code into a generated prompt.
6. Syntax is necessary but not sufficient — a trigger only activates when placed correctly. Apply `references/06-invocation-and-composition.md` for placement, role consistency, and goal splitting.

## Caveats

Verified against live documentation on 24 July 2026. Time-sensitive: the plugin bare-alias fallback in Claude Code is version-gated behavior that changed within the current release line, so treat `/plugin-name:skill-name` as the only stable form. The in-scope model list moves with each release; re-check `references/90-model-selection.md` and the live model pages before treating this table as current.

## Sources

- [Extend Claude with skills](https://code.claude.com/docs/en/skills)
- [Agent Skills – Codex](https://developers.openai.com/codex/skills)
- [Slash commands – Codex CLI](https://developers.openai.com/codex/cli/slash-commands)
- [Model configuration – Claude Code](https://code.claude.com/docs/en/model-config)
