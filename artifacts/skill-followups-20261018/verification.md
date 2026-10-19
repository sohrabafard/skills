# Skill follow-up verification — 2026-10-18

## Disposition

Both investigations confirmed skill defects and received scoped corrections under the user's
follow-up authorization. They are independent `spike` issues with label `repo:skills` in the
shared `alaa-task-hub/.beads` workspace. `alaa-147` has a `discovered-from` relationship to
`alaa-6dh.3.3`; `alaa-x05` has one to `alaa-6dh.3.2`. Neither is a child of that epic, so an
epic-child view will not list them. Remote synchronization was not performed or verified.

## alaa-147 — obsolete Arvan documentation claims

The skill classified operations as undocumented despite current official per-operation SDK
pages. Eleven pages were read, covering CORS put/delete, multipart upload/part listing,
object tagging, object listing (including the separate ListObjectsV2 Go example), deletion
and bucket/object ACL get/put. Exact URLs, content observations and read dates are in
`skills/sohrab/alaa-arvan-object-storage/references/SOURCES.md`, under the per-operation refresh.

Corrected seven matrix rows plus the repeated CORS, migration and cost guidance. The matrix
remains the single operation inventory. Its existing Supported label means documentation
was read; it does not mean a live provider request succeeded. SDK example quality, pagination,
browser preflight, lifecycle parity and target-region behavior remain separate verification
obligations. No credentials, provider calls or bucket mutations were used.

Changed references: `20-s3-compatibility-matrix.md`, `30-limits-quotas-and-cost.md`,
`40-migration-and-portability.md`, `SOURCES.md` in that skill.

## alaa-x05 — a false-green singleton oracle

Laravel v13.34.0 TestCase assigns a newly created application in `refreshApplication()`.
Recreating the container also recreates ordinary singleton instances, so the former example
could pass against the very defect it claimed to detect. Container `scoped()` tracks the
binding; `forgetScopedInstances()` removes those tracked instances without removing ordinary
singletons. Octane v2.20.0 uses a booted root application and per-request sandboxes; its
cleanup listener invokes scoped cleanup and removes configured flush entries. Exact pinned
sources are in the skill's `references/source-map.md` under Leak-harness mechanics.

Shape A now keeps one container and checks the actual scoped registration. Shape B owns
worker lifecycle, listener wiring and flush-configuration claims, with readiness, positive
tenant fixtures and same-surviving-worker verification. The bisect guide now selects the
appropriate shape and no longer describes a pre-cleanup snapshot as post-flush proof.
No production binding, listener, tuning value or deployed service was changed.

Changed references: `leak-detection-harness.md`, `diagnostic-drills.md`, `source-map.md`
in `skills/sohrab/alaa-octane-performance`.

### Observed behavioral proof

Local Docker Desktop Linux engine; cached `linux/amd64` application image:

```text
registry.takhtenegar.ir:5010/alaa/services/auth@sha256:cdaadb011ff58135f93516cfb9f460ccd539f6373a925bb1354ee64781a276ba
PHP 8.5.11
laravel/framework v13.34.0
laravel/octane v2.20.0
```

The run used one CPU, 512 MiB, no network, a read-only filesystem and evidence mount, no
capabilities and no new privileges. Only the packaged autoloader/framework was used; the
service was not bootstrapped. No image pull, package installation or sibling checkout edit.

Reproduce from the repository root in PowerShell (the mount path resolves to this checkout):

```powershell
$probeEvidence = (Resolve-Path artifacts/skill-followups-20261018).Path
docker run --rm --pull=never --network none --read-only --cpus 1 --memory 512m --cap-drop ALL --security-opt no-new-privileges --mount "type=bind,source=$probeEvidence,target=/evidence,readonly" --entrypoint sh registry.takhtenegar.ir:5010/alaa/services/auth@sha256:cdaadb011ff58135f93516cfb9f460ccd539f6373a925bb1354ee64781a276ba /evidence/run-octane-probe.sh
```

Observed output, aggregate exit 0:

```text
No syntax errors detected in /evidence/octane-probe.php
No syntax errors detected in /evidence/octane-snippet.php
scoped: ORACLE PASS
singleton: ORACLE FAIL: previous request's tenant survived the flush: 'tenant-a'
no-reset: ORACLE FAIL: previous request's tenant survived the flush: 'tenant-a'
rebuild-singleton: ORACLE PASS
scoped: ORACLE PASS
PASS: corrected oracle green, both mutants red, restored green; rebuilt singleton falsely green.
```

The two negative controls exited 1 as required; the original and restored cases exited 0.
The rebuilt-container case illustrates the old mechanism's false green, not a full PHPUnit
application bootstrap. `octane-snippet.php` contains the exact PHP method extracted from the
edited Markdown, plus two single-change mutants. Its assertion adapter uses strict PHP
checks instead of PHPUnit; the container is the real installed framework. The tenant holder
is a deterministic in-memory fixture. This is unit/in-memory proof, not a running Octane
server test, deployed tenant-isolation proof, performance measurement or Sentry resolution.
Telemetry was not relevant: this repository ships guidance, not the affected service runtime.

Installed source SHA-256:

| Source within image | SHA-256 |
|---|---|
| framework Container.php | `8bbfbc5955205f817106077355a493952e685bc376653236a7188f20ff634ea8` |
| framework Testing/TestCase.php | `2fdaa924cae3a27e2427b08ad5067ca5031566e84d9fa724ce2c6ac0f10880b2` |
| Octane FlushTemporaryContainerInstances.php | `9765b917d242abdd21c1a4fd506617389f1b92c6c5f00cdc1a15a5a27152d1e3` |
| Octane Worker.php | `bc514ae97f53dd89d082648762f328e3e412f6f31c7222dbf0e9dc3273e8f959` |

## Repository checks and final inspection

- `python scripts/validate_sohrab_skill_pack.py`: exit 0, 69 skills; existing body-length
  warnings only. No SKILL.md entrypoint changed.
- `python scripts/check_fleet_references.py --skill alaa-arvan-object-storage --skill alaa-octane-performance`:
  exit 0, 16 Markdown files, 103 citations, no findings; one existing informational target path.
  Rerun after the final diagnostic/source wording correction passed.
- `python skills/sohrab/alaa-arvan-object-storage/scripts/check_arvan_storage_config.py --self-test`:
  exit 0, five tree cases, eight size cases, output format verified. The sandboxed attempt
  failed to create its temporary fixture directory with WinError 5; the exact escalated retry passed.
- `git diff --check`: exit 0. Scoped diff inspected against source claims and proof boundaries.
  Legacy dual-form skill calls were normalized only in already edited files, as repository policy requires.
- No unrelated broad application suite, provider integration suite, live worker test or benchmark
  was run. This follow-up changes documentation and its demonstration, not a service.

The first Docker inventory read was denied by the named-pipe sandbox; its scoped escalation
succeeded. The cached shared CI image intentionally lacks PHP (confirmed by its owner README
and a failed PHP entrypoint probe), so the already cached application image supplied the runtime.
An initial version probe found no lockfile `source` field; final provenance uses package versions,
image digest and actual installed file hashes rather than inventing a source commit.

Growth is confined to newly verified provider API evidence and the corrected oracle/proof
boundaries. No router moved, no topic map retired and no always-loaded entrypoint grew.

A concurrent vendor-subtree merge moved HEAD from `a730b1c31` to
`18f0264e7dfbb1b0cb02ad00fc0e549f2cd3ed25`. The diff between those commits contains no changes
to `skills/sohrab`, `scripts` or `AGENTS.md`, so it did not alter these checks' covered inputs.
Those vendor changes are not this follow-up's work. No Git commit, push or Dolt remote sync
was performed for this follow-up.

## Reviewed snapshot

Product references and executed PHP/shell evidence are listed in `scope.sha256`.
The scoped digest is SHA-256 over that UTF-8/LF manifest, sorted product paths
then sorted probe paths; each row is the file SHA-256, two spaces, and repository-relative path.

`HEAD 18f0264e7dfbb1b0cb02ad00fc0e549f2cd3ed25 + scoped SHA-256 e01171bc1434dd4723bd14e38c0ad099208d6b0c4a017cec1cdacccd68cdbc2e`

Verified UTF-8 without BOM, LF, portable artifact paths and exact documentation-method
parity with the executed snippet. Beads lint initially required Findings sections in both
spikes; after appending findings without removing original scope/provenance, both passed.

Closure readback confirmed `alaa-147` and `alaa-x05` are `closed`, with saved Findings,
distinct close reasons, this evidence path, reviewed snapshot and unchanged discovered-from
edges. The scoped stale check reported neither issue. Existing Python caches dated April
and July were left untouched; these checks created no repository-local bytecode cache.
