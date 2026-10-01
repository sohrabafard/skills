# Caching, Routing and Rewrites

This file writes directives. **It decides no policy.** The boundary sentence is stated once, in
`SKILL.md`. What follows is how each policy value becomes a line of HAProxy config, and what goes
wrong when it is written the obvious way.

The four obligations this skill owes `/alaa-frontend-devops`,
`alaa-frontend-devops references/30-serving-caching-and-public-path.md`, each answered below:
the asset prefix reaches the origin unchanged; HTML is not stored under the immutable policy;
compression does not alter the bytes that Subresource Integrity covers; a hard refresh on a deep
link returns the same document as a client-side navigation.

`20-static-asset-cache-and-rewrite.cfg` is the worked artifact for all four.

## When no policy has been given

When caching policy is missing, read [Policy prerequisites](50-caching-routing-and-rewrites/10-policy-boundary.md) for the mandatory owner handoff and stop condition.

## Emitting `Cache-Control`

When expressing an agreed response policy, read [Cache-Control emission](50-caching-routing-and-rewrites/20-cache-control.md) for immutable/HTML directives and request-to-response classification.

## HAProxy's own cache

When adding an in-process cache, read [Response cache](50-caching-routing-and-rewrites/30-response-cache.md) for eligibility, memory/object limits, cache-use/cache-store and inspection.

## Compression

When enabling HTTP compression, read [Compression](50-caching-routing-and-rewrites/40-compression.md) for build providers, MIME types, explicit filters and cache ordering.

## Path rewrites

When rewriting a path or adding a deep-link fallback, read [Rewrites and fallback](50-caching-routing-and-rewrites/50-rewrites-and-fallback.md) for strip/add-prefix directives and policy boundaries.

## Selecting a backend

When selecting an origin, read [Backend selection](50-caching-routing-and-rewrites/60-backend-selection.md) for ACL/map selection syntax, policy owners and example choice.
