# Classification — three kinds of failure, three destinations

## Classification — three kinds of failure, three destinations

Classify by whether a retry could ever succeed, not by how bad the failure looks.

| Class | Test that identifies it | Destination |
|---|---|---|
| **Transient** | The failure is a property of this moment: dependency unreachable, timeout, lock contention, a `502`/`503`/`504` | Use the verified bounded retry path above, then its terminal DLQ disposition |
| **Permanent** | The failure is a property of the message: schema violation, unknown message type, an entity it references was deleted for good | Reject without requeue. It goes to the DLQ on the first failure, because redelivering it cannot change the outcome |
| **Tenant-scoped** | The failure is a property of one tenant or project: a disabled account, a revoked credential, an exhausted quota | Reject without requeue, and record the tenant on the message. Redelivering consumes the fleet's capacity on one tenant's messages and starves every other tenant |

**A handler that cannot classify a failure treats it as transient within the verified retry bound.**
At exhaustion, apply the declared terminal disposition; an endless non-counting return path is not a bound.
Do not discard unknown failures on the first uncertain attempt.

**A tenant-scoped failure is the one that hides in aggregate metrics.** One tenant producing every failure
looks identical, at the queue level, to a broken consumer — which is why `../50-failure-classes.md` makes
"group the DLQ by tenant" the first diagnostic step.
