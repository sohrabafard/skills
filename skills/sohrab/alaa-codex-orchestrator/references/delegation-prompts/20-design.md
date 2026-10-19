# Design and test strategy templates

## Test strategist

```xml
<task>Design the minimal test matrix that proves: <acceptance criteria>.</task>
<doctrine>Apply /alaa-testing-strategy, which owns the method: derive the matrix from the failure modes this change introduces, drop every candidate that is not owed a test and record why, name the plausible broken implementation each test must fail against, place each behaviour at exactly one layer, bind every double that can drift, give each test its topic and layer selector and its shared setup, and assign each claim the proof level it requires.</doctrine>
<failure_models><plausible broken implementations and failure modes to catch></failure_models>
<repository_commands><known test commands and helpers></repository_commands>
<action_safety>Read-only; do not write tests.</action_safety>
```

## Architecture critic

```xml
<task>Pressure-test this architecture and its implemented candidate: <plan and candidate>.</task>
<review_boundary>Consume the inherited <cadence> through references/verification-and-gates.md. Judge only at its declared phase|final boundary: the complete phase candidate for phase, or whole-engagement candidate including pending earlier phases for final. Nested invocations never reset that scope. Return missing, conflicting or premature cadence to the parent without judgment.</review_boundary>
<standard>Judge it against /alaa-system-design, which owns this design method: the six conditions requiring a design pass, the boundary and seam tests, contract-before-code, one writer per datum with every second copy labelled cache or fork, the dependency classification, and the two-candidate rule. Its references/70-review-and-readiness.md states what blocks at each step.</standard>
<design_record><pre-implementation design record; if absent, state which design-pass condition fired and report the missing record></design_record>
<invariants><required correctness, compatibility, security, and operability invariants></invariants>
<evidence><architecture docs, relevant code paths, external contracts></evidence>
<question>Find blockers, hidden assumptions, simpler alternatives, rollout/rollback conditions.</question>
```
