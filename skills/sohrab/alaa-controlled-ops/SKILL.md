---
name: alaa-controlled-ops
description: "Ownership boundary and release governance for the `alaa/controlled-ops` Composer package (ControlledOps) and the services that adopt it. Use when deciding whether a behaviour is package-owned or adopter-owned, releasing or semver-tagging the package, publishing it to Ala Satis, verifying a Composer lock or Satis dist source, moving an adopter service onto a new tag, specifying dry-run canonical hashes or payload fingerprints, handling a reviewed-hash mismatch, classifying replay versus conflict, or validating the ControlledOps write boundary and ControlledOps route/Postman parity. Do not use it for generic queue, docs, Postman, or Laravel work that has no ControlledOps surface. Route general idempotency-store, retry, timeout, and backoff design to /alaa-reliability-sla ($alaa-reliability-sla), and the design of an approval workflow inside a service to /alaa-services-contract ($alaa-services-contract)."
---

# Alaa ControlledOps

You arbitrate which repository owns a behaviour, and you gate every publishing action. You do not implement the adopter service's approval workflow.

## When to use

Identify the target by repository identity, never by a filesystem path:

- **the package** — the working tree whose `composer.json` declares `"name": "alaa/controlled-ops"`
- **an adopter** — a service whose `composer.json` requires `alaa/controlled-ops`
- **cross-repo release work** — cutting a package tag, publishing it, or moving an adopter onto it

Also for dry-run hash, payload fingerprint, reviewed-hash, replay-or-conflict, write-boundary, and ControlledOps route or Postman parity questions in either repository.

## When NOT to use

Beyond the negatives in the description: do not use it for approval-workflow design in a product that does not depend on `alaa/controlled-ops`, nor for domain feature work in an adopter where no ControlledOps contract, digest, or package version is touched.

## Quick start

1. Read the active repository's `AGENTS.md`.
2. Classify the target as package, adopter, or cross-repo release work, and state that classification before editing anything.
3. Establish current behaviour from the active repository under the ranking in `references/10-source-priority-and-boundaries.md` before using any route count, permission ID, package version, or phase name from elsewhere.
4. Read only the reference matching the class.
5. Close on `references/40-validation-and-release-gates.md`. A gate you did not run is reported as not run, never as passed.

## Non-negotiables

- Package availability does not create service runtime behavior. A service must implement and validate its own routes, requests, resources, locks, transactions, workers, and outbox behavior.
- Every claim about dry-run, approval, execution, retry, cancellation, or recovery behaviour names the file and symbol it was read from, or is reported as unverified.
- Never publish a ControlledOps package release, push a release tag, push package code as part of a release, run the Satis build, or perform the consuming-service release adoption step without explicit user approval, unless the user explicitly said approval is not required or that publishing is authorized in the current request.

## References

- `10-source-priority-and-boundaries.md` — before any ownership or contract claim.
- `20-package-service-adoption.md` — releasing the package, or moving an adopter onto a tag.
- `30-lifecycle-idempotency-validation.md` — canonical hashing, reviewed-hash comparison, replay versus conflict.
- `40-validation-and-release-gates.md` — before closing package or adopter work.
- `90-source-map.md` — source freshness, and the skills owning surfaces this one does not.
