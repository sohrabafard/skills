# Stick-table capacity and saturation

## Sizing a stick table, and what happens when it is full

`stick-table type ip size <N> expire <T> store <counters>`.

- `size` is a **count of entries**, not bytes. Size it for the peak number of **distinct keys**
  that can be live within `expire`, which is unrelated to the peak request rate.
- Each entry costs roughly the key size plus the stored counters; the practical planning number is
  tens of bytes to a few hundred bytes per entry, so a `500k` IP table with three counters is on
  the order of tens of megabytes of resident memory. Measure it with `show table` under load
  rather than trusting an estimate.
- **At saturation HAProxy flushes older entries unless `nopurge` is set.** That is the attacker who has
  just gone quiet for a moment. An undersized purging table therefore
  quietly forgets the thing it was tracking, and the abuser returns to a clean counter.
- `expire` must be comfortably longer than the measurement window in the counters. `expire 30m`
  with `http_req_rate(10s)` keeps a penalty counter alive for thirty minutes, which is deliberate
  for a penalty and wrong for a rate.

`show table <name>` on the Runtime API dumps entries and is how you confirm the key is what you
think it is. Run it once against real traffic before trusting any limiter.
