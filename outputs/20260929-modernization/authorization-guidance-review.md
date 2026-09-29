# Authorization guidance design review

Verdict: SOUND-WITH-CONDITIONS. Reviewer: alaa-architecture-critic, configured gpt-6-astra/high; observed identity unknown. Read-only work observed; effective isolation unknown. Checked 2026-09-29.

Design status: not-required for the proposed clarification. The consistency trigger was considered, but all six system-design conditions remain unchanged: no interface, ownership, consistency/cache behavior, dependency, deployable or failure-response change is proposed.

Permitted scope: one source-backed explanation beside the existing Check example in the services-contract authorization reference. Preserve projector-only tuple writes, sidecar read-only behavior, request JSON, store/model pins, status codes, TTL values, fail-closed behavior and the existing cache restriction.

Official source: https://openfga.dev/docs/interacting/consistency

- MINIMIZE_LATENCY is the documented default and permits cache results only when OpenFGA caching is enabled. Upstream says server caching is disabled by default; neither fact establishes consumer settings.
- HIGHER_CONSISTENCY bypasses OpenFGA caches for that query. It does not advance an unprojected event or bypass/invalidate a sidecar decision cache.
- This capability description does not authorize activating OpenFGA caches or weakening the fleet restriction in the existing failure/load contract.
- Before claiming revoke visibility, inspect projection completion/lag, sidecar and server cache settings, deployed server/SDK semantics and the agreed end-to-end budget. Missing evidence remains unknown.
- Add no numeric budget, request field, new algorithm or blanket consistency mandate. Changing actual policy later requires consumer-owner decisions and measured load/latency consequences.

No product question blocks this documentation-only scope. Runtime revocation behavior was not tested. Independent security/instruction review must inspect the final wording and unchanged examples.
