# Real IndexedDB regression harness

## Real IndexedDB regression harness

On Node 24+, prepare a new isolated output directory with
`node scripts/build-browser-regressions.mjs <new-output-directory>` from this skill. This transpiles
the actual examples and copies `scripts/browser-storage-cases.mjs`; it installs nothing and starts
no server. Serve that directory on an isolated local origin and open `index.html` only in an authorized
browser lane. The visible JSON lists each PASS/FAIL; retain its browser/version and event evidence.
Use synthetic fixtures only. Test databases have a unique prefix and remain inspectable; the harness
does not delete databases. Do not serve it on a consumer application's origin.

The cases cover fresh/v1/v3-to-v4 schema preservation, existing metadata indexing, blocked/versionchange,
old-v3 rejection, aborted upgrade, all-store and orphan purge, other-account preservation, data-only
count, repeated purge and forced transactional rollback. Real quota-pressure and cross-browser/device
coverage remain separate required consumer gates. Preparing the harness is not executing it; report
prepared/unrun separately from browser results. Vitest/fake-indexeddb and Node doubles prove only their
respective logic and cannot substitute for engine upgrade/abort evidence.
