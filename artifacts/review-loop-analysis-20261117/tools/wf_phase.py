#!/usr/bin/env python3
"""Per workflow run and phase: agents, wall span, summed agent minutes, tokens (deduped by message id)."""
import json, sys, glob, os, collections, datetime
root = sys.argv[1]
def f(s): return datetime.datetime.fromisoformat(s.replace("Z", "+00:00"))
runs = sorted(glob.glob(os.path.join(root, "workflows", "*.json")), key=lambda p: json.load(open(p))["startTime"])
grand = collections.Counter()
for i, p in enumerate(runs, 1):
    run = json.load(open(p))["runId"]
    ph = collections.defaultdict(lambda: dict(n=0, first=None, last=None, agentmin=0.0, tok=collections.Counter(), tools=0, labels=collections.Counter()))
    for a in glob.glob(os.path.join(root, "subagents", "workflows", run, "agent-*.jsonl")):
        meta = json.load(open(a[:-6] + ".meta.json")) if os.path.exists(a[:-6] + ".meta.json") else {}
        first = last = None; usage = {}; tools = 0
        for line in open(a):
            try: d = json.loads(line)
            except Exception: continue
            if d.get("type") not in ("user", "assistant"): continue
            ts = d.get("timestamp")
            if ts: first = first or ts; last = ts
            m = d.get("message") or {}
            if d["type"] == "assistant":
                if m.get("id") and m.get("usage"): usage[m["id"]] = m["usage"]
                tools += sum(1 for x in m.get("content") or [] if x.get("type") == "tool_use")
        e = ph[meta.get("workflowPhase") or "?"]
        e["n"] += 1; e["tools"] += tools
        e["labels"][(meta.get("agentType") or "?") + ":" + (meta.get("description") or "").split(":")[0][:22]] += 1
        if first:
            e["first"] = min(e["first"] or first, first); e["last"] = max(e["last"] or last, last)
            e["agentmin"] += (f(last) - f(first)).total_seconds() / 60
        for u in usage.values():
            for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens"):
                e["tok"][k] += u.get(k) or 0
    print(f"\n== RUN {i} {run}")
    for name, e in sorted(ph.items(), key=lambda kv: kv[1]["first"] or ""):
        t = e["tok"]; grand.update(t)
        span = (f(e["last"]) - f(e["first"])).total_seconds() / 60 if e["first"] else 0
        print(f"  {name:12} agents {e['n']:3} | {e['first'][11:19]}..{e['last'][11:19]} span {span:5.1f}m | agent-min {e['agentmin']:6.1f} | fresh-in {(t['input_tokens']+t['cache_creation_input_tokens'])/1e3:7.0f}k cacheR {t['cache_read_input_tokens']/1e6:6.1f}M out {t['output_tokens']/1e3:5.0f}k | tools {e['tools']}")
        print("     ", dict(e["labels"].most_common(8)))
print("\nGRAND workflows: fresh-in %.1fM cacheR %.1fM out %.0fk" % ((grand['input_tokens']+grand['cache_creation_input_tokens'])/1e6, grand['cache_read_input_tokens']/1e6, grand['output_tokens']/1e3))
