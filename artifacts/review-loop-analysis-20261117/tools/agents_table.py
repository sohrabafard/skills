#!/usr/bin/env python3
"""Per-subagent table: type, model, effort, start, end, tokens (deduped by message id), tool calls.
Usage: agents_table.py <session dir> [direct|wf|wfsum]"""
import json, sys, glob, os, collections
root = sys.argv[1]; mode = sys.argv[2] if len(sys.argv) > 2 else "direct"
def load(path):
    meta = {}
    for ext in (".meta.json", ".prefix.json"):
        p = path[:-6] + ext
        if os.path.exists(p):
            try: meta[ext] = json.load(open(p))
            except Exception: pass
    first = last = None; usage = {}; tools = 0; models = collections.Counter(); final = ""; firstprompt = ""
    for line in open(path):
        try: d = json.loads(line)
        except Exception: continue
        if d.get("type") not in ("user", "assistant"): continue
        ts = d.get("timestamp")
        if ts: first = first or ts; last = ts
        m = d.get("message") or {}
        c = m.get("content")
        if d["type"] == "user" and not firstprompt:
            firstprompt = c if isinstance(c, str) else " ".join(x.get("text", "") for x in c or [] if x.get("type") == "text")
        if d["type"] == "assistant":
            if m.get("id") and m.get("usage"): usage[m["id"]] = m["usage"]
            if m.get("model"): models[m["model"]] += 1
            for x in c or []:
                if x.get("type") == "tool_use": tools += 1
                if x.get("type") == "text" and x.get("text", "").strip(): final = x["text"]
    tot = collections.Counter()
    for u in usage.values():
        for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens"):
            tot[k] += u.get(k) or 0
    return dict(path=path, meta=meta.get(".meta.json", {}), prefix=(meta.get(".prefix.json", {}) or {}).get("state", {}), first=first, last=last,
                tok=tot, tools=tools, model=(models.most_common(1) or [("?", 0)])[0][0], final=final, prompt=firstprompt, turns=len(usage))
def hm(ts): return ts[5:19] if ts else "?"
def mins(a, b):
    import datetime
    f = lambda s: datetime.datetime.fromisoformat(s.replace("Z", "+00:00"))
    return round((f(b) - f(a)).total_seconds() / 60, 1) if a and b else 0
def k(n): return f"{n/1000:.0f}k"
if mode == "direct":
    rows = [load(p) for p in glob.glob(os.path.join(root, "subagents", "*.jsonl"))]
    rows.sort(key=lambda r: r["first"] or "")
    print("start | end | min | type | model | effort(prefix) | defaults | turns | tools | in+cacheW | cacheR | out | description")
    for r in rows:
        m = r["meta"]; t = r["tok"]
        print(hm(r["first"]), "|", hm(r["last"])[6:], "|", mins(r["first"], r["last"]), "|", m.get("agentType"), "|", r["model"].replace("claude-", ""), "|", r["prefix"].get("effortValue"),
              "|", m.get("launchedWithDefaults"), "|", r["turns"], "|", r["tools"], "|", k(t["input_tokens"] + t["cache_creation_input_tokens"]), "|", k(t["cache_read_input_tokens"]), "|", k(t["output_tokens"]), "|", m.get("description"), "|", m.get("worktreePath", ""))
else:
    for run in sorted(os.listdir(os.path.join(root, "subagents", "workflows"))):
        rows = [load(p) for p in glob.glob(os.path.join(root, "subagents", "workflows", run, "*.jsonl"))]
        rows.sort(key=lambda r: r["first"] or "")
        tot = collections.Counter(); 
        for r in rows: tot.update(r["tok"])
        bytype = collections.Counter((r["meta"].get("agentType"), r["model"].replace("claude-", ""), r["prefix"].get("effortValue")) for r in rows)
        print(f"\n== {run}: {len(rows)} transcripts | first {hm(min(r['first'] for r in rows if r['first']))} last {hm(max(r['last'] for r in rows if r['last']))} | in+cacheW {k(tot['input_tokens']+tot['cache_creation_input_tokens'])} cacheR {k(tot['cache_read_input_tokens'])} out {k(tot['output_tokens'])} | tools {sum(r['tools'] for r in rows)}")
        print("  by (type, model, effort):", dict(bytype))
        if mode == "wf":
            print("  meta keys:", sorted(set(kk for r in rows for kk in r["meta"])))
            for r in rows:
                m = r["meta"]; t = r["tok"]
                print("  ", hm(r["first"])[6:], hm(r["last"])[6:], mins(r["first"], r["last"]), m.get("agentType"), r["model"].replace("claude-", ""), r["prefix"].get("effortValue"), "tools", r["tools"], "out", k(t["output_tokens"]), "|", (m.get("description") or m.get("label") or "")[:60])
