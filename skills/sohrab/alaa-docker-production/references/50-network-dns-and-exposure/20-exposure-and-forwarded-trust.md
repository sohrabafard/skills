# 20 Exposure And Forwarded Trust

When publishing ports or trusting forwarded headers, read this reference.

## 3. Exposure, with a scope

"Publicly exposed" needs a definition or the rule cannot be applied. Four distinct things are called
"exposing a port", and only one of them is a public exposure:

| Form | Reachable from | Verdict |
|---|---|---|
| No `ports:` key at all | the Docker network only | Correct default for anything that only serves other containers |
| `ports: "127.0.0.1:15432:5432"` | the host's loopback only | **Not a public exposure.** Correct for operator access on a single host |
| `ports: "5432:5432"` or `"0.0.0.0:5432:5432"` | every interface on the host, including the public one | A public exposure. Never for a database, broker, cache or admin tool |
| Swarm `ports: {mode: ingress}` | **every node in the swarm**, on every interface | A public exposure. Only for an edge proxy |
| Swarm `ports: {mode: host}` | the interfaces of the node running the task | Published on the task node; not restricted to loopback |
| `expose:` | documentation only; changes nothing | Harmless and informational |

The rule, with the scope the older fleet sentence lacked:

**No database, broker, cache or administrative interface is published on an address other than
`127.0.0.1` in a production-shaped Compose file, and infrastructure ports stay unpublished in Swarm unless an explicitly approved
network boundary restricts their reachability. Host publishing alone is not that
boundary. Only an edge proxy is published on a publicly routable address.**

That makes the fleet's owner-standard host-port table compliant rather than a violation. It
publishes each shared-infra protocol port on `127.0.0.1` with a `1`-prefixed default of its
in-network port — PostgreSQL `15432`, Redis `16379`, RabbitMQ AMQP `15672`, ClickHouse HTTP `18123`
and native `19000` — so every service and host tool finds shared infrastructure in the same place.
The table is `/alaa-services-contract`'s register; per-host deviations
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
published `mode: ingress` on a swarm whose nodes have public addresses is a public database. The following `mode: host` example bypasses the routing mesh but can still expose
the database on the task node's routable interfaces. Use it only with verified
network restrictions; otherwise omit `ports:`. See [Swarm direct port publication](https://docs.docker.com/engine/swarm/services/#publish-a-services-ports-directly-on-the-swarm-node), read 2026-09-29:

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
`/alaa-services-contract`'s register. Where the trust boundary sits, and
what an attacker gains by crossing it, is `/alaa-security-review`'s
decision. This skill states that the boundary must be expressed in the container's configuration
rather than assumed, and that the value expressing it must fail closed.

Authentication and authorisation at the gateway are `/alaa-trust-gateway-auth`'s ground.
