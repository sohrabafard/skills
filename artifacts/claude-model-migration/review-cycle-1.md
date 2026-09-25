# Independent correctness review - cycle 1

- Agent: claude_review, temporary alaa-reviewer-deep.
- Requested/configured: GPT-6 Astra/high; observed identity unknown.
- Verdict: CHANGES-REQUESTED.
- Scope: source candidate against HEAD `4fdd8b709a745314a0575c25c06d0a390847bde6`, including new policy/checker/corpus files.

## Findings returned

1. Major, confidence 0.98, `skills/sohrab/alaa-prompting-guide/scripts/check_claude_agent_evals.py:149`: calibration accepts records declaring a CLI below policy minimum. `validate_resolution` checks version-dependent precedence but not `availability.minimum_claude_code`. An in-memory completed nonsynthetic 32-run record with CLI `0.0.0` passed both results and reviewer calibration despite minimum `2.1.280`. Required correction: enforce canonical availability evidence and add boundary fixtures through results and calibration.
2. Minor, confidence 0.96, same file line 181: unreadable/malformed calibration JSON becomes ordinary findings instead of `CannotRun`, yielding exit 1 rather than promised unavailable-proof exit 2. Both fail closed. Required correction: preserve exception classification and add malformed/unreadable fixtures.

Both findings were sent unchanged in substance to the original policy implementation lane for fix cycle 1. No finding is accepted as a permanent exception.

## Independent re-review

Final verdict: APPROVED. No remaining findings. The same independent reviewer inspected the amended schema and implementation and reproduced these results: CLI `0.0.0` rejects all 32 rows through results/calibration; `2.1.282` passes; Fable rejects `2.1.256` and accepts `2.1.257`; policy rejects profile minima below model minima and unknown keys; SemVer prerelease/build comparisons pass; malformed linked evidence exits 2. The reviewer changed no files and performed no live evaluation. Both findings are resolved within fix cycle 1. Focused implementation records: `policy/fix-cycle-1/focused-checks.json`.

## Evidence and limits

Reviewer independently observed 23 projections with zero findings, preserved bodies/non-pin metadata for all 23 agents, and no Codex policy/orchestrator source changes. Specific in-memory probe reproduced the major defect without source writes or model calls. Broad verification belongs to the verifier. Live activation, serving identity, Desktop grants, plugin packaging and full system-card conclusions were not established. Source symlinks expose repository changes through installed skill paths.
