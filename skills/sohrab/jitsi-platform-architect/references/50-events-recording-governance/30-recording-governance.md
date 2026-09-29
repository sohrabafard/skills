Version-sensitive claims in this topic depend on [Jitsi source map](../90-source-map.md).

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
- Object-storage policy — bucket lifecycle, replication, IAM, CDN origin and credential rotation — belongs to
  `/alaa-minio-object-storage`, with Arvan differences in `/alaa-arvan-object-storage`. Apply that owner and
  name the team implementing the recording's storage requirements in the deliverable.

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
