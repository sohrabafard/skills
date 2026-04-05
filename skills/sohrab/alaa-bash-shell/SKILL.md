---
name: alaa-bash-shell
description: Generate, refactor, validate, debug, explain, and port Bash and POSIX shell scripts, including one-off utilities, multi-script toolchains, CI helpers, text-processing pipelines, and command wrappers. Use when the task involves .sh or .bash files, Bash-vs-sh decisions, mandatory -h/--help output, self-documenting shell code, ShellCheck/shfmt/checkbashisms/Bats workflows, Alpine BusyBox ash, Debian dash, or GNU/BSD/macOS portability. Do not use for zsh, fish, PowerShell, or for large systems that should be implemented in a fuller language instead of shell.
---

# Alaa Bash & Shell

One skill for the full shell lifecycle: generate, refactor, validate, debug, explain, and port Bash or POSIX shell code. This skill replaces split generator and validator workflows.

## Use this skill when

- The user wants one or more new or rewritten `.sh` or `.bash` files.
- The task involves Bash vs POSIX `sh` decisions, portability, or distro-specific behavior.
- The script must be self-documenting, readable, debuggable, and safe to maintain.
- The output must include `-h` and `--help`.
- The work needs static checks, format checks, smoke tests, or debug guidance.
- The task involves Alpine, BusyBox `ash`, Debian `dash`, macOS, GNU vs BSD tools, or shell-friendly CI.

## Do not use this skill when

- The target is `zsh`, `fish`, `PowerShell`, or Windows batch.
- The real solution should be Python, Go, Rust, or another fuller language and shell would only make the implementation brittle.
- The user is only asking for unrelated terminal usage with no script design, review, portability, or debugging component.

## First decisions

Before writing or editing code, make these decisions explicit:

1. **Target shell**
   - Default to **Bash** for controlled environments, richer ergonomics, arrays, associative arrays, `[[ ]]`, `mapfile`, process substitution, or more maintainable multi-file tooling.
   - Default to **POSIX `sh`** when the script will run as `/bin/sh`, inside minimal containers, in init/packaging hooks, or across Alpine, Debian, and other constrained systems.

2. **Platform matrix**
   - Note whether the script must work on Linux only, Linux plus macOS, Alpine, Debian, BusyBox, or mixed GNU/BSD environments.
   - Treat `/bin/sh` portability and external utility portability as separate concerns.

3. **Artifact shape**
   - Single CLI script.
   - Multiple entrypoints with a shared library.
   - Library-only shell module.
   - Script plus Bats smoke or regression tests.

## Output contract

Every generated or refactored user-facing CLI script must satisfy this contract unless the user explicitly asks for something narrower:

- Include a correct shebang.
- Include `-h` and `--help`, and make help exit successfully.
- Be self-documenting:
  - concise file header
  - clear function names
  - structured function docblocks for non-trivial functions
  - documented dependencies, environment variables, and exit codes
- Use the smallest shell dialect that still fits the job.
- Prefer readable control flow over dense one-liners.
- Make debugging practical with clear error messages and optional verbose or debug modes where appropriate.
- Validate before final delivery:
  - syntax check
  - ShellCheck when available
  - `shfmt` when available
  - `checkbashisms` when targeting `/bin/sh`
  - smoke `-h`/`--help` execution for CLI scripts

## Default workflow

1. Read the smallest relevant reference files from `references/`.
2. Decide the target shell and platform matrix.
3. Start from the closest template in `assets/templates/` when it helps.
4. Build or refactor in layers:
   - skeleton and help
   - argument parsing
   - validation and dependency checks
   - business logic
   - cleanup and exit handling
   - tests or smoke checks
5. Run `scripts/validate-shell.sh` when the environment can execute local tools.
6. If the task covers several scripts, factor shared logic into a sourced library instead of copying helpers between files.
7. In the final answer, state the shell target, portability assumptions, dependencies, and what was validated.

## Design rules

- Do not switch a script from Bash to `sh` by changing only the shebang.
- Do not promise POSIX portability if the script uses Bash-only syntax or GNU-only external flags.
- Prefer shell builtins for simple shell-native tasks, but prefer specialist tools for structured data and heavy search:
  - `awk` for stateful text transforms
  - `jq` for JSON
  - `yq` for YAML or mixed structured formats
  - `rg` and `fd` for fast repository-scale search
- Avoid external `getopt` for portable scripts. Prefer a manual `case` parser or `getopts` plus a tiny long-option pre-pass.
- Use `printf`, not `echo -e`, for predictable output.
- Be explicit when a dependency is non-portable or optional.
- When shell becomes an awkward fit, say so and recommend a better implementation language.

## Reference navigation

Start with `references/00-topic-map.md`, then read only what the task needs:

- `references/script-contract.md` for the mandatory script shape and self-documenting rules
- `references/generation-workflow.md` for build and refactor workflows
- `references/validation-and-debugging.md` for static checks, smoke tests, and debug tactics
- `references/portability-and-platforms.md` for Bash vs `sh`, Alpine, Debian, GNU/BSD, and macOS
- `references/tool-selection-and-performance.md` for command choice and performance heuristics
- `references/testing-and-ci.md` for Bats, pre-commit, and CI
- `references/patterns-and-examples.md` for reusable snippets and multi-script patterns
- `references/official-reference-map.md` for official external docs

## Bundled tools

- `scripts/new-script.sh`
  - Scaffold a new script from a bundled template.
- `scripts/validate-shell.sh`
  - Run syntax, ShellCheck, `shfmt`, `checkbashisms`, and optional help smoke checks.

## Templates

- `assets/templates/bash-cli-template.sh`
- `assets/templates/posix-cli-template.sh`
- `assets/templates/bash-lib-template.sh`
- `assets/templates/bats-test-template.bats`

## Subagent strategy

If multi-agent workflows are enabled, this skill benefits from parallel review passes:

- one agent for shell-target and portability analysis
- one agent for static validation and lint findings
- one agent for smoke tests, Bats coverage, or CI snippets

Keep the parent agent responsible for the final shell choice, final edits, and validation summary.

## Failure handling

- If the shell target is ambiguous, infer it from the environment and constraints. Favor Bash unless `/bin/sh`, BusyBox, `dash`, packaging, or strict portability is central.
- If a requested feature is incompatible with the target shell, either redesign it portably or clearly mark Bash as required.
- If a validator is unavailable, report that honestly and still do the checks that are possible.
