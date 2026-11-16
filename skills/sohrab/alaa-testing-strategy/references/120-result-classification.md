# Result Classification

Use one primary classification per command and record secondary factors separately. This vocabulary allocates no repair authority.

## PASS

The exact recorded command completed successfully, evidence was captured, and no unexpected tracked change occurred. Selection decides these cases:

- A test or benchmark command, including whole-suite discovery and each covered child of an aggregate, whose selection is empty or differs from the expected cases recorded for it is `TEST-INFRA-FAILURE`, never `PASS`; inside a container run, an incomplete copy or mount is instead `ENVIRONMENT-BLOCKED` under `110-execution-resources.md`.
- A test or benchmark command that selected cases but executed none takes the class its skip reasons name (`SKIPPED`, `ENVIRONMENT-BLOCKED`, or the failed setup's class), never `PASS`.
- A scoped lint, type-check or build command whose scope matches no file is `TEST-INFRA-FAILURE`.
- A list or collect selection check executes no case by design: it is `PASS` when it lists exactly the expected cases.

## PRODUCT-FAILURE

The implemented repository behavior violates a test, lint rule, type or build contract, smoke scenario or acceptance criterion. Identify its behavior owner, and follow `100-test-execution.md` collection and batch repair before changing code.

## TEST-INFRA-FAILURE

The test harness, fixture, runner, generated setup, service dependency or test environment is broken independently of the intended product behavior. Identify the required infrastructure scope in the combined repair record under `100-test-execution.md`.

## ENVIRONMENT-BLOCKED

A required executable, service, permission, network dependency, secret, browser, database or platform capability is unavailable. Do not disguise this as a product failure, and do not install anything or change the environment without authority.

## TIMEOUT

The command exceeded its declared timeout. Preserve partial logs and process and resource evidence. Diagnose the cause before you assign repair: a product deadlock, a test deadlock, resource starvation or an unrealistic timeout. When the cause cannot be diagnosed, the timeout remains unresolved.

## FLAKY

Identical execution produces inconsistent outcomes, including fail-then-pass. Never promote it to PASS. Capture ordering, seed, timing, resource and environment evidence.

## CONTAMINATED

Unexpected tracked-source changes, concurrent external modifications, a wrong worktree, stale generated output, or an unowned service or state makes the result unreliable. Do not revert automatically.

## SKIPPED

The check was explicitly not run. Record the reason and the risk. Unexecuted checks are never implied passes.

## Host-environment sub-classes

A product command surfaces these failures, so they are misread as product defects. Record the sub-class beside its primary class.

| Observation | Primary class | Discriminator |
|---|---|---|
| The command line was parsed by a shell other than the intended one: quoting or word splitting that differs between `sh` and Bash, a variable expanded by the wrong shell, a here-document that did not close | `ENVIRONMENT-BLOCKED` | The same command parses under the intended shell; the product was never reached |
| A container runtime is not running, an image is absent, a mount failed, or the daemon refused the socket | `ENVIRONMENT-BLOCKED` | The failure precedes the start of the process under test |
| A file, directory, port, or device was refused, locked, or held open by another process | `ENVIRONMENT-BLOCKED` | The message names an OS-level permission, lock or address, not an assertion |
| A required executable, service, credential, browser, or platform capability is absent | `ENVIRONMENT-BLOCKED` | Absence, not misbehaviour |
| A build, dependency, module, or test cache served an artifact from before the change | `CONTAMINATED` | The outcome changes after the cache is cleared with no source edit |
| The harness, fixture, factory, seed, or generated setup broke independently of the behaviour under test | `TEST-INFRA-FAILURE` | Reverting the change under test leaves the failure in place |

Never repair the product in response to any row above: each cause lies outside product behavior.

Clearing a cache, installing a tool, changing a permission, or starting a service is a declared and reported action, never a silent retry step. A silent clear destroys the evidence of the cause.

## Diagnostic sequence

1. Identify the first causal error, not the last stack trace.
2. Confirm the command, working directory, environment and resource limits.
3. Compare the initial and final git status, and check for concurrent changes.
4. Reproduce the failure in the smallest targeted scope, if one authorized rerun exists.
5. Classify the owner as product, test infrastructure, environment, or unresolved ownership.

A `TEST-INFRA-FAILURE` or `ENVIRONMENT-BLOCKED` recurring with the same first causal error earns no further full run: its owner reproduces the smallest failing path within the active retry budget while safe independent checks continue.
