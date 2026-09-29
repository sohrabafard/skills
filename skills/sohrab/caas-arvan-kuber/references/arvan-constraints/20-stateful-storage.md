# Arvan constraints: Stateful Storage

## 2. Scaling is stateless-only

**Confirmed by Arvan** — https://docs.arvancloud.ir/en/cloud-container/manage-app/scaling, checked 2026-07-29.

- Horizontal scaling "is only applicable to stateless applications".
- "If your application has Persistent Storage enabled, you cannot use manual or automatic scaling." Both are disabled, not just the automatic one.

Therefore: an HPA targets a `Deployment`. A workload with a PVC gets no HPA and no replica knob in values; it gets a runbook procedure instead, and the RUNBOOK states that scaling requires detaching storage. `--profile arvan` in the shared manifest checker enforces the HPA target.

## 3. Disk lifecycle

**Confirmed by Arvan** — https://docs.arvancloud.ir/en/cloud-container/disk/, checked 2026-07-29.

- The container filesystem is ephemeral: its contents are deleted on every application restart. Anything that must survive a restart is on a disk.
- Disk size **increases only**; decreasing is not possible, and the size must be a whole number.
- **Detaching a disk restarts the application.** A detached disk keeps its data and can be reattached with a new mount path and capacity.
- **Deleting a disk is irreversible**; the data is unrecoverable.

Therefore: every disk operation is a runbooked, announced change, and the operator RUNBOOK carries the procedure before the first disk is attached, not after.



Provenance and source dates: [SOURCES.md](../SOURCES.md).
