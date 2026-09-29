# Feature and version notes

A version number written into a file goes stale silently. This file therefore
states the **cadence**, so an agent can compute the current baseline, then only
facts that do not move: general-availability milestones, features that are still
experimental, hard numeric limits, and deprecations paired with their
replacement.

Each entry names the command or URL that re-derives it. Check rather than trust.

## Compute the baseline, do not read it

When a target GitLab or Runner version is unknown, derive the supported baseline and live-version facts before choosing version-dependent behavior. read [Compute the supported baseline](./feature-version-notes/10-compute-supported-baseline.md).

## Generally available, and therefore safe to use without a caveat

When deciding whether a named feature is generally available, read [feature status, limits, and deprecations](./feature-version-notes/20-feature-status-limits-and-deprecations.md).

## Still experimental — do not build a production pipeline on these

When evaluating experimental features or an existing experimental configuration, read [feature status, limits, and deprecations](./feature-version-notes/20-feature-status-limits-and-deprecations.md).

## Hard limits — these are checkable rules, not guidance

When checking a GitLab or Runner hard limit, read [feature status, limits, and deprecations](./feature-version-notes/20-feature-status-limits-and-deprecations.md).

## Deprecations, each with its replacement

When replacing a deprecated GitLab keyword, API surface, or tool, read [feature status, limits, and deprecations](./feature-version-notes/20-feature-status-limits-and-deprecations.md).

## Writing an answer when the target versions are unknown

When writing a design answer without known target versions, follow the baseline and qualification steps in read [Compute the supported baseline](./feature-version-notes/10-compute-supported-baseline.md).
