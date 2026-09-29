Version-sensitive claims in this topic depend on [Jitsi source map](../90-source-map.md).

## Debian or VM installs

This is often the cleanest route to production Jitsi where the organisation can run virtual machines or bare metal:
it aligns with the upstream operations model, separates web, signalling, bridge, TURN and recording roles without
abstraction, and gives direct control over UDP, host networking and bridge placement.

Choose it when the product needs multiple bridges, when infrastructure can manage TLS, DNS and host firewalling,
or when predictable public addressing matters.
## Docker Compose

Use Compose when packaging simplicity matters more than platform abstraction: proof of concept, integration
development, internal pilot, and controlled production with a stated concurrency limit.

- Use the official self-hosting bundle and its documented password-generation workflow rather than ad hoc secrets.
- Keep environment values explicit and version-controlled through the secure configuration process; the signing
  key is not one of them — see `references/10-architecture-and-jwt-trust.md`.
- Set advertised addresses correctly when hosts sit behind NAT, because a wrong advertised address produces exactly
  the symptom in class 6 of `references/20-failure-classes.md`.
- Use a dedicated subdomain. Do not design around subdirectory hosting.

**Do not present a single Compose node as a credible answer to a high-availability commitment.** One node carrying
a timetable means one restart cancels the school day.
## Docker Swarm

Be conservative. Swarm can work where the organisation already operates it well, where node placement and public
exposure are tightly controlled, and where the team understands that media traffic is not ordinary stateless web
traffic. Bridge UDP exposure and placement need deliberate design, and rolling updates disrupt media when bridge
identity and placement are not handled explicitly.

Do not choose Swarm because it looks more clustered than Compose. Choose it because the organisation already runs
it, or do not choose it.
