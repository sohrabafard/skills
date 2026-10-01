# Execution Model

Most HAProxy Lua defects are execution-model defects wearing a logic-defect costume. Read this file before writing the first line of a module.

## Focused references

When establishing binary and interpreter compatibility, read [build prerequisites, Lua versions and the selected compatibility target](./10-execution-model/10-build-and-interpreter.md).

When choosing a load directive or sharing module state, read [shared/per-thread state, lock interleaving and once-only initialization](./10-execution-model/20-state-and-initialization.md).

Before registering or calling a context-specific API, read [the execution contexts and initialization/runtime boundaries](./10-execution-model/30-execution-contexts.md).

When bounding execution or diagnosing a stall, read [yielding, blocking I/O, execution timeouts and memory budgets](./10-execution-model/40-scheduling-and-budgets.md).
