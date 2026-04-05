# Variables and inputs

## Table of contents

- Choose the right mechanism
- Variable precedence
- Masked, protected, and file variables
- Inputs and components
- Rules and variable limitations
- Downstream pipelines and forwarding
- Debugging variable issues
- Variable inventory template

## Choose the right mechanism

Use the smallest mechanism that matches the problem.

### `spec:inputs`

Use for compile-time configuration of reusable CI files and components.

Good fit:

- Reusable job names.
- Selectable images or stages.
- Boolean or string options that should validate before the pipeline is created.

### CI/CD variables

Use for runtime values:

- Secrets.
- Environment-specific URLs.
- Registry credentials.
- Feature flags consumed by scripts or tools at job runtime.

### File variables

Use for opaque content that tools expect to read from a file:

- Kubeconfig.
- TLS certs.
- JSON service credentials.
- Docker config blobs.

Do not pretend a YAML-defined variable is a file variable. If you only have a plain CI variable, write it to a temp file during the job.

### Dotenv artifacts

Use for values produced by one job and consumed by later jobs in the same pipeline.

Do not use dotenv as a substitute for long-lived secrets.

## Variable precedence

Treat precedence collisions as a design problem, not a trivia problem.

Highest-risk mixes:

- Manual or trigger variables overriding project defaults.
- Group variables shadowing project variables.
- `workflow:rules:variables` unexpectedly flowing into downstream jobs.
- Job-level variables hiding top-level defaults.
- Dotenv values silently replacing earlier assumptions.

When a task mixes several variable sources, write a short precedence note in the final answer.

## Masked, protected, and file variables

### Masked variables

Use masking for secrets that may appear in logs, but do not rely on masked variables to expand other variables safely.

Important operational rules:

- Masking can fail if the logged output transforms the value.
- Masked or hidden variables are not a good place for nested variable expansion.
- `echo` or shell tracing can still leak sensitive data through transformed output.

### Protected variables

Use protected variables for deploy credentials, signing keys, and other values that must stay off unprotected branches.

Whenever protected variables are involved, say whether the jobs run only on protected refs.

### File variables

Prefer file variables for credentials that tools expect as a path. In the final YAML, consume them like regular environment variables that already point to a generated file path.

## Inputs and components

### Recommended pattern

Use a component or reusable file with typed inputs for stable structure, and leave secrets or runtime-only settings to variables.

Example split:

- Input: target stage name, base image, job prefix.
- Variable: registry password, cloud role, deploy URL.

### Job inputs

If the environment supports job inputs, they can make manual runs and retries safer than ad hoc pipeline variables. Use them only when the GitLab and Runner versions support them.

## Rules and variable limitations

Use these guardrails when reviewing or generating YAML:

- In `rules:if`, reference variables as `$VAR`, not `${VAR}`.
- Keep literal strings quoted inside `if` expressions.
- Do not depend on variable expansion inside `rules:changes`, `rules:exists`, or related path filters.
- Keep path-based rule patterns literal when correctness matters.

## Downstream pipelines and forwarding

### Triggered or child pipelines

Be explicit about variable forwarding. Do not assume that only the variables you care about are passed.

When using `workflow:rules:variables`, remember that they become default variables and can flow into downstream pipelines unless you restrict inheritance.

Use unique variable names when forwarding is unavoidable.

## Debugging variable issues

When a pipeline behaves as if variables are wrong, check in this order:

1. Was the variable created at the scope you expected?
2. Is a higher-precedence source overriding it?
3. Is the job running on a ref that can read protected variables?
4. Is the value masked or hidden in a way that prevents safe expansion?
5. Is the variable being used in a GitLab YAML context that does not support expansion?
6. Is the job actually running in a downstream or child pipeline with different inheritance?

## Variable inventory template

Use a compact table in the final answer when you introduce custom values:

| Name | Type | Source | Sensitive | Default | Consumed by |
| --- | --- | --- | --- | --- | --- |
| `IMAGE_TAG` | variable | pipeline or default | no | `$CI_COMMIT_SHA` | build job |
| `KUBECONFIG` | file variable | project | yes | none | deploy job |
| `AWS_ROLE_ARN` | variable | project | no | none | OIDC auth step |
