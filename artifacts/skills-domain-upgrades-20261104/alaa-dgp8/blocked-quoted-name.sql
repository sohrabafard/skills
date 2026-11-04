CREATE TABLE "odd CREATE TABLE forged (tenant_id UInt32) ENGINE MergeTree ORDER BY tenant_id SETTINGS x"
(tenant_id UInt32, object_type String, amount SimpleAggregateFunction(sum, UInt64))
ENGINE = AggregatingMergeTree ORDER BY tenant_id;
