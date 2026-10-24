# Verification Failure Taxonomy

Use one primary classification per command and record secondary factors separately.

## PASS

The exact dispatched command completed successfully, evidence was captured, and no unexpected tracked changes occurred. A command whose selector selected zero cases is `TEST-INFRA-FAILURE`, never `PASS`. A command that selected cases but executed none takes the class its skip reasons name — `SKIPPED`, `ENVIRONMENT-BLOCKED`, or the failed setup's class — never `PASS`.

## PRODUCT-FAILURE

The implemented repository behavior violates a test, lint rule, type/build contract, smoke scenario, or acceptance criterion. Identify its behavior owner; repair scheduling follows `verification-and-gates.md` Gate economics.

## TEST-INFRA-FAILURE

The test harness, fixture, runner, generated setup, service dependency, or test environment is broken independently of the intended product behavior. Identify required infrastructure scope in the combined repair assignment under `verification-and-gates.md` Gate economics.

## ENVIRONMENT-BLOCKED

A required executable, service, permission, network dependency, secret, browser, database, or platform capability is unavailable. Do not disguise this as a product failure or install/change the environment without authority.

## TIMEOUT

The command exceeded its declared timeout. Preserve partial logs and process/resource evidence. A timeout may indicate product deadlock, test deadlock, resource starvation, or an unrealistic timeout; use the failure analyst.

## FLAKY

Identical execution produces inconsistent outcomes, including fail-then-pass. Never promote it to PASS. Capture ordering, seed, timing, resource, and environment evidence.

## CONTAMINATED

Unexpected tracked-source changes, concurrent external modifications, wrong worktree, stale generated output, or unowned service/state makes the result unreliable. Do not revert automatically.

## SKIPPED

The check was explicitly not run. Record the reason and risk. Unexecuted checks are never implied passes.

## Host-environment sub-classes

These are the failures most often misread as product defects, because the command that surfaced them is a product command. Each resolves to one primary class above; record the sub-class beside it so the same block is recognised on sight the second time.

| Observation | Primary class | Discriminator |
|---|---|---|
| The command line was parsed by a shell other than the intended one — PowerShell quoting, `$VAR` versus `%VAR%`, backtick versus backslash escaping, a Git Bash path rewritten to a Windows path, a here-string that did not close | `ENVIRONMENT-BLOCKED` | The same command parses under the intended shell; the product was never reached |
| A container runtime is not running, an image is absent, a mount failed, or the daemon refused the socket | `ENVIRONMENT-BLOCKED` | The failure precedes the process under test starting |
| A file, directory, port, or device was refused, locked, or held open by another process | `ENVIRONMENT-BLOCKED` | The message names an OS-level permission, lock, or address rather than an assertion |
| A required executable, service, credential, browser, or platform capability is absent | `ENVIRONMENT-BLOCKED` | Absence, not misbehaviour |
| A build, dependency, module, or test cache served an artifact from before the change | `CONTAMINATED` | The outcome changes after the cache is cleared with no source edit |
| The harness, fixture, factory, seed, or generated setup broke independently of the behaviour under test | `TEST-INFRA-FAILURE` | Reverting the change under test leaves the failure in place |

Never repair the product in response to any row above: each names an owner outside the implementation lane, and a product edit made against one of them is a change with no defect behind it.

Clearing a cache, installing a tool, changing a permission, or starting a service is a declared and reported action, never a silent retry step. A silent clear destroys the only evidence that the cache was the cause, and the same block then returns unrecognised on the next run.

## Diagnostic sequence

1. Identify the first causal error, not the last stack trace.
2. Confirm command/cwd/environment/resource limits.
3. Compare initial/final git status and concurrent changes.
4. Determine whether the failure reproduces in the smallest targeted scope, if one authorized rerun exists.
5. Inspect the owning code/test/config path.
6. Classify owner: implementation lane, test infrastructure lane, environment owner, or orchestrator decision.
7. Route the smallest grounded next action.

A `TEST-INFRA-FAILURE` or `ENVIRONMENT-BLOCKED` recurring with the same first causal error earns no further full run: its owner reproduces the smallest failing path within the active retry budget while safe independent checks continue, because a full rerun repeats the cost and returns the same evidence.
