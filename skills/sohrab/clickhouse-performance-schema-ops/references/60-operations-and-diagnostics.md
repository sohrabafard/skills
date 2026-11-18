# Operations and diagnostics

Start from a measurement. Run the matching query in `assets/templates/diagnostic_queries.sql` and
paste its result before you propose a change, because one ClickHouse symptom has several causes
that look the same from outside.

`system.query_log`, `system.query_thread_log` and `system.part_log` are server-configured and can
be off or truncated by retention. Establish that first, so an empty result reads as "logging is
off" and not as "nothing happened". Read an effective setting from `system.settings` or
`system.merge_tree_settings`, never from a quoted default.

## Playbook: inserts fail with `TOO_MANY_PARTS`

Entry condition: an insert returns the error, or part counts climb while the insert rate is flat.

1. Count active parts per partition, not per table. Many partitions with few parts each is a
   partitioning problem. One partition with hundreds of parts is an insert-shape problem.
2. Measure rows per insert and inserts per second at the writer against the bar in
   `30-ingest-and-parts.md`. If rows per insert is below the bar, fix the writer. That is the whole
   remedy in most cases.
3. If the writer batches well, check whether one insert spreads across many partitions. An insert
   that touches N partitions writes at least N parts. Narrow the partition key or the batch's key
   range.
4. Check `system.merges` and host CPU and IO to tell starved merges from overloaded merges.
5. Only after steps 1 to 4, and with the owner's agreement recorded, consider a merge-tree setting.

## Playbook: a mutation does not finish

Entry condition: a row in `system.mutations` has `is_done = 0` past the time its owner expected, or
has a non-empty `latest_fail_reason`.

1. Read `latest_fail_reason` first. A failed mutation can retry and block later work.
2. In `replicated` mode, check `is_done` on each replica. A mutation with `parts_to_do = 0` can
   still wait for an in-flight insert. `finish_time` of zero means unfinished or unknown.
3. Estimate the touched parts and columns from the command and the layout. A mutation rewrites
   affected data and amplifies IO even for a small logical update.
4. Decide with the table's owner whether it finishes or is killed. `KILL MUTATION` is a
   shared-system action: name the mutation and its approver, and record the state the table is left
   in, because a killed mutation leaves the table partly mutated.
5. Ask why the mutation existed. A recurring mutation means the engine choice
   (`20-table-design.md` section 6) or the deletion mechanism (`50-mvs-projections-and-ttl.md`) is
   wrong.

## Playbook: one query is slow

Entry condition: a named query exceeds the latency its owner expects, and you hold its exact text.
Follow the four steps in `40-query-tuning-and-read-lane.md`, then prove the fix under "Compare bytes
read, not wall time" in `80-proof-and-validation.md`.

## Playbook: disk grows faster than rows

Entry condition: `sum(bytes_on_disk)` from `system.parts` grows faster than `sum(rows)` over the
same window.

1. Separate active from inactive parts. The server keeps inactive parts for a configured period
   after a merge; they are not a leak.
2. Look for mutation write amplification in `system.mutations` and `system.part_log`.
3. Look for a partition whose parts never merge to a large size: the too-many-partitions shape.
4. Compare the compression each column achieves with what its type implies.

## Playbook: a replica is read-only or behind

Entry condition: `system.replicas` shows `is_readonly = 1`, a growing `queue_size` or a rising
`absolute_delay`. Follow "Replicated with Keeper" in `25-topology-and-replication.md`. A read-only
replica with a reachable server means Keeper is unreachable or lost its quorum; that is the
operator's incident, not a table defect.

## `OPTIMIZE … FINAL` is not a performance fix

`OPTIMIZE … FINAL` merges all active parts into a single part, ignores the merge-size
safeguard of about 150 GB, and risks long merges, memory pressure and out-of-memory failures. The
oversized part then merges poorly, so duplicates accumulate in a `ReplacingMergeTree`. The official
guidance sanctions it only for finalizing data before a table is frozen or exported. In every other
case, let background merges run.

Query-time `FINAL` is a different thing: it gives one `SELECT` a deduplicated view and changes no
stored bytes.
