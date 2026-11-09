# Review follow-up templates

## Fix-cycle dispatch

Apply Gate economics in `verification-and-gates.md` to scope and serialize the repair batch. Select the role for this assignment through Failure routing in `routing-matrix.md`. For Ent-owned findings, use the Ent specialist dispatch contract from the common router in `implement` mode. Preserve the repair scope and focused retest limits below. If continuing a lane, apply the common envelope's Mandatory Ponytail binding route. Route a `disputed` result to the finding refuter under `alaa-workflow references/review-mode.md` `## Finding triage`, never to the lead's judgment.

```xml
<task>Resolve reviewer/specialist findings assigned to this repair scope.</task>
<findings_verbatim><root-cause key, file:line, severity, failure, required fix></findings_verbatim>
<role_selection><outcome/scope; settled and open decisions; failure/invariant reasoning; managed profile or admitted external role, selection reason and exceptional-admission evidence go once in `<task_controls>`></role_selection>
<handoff><remaining work, surviving edits/checkpoint, evidence, and retired writer if reassigned; or none></handoff>
<original_scope_and_acceptance>unchanged unless the orchestrator explicitly revises them</original_scope_and_acceptance>
<verification tier="focused">
  <commands><exact focused commands for each fixed finding; scoped lint/type/build></commands>
  <excluded>the full suite, race detector, end-to-end suite, and any other lane's checks</excluded>
</verification>
<task_acceptance><only for the explicitly assigned task owner: exact bounded task-acceptance selectors changed by these fixes, or not assigned></task_acceptance>
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
