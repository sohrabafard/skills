# Source map

Which official page is authoritative for which claim, when to re-check, and how
to resolve a conflict. Version facts and the cadence that lets you compute a
baseline live in `feature-version-notes.md`; this file is the provenance ledger
behind them.

## Freshness triggers

Re-check the official source before answering when the task turns on any of:
current or version-specific behaviour; a GitLab or Runner minimum version; a
feature that may be beta or experimental; CI inputs, components or the catalog;
token or secret behaviour; Kubernetes executor behaviour; runner Helm chart
changes; registry authentication; a security-hardening recommendation; an image
or tool version that a template pins; or a live CI failure that may depend on
platform behaviour.

## First-check official GitLab sources

- Release and maintenance policy (cadence, backports, current stable): https://docs.gitlab.com/policy/maintenance/
- Release notes index: https://docs.gitlab.com/releases/
- CI/CD YAML reference: https://docs.gitlab.com/ci/yaml/
- Deprecated keywords: https://docs.gitlab.com/ci/yaml/deprecated_keywords/
- CI/CD variables: https://docs.gitlab.com/ci/variables/
- CI/CD inputs: https://docs.gitlab.com/ci/inputs/
- CI/CD components and catalog: https://docs.gitlab.com/ci/components/
- GitLab Functions (the `run:` keyword): https://docs.gitlab.com/ci/functions/
- Caching in GitLab CI/CD: https://docs.gitlab.com/ci/caching/
- CI/CD job token: https://docs.gitlab.com/ci/jobs/ci_job_token/
- ID tokens and OIDC: https://docs.gitlab.com/ci/secrets/id_token_authentication/
- External secrets: https://docs.gitlab.com/ci/secrets/
- Secure files: https://docs.gitlab.com/ci/secure_files/
- Pipeline security: https://docs.gitlab.com/ci/pipelines/pipeline_security/
- Docker builds in GitLab CI: https://docs.gitlab.com/ci/docker/using_docker_build/
- Building images with kaniko (for its maintenance status): https://docs.gitlab.com/ci/docker/using_kaniko/
- Container registry: https://docs.gitlab.com/user/packages/container_registry/
- CI Lint: https://docs.gitlab.com/ci/lint/
- Instance limits (plan limits such as `ci_needs_size_limit`): https://docs.gitlab.com/administration/instance_limits/

## Runner and executor sources

- GitLab Runner documentation: https://docs.gitlab.com/runner/
- Advanced configuration reference (`config.toml`): https://docs.gitlab.com/runner/configuration/advanced-configuration/
- Shell executor: https://docs.gitlab.com/runner/executors/shell/
- Kubernetes executor: https://docs.gitlab.com/runner/executors/kubernetes/
- Runner Helm chart configuration: https://docs.gitlab.com/runner/install/kubernetes_helm_chart_configuration/
- New runner creation workflow (authentication tokens): https://docs.gitlab.com/ci/runners/new_creation_workflow/
- Runner security: https://docs.gitlab.com/runner/security/
- Runner releases: https://gitlab.com/gitlab-org/gitlab-runner/-/releases
- Runner helper image tags: https://hub.docker.com/r/gitlab/gitlab-runner-helper/tags

## Image and tool lifecycle sources

Every image this skill's templates pin is checked against the vendor's own
lifecycle page, not against a copy of it.

- Docker Engine support lifecycle: https://endoflife.date/docker-engine
- Docker library image tags: https://hub.docker.com/_/docker/tags
- Alpine release branches and end-of-support dates: https://alpinelinux.org/releases/
- BuildKit releases: https://github.com/moby/buildkit/releases and https://hub.docker.com/r/moby/buildkit/tags
- PHP image tags: https://hub.docker.com/_/php/tags
- Node image tags: https://hub.docker.com/_/node/tags
- Docker build documentation: https://docs.docker.com/build/
- Podman: https://docs.podman.io/ · Buildah: https://buildah.io/
- Kubernetes: https://kubernetes.io/docs/ · Helm: https://helm.sh/docs/

## Conflict resolution

1. Live GitLab project and runner behaviour observed in this task.
2. Official GitLab documentation for the matching GitLab and Runner versions.
3. Official executor, Kubernetes, Docker or Helm documentation.
4. This skill's own references and templates.

Where 2 and 4 disagree, 2 wins and the reference is wrong — except for the one
divergence this skill states deliberately and explains, the build-path ordering in
`container-build-strategies.md`.

Use community posts, Stack Overflow answers and issue comments only for symptom
troubleshooting, and only after official documentation, CI Lint, runner logs and
project settings have been checked. Never as normative security or design
guidance.

## Re-checking the pinned values

Every image pin in `assets/templates/` carries a comment naming the URL that
re-derives it. To re-baseline the whole skill:

1. Open the release and maintenance policy page and record the current stable
   GitLab minor and the Runner version the Runner docs describe.
2. For each template, open the URL in its header comment, compare the pinned tag
   against the current supported line, and repin where the pinned line has
   reached end of support.
3. Run both checkers' `--self-test`, then run them over `assets/templates/`.
4. Record the date and what changed in this file's log below.

## Verification log

- **2026-07-29.** Full re-baseline. Verified against the pages above: GitLab
  release cadence and current stable line; Runner documentation version; Docker
  Engine supported lines (24.0 ended 2024-06-08, 29 and 25.0 supported, 25.0 ends
  2026-12-04); Alpine branches (3.20 out of support since 2026-04-01, 3.24 current
  stable to 2028-06-01); BuildKit latest release; components and ID tokens GA
  milestones; GitLab Functions still experimental with the `step:` to `func:`
  rename; kaniko unmaintained; `cache:key:files` maximum of two and
  `fallback_keys` maximum of five; `read_only_root_filesystem` absent from every
  documented Kubernetes executor security context, which is why the rule that
  keyed on it was removed from `validate_runner_config.py`.
