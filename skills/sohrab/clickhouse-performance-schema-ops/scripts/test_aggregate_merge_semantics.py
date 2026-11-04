#!/usr/bin/env python3
"""Prove physical aggregate merge behavior on the authorized cached 24.8 fixture."""

import argparse
import json
import os
import subprocess
import time
from uuid import uuid4

IMAGE = "sha256:1ffa82edee000a42c09313bd9f1293d94c570aee74babc1b3ca9983a35fa597b"
VERSION = "24.8.14.39"
TABLES = {"good": ", object_type", "broken": ""}
CREATE = """CREATE TABLE {table} (
    tenant_id UInt32,
    day Date,
    object_id UInt64,
    object_type String,
    amount SimpleAggregateFunction(sum, UInt64)
) ENGINE = AggregatingMergeTree
PARTITION BY toYYYYMM(day)
PRIMARY KEY (tenant_id, day)
ORDER BY (tenant_id, day, object_id{discriminator})
SETTINGS max_bytes_to_merge_at_max_space_in_pool = 1,
         max_bytes_to_merge_at_min_space_in_pool = 1"""


def require(actual, expected, label):
    if actual != expected:
        raise AssertionError(f"{label}: expected {expected!r}, got {actual!r}")
    print(f"{label}: {actual!r}", flush=True)


def command(args, timeout=20):
    result = subprocess.run(["docker", *args], text=True, capture_output=True, timeout=timeout)
    if result.returncode:
        raise RuntimeError(f"docker {args[0]} exit {result.returncode}: {result.stderr.strip()}")
    return result.stdout.strip()


def run(image):
    if os.environ.get("DOCKER_HOST") or os.environ.get("DOCKER_CONTEXT"):
        raise RuntimeError("explicit Docker target override is outside the fixture boundary")
    require(command(["context", "inspect", "--format", "{{.Endpoints.docker.Host}}"]),
            "unix:///var/run/docker.sock", "local Docker socket")
    require(command(["image", "inspect", image, "--format", "{{.Id}}"]), image, "cached image ID")
    print("repo digests:", command(["image", "inspect", image, "--format", "{{json .RepoDigests}}"]))
    name = "alaa-dgp8-merge-" + uuid4().hex
    deadline = time.monotonic() + 180

    def sql(query, limit=30):
        return command(["exec", name, "clickhouse-client", "--max_threads", "4",
                        "--optimize_on_insert", "0", "--query", query],
                       timeout=max(0.1, min(limit, deadline - time.monotonic())))

    try:
        ready_by = time.monotonic() + 120
        command(["run", "--detach", "--pull", "never", "--name", name,
                 "--network", "none", "--cpus", "4", "--memory", "2g",
                 "--memory-swap", "2g", "--tmpfs", "/var/lib/clickhouse:rw,size=512m",
                 "--entrypoint", "/usr/bin/clickhouse-server", image,
                 "--config-file=/etc/clickhouse-server/config.xml", "--",
                 "--background_schedule_pool_size=16",
                 "--background_buffer_flush_schedule_pool_size=8",
                 "--background_message_broker_schedule_pool_size=8",
                 "--background_distributed_schedule_pool_size=8"])
        host = json.loads(command(["inspect", name, "--format", "{{json .HostConfig}}"]))
        require((host["NetworkMode"], host["NanoCpus"], host["Memory"], host["MemorySwap"]),
                ("none", 4_000_000_000, 2 * 1024**3, 2 * 1024**3), "runtime limits")
        require(host["PortBindings"], {}, "published ports")
        require(host["Binds"], None, "host binds")
        while True:
            try:
                version = sql("SELECT version()", limit=3)
                break
            except (RuntimeError, subprocess.TimeoutExpired):
                if time.monotonic() >= ready_by:
                    raise
                time.sleep(0.25)
        require(version, VERSION, "server version")
        require(command(["exec", name, "clickhouse-client", "--version"]),
                f"ClickHouse client version {VERSION} (official build).", "client version")

        def active_parts(table):
            return sql("SELECT count() FROM system.parts WHERE active "
                       f"AND database = currentDatabase() AND table = '{table}'")

        def totals(table):
            return sql(f"SELECT object_type, sum(amount) FROM {table} GROUP BY object_type ORDER BY object_type")

        for table, discriminator in TABLES.items():
            sql(CREATE.format(table=table, discriminator=discriminator))
            sql(f"SYSTEM STOP MERGES {table}")
            sql(f"INSERT INTO {table} VALUES (1,'2024-08-01',42,'A',2),(1,'2024-08-01',42,'B',7)")
            sql(f"INSERT INTO {table} VALUES (1,'2024-08-01',42,'A',3),(1,'2024-08-01',42,'B',11)")
            require(active_parts(table), "2", f"{table} before: active parts")
            require(sql(f"SELECT count() FROM {table}"), "4", f"{table} before: physical rows")
            require(totals(table), "A\t5\nB\t18", f"{table} before: grouped totals")

        for table in TABLES:
            sql(f"SYSTEM START MERGES {table}")
            sql(f"OPTIMIZE TABLE {table} FINAL SETTINGS optimize_throw_if_noop = 1")
            require(active_parts(table), "1", f"{table} after: active parts")
        require(sql("SELECT count() FROM good"), "2", "good after: physical rows")
        require(totals("good"), "A\t5\nB\t18", "good after: grouped totals")
        require(sql("SELECT count(), sum(amount) FROM broken"), "1\t23", "broken after: physical rows and total")
    finally:
        containers = command(["ps", "-aq", "--filter", f"name=^/{name}$"])
        if containers:
            command(["rm", "--force", "--volumes", name])
        require(command(["ps", "-aq", "--filter", f"name=^/{name}$"]), "", "fixture cleanup")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", required=True, choices=[IMAGE])
    run(parser.parse_args().image)
