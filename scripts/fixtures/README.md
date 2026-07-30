# Fixtures for the fleet-scope checkers

Every assertion the three checkers in `skills/scripts/` make is shown here to fail on an input
that violates it. A green checker with no red fixture reports nothing about the tree; it reports
that it ran.

Run all three:

```
python skills/scripts/check_fleet_references.py --self-test
python skills/scripts/check_skill_index.py --self-test
python skills/scripts/validate_sohrab_skill_pack.py --self-test
```

Each harness exits `0` when every case matched, `1` when a case produced the wrong verdict, and
`2` when a case could not be run at all — a missing fixture, or a target that exited 2 where it
was not expected to. A case that cannot be run is recorded BLOCKED, never FAIL, because "the
fixture is gone" and "the rule is broken" are different facts and a CI gate must not confuse them.

Each fixture is a real repository root, `<case>/skills/sohrab/<skill>/`, so the checkers exercise
their own root discovery rather than a shortcut only the tests use.

## `fleet/` — `check_fleet_references.py`

| Fixture | What it proves |
| --- | --- |
| `green` | the three ordinary citation forms resolve: local, owner-on-the-line, owner-as-path-prefix |
| `green-trap-forms` | the seven shapes that broke earlier resolvers, in one file — see below |
| `green-marked-notation` | `$SKILL_DIR/` resolves and is checked, `<repo>/` is never resolved, and an unmarked target-repository path is informational and does not fail the run |
| `red-r1-dangling-named` | R1 fires both when the owner is a path prefix and when the owner is named on the line, and in neither case does the file exist in that owner |
| `red-r2-dangling-local` | R2 fires on a bare `references/` path that resolves nowhere, and on a `$SKILL_DIR/` path the skill does not ship |
| `red-r3-ambiguous-multi` | R3 fires when two other skills own a file of that name and no owner is named |
| `red-r4-ambiguous-bare` | R4 fires when exactly one other skill owns it and no owner is named in the paragraph |
| `red-r5-contextual` | the owner-named-nearby form passes by default and fails only under `--strict-owner`. Both directions are asserted, because a rule that is off by default still has to work when it is turned on |
| `red-r6-topic-map` | R6 fires when a `references/00-topic-map.md` router points at a file that does not exist |
| `red-undecodable` | a skill shipping invalid UTF-8 with a NUL byte under `assets/fixtures/` is skipped by default, and produces exit **2** — not a crash, not a pass — under `--include-fixtures` |
| `red-no-skills` | a pack directory holding no skill produces exit 2, so a CI gate run from the wrong directory cannot see a pass |
| `red-r4-.../baseline-suppresses.txt` | a baseline entry suppresses its finding and the run reaches 0 |
| `red-r4-.../baseline-stale.txt` | a baseline entry that matches nothing exits **1**, so a baseline can only shrink and never becomes a permanent amnesty |
| `red-r4-.../baseline-malformed.txt` | a baseline the checker cannot parse is exit 2, not a silent empty baseline |

The seven shapes in `green-trap-forms`, each of which produced a false finding in some earlier
generation of this resolver:

1. `` `/owner-skill` (`$owner-skill`) `references/40-proof-strength.md` `` — the token-adjacency
   trap. The owner is named; an intervening backtick and closing parenthesis separate it from the
   path. Requiring adjacency rejected 150 correctly attributed citations fleet-wide and produced
   a reported figure of 582 unresolved paths against a fleet with eight real defects.
2. the owner named *after* the path, in a two-column table.
3. the owner as an explicit path prefix.
4. `references/arvan-caas-openAPI-1.25.json` — an extension alternation with `js` before `json`
   truncated this to `.js` and invented two phantom dangling citations.
5. an illustrative sentence inside a code span, which is an example and not a citation.
6. retirement prose about a file the skill already retired. **The exclusion is same-line only**:
   the retiring words and the path must share a line. Widening it across a line break would
   suppress a genuine broken citation that happens to follow a sentence containing "was", and
   false suppression is the one direction a checker must not fail in.
7. a `../` path resolved against the citing file's directory rather than the skill root.

## `index/` — `check_skill_index.py`

| Fixture | What it proves |
| --- | --- |
| `green` | a pack whose two indexes and disk agree in both directions passes |
| `green-bridged` | a `CLAUDE.md` whose first line is `@AGENTS.md` satisfies X6 and X7 |
| `green-marked-map` | the map is read from `<!-- skill-map:start -->` / `<!-- skill-map:end -->` when present |
| `green-crlf-agents` | a CRLF `AGENTS.md` beside an LF `CLAUDE.md` with identical content **passes**. This is the live state of the repository root, and a byte comparison would fail here for the wrong reason while masking a real divergence later |
| `red-x1-dir-not-in-readme` | X1 fires on a directory the English map omits |
| `red-x2-readme-name-not-a-dir` | X2 fires on a map name with no directory |
| `red-x3-dir-not-in-readme-fa` | X3 fires on a directory the Persian tables omit |
| `red-x4-readme-fa-name-not-a-dir` | X4 fires on a Persian table name with no directory |
| `red-x5-consolidated-still-exists` | X5 fires when a name listed as removed still has a folder |
| `red-x6-agents-claude-diverged` | X6 fires when the root pair differ in content and no bridge joins them |
| `red-x7-claude-md-stub` | X7 fires on a 9-byte `skills/sohrab/CLAUDE.md` whose entire content is `AGENTS.md` — what a git mode-120000 symlink becomes on a Windows checkout without `core.symlinks`, loaded silently in place of the contract |
| `red-x8-missing-openai-yaml` | X8 fires on a skill with no `agents/openai.yaml`, and its three baseline files prove suppression, staleness and malformed-baseline handling |
| `red-x9-duplicate-in-index` | X9 fires when a name is listed twice, which is the other half of "appears exactly once" |
| `red-no-map-region` | exit 2 when neither the markers nor the `## Current skill map` heading can be found |
| `red-missing-readme-fa` | exit 2 when an index the rule needs is absent |
| `red-no-skills` | exit 2 on a pack directory with no skill in it |

Two parsing decisions are load-bearing and each has a fixture behind it:

- The first cell of a Persian table row may name **more than one** skill. `README.fa.md:99` reads
  ``| `ansible-generator` / `ansible-validator` | ... |``. Reading only the first name reported
  two real skills as missing from the index.
- In "Consolidated or removed from this pack", only the names **before** the separator were
  removed; the names after it are what replaced them. Taking every backticked token on the line
  reported the replacing skill as removed, which fires on all four bullets of the live
  `README.md`.

## `validator/` — `validate_sohrab_skill_pack.py`

| Fixture | What it proves |
| --- | --- |
| `green` | a valid skill passes |
| `green-unquoted-scalars` | **the regression fixture.** `short_description` and `default_prompt` written as unquoted YAML scalars are read correctly. The previous version extracted them with a regex requiring double quotes and therefore reported two errors per skill against valid YAML |
| `green-flow-mapping` | a single-line `interface: {…}` flow mapping is read correctly |
| `green-block-scalar` | folded (`>-`) and literal (`|-`) block scalars are read correctly |
| `green-repo-notation` | `<repo>/` and `$SKILL_DIR/` citations are inert here, so adopting the notation cannot break this validator |
| `green-sequence-of-mappings` | **the regression fixture for this batch.** A block sequence of mappings — `- domain: …` with a sibling `route_to:` at the column of the text after the dash — is read correctly, as is a folded scalar under default clip chomping. The bundled parser rejected that sequence form, so one real file in the fleet returned exit 2 against valid YAML |
| `red-short-description-too-short` | V7 still fires on a genuinely out-of-range value, written unquoted — the fix removes false positives without removing the rule |
| `red-default-prompt-no-sigil` | V8 fires when the prompt does not name `$<skill>` |
| `red-missing-when-not-to-use` | V3 fires on a body whose only negative-scope heading is "What this skill does not decide" |
| `red-missing-openai-yaml` | V6 fires |
| `red-broken-reference-path` | V5 fires |
| `red-topic-map-path-missing` | V9 fires |
| `red-description-over-hard-max` | a 1100-character description is an error |
| `warn-description-over-target` | a 940-character description is a **warning** and the run still exits 0, at the 900 target rather than the old 950 |
| `warn-body-over-120-lines` | V4 warns and does not fail |
| `red-registry-unregistered-metric` | V10 fires when `alaa-services-contract` names an `alaa_*` metric with no registry row |
| `red-unparseable-openai-yaml` | a YAML anchor — outside the supported subset — produces exit **2** naming the file, never a silent pass |
| `red-unparseable-sequence-indent` | a sequence item whose sibling key is indented one space too deep produces exit **2**. PyYAML rejects this file too, so it is malformed YAML rather than an unsupported construct: it is the red half of `green-sequence-of-mappings`, and it proves the new sequence support did not become "accept any indentation" |
| `red-unparseable-frontmatter` | a tab used for indentation produces exit 2. Measuring only the leading *spaces* reported indent 0 and silently promoted a tab-indented nested key to a top-level key |
| `red-empty-pack` | a pack directory with no skill produces exit 2, not 0 |

Three tables in that self-test assert the bundled parser directly, because a pack fixture only
exercises the handful of keys the rules happen to read.

- **`mini-yaml:`, 8 cases** — one scalar value read out of one key: plain, double-quoted,
  single-quoted with a doubled quote, folded, literal, single-line flow, a trailing comment on a
  plain scalar, and a `#` inside a quoted scalar that is not a comment.
- **`mini-yaml structure:`, 12 cases** — whole parsed objects, which is the only way a collection
  shape is visible at all: sequences of mappings and of scalars, a sequence at its parent key's own
  column, a bare dash whose value is the block below it, extra spaces after the dash, a mapping
  nested inside a sequence item, and all three chomping indicators including an unterminated final
  line. Every expected value was confirmed identical to PyYAML's parse of the same text.
- **`mini-yaml rejects:`, 16 cases** — inputs that must raise. Each is either malformed YAML that
  PyYAML also rejects, or a construct outside the subset that would otherwise be coerced to a wrong
  value. This is the half that keeps exit 2 reachable: a parser that guesses at malformed YAML
  reports a rule verdict on a value the file does not carry.

PyYAML is the oracle for those expected values and is deliberately never imported at runtime.
Importing it when present would fork behaviour, so a file the fallback rejects would pass on a
laptop and fail in CI.
