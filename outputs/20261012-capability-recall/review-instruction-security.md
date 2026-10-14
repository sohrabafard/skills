# Independent instruction and security review

Reviewed 2026-10-13 against baseline `daaa3694c744667975d187bcdb33eaae75d9e7fd`.

## Instruction review, initial final candidate

Reviewer: `/root/instruction_review`, alaa-instruction-reviewer, requested gpt-6.1-sol/medium; serving identity and read-only enforcement unknown. Native read-only inspection only.

Verdict: CHANGES-REQUESTED. One major finding: `references/checkers-and-hooks.md` claims `test/run-tests.ps1` runs every self-test, although it invokes only five PowerShell scripts. Correct coverage and add explicit commands for the new Python hook safety, checker input failure and root capability checks, including their self-tests. Independent verification remains required. T2 owns correction, fix cycle 1.

No other instruction-contract findings. Reviewer verified W1-W16 application records/current hashes and all 18 accepted draft snapshots. Final compression preserves accepted semantics. Setup relocation is separately admitted. Owners, shared recall deadlines, source verification, classifications, authorization, retry/native-status boundaries, terminal outcomes, secrets, lesson provenance/deduplication/freshness and workflow reopening remain intact. Codex/Claude consumer text is identical and pointers reachable. Final RFC/report extension remains pending.

## Security review

Reviewer: `/root/security`, alaa-security-reviewer, requested gpt-6.1-sol/medium; serving identity and read-only enforcement unknown.

Verdict: PASS for bounded source change. No confirmed vulnerability, material weakness or required security fix. Reviewed recalled text/transcripts as untrusted, repository truth and authorized stores as protected boundaries. Confirmed separate write authority, uncertain-write reconciliation, secret exclusions, scoped ingestion, no adapter fallback, nonwriting PreCompact, bounded SessionStart output and unavailable partial scans.

Independent commands all exit 0:

- `python scripts/check_capability_recall.py --self-test`: 27 negative fixtures rejected.
- `python skills/sohrab/alaa-memory-os/test/test-hook-safety.py`: no-write/canary, vault precedence and argv secrecy checks passed.
- `python skills/sohrab/alaa-memory-os/test/test-checker-input-failures.py`: 11 process regressions; fixture tree unchanged.

No external memory operation. Installed activation, live transport/store outcomes, agent compliance and runtime isolation remain unverified. This review does not substitute for final native verification or the complete documentation review.

## Instruction fix cycle 1

Verdict: APPROVED. W17 closes the sole major: all five PowerShell targets and five independent Python commands are named. Reviewer confirmed exit meanings, limited proof, nonzero blocking and independent verification remain intact; W17 equals its accepted semantic correction. Exact replacement and SHA match application evidence; surrounding text unchanged. The prior complete candidate review remains eligible. Final RFC/report extension is pending.

## Complete-change documentation extension

Verdict: APPROVED-WITH-NITS. No blocking instruction finding; RFC IMPLEMENTED status justified by source acceptance, independent verification and reviews. Complete source manifest verified; final citation wrap preserves tokens and ownership. Counts and74/75 to75/75 claims match evidence and retain limits. Two documentation nits assigned to documenter: label the RFC unlabelled original later-implementation paragraph as historical, and change report round1 rerun-pending wording to reflect its later passing round2. Final documentation checks and workflow finality remain separate gates.

## Final documentation closure

Verdict: APPROVED, no findings remain. Both nits closed; report factual alignment is accurate and routes final documentation/curation state to canonical evidence. Reviewer independently confirmed four-document manifest e776e06d84c2dbdd56a3a1cc477d3f0d64358c998564f79d03d79b27ebcc549f. Prior complete-change approval remains eligible. Refreshed native documentation checks and workflow validation are separate gates; live/installed/serving proof remains unclaimed.
