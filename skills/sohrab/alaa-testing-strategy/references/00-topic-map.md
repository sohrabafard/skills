# Topic Map

Read only the files whose condition the task meets.

| You are about to | Read |
|---|---|
| Write or review a test, or question an existing test's value | `10-what-makes-a-test.md` |
| Decide where a behaviour is tested, investigate a slow suite, or find one behaviour tested more than once | `20-layers.md` |
| Substitute anything for a real dependency, meet an existing double, or see a suite pass while an integration breaks | `30-doubles.md` |
| Assign or review a proof level, report a claim as validated, or find that the environment cannot reach the level a claim needs | `40-proof-strength.md` |
| Handle a test that produced two outcomes on the same code, or meet a proposed retry | `50-flake.md` |
| Measure, gate or cite coverage, or decide what still needs a test | `60-coverage.md` |
| Start a change, before any test is written, or write its happy path | `70-failure-mode-first.md` |
| Report a test result, review someone else's, handle a test that cannot run, or decide whether to cite an earlier result instead of a re-run | `80-evidence-and-reporting.md` |
| Decide whether a candidate is owed a test, give a test its selector, create or share setup, write or review a test over shared infrastructure, repair or delete an existing test on a touched topic, choose which commands a gate runs, or find a build, compile, render or image produced twice in a pass | `90-test-economy.md` |
| Choose or run validation commands, check selector and aggregate coverage, reuse results, or collect failures before batch repair and retest | `100-test-execution.md` |
| Run CPU-heavy checks, allocate test or dependency containers, use the low-priority runner, choose a CI-image host, or compare before and after timing | `110-execution-resources.md` |
| Interpret a command outcome, an empty or mismatched selection, selected-but-unexecuted cases, a collect-only success, a timeout or a host obstruction, or classify before repair | `120-result-classification.md` |

## Owned by another skill

| Question | Owner | This skill keeps |
|---|---|---|
| Which fault to inject at a dependency boundary, the per-mechanism evidence table, load tests at saturation, production experiments | `/alaa-reliability-sla` `references/80-verification.md` | where those tests sit in the plan, their layer and their proof level |
| Which controls must be security-tested, and the minimum negative tests for credentials and cryptography | `/alaa-security-review` `references/50-credentials-and-cryptography.md` | the method behind those tests; it names no security control |
| An envelope, code, header, field name or value that a contract test asserts | `/alaa-services-contract` | assert what that skill declares, and report drift instead of asserting it |
| API-level request tests, their five minimum assertions, examples and scripts | `/alaa-postman-collections` | their layer, and the rule that no request is exempt |
| The failure-mode enumeration table, and the signal, query and alert of each mode | `/alaa-observability-soc` `references/10-signal-model.md` | the test of each mode, from the same enumeration |
