# Decision Matrix

Answer the first question before any other, because it decides which register the whole answer comes from.

## Question 0 — which register are you in?

| Condition | Register | What follows |
|---|---|---|
| The work is inside the Ala `tusd` repository | **(c)** | read `15-ala-service.md` first; no CLI flag applies; the shape is already chosen and this file only tells you whether a proposed change fits it |
| The work is a new upload plane for some other service | **(a)** | this file chooses the shape |
| The work is browser code against an existing plane | **(b)** | this file chooses nothing; go to `60-browser-client.md` |

## Binary or library

| Condition | Choose | Why | Cost you accept |
|---|---|---|---|
| One storage backend, no per-request policy beyond authorization, no control-plane record that must be written inside the request | the **tusd binary** with HTTP hooks | zero code to own; flags and hooks cover it; upgrades are an image bump | a hook transport to secure, reach, time out and monitor |
| Authorization needs trusted context that the hook transport would have to re-derive, or a control-plane row must be written transactionally with creation | the **embedded library** | callbacks are in-process function calls, so there is no transport, no timeout and no forwarded-credential problem | you own routing, locking, metrics registration, size limits and shutdown, none of which the library sets for you |
| More than one storage backend must be selected per request | the **embedded library**, or two deployments | one binary process binds one backend for its lifetime | if you take two deployments, two of everything operational |
| Someone proposes custom append, offset, lock or chunk-storage mechanics | **refuse and re-check** | these are the parts of tus that are hard to get right and that upstream has already got right | prove a specific upstream capability gap first, in writing |

The Ala service took the embedded library and then, predictably, had to supply each thing the binary would have given it. Every unset item in the "cost you accept" column above is a real defect in `15-ala-service.md`. Treat that table as the checklist a new embedded service must complete before it ships.

## One deployment or two

| Condition | Choose |
|---|---|
| Two upload classes with different retention, different storage and different blast radius | two deployments |
| Two upload classes that differ only by a metadata value | one deployment |
| A provider's credentials must never reach the browser and the provider offers no hooks you can use | staging deployment plus an asynchronous relay worker; see `30-topologies.md` |
| Someone wants one deployable unit and accepts owning Go code | one embedded service with more than one composer |

## Hook transport

Only relevant in register (a); the embedded library has no transport.

| Transport | Use when | Refuse when |
|---|---|---|
| HTTP | default; one central hook service, any language, ordinary service-to-service auth | you cannot authenticate the caller of the hook endpoint |
| gRPC | the platform already runs gRPC with mTLS in production today | gRPC would be introduced for this alone |
| File | local development on one machine | anything shared or clustered |
| Plugin | a single-instance Go deployment where hook latency is measured and dominant | more than one instance must share hook state |

Only one transport can be enabled per process. Choosing a transport is choosing where the authorization decision is reachable from, so decide the failure posture in `45-hooks.md` in the same breath.

## Authorization placement

| Requirement | Where it goes |
|---|---|
| May this caller start an upload at all | the creation-time gate: `pre-create` hook, or the pre-create callback in an embedded service |
| May this caller resume, inspect the offset of, or terminate this upload | a per-method check in front of the byte-transfer handler, on every request |
| Has the caller's right been revoked since the upload started | `post-receive` returning a stop decision, in register (a) only |
| Must the provider's credentials stay server-side | stage locally, relay from a worker |

Creation-time authorization alone is never sufficient, because every later request presents only the upload URL. Full treatment in `40-authorization.md`.

## Front door

| Condition | Choose |
|---|---|
| The platform already runs HAProxy | HAProxy; it is the only front door in the Ala fleet |
| A greenfield plane with no existing ingress | whichever the operating team already runs well; both work if buffering is off and timeouts are sized |
| More than one binary instance shares storage | add stickiness before considering a distributed lock; a lock is a design you must then own |

## Defaults

These are defaults, not preferences: apply them, and record the reason when a requirement forces a different value.

- one control-plane call issues an upload plan before any byte moves;
- a server-side size cap on every plane;
- `-disable-download` and, unless the product exposes cancellation through tus, `-disable-termination`;
- one stable trace identifier per upload plus a per-request identifier;
- `removeFingerprintOnSuccess: true` in the browser;
- service-worker exclusion for every upload route;
- `/metrics` and any profiling path reachable only from the internal network;
- an exact version pin, never a floating tag.
