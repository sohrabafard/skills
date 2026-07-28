# Source Map and Provenance

Every fact in this skill belongs to one of three registers. A fact without a register is unusable, because the reader cannot tell whether it describes what tusd does, what a browser does, or what the Ala service decided.

| Register | Authoritative source | How to refresh it |
|---|---|---|
| **(a) Upstream tusd** | The tus protocol specification, the tusd repository and the release notes for the pinned version | fetch from the URLs below and record the date |
| **(b) Browser client** | The `tus-js-client` repository and the version in the consuming project's lockfile | read the lockfile, then the release notes for that exact version |
| **(c) Ala `tusd` service** | The Ala `tusd` repository source, read in the current session | read the Go file and cite it by path and line |

Register (c) never comes from memory, from an older skill revision, or from a document inside the Ala repository that describes intent. Design documents there describe what was planned; several planned components do not exist. Cite executable code, a migration, a Compose file or a committed test.

## Upstream source priority

1. The tus protocol specification and the tus organisation docs: `https://tus.io/protocols/resumable-upload`, `https://tus.io/implementations`.
2. tusd documentation and releases: `https://tus.github.io/tusd/getting-started/configuration/`, `https://tus.github.io/tusd/advanced-topics/hooks/`, `https://tus.github.io/tusd/storage-backends/`, `https://github.com/tus/tusd/releases`.
3. The tusd Go source for the pinned version, when a documented default and observed behaviour disagree. The source wins.
4. `tus-js-client` docs and releases: `https://github.com/tus/tus-js-client`, `https://github.com/tus/tus-js-client/releases`.
5. Official docs for the chosen proxy and object store.
6. Community issues and posts as symptom leads only. Confirm the conclusion against 1 to 5 and a real upload before recommending it.

## Version snapshot

This is the only file in this skill that carries a version string. Every asset takes its version from an environment variable so that a bump is one edit here plus one edit in the deployment's own environment.

| Artifact | Version | Read on | Read from |
|---|---|---|---|
| `tus/tusd` latest release | `v2.9.2`, published 2026-03-11 | 2026-04-24 | GitHub releases |
| `tus/tus-js-client` latest stable | `v4.3.1`; a `v5.0.0-pre2` prerelease exists and is not stable | 2026-04-24 | GitHub releases |
| `github.com/tus/tusd/v2` module used by the Ala service | `v2.8.0` | 2026-07-27 | Ala `tusd` `go.mod` |
| Ala `tusd` Go toolchain | `go 1.25.0` | 2026-07-27 | Ala `tusd` `go.mod` |

The Ala service is one minor release behind the latest upstream tag. Confirm both numbers before asserting that a fixed upstream bug is fixed in the Ala service.

## Freshness triggers

Re-read the source before asserting any of these, because each has changed between tusd minor releases:

- a flag name, a flag default, or whether a flag exists at all;
- a hook payload field, a hook response field, or an ordering guarantee between events;
- a storage backend default, especially part sizes, buffered-part counts and object size ceilings;
- CORS defaults, the metrics path, or which metrics are registered without an explicit call;
- whether a `tus-js-client` option exists in the version the project actually installs;
- proxy behaviour for buffering, streaming bodies, timeouts and forwarded headers.

## Recording a claim

Write an upstream claim as: the value, the version it was read from, and the date. Write an Ala claim as: the value and the source path with a line number. A claim with neither is a guess, and a guess about an upload plane is acted on as though it were measured.

Anything this skill could not verify is stated as unverified rather than omitted, because an omission reads as absence of risk.
