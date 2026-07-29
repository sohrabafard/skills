#!/usr/bin/env node
// verify-package-entrypoints.mjs — assert the export surface, peer contract and
// asset side-effect declaration of every workspace package.
// Owned by the alaa-mono-package skill.
//
// Exit codes are part of the contract; see printHelp().

import { readFileSync, readdirSync, existsSync, realpathSync, statSync, mkdtempSync, mkdirSync, writeFileSync, rmSync } from "node:fs";
import { join, resolve, dirname, sep } from "node:path";
import { pathToFileURL } from "node:url";
import { tmpdir } from "node:os";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

// On Windows, new URL(import.meta.url).pathname is "/D:/...", which Node cannot
// spawn as a filesystem path. fileURLToPath is the only correct conversion.
const SELF_PATH = fileURLToPath(import.meta.url);

const EXIT_OK = 0;
const EXIT_VIOLATION = 1;
const EXIT_CANNOT_RUN = 2;
const EXIT_USAGE = 3;

const SHARED_RUNTIMES = ["vue", "quasar", "vue-router", "pinia"];

const HELP = `verify-package-entrypoints.mjs — workspace export-surface gate

USAGE
  node verify-package-entrypoints.mjs [workspace-root] [options]
  node verify-package-entrypoints.mjs --self-test
  node verify-package-entrypoints.mjs --help

ARGUMENTS
  [workspace-root]       Repository root holding the workspace manifest. Default: cwd.

OPTIONS
  --package <dir>        Check one package directory instead of every member.
  --shared <a,b,c>       Names that must stay peers and resolve once.
                         Default: ${SHARED_RUNTIMES.join(",")}
  --skip <ids>           Comma-separated assertion ids to skip, e.g. --skip E4
  --no-load              Do not spawn subprocess imports (skips E4). E4 spawns one
                         Node process per package and is the slow assertion; use this
                         when a fast manifest-only pass is wanted.
  --load-timeout <ms>    Per-package E4 timeout. Default: 15000. A package whose entry
                         does not let the process exit within it fails E4.
  --json                 Emit findings as JSON on stdout.
  --self-test            Run built-in fixtures and exit. Writes only under the OS temp dir.
  --help, -h             Print this text.

ASSERTIONS
  E1  Every target in every "exports" entry exists on disk.
  E2  "types" is the first key in every conditions object. Condition matching is
      first-match and order-sensitive, so a "types" key placed after "import" is
      unreachable and the consumer silently sees "any".
  E3  "main" and "module", if present beside "exports", point at the same file the
      "." default condition points at.
  E4  The package's default entry loads in a subprocess, not merely resolves.
  E5  Shared runtimes are declared in peerDependencies, are absent from
      dependencies, and resolve to exactly one real path across the workspace.
  E6  A package that emits CSS does not declare "sideEffects": false.
  E7  Every internal workspace specifier matches the manager detected from the
      lockfile.

REPORTING
  A gate that could not run is printed as "not run" with its reason and is never
  counted as a pass. E4 reports "not run" when a declared peer is not installed,
  because a missing peer is an environment fact and not an export-surface defect.

EXIT CODES
  0  Every applicable assertion passed.
  1  At least one assertion failed. Each failure names package, subpath and condition.
  2  Could not run: the workspace root, the manifest, or a package's build output is
     absent or unreadable. Deliberately distinct from 0 and from 1 so an unbuilt
     package reads differently from a contract defect, and so a pipeline can never
     mistake an unparsed workspace for a passing one.
  3  Invocation error: unknown option, missing argument.
`;

// ---------------------------------------------------------------- arg parsing

function parseArgs(argv) {
  const o = { root: null, package: null, shared: SHARED_RUNTIMES.slice(), skip: new Set(), load: true, loadTimeoutMs: 15000, json: false, selfTest: false, help: false };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    const need = (n) => { const v = argv[++i]; if (v === undefined) throw { usage: `${n} requires a value` }; return v; };
    if (a === "--help" || a === "-h") o.help = true;
    else if (a === "--self-test") o.selfTest = true;
    else if (a === "--json") o.json = true;
    else if (a === "--no-load") o.load = false;
    else if (a === "--load-timeout") { const v = Number(need("--load-timeout")); if (!Number.isFinite(v) || v <= 0) throw { usage: "--load-timeout must be a positive number of milliseconds" }; o.loadTimeoutMs = v; }
    else if (a === "--package") o.package = need("--package");
    else if (a === "--shared") o.shared = need("--shared").split(",").map((s) => s.trim()).filter(Boolean);
    else if (a === "--skip") need("--skip").split(",").map((s) => s.trim().toUpperCase()).filter(Boolean).forEach((s) => o.skip.add(s));
    else if (a.startsWith("-")) throw { usage: `unknown option ${a}` };
    else if (o.root === null) o.root = a;
    else throw { usage: `unexpected argument ${a}` };
  }
  return o;
}

// ---------------------------------------------------------------- workspace

function detectManager(root) {
  if (existsSync(join(root, "pnpm-lock.yaml"))) return "pnpm";
  if (existsSync(join(root, ".yarnrc.yml"))) return "yarn-berry";
  if (existsSync(join(root, "yarn.lock"))) return "yarn-classic";
  if (existsSync(join(root, "package-lock.json"))) return "npm";
  return null;
}

function readJson(p) { return JSON.parse(readFileSync(p, "utf8")); }

function workspaceGlobs(root) {
  const ws = join(root, "pnpm-workspace.yaml");
  if (existsSync(ws)) {
    const globs = [];
    for (const line of readFileSync(ws, "utf8").split(/\r?\n/)) {
      const m = /^\s*-\s*["']?([^"'#]+?)["']?\s*$/.exec(line);
      if (m && m[1].includes("*")) globs.push(m[1].trim());
    }
    if (globs.length) return globs;
  }
  const pkg = join(root, "package.json");
  if (existsSync(pkg)) {
    const w = readJson(pkg).workspaces;
    const arr = Array.isArray(w) ? w : w && Array.isArray(w.packages) ? w.packages : [];
    if (arr.length) return arr;
  }
  return ["packages/*"];
}

function memberDirs(root) {
  const dirs = new Set();
  for (const g of workspaceGlobs(root)) {
    const base = g.replace(/\/\*+$/, "");
    const abs = join(root, base);
    if (!existsSync(abs)) continue;
    if (g.includes("*")) {
      for (const e of readdirSync(abs, { withFileTypes: true })) {
        if (e.isDirectory() && existsSync(join(abs, e.name, "package.json"))) dirs.add(join(abs, e.name));
      }
    } else if (existsSync(join(abs, "package.json"))) dirs.add(abs);
  }
  return [...dirs].sort();
}

// ---------------------------------------------------------------- helpers

function exportTargets(exportsField) {
  // -> [{ subpath, condition, target, conditionKeys }]
  const out = [];
  const visit = (subpath, value, conditionPath, container) => {
    if (typeof value === "string") { out.push({ subpath, condition: conditionPath.join(">") || "(unconditional)", target: value, conditionKeys: container }); return; }
    if (value === null) return;
    if (typeof value !== "object") return;
    const keys = Object.keys(value);
    for (const k of keys) visit(subpath, value[k], [...conditionPath, k], keys);
  };
  if (typeof exportsField === "string") { out.push({ subpath: ".", condition: "(unconditional)", target: exportsField, conditionKeys: null }); return out; }
  if (!exportsField || typeof exportsField !== "object") return out;
  const top = Object.keys(exportsField);
  const looksLikeSubpaths = top.some((k) => k === "." || k.startsWith("./"));
  if (looksLikeSubpaths) for (const k of top) visit(k, exportsField[k], [], null);
  else visit(".", exportsField, [], top);
  return out;
}

function conditionObjects(exportsField, acc = []) {
  if (!exportsField || typeof exportsField !== "object") return acc;
  const keys = Object.keys(exportsField);
  const isSubpathMap = keys.some((k) => k === "." || k.startsWith("./"));
  if (!isSubpathMap) acc.push(keys);
  for (const k of keys) if (exportsField[k] && typeof exportsField[k] === "object") conditionObjects(exportsField[k], acc);
  return acc;
}

function defaultEntryTarget(exportsField) {
  const t = exportTargets(exportsField).filter((e) => e.subpath === ".");
  const pick = t.find((e) => /(^|>)default$/.test(e.condition)) || t.find((e) => /(^|>)import$/.test(e.condition)) || t[0];
  return pick ? pick.target : null;
}

function walkFiles(dir, acc = []) {
  if (!existsSync(dir)) return acc;
  for (const e of readdirSync(dir, { withFileTypes: true })) {
    const p = join(dir, e.name);
    if (e.isDirectory()) walkFiles(p, acc); else if (e.isFile()) acc.push(p);
  }
  return acc;
}

function resolveFromDir(startDir, name, stopAt) {
  let d = startDir;
  for (;;) {
    const cand = join(d, "node_modules", name);
    if (existsSync(cand)) { try { return realpathSync(cand); } catch { return cand; } }
    if (d === stopAt) return null;
    const parent = dirname(d);
    if (parent === d) return null;
    d = parent;
  }
}

// ---------------------------------------------------------------- main check

function run(opts) {
  const findings = [];
  const notRun = [];
  const add = (id, pkg, message) => findings.push({ id, package: pkg, message });
  const skipped = (id, pkg, reason) => notRun.push({ id, package: pkg, reason });

  const root = resolve(opts.root || process.cwd());
  if (!existsSync(root) || !statSync(root).isDirectory()) return { code: EXIT_CANNOT_RUN, findings, notRun, note: `workspace root not found: ${root}` };
  if (!existsSync(join(root, "package.json"))) return { code: EXIT_CANNOT_RUN, findings, notRun, note: `no package.json at workspace root: ${root}` };

  const manager = detectManager(root);
  if (!manager) return { code: EXIT_CANNOT_RUN, findings, notRun, note: `no lockfile at ${root}; the manager cannot be detected and the specifier gate cannot run` };

  const dirs = opts.package ? [resolve(opts.package)] : memberDirs(root);
  if (dirs.length === 0) return { code: EXIT_CANNOT_RUN, findings, notRun, note: `no workspace members found under ${root}` };

  const manifests = new Map();
  for (const d of dirs) {
    const p = join(d, "package.json");
    if (!existsSync(p)) return { code: EXIT_CANNOT_RUN, findings, notRun, note: `no package.json in ${d}` };
    try { manifests.set(d, readJson(p)); } catch (e) { return { code: EXIT_CANNOT_RUN, findings, notRun, note: `unparseable manifest ${p}: ${e.message}` }; }
  }
  const memberNames = new Set([...manifests.values()].map((m) => m.name).filter(Boolean));

  const unbuilt = [];

  for (const dir of dirs) {
    const m = manifests.get(dir);
    const name = m.name || dir.split(sep).pop();
    const targets = exportTargets(m.exports);

    // E1 — targets exist
    if (!opts.skip.has("E1")) {
      let sawMissingDist = false;
      for (const t of targets) {
        if (typeof t.target !== "string" || !t.target.startsWith(".")) continue;
        const abs = resolve(dir, t.target);
        if (!existsSync(abs)) {
          if (t.target.startsWith("./dist/") && !existsSync(join(dir, "dist"))) sawMissingDist = true;
          else add("E1", name, `exports["${t.subpath}"] condition ${t.condition} points at ${t.target}, which does not exist`);
        }
      }
      if (sawMissingDist) unbuilt.push(name);
    }

    // E2 — types first
    if (!opts.skip.has("E2")) {
      for (const keys of conditionObjects(m.exports)) {
        const i = keys.indexOf("types");
        if (i > 0) add("E2", name, `conditions object [${keys.join(", ")}] places "types" at position ${i}; first-match ordering makes it unreachable and the consumer sees "any"`);
        const d = keys.indexOf("default");
        if (d !== -1 && d !== keys.length - 1) add("E2", name, `conditions object [${keys.join(", ")}] places "default" before ${keys.slice(d + 1).join(", ")}; keys after "default" are dead`);
      }
    }

    // E3 — main/module agree with the default entry
    if (!opts.skip.has("E3") && m.exports) {
      const def = defaultEntryTarget(m.exports);
      for (const field of ["main", "module"]) {
        if (typeof m[field] !== "string" || !def) continue;
        if (resolve(dir, m[field]) !== resolve(dir, def)) {
          add("E3", name, `"${field}" is ${m[field]} while the "." default condition is ${def}; a consumer that ignores "exports" would load a different file`);
        }
      }
    }

    // E6 — CSS plus sideEffects:false
    if (!opts.skip.has("E6")) {
      const cssInExports = targets.some((t) => typeof t.target === "string" && /\.(css|scss|sass)$/.test(t.target));
      const cssInDist = walkFiles(join(dir, "dist")).some((f) => /\.(css|scss|sass)$/.test(f));
      const declaresStyle = typeof m.style === "string";
      if ((cssInExports || cssInDist || declaresStyle) && m.sideEffects === false) {
        add("E6", name, `emits CSS and declares "sideEffects": false; the consumer's bundler will tree-shake the stylesheet away and components render unstyled`);
      }
    }

    // E7 — internal specifiers match the detected manager
    if (!opts.skip.has("E7")) {
      for (const section of ["dependencies", "devDependencies", "peerDependencies", "optionalDependencies"]) {
        for (const [dep, spec] of Object.entries(m[section] || {})) {
          if (!memberNames.has(dep) || typeof spec !== "string") continue;
          const ok =
            manager === "pnpm" || manager === "yarn-berry"
              ? spec.startsWith("workspace:")
              : !spec.startsWith("workspace:");
          if (!ok) add("E7", name, `${section}["${dep}"] is "${spec}", which is not the ${manager} internal specifier form`);
          if ((manager === "pnpm" || manager === "yarn-berry") && (spec.startsWith("link:") || spec.startsWith("file:"))) {
            add("E7", name, `${section}["${dep}"] is "${spec}"; a link:/file: specifier carried into a ${manager} workspace bypasses the workspace graph`);
          }
        }
      }
    }

    // E5 (manifest half) — shared runtimes are peers, not dependencies
    if (!opts.skip.has("E5")) {
      for (const s of opts.shared) {
        if (m.dependencies && m.dependencies[s]) {
          add("E5", name, `declares shared runtime "${s}" in dependencies; it must be a peerDependency so the application provides the single instance`);
        }
      }
    }

    // E4 — the default entry loads
    if (!opts.skip.has("E4") && opts.load) {
      const def = m.exports ? defaultEntryTarget(m.exports) : typeof m.main === "string" ? m.main : null;
      if (!def) skipped("E4", name, "no default entry declared");
      else {
        const abs = resolve(dir, def);
        if (!existsSync(abs)) skipped("E4", name, `default entry ${def} is absent; E1 already reports it`);
        else {
          const r = spawnSync(process.execPath, ["--input-type=module", "-e", `await import(${JSON.stringify(pathToFileURL(abs).href)})`], { cwd: dir, encoding: "utf8", timeout: opts.loadTimeoutMs });
          if (r.signal || (r.error && r.error.code === "ETIMEDOUT")) {
            add("E4", name, `default entry ${def} imports without the process exiting within ${opts.loadTimeoutMs} ms; a module-scope side effect is holding the event loop open, which contradicts any "sideEffects": false declaration and runs on every consumer import`);
          } else if (r.status !== 0) {
            const err = (r.stderr || "").trim();
            const missing = /Cannot find package '([^']+)'|Cannot find module '([^']+)'/.exec(err);
            const peer = missing && (missing[1] || missing[2]);
            if (peer && m.peerDependencies && m.peerDependencies[peer]) skipped("E4", name, `declared peer "${peer}" is not installed here, so evaluation was not attempted`);
            else add("E4", name, `default entry ${def} resolves but does not load: ${err.split("\n").slice(0, 3).join(" | ")}`);
          }
        }
      }
    }
  }

  // E5 (workspace half) — one real path per shared runtime
  if (!opts.skip.has("E5")) {
    for (const s of opts.shared) {
      const paths = new Map();
      for (const d of [root, ...dirs]) {
        const p = resolveFromDir(d, s, root);
        if (p) { if (!paths.has(p)) paths.set(p, []); paths.get(p).push(d === root ? "<root>" : d.split(sep).pop()); }
      }
      if (paths.size > 1) {
        const detail = [...paths.entries()].map(([p, who]) => `${p} (from ${who.join(", ")})`).join(" AND ");
        add("E5", "<workspace>", `shared runtime "${s}" resolves to ${paths.size} distinct real paths: ${detail}`);
      }
      if (paths.size === 0) skipped("E5", "<workspace>", `shared runtime "${s}" is not installed anywhere; the single-realpath assertion was not evaluated`);
    }
  }

  if (unbuilt.length) {
    return { code: EXIT_CANNOT_RUN, findings, notRun, manager, packageCount: dirs.length, note: `unbuilt package(s), dist/ absent: ${[...new Set(unbuilt)].join(", ")}. Build the graph first; contract findings from an unbuilt package are not reliable.` };
  }
  return { code: findings.length ? EXIT_VIOLATION : EXIT_OK, findings, notRun, manager, packageCount: dirs.length };
}

// ---------------------------------------------------------------- self-test

function mkPkg(root, name, manifest, files = {}) {
  const dir = join(root, "packages", name);
  mkdirSync(join(dir, "dist"), { recursive: true });
  writeFileSync(join(dir, "package.json"), JSON.stringify({ name: `@fx/${name}`, version: "1.0.0", private: true, type: "module", ...manifest }, null, 2));
  for (const [rel, body] of Object.entries(files)) {
    mkdirSync(dirname(join(dir, rel)), { recursive: true });
    writeFileSync(join(dir, rel), body);
  }
  return dir;
}

function mkWorkspace(base, label) {
  const root = join(base, label);
  mkdirSync(root, { recursive: true });
  writeFileSync(join(root, "package.json"), JSON.stringify({ name: "fx-root", private: true }, null, 2));
  writeFileSync(join(root, "pnpm-lock.yaml"), "lockfileVersion: '9.0'\n");
  writeFileSync(join(root, "pnpm-workspace.yaml"), 'packages:\n  - "packages/*"\n');
  return root;
}

const GOOD_EXPORTS = { exports: { ".": { types: "./dist/index.d.ts", import: "./dist/index.mjs", default: "./dist/index.mjs" } } };
const GOOD_FILES = { "dist/index.mjs": "export const ok = 1;\n", "dist/index.d.ts": "export declare const ok: number;\n" };

function selfTest() {
  const base = mkdtempSync(join(tmpdir(), "alaa-exports-selftest-"));
  const self = SELF_PATH;
  const cases = [];
  const check = (label, root, expectCode, expectIds, extra = []) => {
    const r = spawnSync(process.execPath, [self, root, "--json", ...extra], { encoding: "utf8" });
    let ids = [];
    try { ids = [...new Set(JSON.parse(r.stdout).findings.map((f) => f.id))].sort(); } catch { ids = ["<unparseable>"]; }
    const ok = r.status === expectCode && JSON.stringify(ids) === JSON.stringify(expectIds.slice().sort());
    cases.push({ label, ok, gotCode: r.status, wantCode: expectCode, gotIds: ids, wantIds: expectIds.slice().sort() });
  };

  let root = mkWorkspace(base, "clean");
  mkPkg(root, "a", { sideEffects: false, ...GOOD_EXPORTS }, GOOD_FILES);
  check("clean workspace exits 0", root, EXIT_OK, []);

  check("absent root exits 2, not 0", join(base, "nope"), EXIT_CANNOT_RUN, []);

  root = mkWorkspace(base, "nolock"); rmSync(join(root, "pnpm-lock.yaml"));
  mkPkg(root, "a", GOOD_EXPORTS, GOOD_FILES);
  check("no lockfile exits 2", root, EXIT_CANNOT_RUN, []);

  root = mkWorkspace(base, "unbuilt");
  mkPkg(root, "a", GOOD_EXPORTS, {});
  rmSync(join(root, "packages", "a", "dist"), { recursive: true, force: true });
  check("unbuilt package exits 2, not 1", root, EXIT_CANNOT_RUN, []);

  root = mkWorkspace(base, "missing-target");
  mkPkg(root, "a", GOOD_EXPORTS, { "dist/index.mjs": "export const ok = 1;\n" });
  check("exports target missing on disk fails E1", root, EXIT_VIOLATION, ["E1"]);

  root = mkWorkspace(base, "types-late");
  mkPkg(root, "a", { exports: { ".": { import: "./dist/index.mjs", types: "./dist/index.d.ts", default: "./dist/index.mjs" } } }, GOOD_FILES);
  check("types after import fails E2", root, EXIT_VIOLATION, ["E2"]);

  root = mkWorkspace(base, "default-early");
  mkPkg(root, "a", { exports: { ".": { types: "./dist/index.d.ts", default: "./dist/index.mjs", import: "./dist/index.mjs" } } }, GOOD_FILES);
  check("default before import fails E2", root, EXIT_VIOLATION, ["E2"]);

  root = mkWorkspace(base, "main-drift");
  mkPkg(root, "a", { main: "./dist/legacy.mjs", ...GOOD_EXPORTS }, { ...GOOD_FILES, "dist/legacy.mjs": "export const ok = 0;\n" });
  check("main pointing elsewhere fails E3", root, EXIT_VIOLATION, ["E3"]);

  root = mkWorkspace(base, "css-shaken");
  mkPkg(root, "a", { sideEffects: false, exports: { ".": { types: "./dist/index.d.ts", import: "./dist/index.mjs", default: "./dist/index.mjs" }, "./style.css": "./dist/style.css" } }, { ...GOOD_FILES, "dist/style.css": ".a{color:red}\n" });
  check("CSS plus sideEffects:false fails E6", root, EXIT_VIOLATION, ["E6"]);

  root = mkWorkspace(base, "link-spec");
  mkPkg(root, "a", GOOD_EXPORTS, GOOD_FILES);
  mkPkg(root, "b", { dependencies: { "@fx/a": "link:../a" }, ...GOOD_EXPORTS }, GOOD_FILES);
  check("link: specifier in a pnpm workspace fails E7", root, EXIT_VIOLATION, ["E7"]);

  root = mkWorkspace(base, "peer-as-dep");
  mkPkg(root, "a", { dependencies: { vue: "^3.5.0" }, ...GOOD_EXPORTS }, GOOD_FILES);
  check("shared runtime in dependencies fails E5", root, EXIT_VIOLATION, ["E5"]);

  root = mkWorkspace(base, "two-copies");
  const pa = mkPkg(root, "a", { peerDependencies: { vue: "^3" }, ...GOOD_EXPORTS }, GOOD_FILES);
  mkdirSync(join(root, "node_modules", "vue"), { recursive: true });
  writeFileSync(join(root, "node_modules", "vue", "package.json"), '{"name":"vue","version":"3.5.0"}');
  mkdirSync(join(pa, "node_modules", "vue"), { recursive: true });
  writeFileSync(join(pa, "node_modules", "vue", "package.json"), '{"name":"vue","version":"3.4.0"}');
  check("one peer at two real paths fails E5", root, EXIT_VIOLATION, ["E5"]);

  root = mkWorkspace(base, "throws");
  mkPkg(root, "a", GOOD_EXPORTS, { "dist/index.d.ts": "export declare const ok: number;\n", "dist/index.mjs": "throw new Error('boom at module scope');\n" });
  check("entry that resolves but throws fails E4", root, EXIT_VIOLATION, ["E4"]);

  root = mkWorkspace(base, "hangs");
  mkPkg(root, "a", GOOD_EXPORTS, { "dist/index.d.ts": "export declare const ok: number;\n", "dist/index.mjs": "setInterval(() => {}, 1000);\nexport const ok = 1;\n" });
  check("entry that never lets the process exit fails E4", root, EXIT_VIOLATION, ["E4"], ["--load-timeout", "2500"]);

  root = mkWorkspace(base, "peer-absent");
  mkPkg(root, "a", { peerDependencies: { quasar: "^2" }, ...GOOD_EXPORTS }, { "dist/index.d.ts": "export declare const ok: number;\n", "dist/index.mjs": "import 'quasar';\nexport const ok = 1;\n" });
  check("uninstalled declared peer is not-run, not a failure", root, EXIT_OK, []);

  let failed = 0;
  for (const c of cases) {
    if (!c.ok) failed++;
    console.log(`${c.ok ? "PASS" : "FAIL"}  ${c.label}` + (c.ok ? "" : `\n        want exit ${c.wantCode} ids ${JSON.stringify(c.wantIds)}; got exit ${c.gotCode} ids ${JSON.stringify(c.gotIds)}`));
  }
  rmSync(base, { recursive: true, force: true });
  console.log(`\n${cases.length - failed}/${cases.length} self-test cases passed (fixtures under ${base}, now removed)`);
  return failed ? EXIT_VIOLATION : EXIT_OK;
}

// ---------------------------------------------------------------- entry point

function main() {
  let opts;
  try { opts = parseArgs(process.argv.slice(2)); }
  catch (e) { console.error(`error: ${e.usage || e.message}\n`); console.error(HELP); process.exit(EXIT_USAGE); }

  if (opts.help) { console.log(HELP); process.exit(EXIT_OK); }
  if (opts.selfTest) process.exit(selfTest());

  const res = run(opts);
  if (opts.json) console.log(JSON.stringify({ exitCode: res.code, note: res.note ?? null, findings: res.findings, notRun: res.notRun }, null, 2));
  else {
    if (res.note) console.error(`could-not-run: ${res.note}`);
    for (const f of res.findings) console.error(`${f.id}  ${f.package}: ${f.message}`);
    for (const n of res.notRun) console.error(`${n.id}  ${n.package}: not run: ${n.reason}`);
    if (res.code === EXIT_OK) console.log(`export surface: OK (${res.packageCount} package(s), ${res.manager})`);
    else if (res.code === EXIT_VIOLATION) console.error(`\nexport surface: ${res.findings.length} failure(s)`);
  }
  process.exit(res.code);
}

main();
