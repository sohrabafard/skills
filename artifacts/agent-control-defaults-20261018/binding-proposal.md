# Uniform Beads Binding Amendment

The complete reviewed rollout candidate is `binding-template.md` beside this proposal. It applies these replacements to the current skills Beads block and derives `<repo-name>` from the project label suffix after `repo:`. Substitute only `repo:__PROJECT__`; every project uses the same verified hub. This proposal changes no upstream Beads skill or repository instruction file.

## Start and resume

Insert after the upstream skill/workspace/prime recovery steps and before task-state recovery:

```markdown
Before Beads mutations, claims, ownership comparisons, resume or transfer, load `/alaa-workflow` `references/task-tracking.md` `## Agent identity and ownership`. It owns actor allocation, explicit mutation identity, guarded updates, transfer and closure coordination; its actor rules override actorless upstream examples. If unavailable, stop dependent work. Keep the assigned actor in the existing dispatch or admitted handoff.
```

## Scope and issue lifecycle

Replace the claim bullet with:

```markdown
- Claim before implementation through `/alaa-workflow` `references/task-tracking.md` `## Agent identity and ownership`, and verify its readback. A failed or conflicting claim does not establish ownership.
```

## Issue conventions

Replace the guards bullet with:

```markdown
- Ownership-sensitive mutations follow `/alaa-workflow` `references/task-tracking.md` `## Agent identity and ownership`; guard mechanics and exit 13 follow its `## Beads capabilities in use`.
```

## Quick Reference

Replace the introductory sentence and command block with:

````markdown
Replace `<project-label>` and `<id>` with verified values and `<actor>` with this agent's literal assigned actor from `/alaa-workflow` `references/task-tracking.md` `## Agent identity and ownership`. Its ownership checks, transfer and close coordination apply before these examples. Replace other placeholders with actual values. Run each command separately; all binding rules apply.

```bash
bd ready --label "<project-label>"
bd list --status=in_progress --label "<project-label>"
bd ready --explain --label "<project-label>"
bd blocked --label "<project-label>"
bd --actor "<actor>" create "<title>" --description "<goal, scope, output, plan link>" --acceptance "<criterion or exact plan reference>" --labels "<project-label>" --type <type>
# add when a plan exists: --spec-id "<repo-name>:<repo-relative plan path>"
# add for a follow-up: --deps "discovered-from:<origin-id>"
bd show <id>
bd --actor "<actor>" update <id> --claim
bd show <id>
bd --actor "<actor>" update <id> --if-assignee "<actor>" --if-status in_progress --append-notes "<position, blockers, next step>"
bd show <id>
bd lint <id>
bd stale --label "<project-label>"
bd show <id>
bd --actor "<actor>" close <id> --reason "<verdict>; <commit | HEAD+scoped sha256>; <evidence address>"
bd show <id>
bd prime
```
````

## Integration limits

The workflow owner is the sole naming and ownership policy. Preserve the binding's existing project filtering, hierarchy, evidence, authority and sync rules. Parent integration must review the resulting common block once and verify every authorized project's copy against that same block after substituting only its identity parameters. This proposal itself authorizes no commit or cross-repository write.
