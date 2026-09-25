# Model and Effort Policy Route

/alaa-prompting-guide owns supported capabilities, runtime precedence, local profile selection, and exception evidence. Read its `references/50-effort-and-thinking.md` before selecting a profile or changing a pin. This orchestrator owns only role triggers and authority boundaries.

Executable pins project `alaa-prompting-guide assets/claude-model-policy.json`; that owner records rationale, sources, calibration and availability. Role identifiers remain stable for callers, including the historical `alaa-implementer-opus` name. Standard and deep correctness review both select `alaa-reviewer`; depth changes scope, not reviewer count.

Run `python scripts/validate_pack.py` from this pack; it invokes the canonical policy CLI and the grant gate. After validator changes, also run `python scripts/validate_pack.py --self-test`. For a selected source or packaged agent directory, run `python scripts/check_claude_model_policy.py --agent-root <agent-directory>` from alaa-prompting-guide. Exit `0` is clean, `1` findings, and `2` unavailable proof; either nonzero blocks completion. Missing policy has no fallback. Source validation proves neither runtime compatibility nor account access or serving identity; inspect those against the owner's availability and runtime references before dispatch.

Diagnose a shortfall before changing a profile: repair missing context, a tool failure, or an ambiguous specification through its owner. A comparison changes one factor at a time. Unavailable target profiles are reported explicitly; do not silently substitute another model. Observe effective permissions and tools; API features do not prove that this host exposes them.

Report configured and requested model/effort separately from observed runtime identity. When observation is unavailable, write unknown. Preserve each role's verdict as the first line when it has one, then report metadata. The rule-writer's replacement-only contract remains owned by /alaa-prompting-guide.
