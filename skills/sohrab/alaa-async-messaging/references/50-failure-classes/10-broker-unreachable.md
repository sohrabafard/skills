## 1. Broker unreachable

**Symptom.** `alaa_queue_messages_published_total` flat, `alaa_dependency_request_failures_total` rising on
the broker, consumers logging connection failures and restarting. `alaa_outbox_depth` climbing while the
service continues to answer requests normally.

**Diagnosis.** Separate an unreachable broker from a failing publisher: an unreachable broker fails every
service on the vhost at once, so check whether another service's publish counter also went flat. If only one
service is affected, it is credentials, topology, or that service's network path — not the broker.

**Smallest safe action.** None on the broker. The outbox is absorbing the outage by design: the request path
is unaffected and the facts are durable. Confirm the outbox is in fact filling, since that is the evidence
the design is working; a flat outbox depth during a broker outage means facts are being dropped instead.

**Escalation.** If publishes are being made outside a transaction with no outbox row, that route is losing
facts for the whole outage — this is a code defect, not an incident action. Broker cluster recovery is
`/caas-arvan-kuber`.
