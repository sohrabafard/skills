# Review Semantics

Review the requested surface without creating workflow files unless the user asks for them or a continuing fix loop needs durable state.

## Evidence order

1. Read the named plan, objective, diff, issue, or review artifact first.
2. Inspect current repository behavior and nearby tests.
3. Run the smallest meaningful validation when authorized.
4. Separate confirmed defects from risks, questions, and out-of-scope recommendations.

## Must-check areas

- behavioral correctness and failure handling;
- security, authorization, tenancy, and sensitive data when relevant;
- concurrency, reliability, performance, and observability when relevant;
- architecture and ownership boundaries;
- tests that prove behavior rather than implementation details;
- documentation or contract drift;
- exact validation evidence or the reason a gate could not run.

## Output

Lead with findings ordered by severity. For each finding, give the affected file/surface, evidence, impact, and smallest safe remediation. End with a verdict and validation summary. If no actionable issue exists, say so directly.

Use the same verdict vocabulary as the orchestrator packs' reviewer contract — `APPROVED`, `APPROVED-WITH-NITS`, or `CHANGES-REQUESTED` — so a review reads the same whether it ran inline here or as an orchestrated lane, and a phase can hand a verdict across that boundary without translation.

Do not require a subagent, prompt pack, checkpoint, or JSON state for an ordinary review. Use an independent reviewer role only when the user requests a prompt pack or the review needs real context isolation.

## Finding triage

Collect every finding a review returns, from the reviewer and each specialist, into one list before routing any fix. Critical/blocker and high/major findings block; medium/minor and low/nit findings defer.

- Adversarially verify each medium-or-higher finding before it enters the list: try to refute it from current code, tests and evidence; drop a refuted finding and record its refutation. A low finding enters without a separate verification agent.
- Fix blocking findings and retest before the boundary accepts or integrates the change.
- Record deferred findings in the selected task store under `references/task-tracking.md`. At the engagement's final boundary, fix the in-scope low-risk ones together in one consolidated fix pass, followed by one consolidated verification run; report the rest to the user as one decision set.
- Never start a review round only to re-check low-finding fixes.
