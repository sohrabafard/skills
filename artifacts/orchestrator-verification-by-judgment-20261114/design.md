# Design: verification by judgment (pack version 6.0.0)


## The owner's words
The current skills force agents into test, review and fix cycles. A fixed cap on cycles is superficial and ignores the situation. "I expect the agent to decide and act like a senior developer."

## Diagnosis
The doctrine assigns verification by role and by stage, not by the change. `references/verification-and-gates.md` says: "Model capability never waives an observer or mandatory gate."; "implementer evidence never replaces independent acceptance."; "The analyst diagnoses and never fixes."; and SKILL.md lets the lead implement only a mechanical edit. So every defect crosses at least three hand-offs (reviewer finds, implementer fixes, verifier retests, sometimes the reviewer reads again), whether it is a typo or a change to authentication. One week of sessions showed it: 122 follow-ups to implementers against 28 implementation dispatches in Codex; 13 of 16 non-pass reviews in Claude Code led to another implementation dispatch.

## Principle
The lead owns the outcome. It decides how much verification each change needs, as a senior developer does: from what could be wrong, what a miss would cost, and what evidence already exists. The pack supplies the decision model, the evidence standard and a short list of floors. It prescribes no pipeline.

## The verification decision
Made once per task at plan time, recorded in one or two lines in the plan or compact dispatch, and revisited only when the task changes materially. The lead answers:
1. What can be wrong here that the author's own focused check would not show? (effects in other modules, concurrency, consumers of a contract, a trust boundary, data.)
2. What does a miss cost, and can it be undone? (blast radius, reversibility, exposure of production data, tenants, money or a public contract.)
3. What evidence exists already, and does it hold for this snapshot? (who observed it, on which inputs, whether anything it covers changed since.)
4. What is the cheapest check that could prove the change wrong? Run that one. Stop adding checks when the next one could not change the decision.

From the answers the lead chooses, per task, among: accept the author's observed focused evidence; read the diff itself; have an independent verifier run named checks; an independent reviewer; a specialist gate. An independent observer needs a reason drawn from questions 1 and 2: the lead writes what the observer can see that the author cannot, or what the miss would cost. "The pipeline says so" is not a reason.

## Floors
An independent gate is always required, whatever the lead judges, for a change to: authentication, authorization or tenant isolation; secrets or cryptography; billing or money; a destructive or irreversible data operation, including a migration that drops or rewrites data; a breaking change to a public contract; a production deployment or release. Also when the user asks for a review. On a floor surface the author never approves its own work, the gate's blocking verdict binds the lead, and implementer evidence does not replace the gate. State each floor with its reason in one clause (what an undetected miss does). Keep the existing specialist triggers in `references/routing-matrix.md` as the way to pick which gate; do not widen them.

## Evidence
Observed evidence counts by what it shows, not by who ran it. An implementer's observed focused check on the same snapshot is evidence the lead may accept outside the floors, and the lead says that it did. An independent re-run is for a floor surface, or for evidence that is stale, unobserved or ambiguous. Nothing unchanged is checked again.

## Findings
The lead triages each finding by its consequence, not by its label:
- wrong behaviour or a broken contract: fix it;
- a risk without evidence: settle it with one discriminating check, or record it;
- a preference: decline it with a one-line reason.
A reviewer reports each finding with its evidence and its consequence. Outside the floors the decision is the lead's, and it records it. Every finding and its disposition appears in the final report; none is softened or dropped. That visibility replaces ritual: the user can audit the judgment.

## After a fix
Whoever fixes proves the fix with the check that failed, or with the check that would have caught the defect. A further review happens only for a stated reason: the fix changed the design, it touched a floor surface, or the first review could not see what it needed. There is no cycle count. A new round needs a new reason. When a second round finds blocking findings of the same kind, the lead stops repairing and reconsiders the approach or the decomposition, and tells the user when it cannot resolve that itself.

## Who fixes
The smallest capable hand. The lead may make a small, local, obvious correction itself when that is cheaper than a dispatch and within the authorized scope; this replaces the "mechanical edit only" exception. The implementer that holds the context continues for anything larger. Read-only roles stay read-only by their tool grants; a diagnosis may carry the proposed fix.

## What does not change
The lane-branch commit protocol, model and effort allocation, the stack-bound roles, the fan-out limit rule, the return headers and report contracts, the lifecycle states, and everything `alaa-testing-strategy` owns about which tests are owed, check collection, batch repair and result classification (those reduce cycles). Authority limits on push, deploy, publish and destructive actions stay exactly as they are.

## Where it lands
- Both `references/verification-and-gates.md`: replace the stage pipeline and "Gate economics" absolutes with the verification decision, floors, evidence, findings, after-a-fix and who-fixes rules. Keep the commit protocol and merge timing sections. The file must get shorter.
- Both `SKILL.md`: the stages, the main-thread contract ("must not implement beyond ...", "run heavy verification", "permit self-approval") and the profile table. Decide whether the `lean` and `hardened` profiles still earn their place; the verification decision is the mechanism now, so remove a profile rule that only restates it.
- Both `assets/implementation-contract.md` and the reviewer, verifier and failure-analyst definitions: sentences such as "Your results never discharge independent acceptance" and any sentence that tells a role to demand or expect a re-review. Re-render generated files.
- Both `references/delegation-prompts*`: the review and fix-cycle templates.
- `alaa-workflow/references/review-mode.md` (it owns finding triage and the verdict vocabulary across a lane boundary): make triage consequence-based as above; keep the vocabulary.
- `alaa-testing-strategy`: change a sentence only if it mandates an independent observer or a repeat run regardless of risk; allocation and independence belong to the orchestrators.
- Checkers: `scripts/check_agent_contracts.py` in both orchestrators and `alaa-testing-strategy/scripts/check_execution_contracts.py` hold literals of the old doctrine. Update a literal to the new key sentence when its text changed on purpose. Where a check enforces an absolute this design removes, change that check to assert the new rule's key sentence, and report the exact before and after. Any other logic change: stop and report.
- VERSION 6.0.0 and a CHANGELOG entry in both orchestrators that names the owner's direction and what was removed.

## Style
Write decision guidance with its reason, not prohibition lists: a model of this generation follows a rigid rule literally and judges well from a goal, a criterion and a reason. Short sentences, one idea each. The pair stays mirrored. No fixture, self-test or model comparison. Nothing is deleted; no machine path; English only.

## What to report back
What you removed (quote the old absolute), what replaced it and where; every checker change with before and after; each place where the old doctrine and this design could not be reconciled and what you chose; net size change of the edited files; the gate exit codes.
