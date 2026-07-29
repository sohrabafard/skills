# Deploy Failure Playbook

Open this file when something is wrong right now. Find the symptom, run the diagnosis, apply the smallest retry, escalate if it does not hold. This is not a procedure to run top to bottom.

**First command, every time:** fetch `build-info.json` from the failing deployment and record the `commit` and `builtAt` it reports. Every diagnosis below assumes you know which build is actually serving. If that fetch 404s, the deployment predates provenance and your first fix is `references/25-artifact-identity-and-provenance.md`.

---

## Symptom: the app shell loads, then chunks return 404

**Diagnosis.** Fetch the served HTML and extract one failing asset URL. Compare three things: the URL's path prefix against `build.publicPath`; the URL's filename against the files present at the serving origin; and the `commit` in `build-info.json` against the commit you expected. Exactly one of three causes will match.

- Prefix differs → the base changed without the HTML being rebuilt, or a proxy rewrite is stripping or duplicating the prefix.
- Prefix matches, filename absent at the origin → stale HTML on dead hashes. Go to the next symptom.
- Both match and it still 404s → the origin is serving from a bucket the deploy did not populate.

**Smallest retry.** Re-request the same URL directly against the origin, bypassing the edge. If it succeeds there, the fault is at the edge and the finding goes to `/alaa-haproxy` (`$alaa-haproxy`) with the two responses attached.

**Escalation.** If the prefix is wrong in the emitted HTML, this is a build defect: revert the `publicPath` change and rebuild. Do not patch it at the proxy; that makes the artifact and the serving layer disagree permanently.

---

## Symptom: `index.html` references hashed assets that no longer exist

This is the most common frontend deploy failure and it has two distinct causes that need opposite fixes.

**Diagnosis.** Compare `build-info.json`'s `commit` against the commit of the assets present at the origin.

- HTML is *newer* than the assets → the asset upload did not complete, or it completed after the HTML was swapped. Ordering defect.
- HTML is *older* than the assets → a cache is holding an `index.html` from the previous release, or a service worker is serving a precached one. Retention defect.

**Smallest retry.** For the ordering defect, re-run the asset publish job alone and re-request one failing asset. For the retention defect, request `index.html` with a cache-busting query and compare the asset URLs in the two responses; if they differ, the HTML was cached against the policy in `references/30-serving-caching-and-public-path.md`.

**Escalation.** Ordering: the publish sequence must upload assets before swapping HTML, and this belongs in the pipeline as a `needs:` ordering — state the obligation and route the expression to `/alaa-gitlab-ci-cd` (`$alaa-gitlab-ci-cd`). Retention: the previous release's hashed assets must remain at the origin until no served HTML references them; if a lifecycle rule deleted them, that rule is wrong and the finding goes to `/alaa-minio-object-storage` (`$alaa-minio-object-storage`) or `/alaa-arvan-object-storage` (`$alaa-arvan-object-storage`).

---

## Symptom: the deploy succeeded for some users and failed for others

**Diagnosis.** A half-propagated origin or edge. Request the same asset URL from at least two edge locations or with a cache-bypass header, and compare. Then check whether the failing responses correlate with a single edge node or with users who loaded the page before the swap.

**Smallest retry.** Do not invalidate everything. Invalidate only the documents whose policy is `no-cache` — `index.html`, the service worker, the precache manifest, `build-info.json` — because the hashed assets are immutable and invalidating them achieves nothing while creating a thundering herd against the origin.

**Escalation.** If propagation does not converge within the CDN's stated window, roll back rather than wait. A partially-propagated release is serving two incompatible versions to one user population, which is worse than serving the previous version to all of them.

---

## Symptom: the service worker serves the previous asset base after a deploy

**Diagnosis.** Request the service worker script and read its precache manifest. If it lists the previous release's URLs, the manifest was not regenerated with the new base, or the script itself was cached.

**Smallest retry.** Confirm the service worker script is served `no-cache`. If it is, the manifest is stale in the artifact and the build is at fault, not the serving layer.

**Escalation.** Manifest generation, the update flow, and how an installed worker is superseded belong to `/alaa-quasar-app-vite-v3` (`$alaa-quasar-app-vite-v3`), `references/32-pwa-injectmanifest-guard.md`. Note that this class is not fully recoverable by rollback: workers already installed in users' browsers persist until their own update cycle runs. It is the standing example of an irreversible line in `references/40-verification-and-rollback.md`.

---

## Symptom: two pipelines published at once and the output is inconsistent

**Diagnosis.** Compare `builtAt` in the served `build-info.json` against the pipeline that you believe deployed. If they disagree, or if assets from two commits are both present and the HTML references a mixture, two publishes interleaved.

**Smallest retry.** Re-run the later pipeline's publish job alone, with the exclusive resource held, so one complete build's assets and HTML land together.

**Escalation.** Gate 9 in `references/20-ci-gates-and-predicates.md` was absent or not applied to the publishing job. Add it; the mechanism is `/alaa-gitlab-ci-cd` (`$alaa-gitlab-ci-cd`)'s to express.

---

## Symptom: the runtime container will not start after a configuration change

**Diagnosis.** Read the exit message. A Compose file following the invariant in `references/15-build-time-vs-runtime-config.md` names the missing variable in its own error text. If the container starts but behaves as though a control is off, a `:-default` was written where `:?` was required.

**Smallest retry.** Run the interpolation check: render the Compose configuration with the current environment and confirm the variable resolved to the value you intended, not to a default.

**Escalation.** If the variable is set in a service-level `env_file:` and the Compose file interpolates it, the file is wrong by construction — interpolation never reads that key. Fix the source of the value; the Compose file's authorship is `/alaa-docker-production` (`$alaa-docker-production`)'s.

---

## When to stop diagnosing and roll back

Roll back, using the four lines recorded in `references/40-verification-and-rollback.md`, as soon as any of these is true: the failure affects users who did not have it before this deploy and the cause is not identified within the incident's stated response window; the failure is a leaked secret in a bundle (rotate first, per `references/35-client-bundle-security.md`); or the smallest retry above has been attempted twice with the same result.

Diagnosing a live failure longer than that trades user-visible breakage for your own certainty. The previous artifact is known-good and is one command away.
