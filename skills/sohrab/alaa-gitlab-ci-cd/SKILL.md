---
name: alaa-gitlab-ci-cd
description: Generate, validate, review, and debug GitLab CI/CD pipelines, reusable CI components, runner configs, and container-build workflows for GitLab Runner shell and Kubernetes executors. Use when the task involves one or more `.gitlab-ci.yml` files, included CI files, CI components, GitLab Runner `config.toml`, Helm `values.yaml`, GitLab Kubernetes executor behavior, Docker or daemonless image builds, variables or inputs, job routing via tags, pipeline security, or CI failure triage. Prefer it for both authoring and debugging. Do not use it for unrelated Kubernetes manifests, unrelated Dockerfiles, or non-GitLab CI systems.
---

Use this skill to act like a production GitLab CI/CD specialist, not a generic YAML writer.

## Start fast

Collect only the facts that materially change the design:

- GitLab version and Runner version.
- GitLab.com, GitLab Dedicated, or self-managed.
- Runner type: shell, Kubernetes, or mixed.
- Shared vs dedicated runner and the trust model.
- Whether the job really needs a Docker daemon.
- Registry, cloud, or secret manager involved.
- The failure symptom if this is a debugging task.

If those facts are missing, make safe modern assumptions, state them briefly, and continue. Default to GitLab 18.x behavior, Runner 18.x behavior, dedicated runners for privileged work, and protected branches for release or deploy jobs.

## Open only the reference you need

- `references/pipeline-authoring.md` for new or refactored pipelines, rules, DAGs, includes, components, and child pipelines.
- `references/variables-and-inputs.md` for variable precedence, masking, file variables, inputs, dotenv, and downstream forwarding.
- `references/runner-shell-and-kubernetes.md` for runner architecture, `config.toml`, Helm `values.yaml`, shell runner limits, and Kubernetes executor tuning.
- `references/container-build-strategies.md` for BuildKit rootless, Docker-in-Docker, Podman, Buildah, registry auth, and cache strategy.
- `references/security-and-hardening.md` for runner isolation, secrets, merge request risk, pull policy, token risk, and privileged-mode decisions.
- `references/validation-and-debugging.md` for local validation, CI Lint, `glab`, failure triage, and symptom-to-cause mapping.
- `references/feature-version-notes.md` when a feature might be gated, beta, experimental, or version-dependent.

Do not read every reference by default. Load the narrowest file that matches the task.

## Core workflow

1. Classify the task: generate, review, validate, debug, or migrate.
2. Choose the lane:
   - Pipeline semantics and YAML structure.
   - Variable and input design.
   - Runner configuration and job placement.
   - Container build strategy.
   - Security review.
3. Verify version-sensitive claims against current official GitLab documentation when the feature, flag, or minimum version matters.
4. Produce the smallest correct solution first, then harden it.
5. Validate before finishing:
   - Static local checks with `scripts/validate_gitlab_ci.py` or `scripts/validate_runner_config.py`.
   - Context-aware validation with CI Lint or `glab ci lint` when project access exists.
6. Close with assumptions, version floor, required variables, runner prerequisites, and remaining risks.

## Authoring rules

- Prefer `workflow:rules` plus job `rules` for new work. Avoid introducing `only` or `except` unless you are preserving an older pipeline on purpose.
- Prefer `needs` for DAG execution when stages alone would block parallelism.
- Use `interruptible: true` for cancel-safe jobs that should stop on superseding commits.
- Use `resource_group` for deploys or any job that mutates a shared target.
- Pin images and tools to explicit versions. Do not introduce `latest` in production CI.
- Reuse hidden jobs, components, or includes when repetition is real. Do not abstract a one-off job.
- Keep job scripts deterministic and non-interactive.
- When generating more than one YAML file, make include and child-pipeline boundaries explicit.

Open `references/pipeline-authoring.md` if the task touches rules, workflow, includes, components, child pipelines, matrix, or DAG layout.

## Variable and input rules

- Use `spec:inputs` and CI components for compile-time reusable configuration.
- Use CI/CD variables for runtime values, secrets, and environment-specific overrides.
- Prefer file variables or runtime file creation for kubeconfigs, certificates, JSON credentials, and Docker config blobs.
- Never hardcode secrets in YAML.
- Treat masked variables as non-composable: do not rely on masked values to expand other variables safely.
- Document every non-predefined variable you introduce: name, purpose, source, sensitivity, default, and where it is consumed.
- Watch precedence carefully when mixing pipeline variables, project or group variables, job variables, dotenv artifacts, and downstream pipelines.
- Avoid variable expansion in `rules:changes`, `rules:exists`, and related path filters.

Open `references/variables-and-inputs.md` whenever the task involves variables, secret handling, inputs, components, downstream pipelines, or file-based credentials.

## Runner rules

- Shell runner is for trusted code on a trusted host. Do not treat it as the default safe runner.
- Kubernetes executor is the default choice when you need stronger isolation, ephemeral execution, or cluster-native scaling.
- Use explicit runner tags and make job placement deliberate.
- For Kubernetes runners, keep Helm `values.yaml` separate from embedded TOML in `runners.config`; the embedded `config` block is TOML, not YAML.
- Restrict Kubernetes runners with `allowed_images`, `allowed_services`, and `allowed_pull_policies` when the trust model is not fully closed.
- Use dedicated nodes, labels, or separate runner fleets for privileged or daemon-based builds.

Open `references/runner-shell-and-kubernetes.md` for any runner architecture, `config.toml`, Helm, RBAC, namespace, or executor question.

## Container build strategy rules

Choose the build path before writing YAML:

- Default to BuildKit rootless for Kubernetes or other unprivileged environments.
- Use Docker-in-Docker only when the job truly needs Docker daemon behavior.
- Use Podman or Buildah when the platform or policy favors daemonless OCI builds.
- Do not recommend Kaniko for new designs.
- If Docker-in-Docker is required, prefer a dedicated privileged runner, isolated nodes, and TLS-enabled setup unless a documented platform constraint forces otherwise.

Open `references/container-build-strategies.md` before designing any image-build job.

## Security rules

- Prefer short-lived credentials with `id_tokens` and supported `secrets` integrations over long-lived cloud keys.
- Treat privileged runners, shell runners, `docker.sock`, and shared persistent workspaces as high-risk.
- Be explicit about merge request and fork risk before allowing protected variables, protected runners, or deploy credentials.
- Prefer `pull_policy: always` on shared or untrusted runners for private images.
- Separate safe defaults from risky alternatives. If the user requests the risky path, provide it with clear isolation requirements.

Open `references/security-and-hardening.md` for any security-sensitive review or design.

## Debugging rules

Always separate these layers before proposing fixes:

1. YAML parse or schema problem.
2. Pipeline creation or rule evaluation problem.
3. Include, component, or input expansion problem.
4. Runner matching or tag problem.
5. Executor startup problem.
6. Container build or registry auth problem.
7. Script or application problem.
8. Secret, token, or environment scoping problem.

Do not jump straight to editing scripts when the pipeline might not even be created or picked up.

Open `references/validation-and-debugging.md` for triage steps and command patterns.

## Output contract

When you finish, provide:

- The final YAML, TOML, or `values.yaml` needed for the task.
- A compact variable table for custom inputs or variables.
- Required runner prerequisites and tags.
- Validation results and what was validated statically versus against a live GitLab context.
- Key assumptions, minimum versions, and any feature gates.
- A short hardening note when the design uses privileged mode, shell runners, or sensitive credentials.

## Built-in assets

Use the templates in `assets/templates/` when they match the task closely:

- `app-basic.gitlab-ci.yml`
- `component-with-inputs.gitlab-ci.yml`
- `k8s-buildkit-rootless.gitlab-ci.yml`
- `k8s-dind-tls.gitlab-ci.yml`
- `shell-runner-trusted-host.gitlab-ci.yml`
- `values-k8s-runner.yaml`
- `config-shell-runner.toml`

Treat them as hardened starting points, not blind copy-paste answers.

## Validation scripts

- `python3 scripts/validate_gitlab_ci.py <file> [more files]`
- `python3 scripts/validate_runner_config.py <file> [more files]`

Use local scripts first for cheap feedback. Use CI Lint or `glab ci lint` when you need include resolution, project context, or pipeline simulation.

## Failure-mode handling

- If a feature is beta, experimental, or version-gated, say so and include the minimum version.
- If live GitLab access is unavailable, say what you validated locally and what still needs live CI Lint or project-context validation.
- If the request combines incompatible goals, prefer the safer architecture and explain the tradeoff in one or two lines.

## Subagent strategy

If multi-agent mode is available and the task is large, split work by concern:

- Pipeline semantics and YAML generation.
- Runner or Kubernetes executor configuration.
- Security and version verification.

Merge results only after the version-sensitive and security-sensitive findings agree.
