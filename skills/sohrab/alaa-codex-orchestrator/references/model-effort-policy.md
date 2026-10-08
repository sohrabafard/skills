# Model and Effort Policy Route

/alaa-prompting-guide owns supported capabilities, runtime precedence, local profile selection, and exception evidence. Read its `references/50-effort-and-thinking.md` before selecting a profile or changing a pin. This orchestrator owns only role triggers and authority boundaries.

The canonical executable mapping is `alaa-prompting-guide assets/codex-model-policy.json`. Source TOMLs carry explicit pins checked against it; they are initial evaluation profiles, not benchmark results. No active fallback policy is defined here.

Custom TOML model and effort fields take precedence over caller values. Select `alaa-reviewer-deep` for the deeper correctness review instead of attempting a dispatch override of `alaa-reviewer`. Both wrappers are generated from `assets/reviewer-contract.md`; never dispatch both for the same scope. Select implementation and read-only planner variants through `routing-matrix.md`; exceptional implementation admission is separate from demanding workhorse planning or implementation.

Diagnose a shortfall before changing a profile: repair missing context, a tool failure, or an ambiguous specification through its owner. A comparison changes one factor at a time. Unavailable target profiles are reported explicitly; do not silently substitute another model. Observe effective permissions and tools; API features do not prove that this host exposes them.

Report configured and requested model/effort separately from observed runtime identity. When observation is unavailable, write unknown. Preserve each role's verdict as the first line when it has one, then report metadata. The rule-writer's replacement-only contract remains owned by /alaa-prompting-guide.

Standalone implementation/planner wrappers are generated from `assets/implementation-contract.md`, `assets/planner-contract.md` and metadata-only `assets/profile-wrappers.json`. Run `python scripts/render_agents.py --write` after changes; aggregate validation checks drift, so do not repeat the same standalone drift check. Run renderer self-tests only when renderer logic changes. No wrapper specification owns model/effort values; the canonical policy is their sole source.
