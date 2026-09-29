# Review follow-up templates

## Fix-cycle dispatch

```xml
<task>Resolve reviewer/specialist findings in original lane <n>.</task>
<findings_verbatim><file:line, severity, failure, required fix></findings_verbatim>
<original_scope_and_acceptance>unchanged unless the orchestrator explicitly revises them</original_scope_and_acceptance>
<verification><the focused checks for each fixed finding, plus the affected-tier checks the fix reaches></verification>
<output>For each finding: fixed | disputed with repository evidence; touched files; verification; new risks.</output>
```

## Documenter

```xml
<task>Update documentation for verified shipped change: <goal>.</task>
<change_summary><actual behavior, files, configuration/API/operational changes></change_summary>
<verdicts><review and specialist verdicts></verdicts>
<scope><expected documentation files/sections></scope>
<checks><docs formatter, links, examples, scope check, and the size grade></checks>
<size_grade>Grade every eligible narrative document by the ladder in alaa-repo-docs references/15-document-size-and-clustering.md and report each final grade with the reason that file requires.</size_grade>
<action_safety>Documentation files only; no intended or unverified behavior.</action_safety>
```
