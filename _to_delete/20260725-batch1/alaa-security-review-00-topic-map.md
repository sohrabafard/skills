# Alaa Security Review Topic Map

Use this file to choose the smallest relevant section in `full-guide.md`.

## Covered sections

- `# Purpose`
- `# When to use`
- `# Constraints`
- `# Fast Gate (default) — quick, practical, high-signal`
- `## 1) Trust boundaries (2 minutes)`
- `## 2) Authn/authz (tenant-aware)`
- `### JWT quick checks (apply when JWT is used)`
- `### OAuth/OIDC quick checks (apply when OAuth/OIDC is used)`
- `## 3) Injection & validation`
- `## 4) Secrets & tokens`
- `## 5) Rate limiting & abuse controls`
- `## 6) Data protection`
- `## 7) Dependencies & container hygiene`
- `# “Stop the line” findings (must fix before merge)`
- `# Deep Review (escalate when risk is high)`
- `## 1) Identify trust boundaries & data flows`
- `## 2) Threat modeling (pragmatic)`
- `## 3) JWT/OAuth design review (when applicable)`
- `### Key management (JWT)`
- `### Claim strategy (JWT)`
- `### Access token`
- `### Refresh tokens (recommended)`
- `### Revocation strategy`
- `### Sender-constrained options (optional; evaluate)`
- `### OAuth 2.0 security posture (when OAuth flows exist)`
- `### Testing (minimum)`
- `## 4) Deployment hardening review`
- `## 5) Output a prioritized remediation list (P0/P1/P2)`
- `# Output contract`
- `# Anti-patterns`
- `references/90-source-map.md`

## Working rule

- Read only the sections you need from `full-guide.md`.
- Read `90-source-map.md` before relying on version-sensitive security guidance.
- Keep this topic map small and update it when major sections are added or renamed.
