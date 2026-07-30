# Final Checks Before a Query Ships

Read this before pasting SQL into a production dashboard panel or an alert rule.

Most of what used to be on this list is now executed rather than recited: `SKILL.md` names the three
checkers, their invocations and their exit codes, and `check-signoz-sql.py --help` lists the eleven
rules it enforces. Run them first. **A `2` from any checker is not a pass** — say which one could not
run and treat every assertion it would have made as unverified.

Then spend the reading time on the four judgements no tool can make.

**1. Is this the signal that answers the question?** A checker confirms the SQL is valid against the
logs schema; it cannot tell you the question was about spans. Name the signal, and why, before the
SQL.

**2. Is the window the window the user meant?** Every panel returns something. A query bounded to one
hour when the incident was yesterday returns a clean, empty, convincing panel. State the window in
the answer so the reader can reject it.

**3. Would this output disclose something the requester did not ask to see?** Log bodies, full URLs
and forensic tables are the cases. A query can be correct, cheap and index-supported and still put
customer text on a shared dashboard. When it might, say so and offer the aggregate form.

**4. Is any part of this unverified?** Name it. An answer that says which table it could not confirm
is usable; one that quietly assumed a table is not, and the assumption surfaces as a production panel
error instead of as a question.

## The answer shape

```text
Surface: Dashboard panel ClickHouse | Query Builder | Docs lookup
Signal: logs | traces | metrics
Window: ...
Assumptions and placeholders: ...
SQL:
...
Checked: check-signoz-sql.py exit <code>, findings: ...
Unverified: ...
```

`Alert ClickHouse` is deliberately absent from that list. Read the alert-surface gate in `../SKILL.md`
before offering it.
