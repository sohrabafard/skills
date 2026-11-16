# Agent Instruction Files: `AGENTS.md` and `CLAUDE.md`

An instruction file is the standing context a coding agent carries into every task in a repository: the small set of facts and rules that would otherwise be re-explained at the start of every session. It is neither documentation nor a skill. It loads unconditionally, so every line costs context on every task, including tasks it is irrelevant to. That property decides how these files are written.

## What each file is and which runtime reads it

**`CLAUDE.md`** is Claude Code's instruction file. Claude Code reads `CLAUDE.md`; it reads `AGENTS.md` only under the conditions stated below. It loads from four scopes, listed here in load order from broadest to most specific, so a project instruction appears in context after a user instruction:

| Scope | Location |
|---|---|
| Managed policy | macOS `/Library/Application Support/ClaudeCode/CLAUDE.md`; Linux and WSL `/etc/claude-code/CLAUDE.md`; Windows `C:\Program Files\ClaudeCode\CLAUDE.md` |
| User | `~/.claude/CLAUDE.md` |
| Project | `./CLAUDE.md` or `./.claude/CLAUDE.md` |
| Local (gitignored) | `./CLAUDE.local.md` |

Organizations can also inline managed content through the `claudeMd` key in managed settings, which loads before user and project files and cannot be excluded.

**`AGENTS.md`** is Codex's instruction file. Codex reads global guidance from the Codex home directory (`~/.codex` by default, or `$CODEX_HOME`), then walks the project from its root, typically the Git root, down to the current working directory.

The two runtimes are not symmetric. Verified 14 November 2026 against the Claude Code memory page: since v2.1.277 Claude Code reads a repository's `AGENTS.md` by default only when no `CLAUDE.md`, `.claude/CLAUDE.md` or `CLAUDE.local.md` exists in the working directory or above it. The user-level `~/.claude/CLAUDE.md`, a managed `CLAUDE.md` and `.claude/rules/` files do not count for that check and load alongside. The project-instructions setting `instructionFiles` changes the default: `claude-md-and-agents-md` loads both, and `managed-only` loads neither. A session with the built-in `AGENTS.md` plugin disabled reads no `AGENTS.md`. Codex's fallback filenames are configurable through `project_doc_fallback_filenames` but are not documented to include `CLAUDE.md` by default. A repository that ships both files must still bridge them, because the presence of a `CLAUDE.md` stops the `AGENTS.md` fallback.

## Nesting and precedence

Both runtimes concatenate rather than override, root-down, so files closer to the working directory are read last and win a contradiction by position, not by rule.

**Claude Code** walks up the directory tree from the working directory and loads every `CLAUDE.md` and `CLAUDE.local.md` it finds, in full, at launch. Content is ordered from the filesystem root down to the working directory, and within a directory `CLAUDE.local.md` is appended after `CLAUDE.md`. Files in subdirectories *below* the working directory are not loaded at launch; they load on demand when Claude reads a file in that subdirectory. `@path/to/import` pulls in more files recursively, up to four hops, but imports expand at launch, so they organize content without reducing its context cost. `claudeMdExcludes` skips ancestor files by glob, for example other teams' files in a monorepo; managed policy files cannot be excluded.

**Codex** rebuilds the chain on every run and at the start of each TUI session, so no cache needs clearing. It resolves one file per level. At the global level it checks `AGENTS.override.md` first, then `AGENTS.md`, and uses only the first non-empty file; `~/.codex/AGENTS.override.md` applies a temporary global override without deleting the base file. At each directory from the project root down to the working directory it checks `AGENTS.override.md`, then `AGENTS.md`, then any configured fallback names, and includes at most one file per directory. It joins those files root-down with blank lines, so files closer to the current directory override earlier guidance by appearing later. Codex stops searching at the current directory, so put per-team overrides as close to the specialized work as possible. The whole set is bounded by `project_doc_max_bytes`, 32 KiB by default; empty files are skipped and Codex stops adding files once the combined size reaches the limit.

Note what the byte limit implies. Codex silently truncates the *tail* of the merge order when a repository's instruction files grow past 32 KiB, and the tail is where the most specific guidance lives. A bloated root `AGENTS.md` can therefore evict the leaf file that actually governs the directory being edited.

## The distinction from a skill, and the decision test

When you must decide whether content belongs in an instruction file, a skill, a prompt or a subagent, read `references/60-skill-authoring.md` *Should this be a skill at all?*; it holds the test. An instruction file holds only rules that are true for every task in the repository. In Claude Code, a rule true only for some directories or file types can also go in a path-scoped rule under `.claude/rules/` with a `paths:` frontmatter list. Claude Code's guidance draws the same line: move a multi-step procedure, or content that matters for only one part of the codebase, into a skill or a path-scoped rule. A runbook, a migration checklist or a framework tutorial in the instruction file is paid for on every unrelated bug fix.

Two corollaries follow. First, an instruction file that has crossed roughly 200 lines is usually carrying conditional content that should have been a skill; Claude Code's guidance targets under 200 lines per file and states that longer files consume more context and reduce adherence. Second, splitting a long file into imports is organization, not relief: the imported content still loads at launch. The 200-line target is soft and yields to behavior preservation; the 32 KiB budget above is hard and drops the tail silently, so a file that cannot fit it is restructured — conditional content into a skill — never trimmed by deleting a rule. `references/60-skill-authoring.md` owns what may never be cut.

## What belongs in one

Include only what an agent cannot derive from the repository in a few tool calls, or would derive incorrectly.

- **Commands that actually work.** The real build, test, lint and format invocations, including those that differ from the ecosystem default, such as "Use `make test-payments` instead of `npm test`." Verify each command before you write it down: the agent trusts a stale command and reports a check it never ran.
- **Architecture and directory ownership** where the layout is non-obvious or misleading — which package owns which contract, where generated code comes from, which directory is a vendored copy nobody edits.
- **Conventions a newcomer would violate.** The error-response shape, the logging contract, the migration naming scheme, the dependency-injection idiom the codebase uses everywhere.
- **Non-obvious constraints and invariants.** The table that must not be written to outside a transaction, the service that cannot tolerate a schema change without a compatibility window, the endpoint whose response shape is consumed by a client you do not control.
- **What is off limits.** Directories that are never edited, operations that require a human (publishing, deployment, force-push, credential rotation, production data movement) and the escalation path. Write each one specific, actionable and about a real boundary, such as "Never rotate API keys without notifying the security channel."

## What does not belong

Apply the filter of Claude Code's `/doctor` trim check: cut content the agent can derive from the codebase (directory layouts, dependency lists, architecture overviews), and keep pitfalls, rationale and conventions that differ from tool defaults.

- **Anything re-derivable from the filesystem**, such as a directory tree, a dependency list or a module summary. These go stale and cost tokens on every task.
- **Aspirational rules nobody follows.** A rule the codebase violates in fifty places teaches the agent that the file's rules are advisory. Delete it or fix the codebase.
- **General programming advice**, such as "write clean code". The model already knows it, and it displaces the repository-specific facts the model does not know.
- **Duplicated skill content.** When a procedure lives in a skill, name the skill and its trigger in one line, not a summary.
- **Long code samples.** Point at a real file that shows the pattern instead: the pointer costs one line and cannot go stale.

## Writing rules that are actually obeyed

Instruction files are context, not enforcement. Claude Code delivers `CLAUDE.md` as a user message after the system prompt and guarantees no strict compliance. For anything that must run at a fixed lifecycle point, use a hook or a permission rule, not a sentence. When you write or review a rule, read `references/60-skill-authoring.md` *The wording is the mechanism*; it owns the wording failure modes. Two apply with extra force here: a rule repeated in two sections or two levels will drift, and a model facing two conflicting rules may follow either one.

## One repository, two runtimes

**Import bridge (recommended).** Keep `AGENTS.md` as the single source of truth and create a `CLAUDE.md` containing `@AGENTS.md`, optionally followed by Claude-only additions. Claude Code's documentation recommends this by name. The shared part cannot diverge, and Claude-only guidance still has a place. Cost: two files exist, and a reader must know which one is authoritative.

**Symlink.** `ln -s AGENTS.md CLAUDE.md` is simplest and truly one file. Costs: no place for runtime-specific content, and on Windows a symlink needs Administrator privileges or Developer Mode, so mixed-OS teams use the import bridge instead.

**Two maintained files.** Use them only when the runtimes genuinely need different content: different agent rosters, tool availability or sandbox semantics. Every convention change is then made twice, and the files drift silently because nothing fails when they disagree. Keep the shared 90% in a third file that both import or include, and let each runtime file hold only its delta.

Whichever you choose, keep runtime-specific call prefixes out of the shared body. A shared file names the skill in prose ("the alaa-security-review skill"); a prefixed call form belongs only in a runtime-specific section. When you decide which call form belongs at a live invocation site, read `references/06-invocation-and-composition.md`; it owns the per-runtime call syntax.

## Defects and fixes

| Defect | Symptom | Fix |
|---|---|---|
| Conditional content in an always-loaded file | File exceeds ~200 lines; most of it is irrelevant to most tasks | Move procedures to skills and file-type rules to `.claude/rules/` with `paths:` |
| Stale commands | Agent reports a check that could not have run | Execute every documented command before committing the file; re-verify when tooling changes |
| Re-derivable content | Directory trees and dependency lists in the file | Delete; the agent reads the filesystem faster than it reads your summary |
| Contradiction across levels | Behavior varies unpredictably by working directory | Audit ancestor files; in Claude Code use `claudeMdExcludes`, in Codex place the authoritative rule in the deepest relevant directory |
| Silent truncation | Deep, specific guidance stops taking effect in Codex | Trim the root file; the 32 KiB `project_doc_max_bytes` budget drops the tail of the merge, which is the most specific content |
| Aspirational rules | Agent treats all rules as advisory | Delete rules the codebase violates, or fix the codebase |
| Prohibition without destination | Agent avoids the wrong path and picks another wrong one | Rewrite as a positive instruction naming the correct target |
| Imports used to shrink context | File "shortened" but context unchanged | Imports load at launch; delete content or move it to a skill instead |
| Two divergent runtime files | Conventions differ by runtime for no reason | Collapse to the import bridge or a symlink |

## Checklist

1. Every line is true for every task in this repository; anything conditional has moved to a skill or a path-scoped rule.
2. The file is under roughly 200 lines with no rule deleted to reach it, and imports were not used as a substitute for deleting content.
3. Every command in the file has been executed and observed to work.
4. Nothing in the file is re-derivable from the filesystem in a few tool calls.
5. Each rule is one statement, concrete enough to verify, positive where a positive form exists, and carries a reason where it would otherwise look arbitrary.
6. No rule contradicts another rule at any level of the tree.
7. Off-limits actions and the escalation path are enumerated explicitly.
8. Skills are referenced by name and trigger condition, never summarized.
9. Both runtimes are served by one source of truth, and runtime-specific trigger prefixes appear only in runtime-specific sections.
10. For anything that must happen at a fixed point regardless of model judgment, a hook or permission rule exists — the instruction file is not carrying that weight alone.

## Caveats

Verified 24 July 2026; the Claude Code `AGENTS.md` fallback was verified 14 November 2026. Values that move between releases:

- Claude Code's under-200-line target — guidance, not an enforced limit; `CLAUDE.md` files load in full regardless of length. The `MEMORY.md` 200-line / 25 KB cap governs auto memory only, not `CLAUDE.md`.
- Codex `project_doc_max_bytes` — 32 KiB default; `project_doc_fallback_filenames` is not documented to include `CLAUDE.md` — confirm against the running version before relying on it.
- Claude Code settings names (`claudeMd`, `claudeMdExcludes`, the project-instructions option `instructionFiles`) and the `.claude/rules/` mechanism — carry per-version notes; check against the running version.

## Sources

- [How Claude remembers your project (Claude Code)](https://code.claude.com/docs/en/memory)
- [Extend Claude with skills (Claude Code)](https://code.claude.com/docs/en/skills)
- [AGENTS.md (Codex)](https://developers.openai.com/codex/guides/agents-md)
- [Skills (Codex)](https://learn.chatgpt.com/docs/build-skills)
- [Latest model guide (OpenAI)](https://developers.openai.com/api/docs/guides/latest-model)
