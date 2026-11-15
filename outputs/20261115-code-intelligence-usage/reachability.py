#!/usr/bin/env python3
"""Read-only: instruction reachability in subagents, tightened re-read metric, deduped hook cost."""
import json, os, re, time, glob, collections, hashlib
ROOT = os.path.expanduser('~/.claude/projects'); cut = time.time() - 7 * 86400
C = collections.Counter
reach = C(); byrole = collections.defaultdict(C); reread = C(); hook = {}; refread = C()
SK = 'Select the evidence owner for each question'
MCPI = 'code intelligence over an indexed knowledge graph'
CLI = 'codegraph explore'
PATH = re.compile(r'\*\*`([^`]+\.[a-z]{1,5})`\*\*')
for f in glob.glob(ROOT + '/**/*.jsonl', recursive=True):
    if os.path.getmtime(f) < cut: continue
    sub = '/subagents/' in f
    at = 'MAIN'
    if sub:
        try: at = json.load(open(f[:-6] + '.meta.json')).get('agentType', '?')
        except Exception: at = '?'
    has = dict(skill=False, mcpi=False, cli=False, req=False)
    seq = []; pend = {}
    for l in open(f, errors='replace'):
        if l.startswith('{"type":"api-request'):
            has['req'] = True
            if SK in l: has['skill'] = True
            if MCPI in l: has['mcpi'] = True
            if CLI in l: has['cli'] = True
            continue
        if not sub and '<codegraph_context' in l:
            for m in re.finditer(r'<codegraph_context.*?</codegraph_context>', l, flags=re.S):
                hook[hashlib.md5((f + m.group(0)).encode()).hexdigest()] = len(m.group(0)); break
        if '"tool_use"' not in l and '"tool_result"' not in l: continue
        try: d = json.loads(l)
        except Exception: continue
        if d.get('type') not in ('assistant', 'user'): continue
        c = (d.get('message') or {}).get('content')
        if not isinstance(c, list): continue
        for b in c:
            if not isinstance(b, dict): continue
            if b.get('type') == 'tool_result' and b.get('tool_use_id') in pend:
                x = b.get('content'); x = x if isinstance(x, str) else ' '.join(y.get('text', '') for y in (x or []) if isinstance(y, dict))
                seq[pend.pop(b['tool_use_id'])] = ('cg', {os.path.basename(p) for p in PATH.findall(x)})
            if b.get('type') == 'tool_use':
                inp = b.get('input') or {}; n = b.get('name', '')
                s = str(inp.get('file_path', '')) + ' ' + str(inp.get('command', ''))
                if 'alaa-code-intelligence-routing/references/' in s or '00-topic-map.md' in s or '10-routing-contract.md' in s:
                    refread[('sub' if sub else 'main', 'opened a routing reference')] += 1
                if n == 'Skill' and 'code-intelligence' in str(inp.get('skill', '')): refread[('sub' if sub else 'main', 'invoked routing skill via Skill tool')] += 1
                if 'codegraph' in n: pend[b.get('id')] = len(seq); seq.append(('cg', set()))
                else: seq.append(('t', n, s[:400]))
    if sub and has['req']:
        reach['subagents with captured requests'] += 1
        for k, lab in (('skill', 'routing SKILL.md body in context'), ('mcpi', 'CodeGraph MCP server instructions in context'), ('cli', '"codegraph explore" CLI block in context')):
            if has[k]: reach[lab] += 1; byrole[at][k] += 1
        byrole[at]['n'] += 1
    for i, e in enumerate(seq):
        if e[0] != 'cg' or not e[1]: continue
        nxt = [x for x in seq[i + 1:i + 9] if x[0] == 't']
        hits = sum(1 for x in nxt if x[1] in ('Read', 'Bash') and re.search(r'\b(Read|sed|cat|head|nl|awk)\b', x[1] + ' ' + x[2]) and any(bn in x[2] for bn in e[1]))
        reread['re-read >=1 file CodeGraph had just returned (next 8 calls)' if hits else 'did not re-read returned files'] += 1
def show(t, c):
    print('\n## ' + t)
    for k, v in sorted(c.items(), key=lambda x: -x[1]): print(f'  {v:6d}  {k}')
show('reachability (subagent requests)', reach); show('routing references / skill invocations', refread); show('re-read after CodeGraph', reread)
print('\n## by role: n | skill body | mcp instr | cli block')
for a, c in sorted(byrole.items(), key=lambda x: -x[1]['n'])[:14]: print(f'  {a:30s} {c["n"]:4d} | {c["skill"]:4d} | {c["mcpi"]:4d} | {c["cli"]:4d}')
s = sorted(hook.values())
if s: print('\n## prompt-hook injections deduped: n', len(s), 'median', s[len(s)//2], 'sum', sum(s))
