# Failure Visibility at the Edge

A Lua handler that fails badly does not raise an exception anyone sees. It produces a plausible value, the configuration accepts it, and the request continues to the backend. This file states what each failure shape actually renders and which one you must use.

**Scope: converters and sample fetches.** They are the only handler types whose return value HAProxy reads back and turns into a sample, so they are the only ones every rule below applies to. Actions can return `act.*` control codes and services emit responses; their failure contracts are stated in `references/25-actions-services-and-subrequests.md`. Applying these linked rules to an action produces a rule that cannot be satisfied, and applying the action contract to a converter leaves the converter failing open.

## Focused references

When interpreting a return value or changing conversion mode, read [sample conversion, historical rendering and directional boolean semantics](./30-failure-visibility/10-samples-and-modes.md).

Before deciding a converter or fetch failure policy, read [explicit rejection and owner-approved advisory sentinel contracts](./30-failure-visibility/20-rejection-and-advisory-contracts.md).

When raising or catching a Lua error, read [source-position exposure, logs and protected-call failure semantics](./30-failure-visibility/30-errors-and-protected-calls.md).

When assigning decision variables or handling startup/timeouts, read [variable persistence, explicit reset and failures outside the handler](./30-failure-visibility/40-variable-state-and-external-failures.md).
