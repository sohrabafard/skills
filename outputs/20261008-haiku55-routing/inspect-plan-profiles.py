"""Focused source inspection only; does not discharge independent acceptance."""
from pathlib import Path
import ast
import importlib.util
import json
import subprocess
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / 'skills/sohrab'
PG = PACK / 'alaa-prompting-guide'
sys.path.insert(0,str(PG/'scripts'))
from profile_projection import expected_profiles, profile_text

def module(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    value=importlib.util.module_from_spec(spec);spec.loader.exec_module(value);return value

errors=[]; evidence={}; ast_paths=[]
for kind, filename in [('cc','claude-model-policy.json'),('codex','codex-model-policy.json')]:
    root=PACK/f'alaa-{kind}-orchestrator';policy=json.loads((PG/'assets'/filename).read_text(encoding='utf-8'))
    api=module(PG/'scripts'/('claude_model_policy.py' if kind=='cc' else 'codex_model_policy.py'),f'{kind}_policy_inspection')
    errors.extend(api.validate_policy(policy))
    suffix='md' if kind=='cc' else 'toml'; pins={}
    if kind=='cc':
        grants=module(root/'scripts/check_agent_grants.py','cc_grants_inspection')
    for path in sorted((root/'agents').glob('*.'+suffix)):
        data=grants.frontmatter(str(path)) if kind=='cc' else tomllib.loads(path.read_text(encoding='utf-8'))
        pair={'model':data['model'],'effort':data['effort' if kind=='cc' else 'model_reasoning_effort']}
        target=policy['profiles'][path.stem]
        if pair!={k:target[k] for k in ('model','effort')}:errors.append(f'{kind}: mismatched pin {path.stem}')
        pins[path.stem]=pair
        if 'haiku-4-5' in pair['model'] or pair['model']=='gpt-6-sol':errors.append(f'{kind}: prohibited active pin {path.stem}')
    expected_agents=28 if kind=='cc' else 27
    if len(pins)!=expected_agents:errors.append(f'{kind}: expected {expected_agents} executable agents, observed {len(pins)}')
    expected_profiles_count=31 if kind=='cc' else 30
    if len(policy['profiles'])!=expected_profiles_count:errors.append(f'{kind}: expected {expected_profiles_count} canonical profiles')
    if kind=='codex':
        luna=policy['profiles']['alaa-implementer-luna']
        if (luna['model'],luna['effort'])!=('gpt-6-luna','medium'):errors.append('mechanical Luna requires canonical medium pin')
        if 'Automatic mechanical implementation' not in luna['rationale'] or 'finite explicitly enumerated' not in luna['rationale']:errors.append('automatic mechanical admission rationale missing')
        retired=ROOT/'_to_delete/20261008-planfirst-no-luna-implementation/alaa-implementer-luna.toml'
        if retired.stat().st_size!=6240:errors.append('historical high-copy size changed')
    outputs=expected_profiles(root,policy,'yaml' if kind=='cc' else 'toml')
    for path,data in outputs.items():
        if path.read_bytes()!=data:errors.append(f'{kind}: generated profile drift {path.stem}')
    manifest=json.loads((root/'assets/manifest.json').read_text(encoding='utf-8'))
    import hashlib
    for record in manifest['managed_agents']:
        if hashlib.sha256((root/record['file']).read_bytes()).hexdigest()!=record['sha256']:errors.append(f'{kind}: manifest drift {record["name"]}')
    specification=json.loads((root/'assets/profile-wrappers.json').read_text(encoding='utf-8'))
    for name,entry in specification['profiles'].items():
        if {'model','effort','model_reasoning_effort'} & entry['metadata'].keys():errors.append(f'{kind}: duplicate pin owner')
        body=(root/entry['contract']).read_text(encoding='utf-8')
        if kind=='codex' and tomllib.loads((root/'agents'/(name+'.toml')).read_text(encoding='utf-8'))['developer_instructions']!=body:errors.append(f'{kind}: contract codec drift')
    evidence[kind]={'executable_pins':pins,'canonical_profiles':{n:{k:p[k] for k in ('model','effort')} for n,p in policy['profiles'].items()},'generated_profile_count':len(outputs),'calibration_statuses':sorted({p['calibration_status'] for p in policy['profiles'].values()})}
    ast_paths.extend(root/'scripts'/p for p in ['check_agent_contracts.py','check_agent_grants.py','validate_pack.py','render_agents.py'])
ast_paths.extend(PG/'scripts'/p for p in ['claude_model_policy.py','profile_projection.py'])
for path in ast_paths:ast.parse(path.read_text(encoding='utf-8'),filename=str(path))
evidence['python_ast']=[p.relative_to(ROOT).as_posix() for p in ast_paths]
diff=subprocess.run(['git','-c','core.safecrlf=false','diff','--check'],cwd=ROOT,capture_output=True,text=True)
if diff.returncode:errors.append('git diff --check: '+diff.stdout+diff.stderr)
evidence['git_diff_check']={'exit':diff.returncode,'output':diff.stdout+diff.stderr}
evidence['route_cases']='plan-first-routing-cases.md; independent semantic assessment remains unrun by writer'
evidence['limits']='Static projection/AST inspection only; no live models, activation, installation, broad fixtures or independent acceptance.'
evidence['errors']=errors
path=Path(__file__).with_name('focused-inspection.json')
existing=json.loads(path.read_text(encoding='utf-8'));existing['phase7']=evidence
path.write_text(json.dumps(existing,indent=2)+'\n',encoding='utf-8',newline='\n')
print(('PASS' if not errors else 'FINDINGS')+f': canonical/native pins, shared contracts, manifests, {len(ast_paths)} Python ASTs and diff whitespace; '+str(len(errors))+' findings')
for item in errors:print(item)
raise SystemExit(bool(errors))
