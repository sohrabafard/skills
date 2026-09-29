# Upstream deltas, version truth, and live checks

You are about to state a version number, plan an upgrade, execute a migration, or maintain this skill. This file is the **single home** of every upstream version fact and of the canonical v2 -> v3 delta table. No other file in this pack restates a version number; where one is needed, it points here.

## 1. Refresh before answering

Before stating current versions or upgrade guidance, read [Refresh and authority](./80-upstream-deltas-and-live-checks/10-refresh-and-authority.md) for live commands, exit meanings, source priority, and refresh triggers.

## 2. Release refresh, read 2026-09-29

When checking the observed 2026-09-29 releases or their current effects, read [Current release refresh](./80-upstream-deltas-and-live-checks/20-current-release-refresh.md) for the recorded versions and verified changes. For older registry evidence, read [Historical registry snapshot](./80-upstream-deltas-and-live-checks/30-historical-registry-snapshot.md) for the dated values and their limits.

### Historical npm snapshot, read 2026-07-28

The historical snapshot is preserved in [Historical registry snapshot](./80-upstream-deltas-and-live-checks/30-historical-registry-snapshot.md); do not treat it as the current release list.

## 3. Detect the installed major before any shape advice

Before giving config or API shape advice, read [Installed major](./80-upstream-deltas-and-live-checks/40-installed-major.md) to identify the consumer line and select only its shapes.

## 4. Canonical v2 -> v3 delta table

For a v2-to-v3 migration, read [Canonical v2-to-v3 deltas](./80-upstream-deltas-and-live-checks/50-v2-to-v3-deltas.md) for the complete change table and its migration references.

## 5. Framework and tool deltas

When checking changes in Quasar UI, Vite, Vue Router, Vue, or Workbox, read [Framework and tool deltas](./80-upstream-deltas-and-live-checks/60-framework-tool-deltas.md) for the recorded versions and caveats.

## 6. Verify live before answering

When validating a live claim or updating this skill, read [Live checks and maintenance](./80-upstream-deltas-and-live-checks/70-live-checks-and-maintenance.md) for current uncertainty, allowed sources, and required maintenance checks.

## 7. Skill maintenance

When updating the skill or its version evidence, read [Live checks and maintenance](./80-upstream-deltas-and-live-checks/70-live-checks-and-maintenance.md) for the maintenance and verification procedure.

## 8. Posture history

When reading historical skill posture or selecting a package-manager command, read [Posture and package manager](./80-upstream-deltas-and-live-checks/80-posture-and-package-manager.md) for dated evolution and the repo-owned manager rule.

## 9. Package managers

When selecting the package-manager command, read [Posture and package manager](./80-upstream-deltas-and-live-checks/80-posture-and-package-manager.md) for the repository-owned rule.
