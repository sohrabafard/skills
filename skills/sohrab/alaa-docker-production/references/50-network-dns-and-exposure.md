# Networks, DNS and exposure

Open this file on a service-discovery question, a proxy misrouting, or any decision about which
port is reachable from where.

---

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
`/alaa-data-layer` (`$alaa-data-layer`)'s subject; the container identity is this skill's.

The concrete fleet names — `alaa-shared-network`, `alaa-shared-infra` — and the canonical alias
values are `/alaa-services-contract` (`$alaa-services-contract`)'s register. This skill states the
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
retry behaviour — is `/alaa-haproxy` (`$alaa-haproxy`)'s ground, and any Lua in that configuration
is `/alaa-haproxy-lua` (`$alaa-haproxy-lua`)'s. This skill states which name the proxy must be
pointed at.

## 3. Exposure, with a scope

"Publicly exposed" needs a definition or the rule cannot be applied. Four distinct things are called
"exposing a port", and only one of them is a public exposure:

| Form | Reachable from | Verdict |
|---|---|---|
| No `ports:` key at all | the Docker network only | Correct default for anything that only serves other containers |
| `ports: "127.0.0.1:15432:5432"` | the host's loopback only | **Not a public exposure.** Correct for operator access on a single host |
| `ports: "5432:5432"` or `"0.0.0.0:5432:5432"` | every interface on the host, including the public one | A public exposure. Never for a database, broker, cache or admin tool |
| Swarm `ports: {mode: ingress}` | **every node in the swarm**, on every interface | A public exposure. Only for an edge proxy |
| Swarm `ports: {mode: host}` | the interfaces of the node running the task | Node-local; the Swarm counterpart of a loopback publish |
| `expose:` | documentation only; changes nothing | Harmless and informational |

The rule, with the scope the older fleet sentence lacked:

**No database, broker, cache or administrative interface is published on an address other than
`127.0.0.1` in a production-shaped Compose file, and none is published in `ingress` mode in a Swarm
stack file. Only an edge proxy is published on a routable address.**

That makes the fleet's owner-standard host-port table compliant rather than a violation. It
publishes each shared-infra protocol port on `127.0.0.1` with a `1`-prefixed default of its
in-network port — PostgreSQL `15432`, Redis `16379`, RabbitMQ AMQP `15672`, ClickHouse HTTP `18123`
and native `19000` — so every service and host tool finds shared infrastructure in the same place.
The table is `/alaa-services-contract` (`$alaa-services-contract`)'s register; per-host deviations
live only in the untracked service `.env` through the `*_FORWARD_PORT` variables and are reverted
when the conflict goes away.

Containerised services keep using the in-network aliases and never dial the host ports. A container
that connects to `127.0.0.1:15432` is connecting to itself.

Verifying what is actually published:

```
docker compose ps --format '{{.Service}}\t{{.Publishers}}'
ss -ltnp | grep -v '127.0.0.1'          # anything here is reachable off-host
docker service inspect --format '{{json .Endpoint.Ports}}' SERVICE
```

The `ss` line is the check that matters, because it reports the actual listening sockets rather than
the intent expressed in a file.

Swarm's `ingress` mode is the trap: a published port in `ingress` mode is answered by **every** node
in the swarm, not only the node running the task, and there is no address to bind it to. A database
published `mode: ingress` on a swarm whose nodes have public addresses is a public database. Use
`mode: host` when a Swarm service must be reachable node-locally:

```yaml
    ports:
      - target: 5432
        published: 15432
        protocol: tcp
        mode: host
```

## 4. Trust boundaries and forwarded headers

A container behind a proxy must know which headers it may believe. Two facts and one consequence:

- The proxy sets `X-Forwarded-For`, `X-Forwarded-Proto`, `X-Forwarded-Host` and `X-Request-Id`, and
  strips any inbound copy of them, so a client cannot forge them.
- The application trusts those headers only when the connection came from the proxy. In Laravel that
  is `TRUSTED_PROXIES`; a wildcard makes every client-supplied `X-Forwarded-For` authoritative,
  which is why `TRUSTED_PROXIES` is a class-B register member in this skill's
  `references/25-fail-closed-interpolation.md`.
- `traceparent` is propagated, not trusted for authorisation. It is a correlation identifier and a
  client can set it to anything.

Which headers exist, what each is named and which values are canonical is
`/alaa-services-contract` (`$alaa-services-contract`)'s register. Where the trust boundary sits, and
what an attacker gains by crossing it, is `/alaa-security-review` (`$alaa-security-review`)'s
decision. This skill states that the boundary must be expressed in the container's configuration
rather than assumed, and that the value expressing it must fail closed.

Authentication and authorisation at the gateway are `/alaa-trust-gateway-auth`
(`$alaa-trust-gateway-auth`)'s ground.

## 5. Diagnosing discovery and routing

```
docker compose exec platform-app-php getent hosts comment-pgbouncer
docker compose exec platform-app-php nc -z -w2 redis 6379
docker network inspect alaa-shared-network --format '{{range .Containers}}{{.Name}} {{.IPv4Address}}{{println}}{{end}}'
docker service inspect --format '{{json .Endpoint.VirtualIPs}}' SERVICE
```

| Symptom | Cause | Section |
|---|---|---|
| Name does not resolve inside the container | The service is not attached to the shared network, or the alias is on a different service | §1, §2 |
| Resolves but connection refused | The alias is on a worker or scheduler, which has no listener | §2 |
| Works after `up`, fails after a deploy | The consumer names a container instance or a task ID | §2 |
| Database reachable from outside the host | Published on `0.0.0.0`, or Swarm `mode: ingress` | §3 |
| Client IP is always the proxy's | The application does not trust the forwarded header, or the proxy does not set it | §4 |
| Client IP is attacker-controlled | `TRUSTED_PROXIES` is a wildcard | §4 |
| `down` in one repository broke every other service | The shared network was not `external: true` | §1 |
