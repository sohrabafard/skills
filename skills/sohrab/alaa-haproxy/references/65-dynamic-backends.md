# Dynamic backend operations

Use for backend creation/deletion through the 3.4 Runtime API. Source: the
[3.4 management manual](https://docs.haproxy.org/3.4/management.html), inspected
alongside `v3.4.6` release-source `doc/management.txt` on 2026-10-01.

## Prepare and publish

Retain a named TCP/HTTP `defaults` template: `tune.defaults.purge` frees retained
defaults and prevents using them later. New backends inherit that template; this
does not provide arbitrary runtime editing of configuration rules. Keep the admin
socket protected as described in `60-observability-and-runtime.md`.

1. `add backend <name> from <defaults> [mode http|tcp] [guid <guid>]` creates an
   **unpublished** backend. Mode is required unless explicitly supplied by defaults.
2. `add server <backend>/<server> <address> ...` registers each server. Use the
   supported argument list from `add server help`; enable the server and its health
   checks separately with `enable server` and `enable health` when configured.
3. Observe health and intended server state before `publish backend <name>`.
4. Change a trusted map used by a dynamic `use_backend` sample to select the name.
   Do not interpolate unrestricted Host/path/header text into backend selection.
   An unknown/unpublished selection must reach a reviewed fallback, not a tenant
   chosen by attacker-supplied text. `force-be-switch` overrides the normal skip
   of unpublished/disabled references; do not add it without that requirement.

An unpublished match is skipped and evaluation continues. Provide a later routing
rule or `default_backend` for fallback. A map's default value handles a missing
map key; it does not replace a present key pointing to an unpublished backend.

Creation/deletion requires CLI admin; publish/unpublish allows operator or admin.
Static references can prevent deletion: dynamic map-based selection is the useful
pattern. New backends and runtime map changes are process state, not durable
configuration. State-file restoration restores eligible server state; it does not
recreate a deleted/missing backend's structure.

## Drain and remove

Remove or redirect routing first, then `unpublish backend <name>` to stop future
selection while health checks continue. Preserve existing streams until the agreed
drain condition is met. Server `state drain` allows persistence traffic; it is not
an absolute admission stop. `state maint` prevents selection, including persistence.
Choose their timing according to the drain contract, not a fixed delay.

Use `wait <duration> srv-removable <backend>/<server>` and inspect its result before
`del server`; a timeout is not permission to delete. Remove every server, then
`wait <duration> be-removable <backend>` and `del backend`. Backend deletion also
requires no attached streams, no explicit configuration/sample reference, no
local stick table, no incompatible `dispatch`/`option transparent`, and no QUIC
servers having been present. The CLI rejects an unmet condition; record it and
reconcile state rather than forcing destruction.

## Recovery and proof

Keep desired templates, backend/server membership, GUIDs and routing in one
durable controller/config source. Replay safely after restart/reload and handle
already-existing objects; compare `show backend`, `show servers state`, health
and maps before reopening routes. A reload creates a fresh worker from config,
so dynamic objects are lost unless reconstructed. Persisting map text alone can
route to a backend that was not restored. Rollback must restore both membership
and routing, with a deliberate fallback during reconstruction.

`be-unpublished` allows a configured backend to start unpublished from 3.4.4.
The 3.4.3 changelog removes a stale experimental description; the 3.4.6 commands
above do not require the experimental gate. Test create -> unhealthy server ->
healthy server -> publish -> routed request -> unpublish -> fallback -> drain ->
delete; also test failed deletion, concurrent admin reads, replay and reload.
`haproxy -c` validates only the template/routing config, never this lifecycle.
The focused executable probe is
`scripts/check_runtime_3_4.py --docker-image <cached-3.4.6-alpine-image>`;
its prerequisites and proof limits are in `80-gate-register.md`. Check the dated
receipt in `SOURCES.md` before treating a scenario as observed.
