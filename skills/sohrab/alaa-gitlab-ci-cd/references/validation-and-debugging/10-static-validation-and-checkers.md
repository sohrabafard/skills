# Static validation and checker limits

Open this guide when the task involves the validation ladder, bundled checker findings, or gate severity. The topic map routes to this file.

For current feature claims and release qualifications, use the [source map](../00-source-map.md) and [version notes](../feature-version-notes.md).

## Validation ladder

Use the cheapest check that can still answer the question.

1. Static local validation with the bundled checkers.
2. CI Lint or `glab ci lint` in project context, which resolves `include:`.
3. Runner and executor inspection.
4. Job log and artifact inspection.

## The bundled checkers: what they assert and what they cannot see

```bash
python3 scripts/validate_gitlab_ci.py .gitlab-ci.yml ci/*.yml
python3 scripts/validate_runner_config.py config.toml values.yaml
python3 scripts/validate_gitlab_ci.py --self-test
python3 scripts/validate_runner_config.py --self-test
```

Both take `--help`, `--json`, `--fail-on-warnings` and `--self-test`, and both
use the same exit codes: **0 clean, 1 findings, 2 could not run.** Exit 2 means
the checker could not produce a verdict — a missing dependency, a missing file,
an unparsable input, or the wrong kind of file — and is never a clean result.
When an agent is unsure whether the working directory is the skill root, invoke
the scripts by an absolute path.

### `validate_gitlab_ci.py`

Asserts, per file: stage list shape and uniqueness; job names that do not collide
with reserved keywords; a concrete job having an action; `only`/`except`;
undefined stage; invalid `when`; unresolved `extends`, `needs` and
`dependencies`; `${VAR}` inside `rules:if`; unresolved variable path filters
(as notes, not unsupported-syntax warnings);
image and service pinning including the registry-with-a-port form and any tag
with no version component; cache key presence, `key:files` over its two-path
limit, `fallback_keys` over five, a key not derived from a lockfile, and a
missing `policy:`; artifacts without `expire_in`; a bare `retry:`; inherited
`interruptible: true` on a mutating job; one `resource_group` saturating a
`needs:` graph; a job nothing needs that a later job can outrun; a missing job
`timeout:` where a resource group or an environment is present; deprecated
top-level keywords; `allow_failure: true` and script suffixes that swallow a
failure; a script that skips itself with `exit 0`; a credential written into a
URL or a Git remote; `CI_DEBUG_TRACE`; `set -x`; `docker login` without
`--password-stdin`; a hardcoded-looking secret; GitLab-unsupported
`${VAR:-default}` syntax in a `variables:` value; and the absence of any
recognised test, lint, static-analysis or dependency-audit command.

It **cannot see**:

- anything behind `include:`. When `include:` is present, every cross-file name
  check is downgraded to a note and one `unresolved-include` note is emitted, so
  the fleet's standard thin wrapper produces notes rather than errors. Use
  `glab ci lint --dry-run` for a merged verdict.
- the body of a script the pipeline invokes by path. `bash ci/scripts/deploy.sh`
  is one opaque line to it; everything inside that file is out of scope.
- anything the runner supplies. A pipeline with no `image:` key gets a
  `runner-supplied-image` note pointing at the runner config, which is where that
  pin lives.
- whether a value is correct. It reports that `retry:` is bare, not what the
  count should be.

### `validate_runner_config.py`

Asserts: `concurrent` unset or non-positive; every `[[runners]]` having an
executor; shell executor isolation and explicit `builds_dir`/`cache_dir`; for the
Kubernetes executor — privileged mode and node isolation, `allowed_images` and
`allowed_services` presence and breadth, `allowed_pull_policies`, a `pull_policy`
that contradicts the allowlist, `image_pull_secrets`, an unpinned or unset
`image` and `helper_image`, `namespace_per_job`, `pod_spec`, and a missing
`[runners.cache]` `Type`; and, for Helm values — `gitlabUrl`, legacy
registration tokens, a missing runner token, `rbac.create: false` with no named
service account, privileged job pods, and a `runners.config` block that is
present and valid TOML.

It routes on **content**, not on file extension. Handed a `.gitlab-ci.yml`, it
exits 2 and names `validate_gitlab_ci.py` rather than inventing findings about a
file it does not understand.

## Gate-eligible versus advisory, and who chooses

For the ownership rule that decides which findings block a pipeline, use [gate eligibility](./40-gate-eligibility.md).
