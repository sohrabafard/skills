# Red fixture for check-signoz-links.py

Committed on purpose. Two of these three URLs must produce a finding, and the third must not.
The self-test drives the checker's own judge() over them with a stubbed responder, so it fails
with no network at all. A green checker with no red fixture is decoration.

- must pass: https://example.invalid/good/
- must be reported dead: https://example.invalid/dead/
- must be reported moved, because a silent redirect to a docs index is how a page hides:
  https://example.invalid/moved/page/
- must be skipped as a template, not fetched: https://example.invalid/ingest.REGION.host/
