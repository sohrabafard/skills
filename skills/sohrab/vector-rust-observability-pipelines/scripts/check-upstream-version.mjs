#!/usr/bin/env node
// Compare the Vector and Helm-chart versions this skill pins against what
// upstream currently publishes.
//
// Exit codes are a contract:
//   0  every pin matches the current upstream version
//   1  drift: at least one pin is stale
//   2  the check could not run (network, proxy, or unreadable pin file)
//
// Exit 2 must never be reported as 0. A version checker that treats "the
// network was blocked" as "everything is current" is how a skill silently ages.

import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const SKILL_ROOT = path.resolve(SCRIPT_DIR, '..');
const PIN_FILE = path.join(SKILL_ROOT, 'references', '80-version-and-upgrade-deltas.md');
const FIXTURE = path.join(SKILL_ROOT, 'assets', 'fixtures', 'upstream-releases.sample.json');

const EXIT_CLEAN = 0;
const EXIT_FINDINGS = 1;
const EXIT_CANNOT_RUN = 2;

const RELEASES_API = 'https://api.github.com/repos/vectordotdev/vector/releases?per_page=100';
const MASTER_CARGO = 'https://raw.githubusercontent.com/vectordotdev/vector/master/Cargo.toml';
const TAG_CARGO = (v) => `https://raw.githubusercontent.com/vectordotdev/vector/v${v}/Cargo.toml`;
const CHART_YAML = 'https://raw.githubusercontent.com/vectordotdev/helm-charts/develop/charts/vector/Chart.yaml';

const TIMEOUT_MS = 20000;

function usage() {
  console.log(`check-upstream-version.mjs - detect drift between this skill's version pins and upstream.

Usage:
  node scripts/check-upstream-version.mjs [--self-test] [--help]

Options:
  --self-test  Run offline against the committed fixture in
               assets/fixtures/upstream-releases.sample.json. Asserts that the
               release resolver rejects the \`vdev-*\` tags that GitHub's
               /releases/latest endpoint returns for this repository.
  --help, -h   Show this message.

Exit codes:
  0  pins current    1  drift    2  could not run

Pins are read from references/80-version-and-upgrade-deltas.md, so the document
and this checker cannot disagree about what is pinned.`);
}

// The Vector repository tags its `vdev` developer tool in the same repository.
// GitHub's /releases/latest returns `vdev-v0.3.3`, which is NOT a Vector
// release. Only vX.Y.Z tags count.
const RELEASE_TAG = /^v(\d+)\.(\d+)\.(\d+)$/;

function resolveLatestFromReleases(releases) {
  const versions = [];
  for (const r of releases) {
    const m = RELEASE_TAG.exec(r.tag_name || '');
    if (m) versions.push([Number(m[1]), Number(m[2]), Number(m[3])]);
  }
  if (versions.length === 0) return null;
  versions.sort((a, b) => b[0] - a[0] || b[1] - a[1] || b[2] - a[2]);
  return versions[0].join('.');
}

async function httpGet(url) {
  try {
    const res = await fetch(url, {
      signal: AbortSignal.timeout(TIMEOUT_MS),
      headers: { 'user-agent': 'vector-skill-version-check' },
    });
    if (!res.ok) return { ok: false, status: res.status };
    return { ok: true, body: await res.text() };
  } catch (err) {
    // Some environments route egress through a proxy that Node's fetch does not
    // pick up. curl honours HTTPS_PROXY and ships with Windows 10+ and macOS.
    const curl = spawnSync('curl', ['-sS', '--max-time', String(TIMEOUT_MS / 1000), url], { encoding: 'utf8' });
    if (!curl.error && curl.status === 0 && curl.stdout) return { ok: true, body: curl.stdout };
    return { ok: false, error: err.message };
  }
}

async function resolveVectorRelease() {
  const api = await httpGet(RELEASES_API);
  if (api.ok) {
    try {
      const latest = resolveLatestFromReleases(JSON.parse(api.body));
      if (latest) return { ok: true, version: latest, how: 'GitHub releases API, vX.Y.Z tags only' };
    } catch { /* fall through to tag probing */ }
  }
  // Fallback that needs only raw.githubusercontent.com: master's Cargo.toml
  // carries the in-development version, so the newest RELEASED minor is at most
  // one below it. Probe downward until a tag resolves.
  const cargo = await httpGet(MASTER_CARGO);
  if (!cargo.ok) return { ok: false, reason: `could not reach GitHub (api: ${api.status || api.error}, raw: ${cargo.status || cargo.error})` };
  const m = /^version\s*=\s*"(\d+)\.(\d+)\.(\d+)"/m.exec(cargo.body);
  if (!m) return { ok: false, reason: 'could not parse version from master Cargo.toml' };
  const major = Number(m[1]);
  for (let minor = Number(m[2]); minor >= 0; minor -= 1) {
    for (let patch = 9; patch >= 0; patch -= 1) {
      const cand = `${major}.${minor}.${patch}`;
      const probe = await httpGet(TAG_CARGO(cand));
      if (probe.ok) return { ok: true, version: cand, how: 'highest existing vX.Y.Z tag on raw.githubusercontent.com' };
    }
  }
  return { ok: false, reason: 'no released tag found' };
}

async function resolveChartVersion() {
  const res = await httpGet(CHART_YAML);
  if (!res.ok) return { ok: false, reason: `could not read Chart.yaml (${res.status || res.error})` };
  const version = /^version:\s*"?([^"\s]+)"?/m.exec(res.body);
  const appVersion = /^appVersion:\s*"?([^"\s]+)"?/m.exec(res.body);
  if (!version) return { ok: false, reason: 'could not parse chart version' };
  return { ok: true, version: version[1], appVersion: appVersion ? appVersion[1] : null };
}

function readPins() {
  if (!fs.existsSync(PIN_FILE)) return { ok: false, reason: `pin file missing: ${PIN_FILE}` };
  const text = fs.readFileSync(PIN_FILE, 'utf8');
  const pins = {};
  for (const m of text.matchAll(/^\s*PIN\s+([a-z0-9-]+)\s*=\s*([0-9][0-9A-Za-z.\-]*)\s*$/gm)) {
    pins[m[1]] = m[2];
  }
  if (Object.keys(pins).length === 0) return { ok: false, reason: `no PIN lines found in ${PIN_FILE}` };
  return { ok: true, pins };
}

function compare(pins, current) {
  const drift = [];
  for (const [key, currentValue] of Object.entries(current)) {
    if (!(key in pins)) continue;
    if (pins[key] !== currentValue) drift.push({ key, pinned: pins[key], current: currentValue });
  }
  return drift;
}

function selfTest() {
  console.log('Self-test (offline): the release resolver must reject vdev-* tags.');
  let failures = 0;
  let fixture;
  try {
    fixture = JSON.parse(fs.readFileSync(FIXTURE, 'utf8'));
  } catch (err) {
    console.error(`BLOCKED: cannot read fixture ${FIXTURE}: ${err.message}`);
    return { blocked: true };
  }

  const got = resolveLatestFromReleases(fixture.releases);
  const wantLatest = fixture.expected_latest;
  const okTrap = got === wantLatest;
  if (!okTrap) failures += 1;
  console.log(`  ${okTrap ? 'PASS' : 'FAIL'}  vdev trap: expected ${wantLatest}, got ${got}`);

  const naive = (fixture.releases[0] || {}).tag_name;
  const okNaive = naive === 'vdev-v0.3.3' && got !== '0.3.3';
  if (!okNaive) failures += 1;
  console.log(`  ${okNaive ? 'PASS' : 'FAIL'}  the naive "take /releases/latest" answer (${naive}) is rejected`);

  const onlyVdev = resolveLatestFromReleases([{ tag_name: 'vdev-v0.3.3' }]);
  const okEmpty = onlyVdev === null;
  if (!okEmpty) failures += 1;
  console.log(`  ${okEmpty ? 'PASS' : 'FAIL'}  a vdev-only list resolves to null rather than a bogus version`);

  const drift = compare({ vector: '0.53.0' }, { vector: '0.57.0' });
  const okDrift = drift.length === 1;
  if (!okDrift) failures += 1;
  console.log(`  ${okDrift ? 'PASS' : 'FAIL'}  a stale pin (0.53.0 vs 0.57.0) is reported as drift`);

  const clean = compare({ vector: '0.57.0' }, { vector: '0.57.0' });
  const okClean = clean.length === 0;
  if (!okClean) failures += 1;
  console.log(`  ${okClean ? 'PASS' : 'FAIL'}  a current pin (0.57.0) is reported clean`);

  return { blocked: false, failures };
}

async function main() {
  const argv = process.argv.slice(2);
  if (argv.includes('--help') || argv.includes('-h')) { usage(); return EXIT_CLEAN; }

  if (argv.includes('--self-test')) {
    const st = selfTest();
    if (st.blocked) return EXIT_CANNOT_RUN;
    if (st.failures > 0) { console.error(`Self-test FAILED: ${st.failures} assertion(s).`); return EXIT_FINDINGS; }
    console.log('Self-test passed.');
    return EXIT_CLEAN;
  }

  const pinned = readPins();
  if (!pinned.ok) { console.error(`BLOCKED: ${pinned.reason}`); return EXIT_CANNOT_RUN; }

  const vector = await resolveVectorRelease();
  if (!vector.ok) { console.error(`BLOCKED: ${vector.reason}`); return EXIT_CANNOT_RUN; }
  const chart = await resolveChartVersion();
  if (!chart.ok) { console.error(`BLOCKED: ${chart.reason}`); return EXIT_CANNOT_RUN; }

  console.log(`vector      pinned ${pinned.pins.vector || '(unpinned)'}  current ${vector.version}  (${vector.how})`);
  console.log(`helm-chart  pinned ${pinned.pins['helm-chart'] || '(unpinned)'}  current ${chart.version}  appVersion ${chart.appVersion}`);

  if (chart.appVersion && !chart.appVersion.startsWith(vector.version)) {
    console.log(`note: chart appVersion (${chart.appVersion}) is not the current Vector release (${vector.version}); a Helm-deployed pipeline runs a different Vector build from a package-installed one.`);
  }

  const drift = compare(pinned.pins, { vector: vector.version, 'helm-chart': chart.version });
  if (drift.length > 0) {
    for (const d of drift) console.error(`DRIFT: ${d.key} pinned at ${d.pinned}, upstream is ${d.current}`);
    console.error('Update the pins and the deltas in references/80-version-and-upgrade-deltas.md.');
    return EXIT_FINDINGS;
  }
  console.log('All pins current.');
  return EXIT_CLEAN;
}

main().then((code) => process.exit(code)).catch((err) => {
  console.error(`BLOCKED: checker failed: ${err && err.stack ? err.stack : err}`);
  process.exit(EXIT_CANNOT_RUN);
});
