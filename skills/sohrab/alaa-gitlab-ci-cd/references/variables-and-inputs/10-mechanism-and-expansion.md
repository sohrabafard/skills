# Mechanisms and expansion

Open this guide when choosing a value mechanism or understanding expansion. For current feature claims, consult the [GitLab source map](../00-source-map.md) and [version notes](../feature-version-notes.md).

## Choose the right mechanism

Use the smallest mechanism that matches the problem.

**`spec:inputs`** — compile-time configuration of a reusable file or component.
The value is validated before the pipeline is created, so a wrong value is a
pipeline-creation error rather than a job failure. Use for job names, selectable
images or stages, and options that should be constrained to a fixed set.

**CI/CD variables** — runtime values: secrets, environment-specific URLs,
registry credentials, feature flags a script reads at job time.

**File variables** — opaque content a tool expects to read from a path: a
kubeconfig, a TLS certificate, a JSON service credential, a Docker config blob.
Do not pretend a YAML-defined variable is a file variable. If you only have a
plain variable, write it to a temp file during the job, under `umask 077`, and
remove it with an `EXIT` trap.

**Dotenv artifacts** — a value produced by one job and consumed by later jobs in
the same pipeline. Not a place for a secret: a dotenv report is stored as a job
artifact with the artifact's retention and the project's download rules.

## What GitLab's expansion does and does not do

GitLab expands `$VAR` and `${VAR}`. It does **not** implement shell-style
defaults or error forms:

```yaml
variables:
  # Wrong. GitLab reads the whole brace body — "CI_SERVER_PROTOCOL:-https" — as
  # one variable name, finds nothing, and assigns an empty string. Where the name
  # is a predefined variable, this assignment overwrites it for the job.
  CI_SERVER_PROTOCOL: "${CI_SERVER_PROTOCOL:-https}"
```

`${VAR:-default}`, `${VAR:?message}` and `${VAR+alt}` are shell syntax. They work
inside a `script:` line, because the shell evaluates that; they do not work in a
`variables:` value, a `rules:` expression, or anywhere else GitLab expands. Put
the default in the script, or assign the literal value.
`validate_gitlab_ci.py` reports `variables-shell-default` at error severity.

A value that must be present has no GitLab-level "fail if unset". Express that as
the first line of the job's script — a `require_env`-style check that exits
non-zero — rather than as a default that silently selects a wrong target. A
default that names a namespace, a registry, a chart version or a database is a
fail-open path: when the real value is missing the pipeline does not stop, it
acts on the wrong thing.
