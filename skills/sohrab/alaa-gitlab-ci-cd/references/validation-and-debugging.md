# Validation and debugging

## Table of contents

- Validation ladder
- Static local validation
- Live GitLab validation
- Failure triage model
- Symptom map
- Debugging multiple YAML files

## Validation ladder

Use the cheapest check that can still answer the question.

1. Static local validation.
2. CI Lint or `glab ci lint` in project context.
3. Runner and executor inspection.
4. Job log and artifact inspection.

## Static local validation

Use the bundled scripts first:

```bash
python3 scripts/validate_gitlab_ci.py .gitlab-ci.yml ci/*.yml
python3 scripts/validate_runner_config.py values.yaml config.toml
```

These scripts are intentionally conservative. They catch common syntax, safety, and design issues quickly, but they do not replace GitLab's own CI Lint.

## Live GitLab validation

When GitLab access exists, prefer project-aware validation.

### GitLab CLI

```bash
glab ci lint
glab ci lint .gitlab-ci.yml --dry-run --include-jobs
glab ci lint path/to/pipeline.yml --dry-run --include-jobs --ref main
```

### CI Lint API

Use the API when you need automation or merged-config inspection from a script. Favor pipeline simulation when includes, local project files, or project context matter.

## Failure triage model

Classify the failure before editing YAML.

### 1. YAML or schema failure

Symptoms:

- YAML parse error.
- Unknown structure.
- Missing stage or missing referenced job.

### 2. Pipeline creation failure

Symptoms:

- No pipeline created.
- Jobs unexpectedly missing.
- Parent pipeline exists but child pipeline does not.

Check:

- `workflow:rules`.
- Job `rules`.
- include or component resolution.
- input defaults and version support.

### 3. Runner matching failure

Symptoms:

- Job is stuck with no runner.
- Job never gets picked up.

Check:

- Tags.
- Protected runner and protected ref mismatch.
- Runner paused or offline.
- Project or group scope.

### 4. Executor startup failure

Symptoms:

- Pod never becomes ready.
- Shell runner starts but environment is wrong.
- DinD service never responds.

Check:

- Kubernetes RBAC.
- Namespace and service account.
- cluster capacity and admission webhooks.
- privileged requirements.
- TLS or socket configuration.

### 5. Runtime failure

Symptoms:

- Script runs but the toolchain fails.
- Registry auth fails.
- Secrets are missing.
- Filesystem is read-only.

Check:

- Image contents and entrypoint.
- variable scope and masking.
- file variable paths.
- writable directories.
- network policy and DNS.

## Symptom map

- `job pending` with tags mismatch: runner placement issue.
- `no stages / stage does not exist`: YAML structure issue.
- `config should be an array of hashes` or similar: YAML shape issue.
- `timed out waiting for pod to start`: Kubernetes executor capacity, webhook, or timeout issue.
- `Cannot connect to the Docker daemon`: DinD service, privileged mode, or TLS mismatch.
- `unauthorized: authentication required`: registry auth or token scope issue.
- Variable seems empty only in MR pipeline: protected variable or fork pipeline behavior issue.

## Debugging multiple YAML files

When the task spans includes or components:

- Validate each file statically.
- Validate the merged result in GitLab context.
- Show the include graph in the response.
- Debug parent and child pipelines separately.
- Remember that rerunning a job uses the same pipeline configuration that created it; start a new pipeline to test config changes.
