## What every storage change must exercise

| Scenario | Level |
|---|---|
| fresh install at the current version | 2 |
| upgrade from the previous version, and from the oldest supported version | 2 |
| a second connection blocks the upgrade and the blocked path is taken | 2 branch, 4 real event |
| the old connection receives `versionchange` and closes | 4 |
| the database is unavailable and the fallback store is used | 2 |
| `QuotaExceededError` on an optional cache write, and cleanup frees room | 2 classify, 4 real error |
| `QuotaExceededError` on a draft save, and the user is told | 2 and 4 |
| storage cleared between sessions, and boot recovery runs | 2 state machine, 5 real eviction |
| an offline write flushes when the network returns | 2 and 4 |
| a 401 pauses without burning attempts; a 403 abandons | 2 |
| a row orphaned in `sending` is reaped on the next boot | 2 |
| logout purge removes every record for the previous account, verified by a ranged count | 2, and 4 for atomicity under an interrupted run |
| an older-schema record and a malformed record are rejected on read | 2 |
| private or ephemeral storage degrades to tier 0 | 4 private lane, 5 real device |
| a route's read stays inside its stated bound at a realistic record count | 4 with a seeded store |
