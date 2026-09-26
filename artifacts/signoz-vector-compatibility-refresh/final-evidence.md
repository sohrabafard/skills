# Final source refresh evidence

Date: 2026-09-26. Source-only run; no installation, consumer change, live discovery, benchmark, commit, merge or publication. Baseline and final HEAD: main at 3a62cbb615e0180458ebedd4bc9a0794c17c1e60. Candidate 2 source snapshot is candidate-snapshot-2.json: 109 files, aggregate SHA-256 1a890b9bd8f908041a0d63ee32a1fce2eb1c4d67ce56911c2aac13b4e964665f. Changes remain uncommitted and depend on preserving this checkout; the manifest identifies content but is not a backup.

## Release and compatibility coverage

- Vector: official stable product 0.58.0, released 2026-08-26; baseline 0.57.0, no other intervening stable product release. references/81-release-coverage.md maps all 59 product and 3 VRL entries to instructions/examples/tests or justified omissions. GitHub latest's vdev-v0.3.24 is excluded. Canonical references/80-version-and-upgrade-deltas.md separates chart, appVersion, historical consumers and current unknown inventory.
- SigNoz: references/90-versions.md covers 13 app releases from v0.135.1 through v0.143.0, and separates released chart/appVersion, collector, bundled database, upstream stable/LTS and unknown consumers. Public alert history deprecation does not prove route removal or installed SQL-alert support. Existing alert evidence remains unconfirmed and fail-closed without current deployment acceptance.
- Preserved: old consumer paths; vendor-owned read-only schemas, bounded queries and panel shapes; acknowledgement/retry/backpressure and disk I/O failure distinctions; VRL failure assertions, strict warnings, routing confinement and secret/privacy rules. Added version-qualified oversized-record drop/ack and metric-removal guidance, migration/capability coverage, safer version resolution and meaningful checker regressions.

## Independent finding closure

| Role | Final source verdict | Observed closure |
|---|---|---|
| Correctness | APPROVED | 109 hashes match; quoted vendor CLI returns expected 1/two S8; SQL self-test 0; diagnostic controls 10/10; 33 reference files have resolvable relative links; persisted rule is discovery only |
| Instruction | APPROVED | 109 hashes match; 23 coherent children preserve full SQL/schema blocks and mandatory prerequisites; 3 YELLOW lengths independently confirmed; current phase/checkpoint consistent |
| Security | PASS, bounded source closure | 3 changed hashes match; diagnostic controls 10/10; exact original unrelated-error reproduction now produces one failed assertion; mixed offline/runtime flags reject with exit 2 |
| Observability | PASS-WITH-GAPS | Class 4 source gap closed; acknowledged loss and both discard counters route to exactness/recovery/privacy owners; actual delivery/replay remains unverified |
| Release guidance | READY-WITH-CONDITIONS for source guidance only | No remaining distinct source defect; actual release/deployment NOT-READY and not requested; requested exact workflow recheck evidence now recorded below |

Initial findings and reproductions remain in review-cycle-1.md. Original writers repaired their owned files once; reviewers did not edit. No unresolved source finding was reported at closure. Source approval is not runtime/deployment approval.

## Independent native verification

RUN by alaa-verifier on 2026-09-26 from repository root, sequentially, BelowNormal, maximum 180 seconds per command, no environment overrides. Tier: affected; proof: static level 1. Seven command executions comprise six distinct gates: five initial passes, one initial failure, one targeted post-repair pass. All six final gate results pass; the initial failure remains recorded.

| Exact command | Initial exit / seconds | Final disposition |
|---|---|---|
| `python -B scripts/validate_sohrab_skill_pack.py` | 0 / 0.223 | PASS; 69 skills, warnings including Vector body 130 lines, no errors |
| `python -B scripts/check_skill_index.py` | 0 / 0.144 | PASS; both indexes 69, no findings |
| `python -B scripts/check_fleet_references.py` | 0 / 2.837 | PASS; 69 skills, 849 Markdown files, 3812 citations; 325 informational unmarked target paths |
| `python -B scripts/check_lifecycle_contract.py` | 0 / 0.387 | PASS; four states and two reporters |
| `python -B skills/sohrab/alaa-workflow/scripts/validate_workflow_files.py --plan docs/_agent_plans/20260925-224057_signoz-vector-compatibility-refresh.md` | 1 / 0.143 | Initial PRODUCT-FAILURE: two plan.phase-snapshot fields lacked formatted identity. One lead-owned cause-specific repair; exact-command recheck at 2026-09-26T06:07:15.2307133Z returned 0 / 0.144 seconds, no blocking errors, resumable profile |
| `git diff --check` | 0 / 0.064 | PASS; CRLF normalization warnings only |

Verifier checked candidate 2 before and after the combined source gates: all 109 hashes match. Tracked changes are limited to the two skills; no tracked deletions. Scoped new files are limited to target skills, selected workflow family and subject artifacts. Branch/HEAD unchanged. Full status retains inaccessible retired scratch-directory warnings, never represented as inspected or cleaned. Lead wrote authorized evidence while the source verification ran; source manifests remained unchanged. The final workflow recheck reads the completed plan, prompt and checkpoint; a subsequent instruction-review wording correction makes the IMPLEMENTED verdict explicitly not proven; its final targeted check is recorded below.

Focused results in the following section are CITED from the original writer/reviewer executions, not counted as newly RUN combined gates. The tables preserve their exact command, scope, timestamp, exit and proof boundary. There is no claimed global count of all research/help/inspection tool calls.

Final workflow wording closure: the instruction reviewer requested an explicit IMPLEMENTED verdict. The lead changed only that verdict to "not proven; required focused Vector runtime proof blocked", keeping completed source work separate. The lead then ran the exact workflow-validator command above once more at BelowNormal on 2026-09-26: exit 0, no blocking errors, resumable profile. Total combined-tier invocations are therefore eight: seven independent-verifier invocations and one lead invocation earned by this final wording delta. No source check was unnecessarily repeated. The reviewer's other evidence-gap finding was closed by recording the observed independent recheck above.

The instruction reviewer subsequently returned APPROVED for both corrected portions, with no remaining finding. That read-only closure did not itself execute the final validator; the observed lead result above supplies that separate proof. No source or workflow changes followed the final passing check.

## Focused verification and proof limits

Exact writer commands, timestamps, exits and fixture counts are in signoz-focused.md, vector-focused.md and repair-evidence.md. Initial candidate evidence is historical where repairs changed inputs. Final acceptance cites the repaired SQL/link self-tests, quoted CLI controls and diagnostic controls; unchanged schema self-test/green fixture, official URL scan, stable resolver self-test/official version check and resolver syntax retain prior evidence. Independent reviewers reran only discriminating affected assertions. Help output is inspection, never behavioral proof.

Blocked: actual Vector config self-test emitted spawnSync vector.exe EPERM (wrapper 1, checker diagnostic 2); regular check explicitly propagated exit 2. Offline tests do not replace Vector validate/test or VRL runtime. No further unavailable-runtime retry. Earlier TLS retrieval failures are preserved in vector-focused.md; official Node fetch subsequently succeeded without disabling verification.

Unrun/outside authorization: installed SigNoz schema, real SQL, alert acceptance, consumer/deployment inventory, hostile routing and secret/proxy/TLS runtime, drop/ack/replay/recovery/load behavior, chart deployment/admission and activation. Installed role version sentinel drift and unknown effective runtime/grants remain preflight limitations, not migrated or repaired here.

## Documentation and context curation

Final SigNoz narrative grading: 25 GREEN, 3 YELLOW with cohesive comparison/query reasons in repair-evidence.md. Existing entrypoints retained; no files deleted. Vector sole router is YELLOW 52 with single-router rationale. Other changed documents are atomic execution/security/migration contracts or compatibility/coverage decision records; independent instruction review accepted the classifications. Earlier blanket signal-guide exemption is rejected and superseded by the split.

Final curation scanned source research, accepted review judgments, bounded repairs and proof gaps. Release-selection and diagnostic-discrimination knowledge is already promoted into canonical skill owners/tests; duplicating it as memory fails novelty. Runtime blockage is task evidence, not fleet doctrine. No new durable candidate, no unresolved promotion, no memory created or updated. Deferred skills and prior waves remain untouched.

## Agent and accounting provenance

10 distinct agents dispatched, 9 canonical role types; follow-ups reused original writers/reviewers. Requested lead model: GPT-6 Astra. All actual serving identities/efforts and effective role isolation are unknown; configured pins are not observed runtime identity. Tokens unavailable. No commit branch span exists because no commit was authorized.

| Agent | Canonical role | Configured model / effort |
|---|---|---|
| prior_evidence | alaa-researcher | gpt-6-sol / medium |
| signoz | alaa-implementer-sol | gpt-6-astra / high |
| vector | alaa-implementer-sol | gpt-6-astra / high |
| test_contract | alaa-test-strategist | gpt-6-sol / medium |
| correctness | alaa-reviewer | gpt-6-sol / high |
| instructions | alaa-instruction-reviewer | gpt-6-astra / high |
| security | alaa-security-reviewer | gpt-6-astra / high |
| observability | alaa-observability-reviewer | gpt-6-sol / medium |
| release_guidance | alaa-release-guardian | gpt-6-sol / medium |
| verifier | alaa-verifier | gpt-6-luna / low |

Writer escalation criterion: judgment-bearing instruction and compatibility decisions requiring non-obvious design judgment. No model policy was changed. Tool-capacity rejections affected scheduling only, not role substitution or omitted gates.
