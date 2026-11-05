# Design Plan - Ent skill remediation and Go toolchain evidence

- Plan kind: design
- Task ID: `20261105-160000_ent-skill-remediation`
- Profile: resumable
- Task store: local
- Status: planning
- Created: 2026-11-05
- Checkpoint: `docs/agents/20261105-160000_ent-skill-remediation-state.md`
- Approval status: pending
- Approval by: not recorded
- Approval on: not recorded
- Approval evidence: not recorded

## Summary and Outcome

Prepare the Ent skill for reliable use and managed delegation. Correct every finding from review `alaa-0fov`, including the Go diagnostic interpretation. Preserve the user's existing installation.

The reviewed source is commit `7096e6a769a341fc40842ddd7fe141a9175f5ec3` on branch `codex/services-infra-contract`. The worktree was clean before this planning work. Existing follow-up `alaa-bic2` owns future remediation tracking; this design is not an execution task mirror.

The user confirmed that they installed the native specialist before the review to test it. Existing agent files and a visible role are expected observations, not evidence of an unexplained installation. Source integration, installed-file identity, host discovery and successful invocation remain separate evidence.

On 2026-11-05, the user selected conditional Ent adoption with an explicit decision for each project. This approves the policy direction for this design. It authorizes no source implementation, service migration, installation or system update.

## Scope

In scope for the proposed remediation:

- The complete `skills/sohrab/alaa-ent-go-orm-db/` package, its two pack-index entries and targeted regression checks.
- The canonical Alaa Go dependency policy and narrowly triggered Ent companion routing.
- Both managed orchestrator catalogs, neutral role policies, grants, generators and installer integration needed for the specialist.
- Clear separation of bundled and effective Go versions, with no speculative workstation repair.
- Isolated technical validation, independent review and a preview of the eventual installed update.

Outside this plan's present authority: implementation, changes to personal shell/profile files, global Go changes, replacing installed agents, database access, migration apply, push, publication and remote synchronization. Future execution must identify any authorized dependency downloads or disposable database before using them.

Keep files portable and English. Preserve unrelated changes and installed customizations. Keep domain guidance in the skill, runtime allocation in orchestrators, and capability metadata in the prompting guide. Retire files through the repository's archive rule if later needed.

## Confirmed Go Diagnosis

The same Codex environment produced:

| Observation | Result |
|---|---|
| PATH command | Distribution-provided Go launcher with a bundled Go 1.26.8 compiler |
| Process selection setting | `GOTOOLCHAIN=go1.27.3+auto` |
| User Go environment default | The same setting is present in `$HOME/.config/go/env` |
| Normal `go version` | `go version go1.27.3 linux/amd64` |
| `GOTOOLCHAIN=local go version` | `go version go1.26.8 linux/amd64` |
| Selected GOROOT | Existing Go module-cache toolchain for `go1.27.3` |
| Direct selected compiler with `GOTOOLCHAIN=local` | `go version go1.27.3 linux/amd64` |
| Login, non-login and interactive Bash | All three produced the same normal/local version pair |

The previous review intentionally forced `GOTOOLCHAIN=local`. That measured the compiler bundled with the PATH executable, not the compiler selected for ordinary work. The helper documents that limited scope; the review's installation-readiness interpretation was too broad. There is no observed PATH or shell-initialization defect to repair.

The [official Go toolchain documentation](https://go.dev/doc/toolchain) distinguishes these commands and defines environment/default precedence. Keep the current workstation selection. Do not remove the older launcher, hard-code a cache path into profiles, or recommend a system upgrade from this evidence alone.

## Proposed Design

### Package correctness and concise instructions

| Finding or concern | Proposed correction | Observable acceptance |
|---|---|---|
| Missing exclusion heading | Add `When NOT to use` with unrelated Go, other ORMs, infrastructure and policy-conflict alternatives. | Structure checker passes; exclusions route to an owner. |
| Missing English/Persian index entries | Add one accurate entry to each existing index, preserving each file's language. | Index checker passes without a baseline exception. |
| Repeated ownership rules | Consolidate the duplicated end-of-SKILL policy text into one triggered route. | Same constraints and stop conditions; one owner and no broad policy loading. |
| Older consumers and review routing | Distinguish read-only review from adopting/upgrading Ent and Go. | A projection review on an older pinned project performs no unsolicited upgrade. |
| Unsafe generic Clone advice | Explain named eager-load omission and shared traversal closures for the verified release. Build independent traversal roots; apply named loading after a supported clone. | Source links and focused reproduction show the preserved result and branch isolation. |
| Post-commit hook errors | Separate database outcome from errors in ancillary post-commit work. Preserve outbox/idempotency guidance. | A post-commit failure is not reported as a rolled-back write or blindly replayed. |
| EXPLAIN authority ambiguity | Require an authorized target and permission for the exact diagnostic command; otherwise use existing sanitized plans. | A DSN-only request causes no connection or statement execution. |
| NOT VALID wording | Distinguish INSERT and relevant key updates from unrelated updates of legacy FK violations. Keep orphan checks and explicit validation. | An unchanged invalid FK does not count as validated because another column changed. |
| Existing-database baseline gap | Add an explicit empty-versus-existing database decision and the precise Atlas import/baseline reference. Verify equivalence and later pending migrations before any authorized revision change. | Existing tables are not recreated; revision bookkeeping is not used to hide drift. |
| Installation-surface ambiguity | Route managed installation to `install-skills.md`; identify supported standalone alternatives without duplicate personal copies. | A verified source-to-installed map and one intended definition per host identity. |

Apply the prompting guide's behavior-preserving compression pass after the draft. Read selected-release source for technical changes; never copy a current example into an older pinned API without verification.

### Go helper and reporting

Keep the helper's no-download local probe and existing exit meanings. Fix `workspace_for()` so `GOWORK=auto` follows the unset discovery path. Preserve `off`, absolute paths, invalid-relative rejection, workspace precedence and missing-evidence handling.

Separate three conclusions in the guidance and result interpretation:

- The bundled compiler found on PATH.
- The effective compiler selected by the current environment and project.
- Module/workspace minimum versions and generation/build compatibility.

A bundled compiler below the baseline does not prove that the effective compiler is below it. Preserve existing JSON fields for compatibility; make the selected binary and evidence scope explicit. Do not report unexercised automatic selection as a failed effective toolchain.

Use the existing `--go` option to inspect an already established effective compiler directly. This avoids a new toolchain resolver. In this verified environment, the following command shape succeeded:

```bash
ent_go_root="$(go env GOROOT)"
GOTOOLCHAIN=local "$ent_go_root/bin/go" version
python3 skills/sohrab/alaa-ent-go-orm-db/scripts/check_go_baseline.py   --project "$ENT_MODULE_ROOT" --go "$ent_go_root/bin/go"
```

Run selection commands in the intended module. In an unknown environment, normal Go commands can download a toolchain; first establish existing local availability or use an authorized download scope. The helper itself must retain its no-download contract. Never silently change GOTOOLCHAIN, GOENV, module directives or CI pins to make a check pass.

Regression coverage must discriminate unset/auto/off/absolute/invalid-relative workspace settings, a nested module, no workspace, old bundled versus adequate selected compiler, unsupported or missing compiler, and malformed directives. Use controlled subprocess doubles only for owned decision logic. Preserve a real command observation for the reported version distinction. Do not add wording-only tests.

### Conditional Alaa adoption policy

The canonical decision belongs to `alaa-golang/references/40-production-ready-package-catalog.md`, with data-layer and kit owners consulted where their surfaces change.

Replace the blanket prohibition with a narrowly scoped conditional Ent entry only after implementation is authorized. Existing services retain their current pgx/sqlc/repository approach. A project must record an explicit adoption decision, scope, migration/object ownership, pool/transaction integration and rollback approach before adopting Ent. No existing service migrates merely because this skill is installed or selected.

The Ent skill routes Alaa adoption to the canonical catalog before dependency setup or SQL replacement. It must not duplicate admission policy. Generic Ent projects remain usable without private companion dependencies. Shared kit additions require their own scope and authority; invent no kit API or second pool.

### Managed specialist integration

Use the existing `alaa-ent-specialist` identity. Admit it through both orchestrators' actual catalog/trigger/role-source mechanisms and both prompting-guide capability registries. Keep models and efforts out of role defaults. Add exact tool grants and canonical source-loading behavior through existing generation and materialization owners.

The skill remains the domain owner. Native adapters stay thin. Avoid creating independent copies of domain rules in orchestrator prompts. Mirror shared behavioral changes across Codex and Claude while preserving their documented runtime mechanics.

Delegate only eligible Ent work that benefits from a separate lane. Generic PostgreSQL work continues to its existing owner. The specialist implements or advises within its assigned scope. Independent acceptance uses the existing reviewer/verifier authority with the Ent skill; do not claim an enforceable read-only gate from a write-capable adapter. A required restricted review must use verified effective grants or remain blocked.

Trace installer inclusion from source inventory instead of adding a second installer. Update generator/manifests and installer documentation only where the admitted role changes them. Test in a fresh scratch destination before touching the user's installed files. Existing test-installed files must be compared and preserved until an authorized update selects their replacement.

### Proposed ordering and independence

Core skill/helper corrections and the approved-direction policy draft can proceed independently after execution authorization. Managed role admission depends on the settled specialist contract. Final package/index integration consumes those results and freezes one candidate for consolidated validation.

Technical behavior checks follow the changed decisions. Independent instruction and correctness review consume the frozen candidate. An installation preview follows accepted source checks. A live installed update and fresh-host smoke test require the intended target scope to be authorized.

On execution approval, continue `alaa-bic2` through the workflow owner. Register genuinely independent lanes and allocate actual role/model/effort controls then. This design sequence grants no execution authority.

## Verification Design

All commands below are proposed future checks unless listed under Design Evidence. Use the repository root unless another working directory is stated. Capture exit/result and the tested candidate; a missing dependency or unrun check remains unavailable proof.

| Surface | Required evidence |
|---|---|
| Pack structure and indexes | `python3 -B scripts/validate_sohrab_skill_pack.py`; `python3 -B scripts/check_skill_index.py` |
| References and lifecycle | `python3 -B scripts/check_fleet_references.py`; `python3 -B scripts/check_lifecycle_contract.py` |
| Skill metadata | The installed `skill-creator` quick validator against the Ent directory |
| Helper correctness | Focused behavior cases described above, including the already reproduced GOWORK=auto regression |
| Managed role sources | In each affected orchestrator: `python3 -B scripts/render_agents.py --check`, `python3 -B scripts/validate_pack.py`, and `python3 -B scripts/check_agent_contracts.py` |
| Grants and installer | Applicable `check_agent_grants.py`; Codex scratch materialization and validation; scoped installer tests/dry-run for the admitted role |
| Capability registration | Both model-policy checkers in `alaa-prompting-guide`, covering each changed role root; an aggregate may replace an identical covered child |
| Ent behavior | A pinned disposable fixture for generation/build and Clone/named-edge/traversal behavior; a focused commit-hook outcome case |
| PostgreSQL behavior | Authorized disposable PostgreSQL for NOT VALID FK update/validation and migration-baseline cases, with no production DSN |
| Agent behavior | Ordinary older-version review, DSN-only diagnostics, denied self-approval, authorized dependency setup, and conditional Alaa adoption scenarios |
| Installation | Preview source/installed differences; after separate authorized apply, observe canonical skill loading and exact native role invocation in fresh sessions |

Refresh version-sensitive official evidence at execution. Run focused checks while editing, then one reconciled candidate collection. Repair failed or invalidated paths within the active retry budget. Do not repeat unaffected broad suites. Size parallelism for available capacity and isolate shared fixtures.

No benchmark is required for this documentation/helper change. Do not claim measured query speedups. Runtime and installation evidence must not be replaced by static validators or tabletop outcomes.

## Skill Bindings

Paths below resolve from the repository root. These are decision owners, not an execution-role allocation.

| Skill | Source | Load before | When | If unavailable |
|---|---|---|---|---|
| alaa-workflow | `skills/sohrab/alaa-workflow/SKILL.md` | Admission and continuity | always | Stop dependent workflow work. |
| alaa-prompting-guide | `skills/sohrab/alaa-prompting-guide/SKILL.md` | Instruction and role changes | always | Stop instruction changes. |
| alaa-code-intelligence-routing | `skills/sohrab/alaa-code-intelligence-routing/SKILL.md` | Source evidence selection | always | Use only an already named native owner. |
| alaa-testing-strategy | `skills/sohrab/alaa-testing-strategy/SKILL.md` | Verification design and execution | always | Stop dependent proof claims. |
| alaa-golang | `skills/sohrab/alaa-golang/SKILL.md` | Alaa Go policy and dependency decisions | Alaa adoption or Go behavior changes | Stop affected policy work. |
| alaa-data-layer | `skills/sohrab/alaa-data-layer/SKILL.md` | Database ownership decisions | Store, migration or transaction policy changes | Stop affected data decisions. |
| alaa-ent-go-orm-db | `skills/sohrab/alaa-ent-go-orm-db/SKILL.md` | Ent domain work | Ent examples and behavior | Stop domain changes. |
| alaa-codex-orchestrator | `skills/sohrab/alaa-codex-orchestrator/SKILL.md` | Codex role admission | Managed Codex integration | Stop that integration. |
| alaa-cc-orchestrator | `skills/sohrab/alaa-cc-orchestrator/SKILL.md` | Claude role admission | Managed Claude integration | Stop that integration. |
| alaa-codex-runtime-ops | `skills/sohrab/alaa-codex-runtime-ops/SKILL.md` | Harness diagnosis | Codex/WSL environment mismatch | Preserve failure; no speculative config repair. |
| skill-creator | `skills/.system/skill-creator/SKILL.md` | Skill validation and forward testing | Available canonical installed skill may take precedence | Report missing validator; do not install implicitly. |

## Decisions

| Date | Owner | Decision | Reason |
|---|---|---|---|
| 2026-11-05 | User | The native specialist was installed before the independent review for testing. | Correct provenance; preserve the existing installation. |
| 2026-11-05 | User | Permit Ent conditionally through an explicit adoption decision for each project. | Allow deliberate adoption without automatic service migration. |
| 2026-11-05 | Planning agent | Keep the existing workstation Go selection; distinguish bundled/effective evidence. | All three shell modes run Go 1.27.3 normally; local override explains 1.26.8. |
| 2026-11-05 | Planning agent | Propose canonical managed admission and existing independent reviewer roles. | Avoid bypassing grants or creating duplicated domain authority. |
| 2026-11-05 | Planning agent | Keep overall design approval pending. | The request is to prepare a plan; the policy answer does not authorize implementation. |

## Open Questions

- Overall execution approval is pending. No unresolved product choice blocks completion of this planning deliverable.
- At execution, identify the authorized disposable module/dependency and PostgreSQL test environment before any provisioning or access.
- Before an installed update, confirm the intended personal Codex/Claude targets and obtain authorization for the concrete validated diff.
- Upgrading the system Go launcher is optional and outside the recommended fix. Reconsider only if the user requires local-only tooling to use the newer bundled compiler everywhere.

## Acceptance Criteria

- Every confirmed defect and lower-priority review concern is corrected or explicitly resolved at its canonical owner with evidence.
- The source pack's mandatory gates pass without weakened assertions, new suppressions or fabricated runtime results.
- GOWORK=auto behaves like unset. An older PATH launcher with an adequate effective compiler is not described as an unavailable current compiler.
- No toolchain, dependency, database, permission or installation change happens without the authorized scope for that effect.
- Conditional Ent adoption requires the user-selected per-project decision and preserves existing service choices.
- Both managed runtimes admit the specialist consistently; exact grants and canonical loading are verified before dependent dispatch.
- Implementation and acceptance remain independent. Source, static, generation, compile, database, performance and host-invocation evidence remain distinct.
- The user's test installation is preserved through comparison, preview, authorized update and rollback evidence.

## Design Evidence

- The repository remained at the reviewed commit before this plan; only this design family is changed by the planning turn.
- Bound issue `alaa-bic2` is open and contains no implementation authority. Review `alaa-0fov` is closed with a negative installation-readiness verdict; its comment preserves the full finding set and logs.
- Normal and local Go version probes succeeded in login, non-login and interactive Bash; all returned the same version pair documented above.
- Direct execution of the already selected cached compiler with GOTOOLCHAIN=local returned Go 1.27.3, exit 0.
- Official Go toolchain documentation was refreshed on 2026-11-05. No dependency download, system update or database call was performed for this diagnosis.
- Design validation: the plan-family validator passed with no blocking errors on 2026-11-05; all 11 skill binding sources resolved. A final staged whitespace check precedes the local documentation commit.

## Handoff Package

- Confirmed facts: reviewed commit and all review evidence are in `alaa-0fov`; user installation provenance and policy choice are recorded above; direct Go observations establish bundled/effective distinction.
- Open assumptions: fresh installed canonical-skill loading, managed admission and Ent/PostgreSQL runtime fixtures remain unverified; the future gates above define their proof.
- Ruled out: shell mode or PATH drift as the cause in this host; a mandatory Go reinstall; treating direct native installation as managed admission; treating source checks as runtime proof.
- Read first on resume: this plan; `docs/agents/20261105-160000_ent-skill-remediation-state.md`; `skills/sohrab/alaa-ent-go-orm-db/SKILL.md`; `skills/sohrab/alaa-golang/references/40-production-ready-package-catalog.md`; then the review and follow-up records through the bound Beads owner.
- Environment notes: plain `go version` selects 1.27.3; `GOTOOLCHAIN=local go version` measures the 1.26.8 launcher bundle. Resolve the effective GOROOT in the intended project before using its compiler through `--go`; hard-code no cache path.
- Traps: a visible native role need not satisfy managed grants; a skill link can point into the source worktree; a plan commit does not approve implementation; missing proof is not failed behavior.

## Design Position

- Position owner: `docs/agents/20261105-160000_ent-skill-remediation-state.md`
