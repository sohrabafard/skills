# Deep Review, Configuration, And Deployment Hardening

Read on Deep Review, or when the change touches a security-relevant configuration value or default, a dependency, a container image, or a network exposure.

# Part 1 - Configuration of security controls

**Every security-relevant configuration value is validated at process start, and a value that fails validation stops the process before it serves traffic.** A control configured wrongly is a live vulnerability that no test caught, because no test read the configuration.

## What counts as security-relevant

- The signing algorithm allowlist, key material references, issuer and audience sets, and the clock-skew window.
- Credential lifetimes and the revocation staleness bound.
- The password hashing algorithm and its cost parameters.
- The outbound-fetch host, scheme, and port allowlist; the redirect hop limit; the response byte, time, and content-type bounds.
- The upload media-type allowlist, per-file and per-tenant size ceilings, quota windows, and archive and image expansion bounds.
- Rate-limit ceilings, lockout thresholds, and lockout windows.
- CORS allowed origins, methods, headers, and the credentials flag.
- Trusted-proxy addresses and the number of forwarded hops to trust.
- Cookie attributes and the Content Security Policy.
- TLS versions, cipher policy, and certificate verification settings.
- The tenant-derivation source, and the enabling flag of any cross-tenant path.
- Debug, verbose-error, profiler, and introspection switches: framework debug pages, GraphQL introspection, API-documentation UIs, and detailed health or actuator output.
- Any feature flag that gates one of the controls above.
- The secret-manager reference and the identity used to read it.

## Rules

- **Absence is a boot failure, never a permissive fallback.** No default is less safe than the production value.
- **An empty or missing allowlist denies everything.** An empty list that means "allow all" is stop-the-line item 22.
- A boolean that **enables** a control defaults to on. A boolean that **disables** a control has no default, must be set explicitly, and is refused by the boot validator when the environment is production.
- The validator's failure message names the key and the constraint it violated, and never prints the value.
- Configuration is read once at start into an immutable structure. A control's parameters are not re-read per request from a mutable source, because a runtime change would then bypass the boot validator entirely.
- Where a control's enablement is deliberately runtime-toggleable - a kill switch - toggling it requires an exact permission and emits a security event recording who, when, and why.
- A configuration value that differs between environments differs only in its value, never in whether the control exists.

Flag when: an environment read falls back to a permissive literal; a disable-flag defaults to `true`; a boolean parser treats an unparseable value as the safe-looking branch without saying so; a value is used before validation; a certificate- or hostname-verification switch exists outside a test-only build; a debug or introspection switch defaults to on; an example configuration file carries a working secret; two services that must agree on a value each read it from a different key.

# Part 2 - Dependencies

- A new or upgraded dependency is checked against advisories **before merge**, using the check the repository's CI already runs, and that output is the evidence in the report. Per stack: PHP `composer audit`; Go `govulncheck ./...` together with `go mod verify`; Node the repository's own lockfile audit command; Python `pip-audit` where present.
- Where the repository has no advisory check at all, that absence is a P2 finding on the change that adds the first third-party dependency, and the review names the command for the stack. Never propose adopting a new product.
- The lockfile is committed, and the install in CI and in the image resolves from the lock rather than fresh.
- The licence is open-source and compatible with the repository's existing set; the review names the licence rather than asserting it is fine.
- For each new dependency, answer four questions, because each one routes to a rule elsewhere: does it parse untrusted input (`20-untrusted-input.md`), execute a subprocess (`20-`), open a network connection (`30-outbound-fetch-and-files.md`), or load native code? Add the maintenance signal - most recent release, open advisories, transitive dependency count - and whether the capability already exists in the standard library or in a dependency already present.
- A dependency that runs a script at install time runs it inside CI, with whatever credentials that environment holds. The review names every install-time script the new dependency set introduces and what it does; a dependency carrying one is adopted only with that report and with the lockfile pinning it by integrity hash.

# Part 3 - Deployment and runtime hardening

- **TLS** terminates at a named component, and every hop after it is either encrypted or inside a boundary the review names. The application must know which, because its cookie `Secure` flag and its redirect scheme depend on it.
- **Trusted proxies**: the application accepts forwarded client-address and protocol headers only from a configured set of peer addresses, and trusts a configured number of hops. An application that accepts a forwarded address from any source lets any caller forge the address that every rate limit, audit record, and geographic rule uses.
- **CORS**: allowed origins are an exact list. Never a reflection of the request's `Origin`, and never a wildcard together with credentials - reflecting the origin while allowing credentials is equivalent to having no same-origin policy at all.
- **Container**: a non-root user, no added capabilities, a read-only root filesystem where the workload permits, no container-runtime socket mounted, and a base image pinned by digest. Secrets arrive by mount or environment from the platform, never in an image layer or a build argument.
- **Network**: only the edge is publicly reachable. Databases, caches, brokers, search clusters, and internal sidecars are private, and the review names the mechanism that enforces it - a network policy, a security group, or a listener binding - rather than asserting the topology.
- **Operational endpoints**: health, metrics, profiler, and debug endpoints are not publicly reachable and return no configuration, environment, or dependency detail.
- **Error reporting** in the production configuration returns no stack trace and no framework debug page (`25-browser-trust-and-output.md` owns the response content).
- **Admin surfaces** are separately authenticated and network-restricted. An unlinked path is not a control.

# Part 4 - Threat modelling

Produce a table. One row per entry point in inventory column 1:

| Entry point | Who can reach it | Asset reachable | Control that stops abuse | File | Test |

"Who can reach it" is one of: unauthenticated, any authenticated principal, any member of the tenant, a member holding a specific permission, an internal service only. A row whose **control** column is empty is a finding. A row whose **file** column is empty is FAIL / not determined.

Then walk the change against these abuse capabilities. Each is stated as what an attacker can do, not as a vulnerability name, because the name invites recognition while the capability invites checking. For each, answer whether the change **creates**, **widens**, **narrows**, or **does not change** it. "Narrows" and "does not change" are one clause each; "creates" and "widens" become verdict items.

1. A caller with a valid credential for tenant A requests an object belonging to tenant B.
2. A caller holding a low permission invokes a privileged operation, or reaches it through a second entry point that checks less.
3. A caller replays a captured request.
4. A caller replays a captured credential into a different audience, tenant, purpose, or service.
5. A caller supplies a field the schema does not declare, and it reaches a write.
6. A caller supplies a value that reaches a second interpreter - a query, a shell, a template, a deserializer, a parser, a path.
7. A caller supplies the destination of an outbound request.
8. A caller supplies content that another user's browser will render.
9. A caller issues the same request thousands of times, or twice concurrently.
10. A caller makes one of the service's dependencies fail, and observes whether a control was skipped.
11. An internal component is compromised: enumerate what it can reach that it does not need, and what its credentials permit beyond their purpose.
12. An operator or support user acts on a tenant's data: enumerate what record exists of who did what, to whom, and why.

## Trust boundary and data flow map

List the components the change touches, the boundaries between them, and for each boundary: what it verifies, what it strips from inbound data, and what it forwards. **A boundary that forwards more than it verified is a finding**, and so is a boundary whose strip list the review cannot find in configuration or code.

Mark, per boundary, which side is responsible for each control, so that no control is assumed by both sides and therefore implemented by neither. That assumption is the most common way a two-component system ends up with no check at all.

# Part 5 - What Deep Review adds to the report

Beyond the output contract in `SKILL.md`:

- The threat table and the trust-boundary map are included.
- Each P0 carries a reproduction: the actor, the exact request, and the observed result. Where the reproduction could not be run, the item stays P0 and is marked `reproduction not run` with the reason - the severity comes from the code path, not from whether a test harness was available.
- Each hardening item that the change does not create but the review found nearby is reported at its own severity and attributed to the existing code, not to the change under review, so the change's own verdict stays readable.
