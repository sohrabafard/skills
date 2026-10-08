"""One-shot Phase 5 source update; authoring record, not a runtime dependency."""
from pathlib import Path
import copy
import importlib.util
import json
import re
import tomllib

ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / 'skills/sohrab'
PG = PACK / 'alaa-prompting-guide'
CC = PACK / 'alaa-cc-orchestrator'
CX = PACK / 'alaa-codex-orchestrator'
ARCHIVE = Path(__file__).parent

def read(p): return p.read_text(encoding='utf-8')
def write(p, text):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8', newline='\n')
def save(p, data): write(p, json.dumps(data, indent=2, ensure_ascii=False)+'\n')
def replace(p, old, new):
    text = read(p)
    if old not in text: raise ValueError(f'missing replacement in {p}: {old[:90]}')
    write(p, text.replace(old,new))
def module(path, name):
    spec = importlib.util.spec_from_file_location(name,path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

exception = ('Only documented applicable high-effort workhorse inadequacy for the same remaining problem, '
             'after correcting context, specification and tools and considering decomposition, or explicit user model selection. '
             'Complexity, sensitivity, file count, failure count and imagined insufficiency alone do not qualify. '
             'Reuse applicable prior evidence; no mandatory trial ladder, synthetic benchmark or replay of completed work.')
choices = {
    CC: [('alaa-implementer','claude-sonnet-5-5','medium','Bounded settled implementation with precise scope and checks.'),
         ('alaa-implementer-sonnet-high','claude-sonnet-5-5','high','Harder or longer implementation whose design is settled.'),
         ('alaa-implementer-opus','claude-opus-5-5','medium','Moderate unresolved engineering judgment.'),
         ('alaa-implementer-opus-high','claude-opus-5-5','high','Interacting unresolved design decisions and demanding system reasoning.'),
         ('alaa-implementer-fable','claude-fable-5-1','high',exception.replace('high-effort workhorse','Opus-high'))],
    CX: [('alaa-implementer-luna','gpt-6-luna','high','Narrow mechanical, repeatable implementation with readily checked outcomes.'),
         ('alaa-implementer','gpt-6.1-sol','medium','Normal engineering with grounded scope and acceptance criteria.'),
         ('alaa-implementer-high','gpt-6.1-sol','high','Substantial interacting engineering reasoning.'),
         ('alaa-implementer-astra','gpt-6-astra','high',exception.replace('high-effort workhorse','Sol-high'))],
}
draft = '\n## Phase 5 draft: direct plan-based profiles\n\n' + exception + '\n\n'
draft += ('Classify missing facts for retrieval or clarification before planning. Use the strong workhorse medium '
          'when planning constraints are clear, high when making the plan requires resolving interacting uncertainties. '
          'A costly plan can produce cheap implementation lanes. The lead uses verified compatible controls inline or '
          'dispatches the real read-only planner profile; it ratifies and persists advisory drafts. '
          'Record outcome, scope, settled/open decisions, failure/invariant reasoning, exact registered profile and reason '
          'before dispatch. Custom metadata pins are real; prose and ignored overrides cannot switch the runtime.\n\n')
draft += '\n'.join(f'{root.name}: {name}: {reason}' for root, rows in choices.items() for name,_,_,reason in rows)+'\n'
write(ARCHIVE/'instruction-drafts.md', read(ARCHIVE/'instruction-drafts.md')+draft)

for root, policyname in ((CC,'claude-model-policy.json'),(CX,'codex-model-policy.json')):
    policy = json.loads(read(PG/'assets'/policyname))
    policy['policy_version'] = '2.1.0' if root == CC else '1.2.0'
    policy['verified_on'] = '2026-10-08'
    if root == CX:
        policy['capability_evidence'] += ' Phase 5 official model and runtime guidance reverified on 2026-10-08; workload boundaries are unrun local hypotheses.'
    profiles=policy['profiles']
    for name, model, effort, reason in choices[root]:
        template = profiles.get(name) or profiles['alaa-implementer']
        profile=copy.deepcopy(template)
        profile.update(model=model, effort=effort, rationale=reason+' Unrun local starting hypothesis.', calibration_status='unrun')
        if root == CC:
            model_template=profiles['alaa-implementer'] if 'sonnet' in model else profiles['alaa-implementer-opus'] if 'opus' in model else profiles['alaa-implementer-fable']
            profile['availability']=copy.deepcopy(model_template['availability'])
            profile['source_ids']=model_template['source_ids'][:]
            profile['artifacts']=[f'skills/sohrab/{root.name}/agents/{name}.md']
            profile['escalation_criterion']=exception.replace('high-effort workhorse','Opus-high') if name.endswith('fable') else 'Reassess remaining work at material-scope or fix-follow-up boundaries; use the registered direct-selection route and preserve admission evidence.'
        profiles[name]=profile
    planner_model='claude-opus-5-5' if root==CC else 'gpt-6.1-sol'
    for name, effort, reason in [('main-deep','high','Demanding planning with interacting uncertainties.'),('alaa-planner','medium','Advisory read-only plan when scope, contracts and constraints are clear.'),('alaa-planner-high','high','Advisory read-only plan requiring resolution of interacting uncertainties.')]:
        profile=copy.deepcopy(profiles['main'] if root==CC else profiles.get(name,profiles['main']))
        profile.update(model=planner_model,effort=effort,rationale=reason+' Parent ratifies and owns the durable plan; unrun hypothesis.',calibration_status='unrun')
        if root==CC:
            profile['kind']='policy-only' if name=='main-deep' else 'agent'
            profile['artifacts']=[] if name=='main-deep' else [f'skills/sohrab/{root.name}/agents/{name}.md']
            profile['escalation_criterion']='Missing facts go to retrieval or clarification; planning effort follows actual interacting judgment, independently of implementation effort.'
        profiles[name]=profile
    save(PG/'assets'/policyname,policy)

# Shared editable bodies preserve baseline authority, verification and identity.
identity_start = 'Report metadata after the verdict/status or opening outcome:'
for root in (CC,CX):
    if root==CC:
        native=module(root/'scripts/check_agent_grants.py','cc_grants_for_authoring')
        old=read(root/'agents/alaa-implementer.md')
        body=old.split('\n---\n',1)[1].lstrip('\n')
        metadata=native.frontmatter(str(root/'agents/alaa-implementer.md'))
        planner_metadata=native.frontmatter(str(root/'agents/alaa-spec-analyst.md'))
        metadata={k:v for k,v in metadata.items() if k not in {'name','model','effort'}}
        planner_metadata={k:v for k,v in planner_metadata.items() if k not in {'name','model','effort'}}
    else:
        data=tomllib.loads(read(root/'agents/alaa-implementer.toml'))
        body=data['developer_instructions']
        metadata={'description':data['description'],'sandbox_mode':data['sandbox_mode']}
        planner_metadata={'description':'','sandbox_mode':'read-only'}
    body=body.replace('Run only supplied or repository-established focused commands','Run only supplied focused commands')
    oldline=next(line for line in body.splitlines() if line.startswith('Apply the role-selection reason'))
    body=body.replace(oldline, ('Apply the exact registered profile and selection reason recorded in the ratified plan under /'+root.name+' references/routing-matrix.md. '
        'Verify actual configured controls and narrower effective authority; do not assume prose or a caller override changed pinned controls. '
        'If design reasoning is required, inspect contracts, call sites and failure invariants, compare viable alternatives and record deciding evidence and discriminating checks. '
        'If a substantive decision is unrecorded or new evidence invalidates the selected profile, pause dependent work and return it to the parent for reassessment; do not self-upgrade. '
        'Exceptional admission requires applicable high-effort workhorse inadequacy or explicit user selection, as recorded by the parent; complexity alone is insufficient.'))
    write(root/'assets/implementation-contract.md',body)
    identity=body[body.index(identity_start):body.index('Output contract:')]
    runtime=('Runtime: you are a Claude Code subagent. Use Bash only for authorized read-only inspection.\n\n' if root==CC else '')
    planner=runtime+('You are a read-only planning advisor under an orchestrating parent. Return an advisory draft; the parent ratifies and owns the durable plan. Never edit files, implement, write tests, commit or install.\n\n'
        'Ground the requested outcome in current repository truth. Separate missing facts (retrieve or report for clarification) from interacting design judgment. Do not invent product decisions or infer absent constraints. Inspect applicable instructions, owners, contracts, call sites and focused verification boundaries before proposing lanes.\n\n'
        'Use the recorded registered planning profile. Medium planning applies to clear scope, contracts and constraints; high applies when making the plan requires resolving interacting uncertainties. Planning cost does not set implementation cost: a demanding plan may yield mechanical or settled lanes. Report incompatible configured controls to the parent; prose cannot change model or effort.\n\n'
        'For each proposed lane record outcome, owned scope, exclusions, dependencies, settled versus open decisions, failure/invariant reasoning, exact registered implementation profile and selection reason using /'+root.name+' references/routing-matrix.md. Exceptional implementation requires applicable documented high-effort workhorse inadequacy after correcting context/specification/tools and considering decomposition, or explicit user selection. No speculative complexity admission, mandatory trial ladder, synthetic benchmark or replay of completed work. Reuse applicable prior evidence. Preserve independent gates and one writer per scope.\n\n'
        'Return unresolved user decisions with options and consequences. Declare retrieval and capability limits. Run no broad verification; any authorized inspection is evidence, never independent implementation acceptance.\n\n')+identity+('Output contract:\n1. Outcome, acceptance criteria and repository evidence.\n2. Advisory plan with lane records and proposed exact profiles.\n3. Decisions, alternatives, invariants and reasoning supporting selections.\n4. Required independent gates and uncovered checks, consolidated without duplicate execution.\n5. Unknowns, user decisions, blockers and unrun limits.\n\nReturn a bounded report with evidence paths; no transcript or raw log. Keep it under 40 lines.\n')
    write(root/'assets/planner-contract.md',planner)
    wrappers={}
    for name,_,_,reason in choices[root]:
        meta=copy.deepcopy(metadata)
        meta['description']=reason+' Scoped implementation; admission in /'+root.name+' references/routing-matrix.md. Never self-review or widen scope.'
        wrappers[name]={'contract':'assets/implementation-contract.md','metadata':meta}
    for name,reason in [('alaa-planner','Advisory read-only planner for clear scope, contracts and constraints.'),('alaa-planner-high','Advisory read-only planner for interacting uncertainties that must be resolved to form the plan.')]:
        meta=copy.deepcopy(planner_metadata);meta['description']=reason+' Parent ratifies and owns the durable plan; never implements or edits.'
        wrappers[name]={'contract':'assets/planner-contract.md','metadata':meta}
    save(root/'assets/profile-wrappers.json',{'profiles':wrappers})
    write(root/'VERSION','5.1.0\n')
    changelog=read(root/'CHANGELOG.md')
    write(root/'CHANGELOG.md',changelog.split('\n',1)[0]+'\n\n## 5.1.0 - 2026-10-08\n\n- Select implementation profiles directly from a grounded plan, with real medium/high workhorse and read-only planner variants.\n- Exceptional implementation requires applicable high-workhorse inadequacy or explicit user selection; no speculative complexity promotion or trial ladder.\n- Render implementation/planner variants from shared contracts and canonical pins; preserve reviewer generation and consolidated independent gates.\n'+changelog.split('\n',1)[1])

replace(PG/'scripts/claude_model_policy.py','implementer-opus implementer-fable','implementer-opus implementer-fable implementer-sonnet-high implementer-opus-high planner planner-high')
replace(PG/'scripts/claude_model_policy.py','set(ARTIFACTS) | {"main"}','set(ARTIFACTS) | {"main", "main-deep"}')
replace(PG/'scripts/claude_model_policy.py','exactly main and 24 managed agent profiles required','exactly main/main-deep and 28 managed agent profiles required')
replace(PG/'scripts/claude_model_policy.py','role == "main"','role in {"main", "main-deep"}')

# Extend reviewer generation, retaining its codec and semantic drift tests.
replace(CX/'scripts/render_agents.py','ROOT = Path(__file__).resolve().parent.parent','ROOT = Path(__file__).resolve().parent.parent\nsys.path.insert(0, str(ROOT.parent / "alaa-prompting-guide" / "scripts"))\nfrom profile_projection import expected_profiles, profile_text')
replace(CX/'scripts/render_agents.py','    agents = {path: path.read_bytes()', '    wrappers.update(expected_profiles(root, policy, "toml"))\n    agents = {path: path.read_bytes()')
replace(CX/'scripts/render_agents.py','        outputs = expected_outputs(root, policy)','        (root / "assets/profile-wrappers.json").write_text(\'{"profiles": {}}\\n\', encoding="utf-8")\n        outputs = expected_outputs(root, policy)')
replace(CX/'scripts/render_agents.py','    if evidence_dir is not None:\n        # Keep', '    parsed = _toml.loads(profile_text("toml", "alaa-implementer",\n        {"description": "fixture", "sandbox_mode": "workspace-write"}, tricky,\n        policy["profiles"]["alaa-implementer"], "assets/implementation-contract.md"))\n    assert parsed["developer_instructions"] == tricky, "profile codec must preserve contract"\n    if evidence_dir is not None:\n        # Keep')
for root in (CC,CX):
    extra=[n for n,_,_,_ in choices[root] if not (root/'agents'/(n+('.md' if root==CC else '.toml'))).exists()]+['alaa-planner','alaa-planner-high']
    replace(root/'scripts/validate_pack.py','REQUIRED = {','REQUIRED = {\n'+''.join(f'    "{n}",\n' for n in extra))
    replace(root/'scripts/check_agent_contracts.py',f'len(roles) != {3 if root==CC else 2}',f'len(roles) != {5 if root==CC else 4}')
    replace(root/'scripts/check_agent_contracts.py','expected all three implementer variants' if root==CC else 'expected both implementer variants','expected all registered implementer variants')
    if root==CC:
        replace(root/'scripts/check_agent_grants.py','EXPECTED_NATIVE = {name: READ_NATIVE for name in EXPECTED_MCP}',
            'EXPECTED_MCP.update({"alaa-implementer-sonnet-high": None, "alaa-implementer-opus-high": None,\n                     "alaa-planner": EXPECTED_MCP["alaa-spec-analyst"],\n                     "alaa-planner-high": EXPECTED_MCP["alaa-spec-analyst"]})\nEXPECTED_NATIVE = {name: READ_NATIVE for name in EXPECTED_MCP}')
    else:
        replace(root/'scripts/check_agent_grants.py','ROLE_POLICY["alaa-reviewer-deep"] = ROLE_POLICY["alaa-reviewer"]',
            'ROLE_POLICY["alaa-reviewer-deep"] = ROLE_POLICY["alaa-reviewer"]\nfor name in ("alaa-implementer-luna", "alaa-implementer-high"):\n    ROLE_POLICY[name] = ROLE_POLICY["alaa-implementer"]\nfor name in ("alaa-planner", "alaa-planner-high"):\n    ROLE_POLICY[name] = ROLE_POLICY["alaa-spec-analyst"]')

# One aggregate owns renderer drift, preserving existing child exit checks.
replace(CC/'scripts/validate_pack.py','from check_agent_grants import frontmatter','from check_agent_grants import frontmatter\nfrom render_agents import drift, expected_outputs, load_policy, OWNER')
replace(CC/'scripts/validate_pack.py','    unavailable = False','    errors.extend(f"generated drift: {path.relative_to(ROOT)}" for path in\n                  drift(expected_outputs(ROOT, load_policy(OWNER / "assets/claude-model-policy.json"))))\n    unavailable = False')

planning = ('Separate missing facts (retrieve or clarify) from coupled design judgment before planning. '
    'Use `alaa-planner` when scope, contracts and constraints are clear, or `alaa-planner-high` when formulating the plan requires resolving interacting uncertainties. '
    'The lead may plan inline only after verifying compatible configured controls from the canonical planning profile; otherwise dispatch the real registered planner. '
    'Planner drafts are advisory: the lead ratifies and persists the durable plan. Planning effort is independent of implementation effort; high planning may yield cheap implementation. '
    'The ratified plan records every lane\'s outcome, owned scope, exclusions, dependencies, settled/open decisions, failure/invariant reasoning, exact registered profile and selection reason before implementation dispatch. '
    'Do not pretend prose switches controls or use a caller override that a custom profile ignores.')
for root in (CC,CX):
    normal=choices[root][:-1]
    strong=choices[root][-1][0]
    workhorse='Opus-high' if root==CC else 'Sol-high'
    routing=('## Planning profile selection\n\n'+planning+'\n\n## Implementation routing\n\n'
        'Choose directly from the completed lane record; no mandatory sequence of attempts. Exact model/effort pins belong only to `/alaa-prompting-guide`; these role contracts classify work.\n\n')
    routing+='\n'.join(f'- `{name}`: {reason}' for name,_,_,reason in normal)+'\n\n'
    routing+=f'Use `{strong}` only for '+exception.replace('high-effort workhorse',workhorse)+'\n\n'
    routing+=('Record the actual profile and reason before dispatch. For exceptional admission record the applicable '+workhorse+' result, the remaining inadequacy, corrections and decomposition consideration, or the explicit user direction. '
        'An unresolved decision alone selects an appropriate workhorse profile, never exceptional implementation. Missing facts, unavailable tools and product intent return to their owners.\n\n'
        'Reassess remaining work only at existing initial-assignment, material-scope-change and fix-follow-up boundaries. Continue while the same reason applies; do not switch during a command or ordinary progress update. Before replacing a writer, retire its assignment and reconcile surviving edits/checkpoint. Hand off remaining scope, acceptance criteria and evidence; preserve independent gates, never overlap writers or replay completed work.\n\n'
        'Read `model-effort-policy.md` before profile changes.\n\n')
    p=root/'references/routing-matrix.md';text=read(p)
    start=text.index('## Implementation routing');end=text.index('## Correctness review depth',start)
    write(p,text[:start]+routing+text[end:])
    p=root/'references/agent-catalog.md';text=read(p)
    text=re.sub(r'Twenty[^\n]+(?:available|available\.)', 'Twenty-seven executable agents are available.',text)
    rows=['| `alaa-planner` | read-only | Advisory plan with clear contracts and constraints | Editing or owning the durable plan |',
          '| `alaa-planner-high` | read-only | Advisory plan resolving interacting uncertainties | Editing or owning the durable plan |']
    insert=text.index('\n\n## Implementation and verification')
    text=text[:insert]+'\n'+'\n'.join(rows)+text[insert:]
    for name,_,_,reason in choices[root]:
        row=f'| `{name}` | workspace-write | {reason} | Self-review or unrecorded profile admission |'
        pattern=rf'^\| `{name}` \|.*$'
        if re.search(pattern,text,re.M): text=re.sub(pattern,lambda _:row,text,flags=re.M)
        else:
            pos=text.index('| `alaa-verifier`');text=text[:pos]+row+'\n'+text[pos:]
    write(p,text)
    for relative in ('SKILL.md','references/verification-and-gates.md'):
        p=root/relative;text=read(p)
        # Add the routed prerequisite without replacing existing lifecycle authority.
        heading='## Plan-first profile selection\n\n'+planning+' Read `references/routing-matrix.md` for implementation admission.\n\n'
        at=text.index('\n## ',text.index('\n---\n')+5) if relative=='SKILL.md' else text.index('\n## ')
        write(p,text[:at]+'\n'+heading+text[at:])
    for relative in ('references/delegation-prompts/30-implementation.md','references/delegation-prompts/90-completion/20-review-followup.md'):
        p=root/relative;text=read(p)
        text=re.sub(r'<role_selection>.*?</role_selection>', '<role_selection><exact registered profile from ratified plan; outcome/scope; settled and open decisions; failure/invariant reasoning; selection reason; exceptional admission: applicable high-workhorse inadequacy with context/spec/tool corrections and decomposition consideration, or explicit user direction></role_selection>',text)
        text=re.sub(r'Use `routing-matrix.md` to select[^\n]+', 'Use `routing-matrix.md` to select directly from the ratified lane record. Pass the same bounded lane block to the real registered variant; caller fields or prose do not override custom pins. Preserve surviving work; no trial ladder or replay of completed work.',text)
        write(p,text)

replace(PG/'references/90-model-selection.md', '5. **Codex only:** **Default down when pinning.**', '5. **Select directly from the grounded plan.**')
p=PG/'references/90-model-selection.md';text=read(p)
start=text.index('5. **Select directly');end=text.index('6. **Match delegation',start)
write(p,text[:start]+('5. **Select directly from the grounded plan.** Read the runtime orchestrator routing matrix, then the exact canonical profile. Classify missing facts for retrieval/clarification before planning. Planning uses strong-workhorse medium/high based on the judgment needed to make the plan; high planning can produce cheap implementation. Ordinary and demanding implementation use their registered workhorse variants. Exceptional implementation requires applicable high-effort workhorse inadequacy after correcting context/specification/tools and considering decomposition, or explicit user direction; complexity or sensitivity alone is insufficient. Reuse applicable prior evidence without a mandatory trial ladder, synthetic benchmark or replay. Record the exact profile and reason before dispatch.\n6. **Verify actual controls.** Inline planning requires verified compatible configured controls; otherwise use a registered read-only planner. Pinned custom profiles can override caller controls; prose cannot change the running model. The parent ratifies and owns the durable plan.\n'+text[end:].replace('6. **Match','7. **Match',1).replace('7. **Use','8. **Use',1).replace('8. **Route','9. **Route',1)))
p=PG/'references/50-effort-and-thinking.md';text=read(p)
start=text.index('1. **Classify the judgment.');end=text.index('## Codex profiles and exceptions',start)
write(p,text[:start]+('1. **Classify missing facts before judgment.** Retrieve or clarify absent context, tool capability or product intent; a stronger model does not supply missing evidence.\n'
    '2. **Plan with the appropriate strong-workhorse profile.** Clear scope/contracts/constraints fit medium planning; resolving interacting uncertainties to form the plan fits high. Use verified compatible lead controls or a real read-only planner.\n'
    '3. **Select implementation directly from the completed plan.** Record outcome, scope, settled/open decisions, failure/invariant reasoning and exact registered profile/reason. Planning effort and implementation effort are independent. Runtime routing matrices own workload admission; canonical policies own pins.\n'
    '4. **Reserve exceptional implementation for evidence or explicit direction.** Require applicable high-effort workhorse inadequacy after correcting context/specification/tools and considering decomposition, or explicit user selection. Complexity, sensitivity, file/failure count and imagined insufficiency alone do not qualify. Prior applicable evidence may suffice; no trial ladder, synthetic benchmark or replay is required.\n'
    '5. **Keep selection and calibration separate.** Controlled comparisons vary one factor at a time with task/context/tools/acceptance held constant; compare cost only among passing runs. Local profile rationales remain unrun until measured. A task selection does not require a new experiment.\n'
    '6. **Realize the actual controls.** Verify runtime availability, caps and override precedence. A custom profile may ignore caller model/effort; prose never changes the running configuration. Reassess only at existing material-scope/fix-follow-up boundaries and preserve completed work and independent gates.\n\n')+text[end:])
for relative,root in [('11-codex-runtime-features.md',CX),('41-claude-code-runtime-features.md',CC)]:
    p=PG/'references'/relative
    write(p,read(p)+'\n## Managed direct-selection profiles\n\nThe runtime orchestrator renders standalone implementation and planner variants from one editable contract per role family. `scripts/render_agents.py --write` supplies pins only from this skill\'s canonical policy; `--check` rejects drift. Select the exact registered variant, not a caller effort override that custom metadata ignores. Planning inline requires verified compatible configured controls; a planner draft remains advisory and the parent owns the durable plan. '+('Custom-agent TOML model and model_reasoning_effort pins override caller settings.' if root==CX else 'Subagent YAML model and effort realize the selected pair; environment settings and effort caps may override them. No per-call Agent effort override is assumed without current supported-interface evidence.')+' Static agreement proves source configuration, not runtime identity or model obedience.\n')

write(ROOT/'install-skills.md',read(ROOT/'install-skills.md')+'\n## Managed implementation and planning profiles\n\nBefore an authorized installation, generate and validate each affected orchestrator\'s standalone wrappers with its `scripts/render_agents.py --write` and aggregate validator. Edit `assets/implementation-contract.md`, `assets/planner-contract.md` or wrapper metadata, never generated bodies; model/effort pins come only from `/alaa-prompting-guide`. Existing reviewer rendering remains managed. Register all new implementation/planner files through the existing install procedure; source generation is not installation. Confirm actual host availability, configured controls, override precedence and grants before dispatch. A requested profile that cannot be realized blocks; do not silently substitute a model or effort.\n')
print('Source contracts, canonical profiles, routing and inventories updated; renderer generation remains.')
