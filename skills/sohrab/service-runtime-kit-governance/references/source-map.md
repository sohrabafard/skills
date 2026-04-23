# Source Map

Use this map when runtime-kit behavior, generated Docker runtime files, Compose/Swarm semantics, or current local runtime behavior may have changed.

## Source order

1. Repository truth:
   - service repo runtime inputs under `runtime/`, copied wrappers under `scripts/runtime/`, generated outputs, `.env.example`, local `AGENTS.md`, and observed bootstrap logs.
2. Shared kit truth:
   - sibling `../service-runtime-kit` source, renderer templates, validation scripts, release notes, and the kit pin/fetch config in `runtime/runtime-kit.env`.
   - If a service uses a repo-local `.service-runtime-kit` cache, verify whether it is stale before trusting it.
3. Official runtime sources:
   - Docker Compose docs: https://docs.docker.com/compose/
   - Docker Swarm docs: https://docs.docker.com/engine/swarm/
   - Docker secrets docs: https://docs.docker.com/engine/swarm/secrets/
   - Postgres Docker image: https://hub.docker.com/_/postgres
   - RabbitMQ Docker image: https://hub.docker.com/_/rabbitmq
   - Redis Docker image: https://hub.docker.com/_/redis
   - Laravel deployment docs: https://laravel.com/docs/13.x/deployment
4. Companion skills:
   - `alaa-docker-production` for image/runtime hardening.
   - `alaa-laravel-job-rabbitmq` for Laravel RabbitMQ worker behavior.
   - `alaa-data-layer` for Postgres, PgBouncer, Redis, and data-layer runtime implications.
5. Community posts and StackOverflow answers:
   - Troubleshooting only. Verify any Compose, Swarm, network, volume, or health-check claim against official docs and generated output.

## Freshness triggers

Verify the shared kit, generated output, and official docs before acting when the task mentions:

- `latest`, `current`, `upgrade`, `security`, `CVE`, Docker Compose spec changes, Swarm behavior, secret handling, generated wrappers, stale kit cache, auto-fetch, PgBouncer, RabbitMQ bootstrap, Redis wiring, or helper script refresh.

## Small example

Change service-owned runtime input, then rerender:

```bash
bash scripts/runtime/render-runtime.sh
bash scripts/runtime/validate-runtime.sh
```

Anti-pattern:

```bash
# Editing docker-compose.yml directly as the final fix.
```

Generated runtime outputs can be overwritten on the next render, so direct edits hide the real ownership problem.
