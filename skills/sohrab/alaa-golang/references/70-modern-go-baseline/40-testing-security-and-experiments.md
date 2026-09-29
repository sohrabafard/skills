Version-sensitive claims in this topic depend on [Go version source ledger](../SOURCES.md).

## Testing

- **`t.ArtifactDir()` with `go test -artifacts`** writes golden files, captured payloads, and failure dumps to a
  persistent directory, unlike the auto-cleaned `t.TempDir()`. **Rule:** use it for anything a CI job must upload, and
  point the pipeline's artifact step at `-outputdir`.
- **`for b.Loop() { … }`** no longer blocks inlining of the loop body. **Rule:** write benchmarks with `b.Loop` rather
  than `for i := 0; i < b.N; i++`, and re-baseline any existing `b.Loop` benchmark after upgrading, because its
  numbers changed.
- **`testing/cryptotest.SetGlobalRandom`** is how deterministic crypto is done now. **Forbidden:** linking it into a
  production binary.
- **Not changed by 1.26:** `testing/synctest`, `testing.T.Context`, and fuzzing. **Rule:** verify their API against the
  1.24 and 1.25 notes, not the 1.26 page.
## Security-relevant changes

Go 1.26 changes TLS defaults, deprecates several legacy `GODEBUG` toggles ahead of tighter 1.27 defaults, makes crypto
key generation ignore caller-supplied randomness, deprecates PKCS#1 v1.5 encryption padding, adds `crypto/hpke` and KEM
interfaces, and ships a new FIPS 140-3 module version.

**Rule:** two of these are mechanical and yours to apply:

- Remove any custom `rand.Reader` passed into `crypto/rand.Prime`, `crypto/dsa.GenerateKey`,
  `crypto/ecdh.Curve.GenerateKey`, or `crypto/ed25519.GenerateKey` — it is now a no-op, so code that looks
  deterministic no longer is. Replace deterministic test usage with `testing/cryptotest.SetGlobalRandom`.
- Replace `go tool`-era manual `Certificate.Leaf` population, which 1.27 makes unnecessary.

**Rule:** everything else in this paragraph — which TLS minimum version a service sets, whether a legacy cipher or key
exchange may be re-enabled, whether FIPS enforcement applies, which padding a service may use — is a posture decision
owned by `/alaa-security-review`. Take it there. **Forbidden:** setting
`tls.Config.CurvePreferences`, `MinVersion`, or any `GODEBUG` TLS toggle on your own judgement.
## Experiments

**Forbidden:** shipping `GOEXPERIMENT`-gated packages or behaviour in production. Classify capabilities
against the selected toolchain: promotion and flag removal change their experimental status.

**Rule:** on Go 1.26 only, `GOEXPERIMENT=goroutineleakprofile` belongs in staging, soak and CI, never
production. On Go 1.27 use the stable profile described in [Go 1.27 changes to assess](10-release-status-and-changes.md#go-127-changes-to-assess) without that removed flag.

**Rule:** on Go 1.26, production JSON stays on `encoding/json`; on Go 1.27, use the compatibility migration rule in [Go 1.27 changes to assess](10-release-status-and-changes.md#go-127-changes-to-assess) before adopting the stable v2 API. A stable API alone does not prove wire compatibility.
