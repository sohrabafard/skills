# Feature and version notes

A version number written into a file goes stale silently. This file therefore
states the **cadence**, so an agent can compute the current baseline, then only
facts that do not move: general-availability milestones, features that are still
experimental, hard numeric limits, and deprecations paired with their
replacement.

Each entry names the command or URL that re-derives it. Check rather than trust.

## Compute the baseline, do not read it

GitLab's published release and maintenance policy:

- **Major releases: yearly, in May.** GitLab 19.0 was released 2026-05-21.
- **Minor releases: monthly, on the third Thursday of each month.**
- **Patch releases: twice monthly**, the Wednesday before and the Wednesday after
  the monthly minor.
- **Backports:** bug fixes go to the current stable release only; security fixes
  go to the current stable release plus the previous two monthly releases.

From that: the current supported line is the newest minor, and anything older
than two minors behind receives no security backport. Do not write a baseline
version into a design. Write "the current stable line" and, when a specific
number is needed for an answer, derive it at that moment:

| To find | Run or open |
|---|---|
| the current stable GitLab version and cadence | https://docs.gitlab.com/policy/maintenance/ |
| what a specific release changed | https://docs.gitlab.com/releases/ |
| the GitLab Runner version the docs describe | https://docs.gitlab.com/runner/ |
| the newest published runner helper image tag | https://hub.docker.com/r/gitlab/gitlab-runner-helper/tags |
| the version of a live instance | the instance's `/help` page, or `glab api /version` |
| the version of a live runner | `gitlab-runner --version` on the host |

Keep the Runner's `major.minor` in step with the GitLab instance's. An older
runner usually works against a newer GitLab, but features gated on the newer
version are unavailable and some fail without a clear message.

**As of 2026-07-29** the maintenance policy page named **19.2** as the current
stable release and the Runner documentation described **19.0**; the newest
published helper image tag was `x86_64-v19.1.2`. Those three numbers are here as
a dated observation, not as a baseline to design against.

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

## Writing an answer when the target versions are unknown

1. State that the design targets the current stable line and name the page that
   defines it, rather than naming a version you did not check.
2. Name any feature whose status is experimental, and say what a stable
   alternative would be.
3. Where a design would differ on an older instance, give the difference in one
   sentence rather than designing for the older instance by default.
