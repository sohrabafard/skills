# Resource limits, worker sizing and OS tuning

Open this file when sizing a container, tuning a long-lived PHP or Node process, or diagnosing a
service that is slower or less stable under load than its resource allocation suggests.

Why a timeout, retry, backoff, circuit breaker, backpressure or degradation mechanism exists, and
what shape it takes, is `/alaa-reliability-sla`'s decision. This file
states how the resulting numbers are expressed as container keys and process settings, and gives the
values this fleet uses.

---

## 1. `limits` and `reservations` do different jobs

When sizing Compose or Swarm CPU and memory limits or reservations, use [Container resource ceilings](./60-resource-limits-and-load/10-container-resource-ceilings.md).

## 2. The `nproc` trap

When sizing process limits or PHP workers, use [Process and PHP workers](./60-resource-limits-and-load/20-process-and-php-workers.md).

## 3. OPcache and JIT for a long-lived worker

When tuning OPcache or JIT for a long-lived worker, use [Process and PHP workers](./60-resource-limits-and-load/20-process-and-php-workers.md).

## 4. `nofile` and the sysctls that matter

When sizing file descriptors or setting sysctls, use [File descriptors and pools](./60-resource-limits-and-load/30-file-descriptors-and-pools.md).

## 5. Connection pool sizing against the container

When sizing database connection pools, use [File descriptors and pools](./60-resource-limits-and-load/30-file-descriptors-and-pools.md).

## 6. Complexity budgets

When choosing a structure budget, use [Complexity and load diagnosis](./60-resource-limits-and-load/40-complexity-and-load-diagnosis.md).

## 7. Diagnosing a load problem

When diagnosing a load symptom, use [Complexity and load diagnosis](./60-resource-limits-and-load/40-complexity-and-load-diagnosis.md).
