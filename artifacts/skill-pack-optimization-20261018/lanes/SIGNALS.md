# SIGNALS lane decisions

Status: implementation complete; independent Phase 4 review pending. Full reads of every owned `SKILL.md`, reference, and script were completed before edits; parent authorized subtask `.2`.

## Allocation and scope

- Agent profile: `alaa-implementer-low`; the installed definition is unpinned for model and effort. The parent verified an explicit `gpt-6-luna` / `medium` dispatch with `fork_turns=none`. Serving identity remains unknown. Effective filesystem access is `workspace-write`, narrowed by the parent to the four named skill trees and this lane's artifacts. MCP enforcement is not inferred from filesystem sandboxing.
- Scope: `alaa-bale-provider`, `alaa-sms-provider-mediana`, `alaa-signoz-clickhouse-docs`, and `clickhouse-performance-schema-ops`; no shared-owner files, roots, indexes, scripts, or sibling lanes.
- Bounded semantic admission: explicit outcome and finite trees; grounded frozen decisions and current owner references; settled cross-owner policy; bounded pointer and conditional-wording discretion; and supplied per-item checks plus scoped reference selectors. Reassess if a read uncovers a new cross-boundary decision.

## Ratified decisions

| Intake | Decision | Invariants retained |
|---|---|---|
| 01:A32 | Replace provider line-number citations to service metric registry rows with stable metric-family or section names. | Metric names and ownership stay unchanged; cite the `alaa_dependency_*` rows by name. |
| 01:A42, B21, C1; 02:O23 | Provider skills point to observability's existing phone-derivative rule and remove duplicate masking policy. Default behavior is omission or an independently approved stable internal reference. A separately approved diagnostic derivative may retain only the verified country calling code, optional leading `+`, and fixed `[redacted]` marker. | Never preserve subscriber digits, hash/token surrogates, or emit the derivative as an identity/correlation key or metric label. Retain provider-specific wire-form, token, pattern, message-text, and five-egress constraints. Do not conflate an internal reference with the diagnostic derivative. |
| 01:B22, 02:O23 | Provider skills retain only their vendor-specific mapping to reliability failure classes and point to the owner. | Mediana's zero retry budget and envelope-key resolution remain distinct from Bale's same-`request_id` retry behavior. |
| 01:B25, 02:O22 | `alaa-signoz-clickhouse-docs/SKILL.md` remains the SigNoz tenancy owner. Remove the duplicate tenancy statement from ClickHouse reference 15, retaining a pointer and the raw plus aggregate `project_id` query obligation. | Preserve historical ClickHouse commit/line provenance and its existing re-derive instruction. Do not invent a current schema, default, or new provenance scheme. |

The chosen masking owner is `alaa-observability-soc/references/80-review-gates.md`, the existing classification and egress gate. A new skill/reference is rejected by frozen C1; security review is a plausible alternative but does not own the existing telemetry field-classification gate. No cross-owner change is included in this lane.

## Frozen intake and source evidence

The proposal text came from the embedded report content in `artifacts/skill-pack-optimization-20261018/intake-snapshot.json`, whose SHA-256 is `2bba02162e327a1fefd7bda0a18820cf36c1717e4d41c8bff8bd1aa1ef980ca6`. The snapshot records report hashes `01=6de7223950f08711ad4946039995286cc7efafd4a1558f1876f8ddcf13f6e03a` and `02=da0309f20c76b9bc98a3d3eda4e10ffcd8cdc2a3c815127a92c690e1ce06c7fa`; later report shrinkage explains current on-disk hash drift, so the embedded snapshot content remains the proposal source.

| Source | SHA-256 |
|---|---|
| `artifacts/skill-pack-optimization-20261018/lanes/SHARED.md` | `61a690cd413e74c79ba8acf320f43fe6466de2258fb53bd2432118c38550ba65` |
| `skills/sohrab/alaa-observability-soc/references/80-review-gates.md` | `a4523ec3792b96dc8a7dd9981949058ace00eb77552d678c8cfc085bf972d216` |
| `skills/sohrab/alaa-services-contract/references/24-metric-registry.md` | `a12ff7b35a90fbb8ebaa01364e4ecd797bcc3fb418aea80badc457a68841742d` |
| `skills/sohrab/alaa-reliability-sla/references/20-retries.md` | `fca44fb3b8dc77dd51f159d4606bcc64795c96723302e9edc8e0bc89428935f2` |
| `skills/sohrab/alaa-signoz-clickhouse-docs/SKILL.md` | `53c1b7c265a3092b20b8d09851a061d1c7c1ffdbdf9ebbefc48457c40136ab1c` |
| `skills/sohrab/clickhouse-performance-schema-ops/references/15-fleet-clickhouse-boundary.md` | `7c6045aa7b95d8680415195aee400db335183ba5f5ded1e75c044e3eb6b32cf0` |

## Verification plan after authorization

- Read all owned `SKILL.md`, reference, and script files before editing; inspect the relevant provider mappings and ClickHouse cross-boundary call sites.
- Apply only the per-item transformations above. Preserve the provider-specific vendor maps and all existing non-target semantics.
- Run only the supplied bounded selectors: `python -B scripts/check_fleet_references.py --skill alaa-bale-provider --skill alaa-sms-provider-mediana --skill alaa-signoz-clickhouse-docs --skill clickhouse-performance-schema-ops`, plus the existing repository-docs link checker on changed Markdown and encoding/diff/manifest checks. Do not run full or unrelated suites.
- Rollback is scoped text restoration; there is no data or runtime state to migrate. Parent owns independent Phase 4 review, broader acceptance, Beads, plan/checkpoint, and Git integration.


## Implementation evidence

- Provider phone handling now preserves all five prohibited output surfaces, defaults to omission or an independently approved stable internal reference, and points the separately approved diagnostic derivative to observability's `references/80-review-gates.md`. It is never a correlation key or metric label. SOC/SIEM forwarding points separately to the named egress section in `references/70-soc-evidence.md`.
- Provider metric citations use the `Downstream dependency` section and canonical `alaa_dependency_*` names, not line numbers or shortened stems.
- Mediana's no-retry route remains budget 0 and resolves ambiguous sends at the envelope key; the failure-class page now routes general refusal/timeout retry doctrine to reliability.
- ClickHouse reference 15 points to the SigNoz skill for tenancy rationale and retains the `project_id` requirement for both `wa_raw` and `wa_agg`; the dated commit, line citations, and re-derive trigger remain intact.
- First scoped fleet-reference run failed on an incorrect ref70 filename in the two provider pointers. Corrected once to the current owner path and reran successfully; no other edits resulted.
- Changed files: `skills/sohrab/alaa-bale-provider/SKILL.md`; `skills/sohrab/alaa-sms-provider-mediana/SKILL.md`; `skills/sohrab/alaa-sms-provider-mediana/references/30-failure-and-ambiguity.md`; `skills/sohrab/clickhouse-performance-schema-ops/references/15-fleet-clickhouse-boundary.md`.
- Focused verification: scoped `check_fleet_references.py` passes (4 skills, 61 Markdown files, 206 citations); repo-docs Markdown-link checker passes on the four changed files. No broad, live, or provider-send checks were run.
