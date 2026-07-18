# Platform Audit — YYYY-MM-DD

<!--
Location: <kit-repo>/docs/audits/YYYY-MM-DD-<scope>-audit.md
Rules: references/40-platform-audit.md. Default posture: observe and file documents, do not fix (unless fixes were
explicitly authorized). Every finding maps to exactly one filed action. During KIT_FIRST_STABILIZATION the scope is
kit-only and consumer prompts/actions are forbidden.
-->

```yaml
type: platform-audit
date: YYYY-MM-DD
phase: KIT_FIRST_STABILIZATION | consumer-reactivated
kit_version_or_commit: <version/commit>
scope: <kit-only | kit + explicit consumer list>
auditor_runtime: <claude-code | codex>
fixes_authorized: yes | no
```

## 1. Coverage and evidence boundary (honest scope)

| repo/surface | access | how audited | dimensions skipped + why |
|---|---|---|---|
| alaa-go-chi | full | code + CONTRACTS.md + open change requests + <commands> | |
| <consumer (reactivated only)> | full \| docs-only \| none | | |

<Host/network/runner/truth-tier gaps. During kit-first: state that all consumers are NOT_ASSESSED_KIT_FIRST and
were not inspected.>

## 2. Findings (most severe first; session-verified or marked `suspected`)

### F-1: <title>

- severity: critical | high | normal   (suspected: yes/no — if yes, what would confirm it)
- where: <repo path:line/symbol or doc §>
- dimension: correctness | security | concurrency | contracts-governance | observability | performance-evidence |
  generated-deploy-ci | kit-surface-reimplementation | wrap-hygiene | duplication | behavioral-divergence | drift
- principle/contract: <P1–P13 / CONTRACTS section / governance rule>
- evidence: <what you saw / ran>
- risk: <correctness, security, data, race, contract, observability, capacity>
- fix: <smallest safe remediation>
- action filed: <exact filename of change request / baseline proposal / prompt / drift note — or fix status>

## 3. Duplication matrix (cross-consumer; reactivated audits only)

| logic shape | where seen (repo:path × N) | verdict | action |
|---|---|---|---|
| <e.g. retry/backoff helper> | <a:…, b:…> | baseline candidate \| emerging \| ruled service-local (cite decision) | <proposal filename or —> |

## 4. Validation and production-readiness boundary

<Targeted/full/race/static/contract/gen/governance/truth-tier/render/load/HA/chaos/CI/SLO — each `passed`,
`failed`, `blocked`, `skipped`, or `not run`. Name the evidence tiers that remain missing for any SLA claim.>

## 5. Follow-up ledger

| finding | action file / fix | owner mode | status |
|---|---|---|---|
| F-1 | <filename> | kit-owner \| change-request \| propagation (reactivated only) | filed \| fixed-and-validated \| blocked |

## 6. Registry corrections made

<Rows updated/added in docs/CONSUMERS.md within phase limits, or "none".>
