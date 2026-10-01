# Clean Code and Design Patterns

The constraints here are not general Lua style. They come from three properties of the environment: the module is loaded once and called on every request, HAProxy injects API globals such as `core` and `act`, and a stall is charged to other people's traffic.

Copy `examples/haproxy-lua/token-guard.lua` when starting a module. It is the shape this file describes, and it passes the checker with zero findings.

## Focused references

When creating or naming a module, read [the returned-table pattern, registration and file naming](./60-clean-code-and-patterns/10-module-shape.md).

When organizing repeated computation, read [localized globals, closures, precomputation and metatables](./60-clean-code-and-patterns/20-computation-patterns.md).

When separating pure logic from request state, read [handler boundaries, state lifetime and load-time testability](./60-clean-code-and-patterns/30-state-and-testability.md).
