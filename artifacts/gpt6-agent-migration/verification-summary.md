# GPT-6 migration verification record

## Tested source

- Branch: `codex/gpt6-agent-migration`.
- HEAD: `164d06a8944a87eb77a8b458c505b7efcb82268d` (no new commit).
- Source identity: 201 files in `source-snapshot-manifest.json`, SHA-256 `2e9b5ed0eb60d82ebc35792c9971399d824d10f36044db1ce04977ebaa0a049b`, observed before final gates at `2026-09-25T10:15:52.256190+00:00`.
- Method and exact paths: `source-snapshot.json` and the manifest. All 201 current hashes matched afterward.
- The verifier initially misread the JSON array shape. Its invalid initial integrity output is retained; `final-verification/source-integrity-corrected.txt` records the corrected comparison with the parent's pre-gate manifest. The sixteen gates were not repeated.

## Observed proof

| Evidence | Result | Limit |
|---|---|---|
| Ten approved baseline gates | All exit 0 | Old validators missed stale manifest drift |
| Sixteen final source gates | All exit 0 | Commands and outputs: `final-verification/final-gates.json`, `final-01.log` through `final-16.log`; source consistency, not live quality |
| Workflow unittest | 45 tests, exit 0 | Exact suite recovered outside sandbox after temporary-directory permission failures; workflow hashes unchanged |
| Renderer retained-fixture self-test | Exit 0 | `renderer-selftest-final/`; checks safe TOML serialization and generated-file drift |
| PowerShell installer negative cases | Nine rejected paths, exit 0; destination directories absent | `agent-lane-preflight-powershell-fixed.log` and retained fixtures; includes alternate-source bypass |
| Bash installer negative cases | Nine rejected paths, exit 0; destination directories absent | `preflight-bash-recovery/`; recovered outside sandbox after MSYS signal-pipe Win32 error 5 |
| Live MCP materialization in scratch | 23 profiles resolved against six live servers, exit 0 | `materialized-agents/`; validates exact grants, not installation or activation; later instruction-only edits do not change tested grants |
| Independent artifact review | APPROVED after fixes | Source correctness, instruction contracts, grant/installer boundaries, packaging, and governance; does not prove live quality or doc size |
| Protected user file | `p.md` bytes and original staged empty blob unchanged | SHA-256 `8995E51332EEE0F3F89E9D2BB1A5D40EC6C1F8B2AE5DB03A3FDBBFE4DB59B2FD` |

## Findings resolved

1. Evaluation records now reject concrete observed/requested identity mismatches and incomplete failed-run safety/configuration fields. Unknown identity requires separate configuration-control evidence before a verified configuration claim.
2. Completed adaptive workflow phases reject placeholder commit prose without a genuine commit ID, scoped content snapshot, or explicit no-change record.
3. Both agent installers reject an alternate source directory before any destination write; source preflight and materialization consume the same canonical directory.
4. Standard and deep reviewer disagreements share the adversarial-review trigger.
5. Codex instruction review permits bounded native source inspection while rejecting commands embedded in reviewed material and all mutation.
6. Independent gates remain mandatory where triggered; local-only completion no longer forces a merge prompt or unauthorized integration.

## Unproven and unavailable

- The eight-scenario, two-configuration, two-repeat comparison remains 32 unrun rows in `evaluation-results.json`, `complete=false`. Its record validator passed; no quality verdict was inferred.
- CLI 0.147.0 first failed the minimal Luna probe on sandbox state/IPC access, then its one exact escalated retry reached the backend and received HTTP 400: the requested model is unsupported for this ChatGPT account. This proves only that execution-surface limitation. No hidden fallback or upgrade was attempted.
- Installed home-directory agents, serving identity, and real profile activation were not verified or changed. No installation, commit, merge, or publication occurred.
- New index entries appeared during the task. The implementation lanes report no staging commands. Their origin is unverified; they were preserved rather than reset. The user's `p.md` index entry remains the original empty blob.

## Documentation size

The touched-link check found no broken links in the five selected guide/index documents. The size gate exited 1:

| File | Before | Current | Grade |
|---|---:|---:|---|
| `README.md` | 48 | 51 | Yellow: compact generated inventory and migration route remain together |
| `install-skills.md` | 401 | 405 | Red, explicitly accepted for this revision |
| `skills/sohrab/README.md` | 232 | 232 | Red, explicitly accepted for this revision |
| `skills/sohrab/README.fa.md` | 226 | 226 | Red, explicitly accepted for this revision |
| `docs/gpt6-agent-migration.md` | absent | 67 | Yellow: one migration decision and complete comparison table |

The three red documents were already over the threshold. The user explicitly accepted the exact current files and line counts on 2026-09-25. The same five-file links/line-budget command with --allow-red for those three paths then exited 0; acceptance was not inferred from source-gate success. Broad catalog/installation-document restructuring was not silently added to the migration.

## Curation and authority

The engagement's reusable policy decisions and regression checks now live in their repository owners. No additional durable memory note was admitted: duplicating them would create a second owner, and transient CLI/sandbox behavior remains task evidence. No memory was written; no pipeline reopen is required by curation.

## Agent accounting

Seven distinct agents participated: `dependency_audit`, `official_guidance`, `policy_implementation`, `agent_pack_implementation`, `governance_implementation`, `policy_review`, and `final_verification`. The last five requested configurations were respectively `gpt-6-astra/high`, `gpt-6-astra/high`, `gpt-6-sol/high`, `gpt-6-astra/high`, and `gpt-6-luna/low`. Requested configurations for the two initial research lanes are unavailable in this resumed record. Observed serving identity and total token counters are unavailable; none is inferred from a pin. Branch span to an authorized commit is unavailable because no commit was authorized or made.

## Completion lifecycle

- IMPLEMENTED: proven on the identified source snapshot; changes remain uncommitted.
- MERGE_CANDIDATE: proven for the repository migration after independent review, source gates, installer checks, workflow tests, and the explicit documentation-size acceptance. Live calibration remains a separate unproven claim.
- RELEASE_CANDIDATE: not requested.
- PUBLISHED: not requested.
