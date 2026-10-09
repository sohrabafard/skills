from pathlib import Path
import difflib
import hashlib
import json

root=Path.cwd()
out=root/'outputs/20261010-go-routing-ownership'
base=root/'skills/sohrab/alaa-code-intelligence-routing/references'
before={name:(base/name).read_text(encoding='utf-8') for name in ('10-routing-contract.md','40-stack-bindings.md')}
draft=dict(before)

def change(name,old,new):
    assert old in draft[name], (name,old)
    draft[name]=draft[name].replace(old,new)

change('10-routing-contract.md',
       'Name the question before selecting one primary owner.',
       'Name the question and reuse adequate fresh evidence before selecting one primary owner. A provider preference never requires retrieving an already answered fact again.')
change('10-routing-contract.md',
       'Verify only the needed capability:',
       'Reuse still-valid capability evidence and verify only the needed capability; do not run blanket health probes. Check')
change('10-routing-contract.md',
       '| Unknown code location, related symbols, source call path, callers/callees or likely impact in supported indexed source | CodeGraph\'s installed exploration surface | Same-index CLI for transport failure; supported Serena operation; bounded native source for a narrower claim |',
       '| Source/declaration lookup, location, relationships, call paths or likely impact in supported indexed source, whether the file/symbol is known or unknown | CodeGraph\'s eligible exploration/source operation when it can adequately answer the question | Same-index CLI for transport failure; supported Serena operation; bounded native source for a narrower claim |')
change('10-routing-contract.md',
       '| Known-symbol declaration, references, implementations, hierarchy, diagnostics or semantic edit | Stack-declared semantic owner, otherwise supported Serena backend | Equivalent configured native semantic operation; targeted source for partial read evidence; bounded native edit under the continuation rule below |',
       '| Required binding/build-aware semantics, complete references or implementation hierarchy, diagnostics or semantic mutation | Capable stack-declared semantic owner, otherwise supported Serena backend, directly without a futile graph call | Eligible configured Go gopls or equivalent native semantic operation; targeted source for partial read evidence; bounded native edit under the continuation rule below |')
change('10-routing-contract.md',
       'The CodeGraph server/installer owns exact usage and managed instructions. Its structural priority does not override semantic, native-artifact, runtime, review or proof ownership.',
       'Known file or symbol identity alone does not select Serena. Prefer eligible CodeGraph for source/structural questions it can adequately answer, then eligible Serena, then bounded native evidence. A required semantic operation that CodeGraph cannot establish goes directly to its capable semantic owner; do not make a graph-first call merely to satisfy a preference. Native dependency metadata/resolution, literals, unsupported artifacts, Boost/runtime facts and native proof keep the specialized owners above. The CodeGraph server/installer owns exact usage and managed instructions.')
change('10-routing-contract.md',
       '- Missing known-symbol semantics: use an available equivalent stack-native semantic operation, then targeted source for a partial read claim.',
       '- Missing required semantic operation: use eligible configured Go gopls or an equivalent stack-native semantic operation, then targeted source for a partial read claim.')
change('40-stack-bindings.md',
       'Explore can return source, relationships and impact together: consume it under the routing contract.',
       'Explore accepts file or symbol names and can return verbatim source, relationships and impact together. Known identity does not change its eligibility; use it for adequate source/structural answers under the routing contract. Consume returned provenance: heuristic edges do not prove binding completeness.')
change('40-stack-bindings.md',
       'Use supported symbol search/overview, declaration, references, implementations and diagnostics for exact symbol facts.',
       'Use supported symbol search/overview, declaration, references, implementations and diagnostics for a separately needed semantic fact or eligible source fallback selected by the routing contract. A known file or symbol alone does not require a Serena read after adequate CodeGraph evidence.')
change('40-stack-bindings.md',
       "Use CodeGraph for unknown source flow. Serena's configured Go backend uses gopls; backend use is not a parallel owner. Use direct configured gopls only for a recorded unavailable/unhealthy or missing build-aware, generated-code, dependency-resolution, package-API or code-action operation that it actually supports. For dependency metadata or an authorized upgrade, use the native recipes in `references/45-native-tools.md`;\nsource/impact/API questions trigger their own selection under `references/10-routing-contract.md`. That contract also owns bounded native edits and supplemental diagnostics. Native Go recipes own build/vet/test proof.",
       "For Go source/structural lookup, follow `references/10-routing-contract.md`: eligible CodeGraph is preferred when it can adequately answer, even for a known file or symbol. Required binding/build-aware semantics, diagnostics or semantic mutation select capable Serena directly, then configured gopls for a supported unavailable/unhealthy or missing-operation gap, then eligible native evidence retaining lost guarantees. Serena's Go backend uses gopls; that backend is not a parallel owner. Do not require a graph call for an operation it cannot establish. For dependency metadata/resolution or an authorized upgrade, use `references/45-native-tools.md`; source/impact/API questions trigger separate selection. The routing contract owns bounded native edits and supplemental diagnostics. Native Go recipes own build/vet/test proof.")
change('40-stack-bindings.md',
       'Use CodeGraph for unknown component/composable/store/client flow. Use Serena for known Vue/TypeScript semantics only with the correct configured backend.',
       'Apply the routing contract to component/composable/store/client source questions, including known files/symbols. Required Vue/TypeScript semantics use capable Serena only with the correct configured backend.')

# Save complete policy drafts before wording compression; earlier evidence is untouched.
for name,text in draft.items():
    p=out/'steering-drafts'/name
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(text,encoding='utf-8',newline='\n')

final=dict(draft)
cuts=[]
def compress(name,old,new):
    assert old in final[name]
    final[name]=final[name].replace(old,new)
    cuts.append({'file':name,'draft':old,'final':new,'classification':'wording only; same policy, trigger and limits'})
compress('10-routing-contract.md',
         'Name the question and reuse adequate fresh evidence before selecting one primary owner. A provider preference never requires retrieving an already answered fact again.',
         'Name the question; reuse adequate fresh evidence before selecting one primary owner. Preference never justifies retrieving an answered fact again.')
compress('10-routing-contract.md',
         'Known file or symbol identity alone does not select Serena. Prefer eligible CodeGraph for source/structural questions it can adequately answer, then eligible Serena, then bounded native evidence. A required semantic operation that CodeGraph cannot establish goes directly to its capable semantic owner; do not make a graph-first call merely to satisfy a preference.',
         'Known identity alone does not select Serena. Prefer eligible CodeGraph for adequate source/structural answers, then eligible Serena, then bounded native evidence. Send required semantics beyond CodeGraph directly to the capable semantic owner; do not make a futile graph-first call.')
compress('40-stack-bindings.md',
         'Explore accepts file or symbol names and can return verbatim source, relationships and impact together. Known identity does not change its eligibility; use it for adequate source/structural answers under the routing contract. Consume returned provenance: heuristic edges do not prove binding completeness.',
         'Explore accepts file/symbol names and can return verbatim source, relationships and impact together. Apply the routing contract regardless of known identity; heuristic edges do not prove binding completeness.')
compress('40-stack-bindings.md',
         'A known file or symbol alone does not require a Serena read after adequate CodeGraph evidence.',
         'Known identity alone does not require a Serena read after adequate CodeGraph evidence.')
compress('40-stack-bindings.md',
         'Do not require a graph call for an operation it cannot establish.',
         'Skip graph calls for unsupported operations.')

patch=''
for name,text in final.items():
    path=base/name
    path.write_text(text,encoding='utf-8',newline='\n')
    rel=path.relative_to(root).as_posix()
    patch+=''.join(difflib.unified_diff(before[name].splitlines(True),text.splitlines(True),fromfile='pre-steering/'+rel,tofile='post-steering/'+rel))
(out/'steering-diff.patch').write_text(patch,encoding='utf-8',newline='\n')
(out/'steering-compression.json').write_text(json.dumps(cuts,indent=2)+'\n',encoding='utf-8',newline='\n')
paths=sorted(p for d in ('alaa-golang','alaa-code-intelligence-routing') for p in (root/'skills/sohrab'/d).rglob('*') if p.is_file())
payload=''.join(f'{p.relative_to(root).as_posix()} {hashlib.sha256(p.read_bytes()).hexdigest()}\n' for p in paths)
(out/'steering-final-manifest.txt').write_text(payload,encoding='utf-8',newline='\n')
old_manifest=dict(line.split(' ',1) for line in (out/'fix-final-manifest.txt').read_text(encoding='utf-8').splitlines())
new_manifest=dict(line.split(' ',1) for line in payload.splitlines())
modified=[p for p in new_manifest if new_manifest[p]!=old_manifest[p]]
expected=[(base/name).relative_to(root).as_posix() for name in before]
assert sorted(modified)==sorted(expected), modified
print('Exactly two routing files changed; all Go and other routing file bytes preserved.')
print('Manifest:',len(paths),'files;',hashlib.sha256(payload.encode('utf-8')).hexdigest())
print(patch)
