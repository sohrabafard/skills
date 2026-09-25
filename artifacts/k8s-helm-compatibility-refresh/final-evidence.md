# Compatibility refresh: final evidence

Outcome: source implementation complete; overall completion BLOCKED. Evidence
date is 2026-09-26 in the task's local timezone; command JSON records UTC timestamps.
No commit, merge, installation, publication, deployment, cluster/provider operation,
dependency upgrade, deletion or global configuration change occurred.

## Candidate and changes

- Branch `main`, HEAD `12680f2fd18f4a5ac3822cc3cc130b05524053fd`, unchanged from planning.
- Source/gate manifest: `candidate-manifest.sha256`, 58 files, SHA-256
  `df86cde6dc83d0486e00a8aedc3325654831659ca88c6272de25539d7e82c8e2`.
- Actual source diff, including the new untracked fixture: `candidate.diff`.
- Dated source URLs, local inventory, supported versus authoring bands and unknown
  consumers: `compatibility-ledger.md`; preflight details: `preflight.md`.
- Seven modified source files: SKILL.md; references/version-awareness.md,
  SOURCES.md, validation-workflows.md, kubernetes-resource-patterns.md;
  scripts/check_versions.py and check_manifests.py. One new file:
  scripts/fixtures/version-reference.md. All are under the selected skill.
- Lead changed only the selected three-file workflow family and subject artifacts.
  No staged changes, other skills, consumers, vendor, root scripts, indexes,
  model policy or installed copies were changed.

Version facts and command conditions now distinguish upstream support, authoring
compatibility and actual client/consumer evidence. The old Kubernetes floor and
Helm consumer path remain. Corrected Helm atomic alias, externalIPs deprecation
and HPA maturity claims. The freshness checker rejects preview-only observations
and wrong-year EOL dates, with fixed synthetic self-test expectations. Manifest
security rejection predicates did not change. Namespace, RBAC, least privilege,
OpenShift arbitrary UID/nonroot, immutable identity, served APIs, chart gates,
failure handling and the Arvan ownership boundary were preserved.

## Observed checks and limits

| Evidence | Result | Tier and proof | Exact records |
|---|---|---|---|
| Writer help/self-tests/clean fixture/regressions/whitespace | Seven distinct commands passed; eight executions, including whitespace after final prose change; 17 freshness and 7 manifest self-test cases | focused, static/unit | writer/implementation-evidence.md and logs |
| Structure, index, fleet references, lifecycle, agent contracts | Five commands, each exit 0; all 58 hashes matched pre/post | affected, independent Level 1 static | verification-agent/verdict.md and command JSON/logs |
| Helm lint plus four local renders and four manifest validations | Nine commands, each exit 0, installed Helm 4.2.3 | affected, local CLI/fixture proof only | verification/helm-lint.*, render-134 through render-137.*, manifest-134 through manifest-137.* |
| Source Markdown links | Exit 0; six source Markdown files | affected, static | verification/source-links.* |
| Final workflow links and whitespace | Both exit 0 after final workflow edits; links in three workflow files validated | affected, static only; not workflow-validator proof | verification/workflow-links.* and final-diff-check.* |
| Live freshness | Two process exit 2 results: timeout, then connection timeout with --timeout 30 | ENVIRONMENT-BLOCKED; no freshness PASS | verification/freshness* and runtime-and-network-blockers.md |
| Workflow validator | Two exit 1 results; second after snapshot repair; missing literal paths field syntax remains | BLOCKED after retry budget | workflow-validation.md |
| Bash startup probe | Exit 1 before Bash ran: CreateFileMapping / Win32 error 5 | ENVIRONMENT-BLOCKED; no Bash example or shell-checker runtime proof | runtime-and-network-blockers.md |

The original chart-good fixture contained only a comment template. The lead built
`chart-smoke/` from its unchanged metadata/schema and the committed clean manifest,
so render/manifest checks consumed actual synthetic workloads. Rendering 1.37
capabilities on Helm 4.2.3 does not prove a supported client/server pairing.
No Helm 3 or Helm 4.3 binary was available. No kubeconform/yamllint/oc executable
was returned by the PATH inventory. Schema admission, actual consumers, installed
skill activation, server-side checks and measured quality are unrun/unproven.

## Independent review and completion

- Instruction reviewer: APPROVED, no findings; `instruction-review.md` preserves
  coverage and exclusions. It independently verified the candidate hashes.
- Canonical correctness reviewer: NOT RUN. Two dispatch attempts hit runtime
  thread capacity. No third attempt or silent role replacement; recovery is in
  `runtime-and-network-blockers.md`.
- IMPLEMENTED: proven by focused proof on the identified uncommitted snapshot.
- MERGE_CANDIDATE: not proven; correctness review, freshness and workflow gate open.
- RELEASE_CANDIDATE and PUBLISHED: not requested.

## Documentation, curation and accounting

Changed skill instructions, source ledger and synthetic fixture are EXEMPT-ATOMIC:
they encode ordered procedures, one compatibility decision table or a test payload.
Workflow and evidence records are exempt named artifacts. No unrelated splitting
or compression was performed. Source links passed; final workflow-link evidence is
separate. Writer evidence distinguishes deliberate behavior changes from wording.

Final curation scanned research, implementation and validation boundaries. No new
durable candidate was admitted: compatibility knowledge already lives in its owner;
volatile failures remain task evidence. No memory was written, and excluded Arvan,
normalization, W2 and deferred skill work were not reopened.

Four agents dispatched, four distinct roles: researcher Sol/medium; writer
Astra/high; instruction reviewer Astra/high; verifier Luna/low. All observed
serving identities unknown. Writer escalation criterion: instruction-artifact
judgment and backward compatibility. Failed reviewer dispatches are not agents.
Final snapshot recapture matched the same 58-file digest; `final.diff` includes the
complete source delta. Validation execution count: 29; two self-test results
carried forward by citation into verifier evidence. This count excludes source
reads, snapshots, tool inventory and the failed Bash startup probe. Branch span:
unavailable because no authorized commit exists. Token counters are unavailable.
