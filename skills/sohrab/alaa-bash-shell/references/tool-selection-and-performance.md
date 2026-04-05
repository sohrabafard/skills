# Tool Selection and Performance

## Contents

1. Builtins first
2. Tool selection matrix
3. Performance rules
4. Anti-patterns
5. Safe parallelism

## 1. Builtins first

Use shell builtins when they are the clearest and cheapest option:

- `case` for simple classification
- `printf` for formatted output
- parameter expansion for small string operations
- arithmetic expansion for integer math
- `read` loops for streaming text
- `command -v` for dependency checks

Do not force shell builtins into jobs they are bad at.

## 2. Tool selection matrix

| Job | Preferred tool | Notes |
| --- | --- | --- |
| Filter lines | `grep` or `rg` | `rg` is excellent for repository search; `grep` is more universal |
| Stateful or column-oriented text transforms | `awk` | Usually clearer and faster than multiple shell loops |
| Simple line edits or substitutions | `sed` | Keep it linear; switch to `awk` when logic becomes stateful |
| JSON | `jq` | Do not parse JSON with regex |
| YAML, mixed config, XML, INI | `yq` | Good when the dependency is acceptable |
| Fast file lookup in developer workflows | `fd` | Great ergonomics, not a POSIX replacement for `find` |
| Portable filesystem traversal | `find` | Reach for this when portability or advanced predicates matter |
| Batched command execution | `xargs` or `find -exec ... +` | Use GNU Parallel only when its dependency is acceptable |
| Repository-wide code search | `rg` | Very fast and cross-platform-friendly |

## 3. Performance rules

- Stream data instead of storing everything in shell variables when the dataset can grow.
- Avoid spawning external commands inside tight loops when one `awk`, `jq`, or `sed` call can do the job.
- Avoid `cat file | grep ...`; read the file directly with the consumer command.
- Use one `awk` program instead of chains of `cut`, `sed`, and `grep` when that makes the logic simpler.
- For Bash-only scripts, `mapfile` is appropriate only when the full input comfortably fits in memory.
- Use shell as an orchestrator. Let specialist tools do the heavy data work.

## 4. Anti-patterns

Avoid these unless there is a very good reason:

- parsing JSON or YAML with `grep`, `awk`, or `sed`
- `for line in $(cat file)` style loops
- unbounded accumulation into a single huge variable
- repeated `grep` or `sed` inside a loop over thousands of lines
- external `expr` for simple integer arithmetic
- dense one-liners that save lines but destroy debuggability

## 5. Safe parallelism

Parallelism helps only when the script is mostly delegating independent external work.

Good options:

- `xargs -P` when available and acceptable
- GNU Parallel when its dependency is acceptable and documented
- background jobs with `wait` for small, controlled fan-out

Rules:

- keep work units independent
- capture and propagate failures
- avoid writing to the same output file from multiple jobs without coordination
- document ordering guarantees, or lack thereof
- for portable `/bin/sh`, prefer clarity over aggressive parallel shell tricks
