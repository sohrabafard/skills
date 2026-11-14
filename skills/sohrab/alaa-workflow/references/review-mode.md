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

Lead with findings ordered by severity. For each finding, give the affected file or surface, evidence, impact, and smallest safe remediation. End with a verdict and validation summary. If no actionable issue exists, say so directly.

Use the same verdict vocabulary as the orchestrator packs' reviewer contract — `APPROVED`, `APPROVED-WITH-NITS`, or `CHANGES-REQUESTED` — so a review reads the same whether it ran inline here or as an orchestrated lane, and a phase can hand a verdict across that boundary without translation.

Do not require a subagent, prompt pack, checkpoint, or JSON state for an ordinary review. Use an independent reviewer role only when the user requests a prompt pack or the review needs real context isolation.

## Finding triage

Finish the whole review or verification pass before any fix. Record each finding when found in the selected task store under `references/task-tracking.md`, on the reviewed issue or as its own `discovered-from` issue when deferred, and continue. A read-only lane returns its findings and its parent records them. Only the early-repair obstruction in /alaa-testing-strategy `references/100-test-execution.md` permits an earlier fix.

After every boundary review return arrives, from the reviewer and each triggered specialist, consolidate them into one finding list before verification or repair routing. A critical, blocker, high or major finding blocks. A medium, minor, low or nit finding defers.

- Key each finding by root cause: the violated invariant or contract plus the decisive file and symbol. Line number, reporter and wording are not part of the key.
- Merge findings with one key into one item. Keep every reporter and cited location, keep the strongest evidence, and use the highest severity any lens gave.
- Keep different causes at one location as separate items. Keep items separate when the cause match is uncertain.
- Give each item one repair owner. Adversarial-reviewer findings keep the orchestrator packs' route: report them to the user, never route them to repair.

Verify each medium-or-higher item in two tiers before routing. Low and nit items enter with no verification.

1. Parent check: confirm the cited location exists, the code there matches the claim, and the location is in the reviewed scope. Refute only on a citation mismatch, with file:line evidence. Never refute on judgment, because the parent must not soften an independent gate.
2. Refuter: an item is disputed when the parent check cannot settle it, a fix cycle returns it as disputed, or lens verdicts conflict. Dispatch one fresh read-only refuter per lens that has disputed items, not one per item. This applies also when the parent did the review itself. Use a fresh instance of the role that owns the lens: `alaa-reviewer` for correctness, else the matching specialist. Never use the reporter or the implementer. Send each item's ID, claim, cited evidence and counter-evidence locations. Never send verdicts, severity votes or reporter identity. Stance: "You did not write this code or these findings. Try to refute each item from current code, tests and evidence." The refuter returns exactly one line per item ID: `CONFIRMED`, `REFUTED` or `NEEDS-EVIDENCE`, with evidence. `NEEDS-EVIDENCE` names the exact missing fact.
3. Route the result: `CONFIRMED` routes by severity under this triage, and `REFUTED` enters the register below. `NEEDS-EVIDENCE` joins the user decision set; never fix or drop it. When a refuter cannot run, keep the item as reported.

Register each refuted item, from the parent check or a refuter, at its existing finding owner in the selected task store: key, claim, refutation evidence, refuting role, and reviewed snapshot or commit.

- Every later review or specialist dispatch in the same engagement carries `<refuted_findings>`: key, one-line claim and one-line reason per item.
- A reviewer re-raises a listed item only when code at its location changed since the recorded snapshot or it has new evidence. It marks the re-raise `RE-RAISED: <key>` with that evidence.
- The parent drops a re-raise that meets neither condition and records why.
- A code change at the key location ends that refutation's effect; omit it from later `<refuted_findings>`.

Then repair:

- Fix the blocking findings together in one fix pass and retest before the boundary accepts or integrates the change. At the engagement's final boundary, that same pass and its one consolidated verification run also take the in-scope low-risk deferred findings; report the rest to the user as one decision set.
- Confirm a fix pass with retests; never start a review round to re-check fixes. A blocking finding the retests show still open, or a new defect they expose, enters one more pass within the caller's cycle limit.
