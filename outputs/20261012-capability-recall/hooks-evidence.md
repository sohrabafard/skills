# T3 focused implementation evidence

Status: semantic code and exact emitted-string rewrite accepted by parent; fix-cycle-1 implemented and focused checks passed. Manifest and source packets captured; independent gates and possible final documentation/hash refresh pending.

Official source: [Claude Code hooks reference](https://code.claude.com/docs/en/hooks), accessed 2026-10-12 America/Los_Angeles (UTC date 2026-10-13). Current documentation specifies SessionStart context output without blocking control and discards PreCompact systemMessage/continue fields. Compatibility JSON is emitted locally; no delivered PreCompact reminder is claimed. No hooks were installed or activated.

Invariants: PreCompact reads no input/transcript/vault/git/environment and writes nothing. SessionStart observes repository drift only, reports positive/zero/unavailable separately and never prints supplied paths/content. Workflow owns active continuity. Helper root selection never falls back from an invalid selected destination. Wrapper argv is never printed; underlying third-party output is still raw.

Design: keep a nonwriting legacy hook instead of transcript capture/redaction or removal; retain drift observation with unknown on incomplete reads. Redaction does not make raw capture admissible; removal breaks legacy call sites. Parameter names and hook exit0/JSON shape remain compatible. Removing the implicit machine-specific vault default is intentional; a caller must provide a destination.

All commands ran from the repository root, ordinary bounded single-process commands; no CPU-heavy suite, paid API, network store, installation or external write.

| Command | Observed result |
|---|---|
| `python skills/sohrab/alaa-memory-os/test/test-hook-safety.py` | Exit 0; 16 subprocess checks: five PreCompact payload/vault cases, four drift cases, six destination precedence cases, one argv secrecy case. Fixture tree unchanged; command write traps not called; synthetic canary absent. |
| `python skills/sohrab/alaa-memory-os/test/test-hook-safety.py --self-test` | Exit 0; continue-field, secret-echo and write-command mutations rejected. |
| `python scripts/check_capability_recall.py` | Exit 0; 34 separated scenarios, R1-R8 coverage, source reachability/nonwriting checks. Static proof only. |
| `python scripts/check_capability_recall.py --self-test` | First run exit 1: wrapped named cross-skill references were falsely classified as local. One owner-aware repair; exit 0. Later direct-read fixture added; pre-review observed exit 0 with 24 red fixtures. Fix-cycle-1 final observed exit 0 with 27 red fixtures, including actual child CLI exit2/no-traceback proof for null input/oracle rows. |
| `python outputs/20261012-capability-recall/prepare_probes.py --version before` | Exit 0; frozen baseline packet generated, no model invoked. |
| `python outputs/20261012-capability-recall/measure_loading.py` | Exit 0; initial provisional capture and later final-wording/fix-cycle-1 capture of before/after bodies, tree and six enumerated owner loading paths. Tokens unavailable; no runtime-context or monetary claim. |
| `git diff --check -- skills/sohrab/alaa-memory-os/scripts scripts/check_capability_recall.py` | Exit 0. |

Artifacts: scenario-inputs.json excludes oracle fields; scenario-oracle.json is reviewer-only. before-probe.json contains source-pinned synthetic evaluation input. hook-semantic-draft.json preserves source plus immutable design decisions; hook-rule-writer-items.json isolates five controlling output strings for parent wording review. No source checker is called model evaluation.

Initial audit gaps included permissive staleness/link reads; independent review reproduced partial-scan false-clean and unreadable-note wrong-exit defects. The parent admitted these into fix-cycle-1. Enumeration/read failures now exit2 with a scoped blocked reason; nonempty null content is unavailable, while readable zero-byte files remain readable. SessionStart also accepts readable empty drift files. The static hook guard now catches ReadAllLines. No unrelated store behavior was changed.

Fix-cycle-1 focused evidence: `python skills/sohrab/alaa-memory-os/test/test-checker-input-failures.py` first exited1 because PowerShell EncodedCommand collapsed a checker exit2 into shell exit1; the harness now explicitly exits LASTEXITCODE. One cause-specific repair and retry produced exit0 across 11 child-process cases, including partial scans, read errors, null nonempty content, empty notes, clean inputs and retained hygiene findings. Hook safety reran exit0 after the SessionStart repair. Scoped diff check exited0. Fixture tree remained unchanged.

Manifest regeneration was explicitly approved because no declared generator was found. The exact existing GNU format was reproduced over 39 memory-skill files, excluding SHA256SUMS and caches, followed by exact readback and recomputation of every digest. `manifest-regeneration.json` records the observed result. `after-probe.json` now contains the same 34 evaluation inputs with current target sources; no model was invoked. A final documentation correction may require refreshing hashes and captures.

Remaining audit-only limit: other store wrappers still invoke Basic Memory and forward unsanitized third-party output. Independent verifier owns test/run-tests.ps1 affected breadth and whole-pack checks. Native model probes, independent grading, installed hook/Claude execution and live Hindsight proof did not run in this lane.
