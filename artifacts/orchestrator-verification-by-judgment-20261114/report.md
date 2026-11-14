# Verification by judgment (2026-11-14)

Sixth engagement of the day on the orchestrator pair. Beads issue: `alaa-mdv8s`. This record is dated evidence; verify current repository facts before reusing a conclusion.

## Why

The pack owner asked for a management report during a long run and said, in substance: stop launching test and review cycles; one problem with the current skills was that they force agents into such cycles, and that is why the upgrade was requested. A first proposal (count an approval with nits as accepted, restrict the changes-requested verdict, lower the cycle cap from two to one) was rejected by the owner as superficial and blind to the situation: "I expect the agent to decide and act like a senior developer."

## Diagnosis

The doctrine assigned verification by role and by stage, not by the change. Absolutes such as "Model capability never waives an observer or mandatory gate", "implementer evidence never replaces independent acceptance" and "The analyst diagnoses and never fixes" meant that every defect crossed at least three hand-offs, whether it was a typo or a change to authentication. A cap on the number of cycles does not touch that structure.

## What changed (pack version 6.0.0)

The design is [design.md](design.md). In short:

- **One verification decision per task**, made by the lead at plan time from four questions and recorded in one or two lines: what the author's own check cannot show; what a miss costs and whether it can be undone; what evidence already holds for this snapshot; the cheapest check that could prove the change wrong.
- **An independent observer needs a stated reason.** The pipeline is not a reason.
- **Floors.** A mandatory independent gate stays on authentication, authorization and tenant isolation; secrets and cryptography; money; destructive or irreversible data operations; a breaking change to a public contract; a production deployment or release; and any surface the user asks to have reviewed. A fix on a floor surface returns to that floor's gate.
- **Evidence counts by what it shows, not by who ran it.** Nothing unchanged is checked again.
- **Findings are triaged by consequence** (fix; settle with one check or record; decline with a reason), and every finding with its disposition appears in the final report.
- **No cycle count.** A further round needs a new reason; a returning defect class sends the lead back to the approach or the decomposition.
- **The smallest capable hand fixes.** The lead may make a small, local, obvious correction itself.

Removed: the `lean`, `standard` and `hardened` profiles; the mandatory verifier and reviewer stages; "Gate economics"; the maximum-cycles rule; the absolutes quoted above. The checkers now assert the floors and the key sentences of the decision.

Unchanged: the lane-branch commit protocol, model and effort allocation, the stack-bound roles, the fan-out rule, the return headers, the lifecycle states, and what `alaa-testing-strategy` owns about owed tests, check collection, batch repair and result classification.

## How it was done

One design by the lead, one implementation lane (`alaa-implementer`, requested opus/high) on a lane branch, one independent instruction review, no confirmation pass. The review returned CHANGES-REQUESTED with three major findings: a disputed finding outside the floors still forced a refuter dispatch; one routing sentence still scheduled a contract review for every contract change; and a fix on a floor surface could be approved by its own author. All eleven findings were applied by the same lane. Record: [review.md](review.md). The repaired text was not re-read by a reviewer; the gates passed on it.

## Validation observed

On `main` at the merge commit `b937a229`, each exited `0`: the four root checkers, the installer unittest, both orchestrators' render check, pack validator, grants and contracts checkers, the three `alaa-prompting-guide` checkers, the execution-contract checker, the constitution template check and the memory checksum. The agents of pack version 6.0.0 were installed for both runtimes under the owner's standing authorization; a final Claude Code dry run reported 34 unchanged.

## Limits

- No task has run under the new doctrine yet. Whether agents now verify in proportion is unobserved.
- `references/verification-and-gates.md` still describes Stages A to F as the order of work; it lost its absolutes but not its length.
- One sentence outside the edited scope keeps the old rule: `alaa-go-chi-development references/10-consumer-development.md` deletes a test "only once an independent reviewer accepts that finding".
- `alaa-workflow` validators and phase templates still use the phrase "inherited review"; they were not assessed.
- Not pushed.
