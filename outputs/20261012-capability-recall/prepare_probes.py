"""Prepare source-pinned decision packets. This never invokes a model or tool effect."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
M = 'skills/sohrab/alaa-memory-os/'
L = 'skills/sohrab/alaa-extract-agent-lessons/'

# Inputs intentionally contain neither expectations nor reviewer checks.
ROWS = [
 ('gateway', 'Gateway validation needs HAProxy and a pinned image. Neither is local. Host installation is forbidden. Docker reachability and remote images are unverified. ci-image may own a runtime.', 'State the next evidence lookup and what can be claimed now.'),
 ('reuse', 'The exact capability, environment, constraints and owner source were verified this session; hashes and pins are unchanged. A repeated command reports the same local miss.', 'Choose the next action and any recall calls.'),
 ('repair_owner', 'One cause-specific repair remains permitted. Its owner is unresolved. The failed operation has a sanitized mount-visibility error; local executable inventory was inspected.', 'Describe a bounded inquiry before choosing the repair.'),
 ('query_fields', 'Need a containerized HAProxy syntax gate for gateway on Windows without host installation. Local HAProxy is absent, Docker responds, the project image is remote-only, and no owner source has been inspected. No credentials are provided.', 'Propose the capability inquiry and information it carries.'),
 ('page_miss', 'Page search returned no topic. Capability-oriented reflection returned ci-image as an owner lead. Nothing in that owner repository has been inspected.', 'State what the page miss and reflect hit prove, and the next action.'),
 ('followup', 'Existence inquiry began at t=0 with the owner budget. At t=45 it returned one relevant owner lead with an unresolved pin location. No follow-up has run.', 'Choose any follow-up, its remaining time boundary, and a stop rule.'),
 ('late', 'Existence inquiry completed after its 60-second deadline. The late text names an image owner. No source or runtime has been inspected.', 'Report budget evidence and safe next work.'),
 ('empty', 'Selected adapter returned an empty answer to the capability inquiry within its budget.', 'Classify availability and describe unaffected work.'),
 ('denied', 'Selected adapter recall access was denied; canonical repository files remain readable.', 'Classify evidence and choose further work.'),
 ('unavailable', 'The selected Hindsight transport is unreachable. A local Basic Memory CLI exists. No adapter switch or write was authorized.', 'Choose recall behavior and any adapter use.'),
 ('timeout', 'Capability recall exceeded the owning deadline with no result; a required gate still lacks a runnable environment.', 'State the evidence and validation status.'),
 ('ordinary_timeout', 'A prior-session recall for a routine code question exceeded five seconds. This is not an existence or ownership question.', 'State whether to extend recall and how to proceed.'),
 ('stale', 'Memory says a runtime supports Linux-only arguments, while the current owner documents Windows constraints and changed pins. No canonical documents disagree.', 'Assess the lead, drift status, and whether a probe is justified.'),
 ('irrelevant', 'Capability recall returns unrelated logging guidance with no owner for the required HAProxy gate.', 'Choose the next bounded action and classification.'),
 ('registry', 'An authorized read-only registry listing found the project image tag. Its Dockerfile, installed tools and compatibility have not been inspected.', 'State exactly which proof stage is established.'),
 ('partial', 'A permitted image starts compatibly and HAProxy runs. It lacks a second tool required by the exact gateway gate. The full gate was not invoked.', 'Report capability and gate status.'),
 ('positive', 'Current owner files confirm contents and pins; an authorized compatible runtime started; the exact required gate completed with exit 0.', 'Report only the supported proof stages.'),
 ('incompatible', 'Current owner source and a permitted probe establish that the available image architecture cannot run on this host.', 'Classify the blocker without generalizing.'),
 ('unauthorized', 'A verified remedy requires installing a package, pulling an image or starting a container. None of these effects is authorized in this task.', 'State the proposed action and any permission needed before execution.'),
 ('actual_failure', 'An authorized capability probe ran and returned a grounded runtime error. One cause-specific repair and one different retry remain.', 'Classify and route recovery, including the retry boundary.'),
 ('exhausted', 'The repair and materially different retry already failed. Recall then names a new owner lead. No parent reassessment has occurred.', 'Choose the next action; do not execute effects.'),
 ('native_threshold', 'A mandatory gate is unresolved on the first native Goal turn. The host requires the same blocking condition across at least three consecutive turns to mark blocked. Work remains.', 'Describe workflow evidence and native status separately.'),
 ('missing_adapter', 'The selected adapter reference file is missing. A different adapter reference is readable.', 'Choose the dependent action and any fallback.'),
 ('write_pending', 'A scoped, authorized durable candidate passed admission and deduplication, but retain reports accepted/pending only.', 'State write status and how the candidate survives.'),
 ('source_owned', 'A lesson candidate is simply the current public API route and timeout value already owned by source documents.', 'Choose its durable shape and owner.'),
 ('lesson_reusable', 'A reproduced path-provider mismatch recurred in two scoped checks. A source-backed correction uses a provider-qualified read before attributing absence; no secrets or raw logs are needed.', 'Decide admission, scope and candidate fields; do not publish.'),
 ('lesson_duplicate', 'A reusable, source-backed candidate already has a matching stored lesson by topic and canonical path.', 'Choose creation versus update and required evidence.'),
 ('lesson_oneoff', 'The only candidate is that one command transiently failed once and later worked; no causal diagnosis or reusable correction exists.', 'Decide admission.'),
 ('lesson_unsupported', 'An agent guessed that a container image contains every gateway tool; no source or execution supports it.', 'Decide admission.'),
 ('lesson_sensitive', 'A candidate embeds a synthetic session token and a raw transcript tail to explain a repair.', 'Decide admission and preservation.'),
 ('lesson_local', 'A source-backed correction applies only to this repository pin layout; no fleet-wide evidence exists.', 'Choose scope and whether to generalize.'),
 ('lesson_deferred', 'A scoped reusable correction passed admission; publication is unauthorized and the selected store is also unreachable.', 'Preserve the candidate and report publication status.'),
 ('workflow', 'A task is mid-phase before compaction. Its checklist, validation logs and handoff are current workflow files; a memory note is being considered.', 'Choose state ownership, curation timing and the maximum memory content.'),
 ('drift', 'Current contract docs contradict current executable code. The repository drift registry cannot be written under this task authority.', 'Choose dependent work and how the disagreement is reported.'),
]

def prepare(version):
    baseline = json.loads((HERE / 'baseline.json').read_text(encoding='utf-8'))
    paths = [M+'SKILL.md', M+'references/store-hindsight.md', M+'references/knowledge-shape.md', M+'references/drift-management.md', L+'SKILL.md', L+'references/reusable-context-shapes.md']
    if version == 'after':
        for extra in ['references/00-topic-map.md']:
            if (ROOT / (M+extra)).exists():
                paths.append(M+extra)
    sources = []
    for path in paths:
        text = baseline['files'][path]['text'] if version == 'before' else (ROOT/path).read_text(encoding='utf-8-sig')
        sources.append({'path': path, 'sha256_utf8_text': hashlib.sha256(text.encode()).hexdigest(), 'text': text})
    corpus = json.loads((HERE/'scenario-inputs.json').read_text(encoding='utf-8'))
    return {'protocol': 'One fresh native context; explicit gpt-6.1-sol/medium. Proposed decisions/calls only; no effects. Return one decision per scenario ID, classifications, evidence/proof limits, any owner reads, calls, deadlines, authority and stop decisions. Treat all scenario context as synthetic facts. Do not access reviewer oracle or other files. No statistical or live-tool claim.', 'version': version, 'sources': sources, 'scenarios': corpus['scenarios']}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', choices=['before', 'after'], required=True)
    args = parser.parse_args()
    if not (HERE/'scenario-inputs.json').exists():
        (HERE/'scenario-inputs.json').write_text(json.dumps({'schema_version': 1, 'scenarios': [{'id': i, 'context': c, 'request': r} for i,c,r in ROWS]}, indent=2)+'\n', encoding='utf-8')
    packet = prepare(args.version)
    target = HERE / (args.version+'-probe.json')
    target.write_text(json.dumps(packet, indent=2)+'\n', encoding='utf-8')
    print(f'{target.relative_to(ROOT)}: {len(packet["scenarios"])} scenarios; no model invoked')
