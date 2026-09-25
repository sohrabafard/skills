# Model and Effort Policy Route

/alaa-prompting-guide owns supported capabilities, runtime precedence, local profile selection, and exception evidence. Read its `references/50-effort-and-thinking.md` before selecting a profile or changing a pin. This orchestrator owns only role triggers and authority boundaries.

The canonical executable mapping is `alaa-prompting-guide assets/codex-model-policy.json`. Source TOMLs carry explicit pins checked against it; they are initial evaluation profiles, not benchmark results. No active fallback policy is defined here.

Custom TOML model and effort fields take precedence over caller values. Select `alaa-reviewer-deep` for the deeper correctness review instead of attempting a dispatch override of `alaa-reviewer`. Both wrappers are generated from `assets/reviewer-contract.md`; never dispatch both for the same scope. The compatibility identifier `alaa-implementer-sol` denotes the difficult implementation role and does not name its current model.

Diagnose a shortfall before changing a profile: repair missing context, a tool failure, or an ambiguous specification through its owner. A comparison changes one factor at a time. Unavailable target profiles are reported explicitly; do not silently substitute another model. Observe effective permissions and tools; API features do not prove that this host exposes them.

Report configured and requested model/effort separately from observed runtime identity. When observation is unavailable, write unknown. Preserve each role's verdict as the first line when it has one, then report metadata. The rule-writer's replacement-only contract remains owned by /alaa-prompting-guide.
