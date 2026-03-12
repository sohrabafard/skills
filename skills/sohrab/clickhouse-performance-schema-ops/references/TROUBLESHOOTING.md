
# Troubleshooting

## Too many parts
Usually caused by too many small inserts and/or too many partitions.

## Slow join
Often caused by using ClickHouse like a row-store. Filter early and minimize joins. Consider denormalization, dictionaries, or rollups.

## Duplicate rows with ReplacingMergeTree
Understand query-time `FINAL` versus background merges. Do not confuse `FINAL` with `OPTIMIZE FINAL`.

## Heavy deletes/updates
Avoid recurring large mutations. Revisit engine choice, partition lifecycle, TTL, or lightweight deletes.

## OPTIMIZE FINAL temptation
Treat as an edge-case operational tool, not a standard performance fix.
