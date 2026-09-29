# Reconnect

## Reconnect

**A consumer reconnects with exponential backoff and full jitter, and never with a fixed delay.** Every
consumer in a fleet loses its connection at the same instant when the broker restarts, so a fixed delay
makes them all reconnect in the same instant and the broker refuses the whole fleet again.

**A reconnect redeclares the consumer's topology before consuming.** A queue or binding that was lost with
the connection otherwise leaves the consumer connected, healthy-looking, and receiving nothing.

**A consumer that cannot reconnect exits non-zero rather than idling.** An idle consumer holds its place in
the supervisor and reports nothing wrong, while its queue grows unattended; a process that exits is
restarted and its restart count is visible.

**Set an explicit heartbeat on the connection.** Without one, a connection dropped by an intermediary stays
open from the client's point of view and the consumer waits forever on a socket nothing will deliver to.
The heartbeat interval is a value: `alaa-services-contract`.
