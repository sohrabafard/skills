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

const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const SKILL_ROOT = path.resolve(SCRIPT_DIR, '..');

const EXIT_CLEAN = 0;
const EXIT_FINDINGS = 1;
const EXIT_CANNOT_RUN = 2;

// Vector reports config problems with EX_CONFIG (78). Any non-zero exit is a
// finding; only a failure to launch the binary is "could not run".
const VECTOR_CANDIDATES = ['vector'];

function usage() {
  console.log(`check-vector-configs.mjs - validate the Vector configs this skill ships.

Supply only trusted configs whose secret backends you are authorized to use.
Vector 0.59+ resolves those backends even when health checks are skipped.
Staging rewrites data_dir and leaves supplied backends active. Only the
bundled ClickHouse example uses a staged synthetic secret file.

Usage:
  node scripts/check-vector-configs.mjs [options] [config.yaml ...]

Options:
  --allow-warnings   Do not treat Vector warnings as findings. Off by default:
                     the "acknowledgements are not supported by this source"
                     warning is a silent-data-loss defect, not noise.
  --help, -h         Show this message.

Exit codes:
  0  clean    1  findings    2  could not run

Why not --no-environment:
  That flag suppresses component checks. Vector 0.57.0's routing-template
  confinement errors and disk-buffer bound errors are component checks, so a
  config with either defect validates CLEAN under --no-environment. Vector
  0.58.0 fixes confinement detection under --no-environment, but that flag still
  skips other component checks and never replaces this strict gate.`);
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
function stageConfigs({ files, fixtureSecret }, tmpDir) {
  const dataDir = path.join(tmpDir, 'data');
  fs.mkdirSync(dataDir, { recursive: true });
  return files.map((src) => {
    const configDir = fs.mkdtempSync(path.join(tmpDir, 'config-'));
    const dest = path.join(configDir, path.basename(src));
    let text = fs.readFileSync(src, 'utf8');
    const yamlPath = dataDir;
    text = /^data_dir:/m.test(text)
      ? text.replace(/^data_dir:.*$/m, `data_dir: "${yamlPath}"`)
      : `data_dir: "${yamlPath}"\n${text}`;
    if (fixtureSecret) {
      const templatePath = '    path: /run/secrets/vector-clickhouse.json';
      if (!text.split(/\r?\n/).includes(templatePath)) {
        throw new Error('Bundled ClickHouse secret path changed; update the fixture binding');
      }
      const fixturePath = path.join(tmpDir, 'clickhouse-secret.json');
      fs.writeFileSync(fixturePath, JSON.stringify({ user: 'fixture', password: 'fixture' }));
      text = text.replace(templatePath, `    path: ${JSON.stringify(fixturePath)}`);
    }
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
  const staged = stageConfigs(group, tmpDir);
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
    { name: 'vector-clickhouse', files: [t('vector-clickhouse.yaml')], unitTests: false, fixtureSecret: true },
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

function main() {
  const argv = process.argv.slice(2);
  if (argv.includes('--help') || argv.includes('-h')) { usage(); return EXIT_CLEAN; }
  const denyWarnings = !argv.includes('--allow-warnings');
  const extra = argv.filter((a) => !a.startsWith('-'));

  const vrl = extra.length === 0 ? path.join(SKILL_ROOT, 'assets', 'templates', 'common.vrl') : null;
  if (vrl && !fs.statSync(vrl, { throwIfNoEntry: false })?.isFile()) {
    console.error('BLOCKED: bundled assets/templates/common.vrl is missing or is not a file.');
    return EXIT_CANNOT_RUN;
  }

  const found = findVector();
  if (!found.bin) {
    console.error(`BLOCKED: ${found.reason}.`);
    console.error('Run where an approved Vector binary is already on PATH. Exiting 2 (could not run), not 0.');
    return EXIT_CANNOT_RUN;
  }
  console.log(`Using ${found.version}`);

  const tmpRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'vector-check-'));
  try {
    const groups = extra.length > 0
      ? [{ name: 'supplied configs', files: extra.map((f) => path.resolve(f)), unitTests: false }]
      : defaultGroups();

    const all = [];
    for (const g of groups) {
      const outcome = checkGroup(found.bin, g, tmpRoot, denyWarnings);
      if (outcome.blocked) { console.error(`BLOCKED: ${outcome.message}`); return EXIT_CANNOT_RUN; }
      all.push(...outcome.results);
    }
    if (vrl) {
      const outcome = checkVrl(found.bin, vrl, tmpRoot);
      if (outcome.blocked) { console.error(`BLOCKED: ${outcome.message}`); return EXIT_CANNOT_RUN; }
      all.push(...outcome.results);
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
