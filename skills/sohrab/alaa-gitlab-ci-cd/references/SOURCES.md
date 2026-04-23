# Sources

Use this file when GitLab CI/CD behavior must be current or version-specific.

## Freshness triggers

Re-check official sources when the user asks for latest/current behavior, GitLab or Runner minimum versions, beta or experimental features, CI inputs/components, token or secret behavior, Kubernetes executor behavior, runner Helm chart changes, registry authentication, security hardening, or a live CI failure that may depend on platform behavior.

## First-check official GitLab sources

- GitLab CI/CD YAML reference: https://docs.gitlab.com/ci/yaml/
- GitLab CI/CD variables: https://docs.gitlab.com/ci/variables/
- GitLab CI/CD inputs: https://docs.gitlab.com/ci/inputs/
- CI/CD components: https://docs.gitlab.com/ci/components/
- CI/CD job token: https://docs.gitlab.com/ci/jobs/ci_job_token/
- ID tokens and OIDC: https://docs.gitlab.com/ci/secrets/id_token_authentication/
- External secrets: https://docs.gitlab.com/ci/secrets/
- Pipeline security: https://docs.gitlab.com/ci/pipelines/pipeline_security/
- Docker build in GitLab CI: https://docs.gitlab.com/ci/docker/
- Container registry: https://docs.gitlab.com/user/packages/container_registry/
- CI Lint: https://docs.gitlab.com/ci/lint/
- GitLab release notes: https://docs.gitlab.com/update/versions/gitlab/

## Runner and executor sources

- GitLab Runner documentation: https://docs.gitlab.com/runner/
- Runner configuration reference: https://docs.gitlab.com/runner/configuration/advanced-configuration/
- Shell executor: https://docs.gitlab.com/runner/executors/shell/
- Kubernetes executor: https://docs.gitlab.com/runner/executors/kubernetes/
- Runner Helm chart configuration: https://docs.gitlab.com/runner/install/kubernetes_helm_chart_configuration/
- Runner security: https://docs.gitlab.com/runner/security/
- GitLab Runner releases: https://gitlab.com/gitlab-org/gitlab-runner/-/releases

## Primary ecosystem sources

- Docker docs for daemon and BuildKit behavior: https://docs.docker.com/build/
- BuildKit repository docs: https://github.com/moby/buildkit
- Podman docs: https://docs.podman.io/
- Buildah docs: https://buildah.io/
- Kubernetes docs for executor cluster behavior: https://kubernetes.io/docs/
- Helm docs for runner chart deployment: https://helm.sh/docs/

## Conflict resolution

1. Live GitLab project and runner behavior.
2. Official GitLab docs for the matching GitLab and Runner versions.
3. Official executor, Kubernetes, Docker, or Helm docs.
4. This skill's local references and templates.

## Community troubleshooting sources

Use community posts, Stack Overflow answers, and issue comments only for symptom troubleshooting after official docs, CI Lint, runner logs, and project settings are checked. Do not use them as normative security or pipeline design guidance.
