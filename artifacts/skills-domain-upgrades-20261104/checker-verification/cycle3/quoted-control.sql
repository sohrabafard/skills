CREATE TABLE raw.events (tenant_id UInt32, object_type String, amount UInt64)
ENGINE MergeTree ORDER BY tenant_id;
CREATE TABLE "agg".`rollup` (tenant_id UInt32, object_type String, amount SimpleAggregateFunction(sum, UInt64))
ENGINE AggregatingMergeTree ORDER BY (tenant_id, object_type);
CREATE MATERIALIZED VIEW agg.mv TO agg.rollup AS
SELECT tenant_id, object_type, sum(amount) AS amount FROM raw.events GROUP BY tenant_id, object_type;
