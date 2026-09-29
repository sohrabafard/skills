# Bounds, triggers, reporting

For browser-support evidence and the 2026-07-28 read date, consult [Sources and maintenance](../99-sources-and-maintenance.md), the canonical provenance record.

## Bounds, triggers, reporting

For browser-support evidence and the 2026-07-28 read date, consult [Sources and maintenance](../99-sources-and-maintenance.md), the canonical provenance record.

The queue is bounded by item count and bytes from the feature's budget file
(`30-quota-model-and-budgets.md`). **Drop items with `priority: 'low'` once the queue exceeds the
`hardStop` value in that file, and only for the classes it marks droppable. If it marks none, do not drop.**
`critical` and `normal` are never dropped to make room; stop accepting new ones and tell the user instead.

Flush triggers: boot; `online`; visibility change to visible; a successful session refresh; entering the
owning route; a manual retry control. Background Sync is a bonus where it exists — Chromium only, absent in
every Firefox and Safari/iOS, read 2026-07-28 — owned by `/alaa-quasar-app-vite-v3`; never the only trigger.

Report queue depth and oldest-row age bucketed, rows reaped per pass, per-status counts, and the
classification of every non-2xx. `outbox_reaped` is what separates "slow network" from "contexts are dying
mid-send"; without it the loss is invisible. Names are `/alaa-services-contract`; requirement level is `/alaa-observability-soc`.

Never enqueue a secret, token, decoded claim, trusted header or authorization decision in a body —
`61-authority-boundary.md`.
