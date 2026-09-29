Version-sensitive claims in this topic depend on [Go version source ledger](../SOURCES.md).

## Adoption rules

1. Match the repository's directive; raise it only for a feature the code uses, in its own commit, with the reason
   stated.
2. Run `go fix ./...` with `gofmt`, `go vet`, and `golangci-lint` as a reviewed pass; never blind-commit it.
3. Use `new(expr)` for pointer-to-value fields once the directive allows it.
4. Use `errors.AsType[T]` in new error mapping and `context.Cause` in the shutdown path.
5. Leave Green Tea GC and heap-base randomization on; re-baseline latency and GC metrics after upgrading.
6. Export the new scheduler metrics; take alert thresholds from `/alaa-observability-soc`.
7. Add URL-parsing tests before upgrading a service that ingests external URLs.
8. Take every TLS, cipher, padding, and FIPS decision to `/alaa-security-review`.
9. Write persistent test output to `t.ArtifactDir()`; benchmark with `b.Loop` and re-baseline.
10. Keep every experiment out of production builds.
