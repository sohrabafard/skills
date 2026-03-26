---
name: fluentbit-generator
description: "Comprehensive toolkit for generating best practice Fluent Bit configurations. Use this skill when creating new Fluent Bit configs, implementing log collection pipelines (INPUT, FILTER, OUTPUT sections), or building production-ready telemetry configurations."
---

# Fluent Bit Config Generator

## Purpose

This skill covers: Comprehensive toolkit for generating best practice Fluent Bit configurations. Use this skill when creating new Fluent Bit configs, implementing log collection pipelines (INPUT, FILTER, OUTPUT sections), or building production-ready telemetry configurations.

Keep this top-level file small. Load the topic map, supporting docs, examples, scripts, and the preserved full guide only as needed.

## When to use

- the user asks for work covered by this skill's description
- you need the bundled docs, examples, or scripts to follow the house workflow
- you want a routing-first entrypoint instead of loading a very large inline guide

## When NOT to use

- do not use this skill as a generic replacement for unrelated tooling work
- do not use it when the task is only to audit, lint, or debug an existing file

## Quick start

1. Read the repo-local `AGENTS.md` and the current task constraints.
2. Read `references/00-topic-map.md`.
3. Open only the smallest supporting docs, examples, or scripts needed for the exact task.
4. Read `references/full-guide.md` only when the topic map is not enough.
5. Pair with the companion skill when generation and validation should both happen in the same task.

## Companion routing

- $fluentbit-validator
  - Pair it before final delivery so generated output is checked with the matching validation workflow.

## Reference navigation

- Topic map: `references/00-topic-map.md`
- Full preserved guide: `references/full-guide.md`
- Examples:
  - `examples/application-multiline.conf`
  - `examples/cloudwatch.conf`
  - `examples/file-tail-s3.conf`
  - `examples/full-production.conf`
  - `examples/http-input-kafka.conf`
  - `examples/kubernetes-elasticsearch.conf`
  - `examples/kubernetes-loki.conf`
  - `examples/kubernetes-opentelemetry.conf`
  - `examples/lua-filtering.conf`
  - `examples/multi-destination.conf`
  - `examples/parsers.conf`
  - `examples/prometheus-metrics.conf`
  - `examples/stream-processor.conf`
  - `examples/syslog-forward.conf`
- Scripts:
  - `scripts/generate_config.py`
- Sample output:
  - `output/k8s-errors-elasticsearch.conf`
  - `output/parsers.conf`

## Maintenance rules

- Keep this file routing-first and easy to scan.
- Keep detailed guidance in `references` instead of growing this file again.
- Keep the topic map aligned with the actual headings in the full guide.
- Keep paths in this file one hop away from `SKILL.md` so agents can discover them quickly.
