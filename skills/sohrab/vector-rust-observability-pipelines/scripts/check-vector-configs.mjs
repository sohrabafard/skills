#!/usr/bin/env node
// Validate every Vector config this skill ships, plus any config you pass in.
//
// Exit codes are a contract:
//   0  every target validated clean
//   1  at least one target has a finding
//   2  the check could not run (Vector missing, or the checker itself failed)
//
// A checker whose "could not run" is indistinguishable from "clean" is worse
// than no checker, because a CI gate built on it treats a missing binary as a
// pass. The shell script this replaced exited 127 when Vector was absent and 1
// on a usage error, so "wrong arguments" and "broken pipeline config" looked
// identical to every caller.

import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

// `new URL(import.meta.url).pathname` yields "/D:/..." on Windows, which Node
// cannot open. fileURLToPath is the portable form.
const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const SKILL_ROOT = path.resolve(SCRIPT_DIR, '..');

const EXIT_CLEAN = 0;
const EXIT_FINDINGS = 1;
const EXIT_CANNOT_RUN = 2;

// Vector reports config problems with EX_CONFIG (78). Any non-zero exit is a
// finding; only a failure to launch the binary is "could not run".
const VECTOR_CANDIDATES = process.platform === 'win32' ? ['vector.exe', 'vector'] : ['vector'];

function usage() {
  console.log(`check-vector-configs.mjs - validate the Vector configs this skill ships.

Usage:
  node scripts/check-vector-configs.mjs [options] [config.yaml ...]

Options:
  --self-test        Run the committed red/green fixtures in assets/fixtures/
                     and verify this checker reports each one correctly.
  --allow-warnings   Do not treat Vector warnings as findings. Off by default:
                     the "acknowledgements are not supported by this source"
                     warning is a silent-data-loss defect, not noise.
  --help, -h         Show this message.

Exit codes:
  0  clean    1  findings    2  could not run

Why not --no-environment:
  That flag suppresses component checks. Vector 0.57.0's routing-template
  confinement errors and disk-buffer bound errors are component checks, so a
  config with either defect validates CLEAN under --no-environment. The
  fixtures assets/fixtures/red-unconfined-template.yaml and
  red-undersized-disk-buffer.yaml exist to prove this checker does not use it.`);
}

function findVector() {
  for (const bin of VECTOR_CANDIDATES) {
    const probe = spawnSync(bin, ['--version'], { encoding: 'utf8' });
    if (!probe.error) return { bin, version: (probe.stdout || '').trim() };
    if (probe.error.code !== 'ENOENT') {
      return { bin: null, reason: `${bin}: ${probe.error.message}` };
    }
  }
  return { bin: null, reason: 'no `vector` binary on PATH' };
}

// Vector resolves `data_dir` against the real filesystem during component
// checks, so a config declaring /var/lib/vector cannot be checked on a machine
// that has no such directory - and that failure is environmental, not a finding.
// Copy each config to an OS temp directory (never inside the repository) with
// data_dir rewritten, so the component checks actually run everywhere.
function stageConfigs(files, tmpDir) {
  const dataDir = path.join(tmpDir, 'data');
  fs.mkdirSync(dataDir, { recursive: true });
  return files.map((src) => {
    const dest = path.join(tmpDir, path.basename(src));
    let text = fs.readFileSync(src, 'utf8');
    const yamlPath = dataDir.split(path.sep).join('/');
    text = /^data_dir:/m.test(text)
      ? text.replace(/^data_dir:.*$/m, `data_dir: "${yamlPath}"`)
      : `data_dir: "${yamlPath}"\n${text}`;
    fs.writeFileSync(dest, text);
    return dest;
  });
}

function runVector(bin, args) {
  const res = spawnSync(bin, args, { encoding: 'utf8' });
  if (res.error) return { blocked: true, message: res.error.message };
  return {
    blocked: false,
    code: res.status === null ? 1 : res.status,
    output: `${res.stdout || ''}${res.stderr || ''}`.trim(),
  };
}

function checkGroup(bin, group, tmpRoot, denyWarnings) {
  const tmpDir = fs.mkdtempSync(path.join(tmpRoot, 'grp-'));
  const staged = stageConfigs(group.files, tmpDir);
  const results = [];

  const vArgs = ['validate', '--skip-healthchecks'];
  if (denyWarnings) vArgs.push('--deny-warnings');
  const validate = runVector(bin, [...vArgs, ...staged]);
  if (validate.blocked) return { blocked: true, message: validate.message };
  results.push({ label: `validate ${group.name}`, code: validate.code, output: validate.output });

  if (group.unitTests) {
    const test = runVector(bin, ['test', ...staged]);
    if (test.blocked) return { blocked: true, message: test.message };
    // Unlike the `set -e` shell script it replaces, this runs the unit tests
    // even when validation already failed, so one invocation reports both.
    results.push({ label: `test ${group.name}`, code: test.code, output: test.output });
  }
  return { blocked: false, results };
}

function checkVrl(bin, vrlFile, tmpRoot) {
  const tmpDir = fs.mkdtempSync(path.join(tmpRoot, 'vrl-'));
  const input = path.join(tmpDir, 'event.json');
  fs.writeFileSync(input, '{"message":"x"}\n');
  const res = runVector(bin, ['vrl', '-i', input, '-p', vrlFile]);
  if (res.blocked) return { blocked: true, message: res.message };
  return { blocked: false, results: [{ label: `vrl ${path.basename(vrlFile)}`, code: res.code, output: res.output }] };
}

function defaultGroups() {
  const t = (f) => path.join(SKILL_ROOT, 'assets', 'templates', f);
  return [
    // vector-tests.yaml does not define `normalize`; it must be passed together
    // with vector-basic.yaml or it fails as an unknown component.
    { name: 'vector-basic + vector-tests', files: [t('vector-basic.yaml'), t('vector-tests.yaml')], unitTests: true },
    { name: 'vector-clickhouse', files: [t('vector-clickhouse.yaml')], unitTests: false },
  ];
}

function report(results) {
  let findings = 0;
  for (const r of results) {
    if (r.code === 0) {
      console.log(`  OK    ${r.label}`);
    } else {
      findings += 1;
      console.log(`  FAIL  ${r.label}  (vector exit ${r.code})`);
      for (const line of r.output.split('\n')) console.log(`        ${line}`);
    }
  }
  return findings;
}

function selfTest(bin, tmpRoot) {
  const dir = path.join(SKILL_ROOT, 'assets', 'fixtures');
  const expectations = [
    { file: 'green-minimal.yaml', expectFinding: false },
    { file: 'red-e651.yaml', expectFinding: true },
    { file: 'red-unconfined-template.yaml', expectFinding: true },
    { file: 'red-undersized-disk-buffer.yaml', expectFinding: true },
  ];
  console.log('Self-test: every assertion this checker makes must fail on a fixture that violates it.');
  let failures = 0;
  for (const e of expectations) {
    const outcome = checkGroup(bin, { name: e.file, files: [path.join(dir, e.file)], unitTests: false }, tmpRoot, true);
    if (outcome.blocked) return { blocked: true, message: outcome.message };
    const sawFinding = outcome.results.some((r) => r.code !== 0);
    const ok = sawFinding === e.expectFinding;
    if (!ok) failures += 1;
    const want = e.expectFinding ? 'finding' : 'clean';
    const got = sawFinding ? 'finding' : 'clean';
    console.log(`  ${ok ? 'PASS' : 'FAIL'}  ${e.file}: expected ${want}, got ${got}`);
  }
  return { blocked: false, failures };
}

function main() {
  const argv = process.argv.slice(2);
  if (argv.includes('--help') || argv.includes('-h')) { usage(); return EXIT_CLEAN; }
  const wantSelfTest = argv.includes('--self-test');
  const denyWarnings = !argv.includes('--allow-warnings');
  const extra = argv.filter((a) => !a.startsWith('-'));

  const found = findVector();
  if (!found.bin) {
    console.error(`BLOCKED: ${found.reason}.`);
    console.error('Install Vector, or run this where Vector is on PATH. Exiting 2 (could not run), not 0.');
    return EXIT_CANNOT_RUN;
  }
  console.log(`Using ${found.version}`);

  const tmpRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'vector-check-'));
  try {
    if (wantSelfTest) {
      const st = selfTest(found.bin, tmpRoot);
      if (st.blocked) { console.error(`BLOCKED: ${st.message}`); return EXIT_CANNOT_RUN; }
      if (st.failures > 0) { console.error(`Self-test FAILED: ${st.failures} fixture(s) behaved unexpectedly.`); return EXIT_FINDINGS; }
      console.log('Self-test passed: red fixtures are reported, the green fixture is clean.');
      return EXIT_CLEAN;
    }

    const groups = extra.length > 0
      ? [{ name: 'supplied configs', files: extra.map((f) => path.resolve(f)), unitTests: false }]
      : defaultGroups();

    const all = [];
    for (const g of groups) {
      const outcome = checkGroup(found.bin, g, tmpRoot, denyWarnings);
      if (outcome.blocked) { console.error(`BLOCKED: ${outcome.message}`); return EXIT_CANNOT_RUN; }
      all.push(...outcome.results);
    }
    if (extra.length === 0) {
      const vrl = path.join(SKILL_ROOT, 'assets', 'templates', 'common.vrl');
      if (fs.existsSync(vrl)) {
        const outcome = checkVrl(found.bin, vrl, tmpRoot);
        if (outcome.blocked) { console.error(`BLOCKED: ${outcome.message}`); return EXIT_CANNOT_RUN; }
        all.push(...outcome.results);
      }
    }
    const findings = report(all);
    if (findings > 0) { console.error(`${findings} target(s) with findings.`); return EXIT_FINDINGS; }
    console.log('All targets validated clean.');
    return EXIT_CLEAN;
  } finally {
    fs.rmSync(tmpRoot, { recursive: true, force: true });
  }
}

try {
  process.exit(main());
} catch (err) {
  console.error(`BLOCKED: checker failed: ${err && err.stack ? err.stack : err}`);
  process.exit(EXIT_CANNOT_RUN);
}
