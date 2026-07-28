# Events, Attendance, and Recording Governance

Read this when consuming a meeting event, computing attendance or watch time, or starting, storing, publishing,
retaining or deleting a class recording.

Event field names, event names, error codes and metric names belong to `/alaa-services-contract`
(`$alaa-services-contract`); which signals are required and at what level belongs to `/alaa-observability-soc`
(`$alaa-observability-soc`). Every IFrame API name below has a row in `references/90-source-map.md`.

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
it — the seam is owned by `/alaa-async-messaging` (`$alaa-async-messaging`), and the row's public id is what
becomes the idempotency key.

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

## Recording governance

A recording is a data-protection event, not a feature toggle. In an online class it is a recording of minors in
many jurisdictions, and it may be a graded artifact, which means it can be evidence in an academic dispute. Every
rule below exists because one of those two facts makes the generic answer wrong.

### Who may start one

- A recording starts only after a server-side authorization check against the class roster and the class's
  recording policy. The in-meeting button is a request; the platform decides.
- The recording policy for a class is set before the class starts, by a role the deliverable names. It is not
  decided inside the meeting, because a decision made inside the meeting cannot be reviewed before capture begins.
- **Never record every class automatically by default.** Capture that nobody chose is capture that nobody governs,
  and the retention bill and the consent gap both arrive later.

### Who is told

- Every participant sees a notice before capture begins and a persistent indicator while it runs. A notice that
  appears after the first frame is not consent.
- Guardians are informed by the platform when the class is scheduled, not at the moment of capture. A notice
  delivered to a child at capture time reaches nobody who can act on it.
- The teacher is told, inside the meeting, when a recording fails — see class 5 in
  `references/20-failure-classes.md`.

### Where the artifact lands

- Into a named bucket and path stated in the deliverable, encrypted at rest, never public and never
  world-readable by URL.
- Access is granted through a short-lived platform-issued URL after a platform authorization check, so that access
  is revocable and audited. A permanent link is an unrevokable grant.
- The room identifier may appear in the object path; the class title and any participant name may not, because
  object paths appear in logs, backups and support tickets.
- Object-storage platform mechanics — bucket lifecycle policy, replication, IAM shape, CDN origin, credential
  rotation — have no owning skill in this library. State the requirement in the deliverable and name the team that
  will implement it rather than assuming a default exists.

### How long it is kept

- **Default retention: 90 days from the end of the class**, configurable per tenant, and the number is stated in
  the deliverable rather than left to the storage layer.
- A recording cited in a grade, an appeal or a disciplinary process is held until that process closes and then
  returns to the default.
- **Absolute boundary: no recording is retained beyond what the tenant's data-protection statement declares, and
  where no statement declares a period, no recording is made.** The alternative to this rule is not flexibility —
  it is a retention period decided by whoever eventually runs out of disk.
- Legal review of the recording policy is a prerequisite for the first recorded class, not a follow-up task. The
  project owner approves the policy.

### Deletion

A deletion request deletes the artifact **and every derived copy**: transcodes, thumbnails, captions and
transcripts, cached edge copies, backup snapshots within the retention window, and any analytics record that
embeds the content rather than referring to it. Enumerate those copies in the deliverable at the time the pipeline
is designed. A partial deletion reports success and leaves the material in place, which is the worst of both
outcomes.

### Audit

Every recording start, stop, download, share and deletion is an audited event carrying the actor, the time, the
room identifier and the class session. Audit records are platform truth and outlive the artifact, because the
question asked afterwards is usually who watched it, not what was in it.

### The event chain to instrument

Recording requested → policy check result → worker allocated → client-visible `recordingStatusChanged` → worker
start confirmed → worker completion or failure → object write complete → artifact published or failed.

Never treat the client-visible status as the compliance or billing signal. The worker and storage events are the
stronger evidence, and they are the ones that exist when the browser has already closed.

## Analytics privacy

- Use stable internal user ids in analytics pipelines, never email addresses.
- Do not enable display-name or email-in-statistics flags without a stated requirement.
- Sign server-side webhooks; keep the signing secret off the browser.
- Keep raw diagnostic logs separate from business analytics.
- Define the retention period for watch-time data before shipping the collector, for the same reason as recordings:
  an undeclared period is decided by a disk.
