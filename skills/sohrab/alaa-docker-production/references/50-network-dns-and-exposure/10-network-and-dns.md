# 10 Network And Dns

When connecting service families or resolving an HTTP backend by stable service DNS, read this reference.

## 1. One shared network per family

When services in different repositories must reach each other, they share one external Docker
network whose name is a fleet constant, and each project attaches to it rather than creating its own.

```yaml
networks:
  shared:
    external: true
    name: ${DOCKER_SHARED_NETWORK_NAME:-alaa-shared-network}
```

`external: true` means "this network already exists; do not create it and do not delete it on
`down`". That is what keeps one service's `docker compose down` from disconnecting every other
service on the host.

The network is created once, idempotently, by the delivery wrapper:

```sh
docker network inspect "${network}" >/dev/null 2>&1 \
  || docker network create --driver bridge --attachable "${network}"
```

For Swarm the driver is `overlay` and the network must be `--attachable` if any non-service
container has to join it.

The same rule applies to shared infrastructure: one PostgreSQL, one Redis, one RabbitMQ per host,
reused by every service in the family, with per-service databases, schemas, users and grants inside
them. Sharing the server is an operational decision; sharing a database is not, and the separation
of databases, users and grants stays even when the server is shared. Schema and grant design is
`/alaa-data-layer`'s subject; the container identity is this skill's.

The concrete fleet names — `alaa-shared-network`, `alaa-shared-infra` — and the canonical alias
values are `/alaa-services-contract`'s register. This skill states the
shape and the stability rule; that skill states the values.

## 2. Stable DNS: one name per HTTP backend

Every service on a Docker network resolves by its service key. In addition, a service may declare
aliases:

```yaml
    networks:
      shared:
        aliases:
          - ${DOCKER_PROJECT_NAME:-comment}-platform-app-php
          - comment
```

Rules:

- **The canonical alias belongs to the HTTP-serving service key, never to a worker or a scheduler.**
  In this fleet that key is `platform-app-php` and the alias pattern is
  `<service>-platform-app-php`. A worker holding the alias means a proxy can route a request to a
  process with no listener, and the failure is a connection refused that looks like the application
  is down.
- **Proxies and upstream callers address the alias, never a container instance name, a task ID, a
  replica name or a node IP list.** Instance names change on every recreate; task IDs change on
  every rollout; a node IP list is stale the moment a node is replaced. A configuration that names
  any of them breaks silently at the next deploy, and the symptom is a proxy sending traffic to a
  container that no longer exists.
- One alias per role. A second alias for the same role is a second name to keep in sync, and the two
  diverge.

In Swarm the same property comes from the routing mesh: the service name resolves to a virtual IP
that load-balances across tasks. `endpoint_mode: vip` is the default and is correct for HTTP; when
`dnsrr` is right instead is in this skill's `references/30-swarm-delivery.md` §6.

How a proxy is configured to use the alias — the backend stanza, health checks at the proxy layer,
retry behaviour — is `/alaa-haproxy`'s ground, and any Lua in that configuration
is `/alaa-haproxy-lua`'s. This skill states which name the proxy must be
pointed at.
