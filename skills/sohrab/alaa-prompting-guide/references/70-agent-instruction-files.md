# Agent Instruction Files: `AGENTS.md` and `CLAUDE.md`

An instruction file is the standing context a coding agent carries into every task in a repository. It is not documentation and not a skill: it is the small set of facts and rules that would otherwise be re-explained at the start of every session. Because it is loaded unconditionally, every line is a permanent tax on the context window of every task, including the tasks the line is irrelevant to. That single property determines everything about how these files should be written.

## What each file is and which runtime reads it

**`CLAUDE.md`** is Claude Code's instruction file. Claude Code reads `CLAUDE.md`, not `AGENTS.md`. It loads from four scopes, listed here in load order from broadest to most specific, so a project instruction appears in context after a user instruction:

| Scope | Location |
|---|---|
| Managed policy | macOS `/Library/Application Support/ClaudeCode/CLAUDE.md`; Linux and WSL `/etc/claude-code/CLAUDE.md`; Windows `C:\Program Files\ClaudeCode\CLAUDE.md` |
| User | `~/.claude/CLAUDE.md` |
| Project | `./CLAUDE.md` or `./.claude/CLAUDE.md` |
| Local (gitignored) | `./CLAUDE.local.md` |

Organizations can also inline managed content through the `claudeMd` key in managed settings, which loads before user and project files and cannot be excluded.

**`AGENTS.md`** is Codex's instruction file. Codex looks in two places: the Codex home directory (`~/.codex` by default, or `$CODEX_HOME`) for global guidance, and then the project, starting at the project root — typically the Git root — and walking down to the current working directory.

An important asymmetry: Claude Code does not fall back to `AGENTS.md`, and Codex's fallback filenames are configurable through `project_doc_fallback_filenames` but are not documented to include `CLAUDE.md` by default. Neither runtime reads the other's file for free.

## Nesting and precedence

Both runtimes concatenate rather than override, and both order the concatenation root-down so that files closer to the working directory are read last and therefore win a contradiction by position rather than by rule.

**Claude Code** walks up the directory tree from the working directory and loads every `CLAUDE.md` and `CLAUDE.local.md` it finds, in full, at launch. Content is ordered from the filesystem root down to the working directory, and within a directory `CLAUDE.local.md` is appended after `CLAUDE.md`. Files in subdirectories *below* the working directory are not loaded at launch; they load on demand when Claude reads a file in that subdirectory. `@path/to/import` pulls additional files in, recursively, to a maximum depth of four hops — but imports expand at launch, so they organize content without reducing its context cost. `claudeMdExcludes` skips ancestor files by glob, which matters in monorepos where other teams' files would otherwise be picked up; managed policy files cannot be excluded.

**Codex** resolves one file per level. At the global level it checks `AGENTS.override.md` first, then `AGENTS.md`, and uses only the first non-empty file. At each directory from the project root down to the working directory it checks `AGENTS.override.md`, then `AGENTS.md`, then any configured fallback names, and includes at most one file per directory. It concatenates those files root-down joined by blank lines, so, in its own words, files closer to your current directory override earlier guidance because they appear later in the combined prompt. Codex stops searching at the current directory, which is why per-team overrides belong as close to the specialized work as possible. The whole set is bounded by `project_doc_max_bytes`, 32 KiB by default; empty files are skipped and Codex stops adding files once the combined size reaches the limit.

Note what the byte limit implies. Codex silently truncates the *tail* of the merge order when a repository's instruction files grow past 32 KiB, and the tail is where the most specific guidance lives. A bloated root `AGENTS.md` can therefore evict the leaf file that actually governs the directory being edited.

## The distinction from a skill, and the decision test

A skill costs nothing until it is loaded. An instruction file costs its full length on every task forever. This is the whole difference, and it yields a clean test.

> If a rule is true for every task in this repository, it belongs in the instruction file. If it is true only for some tasks, some directories, or some file types, it belongs in a skill — or, in Claude Code, in a path-scoped rule under `.claude/rules/` with a `paths:` frontmatter list.

Claude Code's own guidance draws the same line: keep the instruction file to facts Claude should hold in every session, and move anything that is a multi-step procedure or only matters for one part of the codebase into a skill or a path-scoped rule. The failure mode this prevents is the instruction file that grows into a procedure manual — a deployment runbook, a migration checklist, a framework tutorial — all of which are paid for on every unrelated bug fix.

Two corollaries follow. First, an instruction file that has crossed roughly 200 lines is usually carrying conditional content that should have been a skill; Claude Code's guidance targets under 200 lines per file and states that longer files consume more context and reduce adherence. Second, splitting a long file into imports is organization, not relief: the imported content still loads at launch. The 200-line target is soft and yields to behavior preservation; the 32 KiB budget above is hard and drops the tail silently, so a file that cannot fit it is restructured — conditional content into a skill — never trimmed by deleting a rule. `references/60-skill-authoring.md` owns what may never be cut.

## What belongs in one

Include only what an agent cannot derive from the repository in a few tool calls, or would derive incorrectly.

- **Commands that actually work.** The real build, test, lint, and format invocations, including the ones that differ from the ecosystem default. Codex's own examples are exactly this shape: "Always run `npm test` after modifying JavaScript files," "Run `npm run lint` before opening a pull request," "Use `make test-payments` instead of `npm test`." Verify each command before writing it down; a stale command is worse than no command, because the agent will trust it and report a check it never ran.
- **Architecture and directory ownership** where the layout is non-obvious or misleading — which package owns which contract, where generated code comes from, which directory is a vendored copy nobody edits.
- **Conventions a newcomer would violate.** The error-response shape, the logging contract, the migration naming scheme, the dependency-injection idiom the codebase uses everywhere.
- **Non-obvious constraints and invariants.** The table that must not be written to outside a transaction, the service that cannot tolerate a schema change without a compatibility window, the endpoint whose response shape is consumed by a client you do not control.
- **What is off limits.** Directories that are never edited, operations that require a human — publishing, deployment, force-push, credential rotation, production data movement — and the escalation path when one is needed. Codex's example, "Never rotate API keys without notifying the security channel," is the right register: specific, actionable, and about a real boundary.

## What does not belong

Claude Code's `/doctor` trim check encodes the distinction better than any argument: it cuts content the agent can derive from the codebase — directory layouts, dependency lists, architecture overviews — and keeps pitfalls, rationale, and conventions that differ from tool defaults. Apply that filter yourself.

- **Anything re-derivable from the filesystem.** A directory tree, a list of dependencies with versions, a summary of what each module does. The agent can read these, they go stale, and they cost tokens on every task.
- **Aspirational rules nobody follows.** A rule the codebase violates in fifty places teaches the agent that the file's rules are advisory. Delete it or fix the codebase.
- **General programming advice.** "Write clean code," "handle errors," "add tests." The model already knows, and this content displaces the repository-specific facts it does not know.
- **Duplicated skill content.** If a procedure lives in a skill, the instruction file should at most name the skill and the condition that triggers it — one line, not a summary.
- **Long code samples.** A twenty-line example costs twenty lines on every task. Point at a real file in the repository that exemplifies the pattern instead; the pointer is one line and the example cannot go stale.

## Writing rules that are actually obeyed

Instruction files are context, not enforcement. Claude Code is explicit that `CLAUDE.md` is delivered as a user message after the system prompt and that there is no guarantee of strict compliance — for anything that must run at a fixed lifecycle point, a hook or a permission rule is the correct mechanism, not a sentence. Within that limit, four properties raise adherence measurably.

**Concrete over abstract.** "Use 2-space indentation" outperforms "format code properly"; "Run `npm test` before committing" outperforms "test your changes"; "API handlers live in `src/api/handlers/`" outperforms "keep files organized." The test is whether a reader could verify compliance without asking you what you meant.

**One statement per rule.** A bullet that carries three obligations gets partially obeyed. Split it. This also matches the cross-model guidance that each instruction should be stated once and in one place — a rule repeated in two sections is a rule whose two copies will eventually disagree, and contradiction is the worst outcome available, because a model facing two conflicting rules may pick either one.

**Positive instruction over prohibition where possible.** "Add new endpoints to the versioned router in `src/api/v2/`" gives the agent a destination; "don't put endpoints in the old router" gives it only a place not to go, and leaves the actual target to be guessed. Reserve prohibitions for genuine boundaries, where there is no alternative action and the point is the boundary itself.

**A stated reason where a rule looks arbitrary.** "Use `pnpm`, not `npm` — the lockfile format is not interchangeable and `npm install` silently rewrites it" survives contact with a model that would otherwise reach for the more common tool. A rule whose rationale is obvious needs no reason; a rule that looks like a preference needs one, or it will be optimized away.

## One repository, two runtimes

Three approaches, with honest tradeoffs.

**Import bridge (recommended).** Keep `AGENTS.md` as the single source of truth and create a `CLAUDE.md` containing `@AGENTS.md`, optionally followed by Claude-specific additions. This is the approach Claude Code's documentation recommends by name. Both runtimes read the same content, divergence is structurally impossible for the shared part, and there is still a place to put genuinely Claude-only guidance. Cost: two files exist, and a reader must know which one is authoritative.

**Symlink.** `ln -s AGENTS.md CLAUDE.md`. Simplest, and truly one file. Two costs: there is nowhere to add runtime-specific content, and on Windows creating a symlink requires Administrator privileges or Developer Mode, so mixed-OS teams should use the import bridge instead.

**Two maintained files.** Only justified when the two runtimes genuinely need different content — different agent rosters, different tool availability, different sandbox semantics. The cost is real and recurring: every convention change must be made twice, and the files drift silently because nothing fails when they disagree. If you choose this, keep the shared 90% in a third file that both import or include, and let each runtime file hold only its own delta.

Whichever you choose, do not hard-code a runtime-specific call prefix into the shared body. A shared file names the skill in prose, with no prefix — "the alaa-security-review skill," not a call form — and a prefixed call form belongs only in a runtime-specific section. When deciding which call form belongs at a live invocation site, read `references/06-invocation-and-composition.md`, which owns the per-runtime call syntax.

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

Verified 24 July 2026. Values that move between releases:

- Claude Code's under-200-line target — guidance, not an enforced limit; `CLAUDE.md` files load in full regardless of length. The `MEMORY.md` 200-line / 25 KB cap governs auto memory only, not `CLAUDE.md`.
- Codex `project_doc_max_bytes` — 32 KiB default; `project_doc_fallback_filenames` is not documented to include `CLAUDE.md` — confirm against the running version before relying on it.
- Claude Code settings names (`claudeMd`, `claudeMdExcludes`) and the `.claude/rules/` mechanism — carry per-version notes; check against the running version.

## Sources

- [How Claude remembers your project (Claude Code)](https://code.claude.com/docs/en/memory)
- [Extend Claude with skills (Claude Code)](https://code.claude.com/docs/en/skills)
- [AGENTS.md (Codex)](https://developers.openai.com/codex/guides/agents-md)
- [Skills (Codex)](https://learn.chatgpt.com/docs/build-skills)
- [Latest model guide (OpenAI)](https://developers.openai.com/api/docs/guides/latest-model)
