# Topology: single node, replicas with Keeper, copies without Keeper

The environment declares the mode, `single-node` or `replicated`, with no default and no fallback
(`/alaa-services-contract` `references/15-deployment-and-runtime-contract.md`). Read the declared
mode before you choose an engine. A change of mode does not authorize conversion of a populated
table. The infrastructure operator owns node count, Keeper placement, listeners and recovery; this
file states what the tables and the clients need from each mode.

`90-source-map.md` holds the default of every setting named here. Read the effective value on the
target before you rely on one.

## What each mode gives and costs

| | single node | replicated with Keeper | copies without Keeper |
| --- | --- | --- | --- |
| engine family | `MergeTree` | `Replicated*MergeTree` | `MergeTree` on each node |
| insert deduplication on retry | off until the table sets a window | on by default, in a bounded window | off, and the nodes do not share it |
| DDL | apply once | not replicated; apply to every replica | apply to every node yourself |
| one node is lost | outage; recover from backup or re-ingest | reads and writes continue on the other replica | the other copy answers from its own data |
| what the design must add | a deduplication window and a recovery path | a Keeper quorum, a quorum decision and lag monitoring | a named primary and a reconciliation procedure |

## One DDL file, both modes

Write fleet DDL so that the same file applies in both declared modes. The engine line is the only
part that differs. The DDL owner chooses and ratifies the substitution mechanism; on `wa`, read its
ratified engine RFC before you select an engine. Never fork the DDL file by mode, because two files
drift.

## Single node

- Set `non_replicated_deduplication_window` on every table that a retrying writer inserts into. It
  is off by default, so a retried insert duplicates rows. Sizing: `30-ingest-and-parts.md`.
- One node is one failure domain. State the recovery path in the change request: a verified backup,
  or re-ingest from the upstream source.
- An existing `MergeTree` table converts to replicated without re-ingest: `ATTACH TABLE … AS
  REPLICATED` on the detached table, or a `convert_to_replicated` flag file in its data directory,
  which takes effect at the next server restart. Conversion of a populated table is the operator's
  action and needs the table owner's ratification.

## Replicated with Keeper

**Coordination.**

- Every `Replicated*` engine needs ClickHouse Keeper. Without a configured Keeper, a replicated
  table cannot be created and an existing one is read-only.
- Keeper runs standalone or inside `clickhouse-server` through a `keeper_server` block. Either way
  it needs a majority of voters alive. Three voters survive the loss of one. Two data replicas that
  each embed Keeper are two voters and survive the loss of none, so a two-replica design needs a
  third, Keeper-only voter.
- Keeper is a write dependency and not a read dependency. While it is unavailable, an `INSERT`
  throws and replicated tables turn read-only; a `SELECT` still runs. The ingest buffer must
  therefore hold a Keeper outage: `/vector-rust-observability-pipelines`
  `references/30-buffers-acks-and-backpressure.md`.

**Tables.**

- Declare `ENGINE = ReplicatedMergeTree` with no arguments, and define the `{shard}` and
  `{replica}` macros on every server before the first `CREATE`. The server defaults
  `default_replica_path` and `default_replica_name` then give each table a unique Keeper path. A
  hand-written path collides when a table is renamed or recreated.
- `INSERT` and `ALTER` data replicate. `CREATE`, `DROP`, `ATTACH`, `DETACH` and `RENAME` run on one
  server. Apply the DDL file to every replica, use `ON CLUSTER`, or hold the tables in a
  `Replicated` database, which replicates metadata only. Without one of these, the replicas hold
  different schemas and nothing errors.
- Replicate every table of a pipeline, the target of each materialized view included. A view fires
  on the replica that receives the `INSERT`; parts fetched by replication do not fire it. A
  non-replicated target therefore differs per replica.
- This fleet runs one shard. A proposal to shard is an architecture decision: `/alaa-system-design`.

**Durability and consistency.** Each is a decision the table owner ratifies.

- By default an `INSERT` is acknowledged after one replica writes it. If that replica is lost before
  the other fetches the part, the acknowledged rows are gone. For a table whose numbers are billed,
  set `insert_quorum` to `2` or `auto` on the writer identity. The cost: inserts fail while fewer
  replicas are alive, and the ingest buffer must hold them.
- Replicas converge asynchronously, so a read on one replica can miss a row another replica already
  holds. Never make a request path depend on reading its own write. Sequential reads need quorum
  inserts plus `select_sequential_consistency=1` with `insert_quorum_parallel=0`; propose that only
  for a named reader that cannot tolerate lag, and state the insert throughput it costs.
- Compare a performance or parity measurement on one named replica.

**Operation.**

- Watch `system.replicas` for `is_readonly`, `absolute_delay` and `queue_size`, and
  `system.replication_queue` for stuck entries. Metric and alert names:
  `/alaa-services-contract`. Requirement levels: `/alaa-observability-soc`.
- A replica that lost its local data or its Keeper metadata is recovered by the operator through
  the official replication recovery procedure. Do not improvise it from a service repository.
- A service lane holds one address. Which address fronts the replicas is the operator's decision.
  Never write a replica hostname into a service.

## Copies without Keeper

No replicated engine works without Keeper. What remains is a copy, not a replica:

| Mechanism | What it does | Limit |
| --- | --- | --- |
| two sinks, two independent nodes | the pipeline writes each batch twice | a failure on one side diverges the nodes until someone reconciles them |
| a `Distributed` table with `internal_replication=false`, the default | writes each insert to every listed replica | official: "the consistency of replicas is not checked and, over time, they will contain slightly different data" |
| backup and restore to a standby | a point-in-time copy | loses every row after the last backup |

Rules for a copy:

- Name one node the primary. Serve a billed or exact number from the primary only.
- After an outage of either side, rebuild the copy from the primary or re-ingest it. Never merge
  the two by hand.
- Each node deduplicates on its own; set the single-node window on both.
- A `Distributed` table over `Replicated*` tables sets `internal_replication=true`, as the official
  text requires; the default `false` is for non-replicated tables only.

When the reason for "no Keeper" is the cost of a separate Keeper service, recommend Keeper embedded
in the server processes with three voters instead. It gives real replicas for the same node count
plus one small voter.
