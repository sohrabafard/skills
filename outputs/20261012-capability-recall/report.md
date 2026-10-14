# Capability recall and lesson economy
Status: IMPLEMENTED and MERGE_CANDIDATE; independent source verification and scoped reviews passed. RELEASE_CANDIDATE and PUBLISHED were not requested. Updated 2026-10-13.

## Scope and ownership
This archive records an implemented instruction-pack change prompted by repeated local-tool blockers. Current policy remains in canonical owners: `/alaa-memory-os` owns capability recall, adapter boundaries and hooks; the selected store adapter owns store-specific query mechanics; `/alaa-codex-runtime-ops` and the orchestrators own cause-specific recovery, retry controls and native lifecycle status; `/alaa-workflow` owns active continuity and task evidence; `/alaa-extract-agent-lessons` owns lesson admission, shaping and routing; `/alaa-prompting-guide` owns model capability evidence and instruction compression. The RFC preserves design history; it does not activate a second policy source.

Semantic changes add a bounded capability-owner check before a local miss becomes a blocker; distinguish local absence, incompatible infrastructure, missing authority, actual failure and unknown; prevent memory from granting authority or resetting retries; and keep workflow state out of memory. Lesson admission/routing follows its owner. PreCompact is nonwriting; SessionStart reports drift without printing supplied paths or content. Existing hook output shape remains. Current source paths are listed in [the source manifest](./final-source-manifest.json).

The separate wording pass compressed approved owner text. The frozen evaluation packet's only source divergence from the final text is a whitespace-only wrapped owner/path line; the reviewer reconstructed it and confirmed token equality, while six other packet texts were unchanged. This packet comparison does not claim that no other source files changed. See [the final compression manifest](./compression/final-manifest.json).

## Evidence
Independent proposed-decision evaluation: 34 synthetic scenarios, 75 fixed criteria; baseline 74 pass/1 fail, candidate 75 pass/0 fail. The repaired case named `ci-image` and the gateway pin owner as possible leads, then required current-source inspection. It measures proposed decisions only; no scenario tool effect, broad model-compliance or runtime behavior is established. See [decision-evaluation.json](./decision-evaluation.json).

The corrected measurement includes inherited workflow owners and was independently verified, including every source hash, count and inherited/incremental sum. Both versions include the full applicable `/alaa-workflow` closure: `SKILL.md` plus `references/artifact-lifecycle.md`, `companion-routing.md`, `context-continuity.md`, `context-curation.md`, `task-tracking.md` and `workspace-and-integration.md`; conditional exclusions and starting-state assumptions are recorded in the JSON audit. Full lesson totals are 12,736 to 11,388 words (-10.6%); admitted-lesson totals 14,642 to 13,116 (-10.4%). Routine recall is 3,399 to 2,216 (-34.8%); setup is 3,399 to 3,506 (+3.1%). The memory body remains 1,654 words; the lesson body falls from 1,048 to 873 (-16.7%), bringing combined bodies from 2,702 to 2,527 (-6.5%). The complete target tree grew from 19,320 to 19,492 words. Tokenizer unavailable; these are declared source-word counts, not runtime-context or cost results. The earlier incomplete capture is superseded. See [loading-measurements.json](./loading-measurements.json), [measurement-fix-evidence.json](./measurement-fix-evidence.json) and [final correctness review](./review-correctness-final.md).

Final correctness/evidence review approved with no findings remaining. Earlier correctness findings for partial-scan/read failures and malformed checker inputs were closed with focused checks. Instruction review requested a checker-coverage correction; fix cycle 1 was approved. Security review passed the bounded source change. See [initial correctness review](./review-initial.md), [final correctness review](./review-correctness-final.md) and [instruction/security review](./review-instruction-security.md).

First independent native batch, run from the repository root:

- `python scripts/validate_sohrab_skill_pack.py` — exit 1: missing `alaa-extract-agent-lessons/references/context-curation.md`; the independent rerun was pending when round 1 stopped and passed in round 2.
- `python scripts/check_skill_index.py` — exit 0.
- `python scripts/check_fleet_references.py` — exit 0.
- `python scripts/check_lifecycle_contract.py` — exit 0.
- `python scripts/check_capability_recall.py` — exit 0; static coverage only.
- `python scripts/check_capability_recall.py --self-test` — exit 0; 27 negative fixtures rejected.
- `python skills/sohrab/alaa-memory-os/test/test-hook-safety.py` — exit 0; hook safety checks passed.

The batch stopped after command seven. Its skill-index, fleet-reference, lifecycle-contract, capability-scenario and hook checks passed; the skill-pack validator failed on the missing path above. The independent correction and resumed batch passed the validator and fleet check; hook self-test, 11 checker-input process regressions, the five-script PowerShell suite, both agent-contract checks, diff check, 39/39 checksum readback and Markdown links for 23 source files also passed. Two infrastructure failures were preserved: the checksum comparator initially mishandled `./` paths, and link-check arguments were joined into one literal-newline path. Each cause was corrected once and its rerun passed. Exact commands, outputs and snapshots are in [verification-round1.json](./verification/verification-round1.json) and [verification-round2.json](./verification/verification-round2.json).

Official sources were refreshed 2026-10-12 America/Los_Angeles. Claude hook documentation was accessed 2026-10-12 America/Los_Angeles (UTC date 2026-10-13). URLs and findings are in [sources.md](./sources.md) and [hooks-evidence.md](./hooks-evidence.md).

## Limits
No hooks were installed or activated; no live Hindsight store, memory write, actual scenario tool operation, Claude runtime, serving identity or runtime compliance was verified. IMPLEMENTED and MERGE_CANDIDATE evidence is recorded under the [canonical workflow lifecycle contract](../../skills/sohrab/alaa-workflow/references/workspace-and-integration.md); release and publication remain out of scope. Current documentation-check and curation disposition is recorded in the [canonical plan](./20261012-220000_capability-recall.md) and [final verification record](./verification/documentation-final.json).
