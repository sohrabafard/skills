# Noise Control Patterns

These commands express the rules of `SKILL.md` *Part 1* and *Part 2*. They are common cases: verify a flag against the installed tool before you script it.

## Discovery and bounded reads

- `rg -n "pattern" <paths>` to locate before you read.
- `rg -n -C 3 "pattern" <paths>` when the surrounding lines decide the answer.
- `rg -c "pattern" <paths>` or a file list when the question is how widespread something is.
- `sed -n '1,120p' path/file.txt` or `tail -n 80 path/file.txt` for a bounded slice where the runtime reads files through the shell.

**Codex.** Discovery mostly uses the shell, so put the bounds in each command: scope every search to real paths, keep `-C` context small, and pipe through `head` or `tail` instead of printing a whole file.

**Claude Code.** Delegate a wide sweep across many files to a subagent, and require findings or paths, not excerpts. The sweep then consumes the child's context instead of the parent's.

## Diffs

Use `git status --short`, `git diff --stat` and `git diff --name-only`, then `git diff -- <path>` for the one file that matters.

## Large logs

Redirect the full output to a repo-local artifact directory, then read back only the tail or the failing slice:

```bash
mkdir -p artifacts
pnpm test > artifacts/test.log 2>&1
tail -n 80 artifacts/test.log
```
