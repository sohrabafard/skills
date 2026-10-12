# Independent correctness review

Initial verdict: CHANGES-REQUESTED. Observer `/root/correctness_gate`, `alaa-reviewer`; configured controls neutral, requested `gpt-6.1-sol/high`, observed identity unknown. Read-only inspection and two in-memory probes; no file writes. Parent managed permissions and unknown MCP isolation were reported.

1. Major, allocation checker line 135: the R15 pressure case accepted a supported ultra effort despite the input's explicit human medium selection. Changing only that effort in synthetic R15 pressure rows made `validate_results` return no findings. Required correction: encode/enforce the explicit requested pair and add an effort-only red fixture.
2. Minor, archive checker line 73: `source_commit` was syntax-checked while the success message claimed provenance validation. Forty zeros passed the in-memory manifest substitution. Archived corpus/policy bytes independently matched baseline HEAD exactly. Required correction: either bind trusted snapshot identity or accurately limit the claim to hashes and provenance-field syntax. Parent selected the latter, preserving distributed use without requiring Git; reference 92 and checker messages must align.

Reviewed evidence: actual scoped policy/control/checker diffs and R1-R15 corpus/oracle; ordinary historical-Sol rejection even with archived enabled flag; separated archive support path; original bytes compared with baseline HEAD; sixteen source commands and three R13 followups all exit zero; recomputed 541-file pin unchanged. This demonstrates why passing fixtures alone did not discharge independent review.

Parent authorized one coordinated fix cycle through the original checker and prose owners. Runtime capture remains held until the corrected candidate clears review and invalidated source gates. The reviewer never writes its fixes.

Limitations: static phrase checks do not establish arbitrary semantic equivalence. Record structure does not establish truthful execution or grading. Actual allocation, child realization, installed activation, worker quality, comparative cost and savings were unrun at this verdict.

## Corrected candidate

Final source verdict: APPROVED, no remaining findings. The same reviewer repeated the exact effort-only repro: Codex ultra and Claude high reject when the human requested medium; correct medium and ordinary R1 supported-high choices still pass. Ordinary current/archive policy paths still reject old Sol. Archive output and reference 92 now state the proof limit accurately.

Independent followup: allocation self-test, archive self-test, history validation and diff check all exit zero; refreshed 541-file pin has no drift. Final source identities are in `verification/review-fix/source-pin-refreshed.json`. This approval covers source correctness and regression fixes; runtime observations and compression remain separate gates.
