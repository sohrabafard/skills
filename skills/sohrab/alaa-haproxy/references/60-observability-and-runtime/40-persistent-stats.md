# Persistent statistics across reloads

## Persistent stats across reloads

Introduced experimentally in 3.3; graduated in 3.4. Use `shm-stats-file <path>`
in `global` and unique GUIDs on the objects whose shareable counters must survive
reload. Gate it with `expose-experimental-directives` only on 3.3; 3.4.6 does not
require that gate. `15-persistent-stats-3.3.cfg` is branch-aware. The source/manual
and historical parser receipt are distinguished in `SOURCES.md`.

- The path must be **writable**. Under `readOnlyRootFilesystem: true` that means an explicit
  writable mount at that path.
- Counters survive a **reload**. They do not survive a **restart**, and they do not survive the
  shared-memory file being removed. A dashboard built on the assumption of continuity still shows
  a discontinuity after a node restart, and that discontinuity is indistinguishable from a traffic
  drop unless the panel is annotated.
- A `guid` is a durable series identifier. Changing one renames the series and breaks history
  exactly as if the counter had reset; treat a guid change as a dashboard migration. A duplicate
  guid is a startup error.

Whether the continuity is required at all is decided by `/alaa-observability-soc`.
