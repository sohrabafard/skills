# WSL Sandbox Recovery

## Classify before retrying

- **Symptom.** The harness cannot start its Linux sandbox, or a command reports `Operation not permitted`, `Permission denied`, `Read-only file system`, a denied socket connection or blocked network access.
- **Diagnosis.** Record whether the command started and the intended check ran. A sandbox setup/launch error identifies the harness; `EPERM`, `EACCES`, `EROFS`, DNS failure or a timeout alone does not prove sandbox causation. Check the named path/operation against effective permissions and bounded Linux evidence.
- **Retry.** For a failed read batch, retry only the failed essential read/search, serially with bounded output, if a smaller request addresses the cause. When the sandbox itself is the evidenced blocker, use the escalation procedure below instead. These are alternatives within the existing retry budget.
- **Fallback.** Reuse successful evidence and mark uncovered work unverified. A harness failure establishes no repository drift or missing file.

## Exact-command escalation

1. Establish that the command is necessary, its effects are already authorized, and sandbox restrictions plausibly prevent it. Separate task authorization from the harness's approval decision; neither this skill nor an old command list supplies approval.
2. Read the active tool schema and permission instructions. When escalation is exposed and allowed, request the exact failed command through that tool. For `exec_command` exposing this contract, use `sandbox_permissions: "require_escalated"` with a concise task-specific `justification` describing the failed capability and required result.
3. Preserve the Linux executable, shell, working directory, environment, arguments and flags. Change only the sandbox permission request; append no cleanup, installation, configuration change or unrelated command. Avoid broad persistent prefixes for shells, interpreters or arbitrary scripts.
4. Let the configured reviewer handle the request: it may be the user or automatic approval review. Reuse applicable existing authorization; do not add a second conversational confirmation for an already authorized action. Honor every required harness approval.
5. If escalation is unavailable, forbidden or denied, do not run the command through another shell, service or tool to evade the restriction. Continue a safe authorized alternative when available. If automatic review remains the blocker, name the rejected action and stated reason; request any needed user decision through the supported flow.
6. Keep both outcomes: a successful retry proves only that command's checks and does not erase the sandbox failure. If the retry fails, preserve its output, diagnose without another execution attempt, and report the next safe action.

Do not change sandbox/approval configuration, disable protections, start a nested unsandboxed Codex session, or add `sudo` as a recovery shortcut. Escalation neither grants Linux root privileges nor repairs ownership, missing tools, stopped services or application defects.

## Network, registry and documentation access

- **Symptom.** DNS, registry, package-index, Composer, npm, Git-remote or docs-fetch failure.
- **Diagnosis.** Decide whether current external state is required. Distinguish a permission denial from authentication, TLS, proxy, DNS or upstream availability failures; do not expose credentials or complete environment dumps.
- **Retry.** If live access is required, the effects are authorized and evidence points to sandbox policy, use exact-command escalation above. A network request does not authorize package installation, publication or remote mutation.
- **Fallback.** Use sufficient local source, lockfiles or vendored documentation and state the freshness limit. Do not edit manifests, lockfiles, mirrors, package configuration, DNS or docs URLs merely to bypass the failure.
