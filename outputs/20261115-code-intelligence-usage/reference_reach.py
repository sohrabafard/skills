#!/usr/bin/env python3
"""Which orchestrator references a lead opened, per session that invoked alaa-cc-orchestrator. Read-only.
Usage: reference_reach.py [days] [--all]. Without --all, sessions of the skills repository are left out,
because opening these files is the work itself there."""
import json, sys, glob, os, time, re, collections
days = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 7
cut = time.time() - days * 86400
REFS = ["verification-and-gates.md", "routing-matrix.md", "delegation-prompts", "agent-catalog.md", "model-effort-policy.md",
        "resource-policy.md", "failure-taxonomy.md", "workspace-and-integration.md", "review-mode.md", "task-tracking.md",
        "100-test-execution.md", "120-result-classification.md", "artifact-lifecycle.md", "context-continuity.md", "companion-routing.md"]
REVIEW = re.compile(r"reviewer|critic|guardian|auditor|verifier")
sessions = 0; reach = collections.Counter(); with_review = 0; review_read_gates = 0; review_read_tmpl = 0
with_impl = 0; impl_read_matrix = 0; with_fix_after_review = 0; fix_read_gates = 0; loaded_ts = 0
projects = collections.Counter()
for p in glob.glob(os.path.expanduser("~/.claude/projects/*/*.jsonl")):
    if os.path.getmtime(p) < cut: continue
    if "--all" not in sys.argv and os.path.basename(os.path.dirname(p)).endswith("-skills"): continue
    orch = False; read_at = {}; first_review = None; first_impl = None; fix_after = None; n = 0; ts_skill = False
    try: fh = open(p)
    except OSError: continue
    for line in fh:
        if '"tool_use"' not in line: continue
        try: d = json.loads(line)
        except Exception: continue
        if d.get("type") != "assistant" or d.get("isSidechain"): continue
        for x in (d.get("message") or {}).get("content") or []:
            if x.get("type") != "tool_use": continue
            n += 1; name = x.get("name"); inp = x.get("input") or {}
            if name == "Skill":
                if inp.get("skill") == "alaa-cc-orchestrator": orch = True
                if inp.get("skill") == "alaa-testing-strategy": ts_skill = True
            elif name in ("Read", "Bash", "Grep"):
                s = str(inp.get("file_path") or inp.get("command") or inp.get("path") or "")
                if "skills" in s or "references" in s:
                    for r in REFS:
                        if r in s: read_at.setdefault(r, n)
            elif name == "Agent":
                t = str(inp.get("subagent_type") or "")
                if REVIEW.search(t) and first_review is None: first_review = n
                if "implementer" in t:
                    if first_impl is None: first_impl = n
                    if first_review is not None and fix_after is None: fix_after = n
    if not orch: continue
    sessions += 1; loaded_ts += ts_skill; projects[os.path.basename(os.path.dirname(p)).split("-project-")[-1]] += 1
    for r in read_at: reach[r] += 1
    if first_impl is not None:
        with_impl += 1; impl_read_matrix += read_at.get("routing-matrix.md", 10**9) < first_impl
    if first_review is not None:
        with_review += 1
        review_read_gates += read_at.get("verification-and-gates.md", 10**9) < first_review
        review_read_tmpl += read_at.get("delegation-prompts", 10**9) < first_review
    if fix_after is not None:
        with_fix_after_review += 1
        fix_read_gates += (read_at.get("verification-and-gates.md", 10**9) < fix_after) or (read_at.get("review-mode.md", 10**9) < fix_after)
print(f"lead sessions that invoked alaa-cc-orchestrator in {days} days: {sessions}; of those loaded alaa-testing-strategy by Skill: {loaded_ts}")
for r in REFS: print(f"  opened {r}: {reach[r]}")
print(f"sessions with an implementer dispatch: {with_impl}; routing-matrix opened before the first one: {impl_read_matrix}")
print(f"sessions with a review-role dispatch: {with_review}; verification-and-gates opened before it: {review_read_gates}; a delegation-prompts file opened before it: {review_read_tmpl}")
print(f"sessions with an implementer dispatch after a review dispatch: {with_fix_after_review}; gates or review-mode opened before it: {fix_read_gates}")
print("sessions by project:", dict(projects))
