#!/usr/bin/env python3
"""Write bounded text extracts of the session into <out>/: workflow scripts, args, results; direct lane dispatches and final reports; lead text."""
import json, sys, glob, os, re, datetime
root, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
def w(name, text):
    open(os.path.join(out, name), "w").write(text); print(name, len(text))
def dump(o, ind=0):
    pad = "  " * ind
    if isinstance(o, dict):
        return "".join(f"{pad}[{k}]\n{dump(v, ind+1)}" for k, v in o.items())
    if isinstance(o, list):
        return "".join(f"{pad}- item {i}\n{dump(v, ind+1)}" for i, v in enumerate(o))
    return "\n".join(pad + l for l in str(o).splitlines()) + "\n"
runs = sorted((json.load(open(p)) for p in glob.glob(os.path.join(root, "workflows", "*.json"))), key=lambda d: d["startTime"])
for i, d in enumerate(runs, 1):
    st = datetime.datetime.fromtimestamp(d["startTime"] / 1000, datetime.timezone.utc).strftime("%m-%dT%H:%M:%SZ")
    head = f"RUN {i} {d['runId']} name={d.get('workflowName')} start={st} durationMin={d.get('durationMs',0)/60000:.1f} agents={d.get('agentCount')} totalTokens={d.get('totalTokens')} toolCalls={d.get('totalToolCalls')}\nsummary: {d.get('summary')}\n"
    w(f"run{i}-script.txt", head + "\n=== SCRIPT ===\n" + d.get("script", "") + "\n=== ARGS ===\n" + dump(d.get("args")))
    w(f"run{i}-result.txt", head + "\n=== RESULT ===\n" + dump(d.get("result")))
    prog = d.get("workflowProgress") or []
    w(f"run{i}-progress.txt", head + "\n".join(json.dumps(p, ensure_ascii=False)[:400] for p in prog))
# main session: Agent dispatch prompts, hand-backs, lead text
main = root + ".jsonl"; parts = []; lead = []
for line in open(main):
    try: d = json.loads(line)
    except Exception: continue
    if d.get("type") not in ("user", "assistant"): continue
    ts = (d.get("timestamp") or "")[5:19]
    c = (d.get("message") or {}).get("content")
    if isinstance(c, str): c = [{"type": "text", "text": c}]
    for x in c or []:
        if d["type"] == "assistant" and x.get("type") == "tool_use" and x.get("name") in ("Agent", "SendMessage", "Workflow", "TaskStop"):
            inp = dict(x.get("input") or {})
            if x["name"] == "Workflow": inp.pop("script", None)
            parts.append(f"\n##### {ts} LEAD CALLS {x['name']}\n{dump(inp)}")
        elif d["type"] == "assistant" and x.get("type") == "text" and x["text"].strip():
            lead.append(f"\n##### {ts} LEAD TEXT\n{x['text']}")
            parts.append(f"\n##### {ts} LEAD TEXT ({len(x['text'])} chars, see lead-text.txt)")
        elif d["type"] == "user" and x.get("type") == "text":
            t = x["text"]
            if "[Subagent hand-back]" in t: parts.append(f"\n##### {ts} HAND-BACK\n{t[:7000]}")
            elif "<task-notification>" in t: parts.append(f"\n##### {ts} TASK-NOTIFICATION\n{t[:6000]}")
            elif t.startswith("# Workflow authoring") or t.startswith("Base directory for this skill"): parts.append(f"\n##### {ts} SKILL BODY LOADED: {t[:90]!r} ({len(t)} chars)")
            elif not t.lstrip().startswith("<system-reminder>"): parts.append(f"\n##### {ts} USER MESSAGE\n{t[:6000]}")
        elif d["type"] == "user" and x.get("type") == "tool_result":
            r = x.get("content")
            r = r if isinstance(r, str) else " ".join(y.get("text", "") for y in r or [] if isinstance(y, dict))
            if "ExitPlanMode" in r[:0]: pass
w("main-events.txt", "".join(parts))
w("lead-text.txt", "".join(lead))
