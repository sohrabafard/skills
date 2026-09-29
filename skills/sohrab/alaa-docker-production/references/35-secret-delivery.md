# Secret delivery into a container

Open this file when a credential, key or token must reach a running container.

Which variables count as secrets, and what interpolation form they take when they must appear in a
Compose file at all, is this skill's `references/25-fail-closed-interpolation.md`. Getting a secret
into a *build* is a different mechanism entirely and is this skill's
`references/15-build-secrets-and-attestations.md`. Whether a particular value is a security control
and what threat class it belongs to is `/alaa-security-review`'s decision.

---

## 1. Why `environment:` is not secret delivery

When deciding why credentials should not use container environment variables, read [Secret delivery modes](./35-secret-delivery/10-container-file-delivery/10-delivery-modes.md).

## 2. The two modes, and which applies

When choosing between file delivery modes, read [Secret delivery modes](./35-secret-delivery/10-container-file-delivery/10-delivery-modes.md).

## 3. The `_FILE` convention

When implementing or auditing the `_FILE` entrypoint contract, read [the `_FILE` convention](./35-secret-delivery/10-container-file-delivery/20-file-convention.md).

## 4. Compose: file-backed secrets

When declaring file-backed Compose secrets, read [Compose file-backed secrets](./35-secret-delivery/10-container-file-delivery/30-compose-file-secrets.md).

## 5. Swarm: external secrets

When declaring an external Swarm secret, read [Swarm secret rotation](./35-secret-delivery/20-swarm-rotation.md).

## 6. Rotation is a create-new-name operation

When rotating or retiring a Swarm secret, read [Swarm secret rotation](./35-secret-delivery/20-swarm-rotation.md).

## 7. Key material with two parties

When delivering two-party key material, read [Key material and audit](./35-secret-delivery/30-key-material-and-audit.md).

## 8. What must never appear in `docker inspect`

When auditing `docker inspect` exposure, read [Key material and audit](./35-secret-delivery/30-key-material-and-audit.md).

## 9. Checklist for a secret change

When reviewing a secret change, read [Key material and audit](./35-secret-delivery/30-key-material-and-audit.md).
