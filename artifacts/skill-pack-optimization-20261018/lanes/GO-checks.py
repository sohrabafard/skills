"""GO-owned static contract counterexamples; no application or live-agent proof."""
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / 'skills/sohrab'
LANE = Path(__file__).parent
source = json.loads((LANE / 'GO-source-manifest.json').read_text(encoding='utf-8'))


def read(skill, name='SKILL.md'):
    return (BASE / skill / name).read_text(encoding='utf-8')


results = []


def check(topic, condition):
    results.append({'topic': topic, 'layer': 'static-instruction-contract', 'passed': bool(condition)})


phase = 'references/05-phase-and-source-truth.md'
phase_owner = read('alaa-go-chi-development', phase)
for skill in ('alaa-golang', 'alaa-golang-clean-code-principles'):
    text = read(skill)
    check(skill + ':phase-authority', phase in text and 'scripts/phase-check.sh' in text
          and 'explicit go-ahead' not in text)
check('phase:action-not-blanket', all(x in phase_owner for x in (
    '`consumer-repo-read`', '`consumer-repo-write`', '`propagation`', '`consumer-impact-claim`',
    '`consumer-release-gate`', '`kit-surface-write-from-consumer-context`',
    'evidence-required', 'forbidden', 'the requester asked for this specific action',
    'before** the action', 'valid reactivation record')))

runtime = read('alaa-golang-clean-code-principles', 'references/30-runtime-and-observability.md')
check('drain:finite-detached-context', 'WithTimeout(context.WithoutCancel(ctx), w.flushBudget)' in runtime
      and 'defer cancel()' in runtime and 'finite, validated component budget' in runtime)
check('loss:all-three-preserved', all(x in runtime for x in (
    'maximum number of records', 'maximum time', 'buffer is empty',
    'counter metric increments on every dropped record', 'an alert fires', 'No agent self-certifies')))
overlap = read('alaa-golang', 'references/11-orchestration-and-overlap-guide.md')
check('goroutine:no-documented-exception', 'documented fire-and-forget' not in overlap
      and 'all three accepted-data-loss conditions' in overlap)
check('signal:kit-owner', 'Standalone service without `runkit`' in read(
    'alaa-golang', 'references/45-failure-behavior-at-the-call-site.md')
    and 'kit consumers register with `runkit` instead' in read(
        'alaa-golang', 'references/70-modern-go-baseline/30-runtime-and-standard-library.md'))

commit = read('service-runtime-kit-governance')
check('commit:explicit-authority', 'only with explicit user authorization' in commit
      and 'leave them uncommitted' in commit and 'no generated file about to be committed carries secret material' in commit)
imports = read('alaa-golang', 'references/62-import-direction-and-boundaries.md')
p5 = read('alaa-golang-clean-code-principles', 'references/20-domain-data-and-consistency.md')
check('imports:complete-owner', all(x in imports for x in (
    'net/http', 'database/sql', 'github.com/gofiber/', 'github.com/jackc/pgx/',
    'github.com/redis/go-redis/', 'github.com/rabbitmq/amqp091-go', 'provider SDK',
    'transitively', 'go list -deps', 'consumer owns the interface', 'returns a concrete type'))
    and 'and it wins' not in imports and 'grep -E' not in p5
    and 'references/62-import-direction-and-boundaries.md' in p5)
provider = read('alaa-data-layer', 'references/50-redis-laravel-octane.md')
check('provider:no-boot-cache-exception', 'references/20-composition-and-boot.md' in provider
      and '$this->app->booting(' not in provider
      and 'unavoidable boot-time cache read' not in provider and 'first use inside the consuming class' in provider)

fiber = read('alaa-golang-fiber', 'references/40-production-readiness.md')
check('fiber:correlation-union', all(x in fiber for x in (
    'TraceContext', 'reinjection', 'missing or malformed', 'fresh valid context',
    'bounded', 'warning signal', 'outer correlation middleware', 'kit change request',
    'references/20-operational-and-observability-contract.md', 'error/probe coverage')))
test = read('alaa-golang-fiber', 'references/30-validation-testing.md')
check('fiber:tdd-and-retained-race', all(x in test for x in (
    'references/63-tdd-and-testing-discipline.md', 'isolated failure confirmation',
    'stop/report', 'retaining any value derived from `fiber.Ctx`', 'including copied values',
    'does not prove', 'command authority')))
check('fiber:no-independent-broad-command', all('go test -race ./...' not in read('alaa-golang-fiber', f)
      for f in ('SKILL.md', 'references/30-validation-testing.md',
                'references/40-production-readiness.md', 'references/45-v2-to-v3-migration.md')))
cache_owner = ' '.join(read('alaa-observability-soc', 'references/20-instrumentation-gates.md')
                       .split('## Cache signals')[1].split('\n## ')[0].split())
check('cache:conditional-union', all(x in cache_owner for x in (
    'hits', 'misses', 'errors', 'source-of-truth fallbacks', 'latency histogram',
    'without a cache', 'not applicable', 'Cache keys and entity identifiers never become metric labels'))
    and 'Cache signals' in fiber
    and 'Cache signals' in read('alaa-golang', 'references/61-redis-cache-layer.md'))
redis = read('alaa-data-layer', 'references/51-redis-golang.md')
check('redis:runtime-facts-and-wiring', all(x in redis for x in (
    '2026-07-26', 'Re-read the cited file', '250ms', 'MaxRetries', 'SeverityDegraded',
    'ErrMissingTTL', '(nil, false, nil)', 'WithCacheMetrics', 'CacheResult',
    'requests their', 'Cache signals', 'double-count')))
check('redis:configuration-contract-preserved', all(x in read('alaa-data-layer', 'references/60-configuration-and-kit-gaps.md')
      for x in ('REDIS_DIAL_TIMEOUT', '`1s`', 'REDIS_CALL_TIMEOUT', '`250ms`', 'REDIS_MAX_RETRIES',
                'REDIS_POOL_SIZE', '51-redis-golang.md', 'PG_ROLLBACK_TIMEOUT', 'unbounded rollback')))
clean_evals = json.loads(read('alaa-golang-clean-code-principles', 'evals/evals.json'))['evals']
check('evals:phase-not-pinned', all('current phase' in clean_evals[i]['expected_output']
      and 'matrix' in clean_evals[i]['expected_output'] for i in (0, 1, 2))
      and 'active KIT_FIRST_STABILIZATION phase' not in clean_evals[6]['expected_output'])
fiber_eval = json.loads(read('alaa-golang-fiber', 'evals/evals.json'))['evals'][0]['expected_output']
check('evals:precedent-observed', 'current kit consumer registry' in fiber_eval
      and 'no Ala service runs on Fiber today' not in fiber_eval)
for skill, ids in (('alaa-golang-clean-code-principles', {0, 1, 2, 6}), ('alaa-golang-fiber', {0})):
    path = 'skills/sohrab/' + skill + '/evals/evals.json'
    before = json.loads(subprocess.check_output(['git', 'show', source['head'] + ':' + path], cwd=ROOT))
    after = json.loads((ROOT / path).read_text(encoding='utf-8'))
    check(skill + ':eval-other-expectations-preserved', before.keys() == after.keys()
          and len(before['evals']) == len(after['evals'])
          and all(a.keys() == b.keys() and [k for k in a if a[k] != b[k]]
                  == (['expected_output'] if a['id'] in ids else [])
                  for a, b in zip(before['evals'], after['evals'])))

changed = []
for record in source['files']:
    path = ROOT / record['path']
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != record['sha256']:
        changed.append(record['path'])
        check(record['path'] + ':encoding', bool(data) and b'\r' not in data and not data.startswith(b'\xef\xbb\xbf'))
check('scope:no-runtime-code-change', all(x.endswith(('.md', 'evals.json')) for x in changed))
for record in source['files']:
    if '/scripts/' in record['path'] or '/assets/' in record['path'] or record['path'].endswith('openai.yaml'):
        check(record['path'] + ':preserved', hashlib.sha256((ROOT / record['path']).read_bytes()).hexdigest() == record['sha256'])

output = {'claim': 'static instruction-contract proof only', 'results': results,
          'changed_files': changed, 'passed': all(r['passed'] for r in results)}
(LANE / 'GO-checks.json').write_text(json.dumps(output, indent=2) + '\n', encoding='utf-8', newline='\n')
failed = [r['topic'] for r in results if not r['passed']]
print(json.dumps({'passed': output['passed'], 'checks': len(results), 'failed': failed}))
raise SystemExit(1 if failed else 0)
