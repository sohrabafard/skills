#!/usr/bin/env python3
"""Read-only: tool availability in subagents, nudge compliance, prompt-hook cost, brief wording."""
import json, os, re, sys, time, glob, collections
ROOT = os.path.expanduser('~/.claude/projects'); cut = time.time() - 7 * 86400
C = collections.Counter
avail = C(); after_nudge = C(); hook_sizes = []; brief = C(); cg_seq = C(); first_tool = C()
deferred = C(); serena_avail = C(); after_cg = C()
CODE = re.compile(r"\.(go|php|ts|vue|js|py)\b")
for f in glob.glob(ROOT + '/**/*.jsonl', recursive=True):
    if os.path.getmtime(f) < cut: continue
    sub = '/subagents/' in f
    seq = []  # ordered events: ('nudge',) or ('tool', name, cmd)
    got_shape = False; first_user = None
    for l in open(f, errors='replace'):
        if sub and not got_shape and l.startswith('{"type":"api-request-shape"'):
            got_shape = True
            try: d = json.loads(l)
            except Exception: continue
            names = [t.get('name', '') for t in (d.get('shape') or {}).get('tools', []) if isinstance(t, dict)]
            s = json.dumps(d.get('shape'))[:400000]
            avail['cg tool loaded' if any('codegraph' in n for n in names) else 'cg tool NOT in tool list'] += 1
            serena_avail['serena tool loaded' if any('serena' in n for n in names) else 'serena NOT in tool list'] += 1
            avail['system mentions codegraph_explore' if 'codegraph_explore' in s else 'system silent on codegraph'] += 0
            continue
        if l.startswith('{"type":"api-request'): continue
        if 'deferred_tools_delta' in l and sub:
            try: d = json.loads(l)
            except Exception: continue
            n = (d.get('attachment') or {}).get('addedNames') or []
            if any('codegraph' in x for x in n): deferred['cg deferred (needs ToolSearch)'] += 1
            if any('serena' in x for x in n): deferred['serena deferred (needs ToolSearch)'] += 1
            continue
        if '<codegraph_context' in l and not sub:
            for m in re.finditer(r'<codegraph_context.*?</codegraph_context>', l, flags=re.S): hook_sizes.append(len(m.group(0)))
        if 'is CodeGraph-indexed. For locating' in l and '"tool_use"' not in l:
            seq.append(('nudge',)); continue
        if '"tool_use"' not in l and first_user is not None: continue
        try: d = json.loads(l)
        except Exception: continue
        if d.get('type') == 'user' and first_user is None and sub:
            c = (d.get('message') or {}).get('content')
            first_user = c if isinstance(c, str) else ' '.join(x.get('text', '') for x in c if isinstance(x, dict))
            low = first_user.lower()
            brief['briefs total'] += 1
            if 'codegraph' in low: brief['brief mentions codegraph'] += 1
            if 'serena' in low: brief['brief mentions serena'] += 1
            if re.search(r'\bgrep\b|\brg\b|sed -n', low): brief['brief itself says grep/rg/sed'] += 1
            continue
        if d.get('type') != 'assistant': continue
        c = (d.get('message') or {}).get('content')
        if not isinstance(c, list): continue
        for b in c:
            if isinstance(b, dict) and b.get('type') == 'tool_use':
                seq.append(('tool', b.get('name', ''), str((b.get('input') or {}).get('command', ''))[:300]))
    for i, e in enumerate(seq):
        if e[0] == 'nudge':
            nxt = [x for x in seq[i + 1:i + 4] if x[0] == 'tool']
            k = 'no following call'
            if nxt:
                k = 'next 3 calls include CodeGraph' if any('codegraph' in x[1] or x[2].lstrip().startswith('codegraph') for x in nxt) else 'kept shell/other, no CodeGraph'
            after_nudge[('sub' if sub else 'main', k)] += 1
        if e[0] == 'tool' and 'codegraph' in e[1]:
            nxt = [x for x in seq[i + 1:i + 6] if x[0] == 'tool']
            reread = sum(1 for x in nxt if x[1] == 'Read' or (x[1] == 'Bash' and re.match(r'\s*(cd [^&]+&&\s*)?(sed|cat|grep|rg|head)\b', x[2]) and CODE.search(x[2])))
            after_cg['next 5 calls contain >=2 shell/Read code reads' if reread >= 2 else 'moved on (<2 code reads)'] += 1
def show(t, c):
    print('\n## ' + t)
    for k, v in sorted(c.items(), key=lambda x: -x[1]): print(f'  {v:6d}  {k}')
show('subagent first request: tool availability', avail); show('serena availability', serena_avail); show('deferred in subagents', deferred)
show('dispatch briefs', brief); show('after a nudge', after_nudge); show('after a CodeGraph call', after_cg)
if hook_sizes:
    s = sorted(hook_sizes); print('\n## prompt-hook injection (main): n', len(s), 'median', s[len(s)//2], 'p90', s[int(len(s)*.9)], 'max', s[-1], 'sum', sum(s))
