# Architecture and Auth

## Table of contents

- Core mental model
- Where Jitsi fits well
- Where Jitsi is weaker
- Component roles
- Control plane versus media plane
- Trust-gateway and JWT pattern
- Token contents and claim rules
- Room lifecycle and authorization flow
- Reservation-style room control
- Security defaults
- Common mistakes

## Core mental model

Treat Jitsi as a componentized conferencing system, not a single monolith and not the product system of record.

In most platform designs:

- your platform owns identity, tenants, billing, policy, audit, and analytics
- Jitsi owns meeting session mechanics, signaling, and media forwarding
- your backend mints narrow meeting-scoped join artifacts after platform authorization succeeds

That is the cleanest fit for security-sensitive products.

## Where Jitsi fits well

Jitsi is usually a strong fit when the product wants:

- self-hosted browser and mobile conferencing
- a modern WebRTC SFU architecture
- JWT-based room admission
- embeddable conferencing inside a larger platform
- externally managed identity and authorization
- horizontal scale mainly through more videobridges

It is especially well aligned with a trust-gateway pattern because the platform can remain the decision-maker and Jitsi can consume a room-scoped assertion.

## Where Jitsi is weaker

Do not oversell Jitsi as a complete classroom suite by default.

Use a more cautious framing when the product expects:

- education-first whiteboard and slide workflows out of the box
- LMS-grade attendance semantics without platform work
- turnkey teaching UX with little product engineering

A useful default comparison is:

- Jitsi = conferencing platform
- BigBlueButton = classroom-first product

## Component roles

Keep the control and media responsibilities explicit.

- `Jitsi Meet`: web app and user-facing meeting surface
- `Jitsi Videobridge (JVB)`: SFU media router and main scale domain
- `Prosody`: XMPP signaling and auth-related flows
- `Jicofo`: conference focus and bridge orchestration
- `Jibri`: recording and streaming worker
- `Jigasi`: SIP and some transcription-related integrations in supported setups
- `TURN`: relay for hostile NAT and firewall paths

A serious production design usually separates at least these domains:

- edge and gateway
- web and signaling
- JVB fleet
- TURN relay layer
- recording workers
- observability stack

## Control plane versus media plane

This separation is the key architectural rule.

### Control plane

Handled by your application and gateway.

Typical responsibilities:

- room creation intent
- room join permission
- tenant and namespace validation
- role assignment such as moderator, speaker, attendee, or visitor
- whether recording or screenshare is allowed
- token minting and session expiry

### Media plane

Handled by WebRTC, JVB, and TURN after the join succeeds.

Typical responsibilities:

- RTP and RTCP transport
- ICE candidate gathering and connectivity checks
- STUN and TURN usage
- stream forwarding and adaptive delivery
- bridge-level media behavior

Do not describe the gateway as authorizing each media packet. The gateway authorizes session entry; Jitsi enforces the resulting session behavior.

## Trust-gateway and JWT pattern

Use this pattern by default.

1. The user authenticates with your platform.
2. The gateway validates the platform token and sanitizes trusted headers.
3. Your backend checks room access through platform policy, membership, and tenant logic.
4. Your backend mints a short-lived Jitsi JWT scoped to the room and role.
5. The client joins Jitsi using that Jitsi token.
6. Your platform separately records attendance, analytics, and artifacts.

Prefer a derived Jitsi token over passing the raw platform access token into Jitsi.

Reasons:

- smaller trust boundary
- room binding and shorter lifetime
- cleaner secret separation
- less coupling between platform auth and Jitsi internals

## Token contents and claim rules

Model the Jitsi token as a narrow meeting assertion.

### Claims that usually matter

- `iss`: issuer controlled by your platform
- `aud`: audience expected by the Jitsi deployment
- `sub`: deployment scope or tenant/base domain, depending on packaging
- `room`: exact room name or carefully controlled wildcard use
- `exp`: short expiration
- optional `nbf` and `iat`

### Optional context fields

The token may also carry optional display and analytics context such as:

- `context.user.id`
- `context.user.name`
- `context.user.email`
- `context.user.avatar`
- `context.group`

Important rule: treat these context values as convenience metadata, not as the main validation boundary.

### Practical guidance

In token-auth deployments, assume every user who joins a protected meeting will need a valid Jitsi token unless the task explicitly describes a guest-domain exception.

- keep tokens short-lived
- bind them to one room whenever possible
- avoid broad wildcard room claims unless there is a very strong reason
- use separate signing secrets or keys from the ones used for your main platform tokens
- do not let the browser invent role claims on its own

When identity must be available inside the meeting analytics path, prefer a stable platform user id in `context.user.id`.

## Room lifecycle and authorization flow

Keep lifecycle control in your platform.

### Minimum flow

- the client asks your API to join a room
- your backend validates tenant, membership, and policy
- your backend decides role and feature access
- your backend mints the Jitsi token and returns only what the client needs
- the client joins and your app listens for client-side meeting events

### Platform-owned data that should stay outside Jitsi

- tenant model
- course or class membership
- permission graph or OpenFGA relationships
- quotas and billing
- attendance rules
- analytics warehouse data
- audit trail
- retention and compliance policy

## Reservation-style room control

When the product needs stronger room governance, reservation-style control is useful.

That pattern can support ideas like:

- create or reserve room before first join
- enforce duration limits
- cap max occupants
- set lobby and password policies
- map platform metadata into room policy

Use this when the product treats rooms as managed resources rather than free-form ad hoc names.

## Security defaults

Default to these positions unless the task explicitly calls for a different tradeoff.

- platform remains the identity source of truth
- gateway strips and rewrites trusted identity headers
- only backend services mint join tokens
- short-lived room-scoped tokens only
- moderator and guest rules derived from platform policy, not arbitrary frontend flags
- private JVB and control endpoints remain private
- TURN credentials and Jitsi signing material are managed separately

## Common mistakes

Avoid these patterns.

- treating Jitsi like a normal REST microservice
- letting raw frontend claims decide moderator privileges
- making long-lived broad tokens that work across many rooms
- mixing platform auth secrets and Jitsi signing secrets
- assuming client display data is the same as validated identity
- turning Jitsi into the system of record for tenants or compliance data
