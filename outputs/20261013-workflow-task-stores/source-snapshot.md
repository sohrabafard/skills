# Source snapshot

- HEAD: `1207d2e8c17d74ea77920ea9cb285b6c73554c7d`
- Observed UTC: `2026-10-13T00:34:41.9523834Z`
- Scope: all 17 tracked/nonignored untracked files under `skills/sohrab/alaa-workflow`, plus the two orchestrators' `references/verification-and-gates.md` (19 files).
- Manifest: `source-manifest.sha256`.
- Manifest SHA-256: `b67537a006084689f21addcf517fbe6df90aab74a90162c11f625be291f52bc9`.
- Method: list scope with `git ls-files --cached --others --exclude-standard`; hash each file's raw bytes using SHA-256; render lowercase digest, two spaces and repository-relative path per line; sort full lines with ordinal comparison; join using LF with one final LF; hash UTF-8 bytes without BOM. Recompute from current files, not from the saved manifest alone.
- State: uncommitted source. The manifest identifies contents but does not provide remote recovery. No commit, installation or publication occurred.
- Gate boundary: writers frozen for independent review and verification. If a covered file changes, capture a new manifest and invalidate affected results.
- Prior snapshot `10524ac5e8e1e79a868670ce8b6d32276fe38887c017c7ce362b8ca63b3dd083` remains the identity for round-one failed suite and successful structure check. Only four test fixtures changed afterward; see code-lane.md and verification-round-1.md.
