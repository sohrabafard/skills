DROP TABLE `application`.`events`;
OPTIMIZE TABLE "application" . "events" FINAL;
INSERT INTO application.events VALUES ('signoz_traces.distributed_signoz_index_v3');
