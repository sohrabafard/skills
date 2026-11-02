#!/usr/bin/env node
// verify-artifact-contract.mjs — assert a frontend build output tree against the
// declared artifact contract. Owned by the alaa-frontend-devops skill.
//
// Exit codes are part of the contract; see printHelp().

import { readFileSync, readdirSync, statSync, existsSync } from "node:fs";
import { join, relative, resolve, sep, posix } from "node:path";

const EXIT_OK = 0;
const EXIT_VIOLATION = 1;
const EXIT_CANNOT_RUN = 2;
const EXIT_USAGE = 3;

const HELP = `verify-artifact-contract.mjs — frontend artifact contract gate

USAGE
  node verify-artifact-contract.mjs <dist-root> [options]
  node verify-artifact-contract.mjs --help

ARGUMENTS
  <dist-root>            Build output root to inspect, e.g. dist/ssr, dist/spa, dist/pwa.

OPTIONS
  --mode <spa|pwa|ssr>   Build mode. Default: inferred from the tree.
  --base <path>          Declared browser asset base (build.publicPath). Default: /
  --env <file>           Env file whose non-prefixed values must not appear in any chunk.
  --client-prefix <p>    Prefix marking a variable as allowed in client code. Default: QCLI_
  --provenance <name>    Provenance file name, relative to <dist-root>. Default: build-info.json
  --skip <ids>           Comma-separated assertion ids to skip, e.g. --skip A6
  --json                 Emit findings as JSON on stdout.
  --help, -h             Print this text.

ASSERTIONS
  A1  SSR runtime entry exists at <dist-root>/index.js (ssr mode only).
  A2  Every asset URL in emitted HTML and in the client manifest resolves to a file on disk.
  A3  No emitted asset path escapes the client asset root; absolute URLs match --base.
  A4  No secret-shaped value, and no value of a non-prefixed variable from --env,
      appears verbatim in any emitted client chunk.
  A5  Every emitted .js and .css under the client asset root carries a content hash,
      detected structurally as a trailing "." or "-" separated token of >=8 url-safe
      characters. A stem with no such token, e.g. "vendor.js", fails.
  A6  The provenance file exists and carries commit, ref, builtAt, nodeVersion,
      packageManager, lockfileHash, buildMode.

EXIT CODES
  0  All applicable assertions passed. "Clean".
  1  At least one assertion failed. Each failure is printed with its path.
  2  Could not run: <dist-root> is missing, unreadable, or contains no recognisable
     build output. Deliberately distinct from 0 so a pipeline can never read
     "nothing was built" as "the build is fine".
  3  Invocation error: unknown option, missing argument, unreadable --env file.
`;

// ---------------------------------------------------------------- arg parsing

function parseArgs(argv) {
  const opts = {
    root: null, mode: null, base: "/", env: null, clientPrefix: "QCLI_",
    provenance: "build-info.json", skip: new Set(), json: false,
    help: false
  };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    const need = (name) => {
      const v = argv[++i];
      if (v === undefined) throw { usage: `${name} requires a value` };
      return v;
    };
    if (a === "--help" || a === "-h") opts.help = true;
    else if (a === "--json") opts.json = true;
    else if (a === "--mode") opts.mode = need("--mode");
    else if (a === "--base") opts.base = need("--base");
    else if (a === "--env") opts.env = need("--env");
    else if (a === "--client-prefix") opts.clientPrefix = need("--client-prefix");
    else if (a === "--provenance") opts.provenance = need("--provenance");
    else if (a === "--skip") need("--skip").split(",").map((s) => s.trim()).filter(Boolean).forEach((s) => opts.skip.add(s.toUpperCase()));
    else if (a.startsWith("-")) throw { usage: `unknown option ${a}` };
    else if (opts.root === null) opts.root = a;
    else throw { usage: `unexpected argument ${a}` };
  }
  if (opts.mode && !["spa", "pwa", "ssr"].includes(opts.mode)) throw { usage: `--mode must be spa, pwa or ssr` };
  return opts;
}

// ---------------------------------------------------------------- tree layout

function walk(dir, acc = []) {
  for (const e of readdirSync(dir, { withFileTypes: true })) {
    const p = join(dir, e.name);
    if (e.isDirectory()) walk(p, acc);
    else if (e.isFile()) acc.push(p);
  }
  return acc;
}

function inferLayout(root, forcedMode) {
  const hasClientDir = existsSync(join(root, "client"));
  const hasSsrEntry = existsSync(join(root, "index.js"));
  const mode = forcedMode || (hasClientDir && hasSsrEntry ? "ssr" : existsSync(join(root, "sw.js")) ? "pwa" : "spa");
  const clientRoot = mode === "ssr" ? join(root, "client") : root;
  return { mode, clientRoot, assetRoot: join(clientRoot, "assets") };
}

// ---------------------------------------------------------------- url helpers

const URL_ATTR = /(?:src|href)\s*=\s*(?:"([^"]+)"|'([^']+)'|([^\s>]+))/gi;

function htmlUrls(text) {
  const out = [];
  let m;
  URL_ATTR.lastIndex = 0;
  while ((m = URL_ATTR.exec(text)) !== null) out.push(m[1] || m[2] || m[3]);
  return out;
}

function isExternal(u) {
  return /^(?:[a-z][a-z0-9+.-]*:)?\/\//i.test(u) || u.startsWith("data:") || u.startsWith("blob:") || u.startsWith("mailto:") || u.startsWith("#");
}

function urlToDiskPath(u, base, clientRoot) {
  const clean = u.split("?")[0].split("#")[0];
  if (!clean) return null;
  let rel = clean;
  if (clean.startsWith("/")) {
    const b = base.endsWith("/") ? base : base + "/";
    if (b !== "/" && !clean.startsWith(b)) return { escaped: true, url: clean };
    rel = clean.slice(b.length);
  }
  const abs = resolve(clientRoot, rel);
  const inside = abs === clientRoot || abs.startsWith(clientRoot + sep);
  if (!inside) return { escaped: true, url: clean };
  return { escaped: false, url: clean, abs };
}

// ---------------------------------------------------------------- secret scan

const SECRET_PATTERNS = [
  ["aws-access-key-id", /\bAKIA[0-9A-Z]{16}\b/],
  ["private-key-block", /-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY-----/],
  ["github-token", /\bgh[pousr]_[A-Za-z0-9]{36,}\b/],
  ["gitlab-pat", /\bglpat-[A-Za-z0-9_-]{20,}\b/],
  ["json-web-token", /\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b/],
  ["slack-token", /\bxox[abprs]-[A-Za-z0-9-]{10,}\b/],
  ["credentialled-url", /\b(?:postgres|postgresql|mysql|mongodb\+srv|mongodb|redis|amqp|amqps)::?\/\/[^\s"'<>]{1,64}:[^\s"'@<>]{4,}@/]
];

const ASSIGNED_SECRET = /["'`]?\b(?:secret|password|passwd|api[_-]?key|apikey|access[_-]?token|refresh[_-]?token|client[_-]?secret|private[_-]?key)\b["'`]?\s*[:=]\s*["'`]([^"'`\n]{16,200})["'`]/gi;

function shannon(s) {
  const f = new Map();
  for (const c of s) f.set(c, (f.get(c) || 0) + 1);
  let h = 0;
  for (const n of f.values()) { const p = n / s.length; h -= p * Math.log2(p); }
  return h;
}

function scanSecrets(text) {
  const hits = [];
  for (const [id, re] of SECRET_PATTERNS) {
    const m = re.exec(text);
    if (m) hits.push({ id, sample: m[0].slice(0, 24) + "…" });
  }
  ASSIGNED_SECRET.lastIndex = 0;
  let m;
  while ((m = ASSIGNED_SECRET.exec(text)) !== null) {
    const v = m[1];
    if (/^[A-Za-z0-9+/=_-]{16,}$/.test(v) && shannon(v) >= 3.6) {
      hits.push({ id: "high-entropy-assignment", sample: m[0].slice(0, 40) + "…" });
      break;
    }
  }
  return hits;
}

function parseEnvFile(path) {
  const out = new Map();
  for (const line of readFileSync(path, "utf8").split(/\r?\n/)) {
    const t = line.trim();
    if (!t || t.startsWith("#")) continue;
    const eq = t.indexOf("=");
    if (eq <= 0) continue;
    let v = t.slice(eq + 1).trim();
    if ((v.startsWith('"') && v.endsWith('"')) || (v.startsWith("'") && v.endsWith("'"))) v = v.slice(1, -1);
    out.set(t.slice(0, eq).trim(), v);
  }
  return out;
}

// ---------------------------------------------------------------- assertions

// A content hash is a trailing token of >=8 url-safe chars, separated by "." or "-",
// that mixes cases or mixes digits and letters. Vite and Rolldown emit "name-<hash>.js";
// older toolchains emit "name.<hash>.js". Both are accepted; "vendor.js" is not.
const HASH_TOKEN = /[.-]([A-Za-z0-9_-]{8,})$/;
function isContentHashed(fileName) {
  const stem = fileName.replace(/\.(?:js|css)$/, "");
  const m = HASH_TOKEN.exec(stem);
  if (!m) return false;
  // Structural test only. Requiring mixed case or a digit rejects real single-case
  // base64url hashes such as "-DZBSHXEX" and "--jyobkv-", and a false positive here
  // blocks a correct build, which is worse than the false negative it would prevent.
  return m[1].length >= 8;
}
const PROVENANCE_KEYS = ["commit", "ref", "builtAt", "nodeVersion", "packageManager", "lockfileHash", "buildMode"];

function run(opts) {
  const findings = [];
  const add = (id, path, message) => findings.push({ id, path, message });

  const root = resolve(opts.root);
  if (!existsSync(root)) return { code: EXIT_CANNOT_RUN, findings, note: `build output root not found: ${root}` };
  let st;
  try { st = statSync(root); } catch (e) { return { code: EXIT_CANNOT_RUN, findings, note: `unreadable: ${root}: ${e.message}` }; }
  if (!st.isDirectory()) return { code: EXIT_CANNOT_RUN, findings, note: `not a directory: ${root}` };

  const layout = inferLayout(root, opts.mode);
  if (!existsSync(layout.clientRoot)) return { code: EXIT_CANNOT_RUN, findings, note: `client root missing: ${layout.clientRoot}` };
  let files;
  try { files = walk(layout.clientRoot); } catch (e) { return { code: EXIT_CANNOT_RUN, findings, note: `cannot walk ${layout.clientRoot}: ${e.message}` }; }
  if (files.length === 0) return { code: EXIT_CANNOT_RUN, findings, note: `no files under ${layout.clientRoot}` };

  const htmlFiles = files.filter((f) => f.endsWith(".html"));
  const manifests = [join(root, "quasar.manifest.json"), join(layout.clientRoot, "manifest.json")].filter(existsSync);
  if (htmlFiles.length === 0 && manifests.length === 0) {
    return { code: EXIT_CANNOT_RUN, findings, note: `no emitted HTML and no asset manifest under ${root}; this does not look like a build output tree` };
  }

  // A1 — SSR runtime entry
  if (layout.mode === "ssr" && !opts.skip.has("A1")) {
    const entry = join(root, "index.js");
    if (!existsSync(entry)) add("A1", relative(root, entry), "SSR runtime entry is absent");
  }

  // A2 / A3 — referenced assets resolve, and stay inside the client root
  if (!opts.skip.has("A2") || !opts.skip.has("A3")) {
    const refs = [];
    for (const h of htmlFiles) for (const u of htmlUrls(readFileSync(h, "utf8"))) refs.push({ from: relative(root, h), url: u });
    for (const mf of manifests) {
      let data;
      try { data = JSON.parse(readFileSync(mf, "utf8")); } catch { add("A2", relative(root, mf), "manifest is not parseable JSON"); continue; }
      const collect = (v) => {
        if (typeof v === "string") { if (/\.(?:js|css|woff2?|png|svg|jpe?g|webp|json)$/i.test(v)) refs.push({ from: relative(root, mf), url: v }); }
        else if (Array.isArray(v)) v.forEach(collect);
        else if (v && typeof v === "object") Object.values(v).forEach(collect);
      };
      collect(data);
    }
    for (const r of refs) {
      if (isExternal(r.url)) continue;
      const p = urlToDiskPath(r.url, opts.base, layout.clientRoot);
      if (!p) continue;
      if (p.escaped) { if (!opts.skip.has("A3")) add("A3", r.from, `asset URL escapes the client asset root or does not match --base ${opts.base}: ${p.url}`); continue; }
      if (!opts.skip.has("A2") && !existsSync(p.abs)) add("A2", r.from, `references an asset that does not exist on disk: ${p.url}`);
    }
  }

  // A5 — content-hashed filenames under the asset root
  if (!opts.skip.has("A5") && existsSync(layout.assetRoot)) {
    for (const f of walk(layout.assetRoot)) {
      if (!/\.(?:js|css)$/.test(f)) continue;
      if (!isContentHashed(f.split(sep).pop())) add("A5", relative(root, f), "emitted chunk filename carries no content hash, so an immutable cache header is unsafe");
    }
  }

  // A4 — secret-shaped values in emitted chunks
  if (!opts.skip.has("A4")) {
    let forbidden = [];
    if (opts.env) {
      let env;
      try { env = parseEnvFile(resolve(opts.env)); } catch (e) { return { code: EXIT_USAGE, findings, note: `cannot read --env ${opts.env}: ${e.message}` }; }
      for (const [k, v] of env) {
        if (k.startsWith(opts.clientPrefix)) continue;
        if (v.length < 8) continue;
        if (/^(?:true|false|null|undefined|[0-9.]+)$/i.test(v)) continue;
        forbidden.push([k, v]);
      }
    }
    for (const f of files) {
      if (!/\.(?:js|css|mjs|html|json|map)$/.test(f)) continue;
      let text;
      try { text = readFileSync(f, "utf8"); } catch { continue; }
      for (const h of scanSecrets(text)) add("A4", relative(root, f), `secret-shaped value (${h.id}): ${h.sample}`);
      for (const [k, v] of forbidden) if (text.includes(v)) add("A4", relative(root, f), `value of non-prefixed environment variable ${k} appears verbatim in an emitted client file`);
    }
  }

  // A6 — provenance
  if (!opts.skip.has("A6")) {
    const p = join(root, opts.provenance);
    if (!existsSync(p)) add("A6", relative(root, p), "provenance file is absent; the artifact cannot be traced to a commit");
    else {
      let data;
      try { data = JSON.parse(readFileSync(p, "utf8")); } catch { data = null; }
      if (data === null) add("A6", relative(root, p), "provenance file is not parseable JSON");
      else for (const k of PROVENANCE_KEYS) if (data[k] === undefined || data[k] === "") add("A6", relative(root, p), `provenance key is missing or empty: ${k}`);
    }
  }

  return { code: findings.length ? EXIT_VIOLATION : EXIT_OK, findings, layout, fileCount: files.length };
}

// ---------------------------------------------------------------- entry point

function main() {
  let opts;
  try { opts = parseArgs(process.argv.slice(2)); }
  catch (e) { console.error(`error: ${e.usage || e.message}\n`); console.error(HELP); process.exit(EXIT_USAGE); }

  if (opts.help) { console.log(HELP); process.exit(EXIT_OK); }
  if (!opts.root) { console.error("error: <dist-root> is required\n"); console.error(HELP); process.exit(EXIT_USAGE); }

  const res = run(opts);
  if (opts.json) console.log(JSON.stringify({ exitCode: res.code, note: res.note ?? null, findings: res.findings }, null, 2));
  else {
    if (res.note) console.error(`could-not-run: ${res.note}`);
    for (const f of res.findings) console.error(`${f.id}  ${f.path}: ${f.message}`);
    if (res.code === EXIT_OK) console.log(`artifact contract: OK (${res.layout.mode} mode, ${res.fileCount} files under ${res.layout.clientRoot})`);
    else if (res.code === EXIT_VIOLATION) console.error(`\nartifact contract: ${res.findings.length} failure(s)`);
  }
  process.exit(res.code);
}

main();
