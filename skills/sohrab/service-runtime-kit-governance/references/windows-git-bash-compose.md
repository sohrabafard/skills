# Windows Git Bash And Docker Compose Env Conversion

Use this reference when local Docker Compose behavior differs between native PowerShell and Windows Git Bash, especially for slash-valued environment variables.

## Problem pattern

Git Bash/MSYS can path-convert values that look like Unix paths before invoking native Windows binaries such as `docker.exe`.

For runtime-kit services, the risky values are usually intentional slash-valued env vars, for example:

- `RABBITMQ_VHOST=/`
- generated fallbacks derived from `RABBITMQ_VHOST_DEFAULT=/`

If the vhost works from PowerShell but fails from Git Bash, suspect shell conversion before changing Laravel queue configuration.

## First checks

1. Re-render and validate runtime outputs from the service repo.
2. Inspect rendered Compose config for the RabbitMQ env values.
3. Compare launching through native PowerShell versus Git Bash.
4. Inspect the in-container environment, not only `.env`.
5. Confirm whether the failure is authentication/vhost related or queue-provisioning related.

## Preferred fixes

- Prefer native PowerShell for local `docker compose` commands on Windows when path conversion is suspect.
- If Git Bash must be used, scope conversion disabling to the affected command:

```bash
MSYS_NO_PATHCONV=1 bash scripts/docker/up-local.sh prod
```

or:

```bash
MSYS2_ARG_CONV_EXCL='*' bash scripts/docker/up-local.sh prod
```

Use the form that matches the current wrapper and shell behavior. Do not make a global shell-profile change unless the user asks for a persistent developer-machine setting.

## Ownership rule

Do not fix this by changing `config/queue.php`, queue driver code, or generated Docker files by hand. If a shared wrapper must guard against this for every service, fix `service-runtime-kit` and regenerate service outputs.

## Validation

After the fix, verify:

- rendered Compose config still contains the intended vhost
- container env contains the intended vhost
- RabbitMQ queue bootstrap can provision queues
- the Laravel worker connects without changing app queue semantics
