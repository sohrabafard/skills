# Model migration lane evidence

> Citation notation: `<repo>/` denotes this repository root; resolve it before invoking a command. Path lists use this display prefix only; strip it when reproducing a recorded hash manifest. [Original exact evidence](./model-evidence.raw.txt.gz) preserves the pre-normalization text.

## Scope and authority

Phase B; owned skills: alaa-prompting-guide, alaa-cc-orchestrator,
alaa-codex-orchestrator, alaa-low-noise. Parent owns plan/checkpoint/assessment.
Base: 0e9681c8253de0373a9bbbe4a9ff24a91b38c6db; branch:
codex/sohrab-sonnet55-modernization. Scope was clean before lane edits.
Configured agent: alaa-implementer-sol, gpt-6-astra/high; requested override: none;
observed identity: unknown. Escalation: judgment-dense instruction authoring.
Sandbox declares workspace-write; independent enforcement of role tool restrictions is unknown.

## Design and draft decisions

Canonical Claude policy owns exact IDs and role pins. Migrate its twelve Sonnet profiles
and controlled agent metadata together, retaining efforts as unrun hypotheses. Raise only
their sourced CLI minimum. Preserve Opus/Fable/GPT profiles and historical Sonnet evidence.
Add a current Sonnet reference and route active pointers there. Disabled thinking is no
longer valid; distinguish adaptive operation from the limited between-tools mode. Preserve
signed history in API loops and verify provider tool support instead of exporting API
settings into Claude Code. Explicit completion criteria and required focused checks prevent
low-effort early stopping; bounded scope and stop conditions prevent high-effort expansion.
Keep independent gates. General delegation bias is unmeasured, so no invented family-wide
polarity. Progress requirements concern visible status, never private reasoning.

Reject blanket replacement because history and capabilities differ. Reject changing all
effort pins without comparisons, and reject duplicating policy into low-noise or domain skills.
Replace the orchestrators' unsupported universal watchdog claim and the Claude lead's blanket
ban on verification instructions with shared bounded-observability/proportional-check rules.
Compression pass must retain authority, focus tiers, independence, blockers and resume safety.

## Official evidence (2026-09-29)

Primary research supplied by model_research through the parent; full rendered model pages
were read by that research lane. Native prose/config inspection is this lane's evidence owner.

- https://platform.claude.com/docs/en/models/sonnet-5-5/overview
- https://platform.claude.com/docs/en/models/sonnet-5-5/migration-guide
- https://platform.claude.com/docs/en/models/sonnet-5-5/whats-new-sonnet-5-5
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5
- https://platform.claude.com/docs/en/build-with-claude/effort
- https://code.claude.com/docs/en/model-config

This lane directly read model-config: full ID, minimum 2.1.284, provider-dependent aliases.
Direct web opens of the platform migration/prompting pages were unavailable; one different
Markdown retrieval failed TLS authentication. No further direct-fetch retries. Research-lane
evidence supplies model/API details; no API execution, installation or calibration claimed.

## Verification

All focused commands below returned exit 0. Cwd was repository root, using Python 3.13
with -B; these bounded static commands each completed below one second and were not declared
CPU-heavy. No installations, API model runs or consumer integration tests occurred.
Independent review, link checks and integrated fleet proof belong to Phase D.

| Command (repository root) | Runs | Observed proof |
|---|---:|---|
| python -B <repo>/skills/sohrab/alaa-prompting-guide/scripts/check_claude_model_policy.py | 2 | Canonical policy and 23 projections |
| python -B <repo>/skills/sohrab/alaa-prompting-guide/scripts/check_claude_model_policy.py --self-test | 1 | 38 policy/parser fixtures plus pin/coverage cases |
| python -B <repo>/skills/sohrab/alaa-prompting-guide/scripts/check_claude_agent_evals.py | 1 | Eight unrun comparison records valid |
| python -B <repo>/skills/sohrab/alaa-prompting-guide/scripts/check_claude_agent_evals.py --self-test | 1 | Corpus, identity, precedence, runtime boundaries, fallback and evidence exits |
| python -B <repo>/skills/sohrab/alaa-cc-orchestrator/scripts/check_agent_contracts.py | 1 | Metadata and authority contracts |
| python -B <repo>/skills/sohrab/alaa-cc-orchestrator/scripts/check_agent_contracts.py --self-test | 1 | 14 positive/negative structural cases |
| python -B <repo>/skills/sohrab/alaa-cc-orchestrator/scripts/validate_pack.py | 2 | 22 agents; includes policy, grant and contract checks |
| python -B <repo>/skills/sohrab/alaa-cc-orchestrator/scripts/check_agent_grants.py | 1 | 22 agents match authored native/MCP/skill grants |
| python -B <repo>/skills/sohrab/alaa-codex-orchestrator/scripts/check_agent_contracts.py | 1 | Metadata and authority contracts |
| python -B <repo>/skills/sohrab/alaa-codex-orchestrator/scripts/check_agent_contracts.py --self-test | 1 | 14 positive/negative structural cases |
| python -B <repo>/skills/sohrab/alaa-codex-orchestrator/scripts/render_agents.py --check | 1 | Three generated files unchanged and valid |
| python -B <repo>/skills/sohrab/alaa-codex-orchestrator/scripts/validate_pack.py | 2 | 23 agents valid |
| git diff --check -- skills/sohrab/alaa-prompting-guide skills/sohrab/alaa-cc-orchestrator skills/sohrab/alaa-codex-orchestrator skills/sohrab/alaa-low-noise | 1 | Clean whitespace |

Total: 16 command executions, 13 distinct commands; source proof only. No failed gate.
Diff inspection caught Windows default decoding changing punctuation in eight edited files;
one UTF-8 repair restored original punctuation, then affected pack validators passed again.
The policy recheck followed compression of repeated calibration notes. Prior corpus/self-test
results remain applicable because those tested structures and executable checks did not change.

## Reconciled outcome

Acceptance 3: all twelve active Claude wrapper pins and policy profiles select Sonnet 5.5;
active routes, interface metadata, corpus and fixtures agree. Old Sonnet content is historical
or a negative fixture/migration exclusion. Acceptance 4: GPT/Opus/Fable profiles are preserved;
calibration remains unrun and account/serving identity unknown. Acceptance 5: focused checks,
independent gates, explicit authority, bounded scope and stop conditions survive. Both
orchestrators carry the same new verification and recovery behavior. Low-noise needs no edit:
its existing owner routing and host-observability contract already fit the migration.

Draft decisions above were compressed into final instructions; repeated per-profile caveats
were reduced to one model note. No prose reduction changes the selected decisions. The
new reference is one current-model migration contract; source dates and historical caveats remain.

No SHA256SUMS is present in these four owned skills. The Codex renderer found its existing
manifest/wrappers current; no generated refresh or version bump was needed. The evidence
manifest below covers the changed tracked files and the new reference, excluding this log.

## Compatibility and remaining proof

Minimum supported Claude Code for the migrated profiles is 2.1.284; older hosts must report
unavailable, not substitute. Policy version 1.1.0 deliberately prevents reusing 1.0.0 result
records as new calibration. Roll back policy, corpus and twelve wrapper pins together if
required; historical guidance remains available. No service state, data, dependencies or
installed configuration changed. API replay/provider behaviors require consuming-client tests;
no live Sonnet calibration or performance/security superiority is claimed. Parent Phase D
owns independent correctness/instruction review and integrated verification.


## Read-coverage limitation and resolution

Touched contracts, policy, corpus, executable validators and affected projections were read;
the entire remaining reference/script inventory of all four owned skills was not read in full.
This does not satisfy the dispatch's full-skill read prerequisite. Parent acceptance must keep
that prerequisite outstanding rather than infer complete skill-wide inspection from passing
static checks. This was the first handoff state, now superseded by the full-read reconciliation below. An evidence-file patch initially missed its
context; the corrected exact-heading insertion succeeded without changing source files.

The continuation fully read all 190 files: prompting-guide 96, Claude orchestrator 38,
Codex orchestrator 50, and low-noise 6. Every reference, script, agent, asset, fixture,
manifest, version file and historical/mirror document is included. The ledger records
file paths, consumed ranges and current SHA-256; inventory comparison found zero omissions
or changed unread files before the follow-up correction. This resolves coverage but does
not retroactively claim that the original edits followed the required read-before-edit order.

Reconciliation found one missed implication: both delegation templates retained a universal
between-step narration rule and watchdog rationale contrary to the changed skill bodies.
Draft decision: a long-running dispatch states meaningful progress expectations under the
active host contract, uses bounded invocations, and does not invent a watchdog. Route recovery
to the skill body instead of copying it. Compress the envelope and rationale together;
retain required progress, return bounds, scope, gates and all role-specific fields.
Add paired regression fixtures and include the dispatch check in both pack validators.
Historical documents, deliberate negative fixtures, untouched runtime-specific grants,
installers, renderer and low-noise contracts need no migration change.

## Changed source snapshot

Aggregate SHA-256 (sorted hash/path lines): `b118d167f358c4da6d9437194184a50c0d861e1bf02cfd7c27958bd99ba2ed94`.

```text
62a60722d2afffa2cbaca48ac2bd642148a0072f4ab157f3204d9211fe459a38  skills/sohrab/alaa-cc-orchestrator/SKILL.md
bcee62b91e66865d130cb62a0b4f6e37b5c2634ac584e3d34d90c2939842c1fa  <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-accessibility-reviewer.md
20d97fd040660cfb4934ad4828a68110c1904feeae7c53a10b5d4c532638301e  <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-browser-qa.md
adc72ed146d384ee2c8e7de903f00e181623e3908e5962f48ff6fec5e44710ba  <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-dependency-auditor.md
d78bc2e27dcd8c8cb3e80ca8811f224733082c247cb67478498ea0788e6a836f  <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-documenter.md
b9da8c3b163140c5fa1be45b3ea732042cd9fe4eaa377592a9baef1a714199c7  <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-explorer.md
3043a4578cef46687d0288cb4c1db7cd9ee88d9aab0eb2524a4ed407fd94c3c0  <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-implementer.md
dd2d10b9603d3ef03966eaaf9b345d97002afa101aac04f4abe635db8fb791cb  <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-observability-reviewer.md
e4a79dc03885c0ceeb5606d9b8929778d3f06d62a0173ae414dff21ba9053143  <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-performance-profiler.md
9527a637df24a161372552457c726def1f9b132af0365b820b07dbb48895f76d  <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-release-guardian.md
4721c57074ee904452f59439b010ca0e41d3d8dff5c9b65e8b87555fca6018c7  <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-researcher.md
bea3193c57930ac5a3ee2bf9b7ccc39d9e4900d20f8bed7dec1c1f218a7b52a3  <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-test-strategist.md
82d5319f231eba78a3af3531b49524f781095ae54170b8b517b0362474113612  <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-verifier.md
9fdedd7aa3bcfa37ee984536bcfbc4a93fa4540b5efb321d81a552225fd1669a  <repo>/skills/sohrab/alaa-cc-orchestrator/scripts/check_agent_contracts.py
d523982c3eeeac5c6a4da3fbfc6cd9103e198060f835876983f1a53f3c967e76  skills/sohrab/alaa-codex-orchestrator/SKILL.md
9fdedd7aa3bcfa37ee984536bcfbc4a93fa4540b5efb321d81a552225fd1669a  <repo>/skills/sohrab/alaa-codex-orchestrator/scripts/check_agent_contracts.py
203c85bc80958d3400a2ad4760ea1add9891c32dfa90082a9a3726d17a46afed  skills/sohrab/alaa-prompting-guide/SKILL.md
2c592b27a32b857747fc24aff2218a1b851c5e4928fc069b7a275bd7690881fb  <repo>/skills/sohrab/alaa-prompting-guide/agents/openai.yaml
4d3ebdd310df52afcfbb6a6b23b6f3e53b1e0218e77ce00b93cbbd57c8e67064  <repo>/skills/sohrab/alaa-prompting-guide/assets/claude-model-policy.json
8b8854a3f7e5e8a432492b265ab053ff6675c4e32e2be3c18fff173f8b4c6ece  <repo>/skills/sohrab/alaa-prompting-guide/assets/evals/claude-agent-comparisons.json
60f53ced08910f649c566af256358e2bb46254ed867052eabc2fdb90639d5074  <repo>/skills/sohrab/alaa-prompting-guide/references/00-source-map.md
e2174298f143299553c3803f9f7c965640860659286ee919076cae96b3933b18  <repo>/skills/sohrab/alaa-prompting-guide/references/00-topic-map.md
a4f813b15caceece150383bc31982ed3fb04a95af56d495508251ffe1d4f1859  <repo>/skills/sohrab/alaa-prompting-guide/references/06-invocation-and-composition.md
23a59c554f64345eb98ca2e860dbf7c68b97239b992e90e6b5b81adb21114bfe  <repo>/skills/sohrab/alaa-prompting-guide/references/30-sonnet-5.md
d5b93336cd539a6d7507491c36842774dcdef83a9615dd2545dcfc13464c99ab  <repo>/skills/sohrab/alaa-prompting-guide/references/31-sonnet-5-5.md
8db2279e1f3119f2ecb8d55f77aed31dd6866c950a3c7f8d675ca9b0528ea9fe  <repo>/skills/sohrab/alaa-prompting-guide/references/50-effort-and-thinking.md
35089c86da4a5797501ce9ccda0086149ca5844ff3f97322cd01754b52cc7516  <repo>/skills/sohrab/alaa-prompting-guide/scripts/check_claude_agent_evals.py
1938aa417f253e80f7ba5e0df568f52de43d4ffa399465fcb53293ac84c1b21e  <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/claude-policy/policy-cases.json
```


## Snapshot scope correction (2026-09-29)

The preceding 31-file scope used the unstaged diff and omitted the already-staged new Sonnet 5.5 guide. The complete candidate uses git diff HEAD --name-only plus git ls-files --others --exclude-standard across the same four owned skills. It contains 32 source files. The previous 31 recorded hashes still match; this correction adds the staged guide rather than claiming new test execution. The existing index was not changed by this lane. Prior observed checks remain scoped to their original execution; final independent verification will identify the complete candidate.

Added source: <repo>/skills/sohrab/alaa-prompting-guide/references/31-sonnet-5-5.md; raw-byte SHA-256 d5b93336cd539a6d7507491c36842774dcdef83a9615dd2545dcfc13464c99ab.

Complete snapshot aggregate (sorted SHA-256, two spaces, repository-relative path, final LF): 1f941b4d7824741502030c1c551f057ca3df5f5d2fbddde63f94e4883dc65df4.

```text
62a60722d2afffa2cbaca48ac2bd642148a0072f4ab157f3204d9211fe459a38  skills/sohrab/alaa-cc-orchestrator/SKILL.md
bcee62b91e66865d130cb62a0b4f6e37b5c2634ac584e3d34d90c2939842c1fa  <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-accessibility-reviewer.md
20d97fd040660cfb4934ad4828a68110c1904feeae7c53a10b5d4c532638301e  <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-browser-qa.md
adc72ed146d384ee2c8e7de903f00e181623e3908e5962f48ff6fec5e44710ba  <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-dependency-auditor.md
d78bc2e27dcd8c8cb3e80ca8811f224733082c247cb67478498ea0788e6a836f  <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-documenter.md
b9da8c3b163140c5fa1be45b3ea732042cd9fe4eaa377592a9baef1a714199c7  <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-explorer.md
3043a4578cef46687d0288cb4c1db7cd9ee88d9aab0eb2524a4ed407fd94c3c0  <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-implementer.md
dd2d10b9603d3ef03966eaaf9b345d97002afa101aac04f4abe635db8fb791cb  <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-observability-reviewer.md
e4a79dc03885c0ceeb5606d9b8929778d3f06d62a0173ae414dff21ba9053143  <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-performance-profiler.md
9527a637df24a161372552457c726def1f9b132af0365b820b07dbb48895f76d  <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-release-guardian.md
4721c57074ee904452f59439b010ca0e41d3d8dff5c9b65e8b87555fca6018c7  <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-researcher.md
bea3193c57930ac5a3ee2bf9b7ccc39d9e4900d20f8bed7dec1c1f218a7b52a3  <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-test-strategist.md
82d5319f231eba78a3af3531b49524f781095ae54170b8b517b0362474113612  <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-verifier.md
b64af563443f9f564171ab68357f9689bd65e3810693b9692817cfd12ed8c60d  <repo>/skills/sohrab/alaa-cc-orchestrator/references/delegation-prompts.md
a154afab91672912ca85ae22c64ef2fd4ba04c2a99a16f7b94e45e5ef67ee47c  <repo>/skills/sohrab/alaa-cc-orchestrator/scripts/check_agent_contracts.py
be9267f5523715fd26f0f6c5c71dac3f99827da7ce22a645c17a17c53f88928b  <repo>/skills/sohrab/alaa-cc-orchestrator/scripts/validate_pack.py
d523982c3eeeac5c6a4da3fbfc6cd9103e198060f835876983f1a53f3c967e76  skills/sohrab/alaa-codex-orchestrator/SKILL.md
6759401a2e0f5690c57700dd0d3013fa81059e725ebc58ecfba0f43ca1db0911  <repo>/skills/sohrab/alaa-codex-orchestrator/references/delegation-prompts.md
a154afab91672912ca85ae22c64ef2fd4ba04c2a99a16f7b94e45e5ef67ee47c  <repo>/skills/sohrab/alaa-codex-orchestrator/scripts/check_agent_contracts.py
22413a2dbfc35497b09f4087b5d82df407f640747fb539762e9b8abaa8cabb04  <repo>/skills/sohrab/alaa-codex-orchestrator/scripts/validate_pack.py
203c85bc80958d3400a2ad4760ea1add9891c32dfa90082a9a3726d17a46afed  skills/sohrab/alaa-prompting-guide/SKILL.md
2c592b27a32b857747fc24aff2218a1b851c5e4928fc069b7a275bd7690881fb  <repo>/skills/sohrab/alaa-prompting-guide/agents/openai.yaml
4d3ebdd310df52afcfbb6a6b23b6f3e53b1e0218e77ce00b93cbbd57c8e67064  <repo>/skills/sohrab/alaa-prompting-guide/assets/claude-model-policy.json
8b8854a3f7e5e8a432492b265ab053ff6675c4e32e2be3c18fff173f8b4c6ece  <repo>/skills/sohrab/alaa-prompting-guide/assets/evals/claude-agent-comparisons.json
60f53ced08910f649c566af256358e2bb46254ed867052eabc2fdb90639d5074  <repo>/skills/sohrab/alaa-prompting-guide/references/00-source-map.md
e2174298f143299553c3803f9f7c965640860659286ee919076cae96b3933b18  <repo>/skills/sohrab/alaa-prompting-guide/references/00-topic-map.md
a4f813b15caceece150383bc31982ed3fb04a95af56d495508251ffe1d4f1859  <repo>/skills/sohrab/alaa-prompting-guide/references/06-invocation-and-composition.md
23a59c554f64345eb98ca2e860dbf7c68b97239b992e90e6b5b81adb21114bfe  <repo>/skills/sohrab/alaa-prompting-guide/references/30-sonnet-5.md
d5b93336cd539a6d7507491c36842774dcdef83a9615dd2545dcfc13464c99ab  <repo>/skills/sohrab/alaa-prompting-guide/references/31-sonnet-5-5.md
8db2279e1f3119f2ecb8d55f77aed31dd6866c950a3c7f8d675ca9b0528ea9fe  <repo>/skills/sohrab/alaa-prompting-guide/references/50-effort-and-thinking.md
35089c86da4a5797501ce9ccda0086149ca5844ff3f97322cd01754b52cc7516  <repo>/skills/sohrab/alaa-prompting-guide/scripts/check_claude_agent_evals.py
1938aa417f253e80f7ba5e0df568f52de43d4ffa399465fcb53293ac84c1b21e  <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/claude-policy/policy-cases.json
```


## Full-read continuation ledger

The following files were fully consumed earlier in this lane, including supplied full skill bodies and composed changes. Remaining files are being read in bounded chunks; a coverage record is appended only after its output is inspected. SHA-256 records exact current bytes.

- FULL <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-accessibility-reviewer.md SHA256 bcee62b91e66865d130cb62a0b4f6e37b5c2634ac584e3d34d90c2939842c1fa
- FULL <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-browser-qa.md SHA256 20d97fd040660cfb4934ad4828a68110c1904feeae7c53a10b5d4c532638301e
- FULL <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-dependency-auditor.md SHA256 adc72ed146d384ee2c8e7de903f00e181623e3908e5962f48ff6fec5e44710ba
- FULL <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-documenter.md SHA256 d78bc2e27dcd8c8cb3e80ca8811f224733082c247cb67478498ea0788e6a836f
- FULL <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-explorer.md SHA256 b9da8c3b163140c5fa1be45b3ea732042cd9fe4eaa377592a9baef1a714199c7
- FULL <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-implementer.md SHA256 3043a4578cef46687d0288cb4c1db7cd9ee88d9aab0eb2524a4ed407fd94c3c0
- FULL <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-observability-reviewer.md SHA256 dd2d10b9603d3ef03966eaaf9b345d97002afa101aac04f4abe635db8fb791cb
- FULL <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-performance-profiler.md SHA256 e4a79dc03885c0ceeb5606d9b8929778d3f06d62a0173ae414dff21ba9053143
- FULL <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-release-guardian.md SHA256 9527a637df24a161372552457c726def1f9b132af0365b820b07dbb48895f76d
- FULL <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-researcher.md SHA256 4721c57074ee904452f59439b010ca0e41d3d8dff5c9b65e8b87555fca6018c7
- FULL <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-test-strategist.md SHA256 bea3193c57930ac5a3ee2bf9b7ccc39d9e4900d20f8bed7dec1c1f218a7b52a3
- FULL <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-verifier.md SHA256 82d5319f231eba78a3af3531b49524f781095ae54170b8b517b0362474113612
- FULL <repo>/skills/sohrab/alaa-cc-orchestrator/references/model-effort-policy.md SHA256 2606726c1732fc3b5e00872477fa56aa348c821d6216b93c0ad27ebca8bd3c3d
- FULL <repo>/skills/sohrab/alaa-cc-orchestrator/scripts/check_agent_contracts.py SHA256 9fdedd7aa3bcfa37ee984536bcfbc4a93fa4540b5efb321d81a552225fd1669a
- FULL <repo>/skills/sohrab/alaa-cc-orchestrator/scripts/validate_pack.py SHA256 e64f1e19dadbc3df0156993c3f66be49e7f41b66fdbebd415eb27b8c0abd2b21
- FULL skills/sohrab/alaa-codex-orchestrator/SKILL.md SHA256 d523982c3eeeac5c6a4da3fbfc6cd9103e198060f835876983f1a53f3c967e76
- FULL <repo>/skills/sohrab/alaa-codex-orchestrator/references/model-effort-policy.md SHA256 116d917e82e4e578675f2f95217af392d576e32783ecb22048c08e88263090f7
- FULL <repo>/skills/sohrab/alaa-codex-orchestrator/scripts/check_agent_contracts.py SHA256 9fdedd7aa3bcfa37ee984536bcfbc4a93fa4540b5efb321d81a552225fd1669a
- FULL skills/sohrab/alaa-low-noise/SKILL.md SHA256 b45d36dffcc8fec9ea98acf3bd9729a852b274f447c44f71ed72fdb0966328ad
- FULL <repo>/skills/sohrab/alaa-low-noise/references/90-source-map.md SHA256 a1c167b2a83c57b04d6e5a10204ce2f5d04d0ffd0d3a83876616db5de03bbfcf
- FULL <repo>/skills/sohrab/alaa-low-noise/references/model-output-profiles.md SHA256 6b40830e582823efa079ec81024b1fa1e4f2a7b2b49a602e823b73348c789013
- FULL <repo>/skills/sohrab/alaa-low-noise/references/noise-control-patterns.md SHA256 9d520b504ef0ab6fa0027a31aa4892c7cc1cdc20be2149a949c9557953245ace
- FULL <repo>/skills/sohrab/alaa-low-noise/references/workflow-integration.md SHA256 28d190cae7ca0a01c148f2b1820988d428afd5500a9e47ac264820c010e03040
- FULL skills/sohrab/alaa-prompting-guide/SKILL.md SHA256 203c85bc80958d3400a2ad4760ea1add9891c32dfa90082a9a3726d17a46afed
- FULL <repo>/skills/sohrab/alaa-prompting-guide/assets/evals/claude-agent-comparisons.json SHA256 8b8854a3f7e5e8a432492b265ab053ff6675c4e32e2be3c18fff173f8b4c6ece
- FULL <repo>/skills/sohrab/alaa-prompting-guide/references/00-source-map.md SHA256 60f53ced08910f649c566af256358e2bb46254ed867052eabc2fdb90639d5074
- FULL <repo>/skills/sohrab/alaa-prompting-guide/references/00-topic-map.md SHA256 e2174298f143299553c3803f9f7c965640860659286ee919076cae96b3933b18
- FULL <repo>/skills/sohrab/alaa-prompting-guide/references/06-invocation-and-composition.md SHA256 a4f813b15caceece150383bc31982ed3fb04a95af56d495508251ffe1d4f1859
- FULL <repo>/skills/sohrab/alaa-prompting-guide/references/12-gpt-6.md SHA256 0ed7f8e1c1a095c339d591905a82a704fa4ea75e5504f7dd0c54c56da6210f3d
- FULL <repo>/skills/sohrab/alaa-prompting-guide/references/21-opus-5-5.md SHA256 a66906f627a23553c295eda8c47cbf02876d788a8e576738900601a41e72a069
- FULL <repo>/skills/sohrab/alaa-prompting-guide/references/30-sonnet-5.md SHA256 23a59c554f64345eb98ca2e860dbf7c68b97239b992e90e6b5b81adb21114bfe
- FULL <repo>/skills/sohrab/alaa-prompting-guide/references/31-sonnet-5-5.md SHA256 d5b93336cd539a6d7507491c36842774dcdef83a9615dd2545dcfc13464c99ab
- FULL <repo>/skills/sohrab/alaa-prompting-guide/references/35-haiku-4-5.md SHA256 0c5ddb78b786528e345bf2a06be2285858064e351424425d5a75e9f995f1353a
- FULL <repo>/skills/sohrab/alaa-prompting-guide/references/42-fable-5-1.md SHA256 6e142dfe7f4c7c77165f18a334d12bd10957ca38760c4ba6fb374fc01c5115b1
- FULL <repo>/skills/sohrab/alaa-prompting-guide/references/50-effort-and-thinking.md SHA256 8db2279e1f3119f2ecb8d55f77aed31dd6866c950a3c7f8d675ca9b0528ea9fe
- FULL <repo>/skills/sohrab/alaa-prompting-guide/references/60-skill-authoring.md SHA256 8c8271e0c30b1dd326091432da41dff4e1ca6b22d7d16bf851bb82be3df61ebc
- FULL <repo>/skills/sohrab/alaa-prompting-guide/references/90-model-selection.md SHA256 7a5fecbef3c320591c77470da517bcb097f08ab8bdfeadbd290264e909a47702
- FULL <repo>/skills/sohrab/alaa-prompting-guide/references/93-claude-evaluation.md SHA256 47a118efff1ea5ae079f5815eb428e6d0914ecc98f52ad476bb248abe7558d8c
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/check_claude_agent_evals.py SHA256 35089c86da4a5797501ce9ccda0086149ca5844ff3f97322cd01754b52cc7516
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/check_claude_model_policy.py SHA256 d86002dfd4e65afc1e0760f61eeb8435bb49eac05749f69f8bc354de5a6283cb
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/claude_model_policy.py SHA256 85953698538693d86934a95c3adf9eab2b1352eae272a0aa5fc4ba2fec1b6f53
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/claude-policy/policy-cases.json SHA256 1938aa417f253e80f7ba5e0df568f52de43d4ffa399465fcb53293ac84c1b21e
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/agents/openai.yaml L1-6 SHA256 2c592b27a32b857747fc24aff2218a1b851c5e4928fc069b7a275bd7690881fb
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/assets/claude-model-policy.json L1-546 SHA256 4d3ebdd310df52afcfbb6a6b23b6f3e53b1e0218e77ce00b93cbbd57c8e67064
- FULL <repo>/skills/sohrab/alaa-prompting-guide/agents/openai.yaml SHA256 2c592b27a32b857747fc24aff2218a1b851c5e4928fc069b7a275bd7690881fb
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/assets/claude-model-policy.json L547-703 SHA256 4d3ebdd310df52afcfbb6a6b23b6f3e53b1e0218e77ce00b93cbbd57c8e67064
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/assets/codex-model-policy.json L1-212 SHA256 7ffd3d7ed719080fc59bfddcf20d078fed8cd72af3275fc6941c0e46d114a027
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/assets/evals/agent-comparisons.json L1-177 SHA256 09eb2c69464fbc478c2916c294f6d84fbb3deb9895405ea3da03d4ac6817c9a8
- FULL <repo>/skills/sohrab/alaa-prompting-guide/assets/claude-model-policy.json SHA256 4d3ebdd310df52afcfbb6a6b23b6f3e53b1e0218e77ce00b93cbbd57c8e67064
- FULL <repo>/skills/sohrab/alaa-prompting-guide/assets/codex-model-policy.json SHA256 7ffd3d7ed719080fc59bfddcf20d078fed8cd72af3275fc6941c0e46d114a027
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/assets/evals/agent-comparisons.json L178-241 SHA256 09eb2c69464fbc478c2916c294f6d84fbb3deb9895405ea3da03d4ac6817c9a8
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/assets/rule-writer/claude/alaa-rule-writer.md L1-39 SHA256 a2a4ccf6f9786bea27eb175bed28b7aaf430e33f4cc8753965d3d46ff06dc6ce
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/assets/rule-writer/codex/alaa-rule-writer.toml L1-38 SHA256 d2cec7e70be9b586f8c827899be27856db3ad736fde482fd24252b240aa1d23c
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/assets/rule-writer/contract.md L1-29 SHA256 aee2ad96fb3f6709debda793701474f992a48b15837426f228a6be03ebbc57c6
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/assets/rule-writer/dispatch.md L1-20 SHA256 6d42cf3cede1b8f1ab3dd5d0e1158a1216a8c96a4d455a8212dba5574a8107bb
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/references/10-gpt-5-6.md L1-42 SHA256 0a2b9d21817d8d3cea76b4066a7e4ddbea766b0f801eabc84e50c39d9f0c8021
- FULL <repo>/skills/sohrab/alaa-prompting-guide/assets/evals/agent-comparisons.json SHA256 09eb2c69464fbc478c2916c294f6d84fbb3deb9895405ea3da03d4ac6817c9a8
- FULL <repo>/skills/sohrab/alaa-prompting-guide/assets/rule-writer/claude/alaa-rule-writer.md SHA256 a2a4ccf6f9786bea27eb175bed28b7aaf430e33f4cc8753965d3d46ff06dc6ce
- FULL <repo>/skills/sohrab/alaa-prompting-guide/assets/rule-writer/codex/alaa-rule-writer.toml SHA256 d2cec7e70be9b586f8c827899be27856db3ad736fde482fd24252b240aa1d23c
- FULL <repo>/skills/sohrab/alaa-prompting-guide/assets/rule-writer/contract.md SHA256 aee2ad96fb3f6709debda793701474f992a48b15837426f228a6be03ebbc57c6
- FULL <repo>/skills/sohrab/alaa-prompting-guide/assets/rule-writer/dispatch.md SHA256 6d42cf3cede1b8f1ab3dd5d0e1158a1216a8c96a4d455a8212dba5574a8107bb
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/references/10-gpt-5-6.md L43-124 SHA256 0a2b9d21817d8d3cea76b4066a7e4ddbea766b0f801eabc84e50c39d9f0c8021
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/references/11-codex-runtime-features.md L1-102 SHA256 4e4a1f2876a8a00d5153fcf2d7745d38e0b944f5bcb199319053dbdc402086a5
- FULL <repo>/skills/sohrab/alaa-prompting-guide/references/10-gpt-5-6.md SHA256 0a2b9d21817d8d3cea76b4066a7e4ddbea766b0f801eabc84e50c39d9f0c8021
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/references/11-codex-runtime-features.md L103-145 SHA256 4e4a1f2876a8a00d5153fcf2d7745d38e0b944f5bcb199319053dbdc402086a5
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/references/20-opus-5.md L1-131 SHA256 ff303b3c316c7682d9df4c3c69e6ac2bf3bc11d317dd5dcf72cd3e4baab9d8a4
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/references/40-fable-5.md L1-25 SHA256 f5f57f1c97475e38f87c837c65f40bb730ddbe5f34565bdd453139c4e381c2ab
- FULL <repo>/skills/sohrab/alaa-prompting-guide/references/11-codex-runtime-features.md SHA256 4e4a1f2876a8a00d5153fcf2d7745d38e0b944f5bcb199319053dbdc402086a5
- FULL <repo>/skills/sohrab/alaa-prompting-guide/references/20-opus-5.md SHA256 ff303b3c316c7682d9df4c3c69e6ac2bf3bc11d317dd5dcf72cd3e4baab9d8a4
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/references/40-fable-5.md L26-155 SHA256 f5f57f1c97475e38f87c837c65f40bb730ddbe5f34565bdd453139c4e381c2ab
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/references/41-claude-code-runtime-features.md L1-92 SHA256 b1e031480dc8fb02756defef63ea161ca8a64538d43b42c82a4ff77506732f4f
- FULL <repo>/skills/sohrab/alaa-prompting-guide/references/40-fable-5.md SHA256 f5f57f1c97475e38f87c837c65f40bb730ddbe5f34565bdd453139c4e381c2ab
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/references/41-claude-code-runtime-features.md L93-182 SHA256 b1e031480dc8fb02756defef63ea161ca8a64538d43b42c82a4ff77506732f4f
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/references/61-skill-platform-mechanics.md L1-43 SHA256 8440ef4c55375d287e07c2aca40313fba939701e4394bb8b7370aae056189657
- FULL <repo>/skills/sohrab/alaa-prompting-guide/references/41-claude-code-runtime-features.md SHA256 b1e031480dc8fb02756defef63ea161ca8a64538d43b42c82a4ff77506732f4f
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/references/61-skill-platform-mechanics.md L44-58 SHA256 8440ef4c55375d287e07c2aca40313fba939701e4394bb8b7370aae056189657
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/references/70-agent-instruction-files.md L1-127 SHA256 349e1be2bc49893682c208d91214e164d0d64f4948ce1277d26c78b0808cc694
- FULL <repo>/skills/sohrab/alaa-prompting-guide/references/61-skill-platform-mechanics.md SHA256 8440ef4c55375d287e07c2aca40313fba939701e4394bb8b7370aae056189657
- FULL <repo>/skills/sohrab/alaa-prompting-guide/references/70-agent-instruction-files.md SHA256 349e1be2bc49893682c208d91214e164d0d64f4948ce1277d26c78b0808cc694
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/references/80-subagent-authoring.md L1-159 SHA256 ad6c507dbbe3423b4d52bd5c5349008beb11824d0744334218f9f1c1d108b08d
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/references/92-agent-evaluation.md L1-38 SHA256 d8cb52e56617107ce9c314a14e5d6e1871287bdb3cc15ea1075ab3c84d115817
- FULL <repo>/skills/sohrab/alaa-prompting-guide/references/80-subagent-authoring.md SHA256 ad6c507dbbe3423b4d52bd5c5349008beb11824d0744334218f9f1c1d108b08d
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/references/92-agent-evaluation.md L39-68 SHA256 d8cb52e56617107ce9c314a14e5d6e1871287bdb3cc15ea1075ab3c84d115817
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/check_agent_evals.py L1-212 SHA256 0e0aa7cfd870929e80fe4d3928e6fe874793f7cda84f2f4e0c5abc5f24e09c71
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/check_codex_model_policy.py L1-86 SHA256 a8fcd13d92ca5e0dc4e734fb783db30f2f38d5248d288ef32ec84aa7f6471d0d
- FULL <repo>/skills/sohrab/alaa-prompting-guide/references/92-agent-evaluation.md SHA256 d8cb52e56617107ce9c314a14e5d6e1871287bdb3cc15ea1075ab3c84d115817
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/check_agent_evals.py SHA256 0e0aa7cfd870929e80fe4d3928e6fe874793f7cda84f2f4e0c5abc5f24e09c71
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/check_codex_model_policy.py SHA256 a8fcd13d92ca5e0dc4e734fb783db30f2f38d5248d288ef32ec84aa7f6471d0d
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/check_rule_writer_grants.py L1-431 SHA256 f302d14d09dab76615293d19a63ee6afc31f5a643165b3b79c7effe4146820c5
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/check_rule_writer_grants.py L432-448 SHA256 f302d14d09dab76615293d19a63ee6afc31f5a643165b3b79c7effe4146820c5
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/codex_model_policy.py L1-125 SHA256 bb1a7388ab245bb096d5f25f0a76d1d3a0ff65f8c21234367f2320c7a1cb2541
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/claude-policy/duplicate.json L1-1 SHA256 ef99a162b17520320cf141fe3ff0574b99d659919be45441acf627c686bc5092
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/claude-policy/malformed.json L1-1 SHA256 7c0bb0046634c2a3cd53224c0bf665eb88f4cdffb06ada9d3d0c8f1b34252f41
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/claude-policy/red-anchor.md L1-5 SHA256 fc716ad4258916ca184215a2440953997560427c5bd30cdf0516a216e08476b8
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/claude-policy/red-duplicate.md L1-6 SHA256 19740d40dd5989a9f56556c3af78a828a00f702795db76fe65b85547c2388457
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/claude-policy/red-flow.md L1-5 SHA256 4c734339be90e2903ea3352396214aeec3ced404daa94ca9d4824842ebe5b6c9
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/claude-policy/red-unterminated.md L1-5 SHA256 e85b84ca87a47f8c18808112870bef55d8ee61c71c751ae553fa57b7e12be12b
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/green/assets/rule-writer/claude/alaa-rule-writer.md L1-12 SHA256 4dd71cf4cc37b96d593d8ca229a2190f463d1dfd4522096e4722186912dce37f
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/green/assets/rule-writer/codex/alaa-rule-writer.toml L1-11 SHA256 1fc85208a56fc0ad09110005e401c90545a7b26eb82cd36b83fc9b9730757574
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/green/assets/rule-writer/contract.md L1-5 SHA256 7e6088b19609626e6e1743efb1c84be5873c30b2e6a42ed1ed3990ef53d81da9
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/green/references/10-detail.md L1-3 SHA256 9160e781ec2eb9a84d325bf7b17cb2066ac4f4749b2866b5a2d5bb5ad2e92c1d
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g1-missing-codex-wrapper/assets/rule-writer/claude/alaa-rule-writer.md L1-12 SHA256 4dd71cf4cc37b96d593d8ca229a2190f463d1dfd4522096e4722186912dce37f
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g1-missing-codex-wrapper/assets/rule-writer/contract.md L1-5 SHA256 7e6088b19609626e6e1743efb1c84be5873c30b2e6a42ed1ed3990ef53d81da9
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g1-missing-codex-wrapper/references/10-detail.md L1-3 SHA256 9160e781ec2eb9a84d325bf7b17cb2066ac4f4749b2866b5a2d5bb5ad2e92c1d
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g10-unpreloaded-skill/assets/rule-writer/claude/alaa-rule-writer.md L1-10 SHA256 fc092eb1c0f339145c256a0977b8a459fc33466b1d49a44f918850c59a071125
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g10-unpreloaded-skill/assets/rule-writer/codex/alaa-rule-writer.toml L1-11 SHA256 1fc85208a56fc0ad09110005e401c90545a7b26eb82cd36b83fc9b9730757574
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g10-unpreloaded-skill/assets/rule-writer/contract.md L1-5 SHA256 7e6088b19609626e6e1743efb1c84be5873c30b2e6a42ed1ed3990ef53d81da9
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g10-unpreloaded-skill/references/10-detail.md L1-3 SHA256 9160e781ec2eb9a84d325bf7b17cb2066ac4f4749b2866b5a2d5bb5ad2e92c1d
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g2-claude-grants-write/assets/rule-writer/claude/alaa-rule-writer.md L1-12 SHA256 22fededd0237e30dc4f9bb97eb39eb80d2c8dda4e6a82308a2a50e8a91cdf703
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g2-claude-grants-write/assets/rule-writer/codex/alaa-rule-writer.toml L1-11 SHA256 1fc85208a56fc0ad09110005e401c90545a7b26eb82cd36b83fc9b9730757574
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g2-claude-grants-write/assets/rule-writer/contract.md L1-5 SHA256 7e6088b19609626e6e1743efb1c84be5873c30b2e6a42ed1ed3990ef53d81da9
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g2-claude-grants-write/references/10-detail.md L1-3 SHA256 9160e781ec2eb9a84d325bf7b17cb2066ac4f4749b2866b5a2d5bb5ad2e92c1d
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g3-codex-grants-mcp/assets/rule-writer/claude/alaa-rule-writer.md L1-12 SHA256 4dd71cf4cc37b96d593d8ca229a2190f463d1dfd4522096e4722186912dce37f
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g3-codex-grants-mcp/assets/rule-writer/codex/alaa-rule-writer.toml L1-12 SHA256 f75c4245ccdfbbb9a2e3b5730f27a405b2c56b928864325cc23676cedbcd3b9a
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g3-codex-grants-mcp/assets/rule-writer/contract.md L1-5 SHA256 7e6088b19609626e6e1743efb1c84be5873c30b2e6a42ed1ed3990ef53d81da9
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g3-codex-grants-mcp/references/10-detail.md L1-3 SHA256 9160e781ec2eb9a84d325bf7b17cb2066ac4f4749b2866b5a2d5bb5ad2e92c1d
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g4-codex-not-read-only/assets/rule-writer/claude/alaa-rule-writer.md L1-12 SHA256 4dd71cf4cc37b96d593d8ca229a2190f463d1dfd4522096e4722186912dce37f
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g4-codex-not-read-only/assets/rule-writer/codex/alaa-rule-writer.toml L1-11 SHA256 39dacbbc8a310dff9e1c7c9034695dc40910a3d39e42b0b7f5f09755996d1367
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g4-codex-not-read-only/assets/rule-writer/contract.md L1-5 SHA256 7e6088b19609626e6e1743efb1c84be5873c30b2e6a42ed1ed3990ef53d81da9
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g4-codex-not-read-only/references/10-detail.md L1-3 SHA256 9160e781ec2eb9a84d325bf7b17cb2066ac4f4749b2866b5a2d5bb5ad2e92c1d
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g5-contract-drift/assets/rule-writer/claude/alaa-rule-writer.md L1-12 SHA256 4dd71cf4cc37b96d593d8ca229a2190f463d1dfd4522096e4722186912dce37f
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g5-contract-drift/assets/rule-writer/codex/alaa-rule-writer.toml L1-11 SHA256 53fbc06670542a479eca9bee99964cee991b751335ae7f5e3794fcf39296c654
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g5-contract-drift/assets/rule-writer/contract.md L1-5 SHA256 7e6088b19609626e6e1743efb1c84be5873c30b2e6a42ed1ed3990ef53d81da9
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g5-contract-drift/references/10-detail.md L1-3 SHA256 9160e781ec2eb9a84d325bf7b17cb2066ac4f4749b2866b5a2d5bb5ad2e92c1d
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g5-toml-escape-drift/assets/rule-writer/claude/alaa-rule-writer.md L1-13 SHA256 6910b8f08088c119d8d9cac9a9ae8234fecb3e508e51af7a2502665991ae0086
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g5-toml-escape-drift/assets/rule-writer/codex/alaa-rule-writer.toml L1-12 SHA256 57b8c8c6136652026b8357b0e0ee6f8199dc0d012666fc06f22357875da58b13
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g5-toml-escape-drift/assets/rule-writer/contract.md L1-6 SHA256 bec51d9724827c23db5ebf00f96959ea78e108e614bc1f9b77baeba86de56e50
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g5-toml-escape-drift/references/10-detail.md L1-3 SHA256 9160e781ec2eb9a84d325bf7b17cb2066ac4f4749b2866b5a2d5bb5ad2e92c1d
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g6-identity-line/assets/rule-writer/claude/alaa-rule-writer.md L1-14 SHA256 70487dd49dd779a8706e8ab0c76557735ac4c3b238c29fc8887113d519c042c4
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g6-identity-line/assets/rule-writer/codex/alaa-rule-writer.toml L1-13 SHA256 af2c17a30bba2d1b1444927b7be70ca6169e391bd499a9654b2f28042fc8fd8c
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g6-identity-line/assets/rule-writer/contract.md L1-7 SHA256 a0daffd6c0c65beccf0b5bf161dc15b5cb583f51c433405b50ad5efc65875f40
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g6-identity-line/references/10-detail.md L1-3 SHA256 9160e781ec2eb9a84d325bf7b17cb2066ac4f4749b2866b5a2d5bb5ad2e92c1d
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g7-dangling-doctrine-path/assets/rule-writer/claude/alaa-rule-writer.md L1-12 SHA256 4dd71cf4cc37b96d593d8ca229a2190f463d1dfd4522096e4722186912dce37f
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/check_rule_writer_grants.py SHA256 f302d14d09dab76615293d19a63ee6afc31f5a643165b3b79c7effe4146820c5
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/codex_model_policy.py SHA256 bb1a7388ab245bb096d5f25f0a76d1d3a0ff65f8c21234367f2320c7a1cb2541
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/claude-policy/duplicate.json SHA256 ef99a162b17520320cf141fe3ff0574b99d659919be45441acf627c686bc5092
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/claude-policy/malformed.json SHA256 7c0bb0046634c2a3cd53224c0bf665eb88f4cdffb06ada9d3d0c8f1b34252f41
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/claude-policy/red-anchor.md SHA256 fc716ad4258916ca184215a2440953997560427c5bd30cdf0516a216e08476b8
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/claude-policy/red-duplicate.md SHA256 19740d40dd5989a9f56556c3af78a828a00f702795db76fe65b85547c2388457
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/claude-policy/red-flow.md SHA256 4c734339be90e2903ea3352396214aeec3ced404daa94ca9d4824842ebe5b6c9
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/claude-policy/red-unterminated.md SHA256 e85b84ca87a47f8c18808112870bef55d8ee61c71c751ae553fa57b7e12be12b
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/green/assets/rule-writer/claude/alaa-rule-writer.md SHA256 4dd71cf4cc37b96d593d8ca229a2190f463d1dfd4522096e4722186912dce37f
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/green/assets/rule-writer/codex/alaa-rule-writer.toml SHA256 1fc85208a56fc0ad09110005e401c90545a7b26eb82cd36b83fc9b9730757574
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/green/assets/rule-writer/contract.md SHA256 7e6088b19609626e6e1743efb1c84be5873c30b2e6a42ed1ed3990ef53d81da9
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/green/references/10-detail.md SHA256 9160e781ec2eb9a84d325bf7b17cb2066ac4f4749b2866b5a2d5bb5ad2e92c1d
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g1-missing-codex-wrapper/assets/rule-writer/claude/alaa-rule-writer.md SHA256 4dd71cf4cc37b96d593d8ca229a2190f463d1dfd4522096e4722186912dce37f
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g1-missing-codex-wrapper/assets/rule-writer/contract.md SHA256 7e6088b19609626e6e1743efb1c84be5873c30b2e6a42ed1ed3990ef53d81da9
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g1-missing-codex-wrapper/references/10-detail.md SHA256 9160e781ec2eb9a84d325bf7b17cb2066ac4f4749b2866b5a2d5bb5ad2e92c1d
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g10-unpreloaded-skill/assets/rule-writer/claude/alaa-rule-writer.md SHA256 fc092eb1c0f339145c256a0977b8a459fc33466b1d49a44f918850c59a071125
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g10-unpreloaded-skill/assets/rule-writer/codex/alaa-rule-writer.toml SHA256 1fc85208a56fc0ad09110005e401c90545a7b26eb82cd36b83fc9b9730757574
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g10-unpreloaded-skill/assets/rule-writer/contract.md SHA256 7e6088b19609626e6e1743efb1c84be5873c30b2e6a42ed1ed3990ef53d81da9
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g10-unpreloaded-skill/references/10-detail.md SHA256 9160e781ec2eb9a84d325bf7b17cb2066ac4f4749b2866b5a2d5bb5ad2e92c1d
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g2-claude-grants-write/assets/rule-writer/claude/alaa-rule-writer.md SHA256 22fededd0237e30dc4f9bb97eb39eb80d2c8dda4e6a82308a2a50e8a91cdf703
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g2-claude-grants-write/assets/rule-writer/codex/alaa-rule-writer.toml SHA256 1fc85208a56fc0ad09110005e401c90545a7b26eb82cd36b83fc9b9730757574
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g2-claude-grants-write/assets/rule-writer/contract.md SHA256 7e6088b19609626e6e1743efb1c84be5873c30b2e6a42ed1ed3990ef53d81da9
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g2-claude-grants-write/references/10-detail.md SHA256 9160e781ec2eb9a84d325bf7b17cb2066ac4f4749b2866b5a2d5bb5ad2e92c1d
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g3-codex-grants-mcp/assets/rule-writer/claude/alaa-rule-writer.md SHA256 4dd71cf4cc37b96d593d8ca229a2190f463d1dfd4522096e4722186912dce37f
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g3-codex-grants-mcp/assets/rule-writer/codex/alaa-rule-writer.toml SHA256 f75c4245ccdfbbb9a2e3b5730f27a405b2c56b928864325cc23676cedbcd3b9a
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g3-codex-grants-mcp/assets/rule-writer/contract.md SHA256 7e6088b19609626e6e1743efb1c84be5873c30b2e6a42ed1ed3990ef53d81da9
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g3-codex-grants-mcp/references/10-detail.md SHA256 9160e781ec2eb9a84d325bf7b17cb2066ac4f4749b2866b5a2d5bb5ad2e92c1d
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g4-codex-not-read-only/assets/rule-writer/claude/alaa-rule-writer.md SHA256 4dd71cf4cc37b96d593d8ca229a2190f463d1dfd4522096e4722186912dce37f
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g4-codex-not-read-only/assets/rule-writer/codex/alaa-rule-writer.toml SHA256 39dacbbc8a310dff9e1c7c9034695dc40910a3d39e42b0b7f5f09755996d1367
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g4-codex-not-read-only/assets/rule-writer/contract.md SHA256 7e6088b19609626e6e1743efb1c84be5873c30b2e6a42ed1ed3990ef53d81da9
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g4-codex-not-read-only/references/10-detail.md SHA256 9160e781ec2eb9a84d325bf7b17cb2066ac4f4749b2866b5a2d5bb5ad2e92c1d
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g5-contract-drift/assets/rule-writer/claude/alaa-rule-writer.md SHA256 4dd71cf4cc37b96d593d8ca229a2190f463d1dfd4522096e4722186912dce37f
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g5-contract-drift/assets/rule-writer/codex/alaa-rule-writer.toml SHA256 53fbc06670542a479eca9bee99964cee991b751335ae7f5e3794fcf39296c654
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g5-contract-drift/assets/rule-writer/contract.md SHA256 7e6088b19609626e6e1743efb1c84be5873c30b2e6a42ed1ed3990ef53d81da9
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g5-contract-drift/references/10-detail.md SHA256 9160e781ec2eb9a84d325bf7b17cb2066ac4f4749b2866b5a2d5bb5ad2e92c1d
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g5-toml-escape-drift/assets/rule-writer/claude/alaa-rule-writer.md SHA256 6910b8f08088c119d8d9cac9a9ae8234fecb3e508e51af7a2502665991ae0086
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g5-toml-escape-drift/assets/rule-writer/codex/alaa-rule-writer.toml SHA256 57b8c8c6136652026b8357b0e0ee6f8199dc0d012666fc06f22357875da58b13
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g5-toml-escape-drift/assets/rule-writer/contract.md SHA256 bec51d9724827c23db5ebf00f96959ea78e108e614bc1f9b77baeba86de56e50
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g5-toml-escape-drift/references/10-detail.md SHA256 9160e781ec2eb9a84d325bf7b17cb2066ac4f4749b2866b5a2d5bb5ad2e92c1d
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g6-identity-line/assets/rule-writer/claude/alaa-rule-writer.md SHA256 70487dd49dd779a8706e8ab0c76557735ac4c3b238c29fc8887113d519c042c4
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g6-identity-line/assets/rule-writer/codex/alaa-rule-writer.toml SHA256 af2c17a30bba2d1b1444927b7be70ca6169e391bd499a9654b2f28042fc8fd8c
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g6-identity-line/assets/rule-writer/contract.md SHA256 a0daffd6c0c65beccf0b5bf161dc15b5cb583f51c433405b50ad5efc65875f40
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g6-identity-line/references/10-detail.md SHA256 9160e781ec2eb9a84d325bf7b17cb2066ac4f4749b2866b5a2d5bb5ad2e92c1d
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g7-dangling-doctrine-path/assets/rule-writer/claude/alaa-rule-writer.md SHA256 4dd71cf4cc37b96d593d8ca229a2190f463d1dfd4522096e4722186912dce37f
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g7-dangling-doctrine-path/assets/rule-writer/codex/alaa-rule-writer.toml L1-11 SHA256 1fc85208a56fc0ad09110005e401c90545a7b26eb82cd36b83fc9b9730757574
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g7-dangling-doctrine-path/assets/rule-writer/contract.md L1-5 SHA256 7e6088b19609626e6e1743efb1c84be5873c30b2e6a42ed1ed3990ef53d81da9
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g8-description-mismatch/assets/rule-writer/claude/alaa-rule-writer.md L1-12 SHA256 4dd71cf4cc37b96d593d8ca229a2190f463d1dfd4522096e4722186912dce37f
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g8-description-mismatch/assets/rule-writer/codex/alaa-rule-writer.toml L1-11 SHA256 565fc2ff7d00e54d079798307faaf7aab0c7680cb498bbecc3f3881b5525d1e9
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g8-description-mismatch/assets/rule-writer/contract.md L1-5 SHA256 7e6088b19609626e6e1743efb1c84be5873c30b2e6a42ed1ed3990ef53d81da9
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g8-description-mismatch/references/10-detail.md L1-3 SHA256 9160e781ec2eb9a84d325bf7b17cb2066ac4f4749b2866b5a2d5bb5ad2e92c1d
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g9-effort-max/assets/rule-writer/claude/alaa-rule-writer.md L1-14 SHA256 9456658c7875aa98b8b3d7e1f6f58841d86b11d58b64f260698a9f4285d4cf7d
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g9-effort-max/assets/rule-writer/codex/alaa-rule-writer.toml L1-12 SHA256 d85082cd42da918df2085e47f1e66bdd9bb50945c89b101ddf4fd7b23de0e1ad
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g9-effort-max/assets/rule-writer/contract.md L1-5 SHA256 7e6088b19609626e6e1743efb1c84be5873c30b2e6a42ed1ed3990ef53d81da9
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g9-effort-max/references/10-detail.md L1-3 SHA256 9160e781ec2eb9a84d325bf7b17cb2066ac4f4749b2866b5a2d5bb5ad2e92c1d
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-unparseable-toml/assets/rule-writer/claude/alaa-rule-writer.md L1-12 SHA256 2cea7c1e211f1a607c4fac883bb5ca241b04cf1ca618a98aac9547ded32947fc
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-unparseable-toml/assets/rule-writer/codex/alaa-rule-writer.toml L1-11 SHA256 ae5978b3b8c07992e11ce2b0caef85238da72e2d768bff8616fbf6f6103c5542
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-unparseable-toml/assets/rule-writer/contract.md L1-5 SHA256 2180315efda961511f0a3d87a16ac74af0dbb0eb918869ca61e97b4ffbda5b4a
- READ-DONE <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-unparseable-toml/references/10-detail.md L1-3 SHA256 9160e781ec2eb9a84d325bf7b17cb2066ac4f4749b2866b5a2d5bb5ad2e92c1d
- READ-DONE <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-adversarial-reviewer.md L1-40 SHA256 29d3fd27ffca50b7842e7a519f56486fadab5cccb57f4bc66a622903b5304114
- READ-DONE <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-api-contract-reviewer.md L1-45 SHA256 c40e9f473eb1595f028edf0b729146728dc3e86bb05ce8d3ea6f8fd6d9ff30ac
- READ-DONE <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-architecture-critic.md L1-52 SHA256 258b877f6fc6b36b75d92e182b0093c344381c40982e36e7a90518620ebd2cff
- READ-DONE <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-failure-analyst.md L1-38 SHA256 0c1e561b4876d805dd170a59de33c9dcbad447d62944791184aa3c39be966a75
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g7-dangling-doctrine-path/assets/rule-writer/codex/alaa-rule-writer.toml SHA256 1fc85208a56fc0ad09110005e401c90545a7b26eb82cd36b83fc9b9730757574
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g7-dangling-doctrine-path/assets/rule-writer/contract.md SHA256 7e6088b19609626e6e1743efb1c84be5873c30b2e6a42ed1ed3990ef53d81da9
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g8-description-mismatch/assets/rule-writer/claude/alaa-rule-writer.md SHA256 4dd71cf4cc37b96d593d8ca229a2190f463d1dfd4522096e4722186912dce37f
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g8-description-mismatch/assets/rule-writer/codex/alaa-rule-writer.toml SHA256 565fc2ff7d00e54d079798307faaf7aab0c7680cb498bbecc3f3881b5525d1e9
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g8-description-mismatch/assets/rule-writer/contract.md SHA256 7e6088b19609626e6e1743efb1c84be5873c30b2e6a42ed1ed3990ef53d81da9
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g8-description-mismatch/references/10-detail.md SHA256 9160e781ec2eb9a84d325bf7b17cb2066ac4f4749b2866b5a2d5bb5ad2e92c1d
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g9-effort-max/assets/rule-writer/claude/alaa-rule-writer.md SHA256 9456658c7875aa98b8b3d7e1f6f58841d86b11d58b64f260698a9f4285d4cf7d
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g9-effort-max/assets/rule-writer/codex/alaa-rule-writer.toml SHA256 d85082cd42da918df2085e47f1e66bdd9bb50945c89b101ddf4fd7b23de0e1ad
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g9-effort-max/assets/rule-writer/contract.md SHA256 7e6088b19609626e6e1743efb1c84be5873c30b2e6a42ed1ed3990ef53d81da9
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-g9-effort-max/references/10-detail.md SHA256 9160e781ec2eb9a84d325bf7b17cb2066ac4f4749b2866b5a2d5bb5ad2e92c1d
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-unparseable-toml/assets/rule-writer/claude/alaa-rule-writer.md SHA256 2cea7c1e211f1a607c4fac883bb5ca241b04cf1ca618a98aac9547ded32947fc
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-unparseable-toml/assets/rule-writer/codex/alaa-rule-writer.toml SHA256 ae5978b3b8c07992e11ce2b0caef85238da72e2d768bff8616fbf6f6103c5542
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-unparseable-toml/assets/rule-writer/contract.md SHA256 2180315efda961511f0a3d87a16ac74af0dbb0eb918869ca61e97b4ffbda5b4a
- FULL <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/rule-writer/red-unparseable-toml/references/10-detail.md SHA256 9160e781ec2eb9a84d325bf7b17cb2066ac4f4749b2866b5a2d5bb5ad2e92c1d
- FULL <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-adversarial-reviewer.md SHA256 29d3fd27ffca50b7842e7a519f56486fadab5cccb57f4bc66a622903b5304114
- FULL <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-api-contract-reviewer.md SHA256 c40e9f473eb1595f028edf0b729146728dc3e86bb05ce8d3ea6f8fd6d9ff30ac
- FULL <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-architecture-critic.md SHA256 258b877f6fc6b36b75d92e182b0093c344381c40982e36e7a90518620ebd2cff
- FULL <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-failure-analyst.md SHA256 0c1e561b4876d805dd170a59de33c9dcbad447d62944791184aa3c39be966a75
- READ-DONE <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-implementer-opus.md L1-54 SHA256 8505299f478e5bfbd6cc93b95dfc60278a3e431f362cc5f883abb807a259eb80
- READ-DONE <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-instruction-reviewer.md L1-28 SHA256 6e7df9190af35a57efda83af8923c065304ce3a1748d33680353f8df6f98aa6e
- READ-DONE <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-migration-guardian.md L1-42 SHA256 77b1abc7047aa3bedc6ff1edc5ef57b2672d66bd714178542f565f96d63b8f7d
- READ-DONE <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-reviewer.md L1-51 SHA256 d020f0cc314573ea104154d2e1cdf9f15e4ffe3621a3db9a8487ceffe1dda2fb
- READ-DONE <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-security-reviewer.md L1-44 SHA256 fff294899b929356b22bd6244f5d6aea21d6ac95a7d4d512702f634d1dd1baf8
- READ-DONE <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-spec-analyst.md L1-31 SHA256 edcd2b3173d2637728275c3772c81d40d5ab0cb3d3971d2412254d2b576339f9
- FULL <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-implementer-opus.md SHA256 8505299f478e5bfbd6cc93b95dfc60278a3e431f362cc5f883abb807a259eb80
- FULL <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-instruction-reviewer.md SHA256 6e7df9190af35a57efda83af8923c065304ce3a1748d33680353f8df6f98aa6e
- FULL <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-migration-guardian.md SHA256 77b1abc7047aa3bedc6ff1edc5ef57b2672d66bd714178542f565f96d63b8f7d
- FULL <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-reviewer.md SHA256 d020f0cc314573ea104154d2e1cdf9f15e4ffe3621a3db9a8487ceffe1dda2fb
- FULL <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-security-reviewer.md SHA256 fff294899b929356b22bd6244f5d6aea21d6ac95a7d4d512702f634d1dd1baf8
- READ-DONE <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-spec-analyst.md L32-41 SHA256 edcd2b3173d2637728275c3772c81d40d5ab0cb3d3971d2412254d2b576339f9
- READ-DONE <repo>/skills/sohrab/alaa-cc-orchestrator/agents/openai.yaml L1-7 SHA256 ef8d309fbd23bf6e793b246856de4ded101992ff5137c904149c1fcc987f5fb1
- READ-DONE skills/sohrab/alaa-cc-orchestrator/CHANGELOG.md L1-91 SHA256 6290c7ae71c364de37aaf93ad46744c277aa62c7702d1b71356b4735897d7e00
- FULL <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-spec-analyst.md SHA256 edcd2b3173d2637728275c3772c81d40d5ab0cb3d3971d2412254d2b576339f9
- FULL <repo>/skills/sohrab/alaa-cc-orchestrator/agents/openai.yaml SHA256 ef8d309fbd23bf6e793b246856de4ded101992ff5137c904149c1fcc987f5fb1
- READ-DONE skills/sohrab/alaa-cc-orchestrator/CHANGELOG.md L92-102 SHA256 6290c7ae71c364de37aaf93ad46744c277aa62c7702d1b71356b4735897d7e00
- READ-DONE <repo>/skills/sohrab/alaa-cc-orchestrator/references/agent-catalog.md L1-131 SHA256 ea38f60077deae833116c6df397a5aaacbce4039a06bda88dc3c00ee37dc90d5
- READ-DONE <repo>/skills/sohrab/alaa-cc-orchestrator/references/delegation-prompts.md L1-116 SHA256 5ad35a2da5c57207e4d267d7b9046e6b3f003b90dca2f9ca3faf3d93ef1543cc
- FULL skills/sohrab/alaa-cc-orchestrator/CHANGELOG.md SHA256 6290c7ae71c364de37aaf93ad46744c277aa62c7702d1b71356b4735897d7e00
- FULL <repo>/skills/sohrab/alaa-cc-orchestrator/references/agent-catalog.md SHA256 ea38f60077deae833116c6df397a5aaacbce4039a06bda88dc3c00ee37dc90d5
- READ-DONE <repo>/skills/sohrab/alaa-cc-orchestrator/references/delegation-prompts.md L117-300 SHA256 5ad35a2da5c57207e4d267d7b9046e6b3f003b90dca2f9ca3faf3d93ef1543cc
- READ-DONE <repo>/skills/sohrab/alaa-cc-orchestrator/references/failure-taxonomy.md L1-62 SHA256 d95a44f4749468ef67d1a4dddf9b1ec1029d6279493788850757ca37a8456ba4
- READ-DONE <repo>/skills/sohrab/alaa-cc-orchestrator/references/resource-policy.md L1-80 SHA256 18787192c9691b3956b4e6772590091f407afcef4dcaf445d73656b1fca0bd21
- FULL <repo>/skills/sohrab/alaa-cc-orchestrator/references/delegation-prompts.md SHA256 5ad35a2da5c57207e4d267d7b9046e6b3f003b90dca2f9ca3faf3d93ef1543cc
- FULL <repo>/skills/sohrab/alaa-cc-orchestrator/references/failure-taxonomy.md SHA256 d95a44f4749468ef67d1a4dddf9b1ec1029d6279493788850757ca37a8456ba4
- FULL <repo>/skills/sohrab/alaa-cc-orchestrator/references/resource-policy.md SHA256 18787192c9691b3956b4e6772590091f407afcef4dcaf445d73656b1fca0bd21
- READ-DONE <repo>/skills/sohrab/alaa-cc-orchestrator/references/routing-matrix.md L1-151 SHA256 60953cf93990aeebb48b6bdacbaff60b37e434119ecfac2b5249653fcab2a8c5
- READ-DONE <repo>/skills/sohrab/alaa-cc-orchestrator/references/verification-and-gates.md L1-64 SHA256 205243e89f219355f0daa03b995f62c3cf39d12640fd00bad33d44a4383aa9ad
- FULL <repo>/skills/sohrab/alaa-cc-orchestrator/references/routing-matrix.md SHA256 60953cf93990aeebb48b6bdacbaff60b37e434119ecfac2b5249653fcab2a8c5
- READ-DONE <repo>/skills/sohrab/alaa-cc-orchestrator/references/verification-and-gates.md L65-155 SHA256 205243e89f219355f0daa03b995f62c3cf39d12640fd00bad33d44a4383aa9ad
- READ-DONE <repo>/skills/sohrab/alaa-cc-orchestrator/scripts/check_agent_grants.py L1-161 SHA256 cd16f05822b9251d474e48cdd545c1f604a8a85fd79f599693878c85d8cebb09
- FULL <repo>/skills/sohrab/alaa-cc-orchestrator/references/verification-and-gates.md SHA256 205243e89f219355f0daa03b995f62c3cf39d12640fd00bad33d44a4383aa9ad
- READ-DONE <repo>/skills/sohrab/alaa-cc-orchestrator/scripts/check_agent_grants.py L162-412 SHA256 cd16f05822b9251d474e48cdd545c1f604a8a85fd79f599693878c85d8cebb09
- READ-DONE <repo>/skills/sohrab/alaa-cc-orchestrator/scripts/Invoke-AlaaLowPriority.ps1 L1-116 SHA256 bf2667dbcb23b4d33fa5015e5d29d8cd2024a4057fb85ab23d7d6f8865c9f714
- READ-DONE <repo>/skills/sohrab/alaa-cc-orchestrator/scripts/run-low-priority.sh L1-33 SHA256 a629cd29554ba67cdd5b37759a058bc787f21582129f48c7ad55fb484d73bc5d
- READ-DONE skills/sohrab/alaa-cc-orchestrator/SKILL.md L1-29 SHA256 62a60722d2afffa2cbaca48ac2bd642148a0072f4ab157f3204d9211fe459a38
- FULL <repo>/skills/sohrab/alaa-cc-orchestrator/scripts/check_agent_grants.py SHA256 cd16f05822b9251d474e48cdd545c1f604a8a85fd79f599693878c85d8cebb09
- FULL <repo>/skills/sohrab/alaa-cc-orchestrator/scripts/Invoke-AlaaLowPriority.ps1 SHA256 bf2667dbcb23b4d33fa5015e5d29d8cd2024a4057fb85ab23d7d6f8865c9f714
- FULL <repo>/skills/sohrab/alaa-cc-orchestrator/scripts/run-low-priority.sh SHA256 a629cd29554ba67cdd5b37759a058bc787f21582129f48c7ad55fb484d73bc5d
- READ-DONE skills/sohrab/alaa-cc-orchestrator/SKILL.md L30-172 SHA256 62a60722d2afffa2cbaca48ac2bd642148a0072f4ab157f3204d9211fe459a38
- READ-DONE skills/sohrab/alaa-cc-orchestrator/SKILL.md L173-174 SHA256 62a60722d2afffa2cbaca48ac2bd642148a0072f4ab157f3204d9211fe459a38
- READ-DONE skills/sohrab/alaa-cc-orchestrator/VERSION L1-1 SHA256 3b10b6ad566eadbcacadb33c591f1ec629593d6adf47442e56e0f61996829ef7
- READ-DONE <repo>/skills/sohrab/alaa-codex-orchestrator/agents/alaa-accessibility-reviewer.toml L1-46 SHA256 7a1aae67562990c0bac34b7bf6174d16e0a8716e6e3ede260db5c6119be17088
- READ-DONE <repo>/skills/sohrab/alaa-codex-orchestrator/agents/alaa-adversarial-reviewer.toml L1-36 SHA256 867210ded42bc548f5f7e2e02bb102baf71dbc038f4cb9f5e9643258f5eb3888
- READ-DONE <repo>/skills/sohrab/alaa-codex-orchestrator/agents/alaa-api-contract-reviewer.toml L1-43 SHA256 519d7832d4df6934959a10f81465f2de4dd6d1a564dd9daf66f8c1e865886dc0
- READ-DONE <repo>/skills/sohrab/alaa-codex-orchestrator/agents/alaa-architecture-critic.toml L1-43 SHA256 5ced3f10047cc7cb086247a1d846f01cb292e70e5c4b5ead7a868a6726121777
- READ-DONE <repo>/skills/sohrab/alaa-codex-orchestrator/agents/alaa-browser-qa.toml L1-35 SHA256 0eb195f26485ba079fcf192e807b9a772d7d57d2a68f0be6f1cff256bd27b2ca
- READ-DONE <repo>/skills/sohrab/alaa-codex-orchestrator/agents/alaa-dependency-auditor.toml L1-30 SHA256 c449bbb19ad9c83946253346a85b68bb0fd6e77bff21f7e36a458a8865363f52
- FULL skills/sohrab/alaa-cc-orchestrator/SKILL.md SHA256 62a60722d2afffa2cbaca48ac2bd642148a0072f4ab157f3204d9211fe459a38
- FULL skills/sohrab/alaa-cc-orchestrator/VERSION SHA256 3b10b6ad566eadbcacadb33c591f1ec629593d6adf47442e56e0f61996829ef7
- FULL <repo>/skills/sohrab/alaa-codex-orchestrator/agents/alaa-accessibility-reviewer.toml SHA256 7a1aae67562990c0bac34b7bf6174d16e0a8716e6e3ede260db5c6119be17088
- FULL <repo>/skills/sohrab/alaa-codex-orchestrator/agents/alaa-adversarial-reviewer.toml SHA256 867210ded42bc548f5f7e2e02bb102baf71dbc038f4cb9f5e9643258f5eb3888
- FULL <repo>/skills/sohrab/alaa-codex-orchestrator/agents/alaa-api-contract-reviewer.toml SHA256 519d7832d4df6934959a10f81465f2de4dd6d1a564dd9daf66f8c1e865886dc0
- FULL <repo>/skills/sohrab/alaa-codex-orchestrator/agents/alaa-architecture-critic.toml SHA256 5ced3f10047cc7cb086247a1d846f01cb292e70e5c4b5ead7a868a6726121777
- FULL <repo>/skills/sohrab/alaa-codex-orchestrator/agents/alaa-browser-qa.toml SHA256 0eb195f26485ba079fcf192e807b9a772d7d57d2a68f0be6f1cff256bd27b2ca
- READ-DONE <repo>/skills/sohrab/alaa-codex-orchestrator/agents/alaa-dependency-auditor.toml L31-40 SHA256 c449bbb19ad9c83946253346a85b68bb0fd6e77bff21f7e36a458a8865363f52
- READ-DONE <repo>/skills/sohrab/alaa-codex-orchestrator/agents/alaa-documenter.toml L1-35 SHA256 422f4e7561fabbf183e69ad60c40b05973c8df518761c64f08fde71653a3dcd8
- READ-DONE <repo>/skills/sohrab/alaa-codex-orchestrator/agents/alaa-explorer.toml L1-35 SHA256 bd47e2a06417660b55b8849099dcadbd60f63e9dfcc5bf777e4d863bd1832d3e
- READ-DONE <repo>/skills/sohrab/alaa-codex-orchestrator/agents/alaa-failure-analyst.toml L1-36 SHA256 0ad5d22bb055736f8c116f21b36e7cdd0c5c933501c87e8700ebdc335df4e61b
- READ-DONE <repo>/skills/sohrab/alaa-codex-orchestrator/agents/alaa-implementer-sol.toml L1-39 SHA256 8381dee3d127a8ef29856e8559ca03797c8b2a46c0a9d6c0a57a11fefc39c5a4
- READ-DONE <repo>/skills/sohrab/alaa-codex-orchestrator/agents/alaa-implementer.toml L1-48 SHA256 c85e785b6f5555bc4d92880e1d626120279df2d0ff6ca594839b9df31b8d3217
- READ-DONE <repo>/skills/sohrab/alaa-codex-orchestrator/agents/alaa-instruction-reviewer.toml L1-26 SHA256 2067c85864531b1a768802cd97ad3d3e89154b726020adde93c4baccd0710549
- FULL <repo>/skills/sohrab/alaa-codex-orchestrator/agents/alaa-dependency-auditor.toml SHA256 c449bbb19ad9c83946253346a85b68bb0fd6e77bff21f7e36a458a8865363f52
- FULL <repo>/skills/sohrab/alaa-codex-orchestrator/agents/alaa-documenter.toml SHA256 422f4e7561fabbf183e69ad60c40b05973c8df518761c64f08fde71653a3dcd8
- FULL <repo>/skills/sohrab/alaa-codex-orchestrator/agents/alaa-explorer.toml SHA256 bd47e2a06417660b55b8849099dcadbd60f63e9dfcc5bf777e4d863bd1832d3e
- FULL <repo>/skills/sohrab/alaa-codex-orchestrator/agents/alaa-failure-analyst.toml SHA256 0ad5d22bb055736f8c116f21b36e7cdd0c5c933501c87e8700ebdc335df4e61b
- FULL <repo>/skills/sohrab/alaa-codex-orchestrator/agents/alaa-implementer-sol.toml SHA256 8381dee3d127a8ef29856e8559ca03797c8b2a46c0a9d6c0a57a11fefc39c5a4
- FULL <repo>/skills/sohrab/alaa-codex-orchestrator/agents/alaa-implementer.toml SHA256 c85e785b6f5555bc4d92880e1d626120279df2d0ff6ca594839b9df31b8d3217
- FULL <repo>/skills/sohrab/alaa-codex-orchestrator/agents/alaa-instruction-reviewer.toml SHA256 2067c85864531b1a768802cd97ad3d3e89154b726020adde93c4baccd0710549
- READ-DONE <repo>/skills/sohrab/alaa-codex-orchestrator/agents/alaa-migration-guardian.toml L1-38 SHA256 b22e63ce9e1951423589fe70a88857abf525fa3ff4ca5835fe01632041cb9ded
- READ-DONE <repo>/skills/sohrab/alaa-codex-orchestrator/agents/alaa-observability-reviewer.toml L1-37 SHA256 c8324f5843aa14799ca60bd9eac81a5158c55dc1b6230c351a8188c6e6ff7930
- READ-DONE <repo>/skills/sohrab/alaa-codex-orchestrator/agents/alaa-performance-profiler.toml L1-41 SHA256 5f0ad5ad773c2762c91119fb17821ec2cf18b44ae7d5b205fe5e2b1d3354be27
- READ-DONE <repo>/skills/sohrab/alaa-codex-orchestrator/agents/alaa-release-guardian.toml L1-39 SHA256 d14eab90602509e662ec72e30a5b796aa08476188b9aff2dc089702764122028
- READ-DONE <repo>/skills/sohrab/alaa-codex-orchestrator/agents/alaa-researcher.toml L1-39 SHA256 b8270e705a402a4575dc7d73c139ea38d37b9a27b62dae10406c667fa0cd62ee
- READ-DONE <repo>/skills/sohrab/alaa-codex-orchestrator/agents/alaa-reviewer-deep.toml L1-9 SHA256 7e6293421171420e61a1a0a60978c83cbd25e88e3de0f7238ccada64255521b4
- READ-DONE <repo>/skills/sohrab/alaa-codex-orchestrator/agents/alaa-reviewer.toml L1-8 SHA256 8bf61f9d3342c938e8676455dcc0711ef927dac94de898d25956cb7186b8c47b
- READ-DONE <repo>/skills/sohrab/alaa-codex-orchestrator/agents/alaa-security-reviewer.toml L1-30 SHA256 76200c7040030d2dc147241dd9183e4eacaaa8274431d00f22146a348dfbe4f2
- FULL <repo>/skills/sohrab/alaa-codex-orchestrator/agents/alaa-migration-guardian.toml SHA256 b22e63ce9e1951423589fe70a88857abf525fa3ff4ca5835fe01632041cb9ded
- FULL <repo>/skills/sohrab/alaa-codex-orchestrator/agents/alaa-observability-reviewer.toml SHA256 c8324f5843aa14799ca60bd9eac81a5158c55dc1b6230c351a8188c6e6ff7930
- FULL <repo>/skills/sohrab/alaa-codex-orchestrator/agents/alaa-performance-profiler.toml SHA256 5f0ad5ad773c2762c91119fb17821ec2cf18b44ae7d5b205fe5e2b1d3354be27
- FULL <repo>/skills/sohrab/alaa-codex-orchestrator/agents/alaa-release-guardian.toml SHA256 d14eab90602509e662ec72e30a5b796aa08476188b9aff2dc089702764122028
- FULL <repo>/skills/sohrab/alaa-codex-orchestrator/agents/alaa-researcher.toml SHA256 b8270e705a402a4575dc7d73c139ea38d37b9a27b62dae10406c667fa0cd62ee
- FULL <repo>/skills/sohrab/alaa-codex-orchestrator/agents/alaa-reviewer-deep.toml SHA256 7e6293421171420e61a1a0a60978c83cbd25e88e3de0f7238ccada64255521b4
- READ-DONE <repo>/skills/sohrab/alaa-codex-orchestrator/agents/alaa-reviewer.toml L9-9 SHA256 8bf61f9d3342c938e8676455dcc0711ef927dac94de898d25956cb7186b8c47b
- READ-DONE <repo>/skills/sohrab/alaa-codex-orchestrator/agents/alaa-security-reviewer.toml L31-39 SHA256 76200c7040030d2dc147241dd9183e4eacaaa8274431d00f22146a348dfbe4f2
- READ-DONE <repo>/skills/sohrab/alaa-codex-orchestrator/agents/alaa-spec-analyst.toml L1-41 SHA256 06899448aad7667243699289baf965892fec8d5b8836919d5fa51324a387cf35
- READ-DONE <repo>/skills/sohrab/alaa-codex-orchestrator/agents/alaa-test-strategist.toml L1-40 SHA256 feb00b29dca1a8a27d88d8c7651a8d9df763e4ea4bab8ea2ad2be5a0d6945a84
- READ-DONE <repo>/skills/sohrab/alaa-codex-orchestrator/agents/alaa-verifier.toml L1-42 SHA256 5d3ad349a82df8ae33b420a804fc2d0e28c5674d872278ba460e7f8ef9d80867
- READ-DONE <repo>/skills/sohrab/alaa-codex-orchestrator/agents/openai.yaml L1-7 SHA256 e78f7a6b290a19ee7055b649aaa1cf58def2b573fe7fe8d809c524810fd38651
- READ-DONE <repo>/skills/sohrab/alaa-codex-orchestrator/assets/manifest.json L1-121 SHA256 6b43131dff91d85e7b8d198c348f1ac5736a56c0ceebd9edf9506373662bc37a
- FULL <repo>/skills/sohrab/alaa-codex-orchestrator/agents/alaa-reviewer.toml SHA256 8bf61f9d3342c938e8676455dcc0711ef927dac94de898d25956cb7186b8c47b
- FULL <repo>/skills/sohrab/alaa-codex-orchestrator/agents/alaa-security-reviewer.toml SHA256 76200c7040030d2dc147241dd9183e4eacaaa8274431d00f22146a348dfbe4f2
- FULL <repo>/skills/sohrab/alaa-codex-orchestrator/agents/alaa-spec-analyst.toml SHA256 06899448aad7667243699289baf965892fec8d5b8836919d5fa51324a387cf35
- FULL <repo>/skills/sohrab/alaa-codex-orchestrator/agents/alaa-test-strategist.toml SHA256 feb00b29dca1a8a27d88d8c7651a8d9df763e4ea4bab8ea2ad2be5a0d6945a84
- FULL <repo>/skills/sohrab/alaa-codex-orchestrator/agents/alaa-verifier.toml SHA256 5d3ad349a82df8ae33b420a804fc2d0e28c5674d872278ba460e7f8ef9d80867
- FULL <repo>/skills/sohrab/alaa-codex-orchestrator/agents/openai.yaml SHA256 e78f7a6b290a19ee7055b649aaa1cf58def2b573fe7fe8d809c524810fd38651
- FULL <repo>/skills/sohrab/alaa-codex-orchestrator/assets/manifest.json SHA256 6b43131dff91d85e7b8d198c348f1ac5736a56c0ceebd9edf9506373662bc37a
- READ-DONE <repo>/skills/sohrab/alaa-codex-orchestrator/assets/reviewer-contract.md L1-31 SHA256 dfc528a4efad37083a6bbbcfbef32e02ad9fc498fec1c0d013caac4951542a05
- READ-DONE skills/sohrab/alaa-codex-orchestrator/CHANGELOG.md L1-77 SHA256 f1951f1d92cbab80611bcae9c542007e9225c6b4d13181f831944bf9cecf9837
- FULL <repo>/skills/sohrab/alaa-codex-orchestrator/assets/reviewer-contract.md SHA256 dfc528a4efad37083a6bbbcfbef32e02ad9fc498fec1c0d013caac4951542a05
- READ-DONE skills/sohrab/alaa-codex-orchestrator/CHANGELOG.md L78-137 SHA256 f1951f1d92cbab80611bcae9c542007e9225c6b4d13181f831944bf9cecf9837
- READ-DONE skills/sohrab/alaa-codex-orchestrator/README-fa.md L1-102 SHA256 ae07a9dca5cb3eb8bacfa3e6388acb7a6c74f7de97b76778e21499ee04cf95fb
- READ-DONE <repo>/skills/sohrab/alaa-codex-orchestrator/references/agent-catalog.md L1-101 SHA256 c88313fbe4e1c0ab1bc02af308c944ff415faead10f518e7fa80aa32879c3833
- READ-DONE <repo>/skills/sohrab/alaa-codex-orchestrator/references/delegation-prompts.md L1-37 SHA256 b4afcdcb8fb93148463370757d22cee651afa72c2248797dba6abe8378247d78
- FULL skills/sohrab/alaa-codex-orchestrator/CHANGELOG.md SHA256 f1951f1d92cbab80611bcae9c542007e9225c6b4d13181f831944bf9cecf9837
- FULL skills/sohrab/alaa-codex-orchestrator/README-fa.md SHA256 ae07a9dca5cb3eb8bacfa3e6388acb7a6c74f7de97b76778e21499ee04cf95fb
- FULL <repo>/skills/sohrab/alaa-codex-orchestrator/references/agent-catalog.md SHA256 c88313fbe4e1c0ab1bc02af308c944ff415faead10f518e7fa80aa32879c3833
- READ-DONE <repo>/skills/sohrab/alaa-codex-orchestrator/references/delegation-prompts.md L38-280 SHA256 b4afcdcb8fb93148463370757d22cee651afa72c2248797dba6abe8378247d78
- READ-DONE <repo>/skills/sohrab/alaa-codex-orchestrator/references/failure-taxonomy.md L1-62 SHA256 d95a44f4749468ef67d1a4dddf9b1ec1029d6279493788850757ca37a8456ba4
- FULL <repo>/skills/sohrab/alaa-codex-orchestrator/references/delegation-prompts.md SHA256 b4afcdcb8fb93148463370757d22cee651afa72c2248797dba6abe8378247d78
- FULL <repo>/skills/sohrab/alaa-codex-orchestrator/references/failure-taxonomy.md SHA256 d95a44f4749468ef67d1a4dddf9b1ec1029d6279493788850757ca37a8456ba4
- READ-DONE <repo>/skills/sohrab/alaa-codex-orchestrator/references/installation.md L1-57 SHA256 fee26330cdbf546137957c022003903626254422af0e06b41ad510b575312ce3
- READ-DONE <repo>/skills/sohrab/alaa-codex-orchestrator/references/resource-policy.md L1-80 SHA256 18787192c9691b3956b4e6772590091f407afcef4dcaf445d73656b1fca0bd21
- READ-DONE <repo>/skills/sohrab/alaa-codex-orchestrator/references/routing-matrix.md L1-137 SHA256 49e1688b40d8f607838c1c3f054e79debb5b4aa7b63b8aaf990df7edf8e2b4bd
- FULL <repo>/skills/sohrab/alaa-codex-orchestrator/references/installation.md SHA256 fee26330cdbf546137957c022003903626254422af0e06b41ad510b575312ce3
- FULL <repo>/skills/sohrab/alaa-codex-orchestrator/references/resource-policy.md SHA256 18787192c9691b3956b4e6772590091f407afcef4dcaf445d73656b1fca0bd21
- READ-DONE <repo>/skills/sohrab/alaa-codex-orchestrator/references/routing-matrix.md L138-147 SHA256 49e1688b40d8f607838c1c3f054e79debb5b4aa7b63b8aaf990df7edf8e2b4bd
- READ-DONE <repo>/skills/sohrab/alaa-codex-orchestrator/references/verification-and-gates.md L1-143 SHA256 c230574d049f60145ff92b26579b9d71f8bcb58aa0ed620823edcb31c183b639
- FULL <repo>/skills/sohrab/alaa-codex-orchestrator/references/routing-matrix.md SHA256 49e1688b40d8f607838c1c3f054e79debb5b4aa7b63b8aaf990df7edf8e2b4bd
- READ-DONE <repo>/skills/sohrab/alaa-codex-orchestrator/references/verification-and-gates.md L144-155 SHA256 c230574d049f60145ff92b26579b9d71f8bcb58aa0ed620823edcb31c183b639
- READ-DONE <repo>/skills/sohrab/alaa-codex-orchestrator/scripts/check_agent_grants.py L1-445 SHA256 a0379947e7fb84be6215806827eb3e81ec9b970ea9c195ca19e52e47bbcf1169
- FULL <repo>/skills/sohrab/alaa-codex-orchestrator/references/verification-and-gates.md SHA256 c230574d049f60145ff92b26579b9d71f8bcb58aa0ed620823edcb31c183b639
- READ-DONE <repo>/skills/sohrab/alaa-codex-orchestrator/scripts/check_agent_grants.py L446-481 SHA256 a0379947e7fb84be6215806827eb3e81ec9b970ea9c195ca19e52e47bbcf1169
- READ-DONE <repo>/skills/sohrab/alaa-codex-orchestrator/scripts/Get-AlaaCodexAgentStatus.ps1 L1-51 SHA256 df1de5d19ec280b3a7396e1661c14b6e928560db34e3af618715401f9f794a7c
- READ-DONE <repo>/skills/sohrab/alaa-codex-orchestrator/scripts/install-agents.sh L1-82 SHA256 b13cd13fd223c7f71024d8c57c95ba4f6b3e03dbef5fd098e98c381d98f0e6f8
- READ-DONE <repo>/skills/sohrab/alaa-codex-orchestrator/scripts/Install-AlaaCodexAgents.ps1 L1-140 SHA256 1bc62f02fb62e1a4a0f4bd034595f528dfaac85ec89f4ec883d58c67bcbd12c6
- READ-DONE <repo>/skills/sohrab/alaa-codex-orchestrator/scripts/Install-AlaaCodexOrchestrator.ps1 L1-95 SHA256 856f94b6f2633fbd93e1c731640d5f6abc517a27f400a25864bf18cc59eaf7b7
- READ-DONE <repo>/skills/sohrab/alaa-codex-orchestrator/scripts/install-skill.sh L1-36 SHA256 288a84b21ebecd7974b9ac1d701f18f584f9bd355361234b5f742c73902e9e1a
- READ-DONE <repo>/skills/sohrab/alaa-codex-orchestrator/scripts/Invoke-AlaaLowPriority.ps1 L1-58 SHA256 bf2667dbcb23b4d33fa5015e5d29d8cd2024a4057fb85ab23d7d6f8865c9f714
- FULL <repo>/skills/sohrab/alaa-codex-orchestrator/scripts/check_agent_grants.py SHA256 a0379947e7fb84be6215806827eb3e81ec9b970ea9c195ca19e52e47bbcf1169
- FULL <repo>/skills/sohrab/alaa-codex-orchestrator/scripts/Get-AlaaCodexAgentStatus.ps1 SHA256 df1de5d19ec280b3a7396e1661c14b6e928560db34e3af618715401f9f794a7c
- FULL <repo>/skills/sohrab/alaa-codex-orchestrator/scripts/install-agents.sh SHA256 b13cd13fd223c7f71024d8c57c95ba4f6b3e03dbef5fd098e98c381d98f0e6f8
- FULL <repo>/skills/sohrab/alaa-codex-orchestrator/scripts/Install-AlaaCodexAgents.ps1 SHA256 1bc62f02fb62e1a4a0f4bd034595f528dfaac85ec89f4ec883d58c67bcbd12c6
- FULL <repo>/skills/sohrab/alaa-codex-orchestrator/scripts/Install-AlaaCodexOrchestrator.ps1 SHA256 856f94b6f2633fbd93e1c731640d5f6abc517a27f400a25864bf18cc59eaf7b7
- FULL <repo>/skills/sohrab/alaa-codex-orchestrator/scripts/install-skill.sh SHA256 288a84b21ebecd7974b9ac1d701f18f584f9bd355361234b5f742c73902e9e1a
- READ-DONE <repo>/skills/sohrab/alaa-codex-orchestrator/scripts/Invoke-AlaaLowPriority.ps1 L59-116 SHA256 bf2667dbcb23b4d33fa5015e5d29d8cd2024a4057fb85ab23d7d6f8865c9f714
- READ-DONE <repo>/skills/sohrab/alaa-codex-orchestrator/scripts/render_agents.py L1-150 SHA256 e397b48954194ec6448e698ad4836862ba2360cf4caceb8ecb8d957f737add34
- READ-DONE <repo>/skills/sohrab/alaa-codex-orchestrator/scripts/run-low-priority.sh L1-33 SHA256 a629cd29554ba67cdd5b37759a058bc787f21582129f48c7ad55fb484d73bc5d
- READ-DONE <repo>/skills/sohrab/alaa-codex-orchestrator/scripts/test_install_preflight.py L1-113 SHA256 37dc555af44bfceb43c6437e33d01413acd55645b408a7d1256b1ea55225a782
- READ-DONE <repo>/skills/sohrab/alaa-codex-orchestrator/scripts/validate_pack.py L1-108 SHA256 9a54d311c319e1fcaedc23d0a407cd87723e35b2c42d546b2cae62d89e99f2df
- FULL <repo>/skills/sohrab/alaa-codex-orchestrator/scripts/Invoke-AlaaLowPriority.ps1 SHA256 bf2667dbcb23b4d33fa5015e5d29d8cd2024a4057fb85ab23d7d6f8865c9f714
- FULL <repo>/skills/sohrab/alaa-codex-orchestrator/scripts/render_agents.py SHA256 e397b48954194ec6448e698ad4836862ba2360cf4caceb8ecb8d957f737add34
- FULL <repo>/skills/sohrab/alaa-codex-orchestrator/scripts/run-low-priority.sh SHA256 a629cd29554ba67cdd5b37759a058bc787f21582129f48c7ad55fb484d73bc5d
- FULL <repo>/skills/sohrab/alaa-codex-orchestrator/scripts/test_install_preflight.py SHA256 37dc555af44bfceb43c6437e33d01413acd55645b408a7d1256b1ea55225a782
- READ-DONE <repo>/skills/sohrab/alaa-codex-orchestrator/scripts/validate_pack.py L109-211 SHA256 9a54d311c319e1fcaedc23d0a407cd87723e35b2c42d546b2cae62d89e99f2df
- READ-DONE skills/sohrab/alaa-codex-orchestrator/VERSION L1-1 SHA256 e1d49c569ae09b2ede16e2d83820a3809b35eb6c44c13ba9b5330598d6b8f43c
- READ-DONE <repo>/skills/sohrab/alaa-low-noise/agents/openai.yaml L1-4 SHA256 afe5575804b65f60ab0f1019b19c275ce71ee589f7d79f7389c62f15302db0f8
- FULL <repo>/skills/sohrab/alaa-codex-orchestrator/scripts/validate_pack.py SHA256 9a54d311c319e1fcaedc23d0a407cd87723e35b2c42d546b2cae62d89e99f2df
- FULL skills/sohrab/alaa-codex-orchestrator/VERSION SHA256 e1d49c569ae09b2ede16e2d83820a3809b35eb6c44c13ba9b5330598d6b8f43c
- FULL <repo>/skills/sohrab/alaa-low-noise/agents/openai.yaml SHA256 afe5575804b65f60ab0f1019b19c275ce71ee589f7d79f7389c62f15302db0f8
- FULL <repo>/skills/sohrab/alaa-cc-orchestrator/references/delegation-prompts.md SHA256 b64af563443f9f564171ab68357f9689bd65e3810693b9692817cfd12ed8c60d
- FULL <repo>/skills/sohrab/alaa-cc-orchestrator/scripts/check_agent_contracts.py SHA256 a154afab91672912ca85ae22c64ef2fd4ba04c2a99a16f7b94e45e5ef67ee47c
- FULL <repo>/skills/sohrab/alaa-cc-orchestrator/scripts/validate_pack.py SHA256 be9267f5523715fd26f0f6c5c71dac3f99827da7ce22a645c17a17c53f88928b
- FULL <repo>/skills/sohrab/alaa-codex-orchestrator/references/delegation-prompts.md SHA256 6759401a2e0f5690c57700dd0d3013fa81059e725ebc58ecfba0f43ca1db0911
- FULL <repo>/skills/sohrab/alaa-codex-orchestrator/scripts/check_agent_contracts.py SHA256 a154afab91672912ca85ae22c64ef2fd4ba04c2a99a16f7b94e45e5ef67ee47c
- FULL <repo>/skills/sohrab/alaa-codex-orchestrator/scripts/validate_pack.py SHA256 22413a2dbfc35497b09f4087b5d82df407f640747fb539762e9b8abaa8cabb04

## Full-read reconciliation and follow-up verification

All 190 owned files are fully read and reconciled (96/38/50/6 by scope order above),
including unchanged files. Zero inaccessible files, omissions or hash mismatches remain.
The six follow-up files were reread through their complete earlier contents and inspected
patches; their updated FULL records supersede old hashes. The two dispatch templates now
match their skill bodies; both checkers and pack entrypoints enforce that contract.
Compression preserves meaningful host-required progress, bounded commands, independent
checks, return limits and interrupted-work recovery. No additional model, grant, installation,
historical or low-noise behavior changes were warranted by the full inventory.

Additional focused checks observed on 2026-09-29, repository-root cwd, Python 3.13 -B,
non-heavy; each completed below one second, each exit 0:

| Command | Observed result |
|---|---|
| python -B <repo>/skills/sohrab/alaa-cc-orchestrator/scripts/check_agent_contracts.py --self-test | 18 positive/negative structural fixtures |
| python -B <repo>/skills/sohrab/alaa-codex-orchestrator/scripts/check_agent_contracts.py --self-test | 18 positive/negative structural fixtures |
| python -B <repo>/skills/sohrab/alaa-cc-orchestrator/scripts/check_agent_contracts.py | Metadata, authority and dispatch source requirements |
| python -B <repo>/skills/sohrab/alaa-codex-orchestrator/scripts/check_agent_contracts.py | Metadata, authority and dispatch source requirements |
| python -B <repo>/skills/sohrab/alaa-cc-orchestrator/scripts/validate_pack.py | 22 agents, version 4.1.0 |
| python -B <repo>/skills/sohrab/alaa-codex-orchestrator/scripts/validate_pack.py | 23 agents, version 4.0.0 |
| git diff --check -- skills/sohrab/alaa-prompting-guide skills/sohrab/alaa-cc-orchestrator skills/sohrab/alaa-codex-orchestrator skills/sohrab/alaa-low-noise | Clean whitespace |

These seven executions are justified by changed dispatch/checker/pack inputs. Earlier
model-policy, corpus, grant and renderer results retain unchanged inputs and were cited.
Total lane validation: 23 executions, 13 distinct commands; no failed gate. The previous
snapshot remains historical evidence; the following current snapshot includes 31 changed
source files and excludes this evidence log. Independent review and live calibration remain
outside this lane and unrun; full-read completion is not a substitute for those gates.

## Current changed source snapshot

Aggregate SHA-256 (sorted hash/path lines): `6c26c1b53dc86ea7f0ad9c971f3090650e6c5f560b124acac80c2d8612d6c461`.

```text
62a60722d2afffa2cbaca48ac2bd642148a0072f4ab157f3204d9211fe459a38  skills/sohrab/alaa-cc-orchestrator/SKILL.md
bcee62b91e66865d130cb62a0b4f6e37b5c2634ac584e3d34d90c2939842c1fa  <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-accessibility-reviewer.md
20d97fd040660cfb4934ad4828a68110c1904feeae7c53a10b5d4c532638301e  <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-browser-qa.md
adc72ed146d384ee2c8e7de903f00e181623e3908e5962f48ff6fec5e44710ba  <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-dependency-auditor.md
d78bc2e27dcd8c8cb3e80ca8811f224733082c247cb67478498ea0788e6a836f  <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-documenter.md
b9da8c3b163140c5fa1be45b3ea732042cd9fe4eaa377592a9baef1a714199c7  <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-explorer.md
3043a4578cef46687d0288cb4c1db7cd9ee88d9aab0eb2524a4ed407fd94c3c0  <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-implementer.md
dd2d10b9603d3ef03966eaaf9b345d97002afa101aac04f4abe635db8fb791cb  <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-observability-reviewer.md
e4a79dc03885c0ceeb5606d9b8929778d3f06d62a0173ae414dff21ba9053143  <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-performance-profiler.md
9527a637df24a161372552457c726def1f9b132af0365b820b07dbb48895f76d  <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-release-guardian.md
4721c57074ee904452f59439b010ca0e41d3d8dff5c9b65e8b87555fca6018c7  <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-researcher.md
bea3193c57930ac5a3ee2bf9b7ccc39d9e4900d20f8bed7dec1c1f218a7b52a3  <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-test-strategist.md
82d5319f231eba78a3af3531b49524f781095ae54170b8b517b0362474113612  <repo>/skills/sohrab/alaa-cc-orchestrator/agents/alaa-verifier.md
b64af563443f9f564171ab68357f9689bd65e3810693b9692817cfd12ed8c60d  <repo>/skills/sohrab/alaa-cc-orchestrator/references/delegation-prompts.md
a154afab91672912ca85ae22c64ef2fd4ba04c2a99a16f7b94e45e5ef67ee47c  <repo>/skills/sohrab/alaa-cc-orchestrator/scripts/check_agent_contracts.py
be9267f5523715fd26f0f6c5c71dac3f99827da7ce22a645c17a17c53f88928b  <repo>/skills/sohrab/alaa-cc-orchestrator/scripts/validate_pack.py
d523982c3eeeac5c6a4da3fbfc6cd9103e198060f835876983f1a53f3c967e76  skills/sohrab/alaa-codex-orchestrator/SKILL.md
6759401a2e0f5690c57700dd0d3013fa81059e725ebc58ecfba0f43ca1db0911  <repo>/skills/sohrab/alaa-codex-orchestrator/references/delegation-prompts.md
a154afab91672912ca85ae22c64ef2fd4ba04c2a99a16f7b94e45e5ef67ee47c  <repo>/skills/sohrab/alaa-codex-orchestrator/scripts/check_agent_contracts.py
22413a2dbfc35497b09f4087b5d82df407f640747fb539762e9b8abaa8cabb04  <repo>/skills/sohrab/alaa-codex-orchestrator/scripts/validate_pack.py
203c85bc80958d3400a2ad4760ea1add9891c32dfa90082a9a3726d17a46afed  skills/sohrab/alaa-prompting-guide/SKILL.md
2c592b27a32b857747fc24aff2218a1b851c5e4928fc069b7a275bd7690881fb  <repo>/skills/sohrab/alaa-prompting-guide/agents/openai.yaml
4d3ebdd310df52afcfbb6a6b23b6f3e53b1e0218e77ce00b93cbbd57c8e67064  <repo>/skills/sohrab/alaa-prompting-guide/assets/claude-model-policy.json
8b8854a3f7e5e8a432492b265ab053ff6675c4e32e2be3c18fff173f8b4c6ece  <repo>/skills/sohrab/alaa-prompting-guide/assets/evals/claude-agent-comparisons.json
60f53ced08910f649c566af256358e2bb46254ed867052eabc2fdb90639d5074  <repo>/skills/sohrab/alaa-prompting-guide/references/00-source-map.md
e2174298f143299553c3803f9f7c965640860659286ee919076cae96b3933b18  <repo>/skills/sohrab/alaa-prompting-guide/references/00-topic-map.md
a4f813b15caceece150383bc31982ed3fb04a95af56d495508251ffe1d4f1859  <repo>/skills/sohrab/alaa-prompting-guide/references/06-invocation-and-composition.md
23a59c554f64345eb98ca2e860dbf7c68b97239b992e90e6b5b81adb21114bfe  <repo>/skills/sohrab/alaa-prompting-guide/references/30-sonnet-5.md
8db2279e1f3119f2ecb8d55f77aed31dd6866c950a3c7f8d675ca9b0528ea9fe  <repo>/skills/sohrab/alaa-prompting-guide/references/50-effort-and-thinking.md
35089c86da4a5797501ce9ccda0086149ca5844ff3f97322cd01754b52cc7516  <repo>/skills/sohrab/alaa-prompting-guide/scripts/check_claude_agent_evals.py
1938aa417f253e80f7ba5e0df568f52de43d4ffa399465fcb53293ac84c1b21e  <repo>/skills/sohrab/alaa-prompting-guide/scripts/fixtures/claude-policy/policy-cases.json
```
