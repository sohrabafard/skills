---
name: alaa-makefile
description: Generate, validate, refactor, modernize, and debug GNU Make and .mk build files for local automation, CI entrypoints, packaging, install targets, and developer workflows. Use when the task involves `Makefile`, `makefile`, `*.mk`, phony targets, variable design, recursive make, shell-safety in recipes, mbake/checkmake/unmake validation, portability concerns, or converting ad-hoc commands into a maintainable Make-based workflow. Do not use it for unrelated shell scripts or CI YAML unless Makefile behavior is the real decision surface.
---

# Alaa Makefile

## What a Make target is

A Make target is a **local invocation of a command whose definition is owned elsewhere**. The skill
decides how the invocation is named, what it depends on and how it fails; it does not decide what the
command is. Its job is to make the local verdict identical to the runner's verdict. Three rules follow,
each with a checker in `scripts/validate_makefile.sh`:

1. A target fronting a CI gate runs the command the runner runs, with the same arguments, adds no flag
   the runner does not pass, and re-implements no part of the gate inline.
2. It passes when the gate passes and fails when the gate fails: no `-` prefix, no `|| true`. Make
   signals a failed recipe with its own exit status 2 rather than the recipe's status, so this is
   pass-or-fail parity, not numeric parity; a caller needing the gate's own number invokes the script
   directly instead of through Make.
3. This skill writes no provider YAML, no Dockerfile and no Compose file, and emits no model name and
   no effort key.

Owners across that boundary:
- `/alaa-gitlab-ci-cd` (`$alaa-gitlab-ci-cd`) owns how a gate is expressed on a runner. When a target
  and the runner job disagree about a command, the runner job is correct and the target changes.
- `/alaa-docker-production` (`$alaa-docker-production`) owns the Dockerfile, the image expression and
  the Compose file a target fronts, including the fail-closed interpolation invariant.
- `/alaa-frontend-devops` (`$alaa-frontend-devops`) owns the frontend gate register: which gates exist
  and what each asserts. A frontend target invokes a gate from that register and adds none.
- `/service-runtime-kit-governance` (`$service-runtime-kit-governance`) decides which generator
  variable expresses a runtime value when a target renders runtime files.

## Start fast

1. **Dialect.** GNU Make by default. Write POSIX-only Make when the file must run under BSD make or an
   `alpine` default shell, and record that in a first-line comment.
2. **Role.** CI entrypoint, build entrypoint, packaging workflow or developer convenience layer. The
   role fixes which reference the topic map sends you to.
3. **Recipe shell.** Set `SHELL := bash` whenever a recipe uses `source`, `[[`, an array, `declare`,
   `pipefail` or process substitution; otherwise recipes run under `/bin/sh`, which is `dash` on Debian
   and `ash` on Alpine, where those constructs fail.

Do not use this skill for shell scripts, CI YAML or package-manager scripts unless Make behaviour is
the decision surface, nor to replace a working repo-native task runner.

## Core authoring rules

- Every Makefile here opens with the six-line hardening preamble; a file omitting a line states in the
  comment above it which environment forbids it. `references/makefile-structure.md` holds the list.
- `?=` for user-overridable values, `:=` for immediate project-owned values.
- Every target that creates no file is declared in `.PHONY`.
- A directory prerequisite takes the order-only form `| $(DIR)`.
- A sub-make is `$(MAKE)`, never bare `make`, which loses `-j`, `-n` and the jobserver.
- Every target carries a `## ` documentation line. Target names are a contract: renaming one needs the
  same review as renaming a runner job.
- A recipe exceeding ten commands, or containing a loop, a conditional or a function definition, moves
  into a script under `scripts/` that the target invokes.

## Blocking defects

A review leaving any of these open does not pass. Each has a checker in `validate_makefile.sh`.

- `.ONESHELL:` without `-e` in `.SHELLFLAGS`, which makes a recipe exit 0 after an earlier command
  failed.
- `-` prefix or `|| true` on a recipe line invoking a gate, an image build, a Compose command or
  `$(MAKE)`.
- Bash-only constructs in a recipe when `SHELL` is not set to bash.
- Spaces where a recipe needs a tab; CRLF anywhere in the file.
- A credential-shaped assignment. Read it from the environment and fail closed:
  `API_TOKEN ?= $(error API_TOKEN is not set)`.
- A recipe re-implementing a command owned by `service-ci-kit` or `service-runtime-kit`.

## Validation

- `bash scripts/validate_makefile.sh <file>` on every change. `0` clean, `1` findings, `2` could not
  run; a caller treating `2` as a pass has no gate. `--no-venv` skips the mbake install on a prepared
  image; `--self-test` checks the checker.
- `make -n <target>`, diffed against the command the runner runs: that diff is the proof of parity.
- `make --shuffle=random -j$(nproc)` on GNU Make 4.4 or newer before claiming parallel safety.
- A portability finding on a GNU-only feature is resolved by confirming the feature is intentional, not
  by removing it; the first-line comment records that decision.

## Routing, and when not to use this skill

Each owner decides its matter; this skill states only how the invocation is shaped.

- `/alaa-bash-shell` (`$alaa-bash-shell`) — shell logic once a recipe becomes a script.
- `/alaa-k8s-helm` (`$alaa-k8s-helm`) — chart and release when a target runs `helm` or `kubectl`.
- `/caas-arvan-kuber` (`$caas-arvan-kuber`) — manifest and API versions when a target deploys to Arvan
  CaaS, whose Kubernetes version is pinned.
- `/alaa-reliability-sla` (`$alaa-reliability-sla`) — whether a target may retry, how long it may wait
  and what degradation is acceptable. This skill adds no retry and no timeout of its own.
- `/alaa-observability-soc` (`$alaa-observability-soc`) — what a failing target emits and what gates on
  it.
- `/alaa-services-contract` (`$alaa-services-contract`) — every shared name a target prints or passes:
  log fields, metric names, `OTEL_*` values, host ports.
- `/alaa-testing-strategy` (`$alaa-testing-strategy`) — what `test:` and `check:` assert.
- `/alaa-security-review` (`$alaa-security-review`) — review triggers and fail-closed doctrine when a
  target handles a secret, signature or credential.
- `/alaa-controlled-ops` (`$alaa-controlled-ops`) — change control when a target deploys or migrates.
- `/alaa-project-constitution` (`$alaa-project-constitution`) — the quality bar, at
  `alaa-project-constitution references/quality-bar.md`.
- `/alaa-prompting-guide` (`$alaa-prompting-guide`) — every model and effort question, at
  `alaa-prompting-guide references/50-effort-and-thinking.md`.

## Deliverables

Generation returns a Makefile matching the repository's real workflow and names the command each target
fronts. Review separates blocking defects from improvements and quotes the validator's exit code. A
refactor preserves target names and user-facing behaviour unless the task authorises a contract change.

`references/00-topic-map.md` is the router. `references/SOURCES.md` is the provenance ledger and carries
the command that re-derives every pinned version.
