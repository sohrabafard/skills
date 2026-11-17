# Review-loop analysis and read-at-need pointers, 2026-11-17

Scope: one Claude Code session in the client repository (title "client: Admin users command center API wiring"),
analysed read-only from its transcripts, and the pack change that followed. Times are UTC. The scripts under
`tools/` and `outputs/20261115-code-intelligence-usage/reference_reach.py` reproduce the numbers; each takes
the session directory or a day count as its argument.

## What the session did

- Active span 2026-11-16 20:41 to 2026-11-17 01:54: 312 minutes. Pack live at its start: orchestrator 6.0.4.
- 14 direct dispatches and six Workflow runs with 311 agents. No dispatch and no `agent()` call carried a
  model: every agent ran on the session's model.
- The lead loaded two skill bodies, one section of `task-tracking.md` and the runtime's workflow reference.
  It opened no orchestrator reference and did not load the testing-strategy skill.
- Review and repair ran from 22:40 to 01:53: 193 minutes (62% of the active span), 20.7M of 22.6M fresh input
  tokens and 1.28M of 1.74M output tokens. The 201 refuters of the first workflow used 10.4M fresh input tokens.

## Rounds

| Round | Start | Started by | Input, by the reviewer's own label | Minutes |
|---|---|---|---|---|
| A review | 22:40 | the lead's plan | 19 findings: 1 major, 3 medium, 5 minor, 8 low, 2 nit; three verdicts of pass with findings | 4 |
| A repair | 22:44 | the lead: fix all, tests first | the same 19 findings and 2 items from the documentation lane | 26 |
| Run 1 | 23:11 | the owner's message to use an ultracode workflow | the whole diff again: 67 findings, 19 confirmed (8 major, 11 minor), 14 distinct; 1 of 4461 tests failed | 19 |
| Run 2 | 23:32 | the result of run 1 | 13 items: 5 major defects, 1 gate failure, the rest minor | 60 |
| Run 3 | 00:32 | the lead, on run 2's fresh review | 1 minor, 2 nits, 2 test files that timed out at load 26 | 28 |
| Run 4 | 01:03 | the advisor call before the final report | a mode missing from the adapter registry; 3 provenance defects | 19 |
| Run 5 | 01:23 | the result of run 4 | 3 unlabelled provenance items, 1 minor, 2 nits | 17 |
| Run 6 | 01:40 | an item run 5 left half done | 1 item a verifier labelled major, 1 nit | 12 |

- Runs 3 to 6 took 77 minutes and carried no blocker.
- Two acceptance gaps were reported by implementation lanes under "Deviations" at 22:16 and 22:32. The lead
  accepted both lanes. The first became the top major finding of run 1, the second the subject of run 4.
- The review dispatches of round A carried no owner requirement and capped the report at 350 to 500 words.
- Run 1 yield by round: 35 found and 14 confirmed, 14 and 3, 18 and 2.
- The full gate list ran six times, about 4 minutes each. Serial fix phases took 101 minutes.

## Lanes

Phases P1, P2 and P3 edited disjoint files (counted from Edit and Write calls) and the plan allowed P2 and P3
after P0 in parallel. They ran one after another: the critical path took 89 minutes where 65 was possible. The
lead's stated reason: it read a dependency restore in a worktree as an installation that needs permission.

## Why the rules did not act

Every rule the session needed existed in a reference at version 6.0.4: finding triage by consequence, the
rule for a further review round, the review template with acceptance criteria, shared checkout for disjoint
lanes. The body pointed at them and the lead did not follow the pointers. After 23:02 the runtime's workflow
reference, which says that token cost is not a constraint, governed the loop.

Baseline of 2026-11-17, seven days, 13 lead sessions outside this repository that invoked the Claude
orchestrator:

| Reference | Sessions that opened it |
|---|---|
| `task-tracking.md` | 12 |
| `routing-matrix.md` | 9 |
| `verification-and-gates.md` | 7 |
| a delegation template | 5 |
| `workspace-and-integration.md` | 4 |
| `review-mode.md` | 0 |

`verification-and-gates.md` was opened before the first review dispatch in 4 of 10 sessions, and before a fix
that followed a review in 3 of 7. The pointer that works is called from the always-loaded project file, fires
at a concrete command, carries a stop rule and leads to a fact the lead cannot guess. The pointer that never
works sits two hops from the body. The sample is small and the pack text changed during that week: pointer
shape is a hypothesis, not a proven cause.

## Owner decisions of 2026-11-17 and the change

1. Workflows: the owner bounds or avoids ultracode in an orchestrated session, and the Claude orchestrator body
   says that an `agent()` call in a Workflow script is a dispatch under the skill.
2. No reference rule moves into a body. Pointers must make the lead read at need. The *Direct references*
   table of both orchestrator bodies now names one section per action, one hop, with a stop rule.
3. `alaa-workflow references/workspace-and-integration.md` says that restoring dependencies from the committed
   lockfile in a lane worktree is not an installation. The client repository gets its own bootstrap script.
4. The client repository states its two local duties that lanes missed.

## Limits

- Text raises the rate at which a reference is opened; it does not prove that it was. Rerun
  `reference_reach.py` after a week of sessions on 8.2.0 before deciding on a deterministic check.
- The avoidable share of the 193 minutes is an estimate (60 to 90 minutes); time per item inside one fix lane
  is not observable.
- Not determined: the text of the 48 rejected findings of run 1, the advisor's message, and whether a commit
  hook of the client repository forbids a shared checkout.

## Review of the change

One instruction review ran on the branch (verdict: changes requested; 4 major, 6 minor, 1 nit). All eleven were
applied; no confirmation pass ran. What changed because of it: the deviation sentence names what a lane
actually reports ("changed or not met, under any heading"), the workflow line tells the lead to read the
sections before it writes the script, the triage row also fires when the lead fixes inline or fixes nothing,
the router reaches `## Before any dispatch`, `## Evidence` and `## Check collection` again, and the lockfile
sentence is bounded to a locked install. `alaa-prompting-guide references/41-claude-code-runtime-features.md`
now records where the `effort` option of a workflow `agent()` call is documented.

Left as it is, reported to the owner: a finding triaged "fix it" does not hold the acceptance of the lane that
reported it; `alaa-workflow references/review-mode.md` sets the fix deadline at the review boundary.
