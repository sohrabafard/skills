#!/usr/bin/env python3
"""Static checker for HAProxy Lua modules.

Detects the defect classes that survive code review but change behaviour at the
edge: CPU-time used as a clock or as entropy, failure signalled by returning nil
from a handler whose return value HAProxy reads, error messages that carry an
absolute source path, Lua 5.3-only syntax with no recorded minimum version,
unguarded load-time access to the HAProxy `core` object, and stdlib calls
HAProxy forbids at runtime.

The checker is lexical: it strips Lua comments and string literals, then tracks
block nesting so that a rule can ask whether a token sits inside a function body,
in the file body, or inside one specific registered handler. It never executes
the module under test.

Windows: standard library only, pathlib for every path, no temp directory.
"""

import argparse
import re
import sys
from pathlib import Path

VERSION = "2.0.0"

EXIT_CLEAN = 0
EXIT_FINDINGS = 1
EXIT_CANNOT_RUN = 2

# --------------------------------------------------------------------------
# Lua lexical scrubbing
# --------------------------------------------------------------------------


def scrub(source):
    """Return source with comments and string literals replaced by spaces.

    Line numbers and column offsets are preserved so that a match position in
    the scrubbed text is a valid position in the original text.
    """
    out = list(source)
    i = 0
    n = len(source)

    def blank(start, end):
        for k in range(start, min(end, n)):
            if out[k] != "\n":
                out[k] = " "

    def long_bracket_end(start):
        # start points at '['. Returns the offset just past the closing bracket.
        m = re.compile(r"\[(=*)\[").match(source, start)
        if not m:
            return None
        level = len(m.group(1))
        close = "]" + ("=" * level) + "]"
        idx = source.find(close, m.end())
        if idx == -1:
            return n
        return idx + len(close)

    while i < n:
        ch = source[i]
        if ch == "-" and source.startswith("--", i):
            lb = long_bracket_end(i + 2) if source.startswith("[", i + 2) else None
            if lb is not None:
                blank(i, lb)
                i = lb
                continue
            j = source.find("\n", i)
            j = n if j == -1 else j
            blank(i, j)
            i = j
            continue
        if ch in ("'", '"'):
            j = i + 1
            while j < n:
                if source[j] == "\\":
                    j += 2
                    continue
                if source[j] == ch or source[j] == "\n":
                    break
                j += 1
            blank(i, min(j + 1, n))
            i = min(j + 1, n)
            continue
        if ch == "[":
            lb = long_bracket_end(i)
            if lb is not None:
                blank(i, lb)
                i = lb
                continue
        i += 1
    return "".join(out)


BLOCK_TOKEN = re.compile(r"\b(function|if|for|while|do|repeat|until|end|then)\b")


def _step_stack(stack, tok, offset):
    """Apply one block token to the nesting stack. Returns the popped entry or None."""
    if tok == "function":
        stack.append(("function", offset))
    elif tok == "if":
        stack.append(("if", offset))
    elif tok == "for":
        stack.append(("for_head", offset))
    elif tok == "while":
        stack.append(("while_head", offset))
    elif tok == "do":
        if stack and stack[-1][0] in ("for_head", "while_head"):
            stack[-1] = (stack[-1][0].replace("_head", ""), stack[-1][1])
        else:
            stack.append(("do", offset))
    elif tok == "repeat":
        stack.append(("repeat", offset))
    elif tok == "until":
        if stack and stack[-1][0] == "repeat":
            return stack.pop()
    elif tok == "end":
        if stack:
            return stack.pop()
    return None


def block_depth_map(scrubbed):
    """Map each character offset to (block_depth, inside_function).

    The stack tracks Lua block openers so a rule can distinguish the file body
    (depth 0) from code inside a function.
    """
    depths = [(0, False)] * (len(scrubbed) + 1)
    stack = []
    pos = 0
    for m in BLOCK_TOKEN.finditer(scrubbed):
        state = (len(stack), any(kind == "function" for kind, _ in stack))
        for k in range(pos, m.start()):
            depths[k] = state
        _step_stack(stack, m.group(1), m.start())
        state = (len(stack), any(kind == "function" for kind, _ in stack))
        for k in range(m.start(), m.end()):
            depths[k] = state
        pos = m.end()
    state = (len(stack), any(kind == "function" for kind, _ in stack))
    for k in range(pos, len(scrubbed) + 1):
        depths[k] = state
    return depths


def function_spans(scrubbed):
    """Return (start, end) for every function body in the file.

    start is the offset of the `function` keyword and end is the offset just past
    the `end` that closes it. A function left unclosed by a truncated or invalid
    file yields a span running to the end of the text, which keeps every caller
    conservative rather than silently empty.
    """
    spans = []
    stack = []
    for m in BLOCK_TOKEN.finditer(scrubbed):
        popped = _step_stack(stack, m.group(1), m.start())
        if popped is not None and popped[0] == "function":
            spans.append((popped[1], m.end()))
    while stack:
        kind, start = stack.pop()
        if kind == "function":
            spans.append((start, len(scrubbed)))
    return sorted(set(spans))


# --------------------------------------------------------------------------
# Which handlers HAProxy reads a return value back from
# --------------------------------------------------------------------------
#
# HAProxy turns the value returned by a converter or a sample fetch into a sample
# and uses it. It reads nothing back from an action, a service, a task, an init
# function, or a CLI handler: doc/lua-api/index.rst gives those prototypes as
# returning nothing. So "failure signalled by returning nil" is a defect only
# inside a converter or a sample fetch, and the internal `return nil, err` pair
# that HAProxy never sees is idiomatic Lua and not a finding. Reporting it
# everywhere was measured against this fleet's only Lua estate on 31 July 2026:
# 35 of 54 findings were that false positive, and a checker with that rate is
# switched off, which silently discards its true findings too.

REGISTER_RE = re.compile(
    r"core\.register_(converters|fetches|action|service|filter|task|cli|init)\b"
)
SAMPLE_REGISTER_RE = re.compile(r"core\.register_(converters|fetches)\s*\(")
IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*(\.[A-Za-z_][A-Za-z0-9_]*)*$")

VERSION_MARKER_RE = re.compile(r"--[^\n]*\blua\b[^\n]*\b5\.[3-9]\b", re.IGNORECASE)
FORBIDDEN_RUNTIME = [
    (r"\bio\.[a-z_]+\s*\(", "io.*"),
    (r"\bos\.execute\s*\(", "os.execute"),
    (r"\bos\.exit\s*\(", "os.exit"),
    (r"\bos\.remove\s*\(", "os.remove"),
    (r"\bos\.rename\s*\(", "os.rename"),
    (r"\bos\.tmpname\s*\(", "os.tmpname"),
    (r"\bpackage\.[a-z_]+", "package.*"),
    (r"(?<![.:\w])print\s*\(", "print"),
]
# A file that seeds from the operating system names the device inside a string
# literal, so the suppression test requires the quotes. Searching the raw source for
# the bare path let a comment that merely mentions the device silence the check; the
# committed red fixture for HL002 mentions it in a comment for exactly that reason.
ENTROPY_SOURCE_RE = re.compile(r"""["']/dev/urandom["']""")
LUA53_CONSTRUCTS = [
    (r"[^<>=~]>>[^>]", "the >> operator"),
    (r"[^<>=~]<<[^<]", "the << operator"),
    (r"\bmath\.tointeger\s*\(", "math.tointeger"),
    (r"\bmath\.type\s*\(", "math.type"),
    (r"[^/]//[^/]", "the // integer-division operator"),
]


def split_call_arguments(scrubbed, open_paren_end):
    """Return [(text, start_offset)] for the top-level arguments of one call.

    open_paren_end is the offset just past the call's opening parenthesis.
    Returns None when the parenthesis is never closed.
    """
    args = []
    depth = 1
    start = open_paren_end
    for i in range(open_paren_end, len(scrubbed)):
        ch = scrubbed[i]
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
            if depth == 0:
                args.append((scrubbed[start:i], start))
                return args
        elif ch == "," and depth == 1:
            args.append((scrubbed[start:i], start))
            start = i + 1
    return None


def definition_spans(scrubbed, name, by_start):
    """Return the function spans defining `name`, by any of the three Lua forms."""
    candidates = [name]
    if "." in name:
        candidates.append(name.rsplit(".", 1)[1])
    for candidate in candidates:
        escaped = re.escape(candidate)
        found = []
        for m in re.finditer(r"\bfunction\s+" + escaped + r"\s*\(", scrubbed):
            if m.start() in by_start:
                found.append(by_start[m.start()])
        for m in re.finditer(r"\b" + escaped + r"\s*=\s*(function)\s*\(", scrubbed):
            if m.start(1) in by_start:
                found.append(by_start[m.start(1)])
        if found:
            return found
    return []


def sample_handler_spans(scrubbed, spans):
    """Return (resolved_spans, unresolved_registration_offsets).

    resolved_spans are the bodies of every function registered as a converter or a
    sample fetch. unresolved_registration_offsets are registrations whose handler
    argument is neither an inline function literal nor a resolvable name, so the
    body cannot be located and HL004 cannot be evaluated for it.
    """
    by_start = dict((start, (start, end)) for start, end in spans)
    resolved = []
    unresolved = []
    for m in SAMPLE_REGISTER_RE.finditer(scrubbed):
        args = split_call_arguments(scrubbed, m.end())
        if args is None or len(args) < 2:
            unresolved.append(m.start())
            continue
        text, offset = args[1]
        stripped = text.strip()
        if stripped.startswith("function"):
            keyword_at = offset + (len(text) - len(text.lstrip()))
            if keyword_at in by_start:
                resolved.append(by_start[keyword_at])
            else:
                unresolved.append(m.start())
            continue
        if IDENTIFIER_RE.match(stripped):
            found = definition_spans(scrubbed, stripped, by_start)
            if found:
                resolved.extend(found)
            else:
                unresolved.append(m.start())
            continue
        unresolved.append(m.start())
    return sorted(set(resolved)), unresolved


def line_of(source, offset):
    return source.count("\n", 0, offset) + 1


def line_text(source, lineno):
    lines = source.splitlines()
    if 1 <= lineno <= len(lines):
        return lines[lineno - 1].strip()
    return ""


class Finding:
    def __init__(self, code, path, lineno, summary, obligation, evidence):
        self.code = code
        self.path = path
        self.lineno = lineno
        self.summary = summary
        self.obligation = obligation
        self.evidence = evidence

    def render(self):
        return "{p}:{l}: {c} {s}\n    evidence: {e}\n    fix: {o}".format(
            p=self.path,
            l=self.lineno,
            c=self.code,
            s=self.summary,
            e=self.evidence,
            o=self.obligation,
        )


def check_source(path, source):
    findings = []
    scrubbed = scrub(source)
    depths = block_depth_map(scrubbed)
    spans = function_spans(scrubbed)
    sample_spans, unresolved_registrations = sample_handler_spans(scrubbed, spans)
    registers = bool(REGISTER_RE.search(scrubbed))

    def add(code, offset, summary, obligation):
        lineno = line_of(source, offset)
        findings.append(
            Finding(code, path, lineno, summary, obligation, line_text(source, lineno))
        )

    def inside_sample_handler(offset):
        return any(start <= offset < end for start, end in sample_spans)

    # HL001 - os.clock is process CPU time, never a clock and never entropy.
    for m in re.finditer(r"\bos\.clock\s*\(", scrubbed):
        add(
            "HL001",
            m.start(),
            "os.clock() is process CPU time, not wall-clock time",
            "Replace with core.now(), which returns a table of sec and usec taken "
            "from the HAProxy clock.",
        )

    # HL008 - os.time scaled past one-second resolution.
    for m in re.finditer(r"\bos\.time\s*\(\s*\)\s*\*\s*\d+", scrubbed):
        add(
            "HL008",
            m.start(),
            "os.time() has one-second resolution, so multiplying it does not add "
            "sub-second precision",
            "Take milliseconds from core.now(): local n = core.now(); local ms = "
            "n.sec * 1000 + n.usec // 1000.",
        )

    # HL002 - seeding the Lua PRNG without reading an operating-system entropy
    # source. The seed then comes from the clock or from a Lua default, and every
    # process that starts in the same second produces the same stream.
    has_entropy_source = bool(ENTROPY_SOURCE_RE.search(source))
    for m in re.finditer(r"\bmath\.randomseed\s*\(", scrubbed):
        if not has_entropy_source:
            add(
                "HL002",
                m.start(),
                "math.randomseed() is called in a file that never reads /dev/urandom, "
                "so the seed comes from the clock and processes starting in the same "
                "second produce the same stream",
                "Read 8 bytes from /dev/urandom in the file body or in "
                "core.register_init and seed from those bytes, or delete the generator "
                "and use the native uuid() sample fetch.",
            )

    # HL003 - error() without level 0 prefixes the message with file:line.
    for m in re.finditer(r"(?<![.:\w])error\s*\(", scrubbed):
        depth = 1
        j = m.end()
        args_start = j
        while j < len(scrubbed) and depth > 0:
            if scrubbed[j] == "(":
                depth += 1
            elif scrubbed[j] == ")":
                depth -= 1
            j += 1
        args = scrubbed[args_start : j - 1]
        top = 0
        has_level = False
        for k, ch in enumerate(args):
            if ch in "([{":
                top += 1
            elif ch in ")]}":
                top -= 1
            elif ch == "," and top == 0:
                if args[k + 1 :].strip() == "0":
                    has_level = True
        if not has_level:
            add(
                "HL003",
                m.start(),
                "error() without level 0 prefixes the operator-facing message with the "
                "absolute source path and line number",
                "Call error(message, 0) so the logged message is the message you wrote.",
            )

    # HL004 - failure signalled by returning nil from a handler HAProxy reads back.
    for m in re.finditer(r"\breturn\s+nil\b", scrubbed):
        if not depths[m.start()][1]:
            continue
        if not inside_sample_handler(m.start()):
            continue
        add(
            "HL004",
            m.start(),
            "a registered converter or sample fetch returns nil, which HAProxy turns "
            "into a boolean-false sample: the variable is set and renders as 0",
            "Call error(message, 0) instead so the sample fails, the variable stays "
            "unset, and a config rule can reject the request.",
        )

    # HL009 - pcall and a nil return inside the same converter or sample fetch.
    for start, end in sample_spans:
        region = scrubbed[start:end]
        pcall_match = re.search(r"\bpcall\s*\(", region)
        nil_match = re.search(r"\breturn\s+nil\b", region)
        if pcall_match and nil_match:
            add(
                "HL009",
                start + pcall_match.start(),
                "pcall() and a nil return inside the same converter or sample fetch "
                "convert every failure into a successful-looking sample",
                "Let the error propagate to HAProxy, which logs it and fails the "
                "sample, or re-raise with error(message, 0) after inspecting it.",
            )

    # HL010 - a converter or fetch registration whose handler body cannot be found.
    for offset in unresolved_registrations:
        add(
            "HL010",
            offset,
            "a converter or sample fetch is registered with a handler expression this "
            "checker cannot resolve to a function body, so HL004 was not evaluated "
            "for that handler",
            "Register a named function or an inline function literal so the failure "
            "path is locatable; if a factory is deliberate, review the returned "
            "closure by hand for a nil return and record that review.",
        )

    # HL005 - Lua 5.3-only constructs with no recorded minimum version.
    if not VERSION_MARKER_RE.search(source):
        for pattern, label in LUA53_CONSTRUCTS:
            m = re.search(pattern, scrubbed)
            if m:
                add(
                    "HL005",
                    m.start(),
                    "{0} requires Lua 5.3 or newer and the file records no minimum "
                    "version".format(label),
                    "Add a comment naming the minimum Lua version, for example "
                    "-- Requires Lua 5.3 or newer.",
                )

    # HL006 - load-time core access outside a guard.
    for m in re.finditer(r"(?<![.:\w])core\s*[.\[]", scrubbed):
        depth, _ = depths[m.start()]
        if depth == 0:
            add(
                "HL006",
                m.start(),
                "the file body touches core outside any guard, so the module cannot be "
                "loaded by a unit test",
                "Wrap every registration in if core ~= nil and core.register_converters "
                "~= nil then ... end and return the module table.",
            )

    # HL007 - stdlib calls HAProxy forbids at runtime, inside a function body.
    if registers:
        for pattern, label in FORBIDDEN_RUNTIME:
            for m in re.finditer(pattern, scrubbed):
                if depths[m.start()][1]:
                    add(
                        "HL007",
                        m.start(),
                        "{0} is forbidden at runtime because it never yields and stalls "
                        "the HAProxy scheduler".format(label),
                        "Move the call into the file body or core.register_init, which "
                        "run before traffic, and store the result in an upvalue. For "
                        "network work inside a handler use core.tcp(), which yields.",
                    )

    findings.sort(key=lambda f: (f.lineno, f.code))
    return findings


# --------------------------------------------------------------------------
# Self test, against committed fixtures
# --------------------------------------------------------------------------

# scripts/ and test/fixtures/ are siblings inside the skill directory. The path is
# built from this file's own resolved location so the checker runs from any working
# directory, on Windows as well as on Linux.
FIXTURES = Path(__file__).resolve().parent.parent / "test" / "fixtures"

RED_FIXTURES = (
    ("red-hl001-os-clock.lua", "HL001"),
    ("red-hl002-clock-seed.lua", "HL002"),
    ("red-hl003-error-no-level.lua", "HL003"),
    ("red-hl004-converter-returns-nil.lua", "HL004"),
    ("red-hl005-lua53-no-version.lua", "HL005"),
    ("red-hl006-unguarded-core.lua", "HL006"),
    ("red-hl007-forbidden-runtime.lua", "HL007"),
    ("red-hl008-os-time-scaled.lua", "HL008"),
    ("red-hl009-pcall-nil.lua", "HL009"),
    ("red-hl010-unresolvable-handler.lua", "HL010"),
)
GREEN_FIXTURES = ("green-converter-module.lua", "green-action-module.lua")


def read_fixture(name):
    """Return the text of one fixture, or raise OSError when it cannot be read."""
    return (FIXTURES / name).read_text(encoding="utf-8")


def self_test():
    """Run every assertion against the committed fixtures.

    Returns 0 when every case passes, 1 when any case fails, and 2 when a fixture
    could not be read, so that a missing fixture can never be mistaken for a pass.
    """
    if not FIXTURES.is_dir():
        sys.stderr.write(
            "error: fixture directory not found: {0}\n".format(FIXTURES)
        )
        return EXIT_CANNOT_RUN

    cases = []
    try:
        for name, code in RED_FIXTURES:
            codes = set(f.code for f in check_source(name, read_fixture(name)))
            cases.append((name + " reports " + code, code in codes))
        for name in GREEN_FIXTURES:
            found = check_source(name, read_fixture(name))
            cases.append(
                (
                    name + " reports nothing",
                    found == [],
                    "" if found == [] else found[0].render(),
                )
            )
        action_codes = set(
            f.code
            for f in check_source(
                "green-action-module.lua", read_fixture("green-action-module.lua")
            )
        )
    except OSError as exc:
        sys.stderr.write("error: fixture unreadable: {0}\n".format(exc))
        return EXIT_CANNOT_RUN

    # The regression that this checker version exists for: an action-only module
    # using the idiomatic "return nil, err" pair and a pcall must produce neither
    # HL004 nor HL009, because HAProxy reads no return value back from an action.
    cases.append(
        (
            "an action-only module reports no HL004 and no HL009",
            not (action_codes & {"HL004", "HL009"}),
        )
    )
    cases.append(
        (
            "string and comment occurrences are ignored",
            scrub('local s = "os.clock()" -- os.clock()\nlocal t = os.clock()\n').count(
                "os.clock"
            )
            == 1,
        )
    )
    cases.append(
        (
            "for ... do counts as one block",
            block_depth_map(scrub("for i = 1, 2 do end\nfunction f() end\n"))[-1]
            == (0, False),
        )
    )

    failed = 0
    for case in cases:
        name, ok = case[0], case[1]
        detail = case[2] if len(case) > 2 and not ok else ""
        print("{0} {1}".format("ok  " if ok else "FAIL", name))
        if detail:
            print("     " + detail.replace("\n", "\n     "))
        if not ok:
            failed += 1
    print("")
    print("{0} of {1} self-test cases passed".format(len(cases) - failed, len(cases)))
    return EXIT_CLEAN if failed == 0 else EXIT_FINDINGS


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

EPILOG = """\
exit codes:
  0  no finding, or every self-test case passed. The module may ship.
  1  at least one finding, or a self-test case failed. Fix every finding, then run
     this checker again; do not ship the module while any finding stands.
  2  a path could not be read, the fixture directory is missing, or the arguments
     were wrong. Nothing was checked. Correct the invocation and rerun; never read
     this exit code as a pass.

checks:
  HL001  os.clock() used anywhere
  HL002  math.randomseed() seeded from the clock
  HL003  error() called without level 0
  HL004  return nil inside a function registered as a converter or a sample fetch.
         Those are the only two handler types whose return value HAProxy reads back
         and turns into a sample. An action, service, task, init or CLI handler
         returns nothing HAProxy consumes, so an internal "return nil, err" pair in
         such a module is idiomatic Lua and is not reported.
  HL005  Lua 5.3-only construct with no minimum version recorded in a comment
  HL006  core touched in the file body outside a guard
  HL007  runtime-forbidden stdlib call inside a function body. It is permitted only
         when that function is called solely from the file body or from
         core.register_init, which run before traffic; name the call site. Network
         work inside a handler belongs on core.tcp(), which yields and is not
         reported here.
  HL008  os.time() multiplied to fake sub-second resolution
  HL009  pcall() and a nil return inside the same converter or sample fetch
  HL010  a converter or sample fetch registered with a handler expression whose body
         this checker cannot locate, so HL004 was not evaluated for it

limits, stated rather than hidden:
  HL004 sees a nil returned directly by the handler. A converter written as
  `return decode(value)` whose helper returns nil is the same defect and is not
  lexically detectable; the obligation for that shape is in
  references/30-failure-visibility.md.
  HL007 is a reachability question a lexical checker cannot settle, so it is
  reported wherever the pattern appears inside a function body, and clearing it
  means naming the call site rather than deleting the check.
"""


def main(argv):
    parser = argparse.ArgumentParser(
        prog="check_haproxy_lua.py",
        description="Check HAProxy Lua modules for edge-behaviour defects.",
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("paths", nargs="*", help="Lua files to check")
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="run the checker against its committed fixtures and exit",
    )
    parser.add_argument("--version", action="version", version=VERSION)
    args = parser.parse_args(argv)

    if args.self_test:
        return self_test()

    if not args.paths:
        parser.print_usage(sys.stderr)
        sys.stderr.write("error: give at least one Lua file, or --self-test\n")
        return EXIT_CANNOT_RUN

    all_findings = []
    for path in args.paths:
        try:
            source = Path(path).read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            sys.stderr.write("error: {0}\n".format(exc))
            return EXIT_CANNOT_RUN
        all_findings.extend(check_source(path, source))

    for finding in all_findings:
        print(finding.render())

    print("")
    print("{0} file(s) checked, {1} finding(s)".format(len(args.paths), len(all_findings)))
    return EXIT_FINDINGS if all_findings else EXIT_CLEAN


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
