# Core Config Structure and Timeouts

## The `defaults` association rule

When the task involves defaults association, use [Defaults association](./20-core-config-and-timeouts/10-defaults-association.md).

### Why this is the rule and not a preference
For this detail, use [the routed procedure](./20-core-config-and-timeouts/10-defaults-association.md#why-this-is-the-rule-and-not-a-preference).

## Timeouts

When the task involves timeouts and retries, use [Timeouts and retries](./20-core-config-and-timeouts/20-timeouts-and-retries.md).

## Retries and redispatch

When the task involves timeouts and retries, use [Timeouts and retries](./20-core-config-and-timeouts/20-timeouts-and-retries.md).

## Connection ceilings and queueing

When the task involves connection capacity and reuse, use [Connection capacity and reuse](./20-core-config-and-timeouts/30-connection-capacity.md).

## Connection reuse

When the task involves connection capacity and reuse, use [Connection capacity and reuse](./20-core-config-and-timeouts/30-connection-capacity.md).

## Maps instead of ACL chains

When the task involves maps and preprocessor, use [Maps and preprocessor](./20-core-config-and-timeouts/40-maps-and-preprocessor.md).

## Environment variables and the preprocessor

When the task involves maps and preprocessor, use [Maps and preprocessor](./20-core-config-and-timeouts/40-maps-and-preprocessor.md).

## Diagnosing by symptom

When the task involves symptom diagnosis, use [Symptom diagnosis](./20-core-config-and-timeouts/50-symptom-diagnosis.md).

### 502 or 503 in bursts
For this detail, use [the routed procedure](./20-core-config-and-timeouts/50-symptom-diagnosis.md#502-or-503-in-bursts).

### Tail latency spikes with normal median
For this detail, use [the routed procedure](./20-core-config-and-timeouts/50-symptom-diagnosis.md#tail-latency-spikes-with-normal-median).

### Too many open files
For this detail, use [the routed procedure](./20-core-config-and-timeouts/50-symptom-diagnosis.md#too-many-open-files).

### Backends flapping in and out of rotation
For this detail, use [the routed procedure](./20-core-config-and-timeouts/50-symptom-diagnosis.md#backends-flapping-in-and-out-of-rotation).
