# Skill Trigger Syntax by Agent Family

Every prompt in this skill's reference files that names a skill (its own or any other `alaa-*` / `$name` skill) must use the correct trigger character for the agent that will actually read the prompt. Getting this backwards is a real failure mode: a `$name` reference inside a Claude Code prompt is just inert text, not an invocation, and the same is true in reverse for a `/name` reference handed to a GPT/Codex agent that expects `$name`. Always look at which runtime will execute the prompt before writing the trigger character, not just which model.

## The rule

- **GPT-5.5 running in Codex (CLI or app):** trigger a skill with a leading `$`, for example `$alaa-prompting-guide`, `$alaa-workflow`, `$openai-docs`. This is the convention already used throughout this pack's `AGENTS.md` files and every other skill's cross-references, so keep new content consistent with it.
- **Claude Opus 4.8, Claude Sonnet 5, and Claude Fable 5 running in Claude Code:** trigger a skill with a leading `/`, for example `/alaa-prompting-guide`, `/alaa-workflow`. All three Claude models share one runtime (Claude Code), so this rule does not vary by which of the three you are targeting — only by the fact that it is Claude Code at all.

A useful shorthand: **`$` is a GPT/Codex habit, `/` is a Claude Code habit.** Whichever runtime is on the other end of the prompt decides the character, not the model name by itself.

## Why both exist, and the one nuance worth knowing

Codex actually accepts a skill's name as a native `/slash-command` too, because a skill's `name:` field is registered as one. That means a `/name` invocation technically works inside Codex. Despite that, this pack's house style still writes `$name` when addressing GPT/Codex, for two practical reasons: it is the convention already baked into every existing `AGENTS.md` and sibling skill in this pack (changing it now would create silent inconsistency across dozens of files), and it keeps a skimmable visual signal in mixed-audience documents — a reader can tell which agent a line is meant for at a glance, without re-reading the surrounding sentence. Do not "correct" existing `$name` references to `/name` inside Codex-facing text on the theory that both work; keep the pack's established convention.

## Practical checklist when writing a prompt for another agent

1. Identify the runtime the prompt will actually run in — Codex (GPT-5.5) or Claude Code (Opus 4.8 / Sonnet 5 / Fable 5). If unsure, ask, because the wrong trigger character silently fails instead of erroring.
2. Use `$skill-name` for every skill reference if the runtime is Codex.
3. Use `/skill-name` for every skill reference if the runtime is Claude Code, regardless of which of the three Claude models is running.
4. When writing a prompt pack that targets both agents in the same document (for example, a Codex implementation prompt paired with a Claude Opus review prompt, as `$alaa-workflow` produces), switch the trigger character section by section — never assume one character carries through the whole document.
5. When in doubt about a specific skill's exact registered name, read that skill's own `SKILL.md` `name:` frontmatter field rather than guessing a shorthand.
