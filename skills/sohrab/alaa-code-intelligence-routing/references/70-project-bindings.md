# Project bindings and Serena profiles

Project bindings are always-loaded declarations. Keep them short: name the available surfaces, their invocation, the worktree identity requirement, and the repository-native proof owner and source. The full decision procedure remains in `/alaa-code-intelligence-routing` (`$alaa-code-intelligence-routing`).

## Copy-ready project bindings

### Laravel repository

```markdown
# Alaa agent platform binding

Invoke `/alaa-code-intelligence-routing` in Claude Code or `$alaa-code-intelligence-routing` in Codex for non-trivial discovery, artifact routing, duplicate-retrieval questions, or routing setup and evaluation. CodeGraph, Serena, and Laravel Boost are available; their roots, Git diff, and native gates must resolve to this worktree. Consume the selected primary owner's evidence and use another owner only for one named missing fact. Native gates own proof. Availability grants no additional mutation, data, secret, production, onboarding, memory-write, initialization, or indexing authority. Project hooks retain Serena activation and cleanup and omit `serena-hooks remind` while CodeGraph routing is enabled.
```

### Non-Laravel source repository

```markdown
# Alaa agent platform binding

Invoke `/alaa-code-intelligence-routing` in Claude Code or `$alaa-code-intelligence-routing` in Codex for non-trivial discovery, artifact routing, duplicate-retrieval questions, or routing setup and evaluation. CodeGraph and Serena are available; their roots, Git diff, and native gates must resolve to this worktree. Consume the selected primary owner's evidence and use another owner only for one named missing fact. Native gates own proof. Availability grants no additional mutation, data, secret, production, onboarding, memory-write, initialization, or indexing authority. Project hooks retain Serena activation and cleanup and omit `serena-hooks remind` while CodeGraph routing is enabled.
```

## Serena `languages:` policy and minimal profiles

`languages:` selects the semantic backends Serena may run. It is not an inventory of repository file types, a declaration of what the agent may read, or a way to make Serena understand every artifact. Files whose languages are absent remain available to native scoped search and read and to their domain owner.

Every additional language may add another language server, prerequisite, installation, startup, indexing, memory, or background-process cost. Use this selection procedure:

1. Enable Serena only when the repository has a recurring known-symbol, reference, hierarchy, diagnostic, or semantic-edit question that requires it.
2. Start with one primary material language. The first language is Serena's default or fallback.
3. Never add `markdown`; repository documents use native tools and `/alaa-repo-docs` (`$alaa-repo-docs`). Do not add Bash, PowerShell, YAML, or another language merely because matching files exist or the agent must understand them; route ordinary configuration, CI, container, and script questions to native or domain owners.
4. Add exactly one language when a named recurring task requires that backend's semantic capability, the native owner cannot preserve the required guarantee, its prerequisites and health are verified, and its observed resource cost is accepted.
5. Remove a language when that recurring semantic requirement no longer exists. Do not preserve speculative fleet-wide expansions.

When Serena is disabled or unavailable by project policy, do not create a placeholder `languages:` profile merely for repository coverage.

Laravel default:

```yaml
languages:
  - php
```

Go default:

```yaml
languages:
  - go
```

HAProxy gateway with material Lua source:

```yaml
languages:
  - lua
```

Use the Lua profile only when the live repository contains material `.lua` source. HAProxy configuration, rendered configuration, Helm, YAML, Compose, shell, and generated artifacts remain outside Serena.

WA uses the Go profile when `<repo>/wa-api/go.mod` exists and is material to the current repository. Verify that Serena exposes the nested module in the same Git worktree; otherwise activate `<repo>/wa-api` rather than adding YAML, Markdown, Bash, PowerShell, or another unrelated language.

## Final `initial_prompt`

Use this concise declarative value with the selected profile:

```yaml
initial_prompt: >-
  Invoke /alaa-code-intelligence-routing in Claude Code or
  $alaa-code-intelligence-routing in Codex for non-trivial discovery, artifact
  routing, duplicate-retrieval questions, or routing setup and evaluation.
  CodeGraph and Serena are enabled; use Laravel Boost only when repository
  instructions declare it. Each current question has one primary owner whose
  returned evidence is consumed; use another owner only for one named missing
  fact. Native and domain owners handle repository documentation,
  configuration, and generated artifacts, and native gates prove completion.
  All evidence and proof surfaces must resolve to this Git worktree. Project
  hooks retain Serena activation and cleanup and intentionally omit
  serena-hooks remind while CodeGraph routing is enabled. Availability grants
  no additional mutation, data, secret, production, onboarding, memory-write,
  initialization, or indexing authority.
```
