# STORAGE proposal decisions

The parent ratified all nine decisions and claimed alaa-6dh.3.3.2 before product writes. Source repairs and bounded lane checks are complete. Independent acceptance remains with Phase 4.

AGENT: alaa-implementer-high. CONFIGURED: model/effort unpinned in the role definition; workspace-write. REQUESTED: gpt-6.1-sol/high, as recorded in the ratified plan. OBSERVED serving model/effort: unknown. Effective scope is the three assigned skill trees and STORAGE artifacts only; tool visibility grants no broader authority. No subdelegation or independent acceptance.

The immutable intake snapshot supplies all nine proposals below. Current Markdown is the primary local evidence owner. The installed role is neutral; high admission remains justified by coupled hook, authorization-outage and multipart control-plane decisions, rather than file count. Parent owns task state and final gates. Selected Hindsight recall is unavailable; the bounded local memory-registry search returned no storage-specific hit. Decisions use current repository and official source evidence.

## A27 - adapt hook failure classification

Owner anchors: tusd `references/45-hooks.md` responsibility table and response shapes; `references/20-decision-matrix.md` authorization placement; `references/55-tests.md` hook cases. Security/reliability owners classify permission decisions as gates and optional hints as contributors; trust owner forbids a backend authentication fallback and does not promise immediate bitmap revocation.

Keep upstream facts separate from required integration posture. A failed pre-finish hook really fails the completion response after storage finish; simply labeling that transport fail-open is false. Optional hint computation must catch its own contributor failure, log/count it and return a successful empty hook response (or an empty response with nil error in-process). The hook endpoint's own outage still fails completion; omit the optional hook when that dependency is unacceptable. Durable work remains outside the hint and queryable from the control plane.

Split post-receive telemetry from a revocation decision. A revocation lookup that denies or cannot decide must request StopUpload in a successful hook response, not return a transport error. A hook endpoint/transport failure itself logs and continues upstream; it does not enforce fail-closed revocation. Retain synchronous authorization before every method through the trusted boundary. If an active-stream revocation deadline is required, stop design approval until that bound is proven even during hook outages. Do not add service-side bearer introspection or claim immediate stop/deletion: progress delivery races completion; termination needs backend support and can fail, so retain durable denial/reconciliation obligations.

Official evidence read 2026-10-18: [hook documentation](https://tus.github.io/tusd/advanced-topics/hooks/) and [hooks.go](https://github.com/tus/tusd/blob/v2.8.0/pkg/hooks/hooks.go) `preFinishCallback`, `postReceiveCallback`; [datastore.go](https://github.com/tus/tusd/blob/v2.8.0/pkg/handler/datastore.go) `FileInfo.StopUpload`; [unrouted_handler.go](https://github.com/tus/tusd/blob/v2.8.0/pkg/handler/unrouted_handler.go) `writeChunk`, `emitFinishEvents`. These versioned checks are not live-engine proof or latest-release verification.

## A28 and O14 - adapt the part-size mapping

Owner anchors: minio `references/05-environment-contract.md` application variables; tusd `references/35-storage-lifecycle.md` multipart sizing; tusd env/Compose assets already map TUSD_S3_PART_SIZE to -s3-part-size. Preserve application STORAGE_PART_SIZE_BYTES (16 MiB estimate) versus binary wrapper TUSD_S3_PART_SIZE / library PreferredPartSize (50 MiB upstream baseline). Neither changes browser chunkSize. The Ala embedded service uses library construction, not CLI env automatically.

Add an explicit mapping, then require the actual tusd part ceiling and dynamically raised part size to fit provider bounds. Checking only preferred size is insufficient: s3store increases effective size above PreferredPartSize for large declared objects. Verify the selected binary's exposed controls or embedded MaxPartSize/MaxMultipartParts/MaxObjectSize; no invented CLI flag or implicit STORAGE_* wiring.

Official evidence read 2026-10-18: [s3store.go](https://github.com/tus/tusd/blob/v2.8.0/pkg/s3store/s3store.go) `New`, `calcOptimalPartSize`; [flags.go](https://github.com/tus/tusd/blob/v2.8.0/cmd/tusd/cli/flags.go) S3 part flags; [Arvan limits](https://docs.arvancloud.ir/en/object-storage/limits/) still publishes 400 MB per part and 10,000 parts. Keep the conservative byte interpretation and provider uncertainty; no provider mutation.

The existing generic baseline was also checked at v2.9.2 on 2026-10-18: [hooks.go](https://github.com/tus/tusd/blob/v2.9.2/pkg/hooks/hooks.go), [s3store.go](https://github.com/tus/tusd/blob/v2.9.2/pkg/s3store/s3store.go), [unrouted_handler.go](https://github.com/tus/tusd/blob/v2.9.2/pkg/handler/unrouted_handler.go). The targeted hook errors, cancellation/termination and dynamic-part conclusions agree with the older consumer pin. This does not refresh unrelated defaults or the declared latest release.

## A29 - accept explicit endpoint selection

Minio `references/05-environment-contract.md`: exclude endpoint, bucket and credentials from profile defaulting; shapes are documentation only. Arvan `references/15-environment-contract-deltas.md`: relabel the value column to allow required shapes, mark endpoint examples as explicit operator selection, and pair region with the selected endpoint rather than silently choose Simin. Align the routing wording in Arvan connection reference. Official [SDK overview](https://docs.arvancloud.ir/en/developer-tools/sdk/object-storage/) and limits page read 2026-10-18 confirm two regional endpoints and region isolation. Existing checker already checks pinned endpoint/bucket/credentials.

## A30 - accept removal of the nonexistent knob example

Arvan `references/15-environment-contract-deltas.md`: remove the claim that a client-abort boolean already exists or has defaults. Keep the requirement to add a genuine missing knob in the shared owner when implementing such behavior; no new variable or optionality is invented. Preserve mandatory Arvan abort and lifecycle backstop.

## A31 - adapt unsafe historical command handling

Minio `references/75-mc-command-line-client.md`: retain the historical positional command as evidence, with DO NOT COPY inside its fence. Mark scoped configuration-file schema/release compatibility unverified rather than claim it works on every release. Keep the verified secret-in-argv reason and both alternatives; no replacement command is fabricated. No live mc invocation is needed.

## B24 - adapt ownership without losing the defect

Preserve both external topic maps. Minio routes generic namespace, tenant prefix and provider bounds; tusd routes upload layout, sidecars, effective part size and temp disk. Replace only generic restatement in tusd storage reference with a precise owning pointer. Retain its historical missing-tenant-prefix observation, impact on prefix policies/cost/lifecycle and explicit existing-key migration warning. Random identifiers and sidecar collision requirements stay with upload identity. Do not remove framework/provider differences.

## O3 - accept source-name correction; retain dated evidence

Normalize the mistaken phrase "tusd-upload-platform repository" to "Ala tusd repository" throughout the owned minio skill, including SOURCES.md. Keep the dated body section and its test-stack/production distinction; no relocation is justified. Historical observations remain historical and unverified as current; this lane does not re-audit another repository.

## O5 - accept output proportional to scope

Tusd SKILL.md expected output: preserve the full ten-part end-to-end design set; a partial review reports applicable items and cross-boundary effects only, with register, tests and risks still identified. Hook work includes posture, lifecycle and observability. Do not require unrelated topology/retention chapters for one hook review.

## Invariants and alternatives

Preserve per-method authorization, trusted tenant/object prefixes, capability-URL sensitivity, resume/offset behavior, credential boundaries, storage unknown-outcome reconciliation, retention/recovery, redirect and CORS rules. Changes are instruction repairs only: no service, provider, metadata default, version bump, key migration or deployed config change. Reject blanket unification of part defaults, transport-error-as-denial, immediate-stop guarantees, missing-prefix erasure and reference-count-driven router relocation. Rollback is scoped text restoration; no data rollback is involved. Added wording earns its cost through explicit revocation-outage and independently configured part-ceiling design checks.

## Proposed focused proof

After ratification: one tiny source assertion per proposal group, then one bounded task check covering all decisions and source/link/encoding preservation. Add hook consumer-test obligations for optional-hint dependency failure versus hook transport failure; explicit revocation denial/lookup outage versus hook endpoint outage; late stop/unsupported or failed termination with denied future resume. Add part-size consumer-test obligations that distinguish preferred from effective ceiling. These are required future consumer tests, not a simulated runtime pass here.

Requested exact acceptance commands: `python -B scripts/check_fleet_references.py --skill alaa-minio-object-storage --skill alaa-arvan-object-storage --skill tusd-upload-platform`; `python -B skills/sohrab/tusd-upload-platform/scripts/validate_pack.py --root skills/sohrab/tusd-upload-platform`; touched Markdown links through the existing link checker only after its supported selector is inspected. Native posture checker self-tests are not covered-input proof for Markdown-only changes and are omitted. No full-pack or consumer integration/upload suite.

## Deferred source drift

The current [Arvan SDK index](https://docs.arvancloud.ir/en/developer-tools/sdk/object-storage/) lists CORS put/delete, multipart listing and tagging pages which the historical compatibility matrix calls undocumented; the current [limits page](https://docs.arvancloud.ir/en/object-storage/limits/) states no request/traffic ceiling. Provider operation behavior remains unverified. This is outside the nine assigned proposals. Parent receives the follow-up for page-specific verification; the historical compatibility matrix is unchanged.

## Ratified validator alignment

The parent additionally ratified removal of the legacy numeric router threshold. The previous source rejects a valid external map with one content reference; `STORAGE-router-before.json` preserves its exact diagnostic and source SHA-256. The repaired `check_single_router` accepts external placement regardless of count and still rejects a missing map, duplicate body pointer or direct body reference beside the map. Existing path-existence and full map-coverage checks are unchanged.

Six focused fixtures cover the accepted one-reference external map and rejected extra body pointer, duplicate map pointer, broken route, unrouted reference and missing external map. `router_policy_self_test` is wired into the existing normal self-test and callable independently; only that callable ran. The existing validator has no inline-body route coverage checker, so no inline-above-threshold path-validation claim is made. No existing path or coverage gate was disabled.

## Implementation and observed evidence

`STORAGE-final-snapshot.json` records HEAD, the sorted path-NUL-bytes digest of all 59 owned inputs, 25 touched files and 34 unchanged inputs. `STORAGE-checks.json` records exact commands, working directory, results and proof limits. Ten MinIO files were compared in full against the exact source-label/sigil transformation; semantic diffs were inspected separately. All touched files are nonempty UTF-8 without BOM with LF. The draft was rewritten into the final clauses without relocating routers or deleting files; every deadline, trust boundary, cleanup obligation, source caveat and provider distinction survived.

- Tiny source assertions passed for A29/A30/A31/O3 and A27/A28/B24/O5/O14.
- Scoped fleet check: exit 0, three skills, 38 Markdown files, 138 citations, no finding; nine informational target paths remain.
- Touched Markdown links: exit 0, 24 files. Scoped `git diff --check`: exit 0.
- Focused router callable: exit 0, six expectations; rerun after the final checker-byte changes. The initial temporary-fixture probe failed before assertions with sandbox WinError 5; one exact outside-sandbox retry succeeded. No ACL or global setting changed.
- The local tusd pack check initially returned shell exit 1, `MISUSE: PyYAML is required to validate agents/openai.yaml: No module named 'yaml'`. PyYAML was missing from default Python 3.14, installed Python 3.13 and the app-bundled Python. This did not establish infrastructure absence: the parent required the supported fallback check below.
- Supported fallback: canonical `ci-image` README and `alpine-tools/Dockerfile` declare Python/PyYAML. Cached immutable image `sha256:d7d5200cf678b9439e2c1bd44bfa5c99fb90915fd9bad96a4a0c4847557d7883`, OCI revision `cb9abf281b9109f4ab8c4c06d9fe33b90e24f29a`, passed an import/full-YAML parse probe with Python 3.14.7/PyYAML 6.0.3. The unchanged required tusd validator then passed all 10 checks, exit 0, zero warnings. Execution used a read-only repository mount, `--pull=never --network none --read-only --cap-drop ALL --pids-limit 64 --memory 128m --cpus 1`. No pull, install, parser substitution or global change occurred. Docker's sandboxed inventory hit named-pipe denial; its exact outside-sandbox inventory retry succeeded. A cached uv PyYAML package was also found but not used.

Resource policy: lightweight bounded commands from the repository root; no heavy suite. Unchanged posture-checker self-tests, unrelated tusd self-tests, live uploads/provider calls and independent acceptance were not run. Consumer test rows describe obligations for future upload-plane changes; they are not executed consumer proof here.

Measured skill bytes changed from 201573 to 198584 for MinIO, 83114 to 83465 for Arvan, and 192300 to 199748 for tusd. Growth adds explicitly verified revocation-outage/termination-race handling, independent effective-part bounds and maintained router-policy fixtures. These are footprint measurements, not quality, performance or cost measurements.
