---
name: jitsi-platform-architect
description: "Self-hosted Jitsi Meet and Videobridge as an Ala subsystem for online classes: the join-token trust domain from the platform's authorization decision onward, room-name entropy, guest-domain lockdown, recording governance, capacity, embedding, and live-conference failure classes. Use when designing, securing, sizing, embedding, deploying or debugging self-hosted Jitsi — minting or renewing a Jitsi JWT, naming a room, assigning a moderator, starting or retaining a recording, exposing JVB or TURN, choosing a substrate, or diagnosing a mid-conference drop. Jitsi is planned here and not yet deployed, so nothing in this skill is evidence about what the platform runs. Do not use it for end-user meeting help, generic WebRTC theory, or another conferencing product except in a direct comparison. Route gateway header trust to /alaa-trust-gateway-auth, frontend code shape to /alaa-vue-typescript-clean-code, substrate mechanics to /alaa-k8s-helm."
---

# Jitsi Platform Architect

Self-hosted Jitsi as one Ala subsystem, carrying online classes. **A class is not a meeting**: its scheduled
start, known roster, teacher-moderator, gradeable recording and pre-known headcount each change a decision below.
It owns everything after the platform decides a caller may join room R as role X — the derived token,
room-name entropy, guest-domain lockdown, moderator assignment, recording governance, and the media plane's
substrate demands.

**Status.** No Jitsi deployment exists in this repository today. Every rule here is a decision to make, not an
observation, so nothing here is evidence about what the platform operates.

## When not to use

End-user meeting help, generic WebRTC theory, or another conferencing product unless the task asks for a
comparison. Editing Jitsi's source, unless maintaining a fork.

## Rules that hold on every task

1. A room name is an opaque server-generated identifier with at least 128 bits of entropy from a cryptographically
   secure source, rendered as 26 lowercase Crockford Base32 characters. Knowing the room name is enough to be in
   the room.
2. Never derive a room name from a tenant, school, class, course id, teacher, date, timetable slot, sequential id
   or UUIDv7; the human title stays in platform metadata. Each is public or enumerable, and UUIDv7 leads with a
   timestamp the published start time discloses.
3. The `room` claim equals exactly one room identifier — never `*`, a prefix wildcard, or a list. A token
   matching more than one room admits its holder to every class it matches.
4. Anonymous authentication is disabled and the guest domain locked before the first real class, verified by
   joining with no token from a clean profile and observing the refusal. A configuration file is not evidence: an
   upgrade can silently restore a default.
5. No platform access token, refresh token or gateway header ever reaches Jitsi; mint a token scoped to one
   conference. Jitsi components log and forward the token, so a platform credential inside one reaches every
   media-plane operator.
6. The mint endpoint verifies its own caller and never treats a trusted header alone as authorization to mint. A
   directly reachable service receives forged headers from anything that can open its port.
7. No recording starts without a server-side authorization check and a notice rendered before capture begins. A
   class recording captures minors in many jurisdictions, and consent never displayed cannot be evidenced later.
8. Never state an upstream Jitsi fact without its row in `references/90-source-map.md`, and re-read any row older
   than 90 days before using it. An undated fact reads as authoritative and gets copied forward until it is wrong.

## References — read the row you match

| You are about to … | Read |
|---|---|
| mint, renew or size a join token; name a room; lock the guest domain; assign a moderator | `references/10-architecture-and-jwt-trust.md` |
| diagnose a dropped conference, vanished participant, stopped recording or missing bridge; plan a drain | `references/20-failure-classes.md` |
| choose a substrate, expose JVB or TURN, brief a cluster team | `references/30-deployment-substrate.md` |
| embed in Vue, Quasar or Vite, or weigh the IFrame API against `lib-jitsi-meet` | `references/40-embedding-contract.md` |
| consume a meeting event, compute attendance, start or retain a recording | `references/50-events-recording-governance.md` |
| size a component, plan the top-of-period join burst, state an availability target | `references/60-scale-and-capacity.md` |
| repeat any claim about Jitsi behaviour, a config key, release or support tier | `references/90-source-map.md` |

## Check the contract

```
python3 scripts/check_jitsi_jwt.py --self-test
python3 scripts/check_jitsi_jwt.py --token-file <path> --profile <profile.json>
python3 scripts/check_jitsi_jwt.py --room-name <name>
```

Exit `0` held; `1` a rule broke — fix the mint path or the generator, never the sample; `2` bad input, never a
pass; `3` the self-test failed, so no result here can be trusted. It asserts claim shape, never a signature: a
signed token can still open a classroom.

## Every deliverable states

- which service mints, what it verifies about its caller, and the lifetime in seconds;
- how room identifiers are generated, stored, retired;
- the recording policy: who may start one, where artifacts land, retention, who is told;
- where public UDP terminates, how TURN is provided, whether the substrate carries more than one bridge;
- the peak join rate from the timetable, with the date it was read;
- the remaining single points of failure and the prerequisites the app team cannot satisfy alone.

## Not owned here

Everything up to "this caller may join room R as role X", the trusted header set, and edge strip-and-reject:
`/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`). Endpoint shapes, envelopes, error codes, telemetry names
and platform values: `/alaa-services-contract` (`$alaa-services-contract`). Doctrine lives with its owner:
retries, timeouts, breakers and degradation `/alaa-reliability-sla` (`$alaa-reliability-sla`); fail-closed and
threat classes `/alaa-security-review` (`$alaa-security-review`); telemetry levels `/alaa-observability-soc`
(`$alaa-observability-soc`); the quality bar `/alaa-project-constitution` (`$alaa-project-constitution`); model
and effort `/alaa-prompting-guide` (`$alaa-prompting-guide`); test layer `/alaa-testing-strategy`
(`$alaa-testing-strategy`). Every other owner — substrate, edge, frontend, data, messaging,
orchestration — is named at the rule it governs inside `references/`.
