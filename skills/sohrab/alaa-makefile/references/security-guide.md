# Makefile security

**Owner of:** credentials in and around a Makefile, validation of untrusted values, shell injection,
path traversal, temporary files, download verification, and what must not reach a build log or an image
layer. Read this first in any review lane.

`/alaa-security-review` (`$alaa-security-review`) decides review triggers, threat classes and what must
fail closed. This file states how those decisions are expressed in Make.

## Credentials

### Never a literal

```makefile
# wrong
DB_PASSWORD := hunter2
AWS_SECRET := AKIAIOSFODNN7EXAMPLE
```

`scripts/validate_makefile.sh` reports any credential-shaped assignment as an error. The pattern covers
`password`, `secret`, `api_key`, `token`, `private_key`, `aws_*`, `github_token`, `database_url`,
`ssh_key`, `ssl_key` and `encryption_key`.

### Fail closed, do not default

```makefile
API_TOKEN ?= $(error API_TOKEN is not set; export it or load it from the secret store)
DB_PASSWORD ?= $(error DB_PASSWORD is not set)
```

`$(error …)` inside `?=` is deferred, so it fires when the variable is referenced. A target that does not
need the credential still runs, and a target that needs it stops before doing half its work. A default is
never correct for a credential: a default that works is a credential in the file, and a default that does
not work turns an authentication failure into an obscure one.

### Fetch at use, do not cache in a Make variable

```makefile
## Deploy using a credential fetched at run time
deploy:
	DB_PASSWORD="$$(vault kv get -field=password secret/database)" ./deploy.sh
```

The value lives in the recipe's shell and never becomes a Make variable, so it cannot leak through
`make -p`, through `.EXPORT_ALL_VARIABLES:` or into a sub-make's environment.

### `.env` files

```makefile
-include .env
export DATABASE_URL APP_KEY
```

`-include` rather than `include`, so a developer without the file still gets a usable Makefile. Export
the specific names; a bare `export` or `.EXPORT_ALL_VARIABLES:` sends every variable to every subprocess
and the validator reports it. Confirm `.env` is in `.gitignore` before writing the `-include`.

Note that a Compose file does **not** read this. Compose interpolates from the shell environment and
`--env-file` only, never from a service-level `env_file:` key; `/alaa-docker-production`
(`$alaa-docker-production`) owns that invariant, and `compose-and-container-targets.md` states how a
target passes `--env-file`.

## Keeping secrets out of logs and layers

```makefile
# wrong: the token is in the build log
deploy:
	curl -H "Authorization: Bearer $(API_TOKEN)" https://api.example.com/

# right: suppress the echo, and read the value in the shell
deploy:
	@curl -H "Authorization: Bearer $$API_TOKEN" https://api.example.com/
```

`@` is correct here and only here. `ci-entrypoint.md` forbids `@` on a gate command, because silencing a
gate hides the command a reader needs; the resolution is that a command carrying a secret is not written
inline in a Makefile at all — it goes into a script, and the target invokes the script.

```makefile
# wrong: --build-arg values are recorded in the image's layer history
image/build:
	docker build --build-arg API_KEY=$(API_KEY) -t $(IMAGE) .

# right: BuildKit secrets are mounted for one RUN and are not committed to a layer
image/build:
	DOCKER_BUILDKIT=1 docker build --secret id=api_key,src=$(API_KEY_FILE) -t $(IMAGE) .
```

The Dockerfile side of that — the `RUN --mount=type=secret` line — belongs to
`/alaa-docker-production` (`$alaa-docker-production`).

## Untrusted values

A value that comes from the command line, the environment or a CI variable is untrusted. Quoting alone
is not enough when the value is interpolated into a command the shell will parse.

### Allow-list, do not sanitise

```makefile
ALLOWED_ENVS := dev staging prod
ENVIRONMENT ?= dev

## Deploy to ENVIRONMENT, which must be one of ALLOWED_ENVS
deploy:
	@echo "$(ALLOWED_ENVS)" | tr ' ' '\n' | grep -qxF "$(ENVIRONMENT)" \
	  || { echo "ERROR: ENVIRONMENT must be one of: $(ALLOWED_ENVS)" >&2; exit 1; }
	./deploy.sh "$(ENVIRONMENT)"
```

An allow-list states what is permitted. A deny-list or a character-stripping filter states what someone
already thought of, and is defeated by the next encoding.

### Quote every expansion that reaches a shell

```makefile
# wrong: a space or a semicolon in USER_INPUT becomes new arguments or a new command
process:
	./script.sh $(USER_INPUT)

# right
process:
	./script.sh '$(USER_INPUT)'
```

Single quotes stop the shell expanding the value. They do not stop a value that itself contains a single
quote, which is why the allow-list above comes first.

### Three constructs that are never acceptable

```makefile
run-command:  ; $(USER_COMMAND)      # the value IS the command
execute:      ; echo $(INPUT) | sh   # the value becomes a script
eval-input:   ; @eval $(USER_INPUT)  # the value becomes shell source
```

There is no safe form of these. Replace them with a fixed command that takes the value as an argument
after the allow-list check.

## Path traversal

```makefile
DATA_DIR := ./data

## Print a file from DATA_DIR
show:
	@case "$(FILE)" in \
	  $(DATA_DIR)/*) [ -f "$(FILE)" ] && cat "$(FILE)" ;; \
	  *) echo "ERROR: FILE must be inside $(DATA_DIR)" >&2; exit 1 ;; \
	esac
```

The prefix test is necessary and not sufficient: `./data/../../etc/passwd` has the right prefix. Resolve
the path before comparing when the value is genuinely hostile, or hold the allowed names in a variable
and match against that list instead.

## Destructive commands

```makefile
# wrong: an unset or wrong BUILD_DIR makes this catastrophic
clean:
	rm -rf $(BUILD_DIR)/*

# right
BUILD_DIR ?= build

clean:
	@case "$(BUILD_DIR)" in \
	  ''|/|/*) echo "ERROR: refusing to clean '$(BUILD_DIR)'" >&2; exit 1 ;; \
	esac
	rm -rf -- "$(BUILD_DIR)"
```

Three separate protections: a default so the variable is never empty,
`MAKEFLAGS += --warn-undefined-variables` from the preamble so a typo is reported, and a guard that
refuses an absolute path. The validator reports `rm -rf`, `sudo`, `curl` and `wget` driven by a variable
the file never defines.

## Temporary files

```makefile
render:
	TMPFILE="$$(mktemp)"
	trap 'rm -f "$$TMPFILE"' EXIT
	./generate-config > "$$TMPFILE"
	./install-config "$$TMPFILE"
```

`mktemp` with no argument uses `TMPDIR` and creates the file with mode 600, so a predictable name in a
world-writable directory cannot be pre-created by someone else. The `trap` needs `.ONESHELL:` to be in
scope for the whole recipe, which the mandated preamble provides.

Never create a scratch directory inside the repository. On this fleet the checkout is read-only in
places, and a leftover directory changes what `$(wildcard …)` returns on the next run.

## Downloads

```makefile
CURL := curl --proto '=https' --tlsv1.2 -fsSL

fetch:
	$(CURL) -o package.tar.gz https://example.com/package.tar.gz
	$(CURL) -o package.tar.gz.sha256 https://example.com/package.tar.gz.sha256
	sha256sum -c package.tar.gz.sha256
```

`--proto '=https'` refuses to follow a redirect to plain HTTP, `--tlsv1.2` sets a floor, `-f` makes an
HTTP error status a non-zero exit rather than a downloaded error page, and `-S` keeps the error message
while `-s` suppresses the progress meter. Verify the checksum or a GPG signature from a *different*
source than the artifact; a checksum served beside the file by the same compromised host proves nothing.

Never pipe a download to a shell.

## File permissions

```makefile
install-config:
	install -d -m 700 $(DESTDIR)/var/lib/$(PROJECT)/secrets
	install -m 600 config.secret $(DESTDIR)/etc/$(PROJECT)/
```

Set the mode in the same command that creates the file. A `chmod` afterwards leaves a window in which the
file exists with the default mode.

## Audit trail

A Makefile is a developer's local tool and is not the system of record for who deployed what. Do not
write an audit log to a fixed host path from a recipe: the path may not exist, may not be writable, and
is not collected. What must be emitted when a privileged target runs, and where it goes, is decided by
`/alaa-observability-soc` (`$alaa-observability-soc`); the names it uses are decided by
`/alaa-services-contract` (`$alaa-services-contract`); and whether the target may run at all outside a
change window is decided by `/alaa-controlled-ops` (`$alaa-controlled-ops`).

## Checklist

- [ ] No credential-shaped assignment; every required credential fails closed with `$(error …)`
- [ ] `.env` is in `.gitignore` and included with `-include`
- [ ] No bare `export` and no `.EXPORT_ALL_VARIABLES:`
- [ ] Every untrusted value passes an allow-list before it reaches a command
- [ ] No `$(USER_COMMAND)`, no `| sh`, no `eval`
- [ ] Destructive commands guarded, and their variables defaulted
- [ ] Temporary files from `mktemp`, removed by a `trap`, never inside the repository
- [ ] Downloads over pinned TLS with `-f`, and verified against an independently sourced checksum
- [ ] No secret in a build log and none in `--build-arg`
- [ ] Permissions set at creation, not afterwards

## What this file does not decide

- The Dockerfile and Compose sides of image and container security: `/alaa-docker-production`
  (`$alaa-docker-production`).
- Which threats require review and what must fail closed: `/alaa-security-review`
  (`$alaa-security-review`).
- Shell-script security once a recipe becomes a script: `/alaa-bash-shell` (`$alaa-bash-shell`).
- The preamble that several of these patterns depend on: `makefile-structure.md`.
