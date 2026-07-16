# Go Consumer Pattern

Use `input_shape: go_service_permission_map`. The catalog emits `permissions_gen.go` in the package inferred from the
target directory. The generated file includes constants, ID/name lookup functions, `MaxPermissionID`, a defensive map
copy, and `Decode(access string) (Set, error)`.

## Required package contract

The owning Go package must provide:

```go
type Set map[string]struct{}

func DecodePermissionSet(
    access string,
    namesByID map[int]string,
    maxPermissionID int,
) (Set, error)
```

Implement the decoder once in a non-generated file. It must accept only non-empty raw unpadded base64url, unpack bits
least-significant-bit first, compute `permissionID := byteIndex*8 + bitIndex + 1`, ignore IDs above the local maximum or
missing from the service map, and return an error when zero known permissions resolve.

## Integration rules

1. Commit the generated file at the exact catalog `source_path`.
2. Use generated permission constants in middleware/route registration.
3. Default production decoding to the generated `Decode` function.
4. Keep any injectable decoder interface narrow and test-only in purpose; do not restore JSON/file/env mapping in
   production.
5. Return copies from exported map accessors so callers cannot mutate generated package state.
6. Keep `permissions_gen.go` byte-for-byte generator-owned except for normal line-ending normalization.

## Tests

- Assert every expected ID/name round-trip and the exact `MaxPermissionID`.
- Decode a bitmap containing the lowest and highest service IDs, including IDs above 8/64.
- Verify unknown-only, empty, padded, invalid-character, and malformed input fail closed.
- Verify unknown bits mixed with a known bit do not remove the known permission.
- Run focused package tests, `go test ./...`, `go vet ./...`, and repository-native lint/build checks.
- Re-run catalog import and strict drift after applying the generated file.

If the service is in a monorepo, keep `owner_repo` as the repository name and use the full nested path in `source_path`,
`generated_target`, and each permission's service target.

