# WA checkpoint finding disposition

| Before | Subject | Original summary | Disposition |
| --- | --- | --- | --- |
| `clickhouse/ddl/001_init.sql:64` CH005 | `wa_raw.events_raw` | column 'user_id' is Nullable(String) with no recorded reason | Genuine finding retained. |
| `clickhouse/ddl/001_init.sql:68` CH005 | `wa_raw.events_raw` | column 'session_locale' is Nullable(String) with no recorded reason | Genuine finding retained. |
| `clickhouse/ddl/001_init.sql:72` CH005 | `wa_raw.events_raw` | column 'device_os' is Nullable(String) with no recorded reason | Genuine finding retained. |
| `clickhouse/ddl/001_init.sql:73` CH005 | `wa_raw.events_raw` | column 'device_os_version' is Nullable(String) with no recorded reason | Genuine finding retained. |
| `clickhouse/ddl/001_init.sql:74` CH005 | `wa_raw.events_raw` | column 'device_browser' is Nullable(String) with no recorded reason | Genuine finding retained. |
| `clickhouse/ddl/001_init.sql:75` CH005 | `wa_raw.events_raw` | column 'device_browser_version' is Nullable(String) with no recorded reason | Genuine finding retained. |
| `clickhouse/ddl/001_init.sql:81` CH005 | `wa_raw.events_raw` | column 'device_screen_w' is Nullable(UInt16) with no recorded reason | Genuine finding retained. |
| `clickhouse/ddl/001_init.sql:82` CH005 | `wa_raw.events_raw` | column 'device_screen_h' is Nullable(UInt16) with no recorded reason | Genuine finding retained. |
| `clickhouse/ddl/001_init.sql:83` CH005 | `wa_raw.events_raw` | column 'device_dpi' is Nullable(UInt16) with no recorded reason | Genuine finding retained. |
| `clickhouse/ddl/001_init.sql:87` CH005 | `wa_raw.events_raw` | column 'network_effective_type' is Nullable(String) with no recorded reason | Genuine finding retained. |
| `clickhouse/ddl/001_init.sql:88` CH005 | `wa_raw.events_raw` | column 'network_downlink_mbps' is Nullable(Float32) with no recorded reason | Genuine finding retained. |
| `clickhouse/ddl/001_init.sql:89` CH005 | `wa_raw.events_raw` | column 'network_rtt_ms' is Nullable(UInt32) with no recorded reason | Genuine finding retained. |
| `clickhouse/ddl/001_init.sql:138` CH005 | `wa_raw.events_raw` | column 'delivery_mode' is Nullable(String) with no recorded reason | Genuine finding retained. |
| `clickhouse/ddl/001_init.sql:139` CH005 | `wa_raw.events_raw` | column 'play_protocol' is Nullable(String) with no recorded reason | Genuine finding retained. |
| `clickhouse/ddl/001_init.sql:144` CH005 | `wa_raw.events_raw` | column 'end_reason' is Nullable(String) with no recorded reason | Genuine finding retained. |
| `clickhouse/ddl/001_init.sql:151` CH006 | `wa_raw.events_raw` | ORDER BY has 9 elements | Genuine finding retained. |
| `clickhouse/ddl/001_init.sql:151` CH007 | `wa_raw.events_raw` | identifier-like columns in the ORDER BY tail: content_id (position 4), set_id (position 5), course_id (position 6), play_id (position 7), event_id (position 9) | Genuine finding retained. |
| `clickhouse/ddl/001_init.sql:193` CH005 | `wa_raw.watch_segments_raw` | column 'user_id' is Nullable(String) with no recorded reason | Genuine finding retained. |
| `clickhouse/ddl/001_init.sql:197` CH005 | `wa_raw.watch_segments_raw` | column 'session_locale' is Nullable(String) with no recorded reason | Genuine finding retained. |
| `clickhouse/ddl/001_init.sql:236` CH005 | `wa_raw.watch_segments_raw` | column 'quality_variant_id' is Nullable(String) with no recorded reason | Genuine finding retained. |
| `clickhouse/ddl/001_init.sql:245` CH006 | `wa_raw.watch_segments_raw` | ORDER BY has 9 elements | Genuine finding retained. |
| `clickhouse/ddl/001_init.sql:245` CH007 | `wa_raw.watch_segments_raw` | identifier-like columns in the ORDER BY tail: content_id (position 3), set_id (position 4), course_id (position 5), play_id (position 6), event_id (position 9) | Genuine finding retained. |
| `clickhouse/ddl/002_agg.sql:78` CH006 | `wa_agg.watch_time_daily` | ORDER BY has 11 elements | Classification corrected to effective sparse index. Finding retained. effective PRIMARY KEY has 11 elements. No real shorter-prefix workload evidence was supplied. |
| `clickhouse/ddl/002_agg.sql:78` CH007 | `wa_agg.watch_time_daily` | identifier-like columns in the ORDER BY tail: course_id (position 9), set_id (position 10), content_id (position 11) | Classification corrected to effective sparse index. Finding retained. identifier-like columns in the effective PRIMARY KEY tail: course_id (position 9), set_id (position 10), content_id (position 11). No real shorter-prefix workload evidence was supplied. |
| `clickhouse/ddl/002_agg.sql:139` CH006 | `wa_agg.views_daily` | ORDER BY has 11 elements | Classification corrected to effective sparse index. Finding retained. effective PRIMARY KEY has 11 elements. No real shorter-prefix workload evidence was supplied. |
| `clickhouse/ddl/002_agg.sql:139` CH007 | `wa_agg.views_daily` | identifier-like columns in the ORDER BY tail: course_id (position 9), set_id (position 10), content_id (position 11) | Classification corrected to effective sparse index. Finding retained. identifier-like columns in the effective PRIMARY KEY tail: course_id (position 9), set_id (position 10), content_id (position 11). No real shorter-prefix workload evidence was supplied. |
| `clickhouse/ddl/002_agg.sql:194` CH006 | `wa_agg.events_hourly` | ORDER BY has 8 elements | Classification corrected to effective sparse index. Finding retained. effective PRIMARY KEY has 8 elements. No real shorter-prefix workload evidence was supplied. |
| `clickhouse/ddl/002_agg.sql:265` CH006 | `wa_agg.heatmap_10s` | ORDER BY has 11 elements | Classification corrected to effective sparse index. Finding retained. effective PRIMARY KEY has 11 elements. No real shorter-prefix workload evidence was supplied. |
| `clickhouse/ddl/002_agg.sql:265` CH007 | `wa_agg.heatmap_10s` | identifier-like columns in the ORDER BY tail: content_id (position 8), set_id (position 9), course_id (position 10) | Classification corrected to effective sparse index. Finding retained. identifier-like columns in the effective PRIMARY KEY tail: content_id (position 8), set_id (position 9), course_id (position 10). No real shorter-prefix workload evidence was supplied. |

## Additional findings and proof gaps

| Location | Subject | Disposition |
| --- | --- | --- |
| `clickhouse/ddl/002_agg.sql:83` CH010 | `wa_agg.watch_time_daily` | Genuine omitted merge dimension. ORDER BY omits writer GROUP BY dimension(s): object_type. |
| `clickhouse/ddl/002_agg.sql:144` CH010 | `wa_agg.views_daily` | Genuine omitted merge dimension. ORDER BY omits writer GROUP BY dimension(s): object_type. |
| `clickhouse/ddl/002_agg.sql:270` CH010 | `wa_agg.heatmap_10s` | Genuine omitted merge dimension. ORDER BY omits writer GROUP BY dimension(s): object_type. |
| `clickhouse/ddl/002_agg.sql:83` CH011 | `wa_agg.watch_time_daily` | Missing source binding proof. The computed `event_date` output can conflict with the source's materialized `event_date` column. The independently bound `object_type` finding still applies. |
| `clickhouse/ddl/002_agg.sql:144` CH011 | `wa_agg.views_daily` | Missing source binding proof. The computed `event_date` output can conflict with the source's materialized `event_date` column. The independently bound `object_type` finding still applies. |
| `clickhouse/ddl/001_init.sql:280` CH011 | `wa_raw.events_raw` | Round 1 proof gap. The additive source ALTER is present in the checkpoint and outside the admitted grammar. Review its effective schema and binding. |
| `clickhouse/ddl/001_init.sql:331` CH011 | `wa_raw.watch_segments_raw` | Round 1 proof gap. The additive source ALTER is present in the checkpoint and outside the admitted grammar. Review its effective schema and binding. |
