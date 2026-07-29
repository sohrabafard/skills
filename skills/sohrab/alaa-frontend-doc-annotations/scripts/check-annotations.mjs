#!/usr/bin/env node
// check-annotations.mjs - annotation checker for alaa-frontend-doc-annotations.
// Checks comments against the code they claim to describe. It never edits a file.
// Exit codes: 0 clean, 1 findings, 2 could not run.

import { execFileSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";

const RULES = {
  ANN101: "exported symbol in a module imported by 2+ modules has no /** */ block",
  ANN201: "NOTE: prefix outside the closed set",
  ANN301: "AUTH NOTE:/SECURITY NOTE: without verified:<ISO-date>",
  ANN302: "file changed after the verified: date on its security annotation",
  ANN401: "JSDoc type annotation in a TypeScript context",
  ANN501: "community or issue-tracker URL inside a comment",
  ANN601: "non-ASCII character in a comment body"
};

const PREFIXES = new Set([
  "SSR NOTE:",
  "HYDRATION NOTE:",
  "STORE NOTE:",
  "AUTH NOTE:",
  "SECURITY NOTE:"
]);

const SECURITY_PREFIXES = new Set(["AUTH NOTE:", "SECURITY NOTE:"]);

const COMMUNITY = [
  /stackoverflow\.com/i,
  /stackexchange\.com/i,
  /superuser\.com/i,
  /serverfault\.com/i,
  /reddit\.com/i,
  /medium\.com/i,
  /dev\.to\//i,
  /github\.com\/[^\s)"']+\/(issues|pull|discussions)\b/i,
  /gitlab\.[^\s)"']+\/-\/(issues|merge_requests)\b/i,
  /\/browse\/[A-Z][A-Z0-9]+-\d+/
];

const SOURCE_EXT = new Set([".ts", ".tsx", ".js", ".mjs", ".cjs", ".vue"]);
const RESOLVE_ORDER = [
  "",
  ".ts",
  ".tsx",
  ".vue",
  ".js",
  ".mjs",
  ".cjs",
  "/index.ts",
  "/index.tsx",
  "/index.vue",
  "/index.js",
  "/index.mjs"
];
const SKIP_DIR = new Set([
  "node_modules",
  "dist",
  ".git",
  ".quasar",
  ".nx",
  "coverage",
  "generated"
]);

const HELP = `check-annotations.mjs - annotation checker (alaa-frontend-doc-annotations)

Usage:
  node scripts/check-annotations.mjs <dir> [<dir>...] [options]
  node scripts/check-annotations.mjs --self-test
  node scripts/check-annotations.mjs --help

Assertions:
  ANN101  every exported function, arrow-const and store action in a module
          imported by two or more other modules carries a leading /** ... */
  ANN201  every "<X> NOTE:" prefix is one of SSR NOTE:, HYDRATION NOTE:,
          STORE NOTE:, AUTH NOTE:, SECURITY NOTE: - the set is closed
  ANN301  every AUTH NOTE: and SECURITY NOTE: carries verified:<ISO-date>
  ANN302  that date is not older than the file's last commit date
  ANN401  no @param {Type} / @returns {Type} in .ts or <script lang="ts">
          (skipped when eslint-plugin-jsdoc check-tag-names typed is configured)
  ANN501  no community or issue-tracker URL inside a comment
  ANN601  every comment body is ASCII-range (files are English)

Options:
  --rules=ANN201,ANN301   run only these rules
  --require-git           exit 2 when git history is unavailable (ANN302)
  --max-findings=N        stop after N findings (default 500)
  --json                  emit findings as JSON on stdout
  --self-test             run built-in fixtures in a temp dir outside any repo
  --help                  this text

Exit codes:
  0  every assertion passed
  1  findings, one "path:line: RULE message" per line on stdout
  2  could not run: no such directory, or a file failed to parse
     (2 is never returned as 0 - an unparsed file is not a clean file)
`;

// ---------------------------------------------------------------- scanning

// Splits source into comment units and a stripped copy where comment and
// string bodies are blanked, so brace matching and export detection see code
// only. Returns { comments, stripped, error }.
function scanSource(src, opts = {}) {
  const startLine = opts.startLine ?? 1;
  const out = new Array(src.length);
  const comments = [];
  let line = startLine;
  let i = 0;
  const n = src.length;
  let lastSignificant = "";

  const blank = (from, to) => {
    for (let k = from; k < to; k += 1) out[k] = src[k] === "\n" ? "\n" : " ";
  };

  while (i < n) {
    const c = src[i];
    const d = src[i + 1];

    if (c === "/" && d === "/") {
      const end = src.indexOf("\n", i);
      const stop = end === -1 ? n : end;
      comments.push({
        kind: "line",
        line,
        body: src.slice(i + 2, stop),
        raw: src.slice(i, stop),
        tsContext: opts.tsContext
      });
      blank(i, stop);
      i = stop;
      continue;
    }

    if (c === "/" && d === "*") {
      const end = src.indexOf("*/", i + 2);
      if (end === -1) return { error: { line, message: "unterminated block comment" } };
      const raw = src.slice(i, end + 2);
      comments.push({
        kind: raw.startsWith("/**") ? "doc" : "block",
        line,
        endLine: line + (raw.match(/\n/g)?.length ?? 0),
        body: raw.slice(2, -2),
        raw,
        tsContext: opts.tsContext
      });
      blank(i, end + 2);
      line += raw.match(/\n/g)?.length ?? 0;
      i = end + 2;
      continue;
    }

    if (c === '"' || c === "'" || c === "`") {
      let k = i + 1;
      let closed = false;
      while (k < n) {
        if (src[k] === "\\") {
          k += 2;
          continue;
        }
        if (src[k] === "\n" && c !== "`") break;
        if (src[k] === c) {
          closed = true;
          break;
        }
        if (src[k] === "\n") line += 1;
        k += 1;
      }
      if (!closed) return { error: { line, message: `unterminated ${c} string` } };
      blank(i, k + 1);
      i = k + 1;
      lastSignificant = "str";
      continue;
    }

    if (c === "/" && regexCanStart(lastSignificant)) {
      let k = i + 1;
      let inClass = false;
      let closed = false;
      while (k < n) {
        const ch = src[k];
        if (ch === "\\") {
          k += 2;
          continue;
        }
        if (ch === "\n") break;
        if (ch === "[") inClass = true;
        else if (ch === "]") inClass = false;
        else if (ch === "/" && !inClass) {
          closed = true;
          break;
        }
        k += 1;
      }
      if (closed) {
        blank(i, k + 1);
        i = k + 1;
        lastSignificant = "str";
        continue;
      }
      // Not a regex after all: fall through and treat as a division operator.
    }

    if (c === "\n") line += 1;
    out[i] = c;
    if (!/\s/.test(c)) lastSignificant = c;
    i += 1;
  }

  return { comments, stripped: out.join(""), error: null };
}

function regexCanStart(prev) {
  if (prev === "" ) return true;
  if (prev === "str") return false;
  return "(,=:[!&|?{};+-*%~^<>".includes(prev);
}

// Merges consecutive // lines into one unit so a verified: date on the second
// line still belongs to the security-prefixed note on the first.
function mergeLineComments(comments) {
  const merged = [];
  for (const c of comments) {
    const prev = merged[merged.length - 1];
    if (c.kind === "line" && prev && prev.kind === "line" && prev.endLine + 1 === c.line) {
      prev.body += "\n" + c.body;
      prev.raw += "\n" + c.raw;
      prev.endLine = c.line;
      continue;
    }
    merged.push({ ...c, endLine: c.endLine ?? c.line });
  }
  return merged;
}

// Splits a .vue file into <script> blocks. Returns [{ text, startLine, ts }].
function vueScriptBlocks(src) {
  const blocks = [];
  const re = /<script\b([^>]*)>/gi;
  let m;
  while ((m = re.exec(src)) !== null) {
    const attrs = m[1] ?? "";
    const bodyStart = m.index + m[0].length;
    const close = src.toLowerCase().indexOf("</script>", bodyStart);
    if (close === -1) return { error: { line: lineAt(src, m.index), message: "unterminated <script> block" } };
    blocks.push({
      text: src.slice(bodyStart, close),
      startLine: lineAt(src, bodyStart),
      ts: /lang\s*=\s*["']?tsx?["']?/i.test(attrs)
    });
    re.lastIndex = close + 9;
  }
  return { blocks };
}

function lineAt(src, index) {
  let line = 1;
  for (let i = 0; i < index; i += 1) if (src[i] === "\n") line += 1;
  return line;
}

// ------------------------------------------------------- exported symbols

const EXPORT_RE =
  /^[ \t]*export[ \t]+(?:async[ \t]+)?(?:function\*?[ \t]+([A-Za-z_$][\w$]*)|(?:const|let|var)[ \t]+([A-Za-z_$][\w$]*)|class[ \t]+([A-Za-z_$][\w$]*))/;

function exportedSymbols(stripped, offsetLine) {
  const lines = stripped.split("\n");
  const found = [];
  for (let i = 0; i < lines.length; i += 1) {
    const m = EXPORT_RE.exec(lines[i]);
    if (!m) continue;
    const name = m[1] ?? m[2] ?? m[3];
    if (!name) continue;
    found.push({ name, line: offsetLine + i, index: i });
  }
  return found;
}

// Store actions: property functions inside actions: { ... } of a defineStore call.
function storeActions(stripped, offsetLine) {
  const found = [];
  const idx = stripped.indexOf("defineStore");
  if (idx === -1) return found;
  const actionsAt = stripped.indexOf("actions:", idx);
  if (actionsAt === -1) return found;
  const open = stripped.indexOf("{", actionsAt);
  if (open === -1) return found;
  let depth = 0;
  let end = -1;
  for (let k = open; k < stripped.length; k += 1) {
    if (stripped[k] === "{") depth += 1;
    else if (stripped[k] === "}") {
      depth -= 1;
      if (depth === 0) {
        end = k;
        break;
      }
    }
  }
  if (end === -1) return found;
  const region = stripped.slice(open, end);
  const base = lineAt(stripped, open);
  const lines = region.split("\n");
  for (let i = 0; i < lines.length; i += 1) {
    const m = /^[ \t]{2,}(?:async[ \t]+)?([A-Za-z_$][\w$]*)[ \t]*\(/.exec(lines[i]);
    if (m && !["if", "for", "while", "switch", "catch", "return"].includes(m[1])) {
      found.push({ name: m[1], line: offsetLine + base - 1 + i, index: base - 1 + i });
    }
  }
  return found;
}

// True when a /** */ block ends on the line above, ignoring blank lines.
function hasDocblockAbove(unitLines, absLine, docEndLines) {
  let probe = absLine - 1;
  while (probe >= 1 && (unitLines.get(probe) ?? "").trim() === "") probe -= 1;
  return docEndLines.has(probe);
}

// ------------------------------------------------------------ file walk

class RunError extends Error {}

function walk(dir, acc) {
  let entries;
  try {
    entries = fs.readdirSync(dir, { withFileTypes: true });
  } catch (err) {
    throw new RunError(`cannot read directory ${dir}: ${err.message}`);
  }
  for (const e of entries) {
    if (e.name.startsWith(".") && e.name !== ".") continue;
    const full = path.join(dir, e.name);
    if (e.isDirectory()) {
      if (SKIP_DIR.has(e.name)) continue;
      walk(full, acc);
    } else if (e.isFile() && SOURCE_EXT.has(path.extname(e.name))) {
      if (/\.d\.ts$/.test(e.name)) continue;
      acc.push(full);
    }
  }
  return acc;
}

// ------------------------------------------------------------- analysis

function analyseFile(file) {
  const src = fs.readFileSync(file, "utf8");
  const ext = path.extname(file);
  const units = [];

  if (ext === ".vue") {
    const res = vueScriptBlocks(src);
    if (res.error) throw new RunError(`${file}:${res.error.line}: ${res.error.message}`);
    for (const b of res.blocks) {
      const scan = scanSource(b.text, { startLine: b.startLine, tsContext: b.ts });
      if (scan.error) throw new RunError(`${file}:${scan.error.line}: ${scan.error.message}`);
      units.push({ ...scan, startLine: b.startLine, ts: b.ts, text: b.text });
    }
  } else {
    const ts = ext === ".ts" || ext === ".tsx";
    const scan = scanSource(src, { startLine: 1, tsContext: ts });
    if (scan.error) throw new RunError(`${file}:${scan.error.line}: ${scan.error.message}`);
    units.push({ ...scan, startLine: 1, ts, text: src });
  }
  return { file, src, units };
}

function importSpecifiers(units) {
  const specs = [];
  const re = /(?:\bfrom\s*|\bimport\s*\(\s*|\brequire\s*\(\s*|\bimport\s+)["']([^"']+)["']/g;
  for (const u of units) {
    const commentless = u.text.replace(/\/\*[\s\S]*?\*\//g, "").replace(/^[ \t]*\/\/.*$/gm, "");
    let m;
    while ((m = re.exec(commentless)) !== null) specs.push(m[1]);
  }
  return specs;
}

function resolveSpecifier(spec, fromFile, known) {
  if (!spec.startsWith(".")) return null;
  const base = path.resolve(path.dirname(fromFile), spec);
  for (const suffix of RESOLVE_ORDER) {
    const candidate = base + suffix;
    if (known.has(candidate)) return candidate;
  }
  return null;
}

function gitCommitDate(file, repoRoot) {
  try {
    const out = execFileSync("git", ["log", "-1", "--format=%cI", "--", file], {
      cwd: repoRoot,
      encoding: "utf8",
      stdio: ["ignore", "pipe", "ignore"]
    }).trim();
    return out === "" ? null : out;
  } catch {
    return null;
  }
}

function findRepoRoot(dir) {
  try {
    return execFileSync("git", ["rev-parse", "--show-toplevel"], {
      cwd: dir,
      encoding: "utf8",
      stdio: ["ignore", "pipe", "ignore"]
    }).trim();
  } catch {
    return null;
  }
}

// eslint-plugin-jsdoc with check-tag-names in typed mode owns ANN401; when the
// repo configures it we defer, when it does not we check it here.
function jsdocLintConfigured(repoRoot) {
  if (!repoRoot) return false;
  let pkg;
  try {
    pkg = JSON.parse(fs.readFileSync(path.join(repoRoot, "package.json"), "utf8"));
  } catch {
    return false;
  }
  const deps = { ...(pkg.dependencies ?? {}), ...(pkg.devDependencies ?? {}) };
  if (!Object.prototype.hasOwnProperty.call(deps, "eslint-plugin-jsdoc")) return false;
  for (const name of fs.readdirSync(repoRoot)) {
    if (!/^(eslint\.config\.|\.eslintrc)/.test(name)) continue;
    try {
      const text = fs.readFileSync(path.join(repoRoot, name), "utf8");
      if (text.includes("check-tag-names") && text.includes("typed")) return true;
    } catch {
      /* unreadable config is not a deferral */
    }
  }
  return false;
}

function checkFile(analysis, ctx) {
  const findings = [];
  const { file, units } = analysis;
  const rel = ctx.relative(file);
  const add = (line, rule, message) => findings.push({ file: rel, line, rule, message });
  const on = rule => ctx.rules === null || ctx.rules.has(rule);

  const lineText = new Map();
  analysis.src.split("\n").forEach((t, i) => lineText.set(i + 1, t));

  const docEndLines = new Set();

  for (const unit of units) {
    for (const c of mergeLineComments(unit.comments)) {
      if (c.kind === "doc") docEndLines.add(c.endLine);
      const body = c.body;
      // Line of a match inside the comment body, so a finding points at the
      // offending line and not at the first line of a merged comment run.
      const lineOf = index => c.line + (body.slice(0, index).match(/\n/g)?.length ?? 0);

      if (on("ANN601")) {
        const bad = /[^\x00-\x7F]/.exec(body);
        if (bad) {
          add(lineOf(bad.index), "ANN601", `non-ASCII character ${JSON.stringify(bad[0])} in comment; files are English`);
        }
      }

      if (on("ANN501")) {
        for (const re of COMMUNITY) {
          const m = re.exec(body);
          if (m) {
            add(lineOf(m.index), "ANN501", `community or issue-tracker citation "${m[0]}" inside a comment`);
            break;
          }
        }
      }

      if (on("ANN401") && unit.ts && !ctx.deferAnn401) {
        const m = /@(param|returns?)\s*\{/.exec(body);
        if (m) {
          add(lineOf(m.index), "ANN401", `@${m[1]} {Type} in a TypeScript context; the type checker owns the type`);
        }
      }

      // Each NOTE owns the text from its own prefix up to the next prefix, so a
      // verified: date can never be borrowed by the note above it.
      const noteRe = /(?:(\S+)[ \t]+)?NOTE:/g;
      const notes = [];
      let nm;
      while ((nm = noteRe.exec(body)) !== null) {
        const word = (nm[1] ?? "").replace(/^[*/\s]+/, "");
        notes.push({ index: nm.index, prefix: word === "" ? "NOTE:" : `${word} NOTE:` });
      }
      for (let k = 0; k < notes.length; k += 1) {
        const { index, prefix } = notes[k];
        const scope = body.slice(index, notes[k + 1]?.index ?? body.length);
        if (on("ANN201") && !PREFIXES.has(prefix)) {
          add(
            lineOf(index),
            "ANN201",
            `prefix "${prefix}" is outside the closed set (SSR|HYDRATION|STORE|AUTH|SECURITY NOTE:)`
          );
        }
        if (SECURITY_PREFIXES.has(prefix)) {
          const vm = /verified:(\d{4}-\d{2}-\d{2})/.exec(scope);
          if (!vm) {
            if (on("ANN301")) add(lineOf(index), "ANN301", `${prefix} without verified:<ISO-date>`);
          } else if (on("ANN302") && ctx.commitDate) {
            const commit = ctx.commitDate(file);
            if (commit && commit.slice(0, 10) > vm[1]) {
              add(
                lineOf(index),
                "ANN302",
                `${prefix} verified:${vm[1]} but the file last changed ${commit.slice(0, 10)}; re-verify or restate`
              );
            }
          }
        }
      }
    }
  }

  if (on("ANN101") && ctx.crossFile.has(file)) {
    for (const unit of units) {
      const symbols = [
        ...exportedSymbols(unit.stripped, unit.startLine),
        ...storeActions(unit.stripped, unit.startLine)
      ];
      for (const s of symbols) {
        if (!hasDocblockAbove(lineText, s.line, docEndLines)) {
          add(
            s.line,
            "ANN101",
            `exported "${s.name}" has no /** */ block; the module is imported by ${ctx.crossFile.get(file)} modules`
          );
        }
      }
    }
  }

  return findings;
}

// ---------------------------------------------------------------- driver

function run(dirs, opts) {
  const files = [];
  for (const d of dirs) {
    let stat;
    try {
      stat = fs.statSync(d);
    } catch {
      throw new RunError(`no such directory: ${d}`);
    }
    if (!stat.isDirectory()) throw new RunError(`not a directory: ${d}`);
    walk(path.resolve(d), files);
  }
  if (files.length === 0) throw new RunError(`no source files under: ${dirs.join(", ")}`);

  const repoRoot = findRepoRoot(path.resolve(dirs[0]));
  if (!repoRoot && opts.requireGit) {
    throw new RunError("--require-git: not a git work tree, ANN302 cannot be evaluated");
  }
  const relative = f => (repoRoot ? path.relative(repoRoot, f) : f);

  const analyses = [];
  for (const f of files) analyses.push(analyseFile(f));

  const known = new Set(files);
  const importers = new Map();
  for (const a of analyses) {
    const seen = new Set();
    for (const spec of importSpecifiers(a.units)) {
      const target = resolveSpecifier(spec, a.file, known);
      if (target && target !== a.file) seen.add(target);
    }
    for (const t of seen) importers.set(t, (importers.get(t) ?? 0) + 1);
  }
  const crossFile = new Map([...importers].filter(([, n]) => n >= 2));

  const dateCache = new Map();
  const commitDate = repoRoot
    ? f => {
        if (!dateCache.has(f)) dateCache.set(f, gitCommitDate(f, repoRoot));
        return dateCache.get(f);
      }
    : null;

  const deferAnn401 = jsdocLintConfigured(repoRoot);
  const ctx = {
    relative,
    crossFile,
    commitDate,
    deferAnn401,
    rules: opts.rules
  };

  const findings = [];
  for (const a of analyses) {
    findings.push(...checkFile(a, ctx));
    if (findings.length >= opts.maxFindings) break;
  }

  return { findings: findings.slice(0, opts.maxFindings), files, repoRoot, deferAnn401, commitDate };
}

// -------------------------------------------------------------- self-test

const FIXTURES = {
  "src/clean.ts": `import { helper } from "./helper";
/** Documented and clean. */
export function ok(): string {
  return helper();
}
`,
  "src/helper.ts": `/** Shared helper. */
export function helper(): string {
  return "x";
}
export const undocumented = () => 1;
`,
  "src/other.ts": `import { helper } from "./helper";
/** Second importer, so helper is cross-file surface. */
export const second = () => helper();
`,
  "src/notes.ts": `// CACHE NOTE: invented sixth prefix.
// AUTH NOTE: gateway strips X-User on ingress.
// SECURITY NOTE: bitmap is a UI hint. verified:2000-01-01
/** Doc. */
export const noted = 1;
`,
  "src/typed.ts": `/**
 * Redundant types.
 * @param {string} name - redundant.
 * @returns {number} redundant.
 */
export function typed(name: string): number {
  return name.length;
}
`,
  "src/cited.ts": `/** See https://stackoverflow.com/questions/1 for the workaround. */
export const cited = 1;
`,
  // The fixture body is written as escapes so that this file itself stays ASCII-only.
  "src/non-ascii.ts": `// ${"\u062a\u0648\u0636\u06cc\u062d"} \u2014 a non-English comment body.
/** Doc. */
export const nonAscii = 1;
`
};

const BROKEN = "/* unterminated block comment\nexport const x = 1;\n";

function selfTest() {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "check-annotations-selftest-"));
  const results = [];
  const record = (name, pass, detail) => results.push({ name, pass, detail });

  try {
    fs.mkdirSync(path.join(root, "src"));
    for (const [rel, text] of Object.entries(FIXTURES)) {
      fs.writeFileSync(path.join(root, rel), text, "utf8");
    }
    const git = args =>
      execFileSync("git", ["-c", "user.email=a@b.c", "-c", "user.name=selftest", ...args], {
        cwd: root,
        encoding: "utf8",
        stdio: ["ignore", "pipe", "ignore"]
      });
    let gitOk = true;
    try {
      git(["init", "-q"]);
      git(["add", "-A"]);
      git(["commit", "-qm", "fixtures"]);
    } catch {
      gitOk = false;
    }

    const res = run([path.join(root, "src")], { rules: null, maxFindings: 500, requireGit: false });
    const by = rule => res.findings.filter(f => f.rule === rule);
    const at = (rule, fileFragment) => by(rule).some(f => f.file.includes(fileFragment));

    record("ANN201 flags an invented sixth prefix", at("ANN201", "notes.ts"), by("ANN201"));
    record("ANN201 accepts the five closed prefixes", by("ANN201").length === 1, by("ANN201"));
    record("ANN301 flags AUTH NOTE: without verified:", at("ANN301", "notes.ts"), by("ANN301"));
    record(
      gitOk ? "ANN302 flags a verified: date older than the last commit" : "ANN302 skipped (no git)",
      gitOk ? at("ANN302", "notes.ts") : by("ANN302").length === 0,
      by("ANN302")
    );
    record("ANN401 flags @param {Type} in a .ts file", at("ANN401", "typed.ts"), by("ANN401"));
    record("ANN501 flags a Stack Overflow URL in a comment", at("ANN501", "cited.ts"), by("ANN501"));
    record("ANN601 flags a non-ASCII comment body", at("ANN601", "non-ascii.ts"), by("ANN601"));
    record(
      "ANN101 flags an undocumented export in a 2+-importer module",
      at("ANN101", "helper.ts"),
      by("ANN101")
    );
    record(
      "ANN101 stays silent on a single-importer module",
      !at("ANN101", "clean.ts") && !at("ANN101", "other.ts"),
      by("ANN101")
    );

    // Exit-code 2 fixture: an unparsed file must never be reported as clean.
    const badDir = fs.mkdtempSync(path.join(os.tmpdir(), "check-annotations-broken-"));
    fs.writeFileSync(path.join(badDir, "broken.ts"), BROKEN, "utf8");
    let threw = false;
    try {
      run([badDir], { rules: null, maxFindings: 500, requireGit: false });
    } catch (err) {
      threw = err instanceof RunError;
    }
    record("an unterminated comment raises could-not-run, not clean", threw, threw);
    fs.rmSync(badDir, { recursive: true, force: true });
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }

  let failed = 0;
  for (const r of results) {
    if (!r.pass) failed += 1;
    process.stdout.write(`${r.pass ? "PASS" : "FAIL"}  ${r.name}\n`);
    if (!r.pass) process.stdout.write(`      got: ${JSON.stringify(r.detail)}\n`);
  }
  process.stdout.write(`${results.length - failed}/${results.length} self-test cases passed\n`);
  return failed === 0 ? 0 : 1;
}

// ------------------------------------------------------------------ main

function main(argv) {
  const dirs = [];
  const opts = { rules: null, maxFindings: 500, json: false, requireGit: false };
  for (const arg of argv) {
    if (arg === "--help" || arg === "-h") {
      process.stdout.write(HELP);
      return 0;
    } else if (arg === "--self-test") {
      return selfTest();
    } else if (arg === "--json") opts.json = true;
    else if (arg === "--require-git") opts.requireGit = true;
    else if (arg.startsWith("--rules=")) opts.rules = new Set(arg.slice(8).split(",").map(s => s.trim()));
    else if (arg.startsWith("--max-findings=")) opts.maxFindings = Number(arg.slice(15)) || 500;
    else if (arg.startsWith("-")) {
      process.stderr.write(`unknown option: ${arg}\n${HELP}`);
      return 2;
    } else dirs.push(arg);
  }
  if (dirs.length === 0) {
    process.stderr.write(`no directory given\n${HELP}`);
    return 2;
  }

  let res;
  try {
    res = run(dirs, opts);
  } catch (err) {
    process.stderr.write(`check-annotations: could not run: ${err.message}\n`);
    return 2;
  }

  if (res.deferAnn401) {
    process.stderr.write("note: eslint-plugin-jsdoc check-tag-names typed is configured; ANN401 deferred to it\n");
  } else {
    process.stderr.write("note: no eslint-plugin-jsdoc check-tag-names typed config found; ANN401 checked here\n");
  }
  if (!res.commitDate) {
    process.stderr.write("note: no git work tree; ANN302 staleness not evaluated (use --require-git to make this fatal)\n");
  }

  if (opts.json) {
    process.stdout.write(JSON.stringify({ files: res.files.length, findings: res.findings }, null, 2) + "\n");
  } else {
    for (const f of res.findings) process.stdout.write(`${f.file}:${f.line}: ${f.rule} ${f.message}\n`);
  }
  process.stderr.write(`checked ${res.files.length} files, ${res.findings.length} findings\n`);
  return res.findings.length === 0 ? 0 : 1;
}

process.exit(main(process.argv.slice(2)));
