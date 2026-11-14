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

After every review return arrives, consolidate the returns into one finding list before routing.

- Key each finding by root cause: the violated invariant or contract plus the decisive file and symbol. Line number, reporter and wording are not part of the key.
- Merge findings with one key into one item. Keep every reporter and cited location, keep the strongest evidence, and use the highest severity any lens gave.
- Keep different causes at one location as separate items. Keep items separate when the cause match is uncertain.
- Give each item one repair owner. Adversarial-reviewer findings keep the orchestrator packs' route: report them to the user, never route them to repair.

Triage each item by its consequence, not its severity label, because the label is one reporter's view:

- wrong behaviour or a broken contract: fix it;
- a risk without evidence: settle it with one discriminating check, or record it;
- a preference: decline it with a one-line reason.

The parent decides and records triage, except where `alaa-cc-orchestrator` and `alaa-codex-orchestrator` `references/verification-and-gates.md` `## Floors` binds it. Every finding and its disposition appears in the final report, never softened or dropped, so the user can audit the judgment.

Before fixing an item, confirm that the cited location exists, matches the claim and lies in the reviewed scope. A mismatch refutes the item, with file:line evidence.

An item is disputed when a fix returns it as disputed or lens verdicts conflict. Outside the floors, the parent settles it with one discriminating check, or decides it and records the reason. On a floor surface, dispatch one fresh read-only refuter per lens that has disputed items, not one per item, because the parent cannot overrule the floor gate. Use a fresh instance of the role that owns the lens: `alaa-reviewer` for correctness, else the matching specialist. Never use the reporter or the implementer. Send each item's ID, claim, cited evidence and counter-evidence locations. Never send verdicts, severity votes or reporter identity. Stance: "You did not write this code or these findings. Try to refute each item from current code, tests and evidence." The refuter returns exactly one line per item ID: `CONFIRMED`, `REFUTED` or `NEEDS-EVIDENCE`, with evidence. `NEEDS-EVIDENCE` names the exact missing fact. `CONFIRMED` returns to triage, `REFUTED` enters the register below, and `NEEDS-EVIDENCE` joins the user decision set; never fix or drop it. When a refuter cannot run, keep the item as reported.

Register each refuted item, from a citation mismatch or a refuter, at its existing finding owner in the selected task store: key, claim, refutation evidence, refuting role, and reviewed snapshot or commit.

- Every later review or specialist dispatch in the same engagement carries `<refuted_findings>`: key, one-line claim and one-line reason per item.
- A reviewer re-raises a listed item only when code at its location changed since the recorded snapshot or it has new evidence. It marks the re-raise `RE-RAISED: <key>` with that evidence.
- The parent drops a re-raise that meets neither condition and records why.
- A code change at the key location ends that refutation's effect; omit it from later `<refuted_findings>`.

Fix the items triaged for fixing in one pass before the boundary accepts or integrates the change; report the items left for the user as one decision set. Prove the pass and decide any further review under `alaa-cc-orchestrator` and `alaa-codex-orchestrator` `references/verification-and-gates.md` `## After a fix`.
