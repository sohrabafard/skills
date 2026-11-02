"""Scoped structural contract and scenario-corpus checker, not a model evaluator.

Exit 0 clean, 1 findings, 2 unavailable input. Linear in selected source/corpus
bytes and local references. Semantic execution/grading belongs to fresh probes
and independent reviewers; no fixture outcome is labelled model execution.
"""
import argparse
import copy
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = 'outputs/20261012-capability-recall/'
MEMORY = 'skills/sohrab/alaa-memory-os/'
LESSONS = 'skills/sohrab/alaa-extract-agent-lessons/'
REQUIRED = {'gateway','reuse','repair_owner','query_fields','page_miss','followup','late','empty','denied','unavailable','timeout','ordinary_timeout','stale','irrelevant','registry','partial','positive','incompatible','unauthorized','actual_failure','exhausted','native_threshold','missing_adapter','write_pending','source_owned','lesson_reusable','lesson_duplicate','lesson_oneoff','lesson_unsupported','lesson_sensitive','lesson_local','lesson_deferred','workflow','drift'}

def corpus_findings(inputs, oracle):
    if not isinstance(inputs,dict) or not isinstance(oracle,dict):
        raise ValueError('corpus root must be an object')
    findings = []
    scenarios = inputs.get('scenarios', [])
    cases = oracle.get('cases', [])
    if not isinstance(scenarios,list) or not isinstance(cases,list) or not all(isinstance(row,dict) for row in scenarios+cases):
        raise ValueError('corpus rows must be objects in arrays')
    ids = [item.get('id') for item in scenarios]
    oracle_ids = [item.get('id') for item in cases]
    if inputs.get('schema_version') != 1 or oracle.get('schema_version') != 1:
        findings.append('unsupported corpus schema')
    if len(ids) != len(set(ids)) or set(ids) != REQUIRED:
        findings.append('missing, duplicate or unexpected input IDs')
    if len(oracle_ids) != len(set(oracle_ids)) or set(oracle_ids) != set(ids):
        findings.append('oracle/input IDs disagree')
    for item in scenarios:
        if set(item) != {'id','context','request'} or not all(isinstance(item.get(k),str) and item[k].strip() for k in ['id','context','request']):
            findings.append('input contains an oracle field or empty scenario')
    coverage = set()
    for case in cases:
        requirements = case.get('requirements', [])
        checks = case.get('checks', [])
        if not requirements or not isinstance(checks,list) or not checks or not all(isinstance(c,str) and c.strip() for c in checks):
            findings.append('oracle lacks requirements or discriminating checks')
        coverage.update(requirements)
    if coverage != {f'R{i}' for i in range(1,9)}:
        findings.append('oracle does not cover exactly R1-R8')
    return findings

def source_findings(sources):
    findings = []
    body = sources[MEMORY+'SKILL.md']
    declarations = re.findall(r'^ACTIVE_ADAPTER:\s*(\S+)\s*$',body,re.M)
    if len(declarations) != 1 or declarations[0] not in {'local','basic-memory','hindsight'}:
        return ['missing or ambiguous selected adapter']
    selected = MEMORY+'references/store-'+declarations[0]+'.md'
    if selected not in sources:
        findings.append('selected adapter missing')
    # Require owner reachability, not exact sentences: wording may be compressed.
    router = sources.get(MEMORY+'references/00-topic-map.md', '')
    if router and 'references/00-topic-map.md' not in body:
        findings.append('conditional router unreachable from body')
    reachable = body+'\n'+router
    for name in ['knowledge-shape.md','drift-management.md', 'store-'+declarations[0]+'.md']:
        if 'references/'+name not in reachable:
            findings.append('memory owner route missing: '+name)
    if not re.search(r'^## Recall\b',body,re.M):
        findings.append('recall policy owner section missing')
    adapter = sources.get(selected,'')
    if declarations[0] == 'hindsight':
        if 'references/hindsight-setup.md' not in adapter:
            findings.append('conditional Hindsight setup route missing')
        if re.search(r'\b(?:five|sixty)[ -]seconds?\b',adapter,re.I):
            findings.append('adapter duplicates policy budgets')
    for path,text in sources.items():
        if path.startswith(MEMORY) and path.endswith('.md'):
            for match in re.finditer(r'`(references/[\w-]+\.md)`',text):
                reference = match[1]
                if MEMORY+reference in sources:
                    continue
                # Named cross-skill citations may wrap onto the following line.
                paragraph = text[text.rfind('\n\n',0,match.start())+2:match.start()]
                owners = re.findall(r'alaa-[a-z0-9-]+',paragraph)
                if owners and (ROOT/'skills/sohrab'/owners[-1]/reference).is_file():
                    continue
                findings.append('unresolved local route: '+path+' -> '+reference)
    lesson = sources[LESSONS+'SKILL.md']
    if '/alaa-memory-os' not in lesson or 'references/context-curation.md' not in lesson:
        findings.append('lesson storage/timing owner unreachable')
    for filename in ['precompact_checkpoint.ps1','session_start_context.ps1']:
        text = sources[MEMORY+'scripts/'+filename]
        # Ignore comments; prohibit direct file APIs in addition to cmdlet writes.
        executable = '\n'.join(line for line in text.splitlines() if not line.lstrip().startswith('#'))
        if re.search(r'\b(?:New-Item|Set-Content|Add-Content|Out-File|Remove-Item|Move-Item|Copy-Item|Write-TextFileNoBom|WriteAllText|WriteAllBytes|AppendAllText|CreateDirectory)\b',executable,re.I):
            findings.append('hook writes: '+filename)
        if filename == 'precompact_checkpoint.ps1' and re.search(r'\b(?:ReadToEnd|ReadAllText|ReadAllBytes|ReadAllLines|ReadLines|OpenRead|Get-Content|Get-ChildItem|Resolve-VaultRoot|transcript_path)\b',executable,re.I):
            findings.append('PreCompact reads payload, transcript or vault')
        if filename == 'session_start_context.ps1' and re.search(r'five.second|search memory first',text,re.I):
            findings.append('SessionStart duplicates recall policy')
    return findings

def load_sources():
    paths = list((ROOT/MEMORY).glob('*.md')) + list((ROOT/MEMORY/'references').glob('*.md'))
    paths += [ROOT/LESSONS/'SKILL.md',ROOT/MEMORY/'scripts/precompact_checkpoint.ps1',ROOT/MEMORY/'scripts/session_start_context.ps1']
    return {p.relative_to(ROOT).as_posix():p.read_text(encoding='utf-8-sig') for p in paths}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test',action='store_true')
    args = parser.parse_args()
    inputs = json.loads((ROOT/ARTIFACT/'scenario-inputs.json').read_text(encoding='utf-8'))
    oracle = json.loads((ROOT/ARTIFACT/'scenario-oracle.json').read_text(encoding='utf-8'))
    sources = load_sources()
    findings = corpus_findings(inputs,oracle)+source_findings(sources)
    if findings:
        for finding in findings: print('FINDING: '+finding)
        return 1
    if args.self_test:
        mutations = json.loads((ROOT/ARTIFACT/'checker-red-fixtures.json').read_text(encoding='utf-8'))
        for fixture in mutations:
            i,o,s = copy.deepcopy(inputs),copy.deepcopy(oracle),dict(sources)
            name = fixture['mutation']
            if name == 'input_leak': i['scenarios'][0]['checks']=['secret oracle']
            elif name == 'input_duplicate': i['scenarios'][1]['id']=i['scenarios'][0]['id']
            elif name == 'input_missing': i['scenarios'].pop()
            elif name == 'oracle_orphan': o['cases'][0]['id']='orphan'
            elif name == 'oracle_empty': o['cases'][0]['checks']=[]
            elif name == 'coverage_missing':
                for case in o['cases']: case['requirements']=[r for r in case['requirements'] if r!='R8']
            elif name == 'adapter_missing': s.pop(MEMORY+'references/store-hindsight.md')
            elif name == 'adapter_duplicate': s[MEMORY+'SKILL.md']+='\nACTIVE_ADAPTER: local\n'
            elif name == 'router_unreachable': s[MEMORY+'SKILL.md']=s[MEMORY+'SKILL.md'].replace('references/00-topic-map.md','references/skill-boundaries.md')
            elif name == 'knowledge_route_missing':
                for path in [MEMORY+'SKILL.md', MEMORY+'references/00-topic-map.md']:
                    s[path]=s[path].replace('references/knowledge-shape.md','references/skill-boundaries.md')
            elif name == 'policy_owner_missing': s[MEMORY+'SKILL.md']=re.sub(r'^## Recall.*$', '## Other', s[MEMORY+'SKILL.md'], flags=re.M)
            elif name == 'setup_route_missing': s[MEMORY+'references/store-hindsight.md']=s[MEMORY+'references/store-hindsight.md'].replace('references/hindsight-setup.md','references/skill-boundaries.md')
            elif name == 'schema_wrong': i['schema_version']=9
            elif name == 'input_empty': i['scenarios'][0]['context']=''
            elif name == 'input_null_row': i['scenarios'][0]=None
            elif name == 'oracle_null_row': o['cases'][0]=None
            elif name == 'requirements_empty': o['cases'][0]['requirements']=[]
            elif name == 'route_dangling': s[MEMORY+'SKILL.md']+='\n`references/missing.md`\n'
            elif name == 'budget_copy': s[MEMORY+'references/store-hindsight.md']+='\nRecall has sixty seconds.\n'
            elif name == 'hook_write': s[MEMORY+'scripts/precompact_checkpoint.ps1']+="\n[IO.File]::WriteAllText('x','y')\n"
            elif name == 'session_write': s[MEMORY+'scripts/session_start_context.ps1']+="\n[IO.File]::WriteAllText('x','y')\n"
            elif name == 'hook_read': s[MEMORY+'scripts/precompact_checkpoint.ps1']+='\nGet-Content $transcript_path\n'
            elif name == 'hook_direct_read': s[MEMORY+'scripts/precompact_checkpoint.ps1']+="\n[IO.File]::ReadAllText('x')\n"
            elif name == 'hook_read_all_lines': s[MEMORY+'scripts/precompact_checkpoint.ps1']+="\n[IO.File]::ReadAllLines('x')\n"
            elif name == 'hook_policy_copy': s[MEMORY+'scripts/session_start_context.ps1']+='\nsearch memory first\n'
            elif name == 'lesson_owner_missing': s[LESSONS+'SKILL.md']=s[LESSONS+'SKILL.md'].replace('/alaa-memory-os','/unknown')
            elif name == 'lesson_timing_missing': s[LESSONS+'SKILL.md']=s[LESSONS+'SKILL.md'].replace('references/context-curation.md','references/other.md')
            else: raise ValueError('unknown red fixture mutation')
            try:
                result = corpus_findings(i,o)+source_findings(s)
            except ValueError:
                if fixture.get('expected_exit') == 2:
                    # Exercise the actual CLI error boundary without modifying
                    # repository inputs. Fault injection only replaces corpus
                    # reads in a fresh child, not source reads or checker logic.
                    snippet = '\n'.join([
                        'import json, runpy, sys',
                        'from pathlib import Path',
                        'original = Path.read_text',
                        'inputs = '+repr(json.dumps(i)),
                        'oracle = '+repr(json.dumps(o)),
                        'def injected(path, *args, **kwargs):',
                        "    if path.name == 'scenario-inputs.json': return inputs",
                        "    if path.name == 'scenario-oracle.json': return oracle",
                        '    return original(path, *args, **kwargs)',
                        'Path.read_text = injected',
                        'sys.argv = ['+repr(str(Path(__file__).resolve()))+']',
                        'runpy.run_path(sys.argv[0], run_name="__main__")',
                    ])
                    child = subprocess.run([sys.executable,'-c',snippet],capture_output=True,text=True,timeout=10)
                    if child.returncode != 2 or 'Traceback' in child.stderr:
                        print('FAIL: malformed corpus did not exit2 cleanly')
                        return 1
                    continue
                raise
            if not any(fixture['expected_finding'] in f for f in result):
                print('FAIL: undetected red fixture '+name)
                return 1
        print(f'PASS: {len(mutations)} negative fixtures rejected; static structure only')
    else:
        print(f'PASS: {len(inputs["scenarios"])} separated scenarios cover R1-R8; owner routes and nonwriting hook source checked; no model executed')
    return 0

if __name__ == '__main__':
    try: sys.exit(main())
    except (OSError,ValueError,KeyError,TypeError,subprocess.TimeoutExpired) as error:
        print('BLOCKED: '+type(error).__name__+' reading scoped checker inputs')
        sys.exit(2)
