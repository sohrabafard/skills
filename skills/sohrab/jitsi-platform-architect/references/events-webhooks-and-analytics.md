# Events, Webhooks, and Watch-Time Analytics

## Table of contents

- Event model first principles
- Event sources to use
- Client events that matter most
- Webhook strategy for product systems
- Watch-time analytics model
- Recording and artifact flows
- Privacy and security guidance
- Failure modes and reconciliation

## Event model first principles

Self-hosted Jitsi should not be described as having one universal built-in webhook bus for every product event.

For platform integration, use a layered event model:

- client-side meeting events from the Jitsi IFrame API
- control-plane events from your own join, leave, reservation, and policy services
- recording and artifact events from your own backend orchestration
- optional Jitsi-side plugin or Prosody extension points when there is a specific need

The platform should publish business-grade webhooks to downstream systems only after it has normalized and deduplicated these sources.

## Event sources to use

### 1. Client-side Jitsi events

These are the fastest path for product analytics and UX reactions.

Use them for:

- real join confirmation
- participant presence changes
- screen-share state
- recording state changes visible to the client
- breakout-room changes
- mute-state analytics where appropriate
- close or cleanup flows

### 2. Your own control-plane APIs

These are the authoritative source for:

- join authorization attempts
- token issuance
- denied joins
- reservation or scheduling changes
- host-initiated recording requests
- artifact publication

### 3. Reservation-style room governance

If you adopt a reservation system or external room policy service, that service becomes a useful server-side source for:

- room create
- room read
- room expiry
- max-occupant enforcement
- password or lobby policy changes

### 4. Worker and pipeline events

For recording or streaming, your own worker orchestration and storage pipeline should emit:

- recording requested
- worker assigned
- recording started
- recording ended
- artifact uploaded
- artifact transcoded
- artifact published or failed

## Client events that matter most

A practical default list:

- `videoConferenceJoined`
- `videoConferenceLeft`
- `participantJoined`
- `participantLeft`
- `screenSharingStatusChanged`
- `recordingStatusChanged`
- `breakoutRoomsUpdated`
- `audioMuteStatusChanged`
- `readyToClose`

Useful utility calls:

- `getSessionId()` for a client-visible meeting session handle
- `getRoomsInfo()` for participant and room snapshots when debugging or reconciling
- `getNumberOfParticipants()` for periodic occupancy snapshots

If your JWT context carries a stable platform user id, use that mapping consistently. `userContext.id` in participant-level data can then be tied back to platform identity without depending on mutable display names.

If Jitsi log forwarding is required, the `log` event can be useful, but do not treat it as your main business event stream.

## Webhook strategy for product systems

Build webhooks in your backend, not directly from the browser.

Recommended path:

1. Browser receives Jitsi event.
2. Browser posts a normalized event to your backend collector.
3. Backend deduplicates against active session state.
4. Backend enriches the event with tenant, room, policy, and user metadata.
5. Backend emits downstream business webhooks or internal events.

Why this is better:

- avoids trusting raw browser payloads as final truth
- allows dedupe and replay handling
- keeps secrets and webhook signing on the server
- makes downstream systems consume one consistent event contract

## Watch-time analytics model

Do not compute watch time from room creation time or room lifetime alone.

Use a session model.

### Recommended session model

When issuing a join token or join response, create a platform-side session id such as `joinSessionId`.

Track at least:

- tenant id
- room id
- platform user id
- joinSessionId
- role
- token issue time
- scheduled session id if one exists

### Event sequence

Use this baseline sequence:

- `join_requested`: platform API request arrives
- `join_granted`: backend returns the Jitsi join artifact
- `conference_joined`: browser receives `videoConferenceJoined`
- heartbeat every 15 to 30 seconds while the session is active
- optional activity change events such as screen share start or breakout-room move
- `conference_left`: browser receives `videoConferenceLeft` or `readyToClose`
- timeout reconciliation closes any orphaned session

### Heartbeat payload ideas

Keep the payload small and product-relevant.

Examples:

- joinSessionId
- room id
- platform user id
- role
- visible or backgrounded state
- audio muted or video muted state if needed
- screen sharing state if needed
- participant count snapshot if useful
- breakout room id if applicable
- client timestamp and server receive time

### Metrics to compute separately

Do not collapse these into one number.

- user watch time
- room occupancy time
- presenter or screen-share time
- moderator presence time
- recording overlap time

## Recording and artifact flows

Treat recording as its own subsystem.

Useful event chain:

- record requested by platform action
- policy check result
- worker allocation
- Jitsi client-side `recordingStatusChanged`
- worker-side start confirmation
- worker-side completion or failure
- object storage write complete
- replay asset published

Do not rely only on client-visible recording status for compliance or billing. Use backend worker and storage events as the stronger signal.

## Privacy and security guidance

Use the minimum personal data that the platform actually needs.

- prefer stable internal user ids over emails in analytics pipelines
- do not enable display-name or email-in-stats flags unless there is a real requirement
- sign server-side webhooks and keep browsers away from webhook secrets
- separate raw diagnostic logs from business analytics data
- define retention policy for watch-time data before shipping it

## Failure modes and reconciliation

Browser events are not perfect. Design for cleanup and reconciliation.

Common failure modes:

- browser closes before sending final leave event
- device sleeps and resumes later
- mobile background throttling delays heartbeats
- connectivity drops cause duplicate join or leave transitions
- page refresh creates a new embed instance before the old one fully closes

Recommended safeguards:

- server-side timeout to close stale sessions
- idempotent event ingestion by `joinSessionId`
- dedupe rules for rapid reconnects
- periodic reconciliation against current room state only for operations support, not as the sole business truth
- explicit distinction between “authorized to join” and “actually joined”
