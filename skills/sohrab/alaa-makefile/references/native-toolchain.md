# Compiling native code with Make

**Owner of:** C, C++ and Java compilation with Make — the GNU tool and flag variables, header dependency
generation, the installation-directory set, VPATH, pkg-config, compiler caches, precompiled headers,
link-time optimisation and unity builds.

**Open this file only when a repository genuinely compiles native code.** Nothing on this fleet does: the
staged `service-ci-kit` and `service-runtime-kit` contain no C, C++ or Java build, and every Makefile
this skill writes for the fleet fronts a shell script. This material is preserved in full, in one place,
so that it stops competing with the task-runner material for a reader's attention. The rest of the skill
assumes you are not here.

Everything general — the preamble, `.PHONY`, automatic variables, order-only prerequisites, `:=` versus
`=` — is owned by the other reference files and is not repeated. This file covers only what is specific
to a compiler.

## The GNU tool and flag variables

Packagers, distributions and CI images already set these, so use the GNU names and never hard-code a
tool path.

```makefile
CC ?= cc
CXX ?= c++
AR ?= ar
RANLIB ?= ranlib
INSTALL ?= install
RM ?= rm -f
YACC ?= bison -y
LEX ?= flex
PKG_CONFIG ?= pkg-config
```

```makefile
CPPFLAGS ?=                        # preprocessor: -I, -D
CFLAGS   ?= -Wall -Wextra -O2      # C compiler
CXXFLAGS ?= -Wall -Wextra -std=c++20 -O2
LDFLAGS  ?=                        # linker: -L, -Wl,...
LDLIBS   ?=                        # libraries: -lfoo
```

The division matters at the command line, not just stylistically: `LDFLAGS` goes before the objects and
`LDLIBS` after, because most linkers resolve symbols left to right.

```makefile
$(TARGET): $(OBJECTS)
	$(CC) $(LDFLAGS) $^ $(LDLIBS) -o $@
```

Every one of these is `?=` so a user can override, and every project-specific addition uses `override
… +=` so a command-line assignment does not silently discard it (`variables-guide.md` owns that rule):

```makefile
override CPPFLAGS += -Iinclude
override CFLAGS   += -DPROJECT_VERSION=\"$(VERSION)\"
```

## Header dependency generation

A C or C++ object depends on every header it includes, transitively. Maintaining that list by hand is the
single largest source of "it did not rebuild" in native projects. Let the compiler emit it.

```makefile
DEPFLAGS = -MMD -MP

$(OBJDIR)/%.o: $(SRCDIR)/%.c | $(OBJDIR)
	$(CC) $(CPPFLAGS) $(CFLAGS) $(DEPFLAGS) -c $< -o $@

DEPENDS := $(OBJECTS:.o=.d)
-include $(DEPENDS)
```

- `-MMD` writes a `.d` file beside the object listing its prerequisites, as a side effect of compiling.
- `-MP` adds a phony target for every header. Without it, deleting a header makes the next build fail
  with `No rule to make target 'utils.h'` instead of just recompiling.
- `-include` rather than `include`, because the `.d` files do not exist before the first build.
- `-MMD` records only quoted includes; `-MD` also records system headers, which is usually noise.

A generated `main.d` looks like this, and make simply reads it as more rules:

```makefile
build/obj/main.o: src/main.c include/common.h include/utils.h
include/common.h:
include/utils.h:
```

Both `gcc` and `clang` support these flags. MSVC does not; use `/showIncludes` with a converter, or a
generator such as CMake, which is outside this skill.

## Directory layout and object placement

```makefile
SRCDIR := src
BUILDDIR := build
OBJDIR := $(BUILDDIR)/obj

SOURCES := $(wildcard $(SRCDIR)/*.c)
OBJECTS := $(SOURCES:$(SRCDIR)/%.c=$(OBJDIR)/%.o)
DEPENDS := $(OBJECTS:.o=.d)
TARGET  := $(BUILDDIR)/$(PROJECT)

$(BUILDDIR) $(OBJDIR):
	mkdir -p $@
```

Mirror the source tree under `$(OBJDIR)` so two files with the same basename in different directories do
not collide. For a recursive source tree, derive the directory list and depend on it order-only:

```makefile
SOURCES := $(shell find $(SRCDIR) -name '*.c')
OBJECTS := $(SOURCES:$(SRCDIR)/%.c=$(OBJDIR)/%.o)
OBJDIRS := $(sort $(dir $(OBJECTS)))

$(OBJECTS): | $(OBJDIRS)
$(OBJDIRS): ; mkdir -p $@
```

## Mixed C and C++

Compile each language with its own compiler and link with the C++ driver, which pulls in the C++ runtime:

```makefile
C_OBJECTS   := $(C_SOURCES:$(SRCDIR)/%.c=$(OBJDIR)/%.o)
CXX_OBJECTS := $(CXX_SOURCES:$(SRCDIR)/%.cpp=$(OBJDIR)/%.o)

$(TARGET): $(C_OBJECTS) $(CXX_OBJECTS) | $(BUILDDIR)
	$(CXX) $(LDFLAGS) $^ $(LDLIBS) -o $@

$(OBJDIR)/%.o: $(SRCDIR)/%.c | $(OBJDIR)
	$(CC) $(CPPFLAGS) $(CFLAGS) $(DEPFLAGS) -c $< -o $@

$(OBJDIR)/%.o: $(SRCDIR)/%.cpp | $(OBJDIR)
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) $(DEPFLAGS) -c $< -o $@
```

## Libraries

```makefile
STATIC_LIB := $(BUILDDIR)/lib$(PROJECT).a
SHARED_LIB := $(BUILDDIR)/lib$(PROJECT).so.$(VERSION)

$(STATIC_LIB): $(OBJECTS) | $(BUILDDIR)
	$(AR) rcs $@ $^
	$(RANLIB) $@

$(SHARED_LIB): $(OBJECTS) | $(BUILDDIR)
	$(CC) -shared -Wl,-soname,lib$(PROJECT).so.$(SOVERSION) $^ -o $@
```

Compile with `-fPIC` for anything that will be linked into a shared object. The soname carries only the
major version, so a compatible upgrade replaces the file without relinking consumers. `ldconfig` belongs
in the packaging step, not in `install`, because `install` runs into a `DESTDIR` staging tree where
running `ldconfig` is wrong.

## The installation directory set

```makefile
PREFIX ?= /usr/local
EXEC_PREFIX ?= $(PREFIX)
BINDIR ?= $(EXEC_PREFIX)/bin
SBINDIR ?= $(EXEC_PREFIX)/sbin
LIBEXECDIR ?= $(EXEC_PREFIX)/libexec
LIBDIR ?= $(EXEC_PREFIX)/lib
INCLUDEDIR ?= $(PREFIX)/include
SYSCONFDIR ?= $(PREFIX)/etc
LOCALSTATEDIR ?= $(PREFIX)/var
DATAROOTDIR ?= $(PREFIX)/share
DATADIR ?= $(DATAROOTDIR)
MANDIR ?= $(DATAROOTDIR)/man
MAN1DIR ?= $(MANDIR)/man1
INFODIR ?= $(DATAROOTDIR)/info
DOCDIR ?= $(DATAROOTDIR)/doc/$(PROJECT)
DESTDIR ?=
```

`DESTDIR` is prepended by the packager to every installed path and is never assigned a value by the
Makefile. Each of these is `?=` because a distribution overrides them:

```makefile
install: all
	$(INSTALL) -d $(DESTDIR)$(BINDIR)
	$(INSTALL) -m 755 $(TARGET) $(DESTDIR)$(BINDIR)/
	$(INSTALL) -d $(DESTDIR)$(INCLUDEDIR)/$(PROJECT)
	$(INSTALL) -m 644 $(HEADERS) $(DESTDIR)$(INCLUDEDIR)/$(PROJECT)/
	$(INSTALL) -d $(DESTDIR)$(MAN1DIR)
	$(INSTALL) -m 644 docs/$(PROJECT).1 $(DESTDIR)$(MAN1DIR)/
```

## pkg-config

```makefile
PACKAGES := openssl zlib

override CFLAGS += $(shell $(PKG_CONFIG) --cflags $(PACKAGES))
override LDLIBS += $(shell $(PKG_CONFIG) --libs $(PACKAGES))

ifeq ($(shell $(PKG_CONFIG) --exists $(PACKAGES) && echo yes),)
$(error missing development packages: $(PACKAGES))
endif
```

Never hard-code `-I/usr/include/openssl`; it is wrong on macOS, wrong on Alpine and wrong under any
cross-compilation. The `--exists` guard turns a link error deep in the build into a message at parse
time.

## VPATH

```makefile
VPATH = src:include
vpath %.c src
vpath %.h include
```

`VPATH` is a global search path for every prerequisite; `vpath` applies to a pattern. Both are legacy
mechanisms that pre-date pattern rules with explicit directories, and both surprise readers when two
directories contain the same filename. Prefer explicit directories in the rules; read this section when a
legacy file uses them.

## Compiler caches and distributed compilation

```makefile
ifneq ($(shell command -v ccache 2>/dev/null),)
override CC := ccache $(CC)
override CXX := ccache $(CXX)
endif
```

`ccache` caches preprocessed compilation results, so switching branches and rebuilding is dramatically
cheaper. Measure the effect on your own project rather than quoting a figure: `time make clean && time
make -j$(nproc)` with and without it. `distcc` distributes compilation across hosts and combines with
`ccache`; its job count is the sum of the remote slots, not `nproc`.

## Precompiled headers, LTO and unity builds

```makefile
# Precompiled header
$(OBJDIR)/common.h.gch: $(SRCDIR)/common.h | $(OBJDIR)
	$(CC) $(CPPFLAGS) $(CFLAGS) -x c-header $< -o $@

$(OBJDIR)/%.o: $(SRCDIR)/%.c $(OBJDIR)/common.h.gch | $(OBJDIR)
	$(CC) $(CPPFLAGS) $(CFLAGS) -include $(OBJDIR)/common.h $(DEPFLAGS) -c $< -o $@
```

```makefile
# Link-time optimisation, release only
release: override CFLAGS += -flto -O3 -DNDEBUG
release: override LDFLAGS += -flto -O3
release: $(TARGET)
```

```makefile
# Unity build: one translation unit. Compiles faster in total, but serially.
$(BUILDDIR)/unity.c: $(SOURCES) | $(BUILDDIR)
	printf '#include "%s"\n' $(SOURCES) > $@
```

Each of these trades something. A precompiled header must be rebuilt whenever anything it includes
changes, and it invalidates every object when it does. LTO moves optimisation to link time, which is
serial, so it can make a parallel build slower in wall-clock terms while making the binary faster. A
unity build removes the parallelism entirely and makes every edit a full rebuild. Measure before adopting
any of them; `optimization-guide.md` owns the parallel-build mechanics that these interact with.

## Intermediate objects

Make treats an object produced only as a step in a chain as intermediate and deletes it, which looks like
a broken cache. `.NOTINTERMEDIATE` (GNU Make 4.4+) or `.SECONDARY` (any release) stops that;
`optimization-guide.md` owns both.

## Java

```makefile
JAVAC ?= javac
JAVA ?= java
JAR ?= jar
JAVAC_FLAGS ?= -Xlint:all -encoding UTF-8

JAVA_SOURCES := $(shell find $(SRCDIR) -name '*.java')

$(CLASSDIR)/.compiled: $(JAVA_SOURCES) | $(CLASSDIR)
	$(JAVAC) $(JAVAC_FLAGS) -d $(CLASSDIR) -cp "$(CLASSPATH)" $(JAVA_SOURCES)
	touch $@
```

`javac` compiles the whole source set in one invocation and produces class files whose names do not map
one-to-one onto sources — an inner class, a lambda and an anonymous class each add files. A per-file
pattern rule therefore does not work. The stamp file `$(CLASSDIR)/.compiled` is the target make tracks,
and `touch $@` updates it after a successful compile.

For anything beyond a single JAR, use the project's real build tool. Make is not a substitute for Maven
or Gradle in a Java project with dependencies.

## What this file does not decide

- The preamble, section order and includes: `makefile-structure.md`.
- Assignment operators and override precedence: `variables-guide.md`.
- `.PHONY`, standard targets and order-only prerequisites: `targets-guide.md`.
- Pattern rules and automatic variables: `patterns-guide.md`.
- Parallel safety, intermediate files and the debugging flags: `optimization-guide.md`.
- Complexity budgets for the code being compiled: `/alaa-algorithms-data-structures`
  (`$alaa-algorithms-data-structures`).
