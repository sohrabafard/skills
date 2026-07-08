# Platform Audit — YYYY-MM-DD

<!--
Location: <kit-repo>/docs/audits/YYYY-MM-DD-platform-audit.md
Rules: alaa-go-chi-development skill, references/40-platform-audit.md.
An audit observes and files documents; it does not fix. Every finding maps to exactly one filed action.
-->

```yaml
type: platform-audit
date: YYYY-MM-DD
kit_version_at_audit: <version/commit>
auditor_runtime: <claude-code | codex>
```

## 1. Coverage (honest scope)

| repo | access | how audited | dimensions skipped + why |
|---|---|---|---|
| alaa-go-chi | full | code + CONTRACTS.md + open change requests | |
| <consumer> | full \| docs-only \| none | | |

## 2. Findings

One block per finding, most severe first. Only session-verified claims (file:line or command evidence);
otherwise mark `suspected` with what would confirm it.

### F-1: <title>
- severity: critical | high | normal   (suspected: yes/no)
- where: <repo file:line / doc §>
- dimension: kit-surface-reimplementation | wrap-hygiene | version-currency | seam-bug | registration |
  duplication | behavioral-divergence | kit-gap | drift
- principle: <P-number when applicable>
- evidence: <what you saw / ran>
- action filed: <exact filename of the change request / baseline proposal / propagation prompt / drift note>

## 3. Duplication matrix (cross-consumer)

| logic shape | where seen (repo:path × N) | verdict | action |
|---|---|---|---|
| <e.g. retry/backoff helper> | news:…, notif:… | baseline candidate \| emerging (1 real + 1 designed) \| ruled service-local (cite the recorded decision) | <proposal filename or —> |

## 4. Follow-up ledger

| finding | action file | owner mode | status |
|---|---|---|---|
| F-1 | <filename> | K \| CR \| propagation | filed |

## 5. Registry corrections made

<Rows updated/added in docs/CONSUMERS.md, or "none".>
