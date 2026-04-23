
# Troubleshooting-only community notes and sharp edges

Use this file only after checking `OFFICIAL_LINKS.md`. These notes capture recurring field symptoms and hypotheses; they are not normative ClickHouse guidance unless official docs or live cluster evidence confirm them.

These are the recurring field problems worth remembering:

1. **Too many parts**
   - usually traces back to tiny frequent inserts and partition explosion
   - fix ingest shape before chasing query knobs

2. **PRIMARY KEY misconceptions**
   - it does not enforce uniqueness
   - it is not a classic B-tree lookup structure

3. **Skip indexes are not row-store secondary indexes**
   - they help block pruning in the right situations
   - they are not a universal filter accelerator

4. **Join pain**
   - broad joins and late filtering can blow memory or scan too much
   - ClickHouse rewards precomputation and smarter data layout

5. **Materialized view backfills**
   - initial population and complex joins can be memory intensive
   - stage backfills and validate with smaller windows first

6. **Avoid NULL unless semantics truly matter**
   - Nullable has real storage and performance cost
