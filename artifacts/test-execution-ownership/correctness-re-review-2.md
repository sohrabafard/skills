# Correctness re-review after the combined repair

- Reviewer: /root/correctness_review; requested gpt-6.1-sol / medium; observed unknown.
- Verdict: CHANGES-REQUESTED.
- Source: read-only reviewer return, persisted by the parent; initial review is preserved separately.
- HEAD: 183f5c5a19daaa0c31c5aa41ce8ce2868181aa34.
- Reviewed shared checker SHA-256: e28f2cd70119ebf31b33d0d10ae1adf8e9c60ccc486ea5e77595f0b975ccac67.

Resolved: all 16 original collection consumer inputs are covered. The first-failure contradiction and short-rule duplicate examples are rejected.

Remaining minor finding at shared checker line 242: the new explicit duplicate catalog omits previously protected complete clauses. Appending `Record each command's machine-readable reporter when available and retain its output` to `codex_resources` returns no finding, although the previous length-based guard rejected that 84-character instruction. Preserve every previously protected complete instruction, including the selected/executed-count rule, and add an independent inventory fixture that fails when a protected entry is removed.

The reviewer inspected source and ran three focused in-memory mutations plus an original-consumer inventory comparison. No suites or source writes. Native Windows, installed activation, live-agent behavior and pending final gates are outside this review.
