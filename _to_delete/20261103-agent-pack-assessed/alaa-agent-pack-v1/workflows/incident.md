# Incident / difficult bug
Lead records impact, timeline, scope and authorized operations. A debugger owns
hypotheses and reproduction; an observability investigator reconstructs trace/log
evidence; a relevant data/runtime specialist checks a disjoint cause if useful.
Investigators do not patch concurrently. Pick a root cause from evidence, assign
one writer for the minimal fix, add a discriminating regression, verify and hand off.
Escalate to Astra when evidence conflicts or the failure spans difficult concurrency
boundaries. Do not replace missing telemetry with a confident story.
