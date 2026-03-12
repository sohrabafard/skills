
# Vector agent prompt

Use this skill to solve a Vector task end-to-end.

## Mission
Design or troubleshoot a Vector topology that is:
- explicit about durability and loss semantics
- validated and unit-tested
- observable via internal logs and metrics
- safe under backpressure
- clear about sink behavior, especially for ClickHouse

## Hard constraints
- Do not treat buffering/ack choices as defaults without explaining the tradeoff.
- Do not skip `vector validate` / `vector test` in the recommended workflow.
- Do not mix experimental sinks into production fanout casually.
- Do not use VRL snippets without handling fallible operations intentionally.
- Do not recommend disk buffers without `data_dir`, capacity, and observability notes.

## Required output sections
1. Topology and failure domains
2. Config fragments
3. VRL notes and tests
4. Buffer / ack rationale
5. Validation commands
6. Monitoring plan
7. Rollout and fallback
