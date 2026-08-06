# Skill Platform Mechanics

Lookup surface for the two runtimes that load a `SKILL.md`: the package layout, where each runtime finds a skill, which frontmatter keys each documents, and the budgets that decide how much of a description reaches the model. Consult a value here; do not carry one from memory, and re-verify against the Sources before quoting one into an artifact.

## Package layout

Both runtimes take a directory whose entrypoint is `SKILL.md`. Every other directory is optional and is loaded only when the body points at it.

```
my-skill/
├── SKILL.md          # required entrypoint: frontmatter + lean body
├── references/       # detail loaded on demand
├── scripts/          # executable code the agent runs rather than reimplements
├── assets/           # templates, fixtures, static resources
└── agents/           # agent definitions shipped with the package
```

The OpenAI skills documentation names `scripts/`, `references/`, and `assets/` directly, plus an optional `agents/openai.yaml` carrying UI metadata, invocation policy, and tool dependencies for that runtime. Claude Code's documentation describes the same idea generically — templates to fill in, example outputs, scripts to execute, detailed reference documentation — and its worked example uses `scripts/` and `examples/`. The layout above satisfies both, which is why the orchestrator packs ship it unchanged across runtimes. When you are about to put a file in `agents/`, read `references/80-subagent-authoring.md`: it owns what a definition pins and how a dispatch is written.

## Discovery

Do not guess a discovery path. Both runtimes publish theirs, and they do not match.

**Claude Code** loads personal skills from `~/.claude/skills/<skill-name>/SKILL.md`, project skills from `.claude/skills/<skill-name>/SKILL.md`, plugin skills from `<plugin>/skills/<skill-name>/SKILL.md`, and enterprise skills from managed settings. On a name clash across levels, enterprise wins over personal and personal wins over project, and any of the three overrides a bundled skill of the same name. Project skills load from the directory the session started in and from every parent up to the repository root. A nested `.claude/skills/` below the starting directory does not load at startup: it loads the first time Claude reads or edits a file inside that subdirectory, and a nested skill whose name clashes with another is reachable under its directory-qualified name. Adding, editing, or removing a skill takes effect inside the running session; creating a top-level skills directory that did not exist at session start requires a restart.

**Codex** scans `.agents/skills` in the current directory, then in the parent, then at `$REPO_ROOT`, then `$HOME/.agents/skills`, then `/etc/codex/skills`, then the skills bundled with Codex. It also discovers user skills under `$HOME/.codex/skills` — field-verified, including on Windows where the path is `Join-Path $HOME ".codex\skills"` — even though the official page omits it. That location is the practical default for personal Codex skills here, because it sits beside `~/.codex/agents/` and keeps the whole Codex setup in one tree; reserve `.agents/skills` for skills that must travel with a specific repository. Carry the general lesson: an official discovery list can be incomplete, so a path that demonstrably works is evidence, not an error to correct.

## Frontmatter key surfaces

Use only keys the runtime documents. An invented key is ignored in silence inside Claude Code and is a hard error on the distribution paths named below.

**Claude Code** documents `name`, `description`, `when_to_use`, `argument-hint`, `arguments`, `disable-model-invocation`, `user-invocable`, `allowed-tools`, `disallowed-tools`, `model`, `effort`, `context`, `agent`, `background`, `hooks`, `paths`, `shell`, `metadata`, `license`, and `compatibility`. Every field is optional, only `description` is recommended, and `name` defaults to the directory name. Five earn their place in most production skills: `disable-model-invocation: true` for a skill that must run only when a human types `/name`; `allowed-tools` to pre-approve exactly the commands the body tells the agent to run; `disallowed-tools` to remove a tool for as long as the skill is active; `paths` to restrict automatic activation to matching files; and `context: fork` to run the skill in a subagent context.

**Outside Claude Code the surface narrows to six keys, and an extra key fails the build rather than being ignored.** claude.ai skill uploads, the Skills API, and packaging with `package_skill.py` accept only `name`, `description`, `license`, `compatibility`, `metadata`, and `allowed-tools`, and reject anything else with an unexpected-key error. A skill that must survive both distribution paths carries only those six.

**Codex** requires `name` and `description` in `SKILL.md` and documents no larger frontmatter surface for skills. Treat anything beyond those two keys as unverified for that runtime, and put the behavior in the body instead of in a speculative key.

A cross-runtime skill therefore carries `name` and `description`, adds a Claude-only key deliberately and knowing it is inert under Codex, and keeps that key out of the package when the same directory is also uploaded to claude.ai.

## Description budgets

Neither runtime loads a body to decide whether to load that body. Both build a listing of names and descriptions and match a request against that listing, so every number below governs how much of a description the model ever sees. Four caps apply, and only the first stops a skill from installing.

- **Plugin validation rejects a `description` longer than 1,024 characters.** It fails the build, so it is the number to write against. Measure the *packaged* description rather than the line on disk: plugin packaging rewrites every cross-skill call in a packaged Markdown file, frontmatter included, into its namespaced form, so each routing reference costs the namespace plus a colon and the packaged length exceeds the on-disk length. The margin to leave below 1,024 is therefore a property of the packaging namespace and not a constant — renaming the plugin moves it. This pack's author target and the validator that computes the packaged length are owned by the pack contract at `skills/sohrab/AGENTS.md`.
- **Claude Code caps each entry's combined `description` plus `when_to_use` at 1,536 characters,** truncating from the end. The cap is configurable through the `skillListingMaxDescChars` setting.
- **Claude Code budgets the whole listing at 1% of the model's context window,** configurable through the `skillListingBudgetFraction` setting or a fixed character count in `SLASH_COMMAND_TOOL_CHAR_BUDGET`. The listing always carries every skill name; when it overflows, Claude Code shortens descriptions starting with the skills invoked least, so a rarely used skill loses its keywords first.
- **Codex budgets the initial listing at at most 2% of the model's context window, or 8,000 characters when the window is unknown.** It shortens descriptions first and, for a large skill set, may omit skills from the initial list entirely and show a warning.

Every one of these mechanisms removes text from the end of a description or removes the description outright, which is why both sets of documentation give the same instruction: front-load the key use case and the trigger words so a shortened description still matches the request. When you are about to write or repair a description, read `references/60-skill-authoring.md` — it owns the three parts a description must state and the defects each missing part produces.

## Freshness

Verified against live documentation on 6 August 2026. Re-check before quoting: the 1,024-character plugin-validation limit; the 1,536-character per-entry cap and the 1%-of-context listing budget in Claude Code, both of which have configurable settings behind them; the 2%-or-8,000-character Codex listing budget; the Claude Code frontmatter field list, which grows between releases and carries per-version notes on several fields; and both runtimes' discovery paths, which have changed in ways that silently broke skills written against the previous documentation.

## Sources

- [Extend Claude with skills (Claude Code)](https://code.claude.com/docs/en/skills)
- [Build skills (OpenAI)](https://learn.chatgpt.com/docs/build-skills)
