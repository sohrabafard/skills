---
name: alaa-makefile
description: Generate, validate, refactor, modernize, and debug GNU Make and .mk build files for local automation, CI entrypoints, packaging, install targets, and developer workflows. Use when the task involves `Makefile`, `makefile`, `*.mk`, phony targets, variable design, recursive make, shell-safety in recipes, mbake/checkmake/unmake validation, portability concerns, or converting ad-hoc commands into a maintainable Make-based workflow. Do not use it for unrelated shell scripts or CI YAML unless Makefile behavior is the real decision surface.
---

# Alaa Makefile

Use this as the single entrypoint for the full Makefile lifecycle: authoring, review, validation, hardening, refactoring, and debugging.

This skill replaces the old split `makefile-generator` and `makefile-validator` workflow with one routing-first skill that keeps context small while still preserving the deeper references and scripts.

## Start fast

Make these decisions before editing:

1. **Make dialect**
   - Default to GNU Make when the repo already relies on GNU features, `bash`, pattern rules, or developer tooling that assumes GNU behavior.
   - Prefer stricter POSIX compatibility only when the target environment really needs it.
2. **File role**
   - project build entrypoint
   - CI wrapper or task runner
   - install/package workflow
   - local developer convenience layer
3. **Recipe shell model**
   - Decide whether recipes must stay portable under `/bin/sh`
   - Or whether the repo should explicitly use `bash` with `.ONESHELL` and safe shell flags
4. **Validation surface**
   - static syntax only
   - style/formatting
   - security and hardening
   - portability
   - runtime smoke check on real targets

## When NOT to use

- Do not use for shell scripts, CI YAML, or package-manager scripts unless Make behavior is the decision surface.
- Do not use to replace a working repo-native task runner without a clear Makefile requirement.
- Do not use for build-system migrations outside GNU Make scope.

## Default operating model

- **Routing-first**: Open the smallest reference that matches the task instead of loading every Makefile guide.
- **GNU-safe by default**: Use modern GNU Make patterns when the repo already depends on them.
- **Reviewable first**: Prefer small, explicit targets and clear variables over clever macro-heavy Makefiles.
- **Shell-aware**: Treat recipe safety as part of the Makefile design, not as an afterthought.
- **Freshness-aware**: Read `references/SOURCES.md` when GNU Make, POSIX make, validation tooling, latest/current behavior, or security-sensitive recipe behavior matters.
- **Validation before closeout**: Run the bundled validator script and any cheap repo-specific smoke checks before finishing.

## Task lanes

### Generate or redesign a Makefile

Read:

- `references/makefile-structure.md`
- `references/variables-guide.md`
- `references/targets-guide.md`
- `references/patterns-guide.md`

Use this lane for:

- creating a new `Makefile` or `.mk` file
- replacing ad-hoc command docs with real targets
- adding install, clean, dist, test, or help targets
- introducing language-specific build patterns

If you need the preserved long-form workflow, open `references/authoring-full-guide.md`.

### Validate, review, or harden an existing Makefile

Read:

- `references/best-practices.md`
- `references/common-mistakes.md`
- `references/security-guide.md`
- `references/optimization-guide.md`

Use this lane for:

- code review
- cleanup or modernization
- security and safety checks
- performance and maintainability improvements
- converting fragile legacy Makefiles into safer patterns

### Validate with tooling

Read:

- `references/bake-tool.md`
- `references/validation-full-guide.md`

Use this lane for:

- `mbake` formatting and validation
- `checkmake` linting
- `unmake` portability checks
- CI or pre-commit validation wiring

Use the bundled script:

- `scripts/validate_makefile.sh`

### Add or scaffold standard targets quickly

Use:

- `scripts/generate_makefile_template.sh`
- `scripts/add_standard_targets.sh`

These are good for deterministic scaffolding, but do not stop there. Review the output against the repo's actual build, install, and test behavior.

## Core authoring rules

- Prefer a clear header and special-target preamble when the repo benefits from GNU Make hardening:
  - `SHELL := bash`
  - `.ONESHELL:`
  - `.SHELLFLAGS := -eu -o pipefail -c`
  - `.DELETE_ON_ERROR:`
  - `MAKEFLAGS += --warn-undefined-variables`
  - `MAKEFLAGS += --no-builtin-rules`
- Use `?=` for user-overridable values and `:=` for immediate project-owned values.
- Keep `.PHONY` accurate and explicit.
- Use order-only prerequisites for directories when that avoids timestamp-driven rebuild noise.
- Prefer `$(MAKE)` for recursive calls, never bare `make`.
- Keep help output and target names stable enough for humans and CI to rely on.

## Validation rules

- Run `scripts/validate_makefile.sh <file>` for any non-trivial change.
- Use `make -n`, `make help`, or a narrow real target when a smoke check is cheap and safe.
- Treat recipe indentation, shell failure behavior, credential leakage, and unsafe variable expansion as high-priority issues.
- If portability matters, check whether GNU-only features are intentional before "fixing" them away.

## Companion routing

- Pair with `$alaa-bash-shell` when recipe complexity becomes shell-script complexity.
- Pair with `$alaa-gitlab-ci-cd` when the Makefile is the operator surface for GitLab jobs or release automation.
- Pair with `$alaa-docker-production` when targets mainly wrap image builds, Compose, or production container workflows.
- Pair with `$alaa-k8s-helm` when Make targets are wrappers around Helm or Kubernetes operations.
- Pair with `$caas-arvan-kuber` when Make targets enforce Arvan-safe delivery behavior.

## Reference navigation

- Fast router:
  - `references/00-topic-map.md`
- Authoring and generation:
  - `references/makefile-structure.md`
  - `references/variables-guide.md`
  - `references/targets-guide.md`
  - `references/patterns-guide.md`
  - `references/authoring-full-guide.md`
- Review, safety, and optimization:
  - `references/best-practices.md`
  - `references/common-mistakes.md`
  - `references/security-guide.md`
  - `references/optimization-guide.md`
- Validation tooling:
  - `references/bake-tool.md`
  - `references/validation-full-guide.md`
- Official-first source map:
  - `references/SOURCES.md`

## Deliverable rules

- For generation tasks, return a ready-to-use Makefile that matches the repo's real workflow.
- For review tasks, separate blocking defects, safety risks, and improvement suggestions.
- For refactors, preserve target names and user-facing behavior unless the task explicitly authorizes a contract change.
- State what you validated: syntax, formatting, safety checks, portability checks, and any smoke-run targets.

## Maintenance rules

- Keep this file routing-first and compact.
- Keep detailed reference material in `references/`.
- Keep the scripts usable as standalone helpers, but do not let them become the only documented workflow.
- Re-check official GNU Make, POSIX, and validation-tool sources when latest, current, version, or security behavior matters.
- When ownership changes, update companion routing and pack-level docs in the same patch.
