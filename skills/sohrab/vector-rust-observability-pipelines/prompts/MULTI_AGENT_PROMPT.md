
# Vector multi-agent prompt

Spawn specialist agents in parallel, then consolidate:

1. Topology agent
   - design source/transform/sink contracts and failure domains
2. VRL agent
   - implement and unit-test transformations
3. Delivery agent
   - choose buffers, acknowledgements, retries, and healthcheck policy
4. Sink agent
   - tune the main destination sink, especially ClickHouse
5. Ops agent
   - internal metrics/logs, capacity, startup policy, and incident runbook
6. Community-risk agent
   - scan current docs/issues/community threads for sharp edges

Return:
- final topology
- final config
- tests
- validation commands
- monitoring / incident notes
