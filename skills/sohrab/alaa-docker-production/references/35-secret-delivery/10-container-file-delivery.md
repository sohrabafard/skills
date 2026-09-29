# Container file delivery

## 1. Why `environment:` is not secret delivery

When deciding whether runtime credentials must use file mounts, use [Secret delivery modes](./10-container-file-delivery/10-delivery-modes.md).

## 2. The two modes, and which applies

When deciding whether runtime credentials must use file mounts, use [Secret delivery modes](./10-container-file-delivery/10-delivery-modes.md).

## 3. The `_FILE` convention

When implementing or auditing the container entrypoint file contract, use [The `_FILE` convention](./10-container-file-delivery/20-file-convention.md).

## 4. Compose: file-backed secrets

When declaring file-backed secrets in Compose, use [Compose file-backed secrets](./10-container-file-delivery/30-compose-file-secrets.md).
