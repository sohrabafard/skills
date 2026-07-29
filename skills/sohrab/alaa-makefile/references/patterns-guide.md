# Pattern rules and automatic variables

**Owner of:** automatic variables (`$@ $< $^ $+ $? $* $(@D) $(@F)`), pattern rules, static pattern rules,
implicit-rule interaction, and the text functions used to derive one file list from another. No other
file in this skill states these rules.

## Automatic variables

Make sets these for each rule, at the moment the recipe runs.

| Variable | Value |
|---|---|
| `$@` | the target |
| `$<` | the first prerequisite |
| `$^` | all normal prerequisites, duplicates removed, order-only excluded |
| `$+` | all normal prerequisites, duplicates kept, in order |
| `$?` | the normal prerequisites newer than the target |
| `$*` | the stem that the `%` matched |
| `$(@D)` `$(@F)` | the directory part and the file part of `$@` |
| `$(<D)` `$(<F)` | the directory part and the file part of `$<` |

Two facts that decide most bugs here. First, `$^` **excludes order-only prerequisites**, which is why a
directory belongs after the `|` — it must exist, and it must not appear in the command line. Second,
`$?` is the incremental-build variable: it holds only what changed, which is what an archive update or a
staged deployment wants.

```makefile
$(BUILDDIR)/bundle.tar: $(FILES) | $(BUILDDIR)
	tar -cf $@ $^          # all files; $(BUILDDIR) is not in $^

$(BUILDDIR)/incremental.tar: $(FILES) | $(BUILDDIR)
	tar -rf $@ $?          # only the files newer than the archive
```

Inside a recipe these are Make variables, so they are expanded before the shell sees the line. Quote them
whenever a path may contain a space: `"$@"`, `"$<"`. `$^` cannot be quoted as a unit, which is one more
reason to keep spaces out of build paths.

## Pattern rules

A `%` in the target matches any non-empty string, and the same string — the stem — substitutes into the
prerequisite.

```makefile
build/%.min.js: src/%.js | build
	esbuild --minify $< --outfile=$@

docs/%.html: docs/%.md
	pandoc $< -o $@
```

Make chooses a pattern rule by looking for one whose target pattern matches the file it wants and whose
prerequisite then exists or can itself be made. With `--no-builtin-rules` in the preamble, only the
rules in the file are candidates, so the search is small and predictable.

Several pattern rules may match. Make prefers the rule whose stem is shortest; among equal stems it takes
the first that can be satisfied. Relying on that ordering is fragile — use a static pattern rule instead
when the file list is known.

An empty recipe cancels a rule:

```makefile
%.o: %.c        # cancels a built-in or earlier rule for this pattern
```

## Static pattern rules

When the target list is known, name it. Make then knows exactly which targets the rule builds instead of
searching.

```makefile
OBJECTS := $(SOURCES:src/%.c=build/%.o)

$(OBJECTS): build/%.o: src/%.c | build
	$(CC) $(CPPFLAGS) $(CFLAGS) -c $< -o $@
```

The form is `targets: target-pattern: prerequisite-pattern`. It is more explicit than a bare pattern
rule, faster because make does no search, and it produces a real error when a target does not match the
pattern rather than silently falling through to another rule.

Use a static pattern rule for a computed list, and a plain pattern rule for a genuinely open-ended
transformation such as "any Markdown file to HTML".

## Deriving one list from another

```makefile
SOURCES := $(wildcard src/*.js)

OBJECTS := $(SOURCES:src/%.js=build/%.min.js)   # substitution reference
OBJECTS := $(patsubst src/%.js,build/%.min.js,$(SOURCES))  # the same thing

TESTS   := $(filter %_test.js,$(SOURCES))
LIB     := $(filter-out %_test.js,$(SOURCES))
DIRS    := $(sort $(dir $(OBJECTS)))            # sort also removes duplicates
NAMES   := $(notdir $(basename $(SOURCES)))
```

Assign every one of these with `:=`. With `=` the whole chain, including the `wildcard` filesystem scan,
re-runs at every reference; `variables-guide.md` owns that rule. `$(sort …)` removing duplicates is the
idiomatic way to build a directory list from a file list.

`$(wildcard …)` is evaluated when the assignment is expanded, so a file created later in the same run is
not in the list. When a rule generates sources, the list must come from the generator's own output, not
from `wildcard`.

## Directories in pattern rules

Create the directory with an order-only prerequisite rather than `mkdir -p` in every recipe:

```makefile
OBJDIRS := $(sort $(dir $(OBJECTS)))

$(OBJECTS): | $(OBJDIRS)

$(OBJDIRS):
	mkdir -p $@
```

`targets-guide.md` owns the order-only rule; this is its pattern-rule application. `mkdir -p $(@D)` at
the top of each recipe also works and is acceptable in a small file, but it re-runs per target and it
hides the dependency from make.

## Multiple targets from one rule

```makefile
# Grouped targets: ONE run of the recipe produces all of them. GNU Make 4.3+.
build/parser.c build/parser.h &: grammar.y
	bison -d -o build/parser.c $<
```

The `&:` form tells make that a single execution produces every listed target, which is what a code
generator does. Plain `:` with several targets means the recipe runs once *per target*, which for a
generator means running it two or three times and racing under `-j`. `&:` requires GNU Make 4.3 or
newer; the current stable release is 4.4.1 (`SOURCES.md`).

## Interaction with the implicit-rule database

`--no-builtin-rules` in the preamble removes make's built-in rules, and `.SUFFIXES:` with no
prerequisites removes the built-in suffix list. Both are in `makefile-structure.md`. Keep them: without
them, a target with no rule can still be built by a rule you never wrote, from a file you did not intend,
and the failure appears as a link error rather than a make error.

Suffix rules (`.c.o:`) are the pre-1990 form of pattern rules. Read them when a legacy file has them;
write pattern rules.

## What this file does not decide

- Which assignment operator the derived lists take: `variables-guide.md`.
- `.PHONY`, order-only prerequisites and the standard target set: `targets-guide.md`.
- The preamble, `.SUFFIXES:` and includes: `makefile-structure.md`.
- Parallel safety of the resulting graph: `optimization-guide.md`.
- C, C++ and Java compilation rules and header dependency generation: `native-toolchain.md`.
