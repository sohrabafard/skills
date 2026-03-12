
# Materialized views, projections, and TTL

## Materialized views
Good for:
- rollups and summaries
- ingestion-time filtering
- explicit target tables
- complex ETL and denormalization
- multi-stage data pipelines

## Projections
Good for:
- alternate single-table layouts
- transparent optimizer use
- cases where changing the base table ORDER BY is not practical

Avoid projections when:
- you need joins in the materialization logic
- you need filtered materialization definitions
- queries rely heavily on `FINAL`
- the engine is not MergeTree-family

## TTL
Use TTL for:
- retention
- moving cold data
- column expiration
Do not rely on ad-hoc heavy delete mutations when TTL or partition drops fit the lifecycle better.
