# Noise Control Patterns

## Introduction

These patterns control context input and printed output. Discovery and runtime sections govern context input. Remaining patterns govern printed output and bulk storage. Patterns are runtime-neutral unless a section names a runtime.

## Table of contents

- Discovery and bounded reads
- Runtime notes: Claude Code and Codex
- Diff and reporting patterns
- Large-log capture patterns
- PowerShell notes
- Bash notes
- When the user wants raw output

## Discovery and bounded reads

Work down this order and stop at the first step that answers the question:

1. Search or inventory to locate the relevant path, symbol, or line range.
2. Read the bounded excerpt around the match.
3. Read the full file only when safe editing requires the whole file.
4. Summarize the result, not the material.

Prefer:

- `rg -n "pattern" <paths>` to locate before reading.
- `rg -n -C 3 "pattern" <paths>` when the surrounding lines decide the answer.
- `rg -c "pattern" <paths>` or a file list when the question is "how widespread is this."
- a changed-file list instead of a full folder dump.
- one well-chosen query instead of several exploratory ones.

Avoid by default:

- full-file dumps to prove a file was inspected;
- full directory trees, especially of generated output;
- Re-reading without a new reason. Your own edit, a failed check, or a changed hypothesis qualifies. Confirming content already in context does not qualify.
- Pulling a large result into context when a count, path, or slice answers the question. Large results are re-read on every later turn.

## Runtime notes: Claude Code and Codex

**Claude Code**

- Prefer file and search tools over shell commands. Matching paths or lines are cheaper and more structured than terminal `rg` output. Explicit offsets and limits cost less than `cat` plus mental filtering.
- Read only the range you need.
- Dispatch independent searches in one turn so they run concurrently.
- When a question needs a wide sweep across many files, delegate it to a subagent. Require findings or paths, not excerpts. The sweep then consumes the child's context instead of the parent's.

**Codex**

Discovery mostly uses the shell. Express bounds in each command:

- Scope every search to real paths.
- Keep `-C` context small.
- Pipe through `head`/`tail` or `Select-Object` instead of emitting whole files.

Route Codex-specific sandbox, refresh, locking, quoting, and command-length failures to `/alaa-codex-runtime-ops`. It has no Claude Code equivalent. Afterward, retry only essential failed work, serially and with bounded output.

## Diff and reporting patterns

Prefer these reporting shapes before raw diff output:

- `git status --short`
- `git diff --stat`
- `git diff --name-only`
- `git diff -- <path>` for the one file that matters

By default, report changes, reasons, validation, remaining risks or blockers, and saved artifact paths. Do not paste a repository-wide unified diff unless requested.

## Large-log capture patterns

When validation or diagnostics are long, keep the bulk out of both the transcript and the context window:

1. Create or reuse a repo-local artifact directory.
2. Redirect the full command output there.
3. Read back only the tail or the failing slice.
4. Report the key outcome and the path.

Keep durable artifacts only when they help the user inspect or resume. Remove throwaway artifacts before finishing when cleanup is safe.

## PowerShell notes

```powershell
rg -n -C 3 "MyPattern" src tests
Get-Content .\path\file.txt -TotalCount 120
Get-Content .\path\file.txt | Select-Object -Last 80
```

```powershell
New-Item -ItemType Directory -Force artifacts | Out-Null
pnpm test *> artifacts\test.log
Get-Content artifacts\test.log | Select-Object -Last 80
```

Notes:

- `*>` redirects all PowerShell streams to one file.
- Prefer `Select-Object -First` or `-Last` over dumping full content.
- Use `git status --short` and `git diff --stat` before any detailed diff.

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

Notes:

- Prefer `tail`, bounded `sed`, or focused `rg -C` over full `cat` output.
- Use `git diff -- path/to/file` before showing larger diffs.

## When the user wants raw output

- Obey explicit requests for full logs, full diffs, or full file contents.
- State whether the output is file-local or repository-wide.
- Identify the most relevant section first.
- Keep unrelated raw outputs separate.

## Caveats

- The `rg`, `git`, PowerShell, and Bash examples describe common cases, not portable guarantees. Before scripting them, verify flags and tool names against the installed shell and versions.
- Claude Code guidance describes general file and search operations. Exact tool parameters change between releases.
- `/alaa-codex-runtime-ops` is Codex-only. Do not look for a Claude Code counterpart.
