# Agent roster

Ten agents, ten distinct roles. Follow-up turns reuse the original lane agent.
Requested model overrides: none. Observed serving identity and effective
read-only enforcement: unknown for every lane; configured pins are reported
separately. Parent model and total input/output tokens are not observable.

| Lane | Role | Configured model / effort | Authority |
|---|---|---|---|
| test_strategy | alaa-test-strategist | gpt-6.1-sol / medium | Read-only test matrix |
| haproxy_package | alaa-implementer | gpt-6.1-sol / high | HAProxy package only |
| lua_package | alaa-implementer-sol | gpt-6-astra / high | Lua package only |
| failure_analysis | alaa-failure-analyst | gpt-6.1-sol / high | Read-only diagnosis, no reruns |
| instruction_review | alaa-instruction-reviewer | gpt-6-astra / high | Read-only instruction closure |
| correctness_review | alaa-reviewer | gpt-6.1-sol / high | Independent read-only correctness |
| release_review | alaa-release-guardian | gpt-6.1-sol / medium | Read-only readiness review |
| security_review | alaa-security-reviewer | gpt-6-astra / high | Read-only security review |
| verification | alaa-verifier | gpt-6-luna / low | Exact gates, evidence only |
| documentation | alaa-documenter | gpt-6-luna / high | Archive navigation and grade ledger |

Lua escalation criterion: subtle version-specific sample conversion, scheduler
and failure semantics requiring design judgment. No generic-role or model
fallback occurred. No lane was authorized to commit, install, publish or deploy.
