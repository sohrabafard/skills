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
