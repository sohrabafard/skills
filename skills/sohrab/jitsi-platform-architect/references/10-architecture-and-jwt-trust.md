# Architecture and the Join-Token Trust Domain

Read this when minting, verifying, sizing the lifetime of, or renewing a Jitsi join token; when naming a room;
when setting the guest domain; or when deciding who is a moderator in a class.

Every upstream Jitsi behaviour named here carries a row in `references/90-source-map.md`. Read the row before the
sentence enters a deliverable. Platform decisions in this file are ours and carry no upstream row.

## Where this skill starts

`/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`) owns everything up to and including one decision: *this
caller is authorized to join room R as role X*. It owns the bearer-token verification, the projection of verified
claims into `X-*` headers, the exact header set a service behind the gateway may believe, and the obligation on a
directly reachable service to strip and reject those headers at its own edge. Do not restate that header set here;
read it there.

This skill owns everything after that decision: the join token derived from it, its claim set, the key that signs
it, the lifetime, what happens when it expires, and what the Jitsi-side verifier is configured to accept.

## The two planes, and why the split decides most arguments

The control plane is your application and the gateway: room-creation intent, join permission, tenant validation,
role assignment, recording permission, token minting and expiry.

The media plane is WebRTC, the videobridge and TURN, after the join succeeds: RTP and RTCP transport, ICE
gathering, STUN and TURN use, stream forwarding, bridge-level behaviour.

The gateway authorizes session entry. It does not authorize a media packet, and no header reaches the media plane.
Any design that says "the gateway checks each stream" has confused the planes and will be built as something that
cannot work.

| Component | Role | Failure blast radius |
|---|---|---|
| Jitsi Meet | web app and meeting surface | one user's browser session |
| Jitsi Videobridge (JVB) | SFU media router, the main scale domain | every conference on that bridge |
| Prosody | XMPP signalling and token verification | every new join, platform-wide |
| Jicofo | conference focus and bridge allocation | every conference it focuses |
| Jibri | recording and streaming worker | one recording per worker |
| TURN | relay for NAT- and firewall-hostile paths | one network path's users |

A production design separates at least: edge and gateway, web and signalling, the JVB fleet, the TURN layer,
recording workers, and the observability stack.

## Who mints, and what the minting service must check

Exactly one service mints join tokens. Name it in the deliverable.

The mint endpoint independently verifies its own caller and never treats a trusted header alone as authorization to
mint. A directly reachable service receives forged headers from anything that can open its port, so a header is
evidence only where the gateway is proven to be the sole path. The header set, the proof mechanism, and the
strip-and-reject obligation are stated by `/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`).

This platform already runs a minting-and-verification pair of exactly this shape, and a Jitsi token endpoint
follows it rather than inventing a second pattern. In TOTP step-up, the auth service mints an RS256-signed proof JWT;
the gateway verifies its signature, its algorithm against an allow-list, its `typ`, `aud` and `iss`, its validity
window, and its binding to the access token; and the gateway holds no list of which operations require step-up, so
the backend decides. The lesson to copy is the separation: the minting service decides policy, the verifier checks
a fixed contract, and neither infers policy from the other.

The endpoint's request and response shape, its error codes and its envelope belong to `/alaa-services-contract`
(`$alaa-services-contract`). Register the route there rather than inventing a shape here.

## The claim set

| Claim | Value | Why it is there |
|---|---|---|
| `iss` | the mint profile identifier the verifier is configured to expect | rejects a token minted by anything else |
| `aud` | the audience of this Jitsi deployment | a staging token cannot open a production class |
| `sub` | the base domain or tenant scope the deployment expects | binds the token to one deployment scope |
| `room` | exactly one room identifier | binds the token to one class session |
| `iat` | issue time, seconds since epoch | the lifetime is measured from here |
| `exp` | expiry, seconds since epoch | bounds the replay window on a stolen token |
| `nbf` | optional not-before | only when a clock-skew allowance is stated |
| `context.user.id` | stable platform user id | ties meeting events back to a person without a display name |
| `context.user.name` | display name | convenience metadata; never a validation input |
| `context.user.avatar`, `context.group` | optional display context | convenience metadata |
| moderator or role, inside `context` | derived server-side from the roster | privilege comes from the platform, never from the browser |

Two rules follow, and both are constraints:

- A claim the verifier does not check is decoration. State in the deliverable which claims this deployment's
  verifier actually checks, and configure it to check `iss`, `aud`, `sub`, `room` and `exp` at minimum. A claim
  present in the token and absent from the verifier's configuration is a comment, and comments do not deny anyone.
- No role, moderator or affiliation claim appears at the top level of the token. Put every such value inside
  `context`. A top-level role claim is the shape most third-party examples use, so it is the shape a copied example
  introduces, and a verifier that ignores it will hand a moderator claim straight through unread.

Run `scripts/check_jitsi_jwt.py` against a real minted token before the mint path ships; it asserts this table.

## Signing-key custody

- The Jitsi signing key is a separate key from every platform access-token key, held in a separate secret, with a
  separate `kid`. Sharing one key means anyone who can read the Jitsi verifier's configuration can mint platform
  access tokens.
- The private key exists in the minting service's secret store and nowhere else — not in an image, a repository, a
  config map, a rendered environment file, or a runbook.
- Use an asymmetric algorithm. Where the release's verifier supports no asymmetric algorithm, record that in the
  deliverable with the ledger row that establishes it, and treat the shared secret as a minting credential held by
  every host that can verify a token — which is more hosts than the auth service has operators.
- Choose exactly one algorithm and configure the verifier to accept only that one. An allow-list of one is what
  turns an `alg: none` token or an algorithm-confusion attempt into a rejected token instead of a valid one.
- Confirm from the release which algorithms the verifier supports before choosing one; that is an upstream fact
  with a row in `references/90-source-map.md`, and it was not verifiable when this file was written.

## Rotation

Rotate on a schedule the project owner sets, and immediately on any suspicion of disclosure.

Scheduled rotation, with zero rejected joins:

1. Publish the new public key or secret to the verifier under a new `kid`, alongside the old one.
2. Wait one full maximum token lifetime, so nothing in flight was minted before the verifier knew the new key.
3. Switch the minting service to the new `kid`.
4. Wait one full maximum token lifetime, so every token signed with the old key has expired.
5. Remove the old key from the verifier.

Disclosure rotation is different and the difference matters: skip the overlap, remove the compromised key from the
verifier immediately, and accept that joins holding a token signed with it will fail. A leaked signing key mints a
moderator into any class, and a few minutes of failed joins costs less than one unauthorized adult in a classroom.

## Lifetime, in seconds

Two numbers get conflated here, and conflating them is the defect:

- the token's validity window, `exp − iat`, which is how long the token may be *presented* at a join;
- the class duration, which is how long the conference runs.

Set the validity window from the join window, never from the class length. **Default: 120 seconds**, on the design
that the client fetches a token immediately before joining. Raise it only to cover a clock-skew allowance and a
retry budget you state as numbers in the deliverable. Never set it to the class duration to avoid mid-call
problems; that trades a diagnosable eject (below) for an undiagnosable replay window on a stolen token.

There is no ratified Jitsi value in `/alaa-services-contract` (`$alaa-services-contract`) yet, so 120 seconds is
this skill's default and the project owner approves any deviation. Timeout, retry and backoff doctrine around the
mint call belongs to `/alaa-reliability-sla` (`$alaa-reliability-sla`).

## Mid-call expiry — the silent eject

The token is validated at join. Once a participant is seated, the token is not re-checked, so an expired token does
not remove anyone. What it breaks is the *next* join — and a reconnect after a network blip performs a join.

The symptom in a classroom: students disappear individually, several minutes into the lesson, more often on mobile
and on poor networks, at no consistent moment, and no server log records a rejection, because from the server's
point of view a stale reconnect is just another failed join among the normal ones. The teacher reports that
students are being randomly kicked. Nothing in the meeting UI says otherwise.

**Design rule: the embed re-fetches a token from the mint endpoint on every reconnect attempt, and never reuses the
token it joined with.** This is the only design that is correct whether or not the release re-validates on
reconnect, which is why it is stated as a rule rather than as a mitigation. The upstream re-validation behaviour has
a row in `references/90-source-map.md` and must be read before any incident report asserts it.

Two consequences to size for: the mint endpoint must stay available for the whole class, not just for its first
minute; and reconnects are correlated, because one school's network event reconnects a whole class at once. See
`references/60-scale-and-capacity.md`.

## Room identity and entropy

On a default Jitsi deployment, knowing the room name is enough to be in the room. The room name is therefore the
access control, and it must be treated as a secret with a stated strength.

- A room name is an opaque, server-generated identifier carrying at least **128 bits of entropy** from a
  cryptographically secure random source. Render it as 26 characters of lowercase Crockford Base32 — see
  `/alaa-crockford-base32-codecs` (`$alaa-crockford-base32-codecs`) for the codec — so that case folding anywhere
  in the path cannot collapse two distinct rooms into one.
- The human-readable title of the class lives in platform metadata, keyed by the room identifier, and never in the
  room name itself. A title in the room name is a title in every browser history, referrer, proxy log and screen
  share of every participant.
- Never derive a room name from a tenant name, a school name, a class name, a course id, a teacher name, a date, a
  timetable slot, or a sequential platform id. Every one of those is either public or enumerable, and a derived
  name reduces a 128-bit search to a guess.
- Never use a UUIDv7 as a room name. Its leading 48 bits are a millisecond timestamp, and a scheduled class has a
  published start time, so those bits are not secret. Use UUIDv7 for the class-session row's public id if you like,
  and generate the room identifier separately.
- Generate the identifier once, when the class session is created, and store it on that row. A recomputed name is a
  derived name, whatever it was derived from.
- Generate a new room identifier for every occurrence of a recurring class. A weekly class that reuses one room
  identifier for a term hands every past attendee a permanent key, including one who has left the school.
- Store the mapping from room identifier to class session in Postgres; schema, index and tenant scoping belong to
  `/alaa-data-layer` (`$alaa-data-layer`).

The `room` claim equals that exact identifier. It is never `*`, never a prefix wildcard, never a list, and never a
pattern. A token matching more than one room admits its holder to every class that matches it, and there is no
in-conference control that recovers from that.

`scripts/check_jitsi_jwt.py --room-name <name>` asserts these rules mechanically. Run it against the generator's
output, not against one hand-written example.

## Guest domain and anonymous authentication

- Anonymous authentication is disabled and the guest domain either is not configured or requires a token. This is
  required configuration for a deployment carrying classes, not a tradeoff to weigh.
- Verify it by observation: from a clean browser profile with no token, open the deployment at a valid room
  identifier and confirm the join is refused. Record that observation, with its date, in the deliverable. A
  configuration file naming token authentication is not evidence, because a package upgrade can restore a default
  and nothing will announce it.
- Repeat that check after every deployment and every upgrade. The check costs a minute; the failure it catches is
  an open classroom.
- When the product genuinely needs unauthenticated guests — a public open day, a parents' evening — build a
  separate deployment with its own domain and its own signing key. Never open a carve-out on the deployment that
  carries classes, because a carve-out outlives the event that justified it and nothing ever closes it.

## Moderator assignment for a class

- The teacher of record is the moderator, resolved server-side from the class roster at mint time and carried
  inside the token's `context`. The client never asserts moderator status; a value from the browser may decide what
  is displayed and never what is permitted.
- Decide, and state, what happens before the teacher arrives. **Default: the class room does not open until the
  moderator's token has been minted at least once.** A room full of students with no adult present is a
  safeguarding event, not a user-experience inconvenience.
- Co-teachers and teaching assistants get their moderator role from the roster, not from an in-meeting grant. If
  in-meeting promotion is enabled, state in the deliverable who may perform it and how it is audited; if that is
  not stated, it is disabled.
- When a teacher's device fails, the recovery path is a fresh mint from the platform, never a promotion granted by
  whoever is left in the room.

## Room lifecycle for a scheduled class

| Platform event | What exists in Jitsi |
|---|---|
| class scheduled | nothing; the room identifier is generated and stored on the class-session row |
| join window opens (default T−10 minutes; state the value) | the mint endpoint begins returning tokens for that room |
| first authorized join | the room materialises on first join |
| class in progress | tokens continue to be minted for reconnects and late arrivals |
| scheduled end | the mint endpoint stops returning tokens |
| after the session | the room identifier is retired and never reused |

The row that surprises people: **the mint endpoint refusing to issue tokens does not end a running conference.**
Seated participants stay seated. State explicitly which mechanism ends the class — a moderator-issued end, a
scheduled removal, or letting the room drain — because "we stop minting at the bell" is not an ending.

Reservation-style room control, where the deployment asks an external service to approve a room before it is
created, is the pattern that fits a scheduled class best: start time, duration and maximum occupancy are all known
before the first join, which is exactly the input a reservation service wants. Its availability and API are an
upstream fact with a row in `references/90-source-map.md`.

## What stays outside Jitsi

Roster and enrolment, attendance truth, grades, the permission graph, billing and quotas, retention and compliance
policy, and the audit trail all stay in the platform. Jitsi holds session mechanics and nothing that must survive
the session. Object-level relations belong to the vendored `/openfga` (`$openfga`) skill and to
`/alaa-trust-gateway-auth` (`$alaa-trust-gateway-auth`).
