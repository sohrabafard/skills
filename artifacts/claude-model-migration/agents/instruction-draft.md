# Draft fragments

Model policy route: The explicit model and effort metadata in the Claude agents is a projection of alaa-prompting-guide assets/claude-model-policy.json, which is the only policy owner. Check that metadata by invoking the documented public CLI from the prompting guide directory with --agent-root pointing at this pack agents directory. The normal pack validator invokes the CLI automatically. If the policy or its checker cannot run, validation fails; do not substitute aliases or other profiles. The policy stores source and availability conditions. Passing these local checks does not show account access, actual serving identity, or that this runtime supports the profile. Keep the existing role names for caller compatibility, even if a name includes a historical model label. Standard and deep review both use the same existing reviewer; the scope differs but there is no extra review lane.

Catalog: The grant checker compares the exact native and MCP tool grants and the implementation safety deny set. It also rejects unapproved metadata fields because adding hooks, server configuration, or permission overrides can give authority outside the authored role.

Rule-writer: The model and effort pins and the rationale for calibration come from the alaa-rule-writer profile in the canonical Claude policy JSON.
