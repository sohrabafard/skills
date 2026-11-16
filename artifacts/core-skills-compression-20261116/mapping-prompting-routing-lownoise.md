# Mapping prompting routing lownoise

Read-only mapping report, 2026-11-16. Dated evidence: verify a line number before relying on it.

I mapped all eight questions from the files and scripts. I edited nothing and ran nothing; I only ran grep/wc/awk and a read-only `python3 -I -B` load of the two policy JSONs. Word counts come from `wc -w` for whole files and from an awk count of each heading's section. Paths below are relative to `skills/sohrab/`; PG = `alaa-prompting-guide`, CIR = `alaa-code-intelligence-routing`, LN = `alaa-low-noise`.

## 1. Model files in PG

None of the current files is written as a delta. Each one stands alone and cites its predecessor only as "historical".

| File (words) | Status | Routed from |
|---|---|---|
| 10-gpt-5-6 (2061) | Superseded (historical; "legacy exception" only) | 00-topic-map:12; 12:3-4 |
| 12-gpt-6 (853) | Current | topic-map:11; 90:59; 11:3, 11:45; 00-source-map:67; 60:116; 10:3 |
| 20-opus-5 (1790) | Superseded | topic-map:15; 21:3 |
| 21-opus-5-5 (413) | Current | topic-map:14; 20:3 |
| 30-sonnet-5 (1385) | Superseded | topic-map:17; 31:3 |
| 31-sonnet-5-5 (774) | Current | topic-map:16; 30:4; source-map:40 |
| 35-haiku-4-5 (151) | Superseded (still has a disabled entry in the policy JSON) | topic-map:23 |
| 36-haiku-5-5 (495) | Current | topic-map:22; source-map:56; 50:17; 06:83 |
| 40-fable-5 (2015) | Superseded | topic-map:21; 43:3; 42:3; 06:99 |
| 42-fable-5-1 (399) | Superseded | topic-map:20; 43:3 |
| 43-fable-5-2 (1120) | Current | topic-map:18; 40:3; 42:3; 90:69; 50:49; 60:93; source-map:64; claude-model-policy.json:168 |

- **Outside PG:** no file in `skills/`, root `AGENTS.md` or any script cites a model file. Only old `artifacts/`, `outputs/` and `docs/_agent_plans` mention them.
- **Superseded total:** 7,801 words, against 3,655 words in the five current files.
- **SKILL.md** routes to none of them directly (SKILL.md:40 points to the topic map). SKILL.md:13 says the "historical references are for reference only".
- **Successor repeating predecessor:**
  - No sentence of 40+ characters is identical in 20→21, 30→31, 35→36 or 10→12.
  - 42→43 shares one near-identical safeguard passage (about 35 words): 42:20-22 = 43:186 ("Never bypass a safeguard or install a local fallback. Keep refusal, fallback and unknown serving identity visible in reports").
- **The same statement repeated across model files** (current files; words approximate):

| Statement | Locations | Words |
|---|---|---|
| Runtime orchestrator owns allocation; role title or availability selects nothing | 12:13,17; 21:3; 36:3,9; 42:3; 43:3; 31:13 | ~200 |
| Don't inherit an old pin; raise effort only after excluding context/tool/spec gaps | 21:7; 31:8-9; 43:154; 36:15 | ~90 |
| Keep focused checks and independent gates; authority test in 80 | 12:30-31; 21:12; 31:20; 42:13-14; 36:7 | ~120 |
| Set length/progress separately from effort | 21:12; 31:31; 42:17; 43:151 | ~60 |
| Append-only history and thinking blocks; don't invent Claude Code keys | 21:19; 31:45-53; 42:28-30; 43:182; 12:39-44 (Codex variant) | ~160 |
| Fallback/safeguard visibility; read 41 before selection | 42:32-35; 43:186; 31:58-61; 36:15 | ~110 |
| Mythos excluded | 42:48; 43:3; plus 90:13 and 41:39 | ~40 |
| Delegation polarity owned by 06 | 21:14-15; 31:21; 42:22-24; 43:168 | ~60 |
| Per-surface default effort | 21:9; 31:8; 36:13; 43:139; also 41:8 and 90:72-77 | ~150 |
| Vendor claims prove no local calibration / unrun | every current file | ~150 |

## 2. Literals bound to checkers

**`PG/scripts/check_rule_writer_grants.py`**
- Fixed paths: `assets/rule-writer/contract.md`, `…/claude/alaa-rule-writer.md`, `…/codex/alaa-rule-writer.toml` (79-81).
- Requires `assets/codex-model-policy.json` (320, 286) and `assets/claude-model-policy.json` (298).
- G5 (255): each wrapper body must equal contract.md exactly after `normalise` (strip edge newlines).
- G2 (86, 222): Claude tools ⊆ {Read, Glob, Grep}; frontmatter keys ⊆ {name, description, tools, model, effort, skills}.
- G4 (275): `sandbox_mode = "read-only"`.
- G6 (90-92, 258-262):
  - MODEL_NAME_RE `\b(opus|sonnet|haiku|fable|luna|terra|sol|astra)\b|gpt-?\d` is banned in the contract body and description.
  - `AGENT:\s*\S+\s*|` and `EFFORT:` are banned.
- G7 (93, 268): DOCTRINE_RE `` `alaa-prompting-guide\s+(references/….md)` `` — each cited file must exist. The contract cites 60-skill-authoring, 00-topic-map, 70-agent-instruction-files and 80-subagent-authoring (contract.md:7, :17).
- G10 (96, 239-248): every `` `<skill> references|assets|scripts/ `` owner named in the contract must appear in the Claude `skills:` preload (alaa-prompting-guide).
- G8 (281): name and description equal across both wrappers.
- G9 (264): no model, effort or model_reasoning_effort key.

**`claude_model_policy.py`**
- Policy path: `assets/claude-model-policy.json` (14).
- Hard-codes `skills/sohrab/alaa-cc-orchestrator/agents` and the writer dir (15-16), plus the ROLES list (17). Coverage requires exactly those profiles plus main and main-deep (149).
- schema_version 2 and surface `claude-code` (92, 96).
- Model ID regex `claude-(?:opus|sonnet|fable)-\d+(?:-\d+)?|claude-haiku-(?:5-5|4-5-\d{8})` (126).
- thinking_mode ∈ {adaptive-always-on, adaptive, extended} (142).
- Haiku 4.5 must have empty supported efforts (140).
- Profile shape kind/selection_mode/artifacts (153-157).

**`check_claude_model_policy.py`**
- Imports `REPO_ROOT/scripts/validate_sohrab_skill_pack.py`'s `mini_yaml_load` (221-225).
- Default roots are the orchestrator agents dir and the writer dir (260).

**`codex_model_policy.py`**
- ARTIFACTS hard-codes `skills/sohrab/alaa-codex-orchestrator/agents/alaa-*.toml` and the rule-writer TOML path (9-10).
- Allowed model IDs {gpt-6-astra, gpt-6-sol, gpt-6.1-sol, gpt-6.1-terra, gpt-6-luna} (59).
- `gpt-6-sol` must have selection_enabled false (55-57).
- Efforts ⊆ {low, medium, high, xhigh, max, ultra} (65).
- Allowed top-level keys (33).

**`check_codex_model_policy.py`**: no Markdown literals; it reads TOMLs under `--agent-root`.

**`task_model_controls.py`**: literal `gpt-6-sol` (26); no Markdown.

**`profile_projection.py`** (run against an orchestrator root)
- Reads `<root>/assets/profile-wrappers.json` (72).
- Requires the anchor `\nEngineering baseline:` exactly once in `implementation-contract.md` (95-98); bindings must start `Stack binding: `.
- Emits the header `# Generated by scripts/render_agents.py; edit {contract}.` and `# grant-template: materialize-live-parent-mcp` (46, 54).

**`check_goal_condition.py`**: CAP 4000 (165); the five surface names (166); the desktop token regexes (172-177). No Markdown dependency.

**Repo-root `scripts/` checkers**
- `validate_sohrab_skill_pack.py`:
  - V3 (856) needs a heading matching `^#+\s+.*\b(when\s+not\s+to\s+use|do\s+not\s+use)\b`.
  - Description ≤1024 hard / 975 warn, measured packaged (96, 113).
  - V4 warns on a body over 120 lines (114, 860). This is the whole body, not "above the first reference".
  - `openai.yaml` short_description 25-64 characters and default_prompt containing `$<name>` (115-116, 874-881).
  - V5/V9: every `` `references|assets|scripts/…` `` path in SKILL.md and `references/00-topic-map.md` must exist (885-891).
- `check_fleet_references.py` (R1-R6, 163-171): every cross-skill path must resolve. Renaming any cited reference breaks the citations in item 3.
- `check_lifecycle_contract.py` L4: the tokens IMPLEMENTED, MERGE_CANDIDATE, RELEASE_CANDIDATE and PUBLISHED must not appear in these skills (none do today).
- `check_skill_index.py`: the skill names must remain in `README.md` and `README.fa.md`.

**Other scripts that import or read PG**
- `alaa-cc-orchestrator/scripts/render_agents.py:10-13` imports `claude_model_policy` and `profile_projection`.
- `alaa-cc-orchestrator/scripts/validate_pack.py:185-188` runs `check_claude_model_policy.py`.
- `alaa-cc-orchestrator/scripts/check_agent_contracts.py:259-260` reads `assets/claude-model-policy.json`.
- `alaa-codex-orchestrator/scripts/render_agents.py:18-39,65` loads task_model_controls, codex_model_policy, profile_projection and `codex-model-policy.json`.
- `alaa-codex-orchestrator/scripts/check_agent_contracts.py:254-255` reads the policy.
- `install-agents.sh:14` and `install-skill.sh:7` take the policy_root.
- Repo `scripts/install_claude_agents.py:20,136` reads the writer `.md` and PG `SKILL.md`.
- `alaa-cc-orchestrator/scripts/check_agent_grants.py:42,244,270` requires the skill name `alaa-code-intelligence-routing` in every preload.

**Cannot change without editing a script:** directory and skill names; the assets paths; the contract-equals-wrappers rule; the doctrine filenames cited in contract.md; topic-map paths; the "When NOT to use" heading; `openai.yaml` fields.

## 3. Citations from outside the three skills

| Cited | Heading | Citing file:line |
|---|---|---|
| PG 60-skill-authoring | — | root `AGENTS.md`:141; `AGENTS.md`:100; alaa-quasar-app-vite-v3/references/91-…:5 |
| PG 06-invocation | — | `AGENTS.md`:70; alaa-cc-orchestrator/SKILL.md:123; alaa-codex-orchestrator/SKILL.md:121; alaa-go-chi-development/SKILL.md:14; alaa-workflow/references/phase-prompts.md:29; quasar 91:5 |
| PG 41-claude-code-runtime | **Native Advisor** | alaa-cc-orchestrator/references/model-effort-policy.md:42 |
| PG 41 | — | alaa-cc-orchestrator/SKILL.md:70; model-effort-policy.md:19,21,34; CHANGELOG:51-52 |
| PG 11-codex-runtime | — | alaa-codex-orchestrator/SKILL.md:68; model-effort-policy.md:30; verification-and-gates.md:101; CHANGELOG:22,38,50 |
| PG 90-model-selection | — | both orchestrators' model-effort-policy.md:3 and routing-matrix.md:72 |
| PG 50-effort-and-thinking | — | about 40 sites, e.g. alaa-docker-production/SKILL.md:65, alaa-golang/SKILL.md:48, both routing-matrix.md:72, alaa-shaka-player/agents/openai.yaml:2 |
| PG 70-agent-instruction-files | — | quasar 91:5 |
| PG assets/claude- and codex-model-policy.json | — | cc and codex model-effort-policy.md:5, plus the scripts in item 2 |
| PG skill (no file) | "authoring and compression criteria" | cc agents/alaa-instruction-reviewer.md; codex agents/alaa-instruction-reviewer.toml:6 |
| CIR SKILL.md | **Operation card** ("apply its operation card") | 38 agent files across both packs; codex assets implementation-contract.md:73, planner-contract.md:32, reviewer-contract.md:40; cc profile-wrappers.json (13 entries) |
| CIR 80-agent-scoping | — | cc agent-catalog.md:85,120; codex agent-catalog.md:112 |
| CIR 10-routing-contract | — | no citation outside CIR (CIR SKILL.md:33 cites its *Selection and identity*) |
| LN workflow-integration | **Delegated lanes** | cc and codex delegation-prompts.md:32 |
| LN skill name | — | alaa-workflow/SKILL.md:16; alaa-workflow/references/companion-routing.md:9; cc SKILL.md:86; codex SKILL.md:84 |

## 4. Duplication inside PG

**Rule-writer wrappers:** nothing generates them. No renderer exists; `check_rule_writer_grants.py` G5 only enforces a verbatim embed of contract.md (550 words) in both wrappers (620 words each). So about 1,100 words are enforced copies, not editable separately.

| Rule | Locations | Apparent owner | Words in copies |
|---|---|---|---|
| Never remove/weaken; compress relocates nothing; done-test | 60:67-71; contract.md:11-14,23,29; SKILL.md:42 | 60 | ~250 (plus wrapper copies) |
| Task controls explicit; orchestrator allocates; main session external | SKILL.md:8,27; dispatch.md:3; 12:13; 41:17,230; 11:58,159; 80:40,84; 90:5-9; 50:28-31,36 | 90 / orchestrator | ~600 |
| Keep focused checks and independent gates | SKILL.md:57; 80:50-57; 60:107; 06:96-100; model files (item 1) | 80 | ~350 |
| Requested vs observed identity; unknown stays unknown | 41:21; 80:72-80; 11:67; 50:38 | 41/80 | ~200 |
| Subagent dirs, `name` identity, frontmatter list | 41:107 vs 80:20-22 (lists differ: 80 adds autoCompactWindow, omitClaudeMd, experimental) | 80 | ~150 |
| Nesting default, `Agent` withholding | 41:113-118; 80:98 | 41 | ~60 |
| Codex AGENTS.md chain and `project_doc_max_bytes` | 70:18,28-30; 11:88-90 (conflict: 70:30 says the tail, i.e. most specific, is dropped; 11:90 says the outermost files) | 70 or 11 | ~200 |
| Codex agent TOML keys and dirs | 80:28; 11:53-56 | — | ~60 |
| Codex skill listing 2%/8000, Codex frontmatter name/description only | 61:36,48; 11:113,115,142 | 61 | ~110 |
| Four-way prompt/file/skill/subagent test | 60:7-16; 70:32-40; 80:5-14 | 60 | ~400 |
| Wording failure modes | 60:119-137; 70:62-72; also `AGENTS.md` "The wording test" | 60 | ~300 |
| Repository `/name` sigil rule | 06:21; 70:84; `AGENTS.md`:66-68 | 06 / AGENTS | ~120 |
| Goal condition plain text / transcript evidence | 06:49-55; 41:169,185 | 06 | ~150 |
| Default efforts per surface | 90:72-77; 41:8; model files | model files | ~150 |
| Body cost vs reference cost | 00-topic-map:3; 60:29 | 60 | ~40 |
| Exit codes 0/1/2 | SKILL.md:35; each script docstring | scripts | — |

**00-source-map vs 00-topic-map:**
- **00-topic-map** (891 words) is the run-time router. SKILL.md:40 says to read it first; it holds the condition→file table and is validated by V9 and R6.
- **00-source-map** (1,089 words) is mixed. Lines 5-34 are run-time rules: source priority, freshness triggers, packaging, interpretation (SKILL.md:63 routes to it for freshness). Lines 36-69 (about 650 words) are a dated refresh log, which is provenance.

## 5. Heading inventories (words; what each decides)

**41-claude-code-runtime-features.md (5,424)**

| Heading | Words | Decides |
|---|---|---|
| Preamble | 44 | Scope |
| Current model, effort and identity resolution | 643 | Precedence, alias-only `model` parameter, effort precedence |
| Fallback and safeguards | 88 | Fallback disclosure |
| Native Advisor | 356 | Advisor pairs and authority |
| Prompts for a session that may have an advisor | 759 | Advisor prompt wording |
| Historical harness mechanics | 56 | Date disclaimer |
| `/loop` | 428 | Loop mechanics (doc-restatement) |
| Agent tool / subagents | 689 | Caps, nesting, worktree base (mostly doc) |
| Workflow tool | 676 | Doc-restatement |
| Plan mode / Ultraplan | 353 | Doc-restatement |
| `/goal` | 322 | Cap and evaluator |
| Surface preflight and rejected commands | 295 | Desktop rejection procedure (house) |
| Choosing between… | 335 | Mechanism choice (mostly doc) |
| Caveats | 119 | Dates |
| Sources | 70 | — |
| Managed task-selected authority roles | 85 | Duplicates 11:159 |

- Narrative/dated text: about 2,000 words on dated lines (7-19, 47, 66, 72, 74-79, 107, 116, 118, 145, 147, 165, 181, 209).
- Incident/observation: line 66 (observed 2.1.307 subagent), 116 (removed in v2.1.224), 118 ("earlier documentation stated…"), 181-183 (user-observed rejection).
- Doc-restatement: about 2,500 words (lines 81-161, 195-205).

**60-skill-authoring.md (3,875)**

| Heading | Words | Decides |
|---|---|---|
| Preamble | 143 | Scope |
| Should this be a skill at all? | 249 | Artifact type |
| The description carries the activation decision | 152 | Description parts |
| Progressive disclosure | 164 | Body vs reference |
| Reference decomposition | 398 | Split procedure and router placement |
| The draft-then-compress loop | 786 | Compression contract (cited by root `AGENTS.md`) |
| ASD-STE100 style | 123 | Style |
| Evidence for instruction changes | 100 | Evidence types |
| Optional comparative evaluation | 75 | Comparison protocol |
| Carry-over review for a new model generation | 342 | Carry-over checks |
| Lean prompts must preserve behavior | 67 | GPT pointer |
| The wording is the mechanism | 434 | Wording failure modes |
| Defects and fixes | 466 | — |
| Checklist | 213 | — |
| Freshness | 61 | Dates (dated: 173) |
| Sources | 32 | — |

Doc-restatement is small: about 40 words (line 13).

**80-subagent-authoring.md (2,686)**

| Heading | Words | Decides |
|---|---|---|
| Preamble | 77 | Scope |
| When a subagent is the right tool | 238 | Mechanism choice |
| Claude Code: markdown with YAML frontmatter | 256 | Doc-restatement |
| Codex: standalone TOML | 223 | Doc plus `skills.config` warning |
| The four things every definition pins | 153 | Definition contents |
| Authority boundaries beat instructions | 229 | Gate retention |
| Output contracts | 286 | Return format |
| Configuration and observed identity | 95 | Identity reporting |
| Task model and effort independent of authority role | 94 | Control ownership |
| Prompting a subagent once defined | 195 | Dispatch content |
| Delegation polarity | 73 | Pointer to 06 |
| Defects and fixes | 312 | — |
| Checklist | 193 | — |
| Caveats | 161 | Dated; issue 14161 history at 136 |
| Sources | 26 | — |

**70-agent-instruction-files.md (2,607)**

| Heading | Words | Decides |
|---|---|---|
| Preamble | 83 | Scope |
| What each file is and which runtime reads it | 274 | Doc-restatement; dated v2.1.277 at 20 |
| Nesting and precedence | 338 | Doc-restatement |
| The distinction from a skill, and the decision test | 277 | Instruction file vs skill |
| What belongs in one | 251 | Content |
| What does not belong | 205 | Content |
| Writing rules that are actually obeyed | 296 | Wording |
| One repository, two runtimes | 253 | Bridge choice |
| Defects and fixes | 258 | — |
| Checklist | 184 | — |
| Caveats | 99 | Dates |
| Sources | 26 | — |

**11-codex-runtime-features.md (2,523)**

| Heading | Words | Decides |
|---|---|---|
| Preamble | 27 | Scope |
| Rejected tool input or patch context | 176 | Repair procedure (house) |
| `/goal` — persistent objective mode | 192 | Doc |
| CLI composer and objective storage | 94 | Dated source evidence |
| Activation | 57 | Goal activation |
| Ready-to-use `/goal` template | 167 | Template |
| Subagents | 448 | Pin precedence and sandbox; dated 58, 61, 65 |
| `spawn_agents_on_csv` | 140 | Doc |
| `AGENTS.md` | 195 | Doc |
| Agent Skills | 337 | Doc plus a "retired Windows host" history (109) |
| Session-shaping slash commands | 173 | Doc |
| Automations | 141 | Doc |
| Caveats | 166 | Dated/history |
| Sources | 46 | — |
| Managed task-selected authority roles | 93 | Duplicates 41:230 |

Doc-restatement is about 1,200 words.

**06-invocation-and-composition.md (2,370)**

| Heading | Words | Decides |
|---|---|---|
| Preamble | 67 | Scope |
| How a skill is actually reached | 237 | Mechanisms |
| Writing a call site | 262 | Sigils |
| Mention versus invocation | 84 | Invocation |
| Compose from skill owners | 117 | Composition |
| Role-consistency contract | 128 | Session role |
| Compose the kickoff and completion condition | 416 | Kickoff and goal |
| Satisfiable completion conditions | 59 | Bounds |
| Delegation polarity | 521 | Per-model polarity |
| Pre-send checklist | 169 | — |
| The failure shape to recognize | 88 | — |
| Freshness | 88 | Dated |
| Sources | 77 | — |

Line 9 cites a bug report as evidence.

**90-model-selection.md (1,732)**

| Heading | Words | Decides |
|---|---|---|
| Capability evidence and allocation ownership | 341 | Ownership; history at 13 |
| Official task guidance and local policy | 1,098 | The OpenAI selector matrix (lines 19-47, about 400 words) restates vendor docs; Claude table |
| Companion routing | 229 | Packs and companions |
| Caveats | 40 | — |

## 6. CIR

**Heading word counts**
- **SKILL.md (860):** preamble/frontmatter 107; Decision procedure 94; Operation card 424; Authority 58; When NOT to use 53; Output 36; Stop and failure 53.
- **00-topic-map:** 292.
- **10-routing-contract (1,851):** Selection and identity 1,074; Consume evidence 128; Finite degraded operation 311; Authorized native continuation 185; Mutation uncertainty 100; Handoff 29.
- **20-documentation-routing:** 200. **30-artifact-boundaries:** 256.
- **40-stack-bindings (1,539):** preamble 42; Project applicability 46; Laravel 429; Independent failure domains 135; CodeGraph specialized groups 201; Claude Code language-service tool 130; Serena specialized groups 208; Go 100; PHP 66; Python 43; Vue/Quasar 59; Other source 38.
- **45-native-tools (1,388):** preamble 114; CLI vs LSP 221; Files, literals and syntax 173; Structured data 137; PHP/Laravel 195; Go 298; Python 91; Package scripts 88; Native sources 33.
- **50-hooks (1,052):** preamble 59; Ownership 445; Adoption 148; Rollback 47; Recorded deviations 338.
- **70-project-bindings (577):** preamble 45; Binding fragment 54; Laravel editable source 66; Serena context 321; Initial-prompt fragment 72.
- **75-serena-repl (803):** preamble 26; Discover and consume 236; Configuration semantics 176; Candidate LSP profile 225; Validate an authorized application 119.
- **80-agent-scoping (522):** preamble 34; Classes 108; Exact allowlists 251; Reachability and validation 117.
- **90-source-map (784):** preamble 69; Provider evidence 628; Runtime and hook owners 75.

**Duplication**

| Rule | Locations |
|---|---|
| Lane-local index init/sync | SKILL:33 ↔ 10:23 ↔ 40:49 |
| Rename/delete needs language-service references | SKILL:31 ↔ 40:47 ↔ 45 (edges heuristic) |
| `LSP` tool | SKILL:26 ↔ 40:51-55 ↔ 80:19 |
| Read with line range; `sed` only via shell | SKILL:28 ↔ 45:20 |
| Do not reread returned source | SKILL:31 ↔ 10:34 ↔ 45:20 |
| Config-change authority | SKILL:37 ↔ 50:27 (pointer only) ↔ 70:3 |
| CodeGraph → Serena → native order | 10:28 ↔ 40:3-7 |
| Skip absent Serena | 10:5,11 ↔ 40:7 ↔ 50:5 |
| Read-only MCP enforcement | 80:24 ↔ 40 Serena section ↔ PG 80:48 and PG 11:63 |
| Routing pointer, not a copied table | 70:25 ↔ 70:39 |

**90-source-map** is provenance plus freshness. Lines 3, 14-15 hold dated local observations from 2026-11-15. It is routed for "change a … claim" (topic-map:16) and cited at 10:13, 40:3, 70:45 and 75:19.

**Hooks and outside readers**
- No script or hook in the repository reads a CIR file.
- The user-level `~/.claude/hooks/codegraph-nudge.py` embeds text that mirrors the Operation card but opens only its own state file (102, 107).
- 50-hooks:57 says to "change … the checker together"; no such checker exists in the repo.
- Outside scripts depend only on the skill directory name (check_agent_grants.py:42).

## 7. LN duplication

| LN location | Other location |
|---|---|
| SKILL:23 (watchdog, no narration) | cc and codex delegation-prompts.md:36 |
| SKILL:49 (one-line opening/update; unattended lane none) | PG 43:170 |
| SKILL:53 (reader saw no tool call) | PG 43:172 |
| SKILL:30-34 (search, slice, capture) | LN noise-control-patterns:18-36,66-73 |
| SKILL:31 (re-read only for a new reason) | CIR SKILL:31; CIR 10:34 |
| SKILL:34 (capture bulky output) | alaa-testing-strategy/references/110-execution-resources.md:67-69 (artifact directory) |
| workflow-integration:7-18 (ownership) | SKILL:10,20,73; alaa-workflow/references/companion-routing.md:9 |
| workflow-integration:41 (children never return transcripts/diffs/logs) | cc SKILL.md:86; codex SKILL.md:84 |
| workflow-integration:45 (polarity) | PG 06:75-77 |
| model-output-profiles:20-23 (ownership) | SKILL:66; 90-source-map:180 |
| model-output-profiles:23 (effort is not verbosity) | PG 50:11 |
| model-output-profiles:27-28 (keep checks/gates) | PG SKILL:57; PG 80:55 |
| 90-source-map:41-46 (standing policy) | SKILL:16-18 |
| 90-source-map:24 and 59 (developers.openai.com/codex/skills) | PG 00-source-map:16 calls that URL stale |

## 8. History, incidents and dates in agent-facing files

| File:lines | Content | ~Words |
|---|---|---|
| PG 00-source-map:36-69 | Dated refresh log | 650 |
| PG 41:7-19, 47, 66, 72, 74-79, 116, 118, 145, 147, 165, 173, 181-183, 192, 209-211 | Dated verification, removed variable, "earlier documentation", user-observed incident | 2,000 |
| PG 11:13, 23, 58, 61, 65, 69, 109, 142-144 | Dated; "retired Windows host" | 770 |
| PG 80:22, 98, 132-136 | Dated; issue 14161/PR 14806 | 300 |
| PG 06:9, 121, 137 | Bug report, dates | 150 |
| PG 12:48-79 | Dated verification paragraphs | 250 |
| PG 21:23-34 / 31:65, 76-78 / 36:28, 32 / 42:39-48 / 43:56-64 | Refresh notes | 400 |
| PG 90:13, 17, 49 | "became history on 14 November 2026", served-asset note | 120 |
| PG 10, 20, 30, 35, 40, 42 | Whole files historical | 7,801 |
| PG 60:173; 70:20, 115; 61:51 | Dates | 200 |
| CIR 90-source-map:3, 14-15; 50-hooks:49 (one-week replay, 140k→37k characters) | Observations | 350 |
| CIR 40:49 (unreleased viewer) | — | ~10 |
| LN | None found beyond generic freshness text | — |

## Not determined

- Whether `check_fleet_references.py` has a baseline that suppresses citations into these skills. It reads a `--baseline` file; I did not inspect `check_fleet_references`' baseline, and the `check_skill_index` baseline does not name these skills.
- Section word counts are awk approximations and include table and fence text.
- I did not read 10/20/30/40 in full; their repeated-statement overlap is judged from openings and sentence matching only.
- PG 35-haiku-4-5:3 cites a "legacy-replacement rule in `assets/claude-model-policy.json` notes". The notes contain no rule by that name, only "Historical capability entries cannot authorize active selection".
