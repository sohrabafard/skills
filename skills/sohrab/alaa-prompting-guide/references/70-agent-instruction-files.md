# Agent Instruction Files: `AGENTS.md` and `CLAUDE.md`

An instruction file loads on every task in a repository, so every line costs context on every task, including the tasks it does not concern. Write it for that cost.

## Which runtime reads which file

**`CLAUDE.md`** is Claude Code's file. It loads from four scopes, broadest first, so a project instruction appears in context after a user instruction:

| Scope | Location |
|---|---|
| Managed policy | macOS `/Library/Application Support/ClaudeCode/CLAUDE.md`; Linux and WSL `/etc/claude-code/CLAUDE.md`; Windows `C:\Program Files\ClaudeCode\CLAUDE.md` |
| User | `~/.claude/CLAUDE.md` |
| Project | `./CLAUDE.md` or `./.claude/CLAUDE.md` |
| Local (gitignored) | `./CLAUDE.local.md` |

The `claudeMd` key in managed settings inlines managed content. It loads before user and project files and cannot be excluded.

**`AGENTS.md`** is Codex's file. Codex reads global guidance from the Codex home directory (`~/.codex`, or `$CODEX_HOME`), then walks the project from its root, typically the Git root, down to the working directory.

**The runtimes are not symmetric** (Claude Code memory page, 14 November 2026):

- Since v2.1.277 Claude Code reads a repository's `AGENTS.md` by default only when no `CLAUDE.md`, `.claude/CLAUDE.md` or `CLAUDE.local.md` exists in the working directory or above it. The user-level `~/.claude/CLAUDE.md`, a managed `CLAUDE.md` and `.claude/rules/` files do not count for that check and load alongside.
- The `instructionFiles` setting changes the default: `claude-md-and-agents-md` loads both, and `managed-only` loads neither. A session with the built-in `AGENTS.md` plugin disabled reads no `AGENTS.md`.
- Codex's `project_doc_fallback_filenames`, in `~/.codex/config.toml`, adds alternative filenames. It is not documented to include `CLAUDE.md` by default.
- A repository that ships both files must bridge them, because a `CLAUDE.md` stops the `AGENTS.md` fallback.

## Nesting and precedence

Both runtimes concatenate root-down and override nothing. A file nearer the working directory is read later and wins a contradiction by position.

**Claude Code** walks up from the working directory and loads every `CLAUDE.md` and `CLAUDE.local.md` in full at launch.

- Order: filesystem root down to the working directory; within a directory, `CLAUDE.local.md` after `CLAUDE.md`.
- A file in a subdirectory below the working directory loads on demand, when Claude reads a file there.
- `@path/to/import` pulls in files recursively, up to four hops. Imports expand at launch, so they organize content without reducing its context cost.
- `claudeMdExcludes` skips ancestor files by glob, such as other teams' files in a monorepo. Managed policy files cannot be excluded.

**Codex** rebuilds the chain on every run and at the start of each TUI session, so no cache needs clearing.

- Global level: `AGENTS.override.md` first, then `AGENTS.md`; only the first non-empty file is used. `~/.codex/AGENTS.override.md` is a temporary global override that leaves the base file in place.
- Each directory from the project root down to the working directory: `AGENTS.override.md`, then `AGENTS.md`, then any configured fallback name; at most one file per directory. Empty files are skipped.
- The files are joined root-down with blank lines. Codex stops searching at the working directory, so put a per-team override as close to the specialized work as possible.
- **Size limit.** `project_doc_max_bytes` bounds the combined size, 32 KiB by default. Codex adds files from the root down and "stops adding files once the combined size reaches the limit". The files nearest the working directory, which hold the most specific guidance, are therefore the ones left out: a bloated root `AGENTS.md` evicts the leaf file that governs the directory being edited. The page advises: "Raise the limit or split instructions across nested directories". It does not say whether a file that crosses the limit is cut or skipped whole, and its 65536 is an example value, not a stated maximum. Source: [AGENTS.md (Codex)](https://learn.chatgpt.com/docs/agent-configuration/agents-md), 16 November 2026.

Symptoms of a chain defect:

| Symptom | Fix |
|---|---|
| Behavior varies by working directory | Audit the ancestor files for a contradiction. In Claude Code use `claudeMdExcludes`; in Codex put the authoritative rule in the deepest relevant directory |
| Deep, specific guidance stops taking effect in Codex | The chain passed `project_doc_max_bytes`. Shrink the root file by moving conditional content into a skill, or raise the limit |

## What belongs in one

To decide between an instruction file, a skill, a prompt, a script and a subagent, read `references/60-skill-authoring.md` *Should this be a skill at all?*. An instruction file holds only what is true for every task in the repository, and only what an agent cannot derive from the repository in a few tool calls or would derive wrongly.

- **Commands that work.** The real build, test, lint and format invocations, above all those that differ from the ecosystem default ("Use `make test-payments` instead of `npm test`"). Run each command before you write it down: the agent trusts a stale command and reports a check that never ran.
- **Architecture and directory ownership** where the layout is not obvious or misleads: which package owns which contract, where generated code comes from, which directory is a vendored copy nobody edits.
- **Conventions a newcomer would violate:** the error-response shape, the logging contract, the migration naming scheme, the dependency-injection idiom.
- **Constraints and invariants that are not obvious:** the table never written outside a transaction, the service that needs a compatibility window for a schema change, the response shape a client you do not control consumes.
- **What is off limits:** directories that are never edited, operations that need a person (publishing, deployment, force-push, credential rotation, production data movement) and the escalation path. Make each one specific and about a real boundary: "Never rotate API keys without notifying the security channel."

## What does not belong

Apply the filter of Claude Code's `/doctor` trim check: cut what the agent can derive from the codebase, and keep pitfalls, rationale and conventions that differ from tool defaults.

- **Content the filesystem already gives:** a directory tree, a dependency list, a module summary, an architecture overview. It goes stale and costs tokens on every task.
- **A rule the codebase violates.** It teaches the agent that the file's rules are advisory. Delete it or fix the codebase.
- **General programming advice** such as "write clean code". The model knows it, and it displaces the repository facts the model lacks.
- **Skill content.** Name the skill and its trigger in one line; never summarize it.
- **A long code sample.** Point at a real file that shows the pattern: the pointer costs one line and cannot go stale.
- **Conditional content.** A multi-step procedure, or content for one part of the codebase, goes into a skill. In Claude Code a rule for some directories or file types can go in a path-scoped rule under `.claude/rules/` with a `paths:` frontmatter list.

## Size

- **Soft target: about 200 lines per file.** Claude Code's guidance targets under 200 lines and says a longer file consumes more context and reduces adherence. A file past that length usually carries conditional content. The target yields to behavior preservation.
- **Hard limit: the Codex byte budget above.** Meet it by restructuring, conditional content into a skill, never by deleting a rule. `references/60-skill-authoring.md` owns what a compress pass may never cut.
- Splitting a file into imports is organization, not relief: imported content still loads at launch.

## Rules that are obeyed

- An instruction file is context, not enforcement. Claude Code delivers `CLAUDE.md` as a user message after the system prompt and guarantees no strict compliance. For anything that must run at a fixed lifecycle point, use a hook or a permission rule.
- For wording, read `references/60-skill-authoring.md` *The wording is the mechanism*.
- State a rule in one section and at one level. A repeated rule drifts, and a model that faces two conflicting rules can follow either.

## One repository, two runtimes

| Option | Use when | Cost |
|---|---|---|
| **Import bridge (recommended):** `AGENTS.md` is the single source of truth, and `CLAUDE.md` contains `@AGENTS.md`, optionally followed by Claude-only additions | By default. Claude Code's documentation recommends it by name | Two files exist, and a reader must know which one is authoritative |
| **Symlink:** `ln -s AGENTS.md CLAUDE.md` | One file serves both and no runtime needs its own content | No place for runtime-specific content. On Windows a symlink needs Administrator privileges or Developer Mode, so a mixed-OS team uses the import bridge |
| **Two maintained files** | The runtimes need different content: agent rosters, tool availability or sandbox semantics | Every convention change is made twice, and nothing fails when the files disagree. Keep the shared part in a third file that both import or include, and let each runtime file hold only its delta |

Keep runtime-specific call prefixes out of the shared body: name a skill there in prose ("the alaa-security-review skill"). A prefixed call form belongs only in a runtime-specific section; `references/06-invocation-and-composition.md` owns the per-runtime call syntax.

## Caveats

Verified 24 July 2026, except the dated facts above. Values that move between releases:

- Claude Code's 200-line target is guidance, not an enforced limit; a `CLAUDE.md` loads in full at any length. The `MEMORY.md` 200-line / 25 KB cap governs auto memory only.
- Confirm the Codex `project_doc_max_bytes` default and the fallback filenames against the running version before you rely on them.
- The Claude Code setting names (`claudeMd`, `claudeMdExcludes`, `instructionFiles`) and the `.claude/rules/` mechanism carry per-version notes.

## Sources

- [How Claude remembers your project (Claude Code)](https://code.claude.com/docs/en/memory)
- [Extend Claude with skills (Claude Code)](https://code.claude.com/docs/en/skills)
- [AGENTS.md (Codex)](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Skills (Codex)](https://learn.chatgpt.com/docs/build-skills)
- [Latest model guide (OpenAI)](https://developers.openai.com/api/docs/guides/latest-model)
