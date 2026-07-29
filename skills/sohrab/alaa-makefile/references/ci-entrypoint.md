# A Make target as a local invocation of a CI gate

This is the file the skill exists for on this fleet. It owns gate fronting, exit-status propagation, the
`make -n` diff, and what a target prints when it fails.

## The situation this file addresses

`service-ci-kit` publishes eleven gate scripts under `ci/scripts/`, and the shared GitLab pipeline
invokes them from `gitlab/platform-app-php-service.yml` as, for example:

```yaml
- bash .service-ci-kit/ci/scripts/build_image.sh
- bash .service-ci-kit/ci/scripts/release.sh
```

`service-runtime-kit` publishes four scripts under `scripts/`: `render-runtime.sh`,
`validate-runtime.sh`, `up-local.sh` and `test-fail-closed-interpolation.sh`. There is no local
entrypoint for either set, so a developer who wants to run a gate the way the runner runs it must read
the YAML and copy the command by hand. Copying by hand is how the local verdict and the runner's verdict
diverge.

A Makefile closes that gap and adds exactly one thing: **a second, local caller of the same command**.

## The rule

> A Make target is a local invocation of a command whose definition is owned elsewhere. This skill
> decides how the invocation is named, ordered, made re-runnable and made to fail loudly. It does not
> decide what the command is.

`/alaa-gitlab-ci-cd` (`$alaa-gitlab-ci-cd`) owns how a gate is expressed on a runner. When a target and
the runner job disagree about a command, the runner job is correct and the target changes.
`/alaa-docker-production` (`$alaa-docker-production`) owns the Dockerfile, the image expression and the
Compose file. This skill writes none of those files.

## Four checkable consequences

### 1. Same command, same arguments

A target that fronts a gate contains the gate's command and nothing else on that line. It adds no flag
the runner does not pass, removes none the runner does pass, and re-implements no part of the gate.

```makefile
CI_KIT ?= .service-ci-kit/ci/scripts

## Build and push the service image through the kit gate
ci/build:
	bash $(CI_KIT)/build_image.sh
```

Wrong, because the target now decides something the kit owns:

```makefile
ci/build:
	docker build -t $(IMAGE) .
	docker push $(IMAGE)
```

`scripts/validate_makefile.sh` reports the second form as a fleet-boundary finding and names
`ci/scripts/build_image.sh` as the owner. Disable that check with `--no-fleet-checks` only in a
repository that is not on this fleet.

### 2. The verdict passes through unmodified

Three constructs destroy a verdict, and all three are blocking:

| Construct | What it does | Replacement |
|---|---|---|
| `-command` | make ignores the command's exit status entirely | delete the `-`; make the command tolerate the condition itself, for example `rm -f` rather than `-rm` |
| `command \|\| true` | converts every failure into success | delete `\|\| true`; if one specific failure is acceptable, test for that condition explicitly and `exit 0` only for it |
| `.ONESHELL:` without `-e` in `.SHELLFLAGS` | the whole recipe is one shell whose status is its **last** command's status | `.SHELLFLAGS := -eu -o pipefail -c` |

The third is the one that hides. This Makefile prints its message and exits 0 while the deploy did not
happen; it ships as `scripts/fixtures/oneshell-swallow.mk` so the repair stays proven:

```makefile
SHELL := bash
.ONESHELL:

deploy:
	cd /nonexistent
	echo "still ran - failure was swallowed"
```

```console
$ make -f oneshell-swallow.mk deploy ; echo "exit=$?"
bash: line 1: cd: /nonexistent: No such file or directory
still ran - failure was swallowed
exit=0
```

**Parity is pass-or-fail, not numeric.** GNU Make signals a failed recipe with its own exit status 2
regardless of what the recipe returned; it prints the recipe's number in the message
(`make: *** [Makefile:6: g] Error 7`) but does not adopt it. A caller that needs the gate's own number
invokes the script directly rather than through Make. State this in the target's `##` line when it
matters to a caller.

### 3. `make -n` is the diff against the runner

`make -n <target>` prints the command without running it. Diff that output against the runner's
`script:` line; when the two differ, one of them is wrong and the runner is authoritative.

```console
$ make -n ci/build
bash .service-ci-kit/ci/scripts/build_image.sh
```

That single line is the operative proof of parity, and it is the artifact to paste into a review. Run it
on every target that fronts a gate, not only on the one being changed, because a shared variable can
move a command that nobody edited.

`make -n` does not expand `$(shell …)` lazily, so a target whose command is assembled by a recursive
variable prints something different from what it runs. Assign such variables with `:=`
(`variables-guide.md` owns that rule) so the printed command is the executed command.

### 4. A failing target names the command and the status

A developer's first sight of a failure is this Makefile's output, so a target that fronts a gate makes
three things identifiable without re-running anything: which target failed, which command it ran, and
what that command exited with. Make's own default output already carries all three, so the rule is
mostly a prohibition:

- Do not prefix a gate command with `@`. Silencing the echo removes the command from the log, and the
  command is the thing a reader needs. Use `@` on `echo`, on `sed`, and on nothing that can fail.
- Do not pipe a gate's output through a filter without `set -o pipefail`, which the mandated
  `.SHELLFLAGS` already provides.
- Do not add a `|| echo "failed"` tail. It converts the failure into success and replaces the command's
  own diagnostics with a shorter, less useful line.

What a failing target must emit beyond that — a metric, a structured log field, an alert — is decided by
`/alaa-observability-soc` (`$alaa-observability-soc`), and the names it uses are decided by
`/alaa-services-contract` (`$alaa-services-contract`). This skill states none of them.

Whether a target may retry a gate, how long it may wait for one, and what degradation is acceptable are
decided by `/alaa-reliability-sla` (`$alaa-reliability-sla`). A Makefile in this fleet adds no retry loop
and no timeout of its own; when one is needed, it belongs inside the owning script, where the runner gets
it too.

## Naming targets against the kit

Namespace the target after the kit that owns the command, and name the target after the gate rather than
after the tool it happens to use. `ci/build` survives a move from `docker build` to `buildx`;
`docker-build` does not.

| Target | Command it fronts | Owner |
|---|---|---|
| `ci/tag` | `bash $(CI_KIT)/make_tag_version.sh` | service-ci-kit |
| `ci/build` | `bash $(CI_KIT)/build_image.sh` | service-ci-kit |
| `ci/release` | `bash $(CI_KIT)/release.sh` | service-ci-kit |
| `ci/db-ready` | `bash $(CI_KIT)/check_db_ready.sh` | service-ci-kit |
| `ci/verify-secret` | `bash $(CI_KIT)/verify_app_secret.sh` | service-ci-kit |
| `ci/db-privileges` | `bash $(CI_KIT)/ensure_db_privileges.sh` | service-ci-kit |
| `ci/migrate` | `bash $(CI_KIT)/migrate_db.sh` | service-ci-kit |
| `ci/deploy` | `bash $(CI_KIT)/deploy.sh` | service-ci-kit |
| `ci/db-export` | `bash $(CI_KIT)/export_db.sh` | service-ci-kit |
| `runtime/render` | `bash $(RUNTIME)/render-runtime.sh --repo-root .` | service-runtime-kit |
| `runtime/validate` | `bash $(RUNTIME)/validate-runtime.sh --repo-root .` | service-runtime-kit |
| `runtime/interpolation` | `bash $(RUNTIME)/test-fail-closed-interpolation.sh` | service-runtime-kit |
| `runtime/up` | `bash scripts/docker/up-local.sh $(COMPOSE_MODE)` | service-runtime-kit |

`scripts/generate_makefile_template.sh fleet <name>` writes exactly this file, preamble included, and
`--self-test` asserts that what it writes passes `validate_makefile.sh` with exit 0.

Renaming any of these targets is a contract change: a runner job, a developer's muscle memory and another
skill's route may all name it. Treat it as you would renaming a runner job.

## Prerequisites express the runner's ordering, not a shortcut

A gate that the runner runs after another gate gets the same ordering locally:

```makefile
## Run the deploy gate; the pipeline runs migrations first
ci/deploy: ci/migrate
	bash $(CI_KIT)/deploy.sh
```

Do not invent an ordering the pipeline does not have, and do not collapse two runner jobs into one
target. Both make the local run pass in a case the pipeline fails. Where a target genuinely must not run
concurrently with another, `optimization-guide.md` owns `.NOTPARALLEL` and `.WAIT`.

## Re-runnability

A gate target is run repeatedly by a developer, so it is phony and it is idempotent to the extent the
underlying script is. When the script is not idempotent — `ci/db-export` writes a timestamped file,
`ci/release` cuts a tag — say so in the `##` line. Do not add a guard that skips the command, because
that is the target deciding something the kit owns.

## What this file does not decide

- The content of a gate script: `service-ci-kit` and its owners.
- How the gate appears in `.gitlab-ci.yml`: `/alaa-gitlab-ci-cd` (`$alaa-gitlab-ci-cd`).
- The Dockerfile, image expression or Compose file: `/alaa-docker-production`
  (`$alaa-docker-production`); target shape for those commands is in
  `compose-and-container-targets.md`.
- Which generator variable expresses a runtime value: `/service-runtime-kit-governance`
  (`$service-runtime-kit-governance`).
- What the `test:` target must assert: `/alaa-testing-strategy` (`$alaa-testing-strategy`).
