# Writer implementation evidence

Date: 2026-09-26. Scope: `skills/sohrab/alaa-k8s-helm/**` and this writer evidence
directory only. Parent owns workflow and integrated proof. No cluster access,
installation, dependency change, commit, deployment or deletion occurred.

## Decision and alternatives

Keep the existing Kubernetes authoring floor and Helm consumer path while adding
new stable-release awareness. Reject moving the authoring floor with the upstream
maintenance window or dropping Helm consumers on a calendar date: neither has
consumer evidence or approval. Keep exact facts in version-awareness and route
dependent commands to it. Local client proof and upstream support remain separate.

The freshness repair keeps the existing regex extraction structure and exit
contract. Exclude prerelease token suffixes, match the EOL year exactly, and use a
fixed synthetic reference for self-tests. A new HTTP/API client or a checker
redesign would exceed the demonstrated defects. No manifest predicate changes.

## Before and after regression observations

Before source changes, direct in-process calls to check_versions produced:

- `v4.3.0 v4.4.0-rc.1` -> `4.4.0`, incorrectly treating preview as stable.
- `1.37.1 1.38.0-alpha.1` -> `1.38`, incorrectly treating preview as stable.
- Pinned `2027-02-10` compared with `February 10th, 2028` -> match.

The focused self-test now covers matching/drifted pages, empty pages, missing
reference, mixed stable/preview inputs, preview-only inputs, multi-digit patches,
and ISO/prose dates with correct and incorrect years. Logs in this directory
record observed results; synthetic fixtures are not upstream freshness proof.

## Intentionally changed behavior

- Recognize the newer stable line without removing the previous authoring floor.
- Require explicit migration approval rather than automatic Helm consumer removal.
- Select rollback flags only after successful supported-major detection.
- Validate against explicit target schema versions and capability conditions.
- Report externalIPs deprecation accurately while still rejecting the field.
- Exclude preview versions and reject wrong-year dates in the freshness checker.
- Keep self-test expectations independent from changes to the live snapshot.

## Preserved behavior and boundaries

Namespace safety, RBAC/least privilege, arbitrary UID/nonroot/SCC handling,
resource identity, target-served APIs, validation gates, failure conditions and
Arvan ownership remain. Existing chart assets, fixtures and manifest predicates
remain unchanged. The new fixture reference contains synthetic test expectations.
No consumer version, installed skill activation, cluster admission or measured
quality is inferred. Independent review and repository gates belong to the parent.

## Sources

The parent compatibility ledger records official sources revalidated 2026-09-26.
An additional bounded official lookup on that date resolved HPA tolerance maturity:
https://kubernetes.io/docs/concepts/workloads/autoscaling/horizontal-pod-autoscale/#tolerance .
It states stable since Kubernetes 1.37, first available in 1.33; the instruction
retains explicit user selection and requires older-target feature/field checks.
All durable version values and their dated source URLs are in the canonical file.

## Draft and compression fidelity

Pass one enumerated support versus authoring, explicit old-consumer paths,
unknown-runtime limits, major-specific flags and checker failure obligations.
Pass two removed repeated date facts from command examples and replaced them
with canonical pointers; it kept approval boundaries, platform exceptions,
security prohibitions, target discovery and every mandatory validation gate.
Legacy dual skill sigils were normalized only in Markdown files already changed,
as repository policy requires. No instruction was relocated as mere compression.
The deliberate behavioral corrections above are distinct from this wording pass.

## Limits

Helm 3 and newest Helm 4 runtime coverage are absent; only the parent-observed
Helm 4.2.3 binary is available. Repository-integrated gates, live freshness and
independent review are not this lane's authority. Source review found unrelated
historical reliability/diagnostic and Arvan documentation issues; they were not
repaired by this compatibility refresh.

## Focused verification, observed 2026-09-26

All commands ran from the repository root with BelowNormal priority. None was
CPU-heavy or parallelized. The source is frozen for independent gates.

| Command | Exit and result | Log in this directory |
|---|---|---|
| `python -B skills/sohrab/alaa-k8s-helm/scripts/check_versions.py --help` | 0 | `check-versions-help.log` |
| `python -B skills/sohrab/alaa-k8s-helm/scripts/check_versions.py --self-test` | 0; 17 cases | `check-versions-self-test.log` |
| `python -B skills/sohrab/alaa-k8s-helm/scripts/check_manifests.py --help` | 0 | `check-manifests-help.log` |
| `python -B skills/sohrab/alaa-k8s-helm/scripts/check_manifests.py --self-test` | 0; 7 cases | `check-manifests-self-test.log` |
| `python -B skills/sohrab/alaa-k8s-helm/scripts/check_manifests.py skills/sohrab/alaa-k8s-helm/scripts/fixtures/clean.yaml` | 0; clean | `clean-manifest.log` |
| `python -B artifacts/k8s-helm-compatibility-refresh/writer/focused_regressions.py` | 0; corrected three defects, externalIPs rejection preserved | `focused-regressions.log` |
| `git diff --check` | 0; rerun after final prose alignment, also 0 | `diff-check.log` |

Seven distinct focused checks, eight executions because final prose changed after
the first whitespace check. No failed writer operation or repair retry. The
complete scoped diff, including the new untracked fixture reference, is
`source.diff`. Parent captures the frozen content snapshot and owns independent
verification, live freshness, chart smoke and review. Parent's workflow validator
blocker is separate from these observed source results and was not retried here.
