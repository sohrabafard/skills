# 30 Discovery Diagnosis

When diagnosing service discovery or routing, read this reference.

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
