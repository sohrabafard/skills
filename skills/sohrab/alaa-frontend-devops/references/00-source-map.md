# Source Map

This file is the source-provenance ledger for this skill, not a router. The router is `references/00-topic-map.md`.

Open this file before asserting a version, a security posture, or a claim about current tool behaviour that this skill does not already state.

## Source priority

Consult in this order and stop at the first that answers the question.

1. Repo-local artifacts, because they are the only evidence of what this repository actually does: `package.json` (`engines`, `packageManager`, `scripts`), the lockfile, `quasar.config.*`, the CI file, the Dockerfile, the Compose file, and the emitted build tree itself.
2. The in-fleet owner of the subject. Platform expression questions do not go to vendor documentation first; they go to the owning skill, which already carries the fleet's ruling. The full list with file paths is `references/90-companion-boundary.md`.
3. Official upstream documentation for the tool that emits or serves the artifact:
   - Quasar CLI with Vite: https://quasar.dev/quasar-cli-vite/
   - Vite: https://vite.dev/
   - Node.js release schedule: https://nodejs.org/en/about/previous-releases
   - Compose variable interpolation: https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/
   - Subresource Integrity: https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity
   - Content Security Policy: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy
4. Official release notes and registry metadata when upstream prose is ambiguous about a version boundary.
5. Community posts, issue comments, and answers, as candidate failure modes to reproduce locally. Never as the source of a rule.

## Freshness triggers

Re-verify against sources 1 to 3 before changing advice when the task contains any of: "latest", "current", "upgrade", "migration", "security", "CVE", "breaking change", "release", a Node or Vite or Quasar version bump, a change to cache behaviour or asset base or service-worker update flow, a base-image change, a lockfile change, or a production-only failure that did not reproduce in staging.

## Recording a claim

Every version-sensitive or behaviour-sensitive claim written into this skill carries a `read: <ISO date>` marker on the same line, and a source URL where one exists. A claim that could not be verified ships as `read: unverified as of <ISO date>` and stays in the file. Deleting an unverified claim removes the record that it was ever asked; keep it and mark it.

"Not documented" means searched in sources 1 to 3 and not found. It is not proof that the behaviour is absent.

## Community-evidence boundary

Acceptable: using a forum thread to identify a proxy timeout symptom, a CDN invalidation mistake, or a package-manager edge case, then reproducing it locally and writing the rule from the reproduction.

Not acceptable: changing a Node or Quasar support statement from a forum answer; copying a Dockerfile or proxy workaround without the owning skill's ruling; treating one issue comment as proof of current behaviour.

## Anti-pattern

Disabling caching everywhere to make missing chunks go away. That hides an artifact-contract defect and makes the next release harder to diagnose. Run `scripts/verify-artifact-contract.mjs` against the emitted tree first; it tells you whether the HTML points at assets that exist.
