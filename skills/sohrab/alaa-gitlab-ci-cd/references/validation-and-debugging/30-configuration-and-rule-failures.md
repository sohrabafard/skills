# Configuration and rule failures

Open this guide when YAML/schema or pipeline-creation rules prevent the expected pipeline. For version-sensitive claims, follow the [source map](../00-source-map.md).

### 1. YAML or schema failure

*Symptoms:* parse error; "config should be an array of hashes"; an unknown
keyword; a referenced job or stage that does not exist.

*Diagnose:* run `validate_gitlab_ci.py` on the file; then CI Lint for the merged
result. A `!reference` tag is valid GitLab syntax — a tool reporting it as a
syntax error is the tool's defect, not the file's.

*Smallest retry:* fix the file and push; configuration changes take effect on a
new pipeline, not on a re-run of an existing job.

*Escalate when:* the merged configuration is valid and the file alone is not —
the problem is in an included file, which is class 2.

### 2. Pipeline creation or rule evaluation failure

*Symptoms:* no pipeline created; jobs unexpectedly missing; a parent pipeline
exists and the child does not; two pipelines for one push.

*Diagnose:* read `workflow:rules` top to bottom for the actual event, then the
job's own `rules:`. Check whether `include:` resolved and whether the component
or input defaults are what you think. Check the pipeline source: the value in
`$CI_PIPELINE_SOURCE` for this run is often not the one the rule assumed.

*Smallest retry:* trigger the same event again — a push, or a merge request
update — rather than re-running an existing pipeline.

*Escalate when:* the rules are provably correct for the event and the pipeline
still does not appear; that is an instance or permission problem.
