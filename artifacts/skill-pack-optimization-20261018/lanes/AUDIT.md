# AUDIT lane source decisions

Status: implementation complete within the ratified scope; parent owns final independent acceptance and Phase 4 review.

## Provenance

The immutable intake snapshot is `artifacts/skill-pack-optimization-20261018/intake-snapshot.json` (SHA-256 `2bba02162e327a1fefd7bda0a18820cf36c1717e4d41c8bff8bd1aa1ef980ca6`). It records the source reports and numbered items; no chat history was recounted. Relevant entries are 01:A10, A34, A35 and 02:O7, O15, O25. The original source report hashes recorded in the immutable snapshot are `6de7223950f08711ad4946039995286cc7efafd4a1558f1876f8ddcf13f6e03a` for report 01 and `da0309f20c76b9bc98a3d3eda4e10ffcd8cdc2a3c815127a92c690e1ce06c7fa` for report 02. At 2026-10-18 15:38 UTC, mutable report hashes were 01 `3c8bc6fc0775f03c0ba82ee50de7df5dd4d725a034a1c3566a7c779a91a230e6` and 02 `b5c28d46b65275df496ad0529251b4d70bb22bf441a22d56bc68363aa857c1ac`; these are point-in-time values, distinct from the immutable snapshot originals.

## Ratified decisions

- **A10 — permission catalog scale:** Removed unsourced service maxima and dated ID ranges from the durable skill body. Preserved registry-derived count, maximum ID, and fingerprint sources and the per-file maximum contract. Final source hashes: skill `87da55b9b4ebb4743cd50c9116fcfc0ee2ea6843266d906cef81da1526aaefc0`; referenced owner sources were fully read before editing.
- **A34/O7 — partitioned FK audit:** Detector execution/findings remain independent of optional guard installation; missing durable guard is reportable. Installation and synthetic fixtures remain optional, explicitly authorized repository mutations. Corrected help/empty-roots wording: zero parent tables means none were found in the supplied roots and proves neither guard installation nor engine behavior. Preserved exit codes, detector algorithm, and `--install` behavior. Final hashes: skill `79a58adcbebdfac7a9b36e072425bf476455faf8dead025c12877e110ed9aafd`; script `d0d1dc36d351e6e9ed558a1683b934a66ccdb15db77bec7009f8f3e461dcebbc`.
- **A35/O15 — permission map and seed:** Coherent generated map and auth seed are applied together only when both operations are authorized. If either authorization is missing, apply neither and report the required companion path as blocked. This prevents unintended partial state. Final permission skill hash is listed above.
- **O25 — MongoDB fleet observation:** Removed the dated external-repository observation from durable `When not to use` policy and retained it as dated historical evidence with a recheck pointer. Final hashes: skill `e69505d2ffc63316154ebcd13d12c517022b8bf44e9248c53b7dc9b2987d25f3`; source map `9571fcda383683bf3e03ef6c45675d4b80095c5c706a471a7b845096945c76ee`.

## Invariants and boundaries

Preserved explicit-operation authority, coherent map/seed state, registry-derived catalog truth, detector findings independent of optional guard installation, and source-versus-engine proof limits. No audit algorithm, target repository, dependency, or external fleet claim was introduced. No generated map/seed was applied; no target repository or live database engine was inspected.

## Lane controls and verification plan

Registered authority is `alaa-implementer-low` for bounded semantic work; requested pair is `gpt-6-luna/medium`. The parent inspected the installed role definition: it is unpinned and grants `workspace-write`; the explicit dispatch supplies the requested pair. Serving identity remains unknown and is not claimed. No task-profile change was needed. The discriminating CLI check exercised `--help` plus an empty supplied root with `--require-parents`; revised wording and retained exit code 4 were asserted, with no installation. Fleet reference check passed with 11 informational unmarked target-repository paths in the permission skill. Repo-docs link checker passed on the five changed Markdown files. UTF-8-no-BOM/LF and scoped `git diff --check` passed; packaged FK skill description measured 833 chars (within 1024) after shortening. A first description measurement was 1026 and was corrected. No whole-pack suite, target engine test, install, or Phase 4 review was run; those remain outside this lane's authority.
