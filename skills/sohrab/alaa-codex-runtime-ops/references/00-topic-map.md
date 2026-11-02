# Alaa Codex Runtime Ops Topic Map

Match the observed condition. Apply every recovery under `SKILL.md` procedure and safety rules.

| You are about to | Read | Decision owned there |
|---|---|---|
| Recover sandbox setup/launch failure, a denied filesystem operation, or blocked network access; decide whether a command may run outside the sandbox | `references/10-wsl-sandbox-recovery.md` | Evidence, exact-command escalation, authority and denial handling |
| Diagnose Bash syntax, executable/path mismatch, command length, filesystem permissions, Docker socket access or port binding | `references/20-command-and-path-discipline.md` | Linux command diagnosis and smallest permitted recovery |
| Inspect Git dubious ownership, an unreadable/active transcript, missing chats or Codex state/config | `references/30-git-session-and-locked-file-recovery.md` | Scoped trust, active-file safety and private-state evidence |
| Recover a Node, Vite, Vitest, Quasar or Yarn gate | `references/40-project-fallbacks.md` | Repository-verified command candidates and proof limits |
| Make a durable claim about Codex, WSL, Bash, Docker, Git or a project-specific fallback | `references/90-source-map.md` | Current primary sources and freshness limits |

## Maintenance

Keep the existing external router as the single reference map. Put recovery details in the owning reference and domain policy in its owning skill. Add recurring failure signatures only from observed evidence, with symptom, diagnosis, smallest retry and fallback. Historical findings require confirmation against current sources.
