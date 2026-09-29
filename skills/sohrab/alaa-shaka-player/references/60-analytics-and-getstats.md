# Analytics, `getStats()` and QoE quantities

All rows `verified` at v5.2.3, read 2026-07-28.

## The seam — read this before naming anything

For source ownership, pipeline count limits, and available analytics events, read [Contract and events](./60-analytics-and-getstats/10-contract-and-events.md).

## `getStats()` — every field

For every `getStats()` field and the public state-history surface, read [Stats catalog](./60-analytics-and-getstats/20-stats-catalog.md).

## `shaka.util.StateHistory` is not a public API

For every `getStats()` field and the public state-history surface, read [Stats catalog](./60-analytics-and-getstats/20-stats-catalog.md).

## Events available for analytics

For source ownership, pipeline count limits, and available analytics events, read [Contract and events](./60-analytics-and-getstats/10-contract-and-events.md).

## Deriving watch-time and QoE correctly

When deriving watch time or QoE, read [QoE derivation](./60-analytics-and-getstats/30-qoe-derivation.md) for reset, NaN, timing, hidden-tab, and error-count rules.

## Hidden-tab policy — a default, not a question

When deriving watch time or QoE, read [QoE derivation](./60-analytics-and-getstats/30-qoe-derivation.md) for reset, NaN, timing, hidden-tab, and error-count rules.

## Working snippet — a QoE quantity collector

When implementing a quantity-only collector, read [QoE collector example](./60-analytics-and-getstats/40-qoe-collector-example.md) for the preserved working snippet and its wire-name boundary.

## Delivery diagnostics

When inspecting the local QoE sink, read [Delivery diagnostics](./60-analytics-and-getstats/50-delivery-diagnostics.md) for status, capacity, send failure, and durability limits.
