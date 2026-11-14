# Skill pack sentence-level wording pass (2026-11-14)

Third engagement of the same day, after the [Fable 5.2 pack upgrade](../skill-pack-fable52-20261114/report.md) and the [clarity rewrite and body reduction](../skill-pack-clarity-20261114/report.md). Beads plan: `alaa-f0jl8`. This record is dated evidence; verify current repository facts before reusing a conclusion.

## Outcome

Every first-party skill file outside the normative references of `alaa-services-contract` was read by a lane for the wording test in `skills/sohrab/AGENTS.md`. A lane changed only a sentence that failed the test: a verbless fragment, a slash that hid "and" or "or", a noun stack, or an elided predicate. No rule was relocated, merged, added or removed. Facts, numbers, code blocks, tables of values and checker-read literals stayed byte-identical, with one planned exception: the clauses that `alaa-testing-strategy/scripts/check_execution_contracts.py` requires as literals were rewritten together with those literals.

Sixteen lanes changed 253 files (828 insertions, 832 deletions). Most files passed unchanged. The branch `skills-wording-pass` was merged into `main` with `--no-ff` as `c6d4d2dd`; two further repairs landed on `main` as `84188c7d`.

## Lanes

Each lane ran as a general-purpose subagent with requested model `opus`; W11 ran at effort high, the others at medium. A lane made no commit and ran no Beads command. The parent recorded each report under `lanes/` and committed the lane's directories.

| Lane | Skills | Coverage and change | Commit |
|---|---|---|---|
| W1 | alaa-docker-production, alaa-k8s-helm, caas-arvan-kuber | Read in full: 64 files. Changed: 21 files, 41 sentences (docker 30 in 12 files, k8s-helm 3, caas 8 in 6), plus call-form conversions inside edited files. | `328eb97d` |
| W2 | alaa-haproxy, alaa-haproxy-lua, alaa-bash-shell, alaa-makefile | Read in full: 116 Markdown files. Changed: 32 files, about 66 sentences (haproxy about 45 in 21 files, haproxy-lua about 20 in 10, bash-shell 1). alaa-makefile unchanged. Configuration and Lua examples, directive tables and checker-read literals unchanged. | `dfd79fe9` |
| W3 | ansible-generator, ansible-validator, service-runtime-kit-governance, jitsi-platform-architect, alaa-cicd-laravel-postgres | Read: about 70 Markdown files (prose in full; code blocks in three Ansible references skimmed). Changed: 16 files, 24 sentences. service-runtime-kit-governance unchanged. | `315a2a15` |
| W4 | alaa-data-layer, alaa-mongodb-patterns, clickhouse-performance-schema-ops, alaa-signoz-clickhouse-docs, alaa-partitioned-table-fk-audit, alaa-crockford-base32-codecs | Read in full: 68 Markdown files. Changed: 21 files, 30 sentences (data-layer 9 in 5 files, clickhouse 4 in 3, signoz 15 in 13, crockford 2 in 1). alaa-mongodb-patterns and alaa-partitioned-table-fk-audit unchanged. SQL, DDL, codec assets and the conformance corpus byte-identical. | `1ae76104` |
| W5 | alaa-async-messaging, alaa-observability-soc, alaa-arvan-object-storage, tusd-upload-platform | Read in full: 69 Markdown files. Changed: 14 files, 23 sentences (slash stacks; one abstract noun). alaa-arvan-object-storage unchanged. | `e922a1d8` |
| W6 | minio, postman, laravel-architecture, laravel-upgrade, controlled-ops, legacy-path-map, tooling-check, codex-runtime-ops | Read in full: 67 Markdown files. Changed: 9 files in 4 skills, 15 sentences (verbless fragments and slash stacks). Unchanged: alaa-codex-runtime-ops, alaa-legacy-path-map, repository-tooling-capability-check, alaa-laravel-architecture. | `1b5abbdf` |
| W7 | alaa-quasar-app-vite-v3, alaa-frontend-devops, alaa-frontend-doc-annotations, alaa-mono-package, alaa-frontend-developer | Read in full: 96 Markdown files. Changed: 20 files, 47 sentences (Quasar 24 in 9 files, frontend-developer 22 in 10 files, mono-package 1). alaa-frontend-devops and alaa-frontend-doc-annotations unchanged. | `1b18b57e` |
| W8 | alaa-shaka-player, alaa-input-normalization | Read in full: 72 files. Changed: 6 reference files, 11 sentences (Shaka 4 in 3 files, input-normalization 7 in 3). 47 of 50 Shaka Markdown files pass as they are. | `f0db74b9` |
| W9 | alaa-vue-typescript-clean-code, alaa-ui-ux-design-system | Read in full: 47 of 51 files (two .mjs scripts partly read and grepped; one SKILL.md given a light read). Changed: 13 files, 16 wording rewrites and 18 legacy call-form twins removed (vue 13, ui-ux 5). Code blocks, token tables, budget numbers and gates unchanged. | `87d5da96` |
| W10 | alaa-indexeddb-browser-storage, alaa-go-chi-development, alaa-golang-fiber, alaa-ponytail | Read in full: 88 files. Changed: 22 files, 39 sentences (go-chi 14 in 8 files, fiber 4 in 3, indexeddb 21 in 11). alaa-ponytail unchanged. | `7fc7a74b` |
| W11 | checker-bound clauses (opus, high) | Rewrote 33 clauses that alaa-testing-strategy scripts/check_execution_contracts.py requires as literals, and changed each literal in the checker in the same edit: 9 in references/100-test-execution.md, 10 in 110-execution-resources.md, 7 in 120-result-classification.md, 3 in SKILL.md, 3 in alaa-workflow references/workspace-and-integration.md, 1 in alaa-workflow references/context-continuity.md. REQUIREMENTS keeps 205 entries and NORMATIVE_DUPLICATES 101; no literal was deleted or shortened and the matching code is unchanged. 23 of the 33 are also normative-duplicate entries, so the frozen hash was recomputed by the script's own method (sha256 over the sorted owner and clause lines). | `c929d67e` |
| W12 | alaa-php-clean-code, alaa-laravel-job-rabbitmq, alaa-laravel-public-api-contract-pack, alaa-permission-generator, alaa-octane-performance, alaa-phpantom | Read in full: 58 files. Changed: 17 files, 46 sentences (php-clean-code 15, rabbitmq 6, permission-generator 1 markup repair, octane 6, phpantom 18). alaa-laravel-public-api-contract-pack unchanged. | `61ef5dca, bde5670e` |
| W13 | alaa-bale-provider, alaa-sms-provider-mediana, alaa-sms-provider-magfa, alaa-system-design, alaa-algorithms-data-structures, alaa-keyset-pagination, alaa-golang-clean-code-principles | Read in full: 54 Markdown files. Changed: 22 files, 41 sentences (verbless fragments turned into commands; slash stacks). Mediana and Magfa unchanged. | `3f1af64b` |
| W14 | alaa-security-review, alaa-reliability-sla, alaa-trust-gateway-auth | Read in full: 29 files. Changed: 6 reference files, 11 sentences. Security invariants, deny codes, headers and thresholds unchanged. | `22647f24` |
| W15 | vector-rust-observability-pipelines, alaa-golang | Read in full: 40 files. Changed: 9 reference files, 19 sentences (slash stacks in prose expanded to "and" or "or"). Unchanged: both SKILL.md files, 21 of 22 alaa-golang files, the version-pin file. | `bef7bdcb` |
| W16 | alaa-gitlab-ci-cd, alaa-repo-docs, alaa-project-constitution, alaa-memory-os | Read in full: 75 Markdown files. Changed: 15 files, 27 sentences (gitlab 10 in 6 files, repo-docs 1, constitution 7 in 4, memory-os 9 in 4 plus regenerated checksums). Templates, adapter blocks, the size paragraph and quality-bar.md unchanged. | `f56dc834` |

## Checker-bound clauses (W11)

`check_execution_contracts.py` holds 205 required literals and 101 normative-duplicate literals with a frozen inventory hash. W11 rewrote 33 telegraphic clauses and changed each matching literal in the same edit; 23 of them are also normative-duplicate entries, so the lane recomputed the hash with the script's own method. No literal was deleted and the matching code is unchanged. The checker exits `0` on the merged tree.

## Review outcome

Four independent `alaa-instruction-reviewer` runs (read-only, requested `opus`; R3-A at high, the others at medium; each self-reported `claude-opus-5-5` with effort unknown) reviewed every lane commit against the lane brief, starting from each lane's own least-sure list.

| Review | Lanes | Verdict | Major | Minor | Nit |
|---|---|---|---|---|---|
| R3-A | W11, W13, W14 | APPROVED-WITH-NITS | 0 | 2 | 2 |
| R3-B | W1, W2, W3 | APPROVED-WITH-NITS | 0 | 1 | 0 |
| R3-C | W4, W5, W6, W10, W15 | APPROVED-WITH-NITS | 0 | 1 | 1 |
| R3-D | W7, W8, W9, W12, W16 | APPROVED-WITH-NITS | 0 | 1 | 2 |

Dispositions are in `lanes/R3-A.md` to `lanes/R3-D.md`. Eight findings were repaired (`3e79b23e` before the merge, `84188c7d` after it). One nit was accepted as disclosed (a dead pointer in `alaa-trust-gateway-auth` replaced inside a wording commit). One nit stays open: the canonical clause in `alaa-testing-strategy references/100-test-execution.md` now says "the scheduling of phases and reviews" while five unchanged carriers still say "phase/review scheduling".

## Confirmation pass

After the merge, the R3-A reviewer was continued with its context intact and returned `VERDICT: APPROVED`: all eleven repairs confirmed, and the two merged `alaa-trust-gateway-auth` files clean. The record is `lanes/R3-confirmation.md`.

## Merge with a moving main

A parallel session committed five changes to `alaa-trust-gateway-auth` and `alaa-services-contract` on `main` while this pass ran. Git merged the two files both sides touched (`alaa-trust-gateway-auth/references/70-review-and-anti-patterns.md` and `90-source-map.md`) without a conflict. The confirmation pass read both merged files.

## Open items for the owner

A wording pass changes no fact, so each lane reported what it found and left it. Every lane file under `lanes/` lists its items on the line that starts `Reported:` or `Left or reported:`. The classes:

- **Stale dated facts.** Release and end-of-life statements past their own re-verify dates in the Docker, Kubernetes, Ansible, HAProxy, Shaka, Quasar, Vue and design-system references.
- **Statements that disagree inside one skill.** Examples: a required first read against "no reference file is unconditionally required" in `alaa-vue-typescript-clean-code`; an "exactly one place" claim that six files contradict in `alaa-ui-ux-design-system`; deny-code and layer-count disagreements in `alaa-trust-gateway-auth`; row counts in `alaa-keyset-pagination`.
- **Slashes a lane could not resolve from the file.** Left as written and listed per lane.
- **A downloading package runner** named in `alaa-ui-ux-design-system references/85` against the rule in `alaa-vue-typescript-clean-code references/60`.
- **Unproven runtimes.** The Go implementation in `alaa-input-normalization` and the Lua implementation in `alaa-crockford-base32-codecs` were skipped by their conformance harnesses on this host, so their parity is not observed in this run.
- **One term, two wordings.** The "phase/review scheduling" carriers named above.

## Validation observed

On `main` at `84188c7d`, each exited `0`: the four root checkers, `python3 -m unittest scripts/test_install_claude_agents.py`, both orchestrators' `render_agents.py --check`, `validate_pack.py`, `check_agent_grants.py` and `check_agent_contracts.py`, the three `alaa-prompting-guide` policy and grant checkers, `check_execution_contracts.py`, `validate_constitution.py --template assets/constitution-template.md`, and `sha256sum -c SHA256SUMS` in `alaa-memory-os`. No fixture, self-test or model comparison was run; the pack owner excludes them.

## Installation

The pack owner authorized agent installation during this engagement. `python3 scripts/install_claude_agents.py --apply` updated 29 Claude Code agent files and `skills/sohrab/alaa-codex-orchestrator/scripts/install-agents.sh` installed 33 Codex agent files, both from pack version 5.6.0; a second dry run reported no differing file. This proves the files are installed. It does not prove that a running session has reloaded them. This pass changed no agent definition.

## Not done

No push. No tag. The normative references of `alaa-services-contract` were excluded from this pass by plan.
