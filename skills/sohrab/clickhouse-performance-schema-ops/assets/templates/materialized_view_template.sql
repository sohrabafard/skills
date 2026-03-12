
-- Incremental materialized view template
-- Use for rollups, denormalization, or ingestion-time filtering.

CREATE TABLE analytics.events_hourly
(
    bucket DateTime,
    tenant_id UInt64,
    service LowCardinality(String),
    event_type LowCardinality(String),
    hits AggregateFunction(count)
)
ENGINE = AggregatingMergeTree
PARTITION BY toYYYYMM(bucket)
ORDER BY (tenant_id, service, event_type, bucket);

CREATE MATERIALIZED VIEW analytics.mv_events_hourly
TO analytics.events_hourly
AS
SELECT
    toStartOfHour(ts) AS bucket,
    tenant_id,
    service,
    event_type,
    countState() AS hits
FROM analytics.events
GROUP BY
    bucket,
    tenant_id,
    service,
    event_type;

-- Query with:
-- SELECT bucket, tenant_id, service, event_type, countMerge(hits)
-- FROM analytics.events_hourly
-- GROUP BY bucket, tenant_id, service, event_type;
