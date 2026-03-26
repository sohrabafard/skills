# Verification and Rollback

Use this file when you need the final deploy-safety checklist for a frontend delivery change.

## Minimum verification loop

1. Run the lightest meaningful build or pipeline check.
2. Inspect the final output tree.
3. Confirm the runtime entry and client assets exist where the deployment expects them.
4. If the task touched routing, public path, or remote assets, test a representative runtime URL.

## SSR and PWA notes

- For SSR builds, verify the runtime entry still exists.
- For PWA or service worker changes, verify the update and offline behavior only if the task actually touched those surfaces.
- Do not claim deployment safety without checking the path that was originally broken or most at risk.

## Rollback expectations

When a change affects build or delivery contracts, be ready to describe:

- which config changed
- which output path or serving rule changed
- which file or setting should be reverted first if deployment breaks

## Final closeout

Report:

- what changed in the build or delivery path
- why it was needed
- what was validated
- what still needs deploy-time confirmation, if any
