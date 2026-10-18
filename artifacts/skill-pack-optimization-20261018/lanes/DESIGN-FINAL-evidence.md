# DESIGN-FINAL repair evidence

Baseline full-read SHA-256 (all 10 owned files; no scripts exist):

```json
{
  "skills/sohrab/alaa-system-design/agents/openai.yaml": "c0313d0822d199c5e493ff6313bfea3b5aa450738ae866a39526ebb86164853e",
  "skills/sohrab/alaa-system-design/assets/design-record-template.md": "3fac5e7c1d1482213ee37e4a63f7cccc7c95e7f4f0c81eb08cf9840589ae838a",
  "skills/sohrab/alaa-system-design/references/10-boundary-and-seam.md": "16c3d53fbb962dadad4f2efa722e662d7598ba9b253aefd146e7b2977cf8ae7e",
  "skills/sohrab/alaa-system-design/references/20-contract-first.md": "333bad6e50b59feef5a2ff408e9fe262e5f8318592a9371bd33726c9f6253f36",
  "skills/sohrab/alaa-system-design/references/30-data-and-consistency.md": "748e278b52ff478d463b80fc9b97b49b626887c02ebdb77ffbf71514c1478e53",
  "skills/sohrab/alaa-system-design/references/40-failure-and-load-inputs.md": "af3008ae45da16ee24c683e660970d97247353d37a5b64297b0c7d55d6c241e8",
  "skills/sohrab/alaa-system-design/references/50-alternatives-and-tradeoffs.md": "cf5dd218e10e0dfae5dc9ec44c2986e5766fe236abb5422c26cd4c27064cc585",
  "skills/sohrab/alaa-system-design/references/60-design-record.md": "fb2fa411b9ba971b089041547e65525445962d3e809df5df8ecd005939681d67",
  "skills/sohrab/alaa-system-design/references/70-review-and-readiness.md": "ed5bf4d298a64f875f844a2f627b1bb91d2a39ec7c01bce82a7e3510ee5edc5d",
  "skills/sohrab/alaa-system-design/SKILL.md": "78fab2f46fc23ad0455418c5e91282f0229df5c9bd54c9e8ff2402588b12f707"
}
```

Draft decisions: Complete every design decision before implementation. Orchestrated review and commit timing use the inherited canonical cadence, not a new early gate. A complete unreviewed draft may guide implementation until that boundary but cannot claim reviewed acceptance. Standalone preimplementation independent review is preserved. Missing cadence returns to the parent before dependent dispatch. Record states and generated prompt must preserve these distinctions; contract-first implementation must not create an early commit.

Compression: final clauses remove repeated scheduling claims and route them to SKILL.md Review and readiness, which points to the canonical orchestrator owner. No design-decision, independence, blocker or authority limit was removed. Legacy dual invocation forms in edited Markdown were converted to the repository single form.

## Execution scope and controls

Agent: alaa-implementer. Configured source and installed definitions omit model/effort; both were inspected and no pin mismatch was found. Requested gpt-6.1-sol/medium is recorded in the active plan second-final-repair allocation and parent dispatch. Observed serving model/effort: unknown. Authority: workspace-write runtime and parent ownership restrict product changes to alaa-system-design and evidence to DESIGN-FINAL-*; no MCP operations were used. Enforcement of unrelated MCP grants is unknown.

Full-read provenance: root AGENTS, skills/sohrab/AGENTS, owned SKILL, all seven references, asset template and agent YAML were read before edits. No nested AGENTS or scripts exist in the owned skill. Canonical cadence sections of both runtime orchestrators, routing-matrix admission, parent allocation, prompting-guide SKILL/topic map/ref60, and code-intelligence Markdown routing were read. Baseline SKILL already had a parent-owned invocation-form correction; it was preserved.

Decision: route orchestrated timing to the canonical owner and distinguish authored draft from reviewed acceptance. Rejected: another preimplementation independent review (violates inherited cadence); treating completed design authoring as reviewed (weakens independence); retaining contract-first commits under final cadence (forces premature commit). Protected: all seven design steps, interface/data/consistency decisions before code, known blocking findings resolved in the record, reviewer checks/verdict authority, standalone preimplementation review, contract-before-code ordering, and no added commit authority. Rollback is a scoped text revert; no application/data mutation occurs. Small wording growth supplies missing cadence interoperability, not new design obligations.

## Clause walkthrough (implementation evidence, not independent review)

| Case | Expected executing behavior and preserved decisions |
|---|---|
| Phase cadence | Complete decisions and hand a draft to implementation; independent design judgment waits for the declared phase review, as the orchestrator specifies. No task/subtask review or commit is introduced. |
| Final cadence | Complete decisions before code, use a draft with review pending, and judge the design with the final candidate. Intermediate status cannot claim reviewed acceptance; shape-before-code does not force a commit. |
| Standalone | Review before implementation dispatch remains mandatory; blocking findings are resolved in the record and reviewed status requires independent judgment. Existing contract-before-implementation commit ordering remains subject to authority. |
| Missing/inconsistent cadence | Return the conflict to the plan owner before dependent dispatch; do not silently choose standalone or reset the review boundary. |
| Undecided contract/data/failure choice | Decision readiness still fails; implementation cannot invent that decision, even if review timing is later. |
| Found blocking defect/change during implementation | Update/escalate the design record and run affected focused checks; independent judgment follows the inherited boundary, with no substitute design hidden in code. |

## Focused verification

Cwd: repository root. Resource policy: sequential lightweight native checks; no CPU-heavy gate or alternate runner needed.

- `python -B scripts/check_fleet_references.py --skill alaa-system-design` => exit 0, 1/69 skills, 9 Markdown files, 20 citations, no findings.
- `python -B skills/sohrab/alaa-repo-docs/scripts/check_markdown_links.py . --files skills/sohrab/alaa-system-design/SKILL.md skills/sohrab/alaa-system-design/references/20-contract-first.md skills/sohrab/alaa-system-design/references/60-design-record.md skills/sohrab/alaa-system-design/references/70-review-and-readiness.md` => exit 0, links validated in 4 Markdown files.
- `git diff --check -- skills/sohrab/alaa-system-design` => exit 0, no output.

Not run: broad pack checks, checker self-tests, installed activation, live worker behavior or independent acceptance. No check logic changed. Parent/same reviewer must clear I1; this lane makes no review verdict. No scope conflict or pending blocker found. Product writes frozen after these checks; only this evidence file was subsequently updated.

## Final changed product hashes

- `skills/sohrab/alaa-system-design/SKILL.md`: `be1132a6c643fef768cec64eebcf98264ba68555a4f52d2020418b1ccebc1ca5`
- `skills/sohrab/alaa-system-design/agents/openai.yaml`: `6af69ff96c3082e93f37ab37035867e20c65df4e919fc9195f25c1e55444326e`
- `skills/sohrab/alaa-system-design/references/20-contract-first.md`: `228e7d8326dcc58b7f33752df7969cdb642ad0e5f9c005d8574474821796086f`
- `skills/sohrab/alaa-system-design/references/60-design-record.md`: `dffe96c782e09f6bbbaa99aef7f851b3b13c05507bf0e317fc1c06c36b6ac75b`
- `skills/sohrab/alaa-system-design/references/70-review-and-readiness.md`: `452530c5c45faa65de8cd2839d9fdb94a4df516071ca220ace249672b979b67e`
