
-- Projection template
-- Use for alternate single-table layouts, not ETL pipelines.

ALTER TABLE analytics.events
ADD PROJECTION p_by_user
(
    SELECT
        tenant_id,
        user_id,
        ts,
        service,
        event_type
    ORDER BY (tenant_id, user_id, ts)
);

ALTER TABLE analytics.events MATERIALIZE PROJECTION p_by_user;

-- Validate whether the optimizer uses it for the target query pattern.
