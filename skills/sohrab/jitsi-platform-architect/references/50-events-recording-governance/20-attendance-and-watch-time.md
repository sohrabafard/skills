Version-sensitive claims in this topic depend on [Jitsi source map](../90-source-map.md).

## Attendance and watch time for a class

Never compute attendance from room lifetime, and never equate "a token was minted" with "the student attended".
Both are the same error: a permission is not a presence.

Create a platform-side join session when the token is minted, and track: tenant, class session, room identifier,
platform user id, join session id, role, and issue time.

Baseline sequence:

- `join_requested` — the platform API request arrives
- `join_granted` — the backend returns the join artifact
- `conference_joined` — the browser reports `videoConferenceJoined`
- a heartbeat every 15 to 30 seconds while the session is active
- activity transitions such as screen-share start or a breakout move
- `conference_left` — the browser reports `videoConferenceLeft` or `readyToClose`
- timeout reconciliation closes any session that never reported a leave

Keep the heartbeat payload small: join session id, room identifier, platform user id, role, visible or backgrounded
state, mute states where the product needs them, an occupancy sample, breakout room where applicable, and both the
client timestamp and the server receive time. Keep those two timestamps separate; a client clock is an input, not
a measurement.

Compute these separately and never collapse them into one number, because a school will ask for each of them
individually: student watch time, room occupancy time, presenter time, moderator presence time, and recording
overlap time.

**Reconciliation is required, not optional.** Browsers close without sending a leave, devices sleep, mobile
background throttling delays heartbeats, connectivity drops duplicate join and leave transitions, and a page
refresh creates a new embed before the old one has closed. Handle it with: a server-side timeout that closes stale
sessions, idempotent ingestion keyed by join session id, deduplication for rapid reconnects, and an explicit
distinction in the data model between "authorized to join" and "actually joined".
