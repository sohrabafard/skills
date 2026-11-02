# WSL skill path audit - 2026-10-23

Task: alaa-da7x. Three user-requested Luna lanes audited disjoint scopes; one lane also
independently reviewed the two edits. Only the Windows source checkout was edited.

## Coverage and changes

The supplied Codex listing contains 175 unique installed targets: 70 first-party, 39 curated,
and 66 vendor. Every supplied symlink target is a Linux path in the user's skills checkout.
No separate Claude listing was supplied; shared source corrections apply if Claude links to
these same sources, but live Claude discovery was not tested.

- Workflow companion routing now requires absolute installed-source paths to use the target
  execution host's syntax: POSIX for Linux/WSL, Windows syntax for Windows.
- Codex runtime guidance distinguishes POSIX path notation from PowerShell and retains the
  historical Windows-only discovery evidence; it does not claim WSL discovery was tested.
- First-party audit and recursive text/reference/script scans of 105 curated/vendor targets
  found no additional actionable Windows-only runtime paths. Explicit Windows instructions
  (including screenshot and optional Hindsight PostgreSQL setup) were preserved.
- Vendor trees, existing Gortex staged/worktree changes, and all WSL files were untouched.

## Evidence

- Cross-skill reference checker: passed, no findings.
- Lifecycle contract checker: passed, no findings.
- Independent review: no findings in the two edited references.
- Git diff whitespace and both edited files' UTF-8 without BOM / LF checks: passed.
- Full pack structure checker: failed on existing Magfa missing exclusion section and
  agents/openai.yaml; warnings were also present before these edits.
- Full index checker: failed on existing Magfa omissions from both indexes and its missing
  agents/openai.yaml. Existing tasks alaa-rqcy and alaa-xrc cover these unrelated gaps.
- No runtime skill discovery, WSL synchronization, commit, push, or Dolt remote sync performed.

Reviewed source SHA-256:

- skills/sohrab/alaa-workflow/references/companion-routing.md : 9CCC9D3C11BFE76B622056BF42AB52DD487D257956025F13D3898995E40AD2F8
- skills/sohrab/alaa-prompting-guide/references/11-codex-runtime-features.md : 519A4A5878912DEDF0E86D151B386348C030E36AC99E93481D55E3C5A7654E17
