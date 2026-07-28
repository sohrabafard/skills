# Provenance Ledger

Read this before repeating any claim about Jitsi behaviour, a configuration key, a release, a capability or a
support tier.

Every upstream fact this skill relies on has a row below. A sentence in a deliverable that depends on a row is
allowed only after that row has been read within its freshness window. A fact with no row is not a fact this skill
has; go and read the source, then add the row.

## The freshness rule

- **A row whose read date is more than 90 days old is re-read against the source and against the release the
  deployment actually runs, before any sentence depending on it enters a deliverable.** Ninety days is roughly the
  interval at which this project's own releases have moved enough to invalidate a configuration or packaging claim,
  and a stale fact is more dangerous than a missing one because it reads as authoritative.
- A row marked `unverified as of 2026-07-27` was never read by this skill's author. Its clock has not started, so
  the 90-day rule does not soften it: read the source before first use, then record the real date.
- When you refresh a row, replace the assertion, the release tag and the read date **in one edit**. Never update the
  date without re-reading; a refreshed date on an unchanged fact is a false claim that someone verified it.
- Record the release tag the fact applies to, not just the source URL. Jitsi behaviour moves per release, and a
  handbook page describes whatever release it was written against.

**This ledger could not be refreshed in the session that created it.** That session had no network access to Jitsi
upstream documentation, which is why most rows below carry `unverified as of 2026-07-27` rather than a read date.
The three dated rows carry their real, and now expired, dates.

## The ledger

| # | Fact class | What this skill asserts | Source | Applies to release | Read | Status |
|---|---|---|---|---|---|---|
| 1 | container release snapshot | `jitsi/docker-jitsi-meet` latest release was `stable-10888`, published 2026-03-30 | https://github.com/jitsi/docker-jitsi-meet/releases | `stable-10888` | 2026-04-24 | expired 2026-07-23 |
| 2 | handbook currency | the handbook releases page was updated 2026-04-11 | https://jitsi.github.io/handbook/docs/releases | unpinned | 2026-04-24 | expired 2026-07-23 |
| 3 | IFrame API page currency | the IFrame API page was updated 2026-04-16 | https://jitsi.github.io/handbook/docs/dev-guide/dev-guide-iframe | unpinned | 2026-04-24 | expired 2026-07-23 |
| 4 | token claim names | `iss`, `aud`, `sub`, `room`, `exp`, `nbf`, `iat` and the `context.*` object are the claims the verifier reads | https://github.com/jitsi/lib-jitsi-meet/blob/master/doc/tokens.md | unpinned | unverified as of 2026-07-27 | read before first use |
| 5 | verifier algorithms | which signature algorithms the Prosody token verifier accepts, and how a public key is supplied to it | token authentication handbook page and `lib-jitsi-meet` token docs | unpinned | unverified as of 2026-07-27 | read before choosing an algorithm |
| 6 | reconnect re-validation | whether the token is re-validated when a client reconnects to a conference it is already part of | upstream source; not documented in the handbook pages this skill cites | unpinned | unverified as of 2026-07-27 | **read before any incident report asserts it** |
| 7 | guest domain and anonymous auth | the configuration keys that disable anonymous authentication and lock the guest domain | https://jitsi.github.io/handbook/docs/devops-guide/secure-domain | unpinned | unverified as of 2026-07-27 | read before writing configuration |
| 8 | room-name handling | whether the deployment normalises or case-folds a room name before matching it against the `room` claim | upstream source | unpinned | unverified as of 2026-07-27 | read before choosing an alphabet |
| 9 | bridge failure recovery | whether Jicofo re-invites participants onto a healthy bridge automatically, and how long that takes | https://jitsi.github.io/handbook/docs/architecture/ and Jicofo source | unpinned | unverified as of 2026-07-27 | read before quoting a recovery time |
| 10 | recording concurrency | one Jibri worker handles one active recording or stream at a time | https://github.com/jitsi/jibri | unpinned | unverified as of 2026-07-27 | read before sizing the worker pool |
| 11 | IFrame API surface | the command, event and function names listed in `references/50-events-recording-governance.md` and `references/40-embedding-contract.md` | https://jitsi.github.io/handbook/docs/dev-guide/dev-guide-iframe-commands | unpinned | unverified as of 2026-07-27 | read before relying on a name |
| 12 | embed-time override limits | which configuration keys can be overridden at embed time, and that host and moderator semantics cannot | https://jitsi.github.io/handbook/docs/dev-guide/dev-guide-configuration | unpinned | unverified as of 2026-07-27 | read before promising an override |
| 13 | reservation system | whether an external reservation service is supported, and its request and response contract | reservation-system handbook material | unpinned | unverified as of 2026-07-27 | read before designing on it |
| 14 | Helm chart capability | that bridge scaling, OCTO and exposure modes in the community chart are community-supported and partly under-tested | https://github.com/jitsi-contrib/jitsi-helm | unpinned | unverified as of 2026-07-27 | read before proposing the chart |
| 15 | restricted-platform support | rootless execution and OpenShift restricted-policy compatibility across all Jitsi containers | upstream issues and `jitsi-contrib` material | unpinned | unverified as of 2026-07-27 | read before promising either |
| 16 | bridge websockets and proxying | what the deployment requires of a reverse proxy for bridge websocket paths | handbook FAQ and proxy material | unpinned | unverified as of 2026-07-27 | read before writing an edge configuration |
| 17 | node sizing examples | the published starting sizes quoted in `references/60-scale-and-capacity.md` | https://jitsi.github.io/handbook/docs/devops-guide/devops-guide-requirements | unpinned | unverified as of 2026-07-27 | read before quoting a size |

## Source priority

Use sources in this order unless the task requires something narrower:

1. the Jitsi handbook, architecture and devops pages;
2. upstream Jitsi repositories and the documentation inside them;
3. the official IFrame API, configuration and token-authentication pages;
4. the official container self-hosting guide and its release notes;
5. `jitsi-contrib` for Helm and Kubernetes material;
6. community issues, pull requests, forum threads and blog posts, for pitfalls only.

`jitsi-contrib` is community-supported and is not the same support tier as the core handbook. Say which tier a
claim comes from whenever the claim decides a deployment.

## Where to start reading, by task

- **Components, scaling and media path:** the architecture handbook, the `jitsi-meet` repository, the
  `jitsi-videobridge` repository.
- **Concurrency, multi-bridge, bridge websockets, node separation:** the scalable devops guide and the requirements
  page. The current scalable guide states that some older scaling tutorials are outdated — use it in place of any
  blog post or video.
- **Tokens, guest access, moderator rules:** the token-authentication handbook page and `lib-jitsi-meet`
  `doc/tokens.md`.
- **Branding, feature flags, embedding:** the configuration guide and the IFrame API pages.
- **Recording and streaming:** the Jibri repository and the handbook sections that mention it.
- **Packaging and self-hosting:** the container self-hosting guide, the container release notes, and the community
  Helm repository.

## Using community sources

Good uses: discovering rootless and Podman friction, chart limitations not yet in the handbook, cluster and CNI
quirks, and upgrade breakages.

Bad uses: making a supportability claim from a single issue, treating an unmerged pull request as product support,
and inferring a scale limit from one anecdote. None of those produces a row in this ledger.

## Claims that need a fresh read every time

These have been wrong often enough that a cached answer is not worth having:

- full rootless support across all Jitsi containers;
- OpenShift compatibility under the strictest restricted policies;
- multiple bridges behind a single public UDP endpoint on Kubernetes;
- one moderator-role semantics that holds across packages and authentication modes;
- 99.99% availability from a single cluster namespace or a single public address;
- server-side webhooks as a universal built-in Jitsi feature.
