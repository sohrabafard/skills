
# VRL guide

## Principles
- keep programs short
- give transforms clear names
- normalize and enrich in steps
- handle fallible parsing explicitly
- write unit tests for non-trivial logic

## Typical tasks
- parse JSON
- coerce types
- normalize timestamps
- set log levels/services/env
- redact secrets
- derive routing keys
- shape events for a specific sink

## Workflow
1. experiment with `vector vrl`
2. move the snippet into a `remap` transform
3. add `vector test` coverage
4. keep tests near the config or in a paired test file

## 0.53+ notes for metric-oriented VRL
- Prefer the dedicated metric helper functions when reading internal metrics in VRL:
  - `get_vector_metric`
  - `find_vector_metrics`
  - `aggregate_vector_metrics`
- Keep metric sampling windows explicit and predictable in tests.
- Do not assume old internal metric names in VRL programs during upgrades.

## Common sharp edges
- field names with hyphens need quoted access
- failed coercions must be handled
- do not leave fallible root expressions unhandled
