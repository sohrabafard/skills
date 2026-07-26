# Import Direction and Package Boundaries

Read this before adding an import to a package that is not a transport or infrastructure package. It states which
package may import what, and how to check it.

Two things this file does not contain. The catalogue of Go design patterns and their mechanics belongs to
`/golang-design-patterns` (`$golang-design-patterns`). What each classic pattern becomes on this platform belongs to
`/alaa-golang-clean-code-principles` (`$alaa-golang-clean-code-principles`) `references/60-design-patterns-kit-era.md`.
Neither is repeated here, and choosing a pattern is not a reason to open this file.

On a kit service, P5 (`ports inward, adapters outward`) is the binding form of the rule below and it wins. This file
states the same direction for every Go service this skill routes, kit or not, and adds the check.

## The direction

Imports point inward. The layers, outermost first:

```
infrastructure  →  application  →  domain
```

`domain` imports nothing from this list. `application` imports `domain`. `infrastructure` imports both. Nothing
imports `infrastructure` except the composition root, which lives inside it. HTTP handlers, repositories, clients and
publishers are all `infrastructure`; the layer names and their directories are in
`60-service-architecture-patterns.md`.

## What is forbidden, concretely

**Forbidden in `domain` and `application` packages** — these imports, and any package that transitively pulls one in:

- `github.com/go-chi/chi/...`, `github.com/gofiber/...`, and `net/http`
- `github.com/jackc/pgx/...`, `database/sql`, and any other driver
- `github.com/redis/go-redis/...`
- `github.com/rabbitmq/amqp091-go` and any other broker client
- any vendor or provider SDK
- any `git.alaatv.com/vk/alaa-go-chi/...` transport, storage, or messaging package

**Rule:** when a domain or application package needs one of those capabilities, declare an interface in the package that
*needs* it, with only the methods that package calls, and implement it in `infrastructure`. The composition root wires
the two.

**Forbidden:** an interface declared in the package that implements it. **Rule:** the consumer owns the interface; the
implementation package returns a concrete type from its constructor.

**Forbidden:** an interface with a method no current consumer calls. **Rule:** add the method when the second consumer
appears, not in anticipation.

**Forbidden:** a package named `utils`, `helpers`, `common`, `shared`, `base`, or `pkg` holding unrelated code. Such a
package is imported by every layer and therefore destroys the direction. **Rule:** name a package for the one thing it
does and put the code with the type it serves.

**Forbidden:** a package-level mutable variable holding a dependency, and `init()` performing wiring or I/O. Both make
the import graph lie about what depends on what. **Rule:** construct in the composition root and pass explicitly.

## Checking it

**Rule:** verify direction with the build graph, not by reading:

- `go list -deps ./internal/domain/... ./internal/application/...` lists everything those layers actually pull in,
  transitively. Nothing in the forbidden list above may appear.
- `/golang-gopls` (`$golang-gopls`) `go_package_api` shows what a package exports; `go_symbol_references` shows who
  depends on a type before you move it.

**Rule:** when the check fails, fix the direction rather than the check — move the type toward the layer that owns it,
or introduce the interface at the consumer. An import cycle in Go is always a boundary that was drawn in the wrong
place; `/golang-refactoring` (`$golang-refactoring`) owns the safe procedure for moving the type.
