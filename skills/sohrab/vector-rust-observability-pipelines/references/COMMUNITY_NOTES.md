
# Troubleshooting-only community notes and sharp edges

Use this file only after checking `OFFICIAL_LINKS.md`. These notes capture recurring field symptoms and hypotheses; they are not normative Vector guidance unless official docs or runtime validation evidence confirm them.

Recurring real-world issues to remember:

1. **Experimental sink in fanout can still affect production flow**
   - even with aggressive drop settings, topology-wide behavior may still surprise you
   - isolate critical sinks when necessary

2. **Disk buffer is not magic**
   - it improves durability, but can still stall under capacity/pathology conditions
   - monitor it and size it intentionally

3. **Acknowledgements can reduce throughput**
   - durability is not free
   - validate the path and test failure behavior

4. **Authentication failures plus acknowledgements can be dangerous**
   - understand what the source does when the sink rejects data

5. **VRL test sharp edges**
   - quote hyphenated field names
   - use assertions
   - keep examples realistic

6. **ClickHouse Arrow stream**
   - can be materially faster, but watch current-version schema caveats before broad rollout
