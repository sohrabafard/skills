For the v5.2.3 API/migration baseline and 2026-07-28 read date, consult [provenance and freshness](../05-provenance-and-freshness.md); source context stays canonical there.

## Delivery diagnostics

`createQoeSink` in `assets/templates/playbackQoe.ts` exposes a local `status()` snapshot: pending depth,
in-flight state, capacity-eviction count and send-failure count. Counters saturate at the safe integer
limit. An optional issue observer receives only these quantities; synchronous throws and rejected
observer promises cannot alter the queue. No raw error, URL, grant, record or account identifier enters
this seam. Consumers map these quantities to registered names through `/alaa-services-contract` and
existing `/alaa-observability-soc` budgets; this API defines no fleet metric or alert threshold.

Capacity eviction remains intentional loss, and a resolved send is only the transport's acknowledgement.
A rejected send retains entries still inside the cap. Query status even when the observer fails. This
in-memory sink is not durable delivery proof. Disposal must capture the pending session before listener
removal, exactly once with the unloading path; `11-vue-quasar-binding.md` owns that implementation.
