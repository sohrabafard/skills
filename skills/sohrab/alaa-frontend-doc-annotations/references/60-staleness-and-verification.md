# Staleness and verification

Read this when judging a `verified:` date, when a comment contains one of the freshness-trigger words, or
when reading the checker's output.

## The staleness contract

A comment is a claim with no expiry unless one is written into it. Three claim classes, three rules:

| Claim class | Rule |
|---|---|
| A claim about the code in the same file | Verified by reading the code beneath it. Any pass that touches the file re-reads it; a disagreement is handled by the table in `references/10-annotation-boundaries.md`. |
| A claim about a security, auth or trust assumption | Carries `verified:<ISO-date>`. Mechanically checked against the file's last commit. `ANN301` and `ANN302`. |
| A claim about external behavior — a browser, a framework version, a "current" or "deprecated" behavior | Re-checked against the official source before the comment is written or updated. Freshness triggers are in `references/00-source-map.md`. |

## The git-mtime versus `verified:` test

For each `AUTH NOTE:` and `SECURITY NOTE:`, the checker compares two dates:

```
git log -1 --format=%cI -- <file>     the last time the file's content changed
verified:<YYYY-MM-DD>                 the last time a human or agent checked the assertion
```

**If the commit date is newer than the verified date, the annotation is stale** and the checker reports
`ANN302`. The logic is deliberately blunt: the file changed after someone last confirmed the assertion, so
nobody has confirmed that the change preserved it. It produces false positives — an unrelated edit in the
same file trips it — and that is the correct trade for this claim class. Clearing a false positive costs one
re-read and one date bump; missing a true positive costs an authorization assumption that quietly stopped
holding.

**Filesystem mtime is not used.** A checkout, a rebase, a `git clone` and a formatter all touch mtime
without changing content. `git log -1 --format=%cI` is the only date that means "the content changed". When
git history is unavailable — a tarball export, a shallow clone with no history for the path — `ANN302` is
skipped and the run says so on stderr. Pass `--require-git` in CI to make an unavailable history exit `2`
instead of silently reducing coverage.

## Refreshing a date

**Bumping a `verified:` date is an act of verification, never an act of editing.** To refresh one:

1. Read the assertion and identify the party that provides the guarantee.
2. Confirm the guarantee against that party's current state — the owner skill, the contract, the service's
   own code. Not against the comment, and not against another comment.
3. If it still holds, set `verified:` to today and leave the wording alone.
4. If it no longer holds, do not rewrite the comment to match the new reality on your own authority. Report
   it as a security finding naming the owner from
   `references/40-security-and-trust-annotations.md`. A weakened guarantee is a change to the system, not a
   change to a comment.

A pass that bumps every stale date in a file without step 2 has converted a detector into a rubber stamp,
and the next real staleness will be indistinguishable from the ones already stamped.

## The cross-service blind spot, and what closes it

`ANN302` cannot see a fact that changed in another repository, because this file never changed. That blind
spot is closed by construction, not by detection: a comment cites
`/alaa-services-contract` (`$alaa-services-contract`) as the source of a cross-service value instead of
restating the value. The rule and its worked form are in
`references/40-security-and-trust-annotations.md`. When the contract changes, the contract's own consumer
review is what catches it — which is that owner's existing responsibility rather than a new one.

## Reading the checker

```
node scripts/check-annotations.mjs src/ packages/*/src
node scripts/check-annotations.mjs src/ --rules=ANN301,ANN302
node scripts/check-annotations.mjs --self-test
node scripts/check-annotations.mjs --help
```

**Exit codes.**

| Code | Meaning | What CI does |
|---|---|---|
| `0` | Every assertion passed on every file that was read | Pass |
| `1` | Findings, one `path:line: RULE message` per line on stdout | Fail with the list |
| `2` | Could not run: no such directory, nothing to check, a file that failed to parse, or `--require-git` with no history | Fail loudly. **Never treated as a pass** |

`2` is distinct from `0` on purpose. A checker that exits `0` when it could not read a file teaches CI that
"did not check" and "clean" are the same state, and every later run inherits that lie. The script never
exits `0` with an unparsed file.

**The rules.**

| Rule | Assertion |
|---|---|
| `ANN101` | Every exported function, arrow-const and store action in a module imported by two or more other modules carries a leading `/** ... */` |
| `ANN201` | Every `NOTE:` prefix is one of the closed five |
| `ANN301` | Every `AUTH NOTE:` and `SECURITY NOTE:` carries `verified:<ISO-date>` |
| `ANN302` | That date is not older than the file's last commit |
| `ANN401` | No `@param {Type}` / `@returns {Type}` in a TypeScript context; skipped when `eslint-plugin-jsdoc` `check-tag-names` `typed` is configured, which then owns it |
| `ANN501` | No community or issue-tracker URL inside a comment |
| `ANN601` | Every comment body is ASCII-range |

**Findings are not a licence to edit.** The checker reports; the pass fixes only what
`references/10-annotation-boundaries.md` allows a documentation-only diff to fix. An `ANN101` finding on a
file whose export needs restructuring is a report, not a refactor.

## First-run expectations

A repository meeting this checker for the first time produces a large `ANN601` count and a large `ANN101`
count, and near-zero `ANN201`/`ANN301`. That distribution is the expected shape and is not evidence the
checker is misconfigured: `ANN601` catches typographic characters and Persian text that accumulated
unremarked; `ANN101` catches the export surface that grew faster than its documentation; and `ANN201` and
`ANN301` are quiet precisely because the prefix convention has not been adopted yet, which is what the pass
is there to establish. Fix `ANN601` first — it is mechanical, it never changes meaning, and it clears the
noise that hides the rest.
