
# Ingestion, batching, and parts

## Core rule
Small frequent synchronous inserts create too many parts and merge pressure.

## Preferred order
1. Large client-side batches
2. Async inserts when client-side batching is impractical
3. Queue-based fan-in when producer coordination is hard

## What to ask
- rows per insert?
- insert queries per second?
- concurrent writers?
- retry behavior?
- replicated or not?
- dedup expectations?

## Symptoms of trouble
- "too many parts"
- rising part counts
- slow merges / merge backlog
- ingest latency spikes
- degraded query performance after write surges

## Default recommendations
- batch more aggressively if the client can do it
- if many agents send small payloads, evaluate `async_insert`
- keep partitions coarse enough that merges can keep up
- make retries idempotent and batch boundaries stable when possible
