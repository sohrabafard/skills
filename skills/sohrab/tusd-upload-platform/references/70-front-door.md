# The Front Door

Whatever sits between the client and the transfer layer — proxy, load balancer, gateway — makes or breaks resumable upload. Directive syntax and tuning belong to `/alaa-haproxy` (`$alaa-haproxy`); this file states the behaviours that must hold whichever product implements them.

The Ala fleet runs HAProxy. There is no Nginx anywhere in it, and this skill no longer ships an Nginx template.

## Behaviours that must hold

1. **Request buffering is off.** A buffering front door holds the whole `PATCH` body before forwarding, which converts a streaming upload into a memory or disk spike and breaks progress reporting. This is the single most common cause of an upload plane that works in development and fails in production.
2. **`PATCH`, `HEAD`, `OPTIONS` and `DELETE` survive unchanged.** A rule that permits only `GET` and `POST` breaks resume in a way that looks like a client bug.
3. **`Upload-Offset` is never rewritten, cached or synthesised.** Resume depends on the offset being the server's, exactly.
4. **`Location` is correct as the client sees it.** Either the transfer layer is told to respect forwarded headers, or the front door rewrites `Location` on the way out. Pick one and write down which, because if neither is true the client receives an internal URL, and if both are true the URL is rewritten twice.
5. **Forwarded host, scheme and client-IP chain are preserved.**
6. **Correlation identifiers are forwarded**, and generated when absent.
7. **Client-supplied copies of trusted internal headers are stripped** on every path that reaches the transfer layer — not only the creation path. Verify this; see `40-authorization.md`.
8. **The metrics path and any profiling path are unreachable from outside the internal network.**
9. **Upstream transport is HTTP/1.1** unless another mode has been tested under load with large bodies.

## Timeouts

Timeout mistakes are the second most common production failure on an upload plane, and they are diagnosable only if you write the numbers down together.

Five numbers, and the relationships between them are the point:

| Number | Must be |
|---|---|
| Client header or request timeout | longer than the slowest legitimate client's think time before it starts sending |
| **Client body timeout** | longer than the longest legitimate `PATCH` on the slowest link the product supports |
| Upstream connect timeout | short; a connect failure is not an upload problem |
| Upstream response timeout | longer than the longest legitimate `PATCH` |
| Graceful shutdown budget | longer than the longest legitimate `PATCH`, and **shorter** than the orchestrator's termination grace period |

**The client body timeout is the one that gets missed, because it is often set once for the whole front door and not per route.** In HAProxy, `timeout client` in `defaults` cannot be overridden per backend: a `defaults` value of 30 s drops any client that stalls for 30 s mid-`PATCH`, no matter what the upload backend's own timeouts say. The Ala deployment has exactly this: `timeout client 30s` in `defaults`, with an upload backend carrying `timeout server 300s` and `timeout tunnel 3600s`. Record it as a deployment defect; the fix is a separate frontend or a `defaults` value that accommodates uploads, not a longer backend timeout.

Size the body timeout from the product's slowest supported link and largest permitted file, not from the average request. An upload of 5 GiB on a 5 Mbit/s link takes over two hours; either the timeout accommodates that or the size cap says it is not supported. State which.

## The Ala HAProxy path

Read from the deployment configuration and recorded here because the client's URL depends on it:

- Backend `be_tusd` sets `timeout server 300s` and `timeout tunnel 3600s`.
- It strips the `^/tusd/` prefix on the way in and **rewrites the `Location` header back to `/tusd/...` on the way out**. Public upload URLs depend entirely on that rewrite, because the service does not set `RespectForwardedHeaders`. Changing or removing the rewrite breaks every upload silently at the second request.
- Request buffering is correctly absent.
- `timeout client 30s` sits in `defaults` and is the defect described above.

## Stickiness

For a multi-instance transfer layer over shared storage, stickiness is the lowest-risk step before a distributed lock — and it is a mitigation with a known failure mode, not a lock. An instance restart loses affinity, and the next `PATCH` arrives at an instance holding no local lock.

- one instance: nothing needed;
- several instances over shared storage: add stickiness and know what a restart does;
- active-active without stickiness: only with a lock design the team owns, including its behaviour when the lock store is unavailable.

## Verify with real uploads

Configuration review does not prove any of this. Before calling a front door ready, run a real large upload and confirm each of these; the corresponding tests are in `55-tests.md`.

- A large upload is not buffered at the front door.
- `HEAD` returns the correct offset through the front door.
- `PATCH` resumes after a network interruption.
- `Location` is correct under TLS termination and through every rewrite.
- Authorization is enforced on `POST`, `PATCH`, `HEAD` and `DELETE`, on the same rule.
- A client-supplied trusted header does not survive.
- The metrics path is refused from outside.
- A graceful shutdown does not corrupt an active upload.
- Where stickiness is configured, the same upload reaches the same instance.
