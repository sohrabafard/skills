# Authorized role-name follow-up

The user requested the explicit rename from `alaa-implementer-sol` to `alaa-implementer-astra` after the routing tune completed.

The source filename and internal name, canonical policy key, grant/pack inventories, generated manifest, active dispatch references and authoring guide now use the new identifier. The old source wrapper is moved, not duplicated. Old-name mentions remain only as migration history; previous task evidence is historical.

Codex source version is 5.0.0 because callers using the retired identifier must change. Claude remains 4.2.1: its role identifier and behavior did not change. The installation guide documents that an authorized installed upgrade must also archive the old managed wrapper outside discovery; the current installer does not remove absent source files automatically.

## Evidence

- All seven commands in [check results](role-rename-checks.json) passed: canonical policy, agent contracts, grants, grant self-tests, renderer, pack validation and fleet references.
- Parsed before/after comparison confirms that the renamed agent changed only its name and obsolete compatibility-description sentence. Model, effort, permissions and instruction body are identical.
- Parsed policy comparison confirms only the profile key and obsolete rationale suffix changed.
- [Identity manifest](role-rename-manifest.json) records the new wrapper, policy and generated manifest; all are LF UTF-8 without BOM.
- Whitespace validation passed. No installed files, commits, model pins or runtime behavior were changed.
- This is a bounded identifier migration, executed directly without new agents; the earlier routing scenarios are not re-run or relabelled as evidence for installed activation.

The earlier report and 21-file snapshot remain evidence of the pre-rename routing tune. Use this follow-up for the current Codex identifier.
