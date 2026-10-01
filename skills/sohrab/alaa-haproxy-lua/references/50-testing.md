# Testing

An HAProxy Lua module is ordinary Lua with one global injected. That single fact makes it unit-testable outside HAProxy, and it is the highest-leverage technique in this skill: it turns "deploy and watch the logs" into a test that runs in milliseconds.

What makes a test a test, which layer a behaviour belongs at, and how strong a given proof is, are owned by `/alaa-testing-strategy`. This file states only what is specific to HAProxy Lua.

## Focused references

When building the unit-test environment, read [mock core, module loading and interpreter selection](./50-testing/10-unit-harness.md).

When specifying validation cases, read [table-driven rejected inputs and failure assertions](./50-testing/20-rejection-tests.md).

When validating identifier generation, read [cross-process collisions, event ordering and non-vacuous properties](./50-testing/30-identity-properties.md).

When selecting a proof level or reporting results, read [native parsing, HTTP runtime evidence and limits](./50-testing/40-integration-and-proof-levels.md).

When running the reproducible package gates, read [exact commands, runtime prerequisites, exit meanings and checker limits](./50-testing/50-target-gate.md).
