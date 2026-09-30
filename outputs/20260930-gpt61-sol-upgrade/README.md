# GPT-6.1 Sol targeted upgrade

The source upgrade and authorized managed-agent installation passed their checks. Fresh CLI
activation is **blocked**: Codex CLI 0.157.0 with this ChatGPT account rejects GPT-6.1 Sol with
HTTP 400. No target role completed its smoke task, and no substitute model was selected.

## Decision and source changes

The user selected official documentation plus bounded smoke as the acceptance basis, without
a local A/B comparison. [OpenAI model guidance](https://learn.chatgpt.com/docs/models) recommends
GPT-6.1 Sol for complex coding and agentic work when available. This does not establish a
measured advantage on this project's workloads.

The central policy is now 1.1.0 and the orchestrator pack is 4.1.0. Exactly 16 existing Sol
profiles changed model: main and 15 custom roles, including the separately owned rule-writer.
Existing medium/high efforts, role instructions, permission fields and active MCP grants were
preserved. Astra/Luna routing, Claude policy, historical records and domain skills were preserved.

The four active Sol comparison pairs now use GPT-6.1 Sol as candidate and GPT-6 Sol as comparator
at the same effort. Every calibration remains `unrun`. The policy checker accepts only the
registered new model and retains unknown-model, invalid-effort and unauthorized-legacy rejection.
Codex's exposed Ultra capability is recorded separately from
[API effort support](https://developers.openai.com/api/docs/models/gpt-6.1-sol).

Only model/capability/evidence metadata changed in the owning GPT reference. The entire Prompt
design section is unchanged: the current
[prompting guide](https://developers.openai.com/api/docs/guides/latest-model#prompting-best-practices)
does not establish a new Sol-specific behavioral rewrite. See [research](research.json),
[source diff](source.diff) and [preservation proof](gate-preservation.txt).

## Read order and evidence

1. [Workflow plan](docs/_agent_plans/20260930-120000_gpt61-sol-upgrade.md) and
   [checkpoint](docs/agents/20260930-120000_gpt61-sol-upgrade-state.md).
2. [Source snapshot](source-snapshot.json), [15 source gate results](gates.json), and
   [independent review](independent-review.json).
3. [Installation receipt](installation-receipt.json), [semantic preservation](installed-verification.json),
   [validated materialization byte proof](installed-byte-proof.json), and [preinstall hashes](preinstall.json).
4. [Smoke result](smoke-result.json), [persistent dispatch evidence](smoke-persistent/dispatch-evidence.json),
   [persistent output](smoke-persistent/smoke-controller-output.txt), and
   [server errors](smoke-persistent/smoke-stderr.txt).
5. [Closure checks](closure.json) and [curation outcome](curation.json).

All 15 source gates exited zero on scoped SHA256
`ef61057c4d8ab519dfadb57605628afe6623f2438e7ec41f0a84fa38f8403855`:
preservation, model policy and negative/positive self-tests, corpus and corpus self-test,
rule-writer grants, renderer, agent contracts/grants, pack validation, the four root checkers,
and whitespace. Independent review approved the source, installation-helper reconciliation and
smoke-helper changes. Passing source gates were not rerun on unchanged inputs.

## Installation and recovery

The official installer updated 23 orchestrator definitions. The prescribed copy updated the
rule-writer separately. All 24 installed model/effort pins passed. Both related installed skills
are symlinks to source and required no reinstall. Global configuration and unrelated installed
agents retained their hashes.

The live materializer refreshed disabled `node_repl`/`cua_repl` transport discriminators and
added an explicitly disabled `code-review` overlay. These inactive overlays are recorded;
active grants, instructions, efforts and permission fields were preserved. All 23 installed
orchestrator files byte-match official materialization validated against seven live MCP servers.

Two supplementary installed-grant invocations failed because `--agents-dir` validates source
templates: the first included the separate rule-writer and the second supplied resolved
transports. These failures remain failures; no third retry occurred. The independent validated
materialization and installed-byte proof are the successful installed-payload evidence.

Before installation, 26 previous managed files were copied and hash-verified in
`<task-cache>/preinstall` outside Git. Retain that directory and its recovery manifest. Restoring
those exact files is the scoped recovery option if the user requests reversal. No deletion,
global configuration edit, service change, commit, push or publication occurred.

## Fresh-session smoke and limits

The three targets were `alaa-spec-analyst` at medium, `alaa-reviewer` at high, and
`alaa-rule-writer` at medium. All target definitions pin GPT-6.1 Sol. The controller deliberately
used GPT-6 Sol/low only to orchestrate the test; it was never a target-model fallback.

An initial setup failed during Windows UTF-8 decoding before any controller dispatch; explicit
UTF-8 decoding repaired setup. The first actual smoke used an ephemeral controller and failed
to resolve its thread. One cause-specific retry used a fresh persisted read-only controller,
preserving separate evidence and the same target pins. That retry created all three child
tasks, but each received the server error:

> The 'gpt-6.1-sol' model is not supported when using Codex with a ChatGPT account.

The refreshed CLI catalog also omits the target. Installed pin discovery and dispatch are
evidenced, but model acceptance, fixture task execution and role output-contract behavior are
blocked. Served model/effort remain unknown. Fixtures retained their hashes. Controller exit
zero does not make the smoke pass, and fallback **metadata** warnings do not prove model
substitution. This CLI result does not establish availability in a different desktop host.

The retry's last-message path was initially relative to the fixture directory, so its file write
failed. The complete final message was recovered from retained JSONL; the helper now resolves
that output path. No additional smoke was run. Raw runtime evidence remains outside Git;
archived paths are normalized without changing errors or results. Native command strings and output bodies
are represented by hashes, with complete raw output retained outside Git; complete controller
results and server errors are preserved in the archive.

Stop here until this CLI/account accepts the exact target or the user selects another host for
the same bounded smoke. No configuration repair, CLI upgrade, API benchmark or silent model
fallback was performed. Smoke is neither a quality benchmark nor calibration.

## Completion and curation

`IMPLEMENTED`: proven on the identified source snapshot; changes remain uncommitted.
`MERGE_CANDIDATE`: not proven for the complete requested pipeline because activation smoke is
blocked, despite passing source gates and independent review.
`RELEASE_CANDIDATE`: not requested. `PUBLISHED`: not requested.

Curation scanned the approved decision, preservation checks, installation drift and runtime
failures. No new durable candidate passed admission: policy choices already have their owner,
and volatile CLI failures remain task evidence. No memory publication occurred.
