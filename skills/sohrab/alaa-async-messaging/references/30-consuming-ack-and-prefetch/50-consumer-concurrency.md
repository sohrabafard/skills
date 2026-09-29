# Consumer concurrency

## Consumer concurrency

**A consumer sets an explicit concurrency bound, and its database pool maximum is set for the worker
process rather than inherited from the HTTP default.** Concurrency times per-handler connections is the
consumer's real footprint on the database, and a consumer fleet that inherits the HTTP pool default
silently doubles the fleet's connection count during exactly the backlog it was scaled up to drain.

**Scale a lane by adding consumers, not by widening one consumer's prefetch.** More consumers spread the
unacknowledged window across processes, so a single crash loses a fraction of it rather than all of it.
