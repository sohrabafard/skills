# The fleet cross-reference census, measured 2026-07-29

`check_fleet_references.py --census` prints the classification histogram for whatever tree it is
pointed at. This file records the measurement the checker was built to reproduce, so that a future
run can be compared against a known state rather than against an impression.

This is a **snapshot, not an invariant.** It is deliberately not asserted by `--self-test`: an
assertion on fleet-wide counts fails on every legitimate edit to any of 805 Markdown files, and a
check that must be edited whenever the tree changes correctly gets ignored. The self-test asserts
counts on the fixture corpus, which this repository controls. Compare the numbers below by hand
when the resolver changes.

## Command

```
python skills/scripts/check_fleet_references.py --census
```

## Scoped to `references/` — the number the carry-over asked for

`references/` is the only bundled-resource prefix that is unambiguously skill-bundled.

| Class | 2026-07-29 |
| --- | ---: |
| RESOLVES-LOCALLY | 1469 |
| RESOLVES-CROSS-SKILL | 625 |
| RESOLVES-CROSS-SKILL-CONTEXTUAL | 150 |
| AMBIGUOUS-BARE | 3 |
| AMBIGUOUS-MULTI | 4 |
| DANGLING | 1 |
| **TOTAL** | **2252** |

The survey read those figures as eight real defects fleet-wide, 3 + 4 + 1, and concluded that
those eight were the whole default finding set. **That conclusion did not survive measurement; see
"Measured 2026-07-30" below.** The tool's own default run reports 17 findings on the pre-batch tree
and 30 on the tree of 2026-07-30. Shipping no baseline is still the right call, because 13 of the 30
were introduced by this batch and are a one-line notation edit each, but it is not true that the
default finding set is eight.

The 150 CONTEXTUAL citations are the trap. An earlier resolver counted them as failures and
reported 582 unresolved paths. They are correctly attributed prose: the owner is named, just not
adjacent to the path. `alaa-frontend-developer` carries 58 of the 150, so `--strict-owner`
belongs in CI only after that one skill's citations are converted.

## All bundled-resource prefixes

| Class | 2026-07-29 |
| --- | ---: |
| RESOLVES-LOCALLY | 2059 |
| RESOLVES-CROSS-SKILL | 644 |
| RESOLVES-CROSS-SKILL-CONTEXTUAL | 154 |
| AMBIGUOUS-BARE | 4 |
| AMBIGUOUS-MULTI | 5 |
| DANGLING | 89 |
| **TOTAL** | **2955** |

Only 8 of those 2955 citations are Markdown links. A link checker built on Markdown link syntax
inspects 0.27% of this fleet's cross-references, which is why this checker reads raw text.

## Two deliberate differences from the 2026-07-29 numbers

Both are stated here so a future comparison is not read as a regression.

1. **`docs/`, `test/`, `tests/`, `ci/` and `charts/` are inside the scanned directory
   alternation.** Adding `docs` alone raised the 2026-07-29 DANGLING count from 89 to 520, of
   which 422 were `docs/…`. Those were never links: they name files the agent is told to write in
   the repository it is working on. Under this checker they are not dangling and not excluded —
   they are `I1-UNMARKED-TARGET-PATH`, informational, and they never fail the run. Expect roughly
   519 informational items on first adoption, falling by one for every citation rewritten as
   `<repo>/…`. That is the mechanism by which the notation is adopted incrementally instead of in
   one 520-file commit, and it is why there is no exclusion list.

2. **A citation that names one or more other skills, none of which owns the path, is
   `R1-DANGLING-NAMED` rather than `AMBIGUOUS-MULTI`.** The 2026-07-29 run classified
   `alaa-cicd-laravel-postgres/references/90-source-map.md:10` as AMBIGUOUS-MULTI because
   `references/SOURCES.md` exists in nine skills, while the line explicitly names
   `alaa-gitlab-ci-cd`, which does not have it. The survey called that out as a real defect masked
   by the multi-owner ambiguity. Checking the named owner first unmasks it. The total finding count
   is unchanged at eight; one finding moves from R3 to R1.

## The two path notations this checker introduces

| Notation | Meaning | Checked? |
| --- | --- | --- |
| `$SKILL_DIR/<path>` | a path bundled inside the citing skill | yes — a missing file is `R2` |
| `<repo>/<path>` | a path in the target repository the agent is working on | never resolved, never a finding |

Neither is invented here. `$SKILL_DIR/` is already used at nine sites in
`alaa-postman-collections`; `<repo>/` is already used in
`alaa-postman-collections/references/70-aggregate-collections-and-consumer-repos.md` and in
`vector-rust-observability-pipelines/INSTALL.md`. Marking a citation removes it from the bare-path
scanner entirely, and both notations are inert to `validate_sohrab_skill_pack.py`. Adoption is
incremental with exactly one exception, measured 2026-07-30 and stated under "The promotion rule"
below: a line that names an owning skill and also names a target-repository path has no passing
unmarked state.

**Still required, and outside this lane's write scope:** one paragraph in
`skills/sohrab/AGENTS.md` stating the pair, so a skill author can discover the notation by reading
the contract rather than by reading a checker's `--help`.

## Measured 2026-07-30 — the first run of this tool against the real 67-skill tree

The 2026-07-29 figures above were inherited from the Phase 1 survey and were produced by that
survey's resolver, not by this tool: the bridge was down when this tool was written, so it had never
been run against the tree. It has now. **Where the two disagree, the figures below are the measured
ones and the table above is the survey's.**

Measured against a local snapshot of `skills/sohrab` verified byte-identical to the mount by
`sha256sum` over all 829 Markdown files. The snapshot exists only because the repository is on a
FUSE-mounted Windows filesystem. One full run makes 27,420 `is_file()` calls, counted by wrapping
`pathlib.Path.is_file`, and that mount was measured at 8.17 ms per stat: 224 seconds of stat alone,
well past any usable timeout. The snapshot changes no result, because the content is identical and
resolution only ever asks `is_file()`.

| Class, scoped to `references/` | survey 2026-07-29 | pre-batch tree, this tool | 2026-07-30 tree |
| --- | ---: | ---: | ---: |
| RESOLVES-LOCALLY | 1469 | 1458 | 1471 |
| RESOLVES-CROSS-SKILL | 625 | 461 | 473 |
| RESOLVES-CROSS-SKILL-CONTEXTUAL | 150 | **150** | 156 |
| AMBIGUOUS-BARE | 3 | **3** | 4 |
| AMBIGUOUS-MULTI | 4 | 1 | 0 |
| DANGLING | 1 | 3 | 3 |
| DANGLING-NAMED | not listed | 1 | 1 |
| SKIPPED-COMMAND-EXAMPLE | not listed | 163 | 169 |
| SKIPPED-RETIREMENT-PROSE | not listed | 13 | 13 |
| TOTAL as this tool prints it | — | 2253 | 2290 |

"Pre-batch tree" is `git archive HEAD` at 2026-07-26, read with this tool. It separates a resolver
difference from a tree difference, which a single run cannot do.

**What reproduces.** CONTEXTUAL is 150 and AMBIGUOUS-BARE is 3 on the pre-batch tree, exactly the
survey's numbers. The 150 contextual citations are therefore confirmed as a real class and not an
artefact, and the earlier resolver's 582 false failures were indeed this class. The form was
verified on real text at
`skills/sohrab/jitsi-platform-architect/references/20-failure-classes.md:26`, which reads
`` `/alaa-reliability-sla` (`$alaa-reliability-sla`) `references/20-retries.md`. `` — a backtick and
a closing parenthesis sit between the owner and the path. The owner does own the path, and this
tool reports nothing there even under `--strict-owner`, so the owner is being read as named on the
line rather than merely nearby.

**What does not reproduce.** RESOLVES-CROSS-SKILL is 461 against a recorded 625, on the same-era
tree, so that gap is a resolver difference and not a tree change; the survey's 625 should not be
quoted again. DANGLING is 3 against a recorded 1. AMBIGUOUS-MULTI is 1 against a recorded 4, of
which one step is the documented R3-to-R1 reclassification and two are unexplained.

**The TOTAL rows above are not comparable.** The survey's 2252 is the sum of the six classes it
listed; this tool's TOTAL sums all twelve classes it prints. Comparing the two TOTALs suggests a
+38 drift where the like-for-like comparison of those six classes is 2252 against 2107. Read the
per-class rows, never the TOTAL.

## Findings, measured, and who owns them

30 findings on the 2026-07-30 tree: 18 R1-DANGLING-NAMED, 5 R6-TOPIC-MAP, 4 R4-AMBIGUOUS-BARE,
3 R2-DANGLING-LOCAL. Against the pre-batch tree the same tool reports 17. Differencing the two by
finding key splits them:

- **16 inherited and still present**, owned outside this batch: `alaa-cicd-laravel-postgres`,
  `alaa-go-chi-development`, `alaa-laravel-upgrade-all-packages`, `alaa-minio-object-storage`,
  `alaa-services-contract` (R1 and R6 on the same citation), `alaa-sms-provider-mediana`,
  `caas-arvan-kuber` (2), `service-runtime-kit-governance`, `alaa-laravel-job-rabbitmq` (2),
  `ansible-validator`, and `alaa-shaka-player` (3).
- **13 introduced by this batch**: 12 in `alaa-repo-docs` and 1 in `alaa-postman-collections`. Every
  one is a `docs/…` target-repository path written without the `<repo>/` marker this batch
  introduced. Marking each retires the finding.
- **1 reclassified, same site**: `alaa-indexeddb-browser-storage/references/99-sources-and-maintenance.md:74`
  moved from R3-AMBIGUOUS-MULTI to R4-AMBIGUOUS-BARE because fewer skills now own
  `references/full-guide.md`. Same defect, narrower class.

**A classification interaction worth the tool owner's attention.** An unmarked target-repository
path is meant to land in the informational `I1-UNMARKED-TARGET-PATH` class, which never fails a
run. It does so only when no other skill is named on the line. Name one — as `alaa-repo-docs`
does throughout — and the same path is promoted to R1-DANGLING-NAMED, which does fail. That is why
one batch's routing sentences turned 13 informational items into hard findings without anyone
citing a new path. The incremental-adoption property the notation was designed for does not hold
on a line that also routes to another skill.


## Measured 2026-07-30, second run: after the 13 batch findings were closed

Same method as the first run of that day: a local snapshot of `skills/sohrab`, verified
byte-identical to the mount by `sha256sum` over all 869 Markdown files, because one run against
the FUSE-mounted Windows filesystem exceeds the shell timeout.

| | before | after |
| --- | ---: | ---: |
| findings, total | 30 | **17** |
| R1-DANGLING-NAMED | 18 | 9 |
| R2-DANGLING-LOCAL | 3 | 3 |
| R4-AMBIGUOUS-BARE | 4 | 4 |
| R6-TOPIC-MAP | 5 | 1 |
| I1-UNMARKED-TARGET-PATH, informational | 354 | 338 |
| citations classified | 3374 | 3383 |

All 17 remaining findings belong to skills outside Batch 8: `alaa-shaka-player` (3),
`alaa-services-contract` (2, R1 and R6 on one citation), `caas-arvan-kuber` (2),
`alaa-laravel-job-rabbitmq` (2), and one each in `alaa-cicd-laravel-postgres`,
`alaa-go-chi-development`, `alaa-indexeddb-browser-storage`,
`alaa-laravel-upgrade-all-packages`, `alaa-minio-object-storage`,
`alaa-sms-provider-mediana`, `service-runtime-kit-governance`, `ansible-validator`.
`alaa-repo-docs` and `alaa-postman-collections` report zero.

`alaa-repo-docs` still carries 91 informational unmarked target paths and
`alaa-postman-collections` 3. Those are the notation's remaining adoption work, not findings.
This lane marked only the sites carrying a finding plus the target paths in the same table or
list, because a half-marked list misinforms a reader within one glance while a half-marked
document does not.

## The promotion rule: measured, and deliberately left alone

Two fixes were available for the 13 findings Batch 8 introduced into its own skills.

**(a) Mark the thirteen lines `<repo>/`.** Correct regardless of anything else: these are
target-repository paths and the notation exists to say so. Done 2026-07-30.

**(b) Stop promoting an unmarked path to `R1-DANGLING-NAMED` merely because a skill is named on
the same line, when the path's leading segment is not a skill-bundled prefix.** Considered and
**rejected**, for a measured reason rather than a preference.

The case for (b) is strong and should not be lost. `R1` exists to catch a citation that lies about
where a bundled file lives -- `alaa-foo references/20-bar.md` where `alaa-foo` has no such file. A
`docs/...` path is not that shape, so promoting it conflates two different defects. Worse, the
promotion is not a function of the property it claims to measure. In
`alaa-postman-collections/SKILL.md` before this edit, one list of four target-repository documents
was split across two physical lines at column 88:

    - repository documentation, including `README.md`, `docs/BIG_PICTURE.md`,
      `docs/api-summary.md`, and `remaining-task.md`: `alaa-repo-docs` owns those; this skill

`docs/BIG_PICTURE.md` on the first line was `I1`, informational. `docs/api-summary.md` on the
second was `R1`, a hard finding. One list, one author, one semantics, one line-wrap apart. A gate
whose verdict changes when a paragraph is reflowed is reporting noise on that axis, and that is a
defect in the rule independent of whose prose it inconveniences.

What stopped (b) is its measured blast radius outside the lane that found it. A prefix allowlist of
`references/ scripts/ assets/ agents/ test/` demotes four findings owned by skills that lane could
not read in context:

| finding | cited | why it would demote |
| --- | --- | --- |
| `alaa-go-chi-development/references/30-kit-owner-workflow.md:7` | `docs/CONSUMERS.md` | leading `docs/` |
| `alaa-laravel-upgrade-all-packages/SKILL.md:14` | `docs/agents/upgrade-all-packages-execution-state.md` | leading `docs/` |
| `alaa-minio-object-storage/references/75-mc-command-line-client.md:195` | `docs/agents/tusd-api-contract-state.md` | leading `docs/` |
| `alaa-sms-provider-mediana/references/50-phone-and-conformance.md:95` | `skills/sohrab/alaa-bale-provider/scripts/phone-conformance-corpus.json` | leading `skills/` |

The last row settles it. That citation names a real skill and a plausible bundled file, and it is
fleet-root-relative rather than skill-relative -- a third path category the notation has no marker
for. A rule keyed on the *leading* segment demotes it to informational, which is the wrong answer.
A change whose measured effect includes deleting another owner's probably-genuine finding does not
belong in a lane scoped to two skills, however good the rule looks in the abstract.

An owner-plausibility variant -- promote only when a skill named on the line *could* own the path,
tested by whether the path's leading segment exists as a directory inside it -- was rejected on
stronger grounds: it makes one skill's verdict depend on another skill's directory listing, so
adding a `docs/` directory anywhere would silently change verdicts everywhere. A non-local rule is
worse than the defect it fixes.

**What the tool owner should do instead, with the whole fleet in view:** make the notation the sole
discriminator -- never promote an unmarked non-bundled-prefix path, on any line -- and hand-triage
the four citations above into their owners' backlogs rather than letting them fall silently into
`I1`. Until then the limit is stated in the module docstring and under `I1` in `--help`, which is
the honest position: the rule is narrower than it looked, and saying so costs less than a gate
nobody trusts.

**A gap this lane could not close.** `<repo>/` cannot be written in a frontmatter `description`,
because plugin validation rejects angle brackets there. `alaa-repo-docs/SKILL.md:3` was therefore
repaired in prose: the four `docs/...` paths were rewritten so the scanner matches nothing, and one
added sentence states in words what the marker would have stated in symbols. Every description
that must name a target-repository path has the same problem and, for now, the same only fix.
