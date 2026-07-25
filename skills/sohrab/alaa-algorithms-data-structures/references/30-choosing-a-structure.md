# Choosing A Structure

Load when a collection is introduced, when a lookup is added over an existing one, or when a structure is being
changed for speed.

`SKILL.md` owns the rule — the structure follows the access pattern, not the shape of the data — and the five
questions that produce the answer. This file maps answers to structures, covers the cases that actually appear in
service code, and states the normalisation rules a key must satisfy.

No language is named here. `/golang-data-structures` (`$golang-data-structures`) owns Go internals and the
per-language clean-code skills own each language's idiomatic equivalent of every row below.

## Access pattern to structure

| Access pattern | Structure | Why the obvious alternative loses |
|---|---|---|
| Repeated lookup by one key over one collection | Map keyed by that key, built once before the loop | Searching the list per lookup multiplies the loop by the list |
| One lookup, collection used once | The sequence as it arrived | Building an index for one lookup costs more than the lookup |
| Membership only, values unique | Set | A list makes each check proportional to the list, and permits a duplicate nobody notices |
| Ordered output, order known at query time | Ordered at the source: `ORDER BY`, or one sort before the loop | Re-sorting inside iteration repeats the sort per element |
| Ordered output, order changes as elements arrive | A structure that maintains order on insert | Re-sorting after each insert converts inserts into sorts |
| Reached only by position, size known | A fixed-size sequence, preallocated | Growing a sequence element by element repeatedly copies it |
| Grouped by a key, then iterated per group | Map from key to sequence, built in one pass | Filtering the whole collection once per group multiplies passes by groups |
| Highest or lowest few from a large set | Bounded selection: the query's `ORDER BY ... LIMIT`, or a bounded structure | Sorting everything to take the first few pays for the whole set |
| Key present in the authoritative store, not in memory | An index on that column, and a query | An in-memory copy is a cache — see below |

## The four everyday cases

**Repeated lookup in a list that should be a map.** The most common structure defect in service code: a collection
is fetched, then searched once per element of another collection. The two collections are usually small in
development and both grow in production, so the cost grows with their product. The fix is one pass to build the
map, then one lookup per element. Apply it when the lookup happens more than once over the same collection; a
single lookup does not justify an index.

**Ordered versus hashed.** Hashed structures answer "is this key present" and nothing about order; ordered
structures answer range and neighbour questions and cost more to maintain. Choose hashed unless the code asks a
range question, a nearest question, or iterates in a defined order — and when it does iterate in a defined order,
say where that order comes from. Iterating a hashed structure and relying on the order it happens to produce is a
defect that surfaces as an intermittently different output.

**Set versus list for membership.** A list used for membership has two costs, and the second is the one that
matters: each check is proportional to the list, and duplicates are silently permitted. When the collection
represents a set of things — permission names, tenant identifiers, deduplicated keys — the set both bounds the check
and makes the duplicate impossible to insert.

**When the answer is a database index.** When the authoritative copy of the data lives in the store and the lookup
key is a column, the right structure is an index on that column plus a query — not an in-memory map. An in-memory
map of a table is a cache with no invalidation: its memory grows with the table rather than with the request, it is
stale the moment another replica writes, and every replica holds its own copy. Index design, keyset pagination, and
cache semantics belong to `/alaa-data-layer` (`$alaa-data-layer`); this file owns only the rule for when to stop
reaching for an in-memory structure.

## Keys must be normalised

**Every value used as a map key, set member, deduplication key, or comparison key has a stated normalisation applied
before that use.** Without one, two values a human calls equal produce different keys, and the failure is silent: a
duplicate row, a second notification, an idempotency check that misses, a cache that never hits.

State the normalisation for each of these where the key involves it:

- **Composite keys** — the field order in which the parts are combined, and the separator, chosen so no field value
  can contain the separator and forge a different key.
- **Text** — Unicode normalisation form, and whether case is folded. Fold case only where two casings genuinely name
  the same thing; folding a case-sensitive identifier merges two distinct records.
- **Absent versus empty** — one of `null`, missing, and empty string is chosen as the canonical form and the others
  map onto it, or all three produce different keys for the same state.
- **Numbers** — one representation. An integer and its decimal string are two keys for one value.
- **Timestamps** — one timezone and one precision. The same instant in two offsets is two keys.
- **Collections inside a key** — whether element order is significant. When it is not, the elements are sorted
  before the key is built.

`/alaa-controlled-ops` (`$alaa-controlled-ops`) specifies exactly this for that package's digests, in full detail
including function and encoding. Read it there when working on that package; the obligation stated here is the
general one and applies to every map, set, cache key, and uniqueness check in the estate.

## Recording the choice

Record, beside the structure, the alternative rejected and the condition that would revive it — "a list, revived if
the lookup becomes single-use"; "an in-memory map, revived if the table becomes immutable reference data". A choice
with no rejected alternative cannot be reviewed, because the reviewer cannot tell what was considered, and it cannot
be revisited, because nobody knows what would change the answer.

## Anti-patterns

- choosing the structure from the shape the data arrived in, so a JSON array becomes a list regardless of how it is
  used;
- building an index for a single lookup;
- an in-memory copy of a table described as a performance optimisation with no invalidation, no maximum size, and no
  eviction;
- relying on a hashed structure's iteration order;
- a set replaced by a list because the language's list literal is shorter to write;
- a composite key built by concatenation with a separator that can appear inside a field;
- a structure chosen for speed with no budget stating what it is faster than, and at what input size.
