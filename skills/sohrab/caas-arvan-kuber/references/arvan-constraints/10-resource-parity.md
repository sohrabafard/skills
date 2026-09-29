# Arvan constraints: Resource Parity

## 1. Resources are mandatory and parity is enforced

**Confirmed by Arvan** — https://docs.arvancloud.ir/en/cloud-container/create-app/manifest, checked 2026-07-29.

- Every container declares `resources.requests` and `resources.limits`, both with `cpu` and `memory`. Arvan's manifest page states that resource consumption must be specified per container.
- **`requests` must equal `limits`.** Arvan's manifest page states that "the values of Limits and Requests must be the same". This also gives the Pod Guaranteed QoS, which is what you want on a shared platform.
- **When resources are omitted, Arvan applies its own defaults of 1 CPU core and 2 GB of RAM per container.** Omitting them is therefore not "unlimited"; it is "whatever the platform decided", which is usually wrong and always unbudgeted.
- **Memory follows CPU at a ratio of 1 to 2.** Arvan's manifest page recommends "the ratio of 1 to 2 processor and RAM", and its own default (1 CPU, 2 GB) follows it.

  One function, so two inputs never get two different rules:

  ```
  memory_MiB = ceil(cpu_cores * 2 * 1024 / 64) * 64
  express it as Gi when the result is a whole multiple of 1024Mi
  ```

  | `cpu` | `memory` |
  |---|---|
  | `0.2` | `448Mi` |
  | `0.3` | `640Mi` |
  | `0.5` | `1Gi` |
  | `1` | `2Gi` |
  | `1.5` | `3Gi` |
  | `2` | `4Gi` |

  This is a starting point, not a measurement. When the workload's real memory profile is known, use the measured value and say that it deviates from the ratio and why. The complexity budget behind the number is `/alaa-algorithms-data-structures`; the headroom target is `/alaa-reliability-sla`.

- Include `ephemeral-storage` in both `requests` and `limits` when the namespace's LimitRange declares a default or a maximum for it. `kubectl -n NS get limitrange -o yaml` shows whether it does.

### CPU written as decimal cores, and why this is style rather than a constraint

`0.2` and `200m` are the **same quantity** to the Kubernetes API: `resource.Quantity` parses both identically and serialises back to `200m`. No Arvan document states that `200m` is rejected, and no admission failure for it has been observed. So write decimal cores to match what the Arvan panel displays, and treat a chart that uses millicores as correct rather than broken. Any checker compares parsed quantities and not strings; `/alaa-k8s-helm` `scripts/check_manifests.py --profile arvan` does.



Provenance and source dates: [SOURCES.md](../SOURCES.md).
