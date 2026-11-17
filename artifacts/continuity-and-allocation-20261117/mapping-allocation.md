# Mapping: model and effort allocation in both orchestrator packs

Read-only mapping report, 2026-11-17. Dated evidence: verify a line number before relying on it.

I mapped all eight questions from the files. Nothing was edited or run, and I did not create the plan file the plan-mode reminder offered. Paths are relative to `skills/sohrab/` unless they start with `outputs/` or `artifacts/`, which are relative to ``. "RM" means `references/routing-matrix.md` and "MEP" means `references/model-effort-policy.md`.

## 1. Model and effort sections of `routing-matrix.md`

**cc** (`alaa-cc-orchestrator/references/routing-matrix.md`):

```
23	## Planning profile selection
24	
25	Before planning, separate missing facts from coupled design judgment, and retrieve or clarify the missing facts.
26	
27	1. Use `alaa-planner` when scope, contracts and constraints are clear. Use `alaa-planner-high` when forming the plan requires resolving interacting uncertainties.
28	2. Select the planning model AND effort for the planning task through All-role task allocation below.
29	3. The lead may plan inline only when its effective controls match that recorded pair. Otherwise dispatch a compatible registered planner.
30	4. A planner draft is advisory. The lead ratifies it and persists the durable plan.
31	5. Before worker allocation, finalize the lane outcomes, scopes, exclusions, dependencies, decisions, and failure and invariant reasoning.
32	
33	## Batch allocation
34	
35	After workflow tasks, dependencies and consolidation decisions are finalized, allocate the ready plan once through All-role task allocation below.
36	
37	- Before dispatch, record each role with its explicit model AND effort: evidence, planning, implementation, verification, review, specialist and documentation lanes.
38	- Compare the ready tasks so that no task inherits the complexity of the whole goal.
39	- Reopen allocation only for remaining work, at a material scope change or a fix follow-up. Reuse unchanged allocations and evidence.
40	
41	## All-role task allocation
42	
43	This orchestrator decides the task complexity, priority, model and effort for EVERY role. Before allocation, read `alaa-prompting-guide references/90-model-selection.md` and its `references/50-effort-and-thinking.md`; they inform the decision and assign no default pair to a role.
44	
45	Role identities are compatibility identities: a role name, including a legacy ID named for a model or effort, selects neither control. Every pair preserves the role's tools, skills, verdicts and independent gates.
46	
47	1. **Ground the task.** Establish each task's scope, acceptance, settled and open decisions, and remaining reasoning need. Retrieve missing facts. Repair context, specification or tool failures before you attribute a shortfall to model capacity.
48	2. **Set the priority.** Use the balanced default priority; priority is not an effort value. Deviate only on an explicit user priority or model choice, or a documented task-based reason. Role title, sensitivity, duration, whole-goal labels and a second independent lens alone never select a frontier or stronger model. Independence comes from context and authority, not model diversity.
49	3. **Select the cheapest suitable pair.**
50	   1. Evaluate the cheapest eligible supported available model AND effort pair for EVERY role, the rule-writer included.
51	   2. A task has bounded suitability only when it has all of these: an explicit outcome, a finite named scope, grounded local contracts/known invariants, a known pattern or causal path, settled cross-boundary decisions, bounded local discretion and a discriminating check.
52	   3. Non-bug semantic work needs no reproduced failure. The mechanical branch keeps its own predicates below.
53	   4. Select the least costly suitable available pair. Depart from it only on an explicit user choice or recorded task evidence. Apply no quotas.
54	   5. Justify model and effort separately, each from the remaining reasoning need, the priority, current official guidance and applicable prior evidence.
55	   6. When you reject a cheaper pair, record the actual failed fit predicate or stronger task-specific evidence. Titles, volume, priority labels and whole-goal complexity are not failed predicates.
56	   7. Select directly. Use no mandatory trial ladder, synthetic experiment or replay.
57	4. **Admit an exceptional model only on evidence.** On ANY role, an exceptional model needs one of these:
58	   - an exact official recommendation for the task and priority that the canonical owner supports, recorded with the remaining reasoning need and the rejected cheaper or decomposed alternatives;
59	   - applicable documented inadequacy of the high-effort workhorse, established after context, specification and tool correction and after decomposition was considered;
60	   - an explicit user selection.
61	
62	   A repairable defect or an imagined insufficiency is not model inadequacy. A model mention alone is not a selection instruction.
63	5. **Record the allocation** once, in the workflow plan, or in the dispatch's `<task_controls>` when no durable plan is admitted: the role, the scope and workload class, a priority that departs from the default with its reason, the selected model AND effort, and the admission with its evidence. A bounded standalone delegation needs no full pipeline and no workflow artifact solely for model selection.
64	6. **Realize the pair.** Before EVERY dispatch, follow `model-effort-policy.md`. Unknown serving identity is a reporting limit, not evidence of a control mismatch and not a reason for paid calibration.
```

```
70	## Implementation routing
71	
72	Choose directly from the completed lane record; no mandatory sequence of attempts applies. Copy the admission predicates you verified for the selected route into the dispatch; the lane rechecks them before editing. These routes classify workload fit only. Apply All-role task allocation separately.
73	
74	Select the exact mechanical branch of `alaa-implementer-haiku` only when ALL of these are recorded before dispatch:
75	
76	- the exact transformation and its exclusions;
77	- a finite, explicitly enumerated scope of existing files;
78	- the expected result;
79	- a settled design with no semantic discretion;
80	- a known pattern;
81	- cheap discriminating checks that detect wrong, incomplete or out-of-scope results.
82	
83	File count alone neither qualifies nor disqualifies a task. Ambiguous matches, undefined scope or design changes fail admission.
84	
85	Select the bounded semantic branch of `alaa-implementer-haiku` only when the plan records explicit expected behavior, a settled local causal path or pattern, named scope, known invariants, bounded decisions and discriminating behavior/regression checks. Use `alaa-implementer-haiku-high` for longer or stricter work that satisfies the same predicates. Interacting design, or unresolved decisions about cross-boundary contracts, trust, shared state or consistency, select a workhorse route below.
86	
87	These routes are uncalibrated workload admissions. Priority or a model preference never waives fit or independent gates. If fit ceases, stop dependent work, preserve valid edits and return the remaining scope for reclassification. Require no lightweight trial and no replay of completed work. No route expands command authority.
88	
89	- `alaa-implementer`: everyday grounded coding, features, local refactoring or debugging with known patterns, explicit contracts and acceptance, and bounded local decisions. The architecture need not prescribe every edit.
90	- `alaa-implementer-sonnet-high`: harder or longer grounded work with bounded decisions and local failure reasoning.
91	- `alaa-implementer-opus`: materially coupled unresolved system decisions beyond the bounded routes.
92	- `alaa-implementer-opus-high`: interacting unresolved design decisions and demanding system reasoning.
93	
94	The legacy exceptional ID `alaa-implementer-fable` remains an implementation authority identity. Apply the exceptional model admission above only when the selected task pair is exceptional, and record its evidence before dispatch. Return missing facts, unavailable tools and unresolved product intent to their owners. An unresolved decision alone never establishes model inadequacy.
95	
96	### Stack-bound roles
...
101	- The lane is not admitted to the mechanical or the bounded semantic branch above.
...
110	- The stack-bound role replaces `alaa-implementer`, `alaa-implementer-sonnet-high`, `alaa-implementer-opus`, `alaa-implementer-opus-high` and `alaa-implementer-fable`. An admitted exceptional pair runs on the stack-bound role.
111	- Record the lane's workload class in the allocation record: everyday, harder or longer, materially coupled, or interacting design. For a stack-bound lane the class informs the task pair and selects no role identity.
112	- Split a lane that owns files of two families when the parts are independent. Otherwise, and for a stack with no bound role, dispatch the generic role for its workload class and name each stack's skills in the dispatch as calls.
113	- When the selected stack-bound role is not available in this session, do not block the lane for that reason. Record the generic role for the workload class as the registered profile, with the unavailable stack-bound role as its reason. Dispatch it and name the stack's skills in the dispatch as calls. This fallback replaces only the role identity; the pair rules still apply.
114	
115	### Reassignment
116	
117	Reassess remaining work only at the initial assignment, a material scope change or a fix follow-up. Before you replace a writer, apply the stopped-writer recovery in `alaa-workflow references/workspace-and-integration.md` and retire its assignment. Hand off the remaining scope, acceptance criteria and evidence. Never overlap writers or replay completed work.
118	
119	## Correctness review depth
120	
121	Select the deep route when review involves complex interactions among subsystems, a broad failure impact, or documented insufficiency of the standard review. Both routes use `alaa-reviewer`; select its model AND effort through All-role task allocation. Record the trigger and select one profile per scope. When you replace an insufficient standard review, retire that assignment and pass its evidence to the deep route. Never run the two reviews concurrently.
```

(I left out lines 97–100 and the table at 103–108. They are the stack-family rule and the file-to-role table; see Q8.)

**codex** (`alaa-codex-orchestrator/references/routing-matrix.md`). I ran `diff` on the two files. Only these hunks differ; the text is **identical otherwise**.

```
48	2. **Apply eligibility, then set the priority.** Apply canonical eligibility: exclude gpt-6-sol ordinarily even if available. Current-family selection never upgrades a suitable Luna pair to Sol. When current Sol is missing, require an exact eligible realization or block the affected lane; never fall back to old Sol. Record an explicit user legacy exception separately; ordinary eligibility stays disabled. Use the balanced default priority; priority is not an effort value. [rest identical to cc 48]
52	   3. Non-bug semantic work needs no reproduced failure. The mechanical and bug branches keep their own predicates below.
66	### Codex Terra eligibility
68	Consider `gpt-6.1-terra` only for supplied-material writing, defined-outcome computer use, or scoped code fixes covered by the prompting guide's Terra workload guidance. Require every bounded-suitability predicate above and an exact verified host model/effort pair. Compare eligible pairs through the same allocation procedure. Apply existing tool and delegation authority at every effort, including `ultra`.
78	Select the mechanical branch of `alaa-implementer-luna` only when ALL of these are recorded before dispatch:
89	Select `alaa-implementer-low` for bounded semantic work only when every All-role bounded-suitability predicate and cheap discriminating checks are recorded. Non-bug local decisions qualify. Allocate its pair separately; a suitable Luna pair is a candidate. Unresolved cross-boundary design, consistency or trust fails admission.
91	Select `alaa-implementer-luna-low`, the bug branch of `alaa-implementer-luna`, or `alaa-implementer-luna-high` from the exact official bug row and the selected priority. Select one only when the plan records a reproduced failure, a traced local causal path, explicit expected behavior, bounded scope and semantic discretion, and a discriminating regression oracle. Unresolved design of cross-boundary contracts, trust, shared state or consistency fails admission.
95	- `alaa-implementer`: normal engineering with grounded scope and acceptance criteria.
96	- `alaa-implementer-high`: substantial interacting engineering reasoning.
97	- `alaa-implementer-xhigh`: sustained coupled technical reasoning admitted by the batch source mapping and lane requirements.
99	The legacy exceptional IDs `alaa-implementer-astra`, `alaa-implementer-astra-medium` and `alaa-implementer-astra-xhigh` remain implementation authority identities. [rest identical to cc 94]
106	- The lane is not admitted to the mechanical branch or either bounded route above.
115	- The stack-bound role replaces `alaa-implementer`, `alaa-implementer-high`, `alaa-implementer-xhigh`, `alaa-implementer-astra`, `alaa-implementer-astra-medium` and `alaa-implementer-astra-xhigh`. An admitted exceptional pair runs on the stack-bound role.
116	- Record the lane's workload class in the allocation record: normal, substantial interacting, or sustained coupled. For a stack-bound lane the class informs the task pair and selects no role identity.
126	Select the deep route when review involves complex interactions among subsystems, a broad failure impact, or documented insufficiency of the standard review. Use `alaa-reviewer` or the compatible `alaa-reviewer-deep` identity for that scope; neither selects a model or effort. Apply All-role task allocation to the review task. Record the trigger and select one profile per scope. [rest identical]
```

- Codex line numbers after 65 are shifted by +4 or +5 relative to cc.
- I found no definition of "the batch source mapping" (codex 97) anywhere in the current pack.

## 2. `model-effort-policy.md`, both packs

**cc** (`alaa-cc-orchestrator/references/model-effort-policy.md`, 40 lines):

```
1	# Model and Effort Control Route
2	
3	`routing-matrix.md` *All-role task allocation* selects the model and effort for EVERY role. This file realizes that pair. The capability registry is `alaa-prompting-guide assets/claude-model-policy.json`. Managed roles carry no executable model or effort pins. Check ordinary eligibility, effort support and host availability separately.
4	
5	## Normalize omitted controls
6	
7	This file alone owns orchestration defaults for this runtime. Preserve ordinary allocation when both controls are selected. Before every dispatch:
8	
9	1. Retain every explicit field and fill only missing model or effort from the default below. Fill each field independently.
10	2. Validate the resulting pair against the capability registry and actual host before invocation. Unsupported, inactive or unrealizable pairs still block the affected lane.
11	3. Record the normalized model AND effort in the plan or compact dispatch. Inherited controls are not normalization.
12	
13	Omission alone and a successfully resolved default are never blocked/degraded.
14	
15	Claude Code default: `model = claude-opus-5-5`, `effort = medium`.
16	
17	Pass the family alias of the selected model on the Agent invocation; for this default, pass `opus`. Supply both parameters on every dispatch, because an omitted parameter falls through to the session's value, not to this default. Verify that the alias resolves to the selected ID on the target provider, or block the affected lane. `alaa-prompting-guide references/41-claude-code-runtime-features.md` owns the alias and precedence facts.
18	
19	Verified 2026-10-18 against the official sources below and the active invocation schema. Record an unresolved future alias mapping as `NEEDS_CONFIRMATION`, never a guessed model ID. Defaults change no role authority, tools, skills, verdicts or independent gates; managed wrappers remain neutral.
20	
21	## Before every dispatch
22	
23	1. Inspect the loaded role definition, the active version, the invocation controls and the effective overrides: environment, hook, force, provider and parent overrides can take precedence over the definition and the invocation.
24	2. Explicitly supply BOTH model AND effort, as normalized, on the verified Agent invocation surface.
25	3. Check that the effective configured pair matches the selected pair. Prose, requested controls or source validation alone cannot prove it.
26	4. If a fork, an older version or a restricted surface cannot realize both values, use only an exact verified available compatibility realization that preserves the role contract, or block the affected lane with evidence. A separate CLI session changes context and permissions, so it is not an automatic substitute.
27	
28	Never silently change the pair, install, mutate shared configuration or claim that source edits activated a session. Source checks prove neither installed activation, account access nor serving identity.
29	
30	Keep permissions separate from model choice. When enforcement is unknown, stay within the narrower role authority.
31	
32	Report the configured and requested model and effort separately from the observed identity. An unknown observation stays unknown.
33	
34	## Native Advisor consultation
35	
36	After you select the executor's task pair, consider native Advisor for a named unresolved decision that consultation can help. Resolve missing facts and tool or context failures first. Read **Native Advisor** in `alaa-prompting-guide references/41-claude-code-runtime-features.md` for supported pairs, session checks and data sharing. Use Advisor only on a verified, authorized surface, and record the reason and the effective advisor control. Consultation stays optional and changes no executor pair, role authority or independent gate.
37	
38	## Default mapping sources
39	
40	[Claude model configuration](https://code.claude.com/docs/en/model-config) and [Claude subagents](https://code.claude.com/docs/en/sub-agents).
```

**codex** (`alaa-codex-orchestrator/references/model-effort-policy.md`, 36 lines). Lines 1–2, 4–14 and 19–22 are identical to cc, except that line 3 names `assets/codex-model-policy.json`. The differing lines:

```
15	Codex default: user alias `sol-6.1-medium` resolves to `model = gpt-6.1-sol`, `effort = medium`.
16	
17	Pass the executable model ID, never the composite alias. `alaa-prompting-guide references/11-codex-runtime-features.md` owns the pin precedence facts.
...
23	1. Inspect the loaded custom definition and the global and parent controls: a custom `model` or `model_reasoning_effort` pin and parent overrides take precedence over caller controls.
24	2. Explicitly supply BOTH model AND effort, as normalized: pass `model` and `reasoning_effort` to the supported spawn surface. Verify that the host permits those arguments and the requested fork or context mode.
25	3. Check that the effective configured pair matches the selected pair. Prose, requested controls or source validation alone cannot prove it.
26	4. If a fork or a fixed named-role definition cannot realize both values, use only an exact verified available compatibility realization that preserves the role contract, or block the affected lane with evidence. Treat the loaded controls of a fixed definition as fixed until a verified reload.
27	
28-32	[identical to cc 28-32]
33	
34	## Default mapping sources
35	
36	[Codex models](https://learn.chatgpt.com/docs/models) and [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents).
```

Codex has no Native Advisor section.

## 3. Checker-bound literals in `scripts/check_agent_contracts.py`

**Matching modes:**
- **N (normalized):** `contract_present` (cc/codex L43–46) collapses whitespace, casefolds, and also accepts the alternative listed in `EQUIVALENT_REQUIREMENTS` (L25–32).
- **R (raw):** a case-sensitive `in` substring test.

Line numbers are cc / codex.

| Function or tuple (line) | Exact literal | Req/Forb | Mode | Target file → matching line(s) |
|---|---|---|---|---|
| `EQUIVALENT_REQUIREMENTS` L30–31 / same | "Explicitly supply BOTH model AND effort" ≡ "Supply an explicit model and an explicit reasoning effort for each dispatch" | alternative | N | MEP:24 |
| `BOUNDED_REQUIREMENTS` L33–40 / same; checked at cc L317–319 / codex L312–314 | "Evaluate the cheapest eligible supported available model AND effort pair for EVERY role" | Req | N | RM:50 |
| same | "explicit outcome", "finite named scope", "grounded local contracts/known invariants", "known pattern or causal path", "settled cross-boundary decisions", "bounded local discretion", "discriminating check" | Req | N | RM:51 (the last also matches cc 81; codex 85, 89) |
| same | "Non-bug semantic work needs no reproduced failure" | Req | N | RM:52 |
| same | "Justify model and effort separately" | Req | N | RM:54 |
| same | "actual failed fit predicate or stronger task-specific evidence" | Req | N | RM:55 |
| same | "no quotas" | Req | N | RM:53 |
| same | "no mandatory trial ladder" | Req | N | RM:56 |
| same | "replay" | Req | N | bare token: cc 56/87/117; codex 56/93/122 |
| `task_allocation_failures` cc L311–316 / codex L306–311 | "## All-role task allocation", "EVERY role", "balanced default", "priority is not an effort value", "Role title, sensitivity, duration", "second independent lens", "not model diversity", "model AND effort", "compatibility identities" | Req | R | RM:41, 43/50, 48 (×5), many (×1), 45 |
| codex only, L315–316 | "exclude gpt-6-sol ordinarily even if available" | Req | R | codex RM:48 |
| `task_allocation_failures` cc L320–324 / codex L317–321 | "Before every dispatch", "Explicitly supply BOTH model AND effort", "effective configured pair matches", "or block", "affected lane", "Source checks prove neither installed activation", "parent overrides" | Req | N | MEP:7/21, 24, 25, 26 (cc also 17), 10/26 (cc also 17), 28, 23 |
| `task_allocation_failures` cc L325–329 / codex L322–326 | "owns only role triggers", "Agent metadata carries executable pins", "both standard and deep review inherit", "non-implementation roles remain fixed", "stronger model solely because it is a second lens" | **Forb** | R | RM and MEP |
| `DEFAULT_REQUIREMENTS` cc L279–290 / codex L274–285, via `default_control_failures` | "This file alone owns orchestration defaults for this runtime"; "Preserve ordinary allocation when both controls are selected"; "retain every explicit field and fill only missing model or effort"; "independently"; "Validate the resulting pair against the capability registry and actual host before invocation"; "unsupported, inactive or unrealizable pairs still block the affected lane"; "Omission alone and a successfully resolved default are never blocked/degraded"; "Record the normalized model AND effort in the plan or compact dispatch"; "inherited controls are not normalization"; "NEEDS_CONFIRMATION"; "never a guessed model ID"; "managed wrappers remain neutral" | Req | N | MEP:7, 7, 9, 9 (bare token), 10, 10, 13, 11, 11, 19, 19, 19 |
| `DEFAULT_MODEL_CLAUSES` cc L278 | "model = claude-opus-5-5", "effort = medium", "https://code.claude.com/docs/en/model-config" | Req | regex for a backtick-delimited `key = value` with whitespace tolerance (L296–305); URL raw | cc MEP:15, 15, 40 |
| `DEFAULT_MODEL_CLAUSES` codex L273 | "model = gpt-6.1-sol", "effort = medium", "sol-6.1-medium", "https://learn.chatgpt.com/docs/models" | Req | regex as above; alias and URL raw | codex MEP:15, 15, 15, 36 |
| `economy_failures` cc L238–240 / codex L237–239 | "## Batch allocation", "tasks, dependencies and consolidation decisions are finalized", "balanced default", "priority is not an effort value", "Reopen allocation only for remaining work" | Req | R | RM:33, 35, 48, 48, 39 |
| **cc only**, `economy_failures` L241–244 | "settled local causal path or pattern", "known invariants", "discriminating behavior/regression checks", "alaa-implementer-haiku-high", "Interacting design" | Req | R, **positional** | must sit between "Select the bounded semantic branch" and "- `alaa-implementer`:" → cc RM:85 |
| `orchestrator_failures` L72 (both) | "Never silently substitute a model or a generic role" | Req | N | SKILL.md (cc 56 / codex 54) |
| `agent_failures` L51–57 (both), run over every `agents/alaa-*` file (cc main L672–674, codex L669) | "CONFIGURED", "REQUESTED", "OBSERVED", "otherwise write unknown", "never from a pin or request", "Report metadata after the first line", "Effective authority:", "parent overrides", "tool/MCP grants", "Task controls:", "model AND effort", "block this lane", "an omitted field is not a block", "The role name selects no control" | Req | R | every agent file; editable sources are the `assets/*-contract.md` files (e.g. cc `implementation-contract.md:43,45`, `planner-contract.md:13,15`; codex also `reviewer-contract.md:22,24`) |
| `agent_failures` L60 | "missing, inherited, stale-pinned" | Forb | R | agents |
| `agent_failures` L64 | regex `AGENT:.*\| MODEL:.*\| EFFORT:` | Forb | regex | agents |
| `dispatch_failures` L103–105 (both) | "<task_controls>", "explicit model AND effort", "verified invocation surface and effective controls", "explicit model AND effort after owner normalization" | Req | R | `delegation-prompts.md:18` |
| `IMPLEMENTER_REQUIREMENTS` **cc only** L140 | "An exceptional-model admission comes only from the lead's recorded task allocation" | Req | R | every cc `agents/alaa-implementer*.md` (e.g. line 18); source `assets/implementation-contract.md:5`. **Codex has no such clause**, although its agents carry the same sentence. |
| `RUN_ECONOMY_REQUIREMENTS` ('gates', codex L566) | "selects another managed profile, external role or task pair" | Req | N | `verification-and-gates.md:52`; runs against **both** packs (cc L664–666, codex L661–663) |
| `RUN_ECONOMY_REQUIREMENTS` ('repair', codex L576) | "If Failure routing selects another role, profile or task pair, dispatch fresh under Who fixes" | Req | N | `delegation-prompts/30-implementation.md:35`; both packs |
| `verification_failures` cc L255–260 / codex L250–255 | the set of `alaa-implementer*` agent files must equal the policy-JSON profiles that start with `alaa-implementer` | Req | set equality | agents vs `claude-model-policy.json` / `codex-model-policy.json` |

**What none of these touch:**
- "Select the cheapest suitable pair" (heading, RM:49)
- RM:53 "Select the least costly suitable available pair…" (only "no quotas" is bound)
- the whole exceptional-admission block RM:57–62
- RM:47 "Repair context…before you attribute a shortfall to model capacity"
- RM:87 "If fit ceases…"
- the implementer workload list (cc 89–92, codex 95–97)
- Correctness review depth (cc 121, codex 126)
- Codex Terra eligibility (66–68) and the codex bug branch (91)

The bare tokens "replay", "independently", "or block", "affected lane", "model AND effort" and "EVERY role" occur in several places, so they pin no particular sentence.

**Other scripts that bind this text:**
- `validate_pack.py` repeats `task_allocation_failures` (cc L73–75, codex L173–174).
- `REQUIRED` agent-name sets: cc L24–58, codex L42–80.
- Cross-runtime `FORBIDDEN` regex. cc L61 bans `codex|gpt-?[56]|openai|sol|terra|luna|astra|opus 4`. Codex L85 bans `claude|opus|sonnet|fable|haiku|anthropic` on any line outside `CHANGELOG.md` and `validate_pack.py`.
- Agents are render outputs. `render_agents.py` drift check plus manifest sha256 means the editable sources are `assets/implementation-contract.md`, `assets/planner-contract.md`, codex `assets/reviewer-contract.md` and `assets/profile-wrappers.json` (role descriptions).
- In prompting-guide, `profile_projection.py` L42–45, 109–123 forbids `model`, `effort` or `model_reasoning_effort` keys in wrappers.
- `codex_model_policy.py` L32–33 forbids unknown top-level keys ("role defaults/legacy selections forbidden"). L55–57 requires `gpt-6-sol.selection_enabled` false. L66–68 requires `recommended_start` to be among the supported efforts. L72–80 requires profiles to be exactly `{kind, selection_mode:"task-selected", artifacts}`.
- `claude_model_policy.py` L128–157 does the same for Claude, with `default_effort`, `selection_enabled`, and `minimum_claude_code` required for active models.

## 4. Prompting-guide evidence on when to choose each model and effort

**General effort rules** (`references/50-effort-and-thinking.md`):
- :7 "Model selects judgment. Effort selects search depth."
- :14 "Keep thinking on and lower the supported effort to cut cost. Then check retrieval, tool-use reliability and task quality."
- :25 "A different model supplies no missing fact."
- :32 "A supported level is a capability, not a task recommendation or a role-wide ceiling."
- :36–40 Raise effort only after excluding prompt bloat, missing context and tool/spec gaps. Never escalate from a vague importance label; never pin max without a measured benefit; never change model and effort together in a comparison.
- There is no corresponding "when to lower" section.

**Ownership and dates** (`90-model-selection.md`): :5 policy JSONs "define no role default and choose no task pair". :22 the OpenAI matrix was refreshed 9 Oct 2026 and the Claude rows 14 Nov 2026.

**Codex**

| Model | Supported efforts (JSON) | `recommended_start` / `selection_enabled` (JSON) | Surface default | Workloads the source assigns |
|---|---|---|---|---|
| gpt-6-luna | low–max, no ultra (L108–117) | high / true | Codex default "Luna high" (`12-gpt-6.md:15`, page dated 16 Nov 2026) | Small existing-file edits L low/med/high (90:26). Well-scoped bug L low/med/high; the med/high cells show no gain over low (90:33, 57). Organize info L low/med (90:44). Search L med/high/xhigh (90:45). Lower-cost cells for update/debug, slides, data analysis (90:34, 27, 47). Prose: Luna low for precise or bounded work, xhigh for cross-app prioritization (90:64). Small edits Luna medium, 8 Oct (12:19). Luna low for precise edits, 9 Oct (12:20). |
| gpt-6.1-sol | low–ultra (L84–94) | medium / true | none stated; API lists low–max, host adds ultra (12:39, 30 Sep) | Most rows in the balanced column (90:26–52). Sol low for features when cost-priority (12:21). Prose: Sol medium for complex revisable technical work, xhigh for polished, connected or conflicting-evidence work (90:65). "Near-Astra performance at lower cost, suited to repeated, long-running work" (12:15). |
| gpt-6-astra | low–ultra (L60–70) | low / true | Codex default "Astra low" (12:15) | Higher-quality cells for slides, source→output, complex polished, migration, polished app, interactive 3D, data analysis and fallbacks; balanced in two cells (90:31 A high, 90:37 A medium). Prose: low for concise nuanced writing, medium for broad projects, xhigh for demanding analysis; "optionally default to Astra when cost and latency are unconstrained" (90:66–67). "Most demanding work" (12:15). |
| gpt-6.1-terra | low–ultra (L96–106) | low (host catalog metadata, `capability_evidence`) / true | API default medium (12:40, 3 Nov) | Supplied-material writing, defined-outcome computer use, scoped code fixes (90:69, 3 Nov 2026); codex RM:66–68. |
| gpt-6-sol | low–ultra | medium / **false** (historical) | — | Excluded from ordinary selection (90:14). |

The Codex JSON has `verified_on` 2026-11-03 and no `default_effort` key.

**Claude**

| Model | Supported efforts | `default_effort` / `selection_enabled` / min CC (JSON) | Surface default | Workloads and effort guidance |
|---|---|---|---|---|
| claude-haiku-5-5 | low–max | medium / true / 2.1.293 (L222–241) | medium, Claude Code too (`36-haiku-5-5.md:24`) | Bounded retrieval, exact procedures, admitted mechanical or bounded semantic implementation, docs. Launch names compaction, classification, queries and coding subagents. "Sonnet and Opus stay the stronger candidates for complex agentic coding" (36:3). Real-time, bulk, cost-sensitive (90:76). Efficiency-first: start Haiku and move up on a demonstrated gap (90:77). Effort, 9 Oct (36:30–35): low = short or simple; medium = most work incl. agentic coding; high = longer or stricter work or knowledge tasks; xhigh/max only with a stated benefit over Sonnet. JSON note L240: "Medium is the starting setting…" |
| claude-sonnet-5-5 | low–max | **high** (= Platform/API) / true / 2.1.284 (L191–210) | medium in Claude Code and apps, high on API (`31-sonnet-5-5.md:7`) | Everyday coding, analysis, content, vision, agent tools (90:73). Start at medium for well-specified agentic work and high for harder or longer tasks (31:8; 90:83). max scored below xhigh in two cases (31:10). Bounded local decisions fit (31:14). |
| claude-opus-5-5 | low–max | medium / true / 2.1.280 (L129–147) | medium, Claude Code too (`21-opus-5-5.md:7`, 14 Nov) | Complex autonomous coding, broad refactors, systems, computer use (90:74). Capability-first: "Start Opus; optimize downward after adequate quality", "Opus medium starting effort" (90:78). "The guide recommends Opus as the starting point for most workloads" (90:82). Benchmark max/xhigh prescribe nothing (21:9). |
| claude-fable-5-2 | low–max | **high** (= API) / true / 2.1.321 (L149–169) | API high, Claude Code medium (`43-fable-5-2.md:13`) | Highest capability, hours-long agent sessions, multistep deep research, finished documents (90:75). Move to Fable when Opus at xhigh or max falls short (90:79; 43:19). Effort (43:23–27): most gain at high; medium for interactive and everyday work; low for well-specified tasks and high-volume subagents; xhigh only for the hardest long-running work with a measured gain; max to measure the ceiling; early stops more frequent at low and medium. |
| claude-fable-5-1, claude-haiku-4-5-20251001 | low–max; [] | high/false; null/false | — | Historical. |

The Claude JSON has `verified_on` 2026-11-14 and no `recommended_start` key. Its `default_effort` records the API default, not the Claude Code default, for Sonnet and Fable (notes at L209 and L168).

## 5. Sentences that push toward a cheaper pair vs. guard against a too-weak pair

**Pushes toward a cheaper or weaker pair:**
- RM:47 (both): "Repair context, specification or tool failures before you attribute a shortfall to model capacity."
- RM:48 (both): "Role title, sensitivity, duration, whole-goal labels and a second independent lens alone never select a frontier or stronger model."
- codex RM:48: "Current-family selection never upgrades a suitable Luna pair to Sol."
- RM:49–50, 53: "Select the cheapest suitable pair" / "Evaluate the cheapest…" / "Select the least costly suitable available pair. Depart from it only on an explicit user choice or recorded task evidence."
- RM:52: "Non-bug semantic work needs no reproduced failure" (widens cheap admission).
- RM:55: rejecting a cheaper pair needs "the actual failed fit predicate or stronger task-specific evidence. Titles, volume, priority labels and whole-goal complexity are not failed predicates."
- RM:57–62: the exceptional-admission requirements, plus "A repairable defect or an imagined insufficiency is not model inadequacy."
- cc RM:94 / codex 99: "An unresolved decision alone never establishes model inadequacy."
- RM:83: "File count alone neither qualifies nor disqualifies…"
- `delegation-prompts/30-implementation.md:27`: "Demanding work alone does not admit the exceptional implementation profile."
- `assets/planner-contract.md:7`: "planning cost does not set implementation cost… never infer an admission from a whole-goal label."
- SKILL.md cc 65 / codex 63: "Planning effort never sets worker effort."
- `implementation-contract.md:5` (all implementers): "Never upgrade your own profile."
- codex `alaa-implementer-luna-low.toml:3`: "cost-priority branch".
- 50-effort:36–39 (raise only after exclusions, no max pin); 50:25; 90:83 ("rule out automatic maximization"); 36-haiku:35.

**Guards against a too-weak pair:**
- RM:51: all seven bounded-suitability predicates are required.
- cc RM:74–83 / codex 78–87: mechanical predicates; "Ambiguous matches, undefined scope or design changes fail admission."
- cc RM:85: "Interacting design, or unresolved decisions about cross-boundary contracts, trust, shared state or consistency, select a workhorse route below."
- codex RM:89, 91: "…fails admission". Codex RM:68: Terra needs every bounded predicate.
- RM:87 (cc) / 93 (codex): "Priority or a model preference never waives fit… If fit ceases, stop dependent work, preserve valid edits and return the remaining scope for reclassification."
- codex RM:48: "When current Sol is missing, require an exact eligible realization or block the affected lane; never fall back to old Sol."
- SKILL.md cc 56 / codex 54: "report each missing, stale or unavailable model or role as blocked or degraded. Never silently substitute a model or a generic role."
- MEP:10, 26, 28: unsupported or unrealizable pairs block; "Never silently change the pair".
- `implementation-contract.md:5`: a failed predicate returns the work for reclassification.
- 36-haiku:16: "Missing scope or evidence, or interacting design decisions, require reassessment, not an inherited Haiku choice."
- 43-fable:27: early stops at low and medium.
- 31-sonnet:15: at low, state the done condition and checks.

**Is it symmetric?** No.
- Escalation has its own evidence gate (the exceptional admission, RM:57–62). Rejecting a cheaper pair needs a recorded failed predicate (RM:55).
- A cheaper choice needs no reason beyond "suitable" (RM:53). Suitability predicates exist only for the mechanical, bounded and bug branches.
- Between workhorse tiers (Sonnet vs Opus, Sol medium vs high/xhigh), the only guidance is the workload descriptions: cc RM:89–92, codex RM:95–97.
- No sentence says how to choose an effort level within a model, beyond "Justify model and effort separately" (RM:54).
- No sentence anywhere addresses a pair that is too strong for its lane (searched for downgrade, over-qualified, lower effort and similar terms).

## 6. Feedback loop after a lane returns

- **Reassessment points:** cc RM:39 and RM:117 / codex RM:39 and RM:122. Allocation reopens only for remaining work "at a material scope change or a fix follow-up"; never replay completed work.
- **Fit ceases:** cc RM:87 / codex RM:93, plus `implementation-contract.md:5`. The lane stops dependent work and returns the remainder for reclassification. Self-upgrade is forbidden.
- **Status handling:** `agent-catalog.md` cc 63–64 / codex 64–65:
  - `INCOMPLETE`: "continue the same agent or reassign the remainder; never accept the lane".
  - `BLOCKED`: "Supply the named input…, correct the controls, or reclassify the lane".
- **Who fixes** (`verification-and-gates.md:50–52`, both): "Use the smallest capable hand… continue the existing implementer… Dispatch fresh only when continuation is unavailable, context is invalid, or `routing-matrix.md` selects another managed profile, external role or task pair."
- **Continuing an implementer** (`delegation-prompts/30-implementation.md`, both): "The original `<task_controls>` stands" (L34); "If Failure routing selects another role, profile or task pair, dispatch fresh under Who fixes" (L35).
- **After a fix** (`verification-and-gates.md:46`): a returning defect class means "reconcider the approach or the decomposition". The pair is not mentioned.
- **Failure routing:** cc RM:154 / codex RM:159: "select the repair role for the remaining work… Implementation routing for the rest". `90-completion/20-review-followup.md:5` points to Failure routing.
- **Stop conditions:** SKILL.md cc 124 / codex 122: "the same lane or cause blocks twice".
- **Exceptional route:** reachable after weak work only via "applicable documented inadequacy of the high-effort workhorse, established after context, specification and tool correction and after decomposition" (RM:59).
- **Not found:** no rule tells the lead to lower the pair after over-qualified work, or to record allocation outcomes for later allocations.

## 7. Recorded owner decisions on model and effort routing

`CONTRACT-DECISIONS.md` mentions no models: nothing matched English model or effort names, and the Persian word «مدل» returns no match.

**2026-10-08**, `outputs/20261008-haiku55-routing/`:

*Recorded as user direction:*
- Replace Haiku 4.5 with Haiku 5.5 and restore `alaa-implementer-opus`: `source-evidence.md:27`; plan `docs/_agent_plans/20261008-140000_haiku55-routing.md:129`.
- Sonnet's omission from a prompt did not authorize removing it (plan:113).
- "Normal implementation should not select below Sol" (`source-evidence.md:60`; plan:202). **Superseded** the same day: "research should determine the structure" (`source-evidence.md:64–66`; plan:208).
- Phase 7: the user "explicitly authorize[d] Luna and Haiku5.5 for exact repeated edits, including finite batches across many files" (`source-evidence.md:70`; `plan-first-routing-cases.md:31`). This is where today's automatic mechanical branch comes from.

*Lead design, ratified and reviewed (not stated as user words):*
- Direct selection with no trial ladder, and strongest-model admission only on diagnosed high-effort-workhorse inadequacy or explicit user selection (plan:151–152, 181; `instruction-drafts.md:37, 53`; `report.md:7, 9`).
- Review separated user selection from inadequacy evidence (`review.md:39, 44`).
- `closure.md:61` says the scan covered "user corrections: direct selection, scoped exceptional admission…". It does not quote the user.

**2026-10-09:**
- *Task model routing:* plan `20261009-160000_task-model-routing.md:151`: "User requirements 1 and 2: actual task allocation belongs to each runtime orchestrator; all-role executable pins removed and explicit supported controls required. No role-title frontier exception remains." `report.md:7` ("Balanced remains the default priority… role titles and independent second lenses select no frontier default"); `report.md:24` ("The user's task-selection ownership correction"); `acceptance.md:19` (A13: no title shortcut, no mandatory trial ladder).
- *Agentic economy:* plan `20261009-090000_agentic-economy.md:131`: "The user requests the complete official task table in skill references… and one batch selection after tasks/dependencies/consolidation are finalized." This is the origin of Batch allocation. Plan:20 and :33 ("Reject blanket downgrades, mandatory trial ladders") are lead planning.
- *Origin of the "exact official recommendation" branch:* `orchestrator-implementation.md:11`: new Astra medium/xhigh "have exact official-task/priority admission with reasoning need and rejected cheaper/decomposed alternatives". This is the lead's implementation; I found no user statement for it.

**2026-10-12**, `outputs/20261012-orchestrator-routing-plan/`, plan `docs/_agent_plans/20261012-120000_orchestrator-routing.md`:
- User: rejects old Sol as normal selection; no cheap-model quotas (plan:116, :49).
- "The user's current-generation and suitable low-cost routing correction" (`validation.md:28`). The user's chat symptoms were "accepted as reported symptoms, not a reproduced dispatch trace" (plan:60).
- Ratified design: the R5 cheap semantic admission, "Select the cheapest supported available suitable pair… record the actual failed fit predicate… No quotas, automatic trial ladder, frontier-by-title or old-Sol fallback" (plan:96).
- Goal: "select the least costly suitable available model/effort for each actual task" (plan:37). "Allocation is by suitability, not model-use quotas. Preserve legitimate Sol, Sonnet, Opus, Astra and Fable cases" (plan:43). Cases R1–R15 (plan:199–215); "quotas manufacture cheap-model usage" (plan:274).
- The enforcement it added, `check_allocation_evals.py` and `assets/evals/`, is **absent** from current `alaa-prompting-guide`.

**2026-11-14 verification by judgment** (`artifacts/orchestrator-verification-by-judgment-20261114/report.md`):
- Owner direction concerns verification cycles, not models (:7).
- ":27 Unchanged: … model and effort allocation".
- It removed the absolute "Model capability never waives an observer or mandatory gate" (:11, :25).

**Defaults** (not in the listed rows): `artifacts/agent-control-defaults-20261018/model-draft.md:5` and `model-report.md:10` call `sol-6.1-medium` "the user's … alias". **I found no record of who chose Claude Opus/medium or why**, and no recorded owner rationale for either default.

**Unread:** `artifacts/core-skills-compression-20261116/mapping-orchestrator-pair.md` exists and mentions the alias. It falls outside the listed rows.

## 8. Defaults and implementer roles

**Omitted-control defaults:**
- **cc:** `claude-opus-5-5` / `medium`, passed as alias `opus` (cc MEP:15, 17; checker cc L278).
- **codex:** `sol-6.1-medium` → `gpt-6.1-sol` / `medium`, passed as the executable ID (codex MEP:15, 17; checker codex L273).
- Resolved defaults "count as task selection" (`90-model-selection.md:8`).
- Recorded omission evidence: model omitted in 508 of 714 Agent dispatches and effort in 591 (`alaa-cc-orchestrator/CHANGELOG.md:55`). "four implementer lanes ran on Fable that way" (`artifacts/orchestrator-stack-roles-20261114/report.md:73`).

**cc implementer roles (11)** — RM plus `assets/profile-wrappers.json` descriptions:

| Role | Workload |
|---|---|
| `alaa-implementer` | everyday grounded coding (RM:89) |
| `alaa-implementer-sonnet-high` | harder or longer grounded work (RM:90) |
| `alaa-implementer-opus` | materially coupled unresolved system decisions (RM:91) |
| `alaa-implementer-opus-high` | interacting unresolved design and demanding system reasoning (RM:92) |
| `alaa-implementer-fable` | exceptional admission (RM:94) |
| `alaa-implementer-haiku` | mechanical or bounded semantic work (RM:74, 85) |
| `alaa-implementer-haiku-high` | longer or stricter bounded work (RM:85) |
| `alaa-implementer-laravel`, `-frontend`, `-go`, `-infra` | stack-bound (RM:103–108) |

**codex implementer roles (14):**

| Role | Workload |
|---|---|
| `alaa-implementer` | normal engineering (RM:95) |
| `alaa-implementer-high` | substantial interacting reasoning (RM:96) |
| `alaa-implementer-xhigh` | sustained coupled reasoning (RM:97) |
| `alaa-implementer-astra`, `-astra-medium`, `-astra-xhigh` | exceptional admission (RM:99) |
| `alaa-implementer-luna` | mechanical, or bug at balanced priority (RM:78, 91) |
| `alaa-implementer-low` | bounded semantic work (RM:89) |
| `alaa-implementer-luna-low` | bug, cost-priority (RM:91) |
| `alaa-implementer-luna-high` | bug (RM:91) |
| `alaa-implementer-laravel`, `-frontend`, `-go`, `-infra` | stack-bound (RM:108–113) |

Both packs also route Ent work to the external `alaa-ent-specialist` (cc RM:66–68 / codex RM:70–72). Role names pick neither model nor effort (RM:45; agent-catalog:3).

**Could not determine:** the user's verbatim words for the 10-12 and 10-09 requirements (only the lead's paraphrases are recorded), and any owner rationale for the Opus/medium default.
