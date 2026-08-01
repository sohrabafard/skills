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

### Document-heavy repository

```markdown
# Alaa agent platform binding

Invoke `/alaa-code-intelligence-routing` in Claude Code or `$alaa-code-intelligence-routing` in Codex for non-trivial discovery, artifact routing, duplicate-retrieval questions, or routing setup and evaluation. Native Markdown-scoped tools and `/alaa-repo-docs` in Claude Code or `$alaa-repo-docs` in Codex own repository documents; CodeGraph is available for supported-source claims and Serena for known-document navigation. All surfaces, Git diff, and native gates must resolve to this worktree. Consume the selected primary owner's evidence and use another owner only for one named missing fact. Native gates own proof. Availability grants no additional mutation, data, secret, production, onboarding, memory-write, initialization, or indexing authority. Project hooks retain Serena activation and cleanup and omit `serena-hooks remind` while CodeGraph routing is enabled.
```

## Serena `languages:` profiles

The copy-ready defaults enable only the primary material language, minimizing startup, installation, and background-service effects. The first language is Serena's default or fallback.

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

Document-heavy pack default:

```yaml
languages:
  - python
```

### Optional polyglot expansions

Add a language only after verifying that it is material to the repository, its Serena backend and prerequisites are healthy, and any dependency installation has normal user or repository authority. Some Serena backends may fetch or install components; current PowerShell support is one such case. YAML and Markdown support provides language-server navigation only and does not grant domain or repository-wide semantic ownership.

Optional Laravel expansion:

```yaml
languages:
  - php
  - bash
  - powershell
  - yaml
  - markdown
```

Optional Go expansion:

```yaml
languages:
  - go
  - bash
  - powershell
  - yaml
  - markdown
```

Optional document-heavy pack expansion:

```yaml
languages:
  - python
  - bash
  - powershell
  - yaml
  - markdown
```

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
  fact. Native and domain owners handle non-symbolic documentation,
  configuration, and generated artifacts, and native gates prove completion.
  All evidence and proof surfaces must resolve to this Git worktree. Project
  hooks retain Serena activation and cleanup and intentionally omit
  serena-hooks remind while CodeGraph routing is enabled. Availability grants
  no additional mutation, data, secret, production, onboarding, memory-write,
  initialization, or indexing authority.
```
