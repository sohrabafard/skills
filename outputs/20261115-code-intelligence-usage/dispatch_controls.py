#!/usr/bin/env python3
"""Count Agent dispatches with and without explicit model and effort. Read-only.

Usage: dispatch_controls.py [days]   (default 2)
"""
import collections
import json
import sys
import time
from pathlib import Path

days = float(sys.argv[1]) if len(sys.argv) > 1 else 2
cutoff = time.time() - days * 86400
root = Path.home() / ".claude/projects"
total = collections.Counter()
by_type = collections.defaultdict(collections.Counter)
models = collections.Counter()
orchestrated = collections.Counter()
for path in root.rglob("*.jsonl"):
    try:
        if path.stat().st_mtime < cutoff:
            continue
        used_orchestrator = False
        rows = []
        with path.open(encoding="utf-8", errors="replace") as handle:
            for line in handle:
                if '"tool_use"' not in line:
                    continue
                try:
                    message = json.loads(line).get("message") or {}
                except ValueError:
                    continue
                for block in message.get("content") or []:
                    if not isinstance(block, dict) or block.get("type") != "tool_use":
                        continue
                    data = block.get("input") or {}
                    if block.get("name") == "Skill" and "orchestrator" in str(data.get("skill", "")):
                        used_orchestrator = True
                    if block.get("name") == "Agent":
                        rows.append(data)
    except OSError:
        continue
    for data in rows:
        kind = data.get("subagent_type") or "(default)"
        key = ("model" if data.get("model") else "no-model", "effort" if data.get("effort") else "no-effort")
        total[key] += 1
        by_type[kind][key] += 1
        models[data.get("model") or "(omitted)"] += 1
        if used_orchestrator and kind.startswith("alaa-"):
            orchestrated[key] += 1
print(f"Agent dispatches in transcripts modified in the last {days:g} days: {sum(total.values())}")
for key, count in total.most_common():
    print(f"  {count:5d}  {key[0]}, {key[1]}")
print("model parameter:", dict(models.most_common()))
print("alaa-* dispatches in sessions that invoked an orchestrator skill:", dict(orchestrated))
print("by agent type (top 12): dispatches | with model | with effort")
for kind, counter in sorted(by_type.items(), key=lambda item: -sum(item[1].values()))[:12]:
    n = sum(counter.values())
    with_model = sum(v for k, v in counter.items() if k[0] == "model")
    with_effort = sum(v for k, v in counter.items() if k[1] == "effort")
    print(f"  {kind:32s} {n:4d} | {with_model:4d} | {with_effort:4d}")
