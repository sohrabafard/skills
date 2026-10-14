"""Same-method body, target-tree and conditional-loading measurements.

Whitespace words include frontmatter and all body text. Byte counts are raw
UTF-8 file bytes; SHA256 identifies each source. No package install, tokenizer
download, model call or performance/cost inference. These are enumerated
instruction loading paths, not observed host context telemetry.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
M = 'skills/sohrab/alaa-memory-os/'
L = 'skills/sohrab/alaa-extract-agent-lessons/'
W = 'skills/sohrab/alaa-workflow/'

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', default='outputs/20261012-capability-recall/loading-measurements.json')
    args = parser.parse_args()
    target = (ROOT/args.output).resolve()
    target.relative_to(HERE)  # Outputs are restricted to this task artifact directory.
    baseline = json.loads((HERE/'baseline.json').read_text(encoding='utf-8'))
    cache = {}
    texts = {}

    def source(version,path):
        key = (version,path)
        if key not in cache:
            if version == 'before' and path in baseline['files']:
                saved = baseline['files'][path]
                texts[key] = saved['text']
                # baseline captures decoded UTF-8-sig text; retain authoritative
                # original byte count/hash if a BOM existed.
                cache[key] = {'path':path,'sha256':saved['sha256'],'words':len(saved['text'].split()),'bytes':saved['bytes'],'origin':'baseline.json'}
                return cache[key]
            if version == 'before':
                result = subprocess.run(['git','show',baseline['head']+':'+path],cwd=ROOT,capture_output=True,check=True)
                raw,origin = result.stdout,'baseline HEAD (supplemental unchanged/paired owner)'
            else:
                raw,origin = (ROOT/path).read_bytes(),'current worktree'
            text = raw.decode('utf-8-sig')
            texts[key] = text
            cache[key] = {'path':path,'sha256':hashlib.sha256(raw).hexdigest(),'words':len(text.split()),'bytes':len(raw),'origin':origin}
        return cache[key]

    def exists(version,path):
        if version == 'before':
            return path in baseline['files']
        return (ROOT/path).is_file()

    # One representative state, identical before/after. Count inherited reads,
    # even when admission/profile/bindings were resolved before this scan.
    workflow_required = {
        'context-continuity.md':'Existing resumable plan was resumed/reconciled; scan disposition is recorded in canonical plan/checkpoint owners.',
        'task-tracking.md':'The existing family selected local task authority; task progress/readiness and phase completion were recorded.',
        'artifact-lifecycle.md':'The existing family was admitted, attached and selected the resumable profile before execution/writes.',
        'companion-routing.md':'Phase/task bindings were populated and loaded before execution; scan consumes those resolved bindings.',
        'workspace-and-integration.md':'First writes and phase verification already recorded scoped source/evidence identity; recording the scan retains that evidence owner.',
        'context-curation.md':'First signal-bearing completed-phase scan selects scope and records its disposition, including no admitted candidates.',
    }
    workflow_excluded = {
        'phase-prompts.md':'No prompt pack is requested/generated; no runtime/model/effort or skill-trigger syntax is being resolved.',
        'review-mode.md':'This is a curation scan, not a workflow diff/plan/artifact review.',
    }
    workflow_reference_names = {p.name for p in (ROOT/W/'references').glob('*.md')}
    workflow_audit = {}

    def workflow_closure(version):
        visited, audit = set(), []
        def visit(path):
            if path in visited:
                return
            visited.add(path)
            source(version,path)
            local_links = sorted(set(re.findall(r'references/([\w-]+\.md)',texts[(version,path)])) & workflow_reference_names)
            included, excluded = [], []
            for name in local_links:
                if name in workflow_required:
                    included.append({'path':W+'references/'+name,'obligation':workflow_required[name]})
                    visit(W+'references/'+name)
                elif name in workflow_excluded:
                    excluded.append({'path':W+'references/'+name,'inactive_condition':workflow_excluded[name]})
                else:
                    raise ValueError('Unclassified workflow-internal obligation: '+name)
            audit.append({'path':path,'included_children':included,'excluded_conditional_children':excluded})
        visit(W+'SKILL.md')
        expected = {W+'SKILL.md'} | {W+'references/'+name for name in workflow_required}
        if visited != expected:
            raise ValueError('Required workflow owner is unreachable for '+version)
        workflow_audit[version] = audit
        return sorted(visited)

    def closures(version):
        memory = [M+'SKILL.md']
        if exists(version,M+'references/00-topic-map.md'):
            memory += [M+'references/00-topic-map.md']
        selected = memory+[M+'references/store-hindsight.md']
        workflow = workflow_closure(version)
        # Memory was already active for prior-context planning in this state.
        inherited = [p for p in workflow if p != W+'references/context-curation.md']+selected
        lesson = workflow+selected+[L+'SKILL.md']
        admitted = lesson+[L+'references/reusable-context-shapes.md',M+'references/knowledge-shape.md']
        setup = selected.copy()
        if exists(version,M+'references/hindsight-setup.md'):
            setup += [M+'references/hindsight-setup.md']
        paths = {
            'ordinary_recall':selected,
            'capability_recall':selected,
            'no_admitted_lesson':lesson,
            'admitted_lesson_authorized_write':admitted,
            'canonical_drift':selected+[M+'references/drift-management.md'],
            'adapter_setup':setup,
        }
        return paths, {name:inherited for name in ['no_admitted_lesson','admitted_lesson_authorized_write']}

    def total(version,paths, inherited=()):
        files = [source(version,p) for p in dict.fromkeys(paths)]
        result = {'words':sum(f['words'] for f in files),'bytes':sum(f['bytes'] for f in files),'tokens':None,'files':files}
        if inherited:
            inherited_set = set(inherited)
            for label, selected_files in [('already_loaded',[f for f in files if f['path'] in inherited_set]),('incremental',[f for f in files if f['path'] not in inherited_set])]:
                result[label] = {'words':sum(f['words'] for f in selected_files),'bytes':sum(f['bytes'] for f in selected_files),'tokens':None,'paths':[f['path'] for f in selected_files]}
            assert result['words'] == result['already_loaded']['words']+result['incremental']['words']
        return result

    result = {
        'word_method':baseline['word_method'],
        'tokenizer': {'tiktoken_installed':importlib.util.find_spec('tiktoken') is not None,'counts':'unavailable: no verified installed compatible model tokenizer; no downloads attempted'},
        'claim_limits':'Total applicable memory/lesson/workflow instruction closure for explicitly declared states, including recursively required and already-loaded workflow owners. Not measured model context, tool runtime or monetary cost. Host/global instructions, task messages/plan contents, platform invocation metadata and cross-skill domain/stack owners outside memory/lesson/workflow are excluded equally. No workflow-internal owner is excluded merely because its obligation was resolved earlier.',
        'lesson_scenario_starting_state': {
            'workflow_active':True,
            'plan':'Existing admitted local resumable multi-phase plan and checkpoint; no JSON consumer or prompt pack.',
            'admission_profile_task_store':'Previously resolved and still valid; their owners remain included in the inherited total.',
            'execution_handoff_bindings':'Phase/task bindings previously populated and loaded; existing-plan resume reconciled canonical state.',
            'prior_memory':'Hindsight memory was already activated for prior-context planning; selected routine adapter and router remain included in inherited total.',
            'boundary':'First signal-bearing completed-phase intermediate scan after phase validation/source identity was recorded.',
            'results_recorded':'Scan disposition is recorded in the existing plan and checkpoint, even when no candidates pass admission.',
            'effects':'Local workflow evidence recording is authorized; admitted-write case additionally authorizes scoped durable publication. No Beads, prompt generation, Git integration, runtime allocation, whole-task completion or workflow review.'
        },
        'closure_conditions': {
            'ordinary_recall':'Standalone memory trigger admitted; current approved Hindsight configuration resolved; routine query only; no active workflow.',
            'capability_recall':'Standalone local miss about to block or unresolved-owner permitted repair; Hindsight existence/ownership query; no active workflow or further effects.',
            'no_admitted_lesson':'Declared existing-plan lesson starting state; scan rejects all candidates before shaping/publication, but workflow disposition recording and inherited obligations remain.',
            'admitted_lesson_authorized_write':'Same existing-plan starting state; scoped candidate passes admission, is shaped/parked and authorized for selected-store write; knowledge shape/dedup required.',
            'canonical_drift':'Standalone current canonical sources disagree; no active workflow; selected-store pointer optional; repository drift owner required.',
            'adapter_setup':'Standalone Hindsight setup/configuration/import/maintenance explicitly authorized; no active workflow.'
        },
        'baseline_head':baseline['head'],
        'versions':{}
    }
    for version in ['before','after']:
        paths = list(baseline['files'])
        if version == 'after':
            paths = sorted({*paths,*(p.relative_to(ROOT).as_posix() for skill in [M,L] for p in (ROOT/skill).rglob('*') if p.is_file() and '__pycache__' not in p.parts)})
        loading, inherited = closures(version)
        result['versions'][version] = {'bodies':total(version,[M+'SKILL.md',L+'SKILL.md']), 'target_tree':total(version,paths), 'loading_closures':{name:total(version,p,inherited.get(name,())) for name,p in loading.items()}}
    result['workflow_internal_obligation_audit'] = workflow_audit
    result['delta_words'] = {name: result['versions']['after']['loading_closures'][name]['words']-result['versions']['before']['loading_closures'][name]['words'] for name in result['closure_conditions']}
    target.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(str(target.relative_to(ROOT))+': words/bytes/hashes; tokens unavailable; no runtime/cost claim')

if __name__ == '__main__':
    try:
        main()
    except (OSError,ValueError,KeyError,subprocess.CalledProcessError) as error:
        print('BLOCKED: '+type(error).__name__+' reading loading sources')
        raise SystemExit(2)
