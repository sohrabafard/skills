# Topic Map

Read only the files whose stated condition the task meets. Loading the whole tree means the task was not scoped.

| You are about to | Read |
|---|---|
| Write or review any individual test, or question an existing test's value | `10-what-makes-a-test.md` |
| Decide where a behaviour is tested, investigate a slow suite, or find the same behaviour tested more than once | `20-layers.md` |
| Substitute anything for a real dependency, meet an existing double, or see a suite pass while an integration breaks | `30-doubles.md` |
| Assign or review a proof level, report any claim as validated, or find an environment that cannot reach the level a claim needs | `40-proof-strength.md` |
| Handle a test that produced two different outcomes on the same code, or meet a proposed retry | `50-flake.md` |
| Measure, gate, or cite coverage, or decide what still needs a test | `60-coverage.md` |
| Start a change, before any test is written | `70-failure-mode-first.md` |
| Report a test result, review someone else's, handle a test that cannot run, or decide whether an earlier result may be cited instead of re-run | `80-evidence-and-reporting.md` |
| Decide whether a candidate is owed a test, give a test its selector, create or share setup, repair or delete an existing test on a touched topic, choose which commands a gate runs, or find a build, compile, render, or image produced more than once in a pass | `90-test-economy.md` |
| Choose or run validation commands, check selector and aggregate coverage, reuse results, or collect failures before batch repair and retest | `100-test-execution.md` |
| Run CPU-heavy checks, allocate test or dependency containers, use a low-priority runner, choose a CI-image host, or compare before/after timing | `110-execution-resources.md` |
| Interpret a command outcome, an empty or mismatched selection, selected-but-unexecuted cases, collect-only success, timeout or host obstruction, or classify before repair | `120-result-classification.md` |

## Owned by another skill

- `/alaa-reliability-sla` owns fault injection doctrine, the failure modes worth injecting at a dependency boundary, the per-mechanism evidence table, load testing at saturation, production experiments, and the rule that an untested degraded path is a broken path (`references/80-verification.md`). This skill owns where those tests sit in the plan, at which layer, and at which proof level.
- `/alaa-security-review` owns which controls must be security-tested and its own minimum negative tests for credentials and cryptography (`references/50-credentials-and-cryptography.md`). This skill generalises the method those tests are built on. It does not restate them. It names no security control.
- `/alaa-services-contract` owns every envelope, code, header, field name, and value a contract test asserts against. Assert what that skill declares and report drift, rather than asserting the drift.
- `/alaa-postman-collections` owns API-level request tests, their five minimum assertions, examples, and scripts. This skill owns the layer that work sits at and the rule that no request is exempt.
- `/alaa-observability-soc` owns the failure-mode enumeration table and the signal, query, and alert each mode needs (`references/10-signal-model.md`). This skill consumes the same enumeration to derive tests. Neither skill maintains a second list.
- `/alaa-controlled-ops` owns its own package and adopter release gates and its boundary-check script. This skill owns the proof-level vocabulary those gates report in.
- The per-language skills and the vendored `/golang-testing` own framework idiom, assertion syntax, fixture and mock libraries, table-driven form, and runner flags. This skill owns the decision. It names no framework construct.
- `/alaa-cc-orchestrator` and `/alaa-codex-orchestrator` own role authority, observer independence, allocation, and the scheduling of phases and reviews. `/alaa-workflow` owns durable execution state, write ownership and resume. Generic execution, resources, runners and classification remain in this skill.
- `/alaa-prompting-guide` owns model/effort capability evidence and runtime mechanics. The runtime orchestrator owns actual task allocation for every authority role. This skill names no model.
