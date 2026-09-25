# Selected normalization and Arvan corrections

Reviewed local result; no commit, installation, consumer mutation, cluster access or external publication performed.

| Lifecycle | Verdict |
|---|---|
| IMPLEMENTED | Proven on final scoped snapshot; uncommitted recovery risk remains |
| MERGE_CANDIDATE | Proven for the selected local pipeline: required affected checks and independent correctness/instruction review passed; no integration requested |
| RELEASE_CANDIDATE | Not requested |
| PUBLISHED | Not requested |

## Changes

- `skills/sohrab/alaa-input-normalization/references/10-normalization-contract.md`: distinguish 1:1 digit folding from NFC; compare text length with NFC(input), typed with text.
- `skills/sohrab/alaa-input-normalization/references/30-backend-middleware-binding.md`: complete PHP example, remove undefined fieldName, use explicit exact dotted opt-in paths. Explain namespace/autoload assumptions and Laravel literal-dot key collision. Consumers accepting literal-dot keys require separate selection design; no custom traversal or new rejection rule.
- `skills/sohrab/alaa-input-normalization/scripts/test_laravel_middleware_example.php`: execute the actual Markdown snippet on real Laravel, assert query/form/JSON, nested selection, NFC, non-string and key preservation, characterize unsupported dot collision, report unavailable dependency input as 2.
- `skills/sohrab/caas-arvan-kuber/SKILL.md`: resolve loaded checker root and rendered.yaml explicitly, quote paths, preserve --profile arvan and exits 0/1/2, require 0 for completion.

Canonical implementations and corpus remain byte-identical to baseline. Other skills, root instructions and installed copies unchanged.

## Evidence and reviews

- [Normalization focused evidence](./normalization-evidence.md): 145 corpus cases in two modes, existing composition case, PHP syntax and real Laravel 13.23.0 on PHP 8.5.8. Some focused commands lack individual timestamps; their later snapshot time is not misrepresented as command time.
- [Arvan focused evidence](./arvan-evidence.md): checker self-test 7 cases; literal Bash valid=0, invalid=1, missing checker=2. Original MSYS sandbox startup failure and successful exact outside-sandbox validation recorded separately.
- [Independent verification](./verification.md): pack, index, fleet references, lifecycle, whitespace, document links/line budgets and actual Laravel example passed. Changed normalization inputs reverified after one fix cycle; unchanged index/lifecycle and Arvan/reference evidence cited.
- [Correctness review](./correctness-review-final.md): APPROVED; all three [initial findings](./correctness-review-1.md) resolved by original owner.
- [Instruction review](./instruction-review.md): APPROVED on final snapshot.
- [Preflight](./preflight.md): root/branch/HEAD, installed-role agreement and observable permission limits.

## Identity

Branch `main`, HEAD `34aeb11db38e1408b1760d9fe3f4c1fec16d0498`, unchanged from planning. [Held manifest](./held-snapshot.json): `93adc14f11bf9daf79881014dc5803437f21ca88c9d3dbd3c17cc38b6e56a5b9`. Method: SHA-256 of sorted repository-relative path, NUL, file SHA-256, LF records; 376 selected source/tool files; HEAD and scoped tracked diff separately bound. Workflow/evidence metadata excluded to avoid self-reference. [Original held snapshot](./held-snapshot-v1.json) preserves pre-fix evidence. No writes overlapped independent source verification.

## Limits and deferred findings

- No unresolved selected-scope correctness or instruction finding. Example adoption is limited to literal input keys without dots; variable-length collection matching is not implicitly enabled.
- Real framework in-process proof does not prove deployed consumer registration before validation. Four-runtime normalization harness unrun; no fresh parity claim.
- No installed activation, live model-quality evaluation, benchmark or live-cluster compatibility claim. Parent requested Astra; observed model/effort unknown for lead and children. Required installed role definitions match source, but installed version sentinel is stale (3.6.0 vs source 4.0.0); no remediation authorized/performed. Effective inherited MCP isolation unknown; lanes used scoped native operations.
- Incidental unchanged Arvan matrix/OpenAPI --check failed (core/v1/pods binding/exec mismatch); excluded from selected repair. Other unselected malformed reference commands were not swept. No claim that the entire skill's historical audit is clean.
- Git cannot enumerate some retired _to_delete scratch directories; unrelated untracked inventory there remains unknown. Selected roots and tracked diff were inspected.
- Documentation grades: normalization contract ORANGE 126 lines, backend reference ORANGE 155, Arvan SKILL YELLOW 92; coherent contract/procedure context preserved. Workflow/evidence are exempt atomic artifacts.

## Reusable context and accounting

Final alaa-extract-agent-lessons scan: no new durable candidate admitted. The Unicode/framework lessons now belong to the corrected source; known sandbox recovery already has an owner; stale installation metadata is volatile task evidence. No memory write, repository promotion, or reopened pipeline remains.

Five agents, four distinct roles: normalization and arvan (alaa-implementer, configured gpt-6-sol/high); verify (alaa-verifier, gpt-6-luna/low); correctness (alaa-reviewer, gpt-6-sol/high); instructions (alaa-instruction-reviewer, gpt-6-astra/high). No model override/escalation; observed runtime identities unknown. One correctness fix cycle. Follow-ups reused agents.

Independent acceptance accounting: 7 initial commands + 6 changed-input commands + two workflow validator attempts = 15 command executions; snapshot/identity guards excluded. Final focused evidence cites 13 results (7 normalization, 5 Arvan repair, 1 excluded OpenAPI failure); discovery commands and environment startup probes excluded. Branch span unavailable because no authorized commit exists. Session tokens not observable.

Final workflow gate first attempt exited 1: completed phases lacked inline HEAD/SHA-256/path fields required by the validator. The existing recorded identities were inserted into each phase; no source content changed. One cause-specific metadata repair and retry, with the failed result preserved.

Workflow validator retry exited 0 (resumable profile, no blocking errors). The first metadata failure was repaired; no skill content changed.

## Final staging reconciliation

On resume, task workflow/evidence and the new PHP example appeared staged although this run issued no staging command. Existing index state was preserved; no stage/unstage/reset occurred. HEAD and every one of the 376 source/tool-input hashes remained identical to the reviewed snapshot. The old whole-diff guard reported CHANGED because previously untracked workflow/evidence now entered Git diff, including the manifest itself. Preserved that manifest as held-snapshot-before-staging-reconciliation.json; aligned the helper's Git diff scope with its declared source/tool roots and exclusions, then held the same content digest. This repairs evidence bookkeeping, not product tests or acceptance assertions. Final independent identity-only check is recorded in verification.md.
