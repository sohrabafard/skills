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

## What was verified, when, and how

Two passes with different provenance. Claims taken from documentation rather than
observation say so where they are made, and a claim carrying no stated observation
is a documentation claim.

**2026-07-30 — the original pass.** Every factual claim then in this skill's
references was checked against Vector `0.57.0`, with a locally installed binary for
the runtime observations: exit codes, error messages, the disk-buffer minimum, and
the interpolation and confinement behaviour.

**2026-08-08 — the capability and pass-through pass.** Added
`35-pass-through-and-relay-paths.md` and `82-capability-surface.md`, and revised
`30-`, `40-`, `50-`, `60-`, `65-`, `75-`, `80-` and `85-`. **Mixed provenance, and
the two kinds must not be conflated:**

- *Observed on the binary* — image `timberio/vector:0.57.0-alpine`, digest
  `sha256:19e3526faf4d4b1ed0c28a0d68d4cc3a1e13e437099986a5b7a768707907497c`, build
  `0.57.0 (x86_64-unknown-linux-musl 8832452 2026-07-14 20:58:30)`: the `api.graphql`
  rejection, `GET /health`, interpolation load behaviour with and without a
  format-constrained value, the `route._unmatched` warning under `--deny-warnings`,
  `expected_event_count`, `request.retry_strategy` nesting, `measure_cpu_usage`
  scope, `vector vrl --quiet`, live internal metric names and histogram buckets, and
  both relay runs.
- *Read from release pages through a summarising fetch* — the whole of
  `82-capability-surface.md` except where it says otherwise, and the version-tagged
  additions in `40-`, `50-`, `60-` and `80-`. **Re-read the page before quoting any
  of it verbatim:** that pass has already been caught altering wording inside what
  looked like a quotation.

Where the two disagree, the binary wins, per the precedence at the top of this file.
