# Verification Failure Taxonomy

Use one primary classification per command and record secondary factors separately.

## PASS

The exact dispatched command completed successfully, evidence was captured, and no unexpected tracked changes occurred.

## PRODUCT-FAILURE

The implemented repository behavior violates a test, lint rule, type/build contract, smoke scenario, or acceptance criterion. Route to the owning implementation lane.

## TEST-INFRA-FAILURE

The test harness, fixture, runner, generated setup, service dependency, or test environment is broken independently of the intended product behavior. Create an explicit infrastructure lane when a repository change is needed.

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

## Diagnostic sequence

1. Identify the first causal error, not the last stack trace.
2. Confirm command/cwd/environment/resource limits.
3. Compare initial/final git status and concurrent changes.
4. Determine whether the failure reproduces in the smallest targeted scope, if one authorized rerun exists.
5. Inspect the owning code/test/config path.
6. Classify owner: implementation lane, test infrastructure lane, environment owner, or orchestrator decision.
7. Route the smallest grounded next action.
