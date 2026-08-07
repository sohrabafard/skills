# Store Adapter: Local File Vault

Mechanics for reading and writing the vault with ordinary file tools and no index server. Everything here dies
with the store; nothing here is policy. The policy is in `SKILL.md`, `references/knowledge-shape.md`, and
`references/drift-management.md`.

**This is the active adapter.** The Basic Memory CLI is being retired; `references/store-basic-memory.md` stays
for the period while `bm` is still installed and for anyone who reinstates it. Nothing was migrated when the tool
was dropped, because the tool was never where the notes lived.

## What the store actually is

`D:/Sohrab/Project/agent-memory` — plain markdown notes in a git repository, roughly 140 of them at the time of
writing. Basic Memory indexed this directory; it never owned it. The consequence worth internalising: **dropping
the index loses search, not content**, and every note remains readable by any agent in any runtime that can read
a file, which is the property the server-backed adapter never had.

Top-level layout, which is also the routing map for recall:

```text
00-control/    governance, playbooks, templates, conventions
architecture/  system maps, service ownership, topology
contracts/     contract cards — envelopes, codes, queues, SDK surfaces
drift/         drift records and the drift registry
lessons/       durable lessons, including project-scoped subdirectories
patterns/      repeated work patterns
projects/      one directory per project: Project Index, Current State, Contracts
handoffs/      concise continuation pointers
operations/    runbook-adjacent operational knowledge
research/      external research worth keeping
inbox/         uncurated captures awaiting a home
archive/       superseded notes, kept rather than deleted
```

## Recall

Search the tree, then read only the matching note. There is no ranking, so the query has to carry the
discrimination that a hybrid search used to.

```powershell
# by topic, across the vault
rg -i -l "notification command contract" D:/Sohrab/Project/agent-memory

# by lifecycle field, which is ordinary frontmatter here
rg -l "^status: needs_review" D:/Sohrab/Project/agent-memory

# by relation, to walk the graph by hand
rg -l "\[\[Alaa System Architecture Map\]\]" D:/Sohrab/Project/agent-memory

# what changed recently, the replacement for recent-activity
git -C D:/Sohrab/Project/agent-memory log --oneline -20 --name-only
```

Three recall behaviours change, and pretending they did not is how an agent reports a miss as an absence:

- **No semantic search.** A note about "pool exhaustion" will not surface for a query about "connection
  starvation". Search two or three phrasings before concluding a topic is unrecorded, and say "not found under
  these terms" rather than "not recorded".
- **No `build_context` traversal.** Relations are `[[wikilinks]]` in the body; follow them by searching for the
  target title. One hop is cheap, three is a research task — budget accordingly.
- **Recall still fails open**, and now it rarely needs to: a file search over a few hundred notes returns well
  inside the five-second budget `SKILL.md` sets. The budget is no longer the binding constraint; query quality is.

## Writing

Create or edit the file directly. Search before creating, as `references/knowledge-shape.md` requires — without an
index, a duplicate is harder to notice later, not easier.

- Path is `<folder>/<Title With Spaces>.md`, matching the existing convention; the title in frontmatter and the
  filename stay in step.
- Frontmatter carries `title`, `type`, `permalink`, `status`, `confidence`, `tags`, and — for anything derived
  from a source — `canonical_source_paths` and `last_verified`.
- Keep `permalink` stable and in the `alaa-memory/<folder>/<slug>` shape already used across the vault, so a
  future indexed store can adopt the vault without rewriting every cross-reference.
- Write UTF-8 without a byte-order mark. A mark immediately before the YAML delimiter breaks the frontmatter
  parse, and on Windows PowerShell 5.1 `Set-Content -Encoding UTF8` emits one.

**Commit every new or changed note in the same session.** This is the one operational rule that has no equivalent
in the server-backed adapter: with an index server, an unsynced note was still on disk; here, an uncommitted note
in a git-backed vault is one `git clean` away from gone, and nothing will report it missing.

```powershell
git -C D:/Sohrab/Project/agent-memory add -A
git -C D:/Sohrab/Project/agent-memory commit -m "memory: <what changed and why>"
```

## What is lost, and what replaces it

| Retired | Replacement |
|---|---|
| `bm tool search-notes` | `rg` over the vault, two or three phrasings |
| `bm tool build-context` | follow `[[wikilinks]]` by title search |
| `bm tool recent-activity` | `git log --name-only` |
| `bm doctor`, `bm orphans` | a link check over `[[...]]` targets, when one is worth writing |
| `bm schema validate` / `diff` | frontmatter review at write time; no automated schema gate |
| `bm reindex` | nothing to reindex |

The schema gate is the real loss. Without it, a malformed or missing frontmatter field is found by a reader
rather than by a checker, so the write-time discipline in `references/knowledge-shape.md` carries weight it did
not have to carry before. Treat a note you are editing as a chance to fix its frontmatter.

## Concurrency

Unchanged from the file-backed store, and now the only mechanism: two agents writing the same note is
last-writer-wins with no warning and no merge. One agent owns a note during a task; an agent that must update a
note it did not read this session re-reads it immediately before writing; a note written by a hook goes to
`inbox/` with a unique filename rather than into an existing note. Git makes a clobber recoverable, which is a
reason to commit often rather than a reason to be careless.

## Security

The vault is a directory on disk with no listening socket, no authentication surface, and no network transport —
the whole class of exposure that `SKILL.md` warns about for a server-backed store does not exist here. The sink
rule is unchanged and absolute: never write a secret, credential, token, cookie, or private key into a note. It
is in git, which means a secret written once survives its deletion.
