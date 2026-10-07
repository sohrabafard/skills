# Verification — entitlement skill source owners

## Outcome

The requested static checks passed on the unchanged candidate files. Static evidence supports the owner/path correction and preserved textual contracts; no runtime or deployed behavior is claimed. The candidate tree digest declared in the manifest does not match the reproducible digest, so the frozen snapshot identity is not fully verified.

## Role and environment

- Agent: alaa-verifier
- Configured model/effort: gpt-6-luna / low (from the installed role definition, supplied in dispatch)
- Requested model/effort: not separately supplied
- Observed model/effort: unknown; runtime evidence did not expose it
- CLI transport was used because collaboration spawn was unavailable. No MCP was enabled.
- Cwd: repository root; HEAD remained `2a2340d3677945578b505fce49de60e11561037d`.
- Initial status: 12 expected modified Markdown files and untracked artifact family; inaccessible `_to_delete` directories caused Git status warnings. Final status: same 12 modified files plus artifact family; no unexpected source changes observed.
- Runtime sandbox/grant enforcement: unknown. Only evidence writes were made under this artifact family.

## Candidate integrity

`candidate-manifest.json` lists 43 files. All 43 current raw-file SHA-256 values and byte counts match their entries, both before and after commands. The manifest file SHA-256 is `c17eac5f88dff08e609ee093cd412b6d046af704673f70316a09be32f268ed94`. Recomputing the plan's stated sorted `sha256␠␠path LF` row format from current bytes yields `615cc91174c1ded0da9346d03ad22067a0f189153f646e8161f6a2e3036e3e68`, not the declared `978b8b181a5381fe502232d3baa487a50b9ef55df97b4b54da1283068059048a`. The per-file contents are frozen, but aggregate identity is discrepant.

## Command evidence

All dispatched checks were focused/static, ran sequentially once, and exited 0. No CPU-heavy suite or retry was used. Proof level 1 is static per `skills/sohrab/alaa-testing-strategy/references/40-proof-strength.md`; no higher proof level is reached.

| Command | Cwd | Limits | Duration | Exit | Classification | Tier | Proof |
|---|---|---|---:|---:|---|---|---|
| `python -B scripts/validate_sohrab_skill_pack.py` | repo root | 120s; no CPU runner required | 0.257s | 0 | PASS | focused | 1 static |
| `python -B scripts/check_skill_index.py` | repo root | 120s; no CPU runner required | 0.186s | 0 | PASS | focused | 1 static |
| `python -B scripts/check_fleet_references.py` | repo root | 120s; no CPU runner required | 2.855s | 0 | PASS | focused | 1 static |
| `python -B scripts/check_lifecycle_contract.py` | repo root | 120s; no CPU runner required | 0.403s | 0 | PASS | focused | 1 static |
| `python -B skills/sohrab/alaa-codex-orchestrator/scripts/check_agent_contracts.py` | repo root | 120s; no CPU runner required | 0.131s | 0 | PASS | focused | 1 static |
| `python -B skills/sohrab/alaa-trust-gateway-auth/scripts/trust_boundary_check.py --self-test` | repo root | 120s; no CPU runner required | 0.168s | 0 | PASS | focused | 1 static |
| `python -X utf8 -B "$env:USERPROFILE/.codex/skills/.system/skill-creator/scripts/quick_validate.py" skills/sohrab/alaa-services-contract` | repo root | 120s; no CPU runner required | 0.157s | 0 | PASS | focused | 1 static |
| `python -X utf8 -B "$env:USERPROFILE/.codex/skills/.system/skill-creator/scripts/quick_validate.py" skills/sohrab/alaa-trust-gateway-auth` | repo root | 120s; no CPU runner required | 0.159s | 0 | PASS | focused | 1 static |
| `python -B skills/sohrab/alaa-repo-docs/scripts/check_markdown_links.py . --files [the 12 dispatched paths]` | repo root | 120s; no CPU runner required | 0.173s | 0 | PASS | focused | 1 static |
| `git diff --check` | repo root | 120s; no CPU runner required | 0.090s | 0 | PASS | focused | 1 static |

Per-command logs: `01-validate-sohrab-skill-pack.log` through `10-git-diff-check.log`. The link-check log abbreviates the file list; the exact full command is preserved in the dispatch and above.

## Static acceptance inspection

- The sibling `entitlement-api/docs/contracts/repository-extraction-v1.md` exists and assigns canonical model/contracts and domain mapping to `authz-openfga`, event/API ownership to `entitlement-api`, request-time checker interface to `authz-sidecar`, and projection to `entitlement-projector`.
- Named sibling source pointers were checked for existence in the `authz-openfga`, `authz-sidecar`, `entitlement-api`, `entitlement-projector`, and `gateway` checkouts. Key model contract, endpoint permissions, checker contract, event contract, projector operations, gateway values/template and Lua paths all exist.
- Changed text distinguishes pinned generated bundles as consumer snapshots from authoring roots, preserves stable runtime identity `projector`, and leaves gateway executable configuration as the edge authority. This is a static text/source-presence finding only.
- Changed files: 12 Markdown references. All decode as strict UTF-8, have LF-only line endings and no BOM.
- Normalized whole-skill size: services 430800 bytes (baseline 430883, -83); trust 135513 bytes (baseline 135534, -21).
- Entrypoints, scripts, metadata, `22-failure-load-and-deprecation-contract.md`, `23-queue-and-exchange-registry.md`, and dated `95-fleet-conformance.md` were unchanged.
- The fleet checker passed with 315 informational unmarked target paths across 30 skills, including 42 in services-contract and 10 in trust-gateway-auth; these are informational by checker contract.

## Failures, blockers, skipped limits

No dispatched command failed or timed out. The aggregate candidate SHA mismatch is an integrity caveat, not a command failure. No checks were skipped from the dispatched set. Runtime integration, deployed gateway behavior, live authorization, and production state were excluded and remain unverified. The independent instruction-review transport files already present in the artifact record failed/empty CLI attempts; they are outside this verifier command set and were not retried here.

## Snapshot identity follow-up

The earlier aggregate-identity caveat is superseded by this independent recomputation; all original gate evidence above is retained. The prior check encoded entries as `sha256  path\n`, which did not match the manifest's declared encoding. Rechecking the declared sorted `path\0raw-file-sha256\n` encoding produced `978b8b181a5381fe502232d3baa487a50b9ef55df97b4b54da1283068059048a` from both manifest entries and current file bytes. All 43 entry hashes match current bytes (zero mismatches), and current HEAD `2a2340d3677945578b505fce49de60e11561037d` matches the manifest HEAD. The assertions passed. This resolves only the aggregate snapshot identity caveat; it does not alter or expand the ten gate results or static acceptance limits.

Follow-up command: the exact PowerShell here-string Python command in `verifier-snapshot-dispatch.txt`, run from the Git root with `python -B -`. Duration: 0.8s. Exit: 0. Classification: PASS, focused, proof level 1 static. No retry. No source or manifest changes.
