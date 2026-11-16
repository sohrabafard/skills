# Noise Control Patterns

## Introduction

These commands express the rules in `SKILL.md`. Discovery and runtime sections govern context input; the rest govern printed output and bulk storage. Patterns are runtime-neutral unless a section names a runtime.

## Table of contents

- Discovery and bounded reads
- Runtime notes: Claude Code and Codex
- Diff and reporting patterns
- Large-log capture patterns
- Bash notes
- When the user wants raw output

## Discovery and bounded reads

`SKILL.md` *Part 1* owns the search, slice and capture rules. These commands express them:

- `rg -n "pattern" <paths>` to locate before reading.
- `rg -n -C 3 "pattern" <paths>` when the surrounding lines decide the answer.
- `rg -c "pattern" <paths>` or a file list when the question is "how widespread is this."
- a changed-file list instead of a full folder dump.

## Runtime notes: Claude Code and Codex

**Claude Code**

- Prefer file and search tools over shell commands: matching paths or lines are cheaper and more structured than terminal `rg` output, and explicit offsets and limits cost less than `cat` plus mental filtering.
- Dispatch independent searches in one turn so they run concurrently.
- Delegate a wide sweep across many files to a subagent, and require findings or paths, not excerpts. The sweep then consumes the child's context instead of the parent's.

**Codex**

Discovery mostly uses the shell, so express bounds in each command: scope every search to real paths, keep `-C` context small, and pipe through `head` or `tail` instead of emitting whole files.

## Diff and reporting patterns

Prefer these shapes to raw diff output: `git status --short`, `git diff --stat`, `git diff --name-only`, and `git diff -- <path>` for the one file that matters.

## Large-log capture patterns

Create or reuse a repo-local artifact directory, redirect the full command output there, and read back only the tail or the failing slice.

## Bash notes

```bash
rg -n -C 3 "MyPattern" src tests
sed -n '1,120p' path/file.txt
tail -n 80 path/file.txt
```

```bash
mkdir -p artifacts
pnpm test > artifacts/test.log 2>&1
tail -n 80 artifacts/test.log
```

Prefer `tail`, bounded `sed` or focused `rg -C` to full `cat` output. Use `git diff -- path/to/file` before showing larger diffs.

## When the user wants raw output

- State whether the output is file-local or repository-wide.
- Identify the most relevant section first.
- Keep unrelated raw outputs separate.

## Caveats

- The `rg`, `git` and Bash examples describe common cases, not portable guarantees. Before scripting them, verify flags and tool names against the installed shell and versions.
- Claude Code guidance describes general file and search operations. Exact tool parameters change between releases.
