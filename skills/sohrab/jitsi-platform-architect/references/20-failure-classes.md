# Failure Classes

Read this when explaining why a conference dropped, why a participant vanished, why a recording stopped, or why a
bridge went away — and before planning a drain, a restart or an upgrade.

Each class is written as symptom, diagnosis in order, the smallest safe retry, and escalation. Follow the diagnosis
order: several of these classes look identical from a browser, and the cheap discriminator is always first.

Retry legality, backoff shape, breaker placement and degradation doctrine belong to `/alaa-reliability-sla`
(`$alaa-reliability-sla`). Telemetry field names, event names and metric names belong to `/alaa-services-contract`
(`$alaa-services-contract`); which of them are required and at what level belongs to `/alaa-observability-soc`
(`$alaa-observability-soc`). This file states what to look at, not what to call it.

## What to capture for every class below

Capture, at the moment of the incident: the correlation id of the join or mint request, the room identifier, the
class-session id, the wall-clock time with timezone, the number of participants affected, and whether the affected
set shares a bridge, a school, or a network. Do not put the class title or a participant name in the same record as
the room identifier; the room identifier is the access control, and a record that pairs it with a human label turns
a log reader into a class attendee.

## The ambiguous outcome, before any class

A mint call that times out after the request bytes were written tells you nothing about whether a token was
issued. A connection refusal and a timeout are different events and must not share a code path — the rule is
`/alaa-reliability-sla` (`$alaa-reliability-sla`) `references/20-retries.md`.

For this boundary specifically: **a mint timeout may be retried once with a fresh request, because a token grants
nothing until it is presented and two tokens for the same user and room are harmless.** The attendance record is
what must not double, so key attendance on the class session and the platform user id, never on the number of
tokens minted. A mint that is counted as an attendance event is a mint that cannot be retried.

## 1. A videobridge dies mid-conference

**Symptom.** Every participant in one or more conferences loses audio and video at the same instant while the
meeting UI stays up and the roster still renders. Conferences on other bridges are unaffected. The teacher reports
that everyone froze at once.

**Diagnosis, in order.**

1. Confirm the affected conferences share one bridge. If they do not, this is not the class — go to class 2 if
   nobody can join either, or class 6 if only some participants are affected.
2. Separate "the process is gone" from "Jicofo cannot reach it". Those have different fixes and the same symptom.
3. Check the bridge's health endpoint and its last-seen time in Jicofo's view.

**Smallest safe retry.** Have the affected participants leave and rejoin once, which forces a fresh conference
allocation onto a healthy bridge. Whether Jicofo re-invites automatically, and how long it takes, is an upstream
behaviour with a row in `references/90-source-map.md`; do not quote a recovery time to a teacher from memory.

**Do not restart Jicofo.** Restarting it to recover one bridge fails every other class running at that moment. See
class 3.

**Escalation.** A second bridge failure inside the same teaching period is a fleet event, not an incident: stop
retrying and look for a capacity limit or a bad release. Carry the bridge id, the affected conference ids, the
time, the participant counts, and whether the process exited or was merely unreachable.

**Prevention.** One bridge serving a whole timetable means one bridge failure cancels the school day. Bridge count
is a capacity decision made before the term, not after the incident — `references/60-scale-and-capacity.md`.

## 2. Prosody restarts

**Symptom.** No new participant can join anything. Participants already seated keep media for a while and then
degrade. The token mint endpoint keeps returning success, because minting never touches Prosody, so the platform's
own health page stays green while every join in the building fails.

**Diagnosis, in order.**

1. Check Prosody's uptime. A restart is visible there in one step and nowhere else quickly.
2. Establish whether joins are failing before or after token verification. A rejected token and a dead signalling
   plane are indistinguishable in the browser. The discriminator: a token fault affects a subset deterministically
   and reproduces on retry; a Prosody restart affects everyone from one instant.
3. If Prosody restarted because it ran out of memory or is crash-looping, this is a control-plane capacity event
   and belongs in `references/60-scale-and-capacity.md`.

**Smallest safe retry.** Wait for Prosody to accept connections, then rejoin. Do not loop the mint-and-join path
while signalling is down: every client retrying at once produces a join storm at the exact moment the service
returns, which is how a thirty-second restart becomes a ten-minute outage.

**Escalation.** Repeated restarts are an infrastructure event; carry the restart times, the memory trend and the
join-failure count.

**Design consequence.** A healthy mint endpoint is not evidence that anyone can join. The only readiness signal
that means anything here is a synthetic join executed continuously against a dedicated room, and it must be part
of the deployment from the first class, not added after the first outage.

## 3. Jicofo loses bridge state

**Symptom.** New conferences fail to allocate a bridge, or every new conference lands on one bridge while others
sit idle. Conferences already running continue normally, which is what distinguishes this from class 1.

**Diagnosis, in order.**

1. Compare Jicofo's view of the bridge list against the bridges actually running. A bridge that is up but absent
   from the list is a registration failure, not a bridge failure.
2. Check the signalling path between that bridge and Prosody before touching Jicofo.

**Smallest safe retry.** Restart the affected bridge so it re-registers. That costs the conferences on that one
bridge. Restarting Jicofo costs every conference it is focusing, which during a teaching period is all of them.

**Escalation.** If restarting Jicofo is genuinely unavoidable, do it in a drain window. A school timetable supplies
one every period — see class 7. **Never restart Jicofo inside a teaching period.**

## 4. A join token expires mid-call — the silent eject

**Symptom.** Participants disappear one at a time, several minutes into the class, more often on mobile and on
poor networks, at no consistent moment. Nothing in the server logs records a rejection that looks unusual. The
teacher reports that students are being randomly kicked.

**Diagnosis, in order.**

1. Compare the token's `exp` against the *reconnect* time, not the join time. If `exp − iat` is shorter than the
   class and the client reuses its original token, this is the class and no further evidence is needed.
2. Reproduce it deterministically: join, disable networking until past `exp`, re-enable. A participant who cannot
   return has confirmed it.

**Smallest safe retry.** The participant rejoins the class from the platform, which mints a fresh token and works
immediately. That is precisely why this defect survives for months: the workaround is invisible and always
succeeds, so nobody files it as a fault.

**Fix.** Re-fetch a token on every reconnect attempt — the rule is in
`references/10-architecture-and-jwt-trust.md`. Do not lengthen the token to the class duration as the fix; that
exchanges a diagnosable eject for an undiagnosable replay window on any token that leaks.

**Escalation.** None. This is a defect in the embed, not an incident, and it is fixed in the frontend — see
`references/40-embedding-contract.md`.

## 5. Jibri fails mid-recording

**Symptom.** The recording indicator disappears during the class, or the artifact is missing or truncated
afterwards. The conference itself is unaffected, so nobody notices until someone looks for the recording.

**Diagnosis, in order.** These are three faults with three different owners, and checking them out of order wastes
the most time:

1. Did the worker exit? That is a recording-plane capacity or crash fault.
2. Did the capture succeed and the upload fail? That is a storage-path fault, and a partial artifact usually
   exists.
3. Did the upload succeed and storage reject or expire it? That is a retention or credential fault.

**Smallest safe retry.** If the class is still running, start a new recording for the remainder. Do not assume the
platform can splice two segments into one artifact unless the pipeline was built to; state which it is.

**Tell the teacher, inside the meeting, that recording stopped.** A class that believes it is being recorded
behaves differently from one that knows it is not, and a silently failed recording of a graded session is a dispute
the platform will lose.

**Escalation.** A second recording failure in the same period means stop starting recordings and queue them. A
recording worker pool with no admission control turns one failure into a cascade, because every failed start
returns capacity to a queue that immediately spends it again.

**Admission control at this boundary is new work on this platform.** The service kit provides no rate limiting, no
circuit breaking, no backpressure, no load shedding, no in-flight cap and no ingress request deadline; the kit's
own `AGENTS.md` names rate limits and breakers as a design goal. Do not plan around a kit capability that does not
exist — either build the cap in the service and say so, or state the accepted risk with a number.

**Governance consequence.** A failed recording still captured part of a class. Notice, retention and deletion apply
to the partial artifact exactly as they apply to a complete one —
`references/50-events-recording-governance.md`.

## 6. TURN relay unreachable

**Symptom.** A subset of participants — one school, one internet provider, one corporate network — join
successfully, see the roster, and exchange no media. Two-party calls sometimes work where larger ones fail.

**Diagnosis, in order.**

1. Confirm the affected participants share a network path before touching anything in Jitsi. If they do not, this
   is not the class.
2. Check UDP reachability from that network to the bridge, and the addresses the bridge advertises.
3. Check TURN reachability and the credentials. **A TURN credential that has expired looks exactly like a firewall
   block from the client side**, and the two lead to opposite fixes, so check the credential before blaming the
   network.

**Smallest safe retry.** None on the client. Retrying a blocked path produces the same result at the same cost.
Moving one affected participant onto a different network confirms the diagnosis in under a minute and is worth more
than any log.

**Escalation.** To whoever owns the network path, carrying the client's ICE candidate evidence, the time, and the
observation that the same client works elsewhere. School and corporate networks are the common case here, not the
exception — plan TURN as a required component, not a fallback.

## 7. Planned shard drain, restart or upgrade

**Symptom.** None, when it is done correctly. This is the class you plan rather than diagnose, and it is in this
file because the unplanned version presents as class 1.

**Procedure.**

1. Stop new conference allocation to the target bridge.
2. Let the running conferences finish. **A conference does not migrate between bridges without dropping media**, so
   drain by waiting, never by evicting.
3. Remove the bridge only when it is empty.

**Use the timetable.** Between teaching periods, occupancy falls to near zero on a predictable schedule. That is
the only cheap maintenance window a class platform has, and it is worth more than any rolling-update mechanism.
State the window, with its clock times, in the deliverable.

**If a drain must happen inside a period, say so and accept that the affected classes see class 1's symptom.** A
drain presented as zero-impact when it is not is worse than a scheduled interruption, because the teacher reports
it as a fault and someone spends the afternoon looking for one.

**Escalation.** None for the drain itself. A drain that cannot wait for a between-period window is a capacity
problem — `references/60-scale-and-capacity.md`.
