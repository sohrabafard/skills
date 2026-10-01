# Version and Branch

## The branch table

Branch table refreshed on 2026-10-01 from `https://docs.haproxy.org/` (branch labels) and `https://www.haproxy.org/`
(latest patch and end-of-life dates). Re-derive both with the commands in `SOURCES.md`.

| Branch | Label | Latest patch, read 2026-10-01 | End of life |
|---|---|---|---|
| 3.5 | DEV | not for production | — |
| **3.4** | **LTS** | **3.4.6, released 2026-09-28** (branch opened 2026-06-03) | 2031-Q2 |
| 3.3 | no label (stable) | 3.3.16 | **2027-Q1** |
| 3.2 | LTS | 3.2.25 | 2030-Q2 |
| 3.0 | LTS | 3.0.29 | 2029-Q2 |
| 2.8 | LTS, critical fixes only | 2.8.30 | 2028-Q2 |
| 2.6 | LTS, critical fixes only | 2.6.34 | 2027-Q2 |
| 3.1 and below, except the rows above | EOL | — | passed |

## Which branch to target

- **A new deployment targets 3.4.** It is the current LTS and it is supported to 2031-Q2.
- **An estate on 3.2 may stay on 3.2.** It is a supported LTS until 2030-Q2. Staying is a
  decision about change velocity, not about correctness, and it is legitimate. Move to 3.4 when
  the estate needs a feature 3.2 does not have, or when 2030 is close enough to plan for.
- **An estate on 3.3 moves to 3.4.** 3.3 is not an LTS and its security support ends 2027-Q1.
  There is no version of "stay here" that survives past that date.
- **Check the exact branch, not a numeric cutoff.** 3.0, 2.8 and 2.6 remain
  supported as shown above; 3.1 is EOL. Plan unsupported-branch migration with
  config, build-feature and rollback checks. Current patches do not prove that
  the historical example image pins or runtime captures were revalidated.

The `-3.3` suffix on four example files means "requires 3.3 or later". Those four features -
backend HTTP/3, `shm-stats-file`, `sni-auto`, `ktls` - shipped in 3.3 under those directive names
and still work under those names on 3.4, confirmed by running `haproxy -c -f` on a 3.4.0 build on
2026-07-29. One thing did change: **`shm-stats-file` is no longer experimental on 3.4**, so a
config that still carries `expose-experimental-directives` for it alone now warns

```
Option 'expose-experimental-directives' is set in the global section but is no longer used.
```

while **`ktls` is still experimental on 3.4** and removing the gate there is a fatal error. Neither
fact is discoverable from the release notes; both come from the binary. `15-persistent-stats-3.3.cfg`
puts the gate behind `.if !version_atleast(3.4)` for this reason and `17-ktls-3.3.cfg` does not.

## Directive and migration routes

When checking build presence or directive syntax, read [Build and directive proof](10-version-and-branch/10-build-and-directive-proof.md) for feature inspection, parser checks and absent-directive alternatives.
When migrating from 3.2, read [3.2 to 3.3](10-version-and-branch/20-migration-3.2-to-3.3.md) for defaults, removals and deprecations.
When migrating from 3.3, read [3.3 to 3.4](10-version-and-branch/30-migration-3.3-to-3.4.md) for introductions, replacements and patch qualifications.

## Upgrading

The upgrade is a config change and a binary change, and the config change comes first:

1. Run `haproxy -c -f <cfg>` **on the new binary** before the new binary runs anything. Startup compatibility failures surface here; runtime/default changes require
   focused behavior checks. Compare feature lists and effective defaults as well.
2. Fix what it reports. Unresolved warnings block the gate under `80-gate-register.md`; a warning
   is not exempt merely because it says deprecated. Alerts block startup.
3. `scripts/check_examples.py --haproxy <path-to-new-binary>` if the estate copied from these
   examples, so the same check runs over every config at once.
4. Roll the binary. Rollback is the previous image tag; the config must remain loadable by both
   binaries for the duration of the rollout, which means no directive that exists in only one of
   them unless it is behind `.if version_atleast(...)`.

Do not share one config fragment across two branches when it uses a deprecated or experimental
directive. Keep one branch-aware config per estate.
