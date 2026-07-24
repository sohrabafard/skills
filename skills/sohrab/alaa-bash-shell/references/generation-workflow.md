# Generation and Refactor Workflow

## Contents

1. Requirement capture
2. Shell selection
3. Build order
4. Refactor order
5. Multi-script layout
6. Safe defaults
7. When to leave shell

## 1. Requirement capture

Before writing code, capture these facts:

- target shell
- target platforms
- required external commands
- input shape and output shape
- whether the script mutates state
- whether the script is a one-off helper, a reusable CLI, or a shared library
- whether the user wants portability or only local convenience

If the user did not specify a shell, infer from the task:

- choose Bash for richer maintainability on controlled systems
- choose POSIX `sh` for `/bin/sh`, Alpine, Debian packaging, init hooks, or minimal environments

## 2. Shell selection

Choose the smallest dialect that still does the job: Bash where its features earn their cost, POSIX `sh` where they do not. A dialect chosen for habit rather than need is a portability liability with no payoff.

### Choose Bash when you need

- arrays or associative arrays
- `[[ ]]`, `(( ))`, or `mapfile`
- process substitution
- clearer error handling with `pipefail`
- more maintainable multi-file tooling
- cleaner handling of complex argument parsing and data structures

### Choose POSIX `sh` when you need

- `/bin/sh` compatibility
- BusyBox `ash` or Debian `dash`
- minimal containers or rescue environments
- package maintainer scripts or other policy-driven shell usage

## 3. Build order

Generate in this order:

1. shebang and shell hints
2. file header
3. constants and global settings
4. `usage()` or `print_help()`
5. argument parser
6. validation and dependency checks
7. small focused helper functions
8. business logic
9. cleanup and trap wiring
10. `main`
11. validation and smoke tests

This order keeps the script readable and lets help, parsing, and validation stabilize early.

## 4. Refactor order

When improving an existing script:

1. identify the real interpreter from shebang and syntax
2. preserve behavior before changing structure
3. add or fix `-h` and `--help`
4. split long pipelines or large `case` arms into named functions
5. replace ambiguous globals with clearly named variables or arguments
6. add dependency checks and input validation
7. remove Bashisms only if portability is required
8. validate after each structural pass

Do not "simplify" by condensing logic into harder-to-debug one-liners.

## 5. Multi-script layout

For a small shell toolchain, prefer this layout:

```text
scripts/
  sync-cache.sh
  publish-report.sh
lib/
  project-common.sh
tests/
  sync-cache.bats
```

Rules:

- entrypoints stay small
- shared logic lives in a sourced library
- each entrypoint owns its own `usage()` text
- shared helpers are namespaced
- dependencies are documented once in the library and again in the entrypoint if user-facing

## 6. Safe defaults

### Bash CLI defaults

Use these defaults unless there is a reason not to:

- `#!/usr/bin/env bash`
- `set -euo pipefail` for straightforward CLI scripts
- `IFS=$'\n\t'`
- `main "$@"`

Caveat: do not apply `set -e` blindly to libraries or highly branchy scripts that intentionally handle failures inline. In those cases, prefer explicit status checks.

### POSIX `sh` defaults

Use these defaults unless there is a reason not to:

- `#!/bin/sh`
- `set -eu`
- no Bash-only syntax
- explicit pipeline restructuring instead of relying on `pipefail`

## 7. When to leave shell

Recommend another language when the task is dominated by:

- complex JSON or YAML business logic
- non-trivial date math across platforms
- concurrency with rich failure handling
- large in-memory data transforms
- network protocols, retries, or authentication logic that exceed simple command orchestration
- long-lived daemons or service processes

Use shell as glue. Use external tools or a fuller language for heavy lifting.
