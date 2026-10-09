# Independent adjunct-tool research

Research date: 2026-10-10. This separately requested read-only investigation does not change the routing upgrade, plan, acceptance criteria, configuration, or installation state. Findings come from the research lane's live primary-source review; no candidate was installed, benchmarked, or tried locally.

## Decision

The current CodeGraph, Serena, Laravel Boost and native-tool set is a sound baseline when each operation uses the correct project and native proof. Evidence does not establish a universally best combination or justify adding another tool everywhere. A bounded Context7 pilot for version-sensitive documentation outside Laravel is the clearest candidate; this is a research inference, not adoption approval.

| Candidate | Incremental gap | Cost or limit | Research recommendation |
|---|---|---|---|
| Context7 | Relevant versioned library documentation outside Laravel | Network/service dependency, incomplete version coverage, query privacy | Narrow documentation pilot |
| RTK | Large shell/test/build output | Filtering can remove needed evidence and cause rereads; filter/hook maintenance | Measure actual shell-output share first |
| Claude Context | Natural-language semantic retrieval when names are unknown | Embeddings, vector database, second index, backend operation and code privacy | Consider only after real retrieval misses |
| Repomix | A selected portable context bundle for handoff | Snapshot drift; compression drops implementation detail | Occasional packaging rather than routine discovery |
| Sentry MCP | Actual errors, traces and performance evidence | Requires telemetry and correct account/project access | Only if equivalent access is not already available |

## Evidence and tradeoffs

Context7 documents version selection and both Claude Code and Codex integration. It does not replace repository truth or Laravel Boost's applicable documentation. Coverage of every dependency/version in the user's projects remains unverified. The service privacy page says queries can be sent to LLM providers for reranking and retained anonymously for retrieval improvement; a local MCP process therefore does not imply offline retrieval. Keep sensitive material out of queries. An outage, missing version or rate limit should leave official version-correct documentation as the fallback. Setup effort is comparatively small, but coverage and data-handling policy need validation. Sources: [CLI/version support](https://github.com/upstash/context7/blob/master/docs/clients/cli.mdx), [Codex integration](https://github.com/upstash/context7/blob/master/plugins/codex/context7/README.md), [privacy](https://context7.com/docs/security/data-privacy), [API limits](https://context7.com/docs/api-guide).

RTK reduces selected command output, a different capability from source intelligence. Its documented integrations cover both runtime families, but local compatibility was not tested. Claude's internal Read/Grep output is not Bash-hook output. Vendor output-reduction percentages are not full-session token savings; the project's savings explanation uses a bytes/4 approximation. A published JetBrains benchmark using RTK 0.43.0, Claude Code 2.1.201 and claude-sonnet-5 reported increased low-effort cost and roughly unchanged high-effort cost, without a meaningful quality difference. That workload and generation do not establish current Codex or other-task results. Sources: [project](https://github.com/rtk-ai/rtk), [integrations](https://github.com/rtk-ai/rtk/blob/develop/docs/guide/getting-started/supported-agents.md), [measurement limits](https://github.com/rtk-ai/rtk/blob/develop/docs/guide/resources/savings-explained.md), [primary benchmark](https://blog.jetbrains.com/ai/2026/07/rtk-claude-code-token-savings/).

Claude Context offers hybrid lexical/vector search, with documented Codex/Claude setup, embedding-provider choices including local Ollama, and Milvus/Zilliz storage. External embedding can transmit source chunks. A second index adds setup, freshness and maintenance costs. The project's benchmark reports token reduction on 30 tasks with GPT-4o-mini against a read/grep baseline; it does not compare with CodeGraph plus Serena. A failed vector service must degrade to existing retrieval without turning incomplete coverage into absence. Sources: [official repository](https://github.com/zilliztech/claude-context), [published evaluation method](https://raw.githubusercontent.com/zilliztech/claude-context/master/evaluation/README.md).

Repomix packages selected context without a permanent index in its local CLI path. Its documented MCP/compression features are experimental; compression removes function bodies and conditional detail, so compressed output cannot prove implementation behavior. Local CLI use is broadly accessible; documented Claude integration and an MCP description do not establish a tested Codex MCP setup here. Sources: [MCP boundary](https://repomix.com/guide/mcp-server), [compression limits](https://repomix.com/guide/code-compress).

Sentry's MCP supplies runtime evidence rather than another source graph. Documentation describes OAuth/HTTP and organization/project controls. Self-hosted operation has separate limitations, and some natural-language searches need an LLM provider. Existing equivalent access removes the case for duplicate registration. During outage local review can continue while live claims remain unverified. Sources: [official service](https://mcp.sentry.dev/), [self-hosted toolkit](https://github.com/getsentry/toolkit).

## If a future pilot is authorized

Choose actual unanswered questions first. Hold task, runtime, model/effort, permissions and baseline tools constant across repeated runs. Measure correct-answer latency, real total-session usage including cache/output, call count, API/version accuracy, native proof, failure behavior, transmitted information and maintenance cost. Qualify any comparison by its workload and environment. Do not infer improvement from vendor output ratios alone.

Adding a duplicate structural index, another registration of an existing capability, or full-repository context without a named need has no demonstrated incremental benefit in this investigation.

## Lane record

Researcher: adjunct_tools_research, alaa-researcher. Requested gpt-6.1-sol/medium; observed serving identity unknown. The lane performed web/source reading only. Its result was kept separate from the implementation and all acceptance decisions.
