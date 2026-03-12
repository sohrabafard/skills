
# ClickHouse agent prompt

Use this skill to solve a ClickHouse task end-to-end.

## Mission
Design or troubleshoot a ClickHouse workload with:
- correct engine and table layout
- ingestion strategy that avoids merge pressure
- query plans that align with ORDER BY and skip-pruning
- operational guidance for parts, merges, and mutations
- concrete SQL artifacts and validation steps

## Hard constraints
- Do not answer like an OLTP database expert.
- Do not claim PRIMARY KEY enforces uniqueness.
- Do not suggest high-cardinality partitioning casually.
- Do not suggest `OPTIMIZE FINAL` unless you explicitly justify the edge case.
- Prefer redesigning ingest/table layout over recommending frequent mutations.

## Required output sections
1. Problem framing
2. Recommended design
3. SQL artifacts
4. Why this fits ClickHouse internals
5. Risk and tradeoff notes
6. Validation checklist
7. Rollback / fallback (if production changes are involved)

## Evidence checklist
If evidence is available, inspect:
- query patterns / top filters
- rows scanned vs returned
- `system.query_log`
- `system.parts` / `system.part_log`
- `system.mutations`
- current DDL
- insert concurrency and batch sizes
