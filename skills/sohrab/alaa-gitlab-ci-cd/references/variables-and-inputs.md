# Variables and inputs

## Table of contents

- Choose the right mechanism
- What GitLab's expansion does and does not do
- Variable precedence
- Masked, protected and file variables
- `id_tokens:`, `secrets:` and secure files
- Inputs and components
- Rules and variable limitations
- Downstream pipelines and forwarding
- Debugging an unexpected value
- Variable inventory template

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

## Variable precedence

Treat a precedence collision as a design problem, not trivia. The highest-risk
mixes:

- Manual or trigger variables overriding project defaults.
- Group variables shadowing project variables.
- `workflow:rules:variables` flowing into downstream pipelines as defaults.
- Job-level variables hiding top-level ones.
- A dotenv report from an earlier job silently replacing an assumption.

When a design mixes several sources, write a short precedence note into the
answer naming which source wins for each contested name.

## Masked, protected and file variables

**Masked variables.** Masking replaces the literal value in the log. It does not
survive transformation: shell tracing prints expanded arguments, `base64` output
is not the masked string, and a value split across lines is not matched. Do not
rely on a masked value to expand another variable safely.

**Protected variables.** Available only to jobs on protected refs. Whenever a
design uses one, state whether the jobs that need it actually run on protected
refs, and test `$CI_COMMIT_REF_PROTECTED == "true"` rather than assuming the
default branch is protected.

**File variables.** GitLab writes the value to a temp file and sets the variable
to that path. Consume it as a path. Do not `cat` it into a log to check it.

## `id_tokens:`, `secrets:` and secure files

```yaml
deploy:
  id_tokens:
    VAULT_ID_TOKEN:
      aud: https://vault.example.com
  secrets:
    DB_PASSWORD:
      vault: production/db/password@ops
      token: $VAULT_ID_TOKEN
      file: false
  script:
    - ./scripts/deploy.sh
```

- `id_tokens:` mints a short-lived JWT per job, with the audience the provider
  expects. Each token gets its own variable name.
- `secrets:` fetches the value with that token and exposes it. `file: true`
  writes it to a temp file and sets the variable to the path; `file: false` sets
  the value directly.
- `CI_JOB_JWT` and `CI_JOB_JWT_V2` are removed and return `401 Unauthorized`.

**Secure files** are the platform feature for a credential that is a file by
nature — a keystore, a signing key, a provisioning profile. Download them in the
job with `glab securefile`, which also verifies the checksum. The older
`download-secure-files` tool was deprecated in GitLab 18.6.

## Inputs and components

Declare a type on every input, and constrain it where the set of valid values is
known:

```yaml
spec:
  inputs:
    stage:
      type: string
      default: test
    php-version:
      type: string
      default: "8.5"
      options: ["8.3", "8.4", "8.5"]
    job-prefix:
      type: string
      default: app
      regex: '^[a-z][a-z0-9-]{0,30}$'
    coverage:
      type: boolean
      default: false
    test-command:
      type: array
      default: ["php artisan test"]
```

`type:` takes `string`, `number`, `boolean` or `array`. `options:` restricts a
value to a list. `regex:` restricts a string. All three are checked when the
pipeline is created, which is the entire reason to prefer an input over a
variable for a compile-time value.

Interpolation is `$[[ inputs.name ]]`, and it happens before YAML is parsed.
Never interpolate a free-text input into a quoted shell command
(`sh -lc '$[[ inputs.cmd ]]'`): a quote in the input breaks out of the string.
Type the input as an array and let each element be one command instead.

The split to hold to: **input** for structure — target stage, base image, job
prefix, a bounded option. **Variable** for a runtime value — a registry password,
a cloud role, a deploy URL.

Reference a published component by commit SHA or tag. Resolution precedence is
commit SHA, then tag, then branch, with `~latest` and partial semantic versions
resolving against the catalog. A branch reference makes the component's content
change under the consumer without a change on the consumer's side.

## Rules and variable limitations

- In `rules:if`, write `$VAR`, not `${VAR}`.
- Quote literal strings inside an `if` expression.
- No variable expansion in `rules:changes`, `rules:exists` or `compare_to`. Write
  the literal paths.
- Keep path-based patterns literal wherever correctness matters more than
  brevity.

## Downstream pipelines and forwarding

Be explicit about what is forwarded. Do not assume only the variables you care
about are passed. `workflow:rules:variables` become default variables and can
flow downstream unless inheritance is restricted. Where forwarding cannot be
avoided, use names unique enough that a collision in the downstream project is
visible.

## Debugging an unexpected value

Check in this order, and stop at the first answer:

1. Was the variable created at the scope you expected — instance, group, project,
   pipeline, job?
2. Is a higher-precedence source overriding it?
3. Is the job running on a ref that can read protected variables?
4. Is the value masked or hidden in a way that prevents safe expansion?
5. Is it being used in a GitLab context that does not expand — a path filter, or
   a shell-style default in a `variables:` value?
6. Is the job actually running in a downstream or child pipeline with different
   inheritance?

## Variable inventory template

Publish this table in the answer whenever the design introduces a custom value.

| Name | Type | Source | Sensitive | Default | Consumed by |
| --- | --- | --- | --- | --- | --- |
| `IMAGE_TAG` | variable | pipeline or `default:` | no | `$CI_COMMIT_SHA` | build job |
| `KUBECONFIG` | file variable | project | yes | none — job fails if unset | deploy job |
| `VAULT_ID_TOKEN` | id_token | per job | yes | n/a | secrets fetch |

A value with no default and a stated "job fails if unset" is a deliberate
fail-closed choice. Say so in the table rather than inventing a default. Where the
name is also read by another service, it is a shared name and
`/alaa-services-contract` (`$alaa-services-contract`) owns it.
