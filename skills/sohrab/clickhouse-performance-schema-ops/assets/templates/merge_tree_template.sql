
-- MergeTree template
-- Replace placeholders with workload-specific values.

CREATE TABLE analytics.events
(
    ts DateTime64(3),
    event_date Date DEFAULT toDate(ts),
    tenant_id UInt64,
    service LowCardinality(String),
    event_type LowCardinality(String),
    user_id UInt64,
    session_id UUID,
    properties String
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(event_date)
ORDER BY (tenant_id, service, event_type, ts, user_id)
SETTINGS index_granularity = 8192;

-- Notes:
-- 1) Revisit ORDER BY based on real filters.
-- 2) Keep PARTITION BY low-cardinality and lifecycle-oriented.
-- 3) Avoid Nullable unless semantics require it.
