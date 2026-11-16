# Skill Platform Mechanics

Lookup values for the two runtimes that load a `SKILL.md`. Take a value from here, never from memory, and re-verify it against the Sources before you quote it into an artifact.

## Package layout

Both runtimes take a directory whose entrypoint is `SKILL.md`. Every other directory is optional and loads only when the body points at it.

```
my-skill/
├── SKILL.md          # required entrypoint: frontmatter + lean body
├── references/       # detail loaded on demand
├── scripts/          # executable code the agent runs rather than reimplements
├── assets/           # templates, sample inputs, static resources
└── agents/           # agent definitions shipped with the package
```

- The OpenAI documentation names `scripts/`, `references/` and `assets/`, plus an optional `agents/openai.yaml` that carries UI metadata, invocation policy and tool dependencies for that runtime. Its `allow_implicit_invocation` (default `true`) set to `false` stops a skill from firing on its own.
- Claude Code describes the same layout generically; its worked example uses `scripts/` and `examples/`.
- Before you put a file in `agents/`, read `references/80-subagent-authoring.md`.

## Official structure guidance

Fetched 16 November 2026 from [Claude Code skills](https://code.claude.com/docs/en/skills) and [Agent Skills best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices):

- Keep `SKILL.md` under 500 lines, and move detailed reference material to separate files.
- Put the most important instructions near the top of `SKILL.md`, because compaction can keep only the start of an invoked skill.
- Keep references one level deep from `SKILL.md`.
- A reference longer than 100 lines carries a table of contents.
- Write a description in the third person.
- Agent Skills `name`: at most 64 characters; lowercase letters, numbers and hyphens; no reserved word `anthropic` or `claude`. Agent Skills `description`: at most 1,024 characters.

## Discovery

Never guess a discovery path. The two runtimes publish different ones.

**Claude Code.**

| Level | Path |
|---|---|
| Personal | `~/.claude/skills/<skill-name>/SKILL.md` |
| Project | `.claude/skills/<skill-name>/SKILL.md` |
| Plugin | `<plugin>/skills/<skill-name>/SKILL.md` |
| Enterprise | Managed settings |

- On a name clash, enterprise wins over personal and personal wins over project; any of the three overrides a bundled skill of the same name.
- Project skills load from the directory the session started in and from every parent up to the repository root.
- A nested `.claude/skills/` below the starting directory loads the first time Claude reads or edits a file inside that subdirectory, not at startup. A nested skill whose name clashes with another is reachable under its directory-qualified name.
- Adding, editing or removing a skill takes effect inside the running session. Creating a top-level skills directory that did not exist at session start needs a restart.

**Codex** scans, in order: `.agents/skills` in the current directory, in the parent, and at `$REPO_ROOT`; `$HOME/.agents/skills`; `/etc/codex/skills`; the skills bundled with Codex.

- It also discovers user skills under `$HOME/.codex/skills`, which the official page omits. The evidence came from a retired Windows host, and discovery on WSL is unverified: check it in the target runtime before you rely on it. An official list can be incomplete; a path that demonstrably works is evidence, not an error to correct.
- In install instructions, name `$HOME/.codex/skills` for personal skills unless the user said otherwise, because it keeps skills beside `~/.codex/agents/` in one tree. Name `.agents/skills` for skills that must travel with a repository.

## Frontmatter key surfaces

Use only keys the runtime documents. Claude Code ignores an invented key in silence; the distribution paths below reject it.

| Surface | Keys |
|---|---|
| Claude Code | `name`, `description`, `when_to_use`, `argument-hint`, `arguments`, `disable-model-invocation`, `user-invocable`, `allowed-tools`, `disallowed-tools`, `model`, `effort`, `context`, `agent`, `background`, `hooks`, `paths`, `shell`, `metadata`, `license`, `compatibility`. Every field is optional, only `description` is recommended, and `name` defaults to the directory name |
| claude.ai skill uploads, the Skills API, and packaging with `package_skill.py` | Only `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`. Any other key fails with an unexpected-key error |
| Codex | Requires `name` and `description` and documents no larger surface. Treat any other key as unverified, and put the behavior in the body |

A cross-runtime skill carries `name` and `description`. Add a Claude-only key deliberately, knowing it is inert under Codex, and keep it out of a package that is also uploaded to claude.ai.

Five Claude Code keys earn their place in most production skills:

| Key | Use |
|---|---|
| `disable-model-invocation: true` | A skill that runs only when a human types `/name` |
| `allowed-tools` | Pre-approve exactly the commands the body tells the agent to run |
| `disallowed-tools` | Remove a tool while the skill is active |
| `paths` | Restrict automatic activation to matching files |
| `context: fork` | Run the skill in a subagent context |

## Description budgets

Neither runtime loads a body to decide whether to load it. Both match a request against a listing of names and descriptions. Four caps apply; only the first stops a skill from installing.

| Cap | Effect |
|---|---|
| Plugin validation: `description` at most 1,024 characters | Longer fails the build. Write against this number |
| Claude Code: `description` plus `when_to_use` at most 1,536 characters per entry | Truncates from the end. Configurable through `skillListingMaxDescChars` |
| Claude Code: whole listing at 1% of the model's context window | Configurable through `skillListingBudgetFraction`, or a fixed character count in `SLASH_COMMAND_TOOL_CHAR_BUDGET`. The listing always carries every skill name; on overflow Claude Code shortens descriptions, starting with the skills invoked least |
| Codex: initial listing at most 2% of the context window, or 8,000 characters when the window is unknown | Shortens descriptions first; for a large skill set it can omit skills from the initial list and show a warning. The full `SKILL.md` loads once a skill is selected, whatever the budget |

**Measure the packaged description, not the line on disk.** Plugin packaging rewrites every cross-skill call in a packaged Markdown file, frontmatter included, into its namespaced form. Each routing reference then costs the namespace length plus one for the colon.

**Derive the author target; never recall it.** From 1,024, subtract the namespace length plus one, multiplied by the number of routing references the description carries, and leave room for one more reference. At this pack's two-character namespace the target is 975, which its validator checks. A longer namespace lowers the target, renaming the plugin moves it, and a description with several routing references sits nearer the limit than a longer one with none.

Every mechanism cuts from the end of a description or drops it, so front-load the key use case and the trigger words. To write or repair a description, read `references/60-skill-authoring.md`; it owns the parts a description states.

## Freshness

Verified against live documentation on 6 August 2026, except the section dated 16 November 2026. Re-check before you quote: the three character caps and the two listing budgets, the Claude Code frontmatter list (it grows between releases and carries per-version notes), and both runtimes' discovery paths, which have changed and silently broken skills.

## Sources

- [Extend Claude with skills (Claude Code)](https://code.claude.com/docs/en/skills)
- [Agent Skills best practices (Claude Platform)](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Build skills (OpenAI)](https://learn.chatgpt.com/docs/build-skills)
