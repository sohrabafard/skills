#!/usr/bin/env node
/**
 * check-shaka-api.mjs - report Shaka Player call sites that use an API removed or
 * deprecated between the repository's installed version and the current release.
 *
 * Facts source: /alaa-shaka-player references/80-version-migration-and-release-deltas.md
 * and references/05-provenance-and-freshness.md. Anchor version v5.2.3, read 2026-07-28.
 *
 * Exit codes (documented, and distinct on purpose):
 *   0  clean          - the scan ran and found no removed or deprecated API in scope
 *   1  findings       - the scan ran and found at least one REMOVED api (a defect)
 *   2  could-not-run  - the scan did NOT complete: bad path, no package.json,
 *                       unreadable version, no source files. NEVER confuse with 0.
 *   3  self-test-fail - --self-test ran and a case did not produce its expected verdict
 * A deprecated-only result exits 0 and prints warnings, unless --strict is given.
 */

import { readFile, readdir, stat } from "node:fs/promises";
import { join, relative, resolve, extname } from "node:path";
import process from "node:process";

const ANCHOR_VERSION = "5.2.3";
const ANCHOR_READ_DATE = "2026-07-28";

/** One rule. `removedIn` is the first version where the symbol no longer exists. */
const RULES = [
  // --- REMOVED in v5.0. Calling these throws; optional-chaining them silently no-ops. ---
  { symbol: "selectAudioLanguage", kind: "removed", removedIn: "5.0.0",
    replacement: "selectAudioTrack(audioTrack, safeMargin)", ref: "26-tracks-audio-video-text.md" },
  { symbol: "getAudioLanguagesAndRoles", kind: "removed", removedIn: "5.0.0",
    replacement: "getAudioTracks()", ref: "26-tracks-audio-video-text.md" },
  { symbol: "getAudioLanguages", kind: "removed", removedIn: "5.0.0",
    replacement: "getAudioTracks()", ref: "26-tracks-audio-video-text.md" },
  { symbol: "setTextTrackVisibility", kind: "removed", removedIn: "5.0.0",
    replacement: "selectTextTrack() - selecting makes a track visible", ref: "26-tracks-audio-video-text.md" },
  { symbol: "isTextTrackVisible", kind: "removed", removedIn: "5.0.0",
    replacement: "read TextTrack.active from getTextTracks()", ref: "26-tracks-audio-video-text.md" },
  { symbol: "getChapters", kind: "removed", removedIn: "5.0.0", exact: true,
    replacement: "getChaptersAsync(language)", ref: "26-tracks-audio-video-text.md" },
  { symbol: "initClientSide", kind: "removed", removedIn: "5.0.0",
    replacement: "requestClientSideAds(imaRequest, adsRenderingSettings)", ref: "55-ads-vast-vmap-and-ima.md" },
  { symbol: "initServerSide", kind: "removed", removedIn: "5.0.0",
    replacement: "requestServerSideStream(imaRequest, backupUrl)", ref: "55-ads-vast-vmap-and-ima.md" },
  { symbol: "initMediaTailor", kind: "removed", removedIn: "5.0.0",
    replacement: "requestMediaTailorStream(url, adsParams, backupUrl)", ref: "55-ads-vast-vmap-and-ima.md" },
  { symbol: "initInterstitial", kind: "removed", removedIn: "5.0.0",
    replacement: "interstitials auto-initialise; use addCustomInterstitial / addAdUrlInterstitial",
    ref: "55-ads-vast-vmap-and-ima.md" },
  { symbol: "onDashTimedMetadata", kind: "removed", removedIn: "5.0.0",
    replacement: "onDASHMetadata(region)", ref: "55-ads-vast-vmap-and-ima.md" },
  { symbol: "useNativeHlsOnSafari", kind: "removed", removedIn: "5.0.0",
    replacement: "streaming.useNativeHlsForFairPlay or streaming.preferNativeHls",
    ref: "22-streaming-formats-and-native-hls.md" },
  { symbol: "forceTransmuxTS", kind: "removed", removedIn: "5.0.0",
    replacement: "streaming.forceTransmux", ref: "80-version-migration-and-release-deltas.md" },
  { symbol: "liveSyncMinLatency", kind: "removed", removedIn: "5.0.0",
    replacement: "streaming.liveSync.targetLatency", ref: "32-live-and-low-latency.md" },
  { symbol: "liveSyncMaxLatency", kind: "removed", removedIn: "5.0.0",
    replacement: "streaming.liveSync.targetLatency", ref: "32-live-and-low-latency.md" },
  { symbol: "autoShowText", kind: "removed", removedIn: "5.0.0",
    replacement: "preferredText[]", ref: "26-tracks-audio-video-text.md" },
  { symbol: "addBigPlayButton", kind: "removed", removedIn: "5.0.0",
    replacement: "UI config bigButtons", ref: "65-ui-library-skin-and-localisation.md" },
  { symbol: "FairPlayUtils", kind: "removed", removedIn: "5.0.0",
    replacement: "shaka.drm.FairPlay", ref: "45-drm.md" },
  { symbol: "smallGapLimit", kind: "removed", removedIn: "4.0.0",
    replacement: "none - all gaps are now jumped", ref: "35-unstable-networks-and-resilience.md" },
  { symbol: "jumpLargeGaps", kind: "removed", removedIn: "4.0.0",
    replacement: "none - all gaps are now jumped", ref: "35-unstable-networks-and-resilience.md" },

  // --- NEVER EXISTED. Named in briefs; searched for and not found at v5.2.3. ---
  { symbol: "removeEmptyEpisodes", kind: "absent", removedIn: "0.0.0",
    replacement: "storage.remove(uri) / storage.removeEmeSessions()", ref: "50-offline-and-in-app-download.md" },

  // --- DEPRECATED in v5.1, scheduled for removal in v6.0. Also absent from the shipped .d.ts. ---
  ...["preferredAudioLanguage", "preferredAudioRole", "preferredAudioLabel",
      "preferredAudioChannelCount", "preferSpatialAudio", "preferredAudioCodecs"]
    .map(s => ({ symbol: s, kind: "deprecated", removedIn: "6.0.0",
                 replacement: "preferredAudio: [{...}]", ref: "26-tracks-audio-video-text.md" })),
  ...["preferredTextLanguage", "preferredTextRole", "preferForcedSubs", "preferredTextFormats"]
    .map(s => ({ symbol: s, kind: "deprecated", removedIn: "6.0.0",
                 replacement: "preferredText: [{...}]", ref: "26-tracks-audio-video-text.md" })),
  ...["preferredVideoLabel", "preferredVideoRole", "preferredVideoHdrLevel",
      "preferredVideoLayout", "preferredVideoCodecs"]
    .map(s => ({ symbol: s, kind: "deprecated", removedIn: "6.0.0",
                 replacement: "preferredVideo: [{...}]", ref: "26-tracks-audio-video-text.md" })),
  { symbol: "preferredVariantRole", kind: "removed", removedIn: "5.0.0",
    replacement: "preferredAudio[].role", ref: "26-tracks-audio-video-text.md" }
];

const SOURCE_EXT = new Set([".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".vue"]);
const SKIP_DIR = new Set(["node_modules", ".git", "dist", "build", "coverage", ".nx", ".output",
                          ".quasar", ".next", ".cache", "_to_delete"]);

function parseVersion(v) {
  const m = String(v).match(/(\d+)\.(\d+)\.(\d+)/);
  return m ? [Number(m[1]), Number(m[2]), Number(m[3])] : null;
}
function cmp(a, b) {
  for (let i = 0; i < 3; i += 1) { if (a[i] !== b[i]) return a[i] < b[i] ? -1 : 1; }
  return 0;
}

function usage() {
  process.stdout.write(`check-shaka-api.mjs - find Shaka APIs removed or deprecated between the
repository's installed shaka-player version and v${ANCHOR_VERSION} (facts read ${ANCHOR_READ_DATE}).

USAGE
  node check-shaka-api.mjs --repo <path> [--target <version>] [--json] [--strict]
  node check-shaka-api.mjs --self-test
  node check-shaka-api.mjs --help

OPTIONS
  --repo <path>      Repository root to scan. Required unless --self-test/--help.
  --target <ver>     Compare against this version instead of the version found in
                     package.json. Use when planning an upgrade.
  --json             Emit machine-readable JSON instead of text.
  --strict           Treat deprecated-only findings as failures (exit 1).
  --self-test        Run built-in cases against synthetic sources and verify verdicts.

EXIT CODES
  0  clean          scan completed, no removed API in scope
  1  findings       scan completed, at least one removed/absent API found
                    (or a deprecated one under --strict)
  2  could-not-run  scan did NOT complete - distinct from clean, on purpose
  3  self-test-fail --self-test found a case whose verdict was wrong
`);
}

async function findSourceFiles(root, out = [], depth = 0) {
  if (depth > 12) return out;
  let entries;
  try { entries = await readdir(root, { withFileTypes: true }); } catch { return out; }
  for (const e of entries) {
    if (e.isDirectory()) {
      if (SKIP_DIR.has(e.name) || e.name.startsWith(".")) continue;
      await findSourceFiles(join(root, e.name), out, depth + 1);
    } else if (e.isFile() && SOURCE_EXT.has(extname(e.name))) {
      out.push(join(root, e.name));
    }
  }
  return out;
}

/** Reads the installed shaka-player version. Returns {version, source} or null. */
async function readInstalledVersion(repo) {
  const roots = [repo];
  try {
    const pkgs = await readdir(join(repo, "packages"), { withFileTypes: true });
    for (const p of pkgs) if (p.isDirectory()) roots.push(join(repo, "packages", p.name));
  } catch { /* no packages dir */ }

  for (const r of roots) {
    let raw;
    try { raw = await readFile(join(r, "package.json"), "utf8"); } catch { continue; }
    let pkg;
    try { pkg = JSON.parse(raw); } catch { continue; }
    for (const field of ["dependencies", "devDependencies", "peerDependencies"]) {
      const spec = pkg[field] && pkg[field]["shaka-player"];
      if (!spec) continue;
      const parsed = parseVersion(spec);
      if (parsed) {
        return { version: parsed, raw: spec,
                 source: `${relative(repo, join(r, "package.json")) || "package.json"} (${field})` };
      }
    }
  }
  return null;
}

function scanText(text, rule) {
  const hits = [];
  const pattern = rule.exact
    ? new RegExp(`\\b${rule.symbol}\\b(?!Async)`, "g")
    : new RegExp(`\\b${rule.symbol}\\b`, "g");
  const lines = text.split("\n");
  for (let i = 0; i < lines.length; i += 1) {
    pattern.lastIndex = 0;
    if (pattern.test(lines[i])) hits.push({ line: i + 1, text: lines[i].trim().slice(0, 160) });
  }
  return hits;
}

/** Returns findings for one text blob. `installed` may be null (then all rules apply). */
function analyse(text, installed, target) {
  const found = [];
  for (const rule of RULES) {
    const gone = parseVersion(rule.removedIn);
    // A rule is in scope when the symbol is already gone at the target version,
    // or is scheduled to go by then.
    const inScope = !installed || !gone || cmp(target, gone) >= 0 || rule.kind === "deprecated";
    if (!inScope) continue;
    for (const hit of scanText(text, rule)) found.push({ ...rule, ...hit });
  }
  return found;
}

async function runScan(opts) {
  let st;
  try { st = await stat(opts.repo); } catch {
    process.stderr.write(`could-not-run: no such path: ${opts.repo}\n`); return 2;
  }
  if (!st.isDirectory()) {
    process.stderr.write(`could-not-run: not a directory: ${opts.repo}\n`); return 2;
  }

  const installed = await readInstalledVersion(opts.repo);
  if (!installed && !opts.target) {
    process.stderr.write(
      `could-not-run: no shaka-player dependency found in ${opts.repo} ` +
      `(searched package.json at the root and under packages/*). ` +
      `Pass --target <version> to scan anyway.\n`);
    return 2;
  }

  const target = opts.target ? parseVersion(opts.target)
                             : parseVersion(ANCHOR_VERSION);
  if (!target) { process.stderr.write(`could-not-run: unparseable --target\n`); return 2; }

  const files = await findSourceFiles(opts.repo);
  if (files.length === 0) {
    process.stderr.write(`could-not-run: no source files under ${opts.repo}\n`); return 2;
  }

  const findings = [];
  for (const file of files) {
    let text;
    try { text = await readFile(file, "utf8"); } catch { continue; }
    if (!/shaka|Shaka|preferred(Audio|Text|Video)/.test(text)) continue;
    for (const f of analyse(text, installed && installed.version, target)) {
      findings.push({ ...f, file: relative(opts.repo, file) });
    }
  }

  const removed = findings.filter(f => f.kind === "removed" || f.kind === "absent");
  const deprecated = findings.filter(f => f.kind === "deprecated");

  if (opts.json) {
    process.stdout.write(JSON.stringify({
      anchorVersion: ANCHOR_VERSION, anchorReadDate: ANCHOR_READ_DATE,
      installed: installed ? { spec: installed.raw, source: installed.source } : null,
      targetVersion: target.join("."), filesScanned: files.length,
      removed, deprecated
    }, null, 2) + "\n");
  } else {
    process.stdout.write(`shaka-api check\n`);
    process.stdout.write(`  repo         : ${resolve(opts.repo)}\n`);
    process.stdout.write(`  installed    : ${installed ? `${installed.raw}  (${installed.source})` : "not found"}\n`);
    process.stdout.write(`  compared to  : v${target.join(".")}   (facts read ${ANCHOR_READ_DATE})\n`);
    process.stdout.write(`  files scanned: ${files.length}\n\n`);

    if (removed.length === 0 && deprecated.length === 0) {
      process.stdout.write(`CLEAN - no removed or deprecated Shaka API found.\n`);
    }
    for (const f of removed) {
      process.stdout.write(
        `REMOVED   ${f.file}:${f.line}\n` +
        `          ${f.symbol}  - gone since v${f.removedIn}\n` +
        `          use: ${f.replacement}\n` +
        `          ref: references/${f.ref}\n` +
        `          > ${f.text}\n\n`);
    }
    for (const f of deprecated) {
      process.stdout.write(
        `DEPRECATED ${f.file}:${f.line}\n` +
        `          ${f.symbol}  - removal scheduled for v${f.removedIn}; ` +
        `already absent from the shipped .d.ts\n` +
        `          use: ${f.replacement}\n` +
        `          ref: references/${f.ref}\n` +
        `          > ${f.text}\n\n`);
    }
    process.stdout.write(`summary: ${removed.length} removed, ${deprecated.length} deprecated\n`);
    if (removed.length > 0) {
      process.stdout.write(
        `\nNOTE: an optional-chained call to a removed method (foo?.bar()) is still a finding.\n` +
        `      It converts a loud TypeError into a silent no-op, which is worse.\n`);
    }
  }

  if (removed.length > 0) return 1;
  if (opts.strict && deprecated.length > 0) return 1;
  return 0;
}

function selfTest() {
  const cases = [
    { name: "removed method is found",
      text: `player.selectAudioLanguage("fa");`, installed: [5, 1, 11],
      expect: { removed: 1, deprecated: 0 } },
    { name: "optional-chained removed method is still found",
      text: `currentPlayer.setTextTrackVisibility?.(false);`, installed: [5, 1, 11],
      expect: { removed: 1, deprecated: 0 } },
    { name: "deprecated preference key is flagged, not counted as removed",
      text: `player.configure("preferredAudioLanguage", "fa");`, installed: [5, 1, 11],
      expect: { removed: 0, deprecated: 1 } },
    { name: "v6-ready spelling is clean",
      text: `player.configure({preferredAudio: [{language: "fa"}]});`, installed: [5, 1, 11],
      expect: { removed: 0, deprecated: 0 } },
    { name: "current API is clean",
      text: `player.selectAudioTrack(track, 4); player.getAudioTracks();`, installed: [5, 2, 3],
      expect: { removed: 0, deprecated: 0 } },
    { name: "getChaptersAsync is not mistaken for getChapters",
      text: `await player.getChaptersAsync("fa");`, installed: [5, 2, 3],
      expect: { removed: 0, deprecated: 0 } },
    { name: "a method Shaka never had is reported as absent",
      text: `await storage.removeEmptyEpisodes();`, installed: [5, 2, 3],
      expect: { removed: 1, deprecated: 0 } },
    { name: "removed config key is found",
      text: `streaming: { useNativeHlsOnSafari: true }`, installed: [4, 16, 38],
      expect: { removed: 1, deprecated: 0 } }
  ];

  const target = parseVersion(ANCHOR_VERSION);
  let failed = 0;
  for (const c of cases) {
    const out = analyse(c.text, c.installed, target);
    const removed = out.filter(f => f.kind === "removed" || f.kind === "absent").length;
    const deprecated = out.filter(f => f.kind === "deprecated").length;
    const ok = removed === c.expect.removed && deprecated === c.expect.deprecated;
    if (!ok) failed += 1;
    process.stdout.write(
      `${ok ? "PASS" : "FAIL"}  ${c.name}  ` +
      `(removed ${removed}/${c.expect.removed}, deprecated ${deprecated}/${c.expect.deprecated})\n`);
  }
  process.stdout.write(`\n${cases.length - failed}/${cases.length} self-test cases passed\n`);
  return failed === 0 ? 0 : 3;
}

async function main() {
  const argv = process.argv.slice(2);
  if (argv.length === 0 || argv.includes("--help") || argv.includes("-h")) { usage(); return 0; }
  if (argv.includes("--self-test")) return selfTest();

  const opts = { repo: null, target: null, json: argv.includes("--json"),
                 strict: argv.includes("--strict") };
  for (let i = 0; i < argv.length; i += 1) {
    if (argv[i] === "--repo") opts.repo = argv[i + 1];
    if (argv[i] === "--target") opts.target = argv[i + 1];
  }
  if (!opts.repo) {
    process.stderr.write("could-not-run: --repo <path> is required. See --help.\n");
    return 2;
  }
  return runScan(opts);
}

main().then(code => process.exit(code)).catch(err => {
  process.stderr.write(`could-not-run: ${err && err.stack ? err.stack : err}\n`);
  process.exit(2);
});
