# Source priority and freshness

Every figure in this pack is a dated reading of a source, not a property of the web.

## Re-read the source before stating any of these

A quota figure or byte cap for any engine; a browser version at which an API became available; Safari,
WebKit, iOS or iPadOS behaviour of any kind; whether an API is experimental, origin-trial or Baseline; what
grants persistent storage in a named browser; eviction timing or ordering.

Re-read anyway when the date in `99-sources-and-maintenance.md` is over six months old, when the change
ships to production across broad browsers, or when the proposal is a browser-specific workaround.

## Source order

1. W3C and WHATWG specifications for API semantics and terminology.
2. MDN for cross-browser behaviour, the quota and eviction guide, and Baseline status.
3. Engine-vendor publications for engine policy: Chrome for Developers and Chromium docs; the WebKit blog
   and bug tracker; MDN and Bugzilla for Gecko.
4. Can I Use and Browser Compatibility Data for per-version tables.
5. Official documentation for `idb`, Dexie, localForage or RxDB when the task uses one.
6. Issue trackers and community reports as symptom signals only. One becomes a rule here after a test in
   this repository reproduces it.

## How a claim is recorded

Every browser claim carries a source and a `read: <ISO date>`. Three states, and they are distinct:

- **Stated with a source and a read date.** Someone read that source on that date.
- **`unverified as of <ISO date>`.** Retained because deleting it would lose the caution it carries.
  Never dropped, never asserted.
- **`not documented (searched <ISO date>)`.** Searched and not found. Not proof of absence.

An unattributed number is the failure this section prevents: it survives every refresh because nobody knows
which source to re-read.

## Conflict

If documentation and observed behaviour disagree, record the conflict in the feature's ADR, branch on a
runtime probe rather than on the documentation, and add a test in the lane where it appeared.
`assets/browser-test-matrix.yaml` names the lanes.

Skill structure, register, model and effort are not this skill's ground: `/alaa-prompting-guide`
(`$alaa-prompting-guide`), and effort specifically its `references/50-effort-and-thinking.md`.
