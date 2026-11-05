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

Finish the whole review or verification pass before any fix. Record each finding when found in the selected task store under `references/task-tracking.md`, on the reviewed issue or as its own `discovered-from` issue when deferred, and continue. A read-only lane returns its findings and its parent records them. Only the early-repair obstruction in /alaa-testing-strategy `references/100-test-execution.md` permits an earlier fix.

Collect every finding a review returns, from the reviewer and each specialist, into one list before routing any fix. Critical/blocker and high/major findings block; medium/minor and low/nit findings defer.

- Adversarially verify each medium-or-higher finding before it enters the list: try to refute it from current code, tests and evidence; drop a refuted finding and record its refutation. A low finding enters without a separate verification agent.
- Fix the blocking findings together in one fix pass and retest before the boundary accepts or integrates the change. At the engagement's final boundary, that same pass and its one consolidated verification run also take the in-scope low-risk deferred findings; report the rest to the user as one decision set.
- Confirm a fix pass with retests; never start a review round to re-check fixes. A blocking finding the retests show still open, or a new defect they expose, enters one more pass within the caller's cycle limit.
