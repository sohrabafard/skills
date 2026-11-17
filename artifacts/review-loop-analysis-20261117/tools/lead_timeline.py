#!/usr/bin/env python3
"""Bounded timeline of the lead session: user text, Skill/Agent/Workflow calls, notifications, compactions."""
import json, sys, re
path = sys.argv[1]
lim = int(sys.argv[2]) if len(sys.argv) > 2 else 220
def short(s, n=lim):
    s = re.sub(r"\s+", " ", str(s))
    return s[:n] + ("…" if len(s) > n else "")
for line in open(path):
    try: d = json.loads(line)
    except Exception: continue
    t = d.get("type"); ts = (d.get("timestamp") or "")[5:19]
    if t == "system":
        sub = d.get("subtype")
        if sub and "compact" in str(sub): print(ts, "SYSTEM", sub)
        continue
    if t not in ("user", "assistant"): continue
    msg = d.get("message") or {}
    content = msg.get("content")
    if isinstance(content, str):
        content = [{"type": "text", "text": content}]
    for c in content or []:
        ct = c.get("type")
        if t == "user" and ct == "text":
            txt = c.get("text", "")
            tag = "NOTIF" if "<task-notification>" in txt else ("SYSREM" if txt.lstrip().startswith("<system-reminder>") else "USER")
            if d.get("isCompactSummary"): tag = "COMPACT-SUMMARY"
            print(ts, tag, short(txt, 160 if tag != "USER" else 500))
        elif t == "assistant" and ct == "tool_use":
            name = c.get("name"); inp = c.get("input") or {}
            if name == "Agent":
                print(ts, "AGENT", json.dumps({k: (short(v, 70) if isinstance(v, str) else v) for k, v in inp.items() if k != "prompt"}, ensure_ascii=False), "| prompt chars", len(inp.get("prompt", "")), "| id", c.get("id", "")[-6:])
            elif name == "Workflow":
                print(ts, "WORKFLOW", {k: (short(v, 80) if isinstance(v, str) else type(v).__name__) for k, v in inp.items()})
            elif name == "Skill":
                print(ts, "SKILL", inp)
            elif name in ("AskUserQuestion", "ExitPlanMode", "EnterPlanMode", "TaskStop", "SendMessage", "advisor"):
                print(ts, name.upper(), short(json.dumps(inp, ensure_ascii=False), 300))
            elif name == "Read" and ("/skills/" in str(inp.get("file_path", "")) or "/.claude/" in str(inp.get("file_path", ""))):
                print(ts, "READ", inp.get("file_path"), inp.get("offset", ""), inp.get("limit", ""))
        elif t == "assistant" and ct == "text" and len(c.get("text", "")) > 0 and "--text" in sys.argv:
            print(ts, "LEAD", short(c.get("text"), 300))
