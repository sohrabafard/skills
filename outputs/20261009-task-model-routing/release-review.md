# Independent release compatibility review

Reviewer: `routing_release`, registered `alaa-release-guardian`, configured Sol/medium; observed identity unknown. Parent persisted the supplied read-only verdict.

Initial verdict: NOT-READY. The newly introduced unconditional `tomllib` import in `profile_projection.py` broke renderer imports on older Python hosts, including hosts with `tomli`. A masked-import probe reproduced the failure. Existing consumers retained older-host fallbacks, so an undocumented minimum-version increase was not acceptable.

Repair: optional standard-library parser, then backport, then a strict top-level source-wrapper reader. It preserves instruction tokens and rejects unsupported/duplicate syntax. No dependency installation or minimum-version change.

Closure verdict: READY-WITH-CONDITIONS; no remaining actionable finding. An independent read-only probe masked both parser imports, loaded both actual renderer consumers, rendered in memory, and compared current artifacts: PASS for 33 Codex and 29 Claude orchestrator wrappers. The parent also passed the changed projection self-test; independent execution evidence is recorded by the verifier.

This simulates parser absence; it is not actual execution under an older Python interpreter. Final aggregate and installer-preflight gates remain required. Source validation does not prove installed activation, effective task controls, model access or runtime isolation.

Any future separately authorized installation must preserve matching installed policy/agent/configuration preimages, update the matching artifact set, reload the runtime, and verify controls and grants. Restore that set and reload if activation fails. No installation occurred in this task.

Return to [upgrade history](../README.md).
