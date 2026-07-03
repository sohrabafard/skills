# Obsidian Usage

## Vault roles

- `agent-memory`: Basic Memory vault and agent-queryable curated memory.
- `docs`: human sticky notes, personal prompts, rough notes.
- `skills/skills/sohrab`: skill source of truth.

## Properties

Use flat frontmatter. Quote internal links in YAML:

```yaml
related_notes:
  - "[[Service Ownership Matrix]]"
```

Use body relations for agent-queryable typed links:

```md
## Relations

- governs [[Notification Command Contract]]
```

## Templates

Templates live in `00-control/templates/`. They are writing contracts, not automatic Basic Memory behavior. Agents must be instructed to use the matching template.

## Graph hygiene

Use Obsidian to review backlinks, orphan notes, duplicate notes, stale notes, and weak tags. Do not turn graph neatness into memory bloat.
