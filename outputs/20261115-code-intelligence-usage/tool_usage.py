#!/usr/bin/env python3
"""Read-only tally of tool usage in recent Claude Code transcripts."""
import json, os, re, sys, time, glob, collections, shlex
ROOT = os.path.expanduser('~/.claude/projects')
DAYS = float(sys.argv[1]) if len(sys.argv) > 1 else 7
cut = time.time() - DAYS * 86400
SEARCH = {"grep","egrep","fgrep","rg","ag","ack","find","fd"}
READ = {"sed","cat","head","tail","awk","nl","less","wc","ls","tree","cut","sort","uniq","jq","yq"}
SETUP = {"cd","pushd","popd","export","set","source",".","true","unset","echo","printf"}
PREFIX = {"timeout","env","sudo","time","nice","command","exec","xargs"}
CODE = {"go","php","ts","tsx","js","jsx","mjs","cjs","vue","py","rs","java","kt","cs","c","h","cpp","rb"}
SHELL = {"sh","bash"}
EXT = re.compile(r"\.([A-Za-z0-9]{1,6})\b")
C = collections.Counter
tools = collections.defaultdict(C)       # scope -> tool counts
bashcat = collections.defaultdict(C)     # scope -> category
bashtarget = collections.defaultdict(C)  # scope -> target kind for search/read
firstcmd = C()
agent = collections.defaultdict(C)       # agentType -> counters
wt = collections.defaultdict(C)          # worktree flag -> counters
proj = collections.defaultdict(C)
cg_warn = C(); cg_sizes = []
nudges = C()
files_by_agent = C()
no_cg_agents = C()

def seg_cmds(cmd):
    cmd = re.sub(r"<<-?\s*'?\"?(\w+)'?\"?.*?\n\1\b", " ", cmd, flags=re.S)
    out = []
    for seg in re.split(r"&&|\|\||;|\||\n", cmd):
        try: w = shlex.split(seg)
        except ValueError: w = seg.split()
        while w and (("=" in w[0] and not w[0].startswith("-")) or w[0] in PREFIX or re.fullmatch(r"\d+[smh]?", w[0])):
            w = w[1:]
        if not w: continue
        n = os.path.basename(w[0])
        if n == "git" and len(w) > 1: n = "git-" + w[1]
        out.append((n, w[1:]))
    return out

def classify(cmd):
    segs = seg_cmds(cmd)
    real = [(n, a) for n, a in segs if n not in SETUP]
    if not real: return "other", None, None
    n, a = real[0]
    if n == "codegraph": return "codegraph-cli", n, None
    if n in SEARCH or n == "git-grep": cat = "search"
    elif n in READ: cat = "read"
    elif n.startswith("git-"): cat = "git"
    elif n == "bd": cat = "bd"
    elif n in {"go","php","composer","npm","pnpm","make","python3","python","node","vendor/bin/pest","pest","phpunit","golangci-lint","gofmt","docker","bash","sh"} or n.startswith("./"): cat = "run"
    else: cat = "other"
    tgt = None
    if cat in ("search", "read"):
        exts = {e.lower() for e in EXT.findall(" ".join(a))}
        if exts & CODE: tgt = "code-ext"
        elif exts & SHELL: tgt = "shell-ext"
        elif exts: tgt = "noncode-ext"
        else: tgt = "no-ext(dir/unknown)"
    return cat, n, tgt

for f in glob.glob(ROOT + '/**/*.jsonl', recursive=True):
    if os.path.getmtime(f) < cut: continue
    rel = f[len(ROOT)+1:]
    p = rel.split('/')[0].replace('-home-sohrab-project-', '') or 'project-root'
    sub = '/subagents/' in f
    scope = 'sub' if sub else 'main'
    at = 'MAIN'; inwt = False
    if sub:
        m = f[:-6] + '.meta.json'
        try:
            md = json.load(open(m)); at = md.get('agentType', '?'); inwt = bool(md.get('spawnedWithWorktree'))
        except Exception: at = '?'
    files_by_agent[at] += 1
    used_cg = False; ncalls = 0; nshell_sr = 0
    cgids = set()
    try: fh = open(f, errors='replace')
    except OSError: continue
    for l in fh:
        if 'is CodeGraph-indexed. For locating' in l and '"api-request' not in l[:60]:
            nudges[scope] += 1
        if '"tool_use"' not in l and '"tool_result"' not in l: continue
        if l.startswith('{"type":"api-request'): continue
        try: d = json.loads(l)
        except Exception: continue
        t = d.get('type')
        if t not in ('assistant', 'user'): continue
        c = (d.get('message') or {}).get('content')
        if not isinstance(c, list): continue
        for b in c:
            if not isinstance(b, dict): continue
            if b.get('type') == 'tool_result' and b.get('tool_use_id') in cgids:
                x = b.get('content'); x = x if isinstance(x, str) else ' '.join(y.get('text', '') for y in (x or []) if isinstance(y, dict))
                cg_sizes.append(len(x))
                cg_warn['different-worktree' if 'come from a different git worktree' in x else 'same-root'] += 1
                continue
            if b.get('type') != 'tool_use': continue
            name = b.get('name', ''); inp = b.get('input') or {}
            ncalls += 1
            key = name
            if name.startswith('mcp__codegraph'): key = 'CG-MCP'; used_cg = True; cgids.add(b.get('id'))
            elif name.startswith('mcp__serena'): key = 'SERENA:' + name.split('__')[-1]
            elif name.startswith('mcp__laravel-boost'): key = 'BOOST'
            elif name.startswith('mcp__'): key = 'MCP-other'
            if name == 'Bash':
                cat, n, tgt = classify(inp.get('command', ''))
                bashcat[scope][cat] += 1; agent[at]['bash:' + cat] += 1; wt[(scope, inwt)]['bash:' + cat] += 1
                proj[p]['bash:' + cat] += 1
                if cat == 'codegraph-cli': used_cg = True
                if cat in ('search', 'read'):
                    nshell_sr += 1; firstcmd[n] += 1; bashtarget[scope][tgt] += 1; agent[at]['tgt:' + tgt] += 1; proj[p]['tgt:' + tgt] += 1
            tools[scope][key] += 1; agent[at][key] += 1; wt[(scope, inwt)][key] += 1; proj[p][key] += 1
    if sub and ncalls >= 5:
        no_cg_agents[(at, 'used-cg' if used_cg else 'no-cg')] += 1

def show(title, c, n=25):
    print('\n## ' + title); tot = sum(c.values())
    for k, v in c.most_common(n): print(f'  {v:7d} {100*v/max(tot,1):5.1f}%  {k}')
    print(f'  total {tot}')
for s in ('main', 'sub'):
    show(f'tools [{s}]', tools[s], 22); show(f'bash category [{s}]', bashcat[s]); show(f'shell search/read target [{s}]', bashtarget[s])
show('first shell search/read command', firstcmd, 20)
print('\n## worktree split (scope, spawnedWithWorktree): CG-MCP, bash:codegraph-cli, bash:search, bash:read, Read, Grep, Glob')
for k, c in sorted(wt.items()): print(' ', k, [c[x] for x in ('CG-MCP','bash:codegraph-cli','bash:search','bash:read','Read','Grep','Glob')])
print('\n## per agent type: files | CG-MCP cg-cli serena | sh-search sh-read (code-ext/shell-ext/noncode/no-ext) | Read Grep Glob')
for a, n in files_by_agent.most_common(40):
    c = agent[a]; ser = sum(v for k, v in c.items() if k.startswith('SERENA'))
    print(f'  {a:32s} {n:4d} | {c["CG-MCP"]:5d} {c["bash:codegraph-cli"]:4d} {ser:4d} | {c["bash:search"]:6d} {c["bash:read"]:6d} ({c["tgt:code-ext"]}/{c["tgt:shell-ext"]}/{c["tgt:noncode-ext"]}/{c["tgt:no-ext(dir/unknown)"]}) | {c["Read"]:5d} {c["Grep"]:5d} {c["Glob"]:4d}')
print('\n## subagent runs (>=5 calls) that used CodeGraph at all')
agg = collections.defaultdict(lambda: [0, 0])
for (a, u), n in no_cg_agents.items(): agg[a][0 if u == 'used-cg' else 1] += n
for a, (u, nu) in sorted(agg.items(), key=lambda x: -sum(x[1])): print(f'  {a:32s} used={u:4d} never={nu:4d}')
print('\n## per project: CG-MCP cg-cli | sh-search sh-read (code-ext/shell/noncode/no-ext) | Read Grep')
for p, c in sorted(proj.items(), key=lambda x: -sum(x[1].values()))[:16]:
    print(f'  {p:28s} {c["CG-MCP"]:5d} {c["bash:codegraph-cli"]:4d} | {c["bash:search"]:6d} {c["bash:read"]:6d} ({c["tgt:code-ext"]}/{c["tgt:shell-ext"]}/{c["tgt:noncode-ext"]}/{c["tgt:no-ext(dir/unknown)"]}) | {c["Read"]:5d} {c["Grep"]:5d}')
show('codegraph result root', cg_warn)
if cg_sizes:
    s = sorted(cg_sizes); print('\n## codegraph result size chars: n', len(s), 'median', s[len(s)//2], 'p90', s[int(len(s)*.9)], 'max', s[-1], 'sum', sum(s))
print('\n## nudge lines seen', dict(nudges))
