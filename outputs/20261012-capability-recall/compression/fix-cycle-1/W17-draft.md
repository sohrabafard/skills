`test/run-tests.ps1` runs `-SelfTest` only for its five declared PowerShell targets:
`alaa_obsidian_linkcheck.ps1`, `alaa_memory_staleness.ps1`, `alaa_memory_health.ps1`,
`alaa_memory_reindex.ps1`, and `alaa_memory_post_task.ps1`. It does not run the Python hook-safety,
checker-input-failure, or repository capability-contract checks below. A target exiting `2` is recorded
**BLOCKED, not FAIL**, and the harness exits `2`: an unavailable checker and a reported finding require
different actions and must not be collapsed.

Run these separate commands from the repository root:

```text
python skills/sohrab/alaa-memory-os/test/test-hook-safety.py
python skills/sohrab/alaa-memory-os/test/test-hook-safety.py --self-test
python skills/sohrab/alaa-memory-os/test/test-checker-input-failures.py
python scripts/check_capability_recall.py
python scripts/check_capability_recall.py --self-test
```

The hook-safety and checker-input-failure commands execute synthetic process/fixture regressions;
their results prove neither installed hook activation nor live store behavior. The capability checker
and its self-test inspect scoped source/scenario contracts and red fixtures; they execute no model or
memory operation and prove no runtime instruction compliance. These Python commands use `0` for covered
checks passing, `1` for findings/assertion failures, and `2` for unavailable execution or unreadable inputs.
Either nonzero blocks the affected claim; an unrun command is never a pass. Passing the PowerShell harness
covers none of these separate commands. Keep the independent consolidated verification gate; an
implementation lane's focused evidence does not discharge it. `/alaa-testing-strategy` owns test design
beyond this rule.

