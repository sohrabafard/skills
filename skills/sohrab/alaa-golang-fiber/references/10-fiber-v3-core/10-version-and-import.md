The official Fiber API baseline for this slice was verified on **2026-07-26**; claim-specific source URLs and later refresh dates are in [SOURCES.md](../SOURCES.md).

## Version and import

- Import path: `github.com/gofiber/fiber/v3`.
- Current released module at the 2026-09-29 refresh: `v3.5.0`, released 2026-08-13
  (https://github.com/gofiber/fiber/releases/tag/v3.5.0). Check the consumer's resolved module version
  before using a newer API; this does not raise its minimum or change the framework decision.
- Minimum Go version: "Version `1.25` or higher is required."
  (https://docs.gofiber.io/, verified 2026-07-26). If the repository's `go` directive is higher,
  keep it; never regress it.
- Fiber runs on `fasthttp`, not `net/http`. A `net/http` fact is not a Fiber fact. Do not carry
  assumptions across.
