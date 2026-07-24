# Testing and CI

## Contents

1. Smoke tests
2. Bats patterns
3. Pre-commit snippet
4. CI snippet
5. Repository review checklist

## 1. Smoke tests

For every user-facing CLI, start with:

```bash
./script.sh -h
./script.sh --help
```

Then add one success path and one failure path with realistic fixtures.

Strong smoke tests also cover:

- files with spaces in names
- empty inputs
- missing dependencies
- invalid arguments
- repeated execution when idempotence matters

## 2. Bats patterns

Use Bats when the script is important enough to deserve regression coverage.

Typical Bats assertions:

- help text exits with code 0
- missing argument exits with code 2
- normal execution creates the expected file or stdout
- invalid input prints a useful message to stderr
- dry-run mode performs no mutation

Example:

```bash
#!/usr/bin/env bats

@test "help exits successfully" {
  run ./sync-cache.sh --help
  [ "$status" -eq 0 ]
  [[ "$output" == *"Usage:"* ]]
}

@test "missing arguments exits with usage error" {
  run ./sync-cache.sh
  [ "$status" -eq 2 ]
  [[ "$output" == *"Usage:"* ]]
}
```

Note: `.bats` files are executed by Bats. They are not a substitute for plain shell source files and should be validated with `bats`, not with a plain `bash -n` syntax pass.

## 3. Pre-commit snippet

```yaml
repos:
  - repo: local
    hooks:
      - id: shellcheck
        name: shellcheck
        entry: shellcheck
        language: system
        types: [shell]
      - id: shfmt
        name: shfmt
        entry: shfmt -w
        language: system
        types: [shell]
```

If the repository uses both Bash and POSIX shell, keep shebangs accurate so linters and formatters infer the right dialect.

## 4. CI snippet

A minimal GitHub Actions job:

```yaml
name: shell

on:
  push:
  pull_request:

jobs:
  lint-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - name: Install tools
        run: sudo apt-get update && sudo apt-get install -y shellcheck shfmt devscripts bats
      - name: Lint
        run: |
          shellcheck scripts/*.sh
          shfmt -d scripts/*.sh
          checkbashisms scripts/*.sh || true
      - name: Test
        run: bats tests
```

Use `checkbashisms` only for files that are intended to be POSIX shell.

Two parts of this snippet move independently of the shell code and must be checked before it is copied: the major version of `actions/checkout` (`v7` is the version its README recommends as of 2026-07-24, and this pin has moved several majors in recent years), and whether the runner image's package repositories still carry `shfmt` and `bats` under those names. Install from upstream releases instead when the distribution packages lag the versions the repository expects.

## 5. Repository review checklist

For a shell-heavy repository, confirm:

- all shebangs match the real dialect
- user-facing CLIs have `-h` and `--help`
- ShellCheck runs cleanly or suppressions are justified
- `shfmt` formatting is stable
- `/bin/sh` files are reviewed with portability in mind
- the hottest scripts have at least smoke or Bats coverage
