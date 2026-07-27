#!/usr/bin/env python3
"""Static checker for HAProxy Lua modules.

Detects the defect classes that survive code review but change behaviour at the
edge: CPU-time used as a clock or as entropy, failure signalled by returning
nil, error messages that carry an absolute source path, Lua 5.3-only syntax with
no recorded minimum version, unguarded load-time access to the HAProxy `core`
object, and stdlib calls HAProxy forbids at runtime.

The checker is lexical: it strips Lua comments and string literals, then tracks
block nesting so that a rule can ask whether a token sits inside a function body
or in the file body. It never executes the module under test.
"""

import argparse
import os
import re
import sys
import tempfile

VERSION = "1.0.0"

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
        # start points at '['. Returns (content_end_exclusive, level) or None.
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


BLOCK_TOKEN = re.compile(
    r"\b(function|if|for|while|do|repeat|until|end|then)\b"
)


def block_depth_map(scrubbed):
    """Map each character offset to (block_depth, inside_function).

    The stack tracks Lua block openers so a rule can distinguish the file body
    (depth 0) from code inside a function.
    """
    depths = [(0, False)] * (len(scrubbed) + 1)
    stack = []
    pos = 0
    for m in BLOCK_TOKEN.finditer(scrubbed):
        state = (len(stack), any(s == "function" for s in stack))
        for k in range(pos, m.start()):
            depths[k] = state
        tok = m.group(1)
        if tok == "function":
            stack.append("function")
        elif tok == "if":
            stack.append("if")
        elif tok == "for":
            stack.append("for_head")
        elif tok == "while":
            stack.append("while_head")
        elif tok == "do":
            if stack and stack[-1] in ("for_head", "while_head"):
                stack[-1] = stack[-1].replace("_head", "")
            else:
                stack.append("do")
        elif tok == "repeat":
            stack.append("repeat")
        elif tok == "until":
            if stack and stack[-1] == "repeat":
                stack.pop()
        elif tok == "end":
            if stack:
                stack.pop()
        state = (len(stack), any(s == "function" for s in stack))
        for k in range(m.start(), m.end()):
            depths[k] = state
        pos = m.end()
    state = (len(stack), any(s == "function" for s in stack))
    for k in range(pos, len(scrubbed) + 1):
        depths[k] = state
    return depths


def line_of(source, offset):
    return source.count("\n", 0, offset) + 1


def line_text(source, lineno):
    lines = source.splitlines()
    if 1 <= lineno <= len(lines):
        return lines[lineno - 1].strip()
    return ""


# --------------------------------------------------------------------------
# Checks
# --------------------------------------------------------------------------

REGISTER_RE = re.compile(
    r"core\.register_(converters|fetches|action|service|filter|task|cli|init)\b"
)
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
LUA53_CONSTRUCTS = [
    (r"[^<>=~]>>[^>]", "the >> operator"),
    (r"[^<>=~]<<[^<]", "the << operator"),
    (r"\bmath\.tointeger\s*\(", "math.tointeger"),
    (r"\bmath\.type\s*\(", "math.type"),
    (r"[^/]//[^/]", "the // integer-division operator"),
]


class Finding:
    def __init__(self, code, path, lineno, summary, obligation, evidence):
        self.code = code
        self.path = path
        self.lineno = lineno
        self.summary = summary
        self.obligation = obligation
        self.evidence = evidence

    def render(self):
        return (
            "{p}:{l}: {c} {s}\n"
            "    evidence: {e}\n"
            "    fix: {o}".format(
                p=self.path,
                l=self.lineno,
                c=self.code,
                s=self.summary,
                e=self.evidence,
                o=self.obligation,
            )
        )


def check_source(path, source):
    findings = []
    scrubbed = scrub(source)
    depths = block_depth_map(scrubbed)
    registers = bool(REGISTER_RE.search(scrubbed))

    def add(code, offset, summary, obligation):
        lineno = line_of(source, offset)
        findings.append(
            Finding(code, path, lineno, summary, obligation, line_text(source, lineno))
        )

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
    # source. The seed then comes from the clock or from a Lua default, and
    # every process that starts in the same second produces the same stream.
    has_entropy_source = "/dev/urandom" in source
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

    # HL004 - failure signalled by returning nil.
    for m in re.finditer(r"\breturn\s+nil\b", scrubbed):
        inside_function = depths[m.start()][1]
        if inside_function:
            add(
                "HL004",
                m.start(),
                "returning nil from a Lua handler produces a HAProxy boolean-false "
                "sample, which sets the variable and renders as 0",
                "Call error(message, 0) instead so the sample fails, the variable stays "
                "unset, and a config rule can reject the request.",
            )

    # HL009 - pcall around a handler that then returns nil.
    if re.search(r"\bpcall\s*\(", scrubbed) and re.search(r"\breturn\s+nil\b", scrubbed):
        m = re.search(r"\bpcall\s*\(", scrubbed)
        add(
            "HL009",
            m.start(),
            "pcall() combined with a nil return converts every failure into a "
            "successful-looking sample",
            "Let the error propagate to HAProxy, which logs it and fails the sample.",
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
                        "{0} is forbidden at runtime because it blocks the HAProxy "
                        "scheduler".format(label),
                        "Move the call into the file body or core.register_init, which "
                        "run before traffic, and store the result in an upvalue.",
                    )

    findings.sort(key=lambda f: (f.lineno, f.code))
    return findings


# --------------------------------------------------------------------------
# Self test
# --------------------------------------------------------------------------

BAD_FIXTURE = """
local M = {}

local seeded = false
local function ensure_seeded()
    if seeded then return end
    local seed = os.time() + math.floor(os.clock() * 1000000)
    math.randomseed(seed)
    seeded = true
end

function M.stamp()
    local ms = (os.time() * 1000) + math.floor((os.clock() * 1000) % 1000)
    return ms >> 8
end

function M.check(value)
    if value == "" then
        error("empty value")
    end
    local ok, res = pcall(function() return math.tointeger(value) end)
    if not ok then
        return nil
    end
    print("checked")
    return res
end

core.register_converters("stamp", M.stamp)

return M
"""

GOOD_FIXTURE = """
-- Requires Lua 5.3 or newer.
local M = {}

local ALLOWED = {}
for i = 48, 57 do ALLOWED[i] = true end

function M.check(value)
    if type(value) ~= "string" then
        error("check: sample is not a string", 0)
    end
    if #value == 0 or #value > 64 then
        error("check: length outside [1,64]", 0)
    end
    for i = 1, #value do
        if not ALLOWED[string.byte(value, i)] then
            error("check: byte at offset " .. i .. " is not allowed", 0)
        end
    end
    return value
end

if core ~= nil and core.register_converters ~= nil then
    core.register_converters("check", M.check)
end

return M
"""


def self_test():
    cases = []
    bad = check_source("<bad-fixture>", BAD_FIXTURE)
    codes = {f.code for f in bad}
    for expected in (
        "HL001",
        "HL002",
        "HL003",
        "HL004",
        "HL005",
        "HL006",
        "HL007",
        "HL008",
        "HL009",
    ):
        cases.append(("bad fixture reports " + expected, expected in codes))
    good = check_source("<good-fixture>", GOOD_FIXTURE)
    cases.append(("good fixture reports nothing", good == []))
    scrubbed = scrub('local s = "os.clock()" -- os.clock()\nlocal t = os.clock()\n')
    cases.append(
        ("string and comment occurrences are ignored", scrubbed.count("os.clock") == 1)
    )
    depths = block_depth_map(scrub("for i = 1, 2 do end\nfunction f() end\n"))
    cases.append(("for ... do counts as one block", depths[-1] == (0, False)))

    failed = [name for name, ok in cases if not ok]
    for name, ok in cases:
        print("{0} {1}".format("ok  " if ok else "FAIL", name))
    print("")
    print("{0} of {1} self-test cases passed".format(len(cases) - len(failed), len(cases)))
    return 0 if not failed else 3


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

EPILOG = """\
exit codes:
  0  no finding. The module may ship.
  1  at least one finding. Fix every finding, then run this checker again; do
     not ship the module while any finding stands.
  2  a path could not be read or the arguments were wrong. Correct the
     invocation and rerun; no file was checked.
  3  --self-test failed, so the checker itself is untrustworthy. Report the
     failing case and check the module by hand until the checker passes.

checks:
  HL001  os.clock() used anywhere
  HL002  math.randomseed() seeded from the clock
  HL003  error() called without level 0
  HL004  return nil inside a function body. A registered handler must raise
         instead. An internal helper may legitimately return nil, and then the
         obligation is to show that no handler's failure path returns it onward.
  HL005  Lua 5.3-only construct with no minimum version recorded in a comment
  HL006  core touched in the file body outside a guard
  HL007  runtime-forbidden stdlib call inside a function body. It is permitted
         only when that function is called solely from the file body or from
         core.register_init, which run before traffic; name the call site.
  HL008  os.time() multiplied to fake sub-second resolution
  HL009  pcall() paired with a nil return

Checks HL004 and HL007 are reachability questions that a lexical checker cannot
settle. Both are reported wherever the pattern appears, and clearing one means
naming the call site rather than deleting the check.
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
        help="run the checker against its own fixtures and exit",
    )
    parser.add_argument("--version", action="version", version=VERSION)
    args = parser.parse_args(argv)

    if args.self_test:
        return self_test()

    if not args.paths:
        parser.print_usage(sys.stderr)
        sys.stderr.write("error: give at least one Lua file, or --self-test\n")
        return 2

    all_findings = []
    for path in args.paths:
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as handle:
                source = handle.read()
        except OSError as exc:
            sys.stderr.write("error: {0}\n".format(exc))
            return 2
        all_findings.extend(check_source(path, source))

    for finding in all_findings:
        print(finding.render())

    checked = len(args.paths)
    print("")
    print(
        "{0} file(s) checked, {1} finding(s)".format(checked, len(all_findings))
    )
    return 1 if all_findings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
