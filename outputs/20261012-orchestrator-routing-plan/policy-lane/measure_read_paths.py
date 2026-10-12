from pathlib import Path
import json
import hashlib

OUT=Path('outputs/20261012-orchestrator-routing-plan/policy-lane')
PG='skills/sohrab/alaa-prompting-guide/'
common=[PG+'SKILL.md',PG+'references/00-topic-map.md',PG+'references/90-model-selection.md',PG+'references/50-effort-and-thinking.md',PG+'references/80-subagent-authoring.md',
 'skills/sohrab/alaa-low-noise/SKILL.md','skills/sohrab/alaa-low-noise/references/workflow-integration.md',
 'skills/sohrab/alaa-workflow/SKILL.md','skills/sohrab/alaa-workflow/references/artifact-lifecycle.md',
 'skills/sohrab/alaa-workflow/references/context-continuity.md','skills/sohrab/alaa-workflow/references/workspace-and-integration.md',
 'skills/sohrab/alaa-workflow/references/companion-routing.md']
routes={}
for runtime,name,suffix in [('codex','alaa-codex-orchestrator','toml'),('claude-code','alaa-cc-orchestrator','md')]:
 prefix='skills/sohrab/'+name+'/'
 profiles=json.loads(Path(prefix+'assets/profile-wrappers.json').read_text(encoding='utf-8'))['profiles']
 model=[PG+'references/'+('11-codex-runtime-features.md' if runtime=='codex' else '41-claude-code-runtime-features.md'),PG+'references/'+('12-gpt-6.md' if runtime=='codex' else '36-haiku-5-5.md')]
 shared=common+model+[prefix+x for x in ['SKILL.md','references/routing-matrix.md','references/model-effort-policy.md','references/agent-catalog.md','references/delegation-prompts.md','references/verification-and-gates.md']]
 for kind,template,role in [('planning','10-discovery.md','alaa-planner'),('mechanical-implementation','30-implementation.md','alaa-implementer-luna' if runtime=='codex' else 'alaa-implementer-haiku'),('bounded-semantic-implementation','30-implementation.md','alaa-implementer-low' if runtime=='codex' else 'alaa-implementer-haiku'),('correctness-review','50-correctness-review.md','alaa-reviewer'),('documentation','90-completion/20-review-followup.md','alaa-documenter')]:
  contract=profiles[role]['contract'] if role in profiles else ('assets/reviewer-contract.md' if runtime=='codex' and role=='alaa-reviewer' else f'agents/{role}.{suffix}')
  paths=shared+[prefix+'references/delegation-prompts/'+template,prefix+contract]
  if kind in ['mechanical-implementation','bounded-semantic-implementation']:paths.append(prefix+'references/resource-policy.md')
  routes[runtime+'/'+kind]=list(dict.fromkeys(paths))
allpaths=set(x for paths in routes.values() for x in paths)
allpaths.update(p.relative_to(OUT/'before').as_posix() for p in (OUT/'before').rglob('*') if p.is_file())
rows=[]
for rel in sorted(allpaths):
 p=Path(rel);a=(OUT/'before'/rel).read_bytes() if (OUT/'before'/rel).is_file() else p.read_bytes();b=p.read_bytes()
 rows.append({'path':rel,'before_bytes':len(a),'after_bytes':len(b),'before_words':len(a.decode('utf-8').split()),'after_words':len(b.decode('utf-8').split()),'before_sha256':hashlib.sha256(a).hexdigest(),'after_sha256':hashlib.sha256(b).hexdigest()})
lookup={r['path']:r for r in rows};totals=[]
for name,paths in routes.items():
 row={'route':name,'paths':paths}
 for metric in ['before_bytes','after_bytes','before_words','after_words']:row[metric]=sum(lookup[p][metric] for p in paths)
 row['delta_bytes']=row['after_bytes']-row['before_bytes'];row['delta_words']=row['after_words']-row['before_words'];totals.append(row)
result={'method':'Raw UTF-8 file bytes; whitespace words via text.split(), same paths/algorithm before and after, each loaded file once. Frontmatter included as baseline.json. No tokenizer, actual-token or cost claim.',
 'assumptions':'Representative fresh-context generic repository tasks, existing workflow parent, admitted role, no failure/install/integration. Includes common mandatory policy/runtime/role/dispatch/gate/workflow routes and authoritative role source (canonical contract when generated). Product-specific instructions and unchanged tool payloads excluded. Reference 92 is conditional evaluation capability, counted separately; no existing route acquires it. No body content relocated. Unchanged files have equal current/before bytes; owned before snapshots preserve historical bytes.',
 'files':rows,'routes':totals,'conditional_evaluation_change':lookup[PG+'references/92-agent-evaluation.md']}
(OUT/'size-and-read-paths.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
for r in rows:
 if r['path'].endswith('orchestrator/SKILL.md'):print(r['path'],r['before_bytes'],r['after_bytes'],r['before_words'],r['after_words'])
for r in totals:print(r['route'],r['delta_bytes'],r['delta_words'])
