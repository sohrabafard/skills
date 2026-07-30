# Source map

Read this before repeating any version-sensitive claim about Vector, VRL, a
component option, or a default value.

## Precedence

1. **The binary you are deploying.** `vector --version`, `vector generate
   '<source>//<sink>'` for the defaults it actually applies, and `vector validate`
   against the real config. This outranks documentation, because documentation and
   binary have been observed to disagree — the ClickHouse `compression` default is
   a live example, recorded in `40-clickhouse-sink.md`.
2. **Official Vector documentation** and the release notes for the exact version.
3. **Community material** — Stack Overflow, GitHub issues, forum posts, blogs.
   Troubleshooting and hypothesis only. A community claim never becomes a rule in
   this skill without step 1 or step 2 behind it.

## Re-derivation commands

Prefer these over a link when the answer is a version or a default, because they
produce a fresh answer rather than a possibly-stale page.

```bash
# Defaults the installed binary actually applies
vector generate 'demo_logs//clickhouse'

# Current Vector release. Do NOT use /releases/latest: it returns vdev-v0.3.3,
# the tag of the vdev developer tool that shares this repository.
curl -s 'https://api.github.com/repos/vectordotdev/vector/releases?per_page=100' \
  | jq -r '[.[] | select(.tag_name | test("^v[0-9]+\\.[0-9]+\\.[0-9]+$"))] | .[0].tag_name'

# Release notes for one version, as machine-readable source
curl -s https://raw.githubusercontent.com/vectordotdev/vector/master/website/cue/reference/releases/0.57.0.cue

# Buffering model, in full
curl -s https://raw.githubusercontent.com/vectordotdev/vector/master/website/content/en/docs/architecture/buffering-model.md

# Helm chart version and every option's documented semantics
curl -s https://raw.githubusercontent.com/vectordotdev/helm-charts/develop/charts/vector/Chart.yaml
curl -s https://raw.githubusercontent.com/vectordotdev/helm-charts/develop/charts/vector/values.yaml
```

`node scripts/check-upstream-version.mjs` automates the version comparison and exits
1 on drift, 2 if it could not reach upstream.

## Primary documentation

| Subject | URL |
| --- | --- |
| Docs home | https://vector.dev/docs/ |
| Concepts | https://vector.dev/docs/introduction/concepts/ |
| Buffering model | https://vector.dev/docs/architecture/buffering-model/ |
| End-to-end acknowledgements | https://vector.dev/docs/architecture/end-to-end-acknowledgements/ |
| Validating configuration | https://vector.dev/docs/administration/validating/ |
| Unit tests | https://vector.dev/docs/reference/configuration/unit-tests/ |
| Internal monitoring | https://vector.dev/docs/administration/monitoring/ |
| VRL reference | https://vector.dev/docs/reference/vrl/ |
| VRL functions | https://vector.dev/docs/reference/vrl/functions/ |
| VRL error codes | https://vector.dev/docs/reference/vrl/errors/ |
| ClickHouse sink | https://vector.dev/docs/reference/configuration/sinks/clickhouse/ |
| CLI reference | https://vector.dev/docs/reference/cli/ |
| Releases index | https://vector.dev/releases/ |
| Helm install | https://vector.dev/docs/setup/installation/package-managers/helm/ |
| Helm chart repository | https://github.com/vectordotdev/helm-charts |
| Chart README | https://github.com/vectordotdev/helm-charts/blob/develop/charts/vector/README.md |
| Security policy | https://github.com/vectordotdev/vector/security/policy |
| Open disk-buffer bugs | https://github.com/vectordotdev/vector/issues?q=is%3Aissue+state%3Aopen+label%3A%22domain%3A+buffers%22+type%3ABug |

## Fetch current sources when the task involves

A Vector or chart version; a component option name or its default; VRL function
behaviour or fallibility; acknowledgement support for a specific source; disk-buffer
sizing or limits; internal metric names; Helm chart values; a deprecation; or
anything security-sensitive. Those are exactly the claims that go stale without
announcing it.

## What was verified, and when

Every factual claim in this skill's references was checked against Vector `0.57.0`
on **2026-07-30**, with a locally installed binary for the runtime observations
(exit codes, error messages, the disk-buffer minimum, the interpolation and
confinement behaviour). Claims taken from documentation rather than observation say
so at the point they are made.
