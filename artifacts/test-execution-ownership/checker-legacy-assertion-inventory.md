# Legacy assertion migration inventory

Compared both runtime checker constant tables and changed helper assertions against HEAD `183f5c5a19daaa0c31c5aa41ce8ce2868181aa34`. Runtime behavioral tables were mirrored before this change; model/runtime metadata differences are unchanged. This inventory records every removed/moved policy assertion; scenario labels, diagnostics and dictionary keys are not separate policy.

Final combined corrections: restore the legacy broad-zero-selector contradiction; protect original body continuation/SKIPPED/contamination and final-exhaustive/Markdown-input clauses; retain runtime review integrity, analyst-first/environment authority and conflicting-writer reconciliation. The parent-requested compatibility batch also restores Bash help rejection and documents exact maintainer commands/status meanings. No other losses remain in this finite source inventory.

| Original table/helper | Removed or relocated assertion | Current protection |
|---|---|---|
| GATE_REQUIREMENTS | An implementer's broad PASS cannot discharge it, even with unchanged inputs | shared doctrine aggregate inputs/environment/flags/required-observer equivalence + runtime GATE independent observer/author PASS boundary |
| GATE_REQUIREMENTS | Independent acceptance requires an observer independent of the implementation with authority for that gate | shared doctrine aggregate inputs/environment/flags/required-observer equivalence + runtime GATE independent observer/author PASS boundary |
| GATE_REQUIREMENTS | cite valid unchanged independent evidence instead of repeating it | shared doctrine aggregate inputs/environment/flags/required-observer equivalence + runtime GATE independent observer/author PASS boundary |
| GATE_REQUIREMENTS | excludes exhaustive results from reuse | shared doctrine final exhaustive always fresh |
| GATE_REQUIREMENTS | reuse requires the correct observer as well as unchanged tree | shared doctrine aggregate inputs/environment/flags/required-observer equivalence + runtime GATE independent observer/author PASS boundary |
| GATE_REQUIREMENTS | tool/dependency versions, environment/service state, and flags/seed/cwd | shared doctrine four result-validity conditions |
| CADENCE_REQUIREMENTS | Markdown and templates can be checker inputs: documentation-only change proves no equivalence | shared doctrine Markdown/templates input + documentation-only proves no equivalence |
| CADENCE_REQUIREMENTS | covered inputs, environment, flags and required observer match demonstrably | shared REQUIREMENTS[doctrine] |
| CADENCE_REQUIREMENTS | never weaken tests or review to obtain a pass | shared execution assertion integrity + both runtime CADENCE Never weaken review |
| COLLECTION_REQUIREMENTS | A fail-fast aggregate proves only executed coverage: dispatch its supported keep-going mode or exact uncovered child commands; preserve failure exits | shared execution fail-fast coverage, keep-going/uncovered commands and preserved exits |
| COLLECTION_REQUIREMENTS | A failure does not cancel independent remaining checks | shared execution One failure never cancels independent remaining checks |
| COLLECTION_REQUIREMENTS | After batch repair, independent verification reruns the whole recorded check list, including checks it discharged by citation, before Stage D | shared execution complete collection/whole-list retest + runtime COLLECTION review barrier and independent whole-list retest |
| COLLECTION_REQUIREMENTS | Classify first, use the failure analyst for ambiguous ownership and preserve environment/security authority limits | shared execution cause classification + both runtime COLLECTION_SEAMS routing analyst-first/environment authority |
| COLLECTION_REQUIREMENTS | Combine the full collection's failures verbatim into one serialized fix lane with explicit scope/ownership; retire conflicting writers | both runtime COLLECTION_REQUIREMENTS serialized assignment + conflicting-writer reconciliation; shared workspace liveness/ownership |
| COLLECTION_REQUIREMENTS | Continue safe independent checks; stop unsafe or contaminated execution and name affected unrun checks, without calling collection complete | shared execution stop unsafe/contaminated cases; unresolved collection incomplete; continue safe checks |
| COLLECTION_REQUIREMENTS | Invalidate affected evidence | shared REQUIREMENTS[execution] |
| COLLECTION_REQUIREMENTS | Keep existing retry/stop budgets | shared execution no retry reset + runtime COLLECTION existing retry/stop budgets |
| COLLECTION_REQUIREMENTS | Only a failure blocking all or most remaining checks permits a minimal early repair | shared execution all/most-only minimal early repair, obstruction-only scope, resume including blocked checks |
| COLLECTION_REQUIREMENTS | Record each command's exit/result and each unrun check's blocker | shared REQUIREMENTS[execution] |
| COLLECTION_REQUIREMENTS | Unresolved required checks block Review and acceptance | shared execution complete collection/whole-list retest + runtime COLLECTION review barrier and independent whole-list retest |
| COLLECTION_REQUIREMENTS | after Stage C's collection, batch repair and required retests pass | shared execution complete collection/whole-list retest + runtime COLLECTION review barrier and independent whole-list retest |
| COLLECTION_REQUIREMENTS | record blocked checks and cause, repair only that obstruction | shared execution all/most-only minimal early repair, obstruction-only scope, resume including blocked checks |
| COLLECTION_REQUIREMENTS | run every required runnable phase check centrally once through `alaa-verifier` | shared execution every runnable check once + runtime COLLECTION phase-end alaa-verifier barrier |
| COLLECTION_REQUIREMENTS | then run or resume all required checks, including previously blocked checks, before any Review | shared execution complete collection/whole-list retest + runtime COLLECTION review barrier and independent whole-list retest |
| COLLECTION_SEAMS | Identify its behavior owner; repair scheduling follows `verification-and-gates.md` Gate economics | canonical classification owner/repair record + runtime taxonomy pointer and routing infrastructure scope |
| COLLECTION_SEAMS | Identify required infrastructure scope in the combined repair assignment under `verification-and-gates.md` Gate economics | canonical classification owner/repair record + runtime taxonomy pointer and routing infrastructure scope |
| COLLECTION_SEAMS | collect all runnable commands and failures; no fixes or Review during collection | shared execution complete collection before repair + runtime verifier canonical barrier seam |
| COLLECTION_SEAMS | workflow records these barriers without redefining their policy | runtime planning seam: Workflow records barriers without redefining them |
| COLLECTION_CONTRADICTIONS | A fail-fast aggregate proves all required checks ran | shared CONTRADICTIONS |
| COLLECTION_CONTRADICTIONS | Any failed check permits an early repair | shared CONTRADICTIONS |
| COLLECTION_CONTRADICTIONS | Collection resets the retry budget | shared CONTRADICTIONS |
| COLLECTION_CONTRADICTIONS | Review immediately after the minimal early repair | shared CONTRADICTIONS |
| COLLECTION_CONTRADICTIONS | Skip previously blocked checks after early repair | shared CONTRADICTIONS |
| COLLECTION_CONTRADICTIONS | Start one repair lane for each failed test | shared CONTRADICTIONS |
| COLLECTION_CONTRADICTIONS | Stop collection after the first failed command | shared CONTRADICTIONS |
| RUN_ECONOMY_REQUIREMENTS | ## Existing tests on a touched topic | shared REQUIREMENTS[economy] |
| RUN_ECONOMY_REQUIREMENTS | A case failing never stops an independent case from running | shared REQUIREMENTS[doctrine] |
| RUN_ECONOMY_REQUIREMENTS | A command without a test selector, such as lint, type-check, build or render, skips this check | shared execution non-test lint/type/build/render needs no case-selection check |
| RUN_ECONOMY_REQUIREMENTS | A failure alone never justifies deleting a test | shared REQUIREMENTS[economy] |
| RUN_ECONOMY_REQUIREMENTS | A list or collect selection check executes no case by design: it is `PASS` when it lists exactly the expected cases | shared REQUIREMENTS[classification] |
| RUN_ECONOMY_REQUIREMENTS | A scoped lint, type-check or build command whose scope matches no file is `TEST-INFRA-FAILURE` | shared REQUIREMENTS[classification] |
| RUN_ECONOMY_REQUIREMENTS | After batch repair, independent verification reruns the whole recorded check list, including checks it discharged by citation, before Stage D | shared execution complete collection/whole-list retest + runtime COLLECTION review barrier and independent whole-list retest |
| RUN_ECONOMY_REQUIREMENTS | Then assign it by continuing the existing implementer whose still-valid assignment and context cover most failures | both runtime RUN_ECONOMY gate continuation validity/host tool/profile or pair boundary |
| RUN_ECONOMY_REQUIREMENTS | any result in a collected check list after its batch repair | shared REQUIREMENTS[doctrine] |
| RUN_ECONOMY_REQUIREMENTS | dispatch fresh only when no continuation is available, that context is invalid, or Implementation routing selects another profile or task pair | both runtime RUN_ECONOMY gate continuation validity/host tool/profile or pair boundary |
| RUN_ECONOMY_REQUIREMENTS | earns no further full run | shared REQUIREMENTS[classification] |
| RUN_ECONOMY_REQUIREMENTS | including whole-suite discovery and each covered child of an aggregate | shared REQUIREMENTS[classification] |
| RUN_ECONOMY_REQUIREMENTS | independently rerun the whole recorded check list, including outstanding required checks | shared execution whole recorded-list retest + runtime COLLECTION independent whole-list authority |
| RUN_ECONOMY_REQUIREMENTS | inside a container run, an incomplete copy or mount is instead `ENVIRONMENT-BLOCKED` | shared REQUIREMENTS[classification] |
| RUN_ECONOMY_REQUIREMENTS | makes every later result over that state `CONTAMINATED` | shared REQUIREMENTS[doctrine] |
| RUN_ECONOMY_REQUIREMENTS | otherwise compare the selected cases in the first run's report with the expected ones | shared execution compare first selected cases against expected |
| RUN_ECONOMY_REQUIREMENTS | reported `SKIPPED` naming that precondition | shared REQUIREMENTS[doctrine] |
| RUN_ECONOMY_REQUIREMENTS | selected cases but executed none takes the class its skip reasons name | shared REQUIREMENTS[classification] |
| RUN_ECONOMY_REQUIREMENTS | through a continuation tool the current host documents for that agent | both runtime RUN_ECONOMY gate continuation validity/host tool/profile or pair boundary |
| RUN_ECONOMY_REQUIREMENTS | when the runner has a list or collect mode, dispatch it to the verifier as its own command before the first run | shared execution separate list/collect-only selection check before execution |
| RUN_ECONOMY_REQUIREMENTS | whose selection is empty or differs from the expected cases recorded for it is `TEST-INFRA-FAILURE`, never `PASS` | shared REQUIREMENTS[classification] |
| RUN_ECONOMY_CONTRADICTIONS | A command whose selector executed zero cases | shared CONTRADICTIONS |
| RUN_ECONOMY_CONTRADICTIONS | independent verification reruns failed and invalidated checks | shared CONTRADICTIONS |
| RUN_ECONOMY_CONTRADICTIONS | rerun failed topic selectors and checks whose inputs changed | shared CONTRADICTIONS |
| economy_failures | Phase transitions and new agents alone earn no rerun | shared doctrine A phase transition, new agent or compaction alone invalidates nothing |
| economy_failures | only one CPU-heavy | shared resources one CPU-heavy command per host |
| cadence_failures | hard user constraint on browser choice / --browser chromium | shared resources Preserve explicit --browser chromium; both bodies route 110 |

The removed collection scenario labels reuse the same clauses above: independent A/B/C collection, all/most early repair and resumed collection, blocked-independent checks, fail-fast coverage, final-only collection, and retest before Review without a new retry budget. Each retained clause has a fresh-map removal fixture; contradictions are appended with positives intact. Added pointer-prefix/suffix, timing-dispersion and runner help-rejection regressions address this task's acceptance criteria. Structural evidence proves no live-agent scheduling behavior.
