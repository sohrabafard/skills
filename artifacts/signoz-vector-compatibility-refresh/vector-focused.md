# Lane V focused evidence

Observer: vector (alaa-implementer-sol), configured gpt-6-astra/high; serving identity unknown. Frozen 2026-09-26T05:44:39.9784181Z, HEAD 3a62cbb615e0180458ebedd4bc9a0794c17c1e60. Scope skills/sohrab/vector-rust-observability-pipelines, 33 files including new files.

Digest de723cfbe353d71213ac0efe6936fc8767e8b283ee43f4d380931775fe19e973. Method matches lead snapshot: sorted repository-relative POSIX path, TAB, lowercase file-SHA256, LF; SHA-256 of UTF-8 manifest.

Commands from the skill directory at BelowNormal unless Git inspection. Tier focused.

| Command | Exit | Result | Proof |
|---|---:|---|---|
| node scripts/check-upstream-version.mjs --self-test | 0 | 9 PASS | Offline resolver unit |
| node scripts/check-upstream-version.mjs | 0 | Product 0.58.0; chart 0.58.0; appVersion 0.58.0-distroless-libc | Live public release metadata only |
| node --check scripts/check-upstream-version.mjs | 0 | Syntax valid | Static |
| node --check scripts/check-vector-configs.mjs | 0 | Syntax valid | Static |
| node scripts/check-vector-configs.mjs --self-test | wrapper 1; checker diagnostic 2 | spawnSync vector.exe EPERM | ENVIRONMENT-BLOCKED, no actual Vector proof |
| node scripts/check-vector-configs.mjs (with explicit propagation of LASTEXITCODE) | 2 | spawnSync vector.exe EPERM | ENVIRONMENT-BLOCKED, no actual Vector proof |
| git diff --check -- skills/sohrab/vector-rust-observability-pipelines (root cwd) | 0 | No whitespace findings | Static |

The self-test wrapper exit discrepancy was made explicit; it is not a runtime test failure or a pass. Regular invocation confirmed actual unavailable-proof exit 2. Final message-only checker wording did not trigger repeated blocked runtime attempts. PowerShell HTTPS and one curl retrieval attempt failed TLS; Node public metadata fetch subsequently succeeded. No TLS verification was disabled. No binary install, process/container/service launch, provider, benchmark or deployment access.

Coverage: references/81-release-coverage.md maps every item in the tagged 0.58.0 release source: 59 product changes plus 3 VRL changes. Official tag source count was independently fetched by the writer and matched the ledger. The skill baseline is 0.57.0, with no other intervening stable product release listed. Current consumer inventory remains unknown; historical 0.53 and observed 0.57 paths are retained and labelled historical.

Changed: 20 tracked files and 5 new files. New fixtures cover warning rejection and version-qualified confinement failures. Security guidance distinguishes field-specific upstream changes from retained stricter routing controls. Disk oversized-record drop acknowledgement differs from fatal full-volume/I/O failure; exactness paths need admission controls and observable drops. Old buffer gauges are version-qualified instead of promised after removal.

Documentation classification proposed by writer: sole topic router 52 lines YELLOW, because splitting it creates competing routers; all other changed skill documents EXEMPT-ATOMIC topic execution/security/migration contracts. References 75, 80 and 81 are historical decision/evidence, normative version/migration and release-coverage decision records. Independent instruction reviewer will assess these classifications.

Unrun: real Vector validate/test and VRL, provider recovery/load/delivery, deployment and current consumer compatibility. Native repository/workflow gates and independent reviews pending.
