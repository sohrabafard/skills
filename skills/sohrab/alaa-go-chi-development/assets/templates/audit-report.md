# Platform Audit — YYYY-MM-DD

<!--
Location: <kit-repo>/docs/audits/YYYY-MM-DD-<scope>-audit.md
Rules: references/40-platform-audit.md. Default posture: observe and file documents, do not fix unless fixes were
explicitly authorized. Every finding maps to exactly one filed action.
Fill `phase` and `phase_record` from the read described in references/05-phase-and-source-truth.md — copy what the
read returned; do not type a phase name from memory. Sections 3 and the per-consumer rows exist only when the
matching capability cell allowed the work; where it did not, keep the section and write what was not done and why.
-->

```yaml
type: platform-audit
date: YYYY-MM-DD
phase: <phase name exactly as the session-start read returned it>
phase_record: <docs/change-requests/... path the read named>
kit_version_or_commit: <version/commit>
scope: <kit-only | kit + the explicit consumer list the phase permitted>
auditor_runtime: <claude-code | codex>
fixes_authorized: yes | no
```

## 1. Coverage and evidence boundary

| repo/surface | access | how audited | dimensions skipped, and why |
|---|---|---|---|
| alaa-go-chi | full | code + CONTRACTS.md + open change requests + <commands> | |
| <consumer> | full \| docs-only \| not inspected — capability cell `<name>` was `<value>` | | |

<Host, network, runner, and real-dependency gaps. Name every consumer that was not inspected and the capability
cell that prevented it.>

## 2. Findings — most severe first, session-verified or marked `suspected`

### F-1: <title>

- severity: critical | high | normal   (suspected: yes/no — if yes, what would confirm it)
- where: <repo path:line/symbol, or doc §>
- dimension: correctness | security | concurrency | contracts-governance | observability | performance-evidence |
  generated-deploy-ci | kit-surface-reimplementation | wrap-hygiene | duplication | behavioral-divergence | drift
- principle/contract: <P-number / CONTRACTS section / governance rule>
- evidence: <what you saw or ran>
- risk: <correctness, security, data, race, contract, observability, capacity>
- fix: <smallest safe remediation>
- action filed: <exact filename of the change request, baseline proposal, prompt, or drift note — or fix status>

## 3. Duplication matrix

<Only when cross-consumer analysis was permitted. Otherwise state which capability cell blocked it.>

| logic shape | where seen (repo:path × N) | verdict | action |
|---|---|---|---|
| <e.g. retry/backoff helper> | <a:…, b:…> | baseline candidate \| emerging \| ruled service-local (cite decision) | <proposal filename or —> |

## 4. Validation and readiness boundary

<Every gate run, each with an outcome word from references/05-phase-and-source-truth.md, and the proof level it
reached. Name every evidence type still missing for any SLA claim.>

## 5. Follow-up ledger

| finding | action file / fix | owner mode | status |
|---|---|---|---|
| F-1 | <filename> | kit-owner \| change-request \| propagation | filed \| fixed-and-validated \| blocked |

## 6. Registry corrections made

<Rows updated or added in docs/CONSUMERS.md within the capabilities held, or "none".>
