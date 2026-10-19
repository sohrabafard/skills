# Binding batch B receipt

Verdict: ready-for-final-gate. Beads leaf `alaa-sd7.2.1` remains `in_progress`; no commit, push, or install performed.

AGENT: `alaa-implementer-luna`; CONFIGURED: `gpt-6-luna/medium` (explicit parent spawn metadata; definition has no model pins); REQUESTED: `gpt-6-luna/medium`; OBSERVED: unknown (runtime reports only generic GPT-6).

The current `binding-template.md` was applied verbatim with `__PROJECT__` replaced by each directory name. All physical blocks passed exact parity, UTF-8 without BOM/LF checks, and prefix/suffix byte preservation. Initial worktrees were clean, unstaged, and on `main`; no binding differed from HEAD before this lane.

| Repository | Starting HEAD | Logical paths and physical change | Original block SHA-256 | Final block SHA-256 | Physical file SHA-256 before -> after |
|---|---|---|---|---|---|
| tusd | `788de5c560ce6b8713d499f2c995abf295099f3f` | `AGENTS.md`; `CLAUDE.md` remains mode 120000 -> `AGENTS.md` | `3ef43d4e7e7971114abe2519a33f1e77fc1d72a8b6473c8f6ddb472e91394179` | `97c243179b8b44c5b6aa8e1aabff217955494b046f139594f2a3f0de837ffffb` | `47a19cdbba80f054f030a8fa52517b953dba94a7680e1b2346432bd269a56a89` -> `ab61d05ffbd781cc00d337184212924a63a3e288765f3ff8dbca9961da68b83c` |
| gateway | `24c4d7ae5da1947bbe759a585318252ae2d1d447` | `AGENTS.md`; `CLAUDE.md` remains mode 120000 -> `AGENTS.md` | `225ad87ae686d18e0e1db196255b480f9d4ce7eee8f0645ab9c26d78ca504c66` | `3316d74324ffaa79c1e64549e9cb7f250661ad9b12cd70aca7da1ddbe0ce33ba` | `4fd865e1c5dd518b2e239673020e169e1be1851b8f1107bd0e7208327560a472` -> `2329d076baa477d039383b59b9fdc608b482e31056b4101303f89e32da40bf77` |
| alaa-go-chi | `81507da77d837d66e430e73d7bff60ae33964542` | `AGENTS.md`, `CLAUDE.md` (both regular files) | `6d038b03ac9324e6cd089435d81cd24fca1dd27f43874b0c466c6dba3e020750` | `96d1e34b5e721131a055e7805ef724e71324a22756717d978b11137769e61de7` | `AGENTS d26d23e33f71dd7bda4c7ef8fd1a16b303dc3b25cbfd10f9b1f23974fb1ec468` -> `882c829e4f320595da2373d6342f5592ff92b7d19c2c737431fc4d4ef690241b`; `CLAUDE 889e48621d97d328e75aab55a6e01cf6a2cb5a46c5cd05e92c9b8e168aa5bfda` -> `512c9fc740dfc9f3b9bf5d282b8f51a599e5e6cabebe5d552c7d244da6300134` |
| authz-sidecar | `b6d2a646fea2e0515cffcdf3ead7cd77a97208a4` | `AGENTS.md`, `CLAUDE.md` (both regular files) | `95184beb80dd1bedbbdc96c15165feee4387f5958f3f6a8160809914bf30fd88` | `1428d04035117481ce399f0e6b472fc628bb1e57f4795a4f4b5a9f033ef06817` | `AGENTS 530bc42c63fa239e7263dfa5088fc512cb0ed8c29886f3dd17732ff1509d6ddf` -> `33422a6525625840a918c429ccbaa0b836281a942f1e6712abb118861f4dc401`; `CLAUDE 1a3361f2b2b9c1ae29542fb5c81c1c96d984d19409975e0d9d89c179270226b3` -> `4fda9f125dbebc093c6ca29ab7013d8661dbcf4d00f6860ef5751afa15fb4de7` |

Verification: `git diff --check` exited 0 in all four repositories after the template's whitespace revision. alaa-go-chi also passed `python scripts/validate_agent_instruction_pack.py .` and `go test ./scaffold -run 'TestRenderGoldenService|TestRenderGoldenDatastoreFreeService'`.

Runtime evidence: sandboxed Git checks initially hit Git Bash/MSYS `CreateFileMapping`/signal-pipe Win32 error 5. The exact elevated PowerShell checks later passed; gateway took about 50 seconds. authz-sidecar's configured `stripbom` clean filter is `node scripts/encoding/text.cjs --filter`; Node is installed at the host's configured path, and its elevated check passed without changing filter configuration. One parallel post-edit gateway status scan emitted MSYS startup errors and false modified entries with equal index/worktree hashes; that snapshot is unreliable. Initial gateway status was clean, this lane wrote only `AGENTS.md`, and the independent final verifier owns the serial status audit.

No other files were intentionally changed. Parent owns final combined review, verifier acceptance, binding-only commits, and leaf closure.
