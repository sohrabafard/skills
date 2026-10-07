# Independent gate transport recovery

Collaboration spawn for alaa-verifier failed with `agent thread limit reached`. The visible completed agents had no supported close operation exposed. No generic-role or model substitution was made.

The installed Codex CLI supported `exec`, ephemeral execution, command-local TOML overrides, model selection and sandbox selection. The required installed role TOMLs matched shipped name/model/effort/sandbox/developer-instruction fields. Two independent CLI runs loaded those developer instructions verbatim and their model/effort/sandbox values. All configured MCP servers were disabled only for these invocations; no installation or global configuration change occurred.

- Verifier: alaa-verifier, gpt-6-luna / low, workspace-write with artifact-only writes.
- Instruction reviewer: alaa-instruction-reviewer, gpt-6-astra / high, read-only.

Both initial CLI invocations failed before dispatch with `failed to initialize in-process app-server client: Access is denied (os error 5)`. The one cause-specific recovery was an approved elevated launch of each same CLI role, retaining its inner role sandbox. Initial and retry logs remain distinct. Role restrictions still apply; effective enforcement beyond reported runtime configuration is not inferred.

The command-local developer-instruction, effort and MCP controls were checked against the installed CLI help and [official configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference). Transport metadata and JSONL command evidence are in this artifact family. These runtime recoveries do not prove product behavior.
