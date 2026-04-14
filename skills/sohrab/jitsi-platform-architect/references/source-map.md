# Source Map

## Table of contents

- Source priority
- Official docs to read first
- Community and pitfall sources
- Freshness and version checks
- Claims that need extra caution

## Source priority

Use sources in this order unless the task clearly requires something narrower:

1. Jitsi Handbook architecture and DevOps pages
2. Upstream Jitsi GitHub repositories and docs in those repos
3. Official IFrame API, config, and token-auth docs
4. Official Docker self-hosting docs and release notes
5. `jitsi-contrib` docs for Helm and Kubernetes-specific guidance
6. Community issues, PRs, forum threads, and blog posts only for pitfalls or gaps

Treat `jitsi-contrib` as community-supported, not as the same support tier as the core Jitsi handbook.

## Official docs to read first

### 1. Core architecture

Read first when the task touches components, scaling, or media path design.

- Jitsi architecture handbook
- `jitsi-meet` repository
- `jitsi-videobridge` repository

### 2. Scalable production setups

Read when the task touches concurrency, multi-bridge, fleet topology, bridge websockets, or node separation.

- Scalable Jitsi DevOps guide
- Handbook requirements page
- FAQ material around bridge websockets and reverse-proxy caveats

Important: the current scalable guide explicitly says some older scaling tutorials are outdated. Prefer the current handbook over older blog posts or videos.

### 3. Auth, room admission, and identity mapping

Read when the task involves JWTs, guest access, moderator rules, or platform-owned authorization.

- Token authentication handbook page
- `lib-jitsi-meet/doc/tokens.md`
- Optional reservation-system docs if room creation is externally controlled

### 4. Client behavior and product customization

Read when the task involves branding, feature flags, meeting UX, or embedding.

- Jitsi configuration guide
- IFrame API constructor docs
- IFrame API commands, functions, and events docs

### 5. Recording, streaming, and media workers

Read when the task involves recording, livestreaming, replay libraries, or capacity planning.

- Jibri README
- Architecture handbook sections mentioning Jibri

### 6. Self-hosting and packaging

Read when the task involves packaging choice or environment fit.

- Official Docker self-hosting guide
- Docker Jitsi Meet release notes
- Community Helm docs in `jitsi-contrib/jitsi-helm`

## Community and pitfall sources

Use community material only to discover sharp edges, not to replace upstream guidance.

Good use of community sources:

- rootless and Podman friction
- Helm chart limitations not yet reflected in handbook docs
- OpenShift or CNI quirks
- upgrade breakages and migration gotchas

Bad use of community sources:

- making supportability claims from a single issue
- treating an unmerged PR as product support
- inferring scale limits from one anecdote

## Freshness and version checks

Re-check current upstream docs before asserting any of the following:

- current stable release names or tags
- current config keys or deprecated options
- whether a capability is official or community-only
- Helm chart behavior for JVB scaling, OCTO, or exposure modes
- whether a specific deployment path is still recommended

When the task depends on exact current behavior, prefer the doc page or release page that was updated most recently.

## Claims that need extra caution

Be cautious with these claims unless you have just re-verified them:

- full rootless support across all Jitsi containers
- OpenShift compatibility under the strictest restricted policies
- multi-JVB on Kubernetes behind a single public UDP endpoint
- one-size-fits-all moderator role semantics across packages and auth modes
- 99.99% availability from a single cluster namespace or a single public IP
- server-side webhooks as a universal built-in Jitsi feature
