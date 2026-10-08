# Review follow-up templates

## Fix-cycle dispatch

```xml
<task>Resolve reviewer/specialist findings in original lane <n>.</task>
<findings_verbatim><file:line, severity, failure, required fix></findings_verbatim>
<role_selection><exact registered profile from ratified plan; outcome/scope; settled and open decisions; failure/invariant reasoning; selection reason; exceptional admission: applicable high-workhorse inadequacy with context/spec/tool corrections and decomposition consideration, or explicit user direction></role_selection>
<handoff><remaining work, surviving edits/checkpoint, evidence, and retired writer if reassigned; or none></handoff>
<original_scope_and_acceptance>unchanged unless the orchestrator explicitly revises them</original_scope_and_acceptance>
<verification tier="focused">
  <commands><exact focused commands for each fixed finding; scoped lint/type/build></commands>
  <excluded>the full suite, race detector, end-to-end suite, and any other lane's checks</excluded>
</verification>
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
