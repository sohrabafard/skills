Version-sensitive claims in this topic depend on [Jitsi source map](../90-source-map.md).

## Analytics privacy

- Use stable internal user ids in analytics pipelines, never email addresses.
- Do not enable display-name or email-in-statistics flags without a stated requirement.
- Sign server-side webhooks; keep the signing secret off the browser.
- Keep raw diagnostic logs separate from business analytics.
- Define the retention period for watch-time data before shipping the collector, for the same reason as recordings:
  an undeclared period is decided by a disk.
