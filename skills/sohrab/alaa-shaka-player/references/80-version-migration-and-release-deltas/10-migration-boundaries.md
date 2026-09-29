For the v5.2.3 API/migration baseline and 2026-07-28 read date, consult [provenance and freshness](../05-provenance-and-freshness.md); source context stays canonical there.

## Which migrations are real

Shaka has followed semantic versioning since v3.0: *"Upgrading from any v3 release to a newer v3
release should be backward compatible. The same is true of all major version numbers."*

| Transition | Real migration? |
|---|---|
| `5.0.x → 5.1.x`, `5.1.x → 5.2.x` | **No.** Minor bumps, backward compatible by policy. `upgrade.md` has no `## v5.2` section because no breaking change was made. |
| **`v4.16 LTS → v5.x`** | **Yes.** A large `## v5.0` section exists. This is §"v4 → v5" below. v4.16 is LTS until **2027-01-31**. |
| **`v5.x → v6.0`** | **Yes, and already announced.** Deprecated in v5.1, removed in v6.0. Write the v6 spelling today. |
