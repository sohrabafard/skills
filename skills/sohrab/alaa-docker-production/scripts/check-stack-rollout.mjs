#!/usr/bin/env node
// check-stack-rollout.mjs — rollout control on a Swarm stack file.
//
// Enforces `alaa-docker-production references/30-swarm-delivery.md`.
//
// The defect this exists to stop: `docker stack deploy` applies its own defaults when a service
// omits `deploy.update_config`, and those defaults are parallelism 1, `order: stop-first`,
// `failure_action: pause`, `monitor: 0s`. With no `replicas` key the default is one task. One
// task, stopped before its replacement starts, is a full outage of that service on every single
// deployment — and `failure_action: pause` means a bad image leaves the stack half-updated with
// no alarm. Defaults confirmed 2026-07-29 at https://docs.docker.com/reference/compose-file/deploy/

import path from 'node:path';
import {
  CannotRun,
  EXIT_CANNOT_RUN,
  EXIT_CLEAN,
  EXIT_FINDINGS,
  collectTargets,
  expect,
  finding,
  fixturesDir,
  readLines,
  reportFindings,
  run,
} from './lib/common.mjs';
import { lineOf, parseComposeFile } from './lib/mini-yaml.mjs';

const HELP = `Usage:
  node check-stack-rollout.mjs [options] <stack-file-or-directory>...

Description:
  Assert that every long-lived service in a Swarm stack file carries the rollout control a
  zero-downtime deployment needs. A one-shot job service is exempt from the rollout rules and is
  detected by name, by \`deploy.mode\` ending in \`-job\`, or by \`restart_policy.condition: none\`.

Rules:
  no-update-config             \`deploy.update_config\` is absent, so Swarm uses order: stop-first,
                               parallelism 1, failure_action: pause.
  update-order-stop-first      \`update_config.order\` is not \`start-first\`.
  update-failure-action        \`update_config.failure_action\` is not \`rollback\`.
  update-monitor-missing       \`update_config.monitor\` is absent or 0s, so a task that dies one
                               second after starting counts as a successful update.
  no-rollback-config           \`deploy.rollback_config\` is absent, so a rollback inherits the
                               stop-first default that the update was configured to avoid.
  no-replicas                  \`deploy.replicas\` is absent, so the service runs one task and
                               start-first cannot help it.
  healthcheck-missing          No \`healthcheck\`. A health-gated rollout without one is a timer:
                               Swarm marks the new task converged as soon as it is running.
  healthcheck-disabled         \`healthcheck.test: ["NONE"]\`, which also disables any probe
                               inherited from the image.
  resources-reservations-missing  \`deploy.resources.reservations\` is absent, so the scheduler can
                               place a task on a node that cannot actually run it.
  restart-policy-no-delay      \`restart_policy\` has no \`delay\`, so a crash-looping task restarts
                               as fast as the node can fork it.
  stop-grace-period-missing    A queue-worker service with no \`stop_grace_period\`, so SIGKILL
                               arrives 10s after SIGTERM and kills the job in flight.
  secret-mode-missing          A long-form \`secrets:\` entry with no \`mode\`, so the secret lands
                               world-readable at 0444 inside the container.

  A rule is waived for one service only by a comment anywhere in the file:
    # rollout-waiver: <service> <rule-id> reason=<one line saying why this shape is correct here>
  A waiver with no reason= text is itself a finding (waiver-without-reason). The intended use is a
  deliberate singleton — a scheduler whose second replica would run every due job twice — where
  stop-first and one replica are the correct choice and the cost is bounded and stated.

Options:
  --one-shot NAME[,NAME...]  Additional service names to treat as one-shot jobs.
  --quiet                    Print nothing; use the exit code only.
  --self-test                Run against the fixtures shipped beside this script and exit 0.
  -h, --help                 Show this help and exit 0.

Exit codes:
  0  clean, or --help / --self-test succeeded
  1  at least one finding
  2  could not run: a path that does not exist, a YAML construct this checker refuses to guess at,
     or a file with no top-level \`services:\` mapping
`;

const STACK_NAME = /^(docker-)?compose.*swarm.*\.ya?ml$|^stack.*\.ya?ml$|.*\.stack\.ya?ml$/i;
const ONE_SHOT_NAME = /(provision|migrate|migration|bootstrap|seed|setup|composer|vendor-sync|init)/i;
const WORKER_NAME = /(worker|horizon|consumer)/i;
const WORKER_COMMAND = /(queue:work|rabbitmq:consume|horizon|queue:listen)/i;

function main(argv) {
  if (argv.includes('-h') || argv.includes('--help')) {
    process.stdout.write(HELP);
    return EXIT_CLEAN;
  }
  if (argv.includes('--self-test')) return selfTest();

  const quiet = argv.includes('--quiet');
  let extraOneShot = [];
  const targets = [];
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === '--quiet') continue;
    if (arg === '--one-shot') {
      const value = argv[++i];
      if (!value) throw new CannotRun('--one-shot requires a comma-separated list of service names');
      extraOneShot = value.split(',').map((s) => s.trim()).filter(Boolean);
      continue;
    }
    if (arg.startsWith('--')) throw new CannotRun(`unknown option: ${arg}`);
    targets.push(arg);
  }
  if (targets.length === 0) throw new CannotRun('no input path given; pass a stack file or a directory');

  const files = collectTargets(targets, (name) => STACK_NAME.test(name));
  const findings = [];
  for (const file of files) findings.push(...checkStack(file, extraOneShot));
  return reportFindings(findings, { quiet });
}

export function checkStack(file, extraOneShot = []) {
  const { waivers, waiverFindings } = readWaivers(file);
  const doc = parseComposeFile(file);
  if (!doc || typeof doc !== 'object' || Array.isArray(doc)) {
    throw new CannotRun(`${file}: top level is not a mapping`);
  }
  const services = doc.services;
  if (!services || typeof services !== 'object' || Array.isArray(services)) {
    throw new CannotRun(`${file}: no top-level "services:" mapping; this is not a stack file`);
  }

  const findings = [...waiverFindings];
  for (const name of Object.keys(services)) {
    const svc = services[name] || {};
    const at = (key) => lineOf(svc, key) || lineOf(services, name);
    const deploy = svc.deploy && typeof svc.deploy === 'object' ? svc.deploy : null;

    findings.push(...checkSecrets(file, name, svc));

    const oneShot =
      extraOneShot.includes(name) ||
      ONE_SHOT_NAME.test(name) ||
      (deploy && typeof deploy.mode === 'string' && deploy.mode.endsWith('-job')) ||
      (deploy && deploy.restart_policy && deploy.restart_policy.condition === 'none');
    if (oneShot) continue;

    // healthcheck
    const hc = svc.healthcheck;
    if (!hc) {
      findings.push(finding(file, at('image'), 'healthcheck-missing',
        `service "${name}" has no healthcheck; a rollout cannot be gated on health it never measures`));
    } else if (Array.isArray(hc.test) && hc.test.length === 1 && hc.test[0] === 'NONE') {
      findings.push(finding(file, lineOf(hc, 'test'), 'healthcheck-disabled',
        `service "${name}" sets healthcheck test ["NONE"], which also disables the probe inherited from the image`));
    } else if (hc.test === 'NONE') {
      findings.push(finding(file, lineOf(hc, 'test'), 'healthcheck-disabled',
        `service "${name}" sets healthcheck test NONE`));
    }

    if (!deploy) {
      findings.push(finding(file, at('image'), 'no-update-config',
        `service "${name}" has no deploy block at all, so every Swarm rollout default applies`));
      findings.push(finding(file, at('image'), 'no-rollback-config',
        `service "${name}" has no deploy.rollback_config`));
      findings.push(finding(file, at('image'), 'no-replicas',
        `service "${name}" has no deploy.replicas, so it runs exactly one task`));
      findings.push(finding(file, at('image'), 'resources-reservations-missing',
        `service "${name}" declares no deploy.resources.reservations`));
      continue;
    }

    const dline = (key) => lineOf(deploy, key) || lineOf(svc, 'deploy');

    const uc = deploy.update_config;
    if (!uc || typeof uc !== 'object') {
      findings.push(finding(file, dline('update_config'), 'no-update-config',
        `service "${name}" has no deploy.update_config, so stack deploy uses order: stop-first, parallelism 1, failure_action: pause`));
    } else {
      if (uc.order !== 'start-first') {
        findings.push(finding(file, lineOf(uc, 'order'), 'update-order-stop-first',
          `service "${name}" update_config.order is "${uc.order ?? 'unset'}"; a single-replica stop-first update is a full outage`));
      }
      if (uc.failure_action !== 'rollback') {
        findings.push(finding(file, lineOf(uc, 'failure_action'), 'update-failure-action',
          `service "${name}" update_config.failure_action is "${uc.failure_action ?? 'unset'}"; pause leaves the stack half-updated with no alarm`));
      }
      if (!uc.monitor || /^0(s|ms)?$/.test(String(uc.monitor))) {
        findings.push(finding(file, lineOf(uc, 'monitor'), 'update-monitor-missing',
          `service "${name}" update_config.monitor is "${uc.monitor ?? 'unset'}"; without a monitor window a task that dies on its first request counts as a successful update`));
      }
    }

    if (!deploy.rollback_config || typeof deploy.rollback_config !== 'object') {
      findings.push(finding(file, dline('rollback_config'), 'no-rollback-config',
        `service "${name}" has no deploy.rollback_config, so an automatic rollback runs stop-first`));
    }

    const global = deploy.mode === 'global';
    if (!global && deploy.replicas === undefined) {
      findings.push(finding(file, dline('replicas'), 'no-replicas',
        `service "${name}" has no deploy.replicas, so it runs exactly one task and order: start-first cannot protect it`));
    }

    const reservations = deploy.resources && deploy.resources.reservations;
    if (!reservations) {
      findings.push(finding(file, dline('resources'), 'resources-reservations-missing',
        `service "${name}" declares deploy.resources limits without reservations, so the scheduler can place it on a node that cannot run it`));
    }

    const rp = deploy.restart_policy;
    if (rp && typeof rp === 'object' && rp.delay === undefined) {
      findings.push(finding(file, lineOf(rp, 'condition'), 'restart-policy-no-delay',
        `service "${name}" restart_policy has no delay; a task that exits on start restarts as fast as the node can fork it`));
    }

    const command = Array.isArray(svc.command) ? svc.command.join(' ') : String(svc.command || '');
    const isWorker = WORKER_NAME.test(name) || WORKER_COMMAND.test(command);
    if (isWorker && svc.stop_grace_period === undefined) {
      findings.push(finding(file, at('command'), 'stop-grace-period-missing',
        `service "${name}" runs a queue worker with no stop_grace_period; SIGKILL arrives 10s after SIGTERM and kills the job in flight`));
    }
  }
  return findings.filter((f) => !waivers.has(`${serviceOf(f)}|${f.rule}`));
}

/** The service a finding belongs to, taken from the quoted name in its message. */
function serviceOf(f) {
  const m = /service "([^"]+)"/.exec(f.message);
  return m ? m[1] : '';
}

/** Waivers are read from the raw file, because YAML parsing drops comments. */
function readWaivers(file) {
  const waivers = new Set();
  const waiverFindings = [];
  readLines(file).forEach((line, idx) => {
    const m = /#\s*rollout-waiver:\s*(\S+)\s+(\S+)\s*(.*)$/.exec(line);
    if (!m) return;
    const reason = /reason=(.+)$/.exec(m[3] || '');
    if (!reason || reason[1].trim() === '') {
      waiverFindings.push(finding(file, idx + 1, 'waiver-without-reason',
        `waiver for ${m[1]} ${m[2]} states no reason=; a waiver with no argument is a silenced rule, not an accepted one`));
      return;
    }
    waivers.add(`${m[1]}|${m[2]}`);
  });
  return { waivers, waiverFindings };
}

function checkSecrets(file, name, svc) {
  const out = [];
  if (!Array.isArray(svc.secrets)) return out;
  for (const entry of svc.secrets) {
    if (typeof entry === 'string') continue; // short form; mode cannot be expressed, see references/35-
    if (entry && typeof entry === 'object' && entry.mode === undefined) {
      out.push(finding(file, lineOf(entry, 'source'), 'secret-mode-missing',
        `service "${name}" mounts secret "${entry.source ?? '?'}" with no mode, so it lands at the 0444 default and every process in the container can read it`));
    }
  }
  return out;
}

function selfTest() {
  process.stdout.write('check-stack-rollout --self-test\n');
  const dir = path.join(fixturesDir(), 'swarm');

  const clean = checkStack(path.join(dir, 'clean.stack.yml'));
  expect(clean.length, 0, 'compliant stack produces no finding');

  const kit = checkStack(path.join(dir, 'kit-rendered.stack.yml'));
  const byRule = {};
  for (const f of kit) byRule[f.rule] = (byRule[f.rule] || 0) + 1;
  expect(byRule['no-update-config'] || 0, 4, 'generated stack: services with no update_config');
  expect(byRule['no-rollback-config'] || 0, 4, 'generated stack: services with no rollback_config');
  expect(byRule['no-replicas'] || 0, 4, 'generated stack: services with no replicas');
  expect(byRule['healthcheck-missing'] || 0, 3, 'generated stack: services with no healthcheck');
  expect(byRule['healthcheck-disabled'] || 0, 1, 'generated stack: services with test ["NONE"]');
  expect(byRule['resources-reservations-missing'] || 0, 4, 'generated stack: services with no reservations');
  expect(byRule['restart-policy-no-delay'] || 0, 4, 'generated stack: restart policies with no delay');
  expect(byRule['stop-grace-period-missing'] || 0, 1, 'generated stack: workers with no stop_grace_period');
  expect(kit.filter((f) => f.message.includes('"platform-app-php"')).length, 6, 'findings on the app service alone');

  const partial = checkStack(path.join(dir, 'partial.stack.yml'));
  const partialByRule = {};
  for (const f of partial) partialByRule[f.rule] = (partialByRule[f.rule] || 0) + 1;
  expect(partialByRule['update-order-stop-first'] || 0, 1, 'update_config present but order is stop-first');
  expect(partialByRule['update-failure-action'] || 0, 1, 'update_config present but failure_action is pause');
  expect(partialByRule['update-monitor-missing'] || 0, 1, 'update_config present but monitor is unset');
  expect(partialByRule['secret-mode-missing'] || 0, 1, 'secret mounted with no mode');

  let cannotRun = 0;
  try {
    checkStack(path.join(dir, 'not-a-stack.yml'));
  } catch (err) {
    if (err instanceof CannotRun) cannotRun = EXIT_CANNOT_RUN;
  }
  expect(cannotRun, EXIT_CANNOT_RUN, 'a file with no services: mapping raises CannotRun (exit 2)');

  let anchorRefused = 0;
  try {
    checkStack(path.join(dir, 'anchors.stack.yml'));
  } catch (err) {
    if (err instanceof CannotRun) anchorRefused = EXIT_CANNOT_RUN;
  }
  expect(anchorRefused, EXIT_CANNOT_RUN, 'a YAML anchor is refused rather than misparsed (exit 2)');

  expect(reportFindings(kit, { quiet: true }), EXIT_FINDINGS, 'findings map to exit 1');
  expect(reportFindings([], { quiet: true }), EXIT_CLEAN, 'no findings maps to exit 0');

  process.stdout.write('self-test passed\n');
  return EXIT_CLEAN;
}

run(main);
