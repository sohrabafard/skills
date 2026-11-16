# Review Semantics

Review the requested surface. Create workflow files only when the user asks for them or a continuing fix loop needs durable state. An ordinary review needs no subagent, prompt pack, checkpoint or JSON state. Use an independent reviewer role only when the user requests a prompt pack or the review needs real context isolation.

## Evidence and must-check areas

Run the smallest meaningful validation when authorized. Separate confirmed defects from risks, questions and out-of-scope recommendations.

Check each of these where it applies:

- behavioral correctness and failure handling;
- security, authorization, tenancy and sensitive data;
- concurrency, reliability, performance and observability;
- architecture and ownership boundaries;
- tests that prove behavior and not implementation details;
- documentation or contract drift;
- exact validation evidence, or the reason a gate could not run.

## Output

Lead with findings ordered by severity. For each finding, give the affected file or surface, the evidence, the impact and the smallest safe remediation. End with a verdict and a validation summary. When no actionable issue exists, say so.

Use the orchestrator packs' reviewer verdicts, `APPROVED`, `APPROVED-WITH-NITS` or `CHANGES-REQUESTED`, so that a phase can pass a verdict between an inline review and an orchestrated lane without translation.

## Finding triage

Finish the whole review or verification pass before any fix. Record each finding when you find it, in the selected task store under `references/task-tracking.md`: on the reviewed issue, or as its own `discovered-from` issue when deferred. A read-only lane returns its findings and its parent records them. Only the early-repair obstruction in /alaa-testing-strategy `references/100-test-execution.md` permits an earlier fix.

After every review return arrives, consolidate the returns into one finding list before routing:

- Key each finding by root cause: the violated invariant or contract plus the decisive file and symbol. Line number, reporter and wording are not part of the key.
- Merge findings with one key into one item. Keep every reporter and cited location and the strongest evidence, and use the highest severity that any lens gave.
- Keep different causes at one location as separate items. Keep items separate when the cause match is uncertain.
- Give each item one repair owner. Adversarial-reviewer findings keep the orchestrator packs' route: report them to the user, never route them to repair.

Triage each item by its consequence, not by its severity label, because the label is one reporter's view:

- wrong behaviour or a broken contract: fix it;
- a risk without evidence: settle it with one discriminating check, or record it;
- a preference: decline it with a one-line reason.

The parent decides and records triage, except where `alaa-cc-orchestrator` and `alaa-codex-orchestrator` `references/verification-and-gates.md` `## Floors` binds it. The final report carries every finding and its disposition, never softened or dropped, so that the user can audit the judgment.

Before you fix an item, confirm that the cited location exists, matches the claim and lies in the reviewed scope. A mismatch refutes the item, with file:line evidence.

An item is disputed when a fix returns it as disputed or lens verdicts conflict. Outside the floors, the parent settles it with one discriminating check, or decides it and records the reason. On a floor surface, the parent cannot overrule the floor gate:

- Dispatch one fresh read-only refuter per lens that has disputed items, not one per item. Use a fresh instance of the lens owner's role (`alaa-reviewer` for correctness, else the matching specialist), never the reporter or the implementer.
- Send each item's ID, claim, cited evidence and counter-evidence locations. Never send verdicts, severity votes or reporter identity.
- Stance: "You did not write this code or these findings. Try to refute each item from current code, tests and evidence."
- The refuter returns exactly one line per item ID: `CONFIRMED`, `REFUTED` or `NEEDS-EVIDENCE`, with evidence. `NEEDS-EVIDENCE` names the exact missing fact.
- `CONFIRMED` returns to triage. `REFUTED` enters the register below. `NEEDS-EVIDENCE` joins the user decision set; never fix or drop it.
- When a refuter cannot run, keep the item as reported.

Register each refuted item, from a citation mismatch or a refuter, at its existing finding owner in the selected task store: key, claim, refutation evidence, refuting role, and reviewed snapshot or commit.

- Every later review or specialist dispatch in the same engagement carries `<refuted_findings>`: key, one-line claim and one-line reason per item.
- A reviewer re-raises a listed item only when code at its location changed since the recorded snapshot, or when it has new evidence. It marks the re-raise `RE-RAISED: <key>` with that evidence.
- The parent drops a re-raise that meets neither condition and records why.
- A code change at the key location ends that refutation's effect; omit the item from later `<refuted_findings>`.

Fix the items triaged for fixing in one pass, before the boundary accepts or integrates the change. Report the items left for the user as one decision set. Prove the pass and decide any further review under `alaa-cc-orchestrator` and `alaa-codex-orchestrator` `references/verification-and-gates.md` `## After a fix`.
