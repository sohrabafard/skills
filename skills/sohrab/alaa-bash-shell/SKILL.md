---
name: alaa-bash-shell
description: Bash and POSIX shell engineering for one-off utilities, multi-script toolchains, CI helpers, text-processing pipelines, and command wrappers. Use to generate, refactor, validate, debug, explain, or port scripts, or for .sh or .bash files, Bash-vs-sh decisions, mandatory -h/--help output, self-documenting shell code, ShellCheck/shfmt/checkbashisms/Bats workflows, Alpine BusyBox ash, Debian dash, or GNU/BSD/macOS portability. Do not use for zsh, fish, PowerShell, or for large systems that should be implemented in a fuller language instead of shell.
---

# Alaa Bash & Shell

One skill for the full Bash and POSIX shell lifecycle. Every rule with an owning reference is stated there, not here.

## First decisions

Settle these three decisions before you write or edit a line. They select every later reference.

1. **Target shell.** Use Bash where arrays, `[[ ]]`, `mapfile`, process substitution, or multi-file tooling earn their cost. Use POSIX `sh` for `/bin/sh`, minimal containers, init and packaging hooks, Alpine, and Debian. When the user did not say, `generation-workflow.md` owns the inference rule.
2. **Platform matrix.** Linux only, Linux plus macOS, Alpine or BusyBox, Debian, or mixed GNU/BSD. Answer `/bin/sh` portability and external utility portability separately.
3. **Artifact shape.** A single CLI, several entrypoints over a shared library, a library-only module, or a script plus Bats coverage. This shape decides two things: whether shared logic needs a sourced library, and whether tests are in scope.

## Non-negotiable rules

- Make every user-facing CLI satisfy `script-contract.md` in full, including `-h` and `--help`. Narrow it only on request, and say which part you dropped.
- Deliver nothing unvalidated. `validation-and-debugging.md` owns the check order. Run `scripts/validate-shell.sh` where local execution is possible.
- Shell is glue. When the task matches the leave-shell triggers in `generation-workflow.md`, say so and name the better language before you write code, not after.
- Terminal usage with no script design, review, portability, or debugging component is not this skill. Answer it directly.

## Reference navigation

Before you choose references, read `references/00-topic-map.md`. Load only the relevant routes.

## Bundled tools

`scripts/new-script.sh` scaffolds from `assets/templates/`. `scripts/validate-shell.sh` runs syntax, ShellCheck, `shfmt`, `checkbashisms`, the `--matrix` portability pass, and optional `--smoke-help` checks. Prefer both over hand-rolling the equivalent.

## When NOT to use

- The target shell is zsh, fish, or PowerShell. Their arrays, quoting and word-splitting differ from Bash and POSIX sh, so a rule taken from here can be silently wrong there.
- The program needs structured data, real concurrency, long-lived state, or a test suite beyond command-level checks. Write it in a fuller language and keep shell for process glue.
- The task is one interactive command with no script to keep, review, or run again.

## Delegation

Delegate only a genuinely independent lane that would otherwise flood the parent context. Portability inventory (shebangs, Bashisms, and GNU-only flags across a tree) and lint or format collection are bounded lanes. Their criteria are fixed before the lane starts, so they search and report rather than decide. Cross-platform redesign is a judgment lane: it starts with the decision open, namely how a Bash-only construct becomes portable, or whether the script should stop being shell.

Pick the model from the judgment the lane requires and the effort from the search that judgment needs. Hardcode no model name here. At dispatch, read `/alaa-prompting-guide`, specifically its `references/50-effort-and-thinking.md`, so routing follows the current roster, not a pin that goes stale.

The parent keeps the final shell choice, every edit, and the validation summary. Do not spawn a lane whose only job is to re-check another lane's output. Required artifact verification and review follow the active orchestrator's declared review boundary.

## Final report

State:

- the target shell
- the platform matrix and its assumptions
- the dependencies, and which are non-portable
- what you validated, and with which tool
- what remains unverified

## Failure handling

- A missing validator, an unexercisable platform, or an unrunnable smoke test is a reported gap. Run the checks that remain possible. Never report an absent check as passed.
- Redesign a feature that is incompatible with the target shell to be portable, or declare it Bash-only in the help text and the file header. Do not leave the conflict implicit.
