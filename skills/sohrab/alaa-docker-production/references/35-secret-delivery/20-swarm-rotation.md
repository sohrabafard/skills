# 20 Swarm Rotation

When declaring, rotating, or retiring a Swarm external secret, read this procedure.

## 5. Swarm: external secrets

```yaml
services:
  platform-app-php:
    secrets:
      - source: comment_app_key_v3
        target: app_key
        uid: "1000"
        gid: "1000"
        mode: 0400

secrets:
  comment_app_key_v3:
    external: true
```

- `external: true` means the secret already exists in the swarm and this file only references it.
  A `file:`-backed secret in a stack file reads the file from the manager node where the deploy runs,
  which makes the deploy depend on which machine ran it.
- `uid`, `gid` and `mode` are supported unconditionally by Swarm. They are absent from every secret
  the generator emits (`render-runtime.sh:1177` writes `source`/`target` only), so every secret in
  the fleet's Swarm stacks currently lands at `0444`. The container-side defence at
  `entrypoint.sh:51-57`, which `chmod 600`s the Passport keys, cannot help: a secret mount is
  read-only and `chmod` on it fails.
- Naming: `<service>_<purpose>_v<n>`. The version suffix is not decoration; see [rotation](#6-rotation-is-a-create-new-name-operation).

## 6. Rotation is a create-new-name operation

A Docker secret is immutable. `docker secret update` exists but changes only labels, not content.
Rotation is therefore:

```
# 1. create the new secret under a new name
printf '%s' "$NEW_VALUE" | docker secret create comment_app_key_v4 -

# 2. update the stack file: source: comment_app_key_v4, target unchanged
#    the target stays `app_key`, so no application code or env var changes

# 3. deploy, which is an ordinary rolling update
docker stack deploy -c docker-compose.swarm.yml --with-registry-auth comment

# 4. confirm no task references the old secret, then remove it
docker service inspect --format '{{range .Spec.TaskTemplate.ContainerSpec.Secrets}}{{.SecretName}} {{end}}' comment_platform-app-php
docker secret rm comment_app_key_v3
```

Two consequences worth stating because they are counter-intuitive:

- **Rotation is a deploy.** There is no way to change a secret's value under a running task. Plan it
  as a rollout, with the rollout control from this skill's `references/30-swarm-delivery.md`.
- **`APP_KEY` is not rotatable this way.** Changing a Laravel `APP_KEY` makes every value encrypted
  under the old key unreadable. Rotating it requires a re-encryption step in the application first,
  with both keys available. That is an application change, not a container change; the container
  side is only the last step.

Never rotate by editing the file a `file:`-backed secret points at while the stack is running: the
task keeps the content it was created with, so half the tasks hold the old value and half the new,
and which is which depends on when each task last restarted.
