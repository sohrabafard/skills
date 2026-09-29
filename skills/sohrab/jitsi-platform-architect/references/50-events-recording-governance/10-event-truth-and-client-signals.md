Version-sensitive claims in this topic depend on [Jitsi source map](../90-source-map.md).

## The event model

Self-hosted Jitsi does not provide one universal server-side webhook bus for every product event. Build a layered
model instead, and be explicit about which layer is authoritative for which fact:

| Layer | Source | Authoritative for |
|---|---|---|
| client meeting events | the IFrame API in the browser | what the participant's client observed |
| control-plane events | your join, mint, roster and policy services | authorization, issuance, denial, scheduling |
| worker and pipeline events | your recording and storage orchestration | whether an artifact exists |
| room-governance events | a reservation service, where one is used | room creation, expiry, occupancy limits |

**A browser event is a report, not a fact.** It is the fastest signal and the least trustworthy one: it arrives
from a client you do not control, it can be replayed, and it is missing whenever a device dies. Use it for
responsiveness and never as the sole basis for attendance, billing or a compliance record.
## The canonical client event list

- `videoConferenceJoined`
- `videoConferenceLeft`
- `participantJoined`
- `participantLeft`
- `screenSharingStatusChanged`
- `recordingStatusChanged`
- `breakoutRoomsUpdated`
- `audioMuteStatusChanged`
- `readyToClose`
- `log`, only where explicit Jitsi-side log capture is required, and never as a business event stream

Useful functions: `getSessionId()` for a client-visible session handle, `getRoomsInfo()` for a room snapshot when
reconciling, `getNumberOfParticipants()` for an occupancy sample, and `getSupportedCommands()` /
`getSupportedEvents()` when a capability may vary across releases. Query the supported lists rather than assuming a
name survives an upgrade.

This list appears exactly once in this skill. The embedding rules that consume it are in
`references/40-embedding-contract.md`.
## From browser event to platform truth

1. The browser receives a Jitsi event.
2. The browser posts a normalized event to your collector.
3. The collector deduplicates against active session state.
4. The collector enriches with tenant, class session, room, policy and user metadata held server-side.
5. The platform emits downstream events from that enriched, deduplicated stream.

This keeps webhook secrets off the browser, makes replay and deduplication possible, and gives downstream systems
one contract. Dispatch every downstream send from a durable row rather than from inside the request that created
it — the seam is owned by `/alaa-async-messaging`, and the row's public id is what
becomes the idempotency key.
