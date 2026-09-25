# Runtime update

Verified on 2026-09-25 after the user's independently performed upgrade.

- Command: `claude --version`
- Observed result: `2.1.282 (Claude Code)`; exit 0.
- Initial observation: `2.1.221`; preserved as the baseline, superseded for current CLI version.
- The documented minimum CLI versions for the proposed profiles are now satisfied.
- Claude Desktop update is user-reported; its version and execution surface were not inspected.
- No account probe, model invocation, configuration change, installation or evaluation was performed by this task.
- Provider/account availability, effective target settings, activation, serving model and effort remain unknown.

Official [Desktop documentation](https://code.claude.com/docs/en/desktop), checked 2026-09-25, describes model selection through Desktop's dropdown and shared CLI configuration. Local Code-tab MCP configuration also includes Desktop-specific sources with distinct precedence. Therefore the standalone CLI version and this process's environment do not establish the effective model, grants or overrides in a Desktop session. Desktop activation needs evidence from that actual surface. This task has not inspected a running Desktop session or imported its configuration.

The Git index now includes task evidence, workflow files and initial policy source additions. The lead issued no staging command, and both implementation lanes reported no index mutations. Origin is unknown; the index is preserved without reset or unstage. This observation does not imply a commit exists.
