---
name: alaa-bash-shell
description: Generate, refactor, validate, debug, explain, and port Bash and POSIX shell scripts, including one-off utilities, multi-script toolchains, CI helpers, text-processing pipelines, and command wrappers. Use when the task involves .sh or .bash files, Bash-vs-sh decisions, mandatory -h/--help output, self-documenting shell code, ShellCheck/shfmt/checkbashisms/Bats workflows, Alpine BusyBox ash, Debian dash, or GNU/BSD/macOS portability. Do not use for zsh, fish, PowerShell, or for large systems that should be implemented in a fuller language instead of shell.
---

# Alaa Bash & Shell

One skill for the full Bash and POSIX shell lifecycle. Every rule with an owning reference is stated there, not here.

## First decisions

Settle these three before writing or editing a line; they select every reference that follows.

1. **Target shell.** Bash where arrays, `[[ ]]`, `mapfile`, process substitution, or multi-file tooling earn their cost. POSIX `sh` for `/bin/sh`, minimal containers, init and packaging hooks, Alpine, and Debian. When the user did not say, `generation-workflow.md` owns the inference rule.
2. **Platform matrix.** Linux only, Linux plus macOS, Alpine or BusyBox, Debian, or mixed GNU/BSD. `/bin/sh` portability and external utility portability are separate questions needing separate answers.
3. **Artifact shape.** A single CLI, several entrypoints over a shared library, a library-only module, or a script plus Bats coverage. This decides whether shared logic needs a sourced library and whether tests are in scope.

## Non-negotiable rules

- Every user-facing CLI satisfies `script-contract.md` in full, including `-h` and `--help`. Narrow it only on request, and say which part was dropped.
- Nothing is delivered unvalidated. `validation-and-debugging.md` owns the check order; run `scripts/validate-shell.sh` where local execution is possible.
- Shell is glue. When the task matches the leave-shell triggers in `generation-workflow.md`, say so and name the better language before writing code, not after.
- Terminal usage with no script design, review, portability, or debugging component is not this skill. Answer it directly.

## Reference navigation

`references/00-topic-map.md` maps task shape to the smallest sufficient set. Rule owners, all under `references/`:

- `script-contract.md` — script shape, help contract
- `generation-workflow.md` — build and refactor order, defaults, leaving shell
- `validation-and-debugging.md` — check order, tracing, failures
- `portability-and-platforms.md` — Bash vs `sh`, Alpine, Debian, GNU/BSD, macOS
- `tool-selection-and-performance.md` — command choice, performance
- `testing-and-ci.md` — smoke tests, Bats, pre-commit, CI
- `patterns-and-examples.md` — reusable snippets
- `official-reference-map.md` — external docs, freshness triggers

## Bundled tools

`scripts/new-script.sh` scaffolds from `assets/templates/`. `scripts/validate-shell.sh` runs syntax, ShellCheck, `shfmt`, `checkbashisms`, the `--matrix` portability pass, and optional `--smoke-help` checks. Prefer both over hand-rolling the equivalent.

## Delegation

Delegate only a lane that is genuinely independent and would otherwise flood the parent context. Portability inventory — shebangs, Bashisms, and GNU-only flags across a tree — and lint or format collection are bounded lanes: their criteria are fixed before the lane starts, so they search and report rather than decide. Cross-platform redesign is a judgment lane, because the decision is still open when it starts: how a Bash-only construct becomes portable, or whether the script should stop being shell.

Pick the model from the kind of judgment the lane requires and the effort from how much search that judgment needs. Do not hardcode a model name here; read `/alaa-prompting-guide` (`$alaa-prompting-guide`), specifically its `references/50-effort-and-thinking.md`, at dispatch time so routing follows the current roster instead of a pin that quietly goes stale.

The parent keeps the final shell choice, every edit, and the validation summary. Do not spawn a lane whose only job is to re-check another lane's output.

## Final report

State the target shell, the platform matrix and its assumptions, the dependencies and which are non-portable, what was validated and with which tool, and what remains unverified.

## Failure handling

- A missing validator, an unexercisable platform, or an unrunnable smoke test is a reported gap. Run the checks that remain possible; never report an absent check as passed.
- A feature incompatible with the target shell is either redesigned portably or declared Bash-only in the help text and the file header. Do not leave the conflict implicit.
