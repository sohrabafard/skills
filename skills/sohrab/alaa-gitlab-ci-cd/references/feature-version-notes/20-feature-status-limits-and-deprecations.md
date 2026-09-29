# Feature status, limits, and deprecations

Use this reference when the task needs current version-sensitive behavior. Every entry retains its re-derivation source; check those sources at use time.

For the dated release and baseline calculation, see [the source map](../00-source-map.md).

## Generally available, and therefore safe to use without a caveat

| Feature | Milestone | Re-derive from |
|---|---|---|
| CI/CD components and the CI/CD Catalog | generally available in GitLab 17.0 | https://docs.gitlab.com/ci/components/ |
| `id_tokens:` and OIDC authentication | generally available on all tiers, on GitLab.com, Self-Managed and Dedicated | https://docs.gitlab.com/ci/secrets/id_token_authentication/ |
| Secure files | generally available on all tiers | https://docs.gitlab.com/ci/secure_files/ |
| `spec:inputs` with `type:`, `options:` and `regex:` | part of the component surface that went GA in 17.0 | https://docs.gitlab.com/ci/inputs/ |

## Still experimental — do not build a production pipeline on these

**GitLab Functions**, invoked by the `run:` keyword. GitLab documents it as "an
experimental feature in active development and is subject to breaking changes".
The feature was renamed from CI/CD Steps: `step:` became `func:` and `step.yml`
became `func.yml`, with the older forms deprecated. Use `script:` unless the task
specifically requires Functions, and if you meet a `func.yml` in an existing
repository, treat it as experimental configuration rather than a stable contract.
Re-derive from https://docs.gitlab.com/ci/functions/.
`validate_gitlab_ci.py` reports `run-experimental`.

## Hard limits — these are checkable rules, not guidance

| Limit | Value | Re-derive from |
|---|---|---|
| `cache:key:files` entries | maximum **two** file paths | https://docs.gitlab.com/ci/yaml/ |
| `fallback_keys` per cache entry | up to **five** | https://docs.gitlab.com/ci/caching/ |
| `artifacts:expire_in` when unset | the instance-wide default applies | https://docs.gitlab.com/ci/yaml/ |
| jobs per `needs:` array | a **plan limit** (`ci_needs_size_limit`), instance-dependent and adjustable on self-managed through the Plan Limits API or the Rails console | https://docs.gitlab.com/administration/instance_limits/ |
| `allowed_images` / `allowed_services` unset | equivalent to `['*/*:*']` — every image | https://docs.gitlab.com/runner/executors/kubernetes/ |

The first two are enforced by `validate_gitlab_ci.py` at error severity. The
fourth is deliberately not a number in this file: writing one would be wrong on
some instances the day it was written.

## Deprecations, each with its replacement

| Deprecated | Replacement | Notes |
|---|---|---|
| `only` / `except` | `rules` | `only:refs` → `rules:if`; `only:variables` → `rules:if`; `only:changes` → `rules:changes`; `only:kubernetes` → `rules:if` with `CI_KUBERNETES_ACTIVE`. Deprecated, not removed |
| top-level `image`, `services`, `cache`, `before_script`, `after_script` | the `default:` section | same semantics, and `default:` says what it means |
| `publish` keyword and the `pages` job name for Pages | `pages` and `pages.publish` | |
| `environment:kubernetes:namespace`, `environment:kubernetes:flux_resource_path` | `environment:kubernetes:dashboard:namespace` and `:dashboard:flux_resource_path` | |
| `CI_JOB_JWT`, `CI_JOB_JWT_V2` | `id_tokens:` | the old variables return `401 Unauthorized` |
| runner registration tokens | runner authentication tokens, prefix `glrt-` | instance administrators and group owners have been able to disable legacy registration since GitLab 17.0 |
| `download-secure-files` | `glab securefile` | deprecated in GitLab 18.6; `glab` also verifies the checksum |
| kaniko | Docker, Buildah or Podman | GitLab's own page states kaniko is no longer a maintained project |

Re-derive the keyword rows from
https://docs.gitlab.com/ci/yaml/deprecated_keywords/.
