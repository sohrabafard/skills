# Cross-service migration
Architect + API/data specialist define invariants, old/new compatibility and rollout
order. Scout enumerates consumers; lead records owners and dependency edges.
Migration engineer makes an expand step, a backfill/transition step and a contract
step when appropriate. Test against mixed old/new versions, interrupted work and
retries. Integrator alone owns shared schema/client regeneration and lockfiles.
Reconcile data before cutover. Recovery can be a forward repair when rollback is
unsafe; name this explicitly. Production execution needs actual authorization.
