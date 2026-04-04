# Sources

Use these sources when the task depends on live release policy, framework compatibility, or the external guidance that
informed `alaa-golang`.

## Official Go sources

- Go release history and support policy:
    - https://go.dev/doc/devel/release
- Organizing a Go module:
    - https://go.dev/doc/modules/layout
- Effective Go:
    - https://go.dev/doc/effective_go

## Official or primary ecosystem sources

- Uber Go Style Guide:
    - https://github.com/uber-go/guide/blob/master/style.md
- Fiber repository and compatibility note:
    - https://github.com/gofiber/fiber

## Requested MCP Market sources

- Effect Concurrency & Fibers:
    - https://mcpmarket.com/tools/skills/effect-concurrency-fibers
    - contributed the lifecycle, bounded-parallelism, timeout, race, and explicit-interruption themes that were
      translated into Go ownership rules
- Go Style (Uber Guide):
    - https://mcpmarket.com/tools/skills/go-style-uber-guide
    - contributed the emphasis on interface safety, receiver rules, zero-value mutexes, boundary copying, error
      handling, preallocation, and early-return clarity
- Fiber Best Practices & Project Structure:
    - https://mcpmarket.com/tools/skills/fiber-best-practices-project-structure
    - contributed the emphasis on `cmd/`, `internal/`, thin handlers, structured logging, request-scoped locals, and
      centralized environment management

## How to resolve conflicts

1. Prefer official Go and framework sources for version-sensitive or normative behavior.
2. Use the MCP Market pages as intent and pattern summaries.
3. Use the installed public Go skills for detailed implementation guidance inside this pack.
4. Use the Sohrab companion skills when the task crosses workflow, platform, contract, or security boundaries owned by
   this repository.
