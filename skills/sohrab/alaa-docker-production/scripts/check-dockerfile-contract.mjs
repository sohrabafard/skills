#!/usr/bin/env node
// check-dockerfile-contract.mjs — the Dockerfile authorship contract.
//
// Enforces `alaa-docker-production references/10-dockerfile-authorship.md`. Every rule id below
// appears beside its paragraph in that file, so a finding leads to the sentence that explains it.
//
// This skill is the sole owner of the Dockerfile for every service in the fleet:
// `service-runtime-kit` generates a `build:` stanza that references a Dockerfile and generates no
// Dockerfile (`service-runtime-kit/README.md:182`). Nothing else checks these files.

import path from 'node:path';
import fs from 'node:fs';
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

const HELP = `Usage:
  node check-dockerfile-contract.mjs [options] <dockerfile-or-directory>...

Description:
  Assert the authorship contract every production Dockerfile in this fleet must satisfy. Nine
  rules, each of which corresponds to a defect that has reached production somewhere.

Rules:
  syntax-directive            Line 1 is \`# syntax=docker/dockerfile:1\`. Without it the build uses
                              whatever frontend the daemon has, so \`RUN --mount\`, heredocs and
                              build checks are available on one machine and not another.
  single-stage                Fewer than two \`FROM\` instructions. Waive with a comment
                              \`# single-stage-exempt: <reason>\`.
  base-image-floating         A \`FROM\` whose tag is \`latest\`, absent, or a bare major.
  final-stage-root            The final stage does not set \`USER\` to a non-root name or UID, or
                              sets it back to root or 0.
  final-stage-build-tooling   A package-manager install, compiler or dependency install runs in
                              the final stage. Permitted only when the same RUN removes it again
                              (\`apk del\`, \`apt-get purge\`).
  context-copy-before-install \`COPY . .\` or \`ADD . .\` appears before the dependency-install RUN in
                              the same stage, so every source edit invalidates the install layer.
  missing-oci-revision-label  No \`LABEL org.opencontainers.image.revision\`. Without it a running
                              container cannot be traced to a commit.
  missing-healthcheck         No \`HEALTHCHECK\` and no \`# healthcheck-exempt: <reason>\` comment.
  dockerignore-missing        No \`.dockerignore\` beside the Dockerfile.
  dockerignore-incomplete     The \`.dockerignore\` does not exclude one of the required entries.

Options:
  --require-ignore A,B,C  Comma-separated .dockerignore entries to require.
                          Default: .git,.env,node_modules,vendor,docker/.local-secrets
  --quiet                 Print nothing; use the exit code only.
  --self-test             Run against the fixtures shipped beside this script and exit 0.
  -h, --help              Show this help and exit 0.

Exit codes:
  0  clean, or --help / --self-test succeeded
  1  at least one finding
  2  could not run: a path that does not exist, an unreadable file, an input set that matched no
     files, or a file with no FROM instruction (which is not a Dockerfile)
`;

const DEFAULT_REQUIRED_IGNORES = ['.git', '.env', 'node_modules', 'vendor', 'docker/.local-secrets'];

const DOCKERFILE_NAME = /^Dockerfile(\..+)?$/i;

const INSTALL_PATTERNS = [
  /\bapt-get\s+(-[^\s]+\s+)*install\b/,
  /\bapt\s+(-[^\s]+\s+)*install\b/,
  /\bapk\s+add\b/,
  /\b(dnf|yum|microdnf|zypper)\s+(-[^\s]+\s+)*install\b/,
  /\bpip3?\s+install\b/,
  /\bnpm\s+(install|ci)\b/,
  /\byarn\s+(install|add)\b/,
  /\bpnpm\s+(install|add)\b/,
  /\bcomposer\s+(install|require|update)\b/,
  /\bgo\s+build\b/,
  /\bcargo\s+build\b/,
  /\b(mvn|gradle)\s+/,
  /\bpecl\s+install\b/,
  /\bdocker-php-ext-install\b/,
];

const REMOVAL_PATTERNS = [/\bapk\s+del\b/, /\bapt-get\s+purge\b/, /\bapt-get\s+remove\b/, /\bpecl\s+uninstall\b/];

function main(argv) {
  if (argv.includes('-h') || argv.includes('--help')) {
    process.stdout.write(HELP);
    return EXIT_CLEAN;
  }
  if (argv.includes('--self-test')) return selfTest();

  const quiet = argv.includes('--quiet');
  let required = DEFAULT_REQUIRED_IGNORES;
  const targets = [];
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === '--quiet') continue;
    if (arg === '--require-ignore') {
      const value = argv[++i];
      if (!value) throw new CannotRun('--require-ignore requires a comma-separated list');
      required = value.split(',').map((s) => s.trim()).filter(Boolean);
      continue;
    }
    if (arg.startsWith('--')) throw new CannotRun(`unknown option: ${arg}`);
    targets.push(arg);
  }
  if (targets.length === 0) throw new CannotRun('no input path given; pass a Dockerfile or a directory');

  const files = collectTargets(targets, (name) => DOCKERFILE_NAME.test(name));
  const findings = [];
  for (const file of files) findings.push(...checkDockerfile(file, required));
  return reportFindings(findings, { quiet });
}

export function checkDockerfile(file, required = DEFAULT_REQUIRED_IGNORES) {
  const lines = readLines(file);
  const findings = [];
  const instructions = parseInstructions(lines);
  const froms = instructions.filter((ins) => ins.op === 'FROM');
  if (froms.length === 0) {
    throw new CannotRun(`${file}: no FROM instruction; this is not a Dockerfile`);
  }

  // syntax-directive
  const firstMeaningful = lines.findIndex((l) => l.trim() !== '');
  const first = firstMeaningful === -1 ? '' : lines[firstMeaningful];
  if (!/^#\s*syntax\s*=\s*\S+/.test(first)) {
    findings.push(finding(file, firstMeaningful + 1 || 1, 'syntax-directive',
      'line 1 is not a syntax directive; write `# syntax=docker/dockerfile:1` as the very first line'));
  } else if (!/docker\/dockerfile:\d/.test(first)) {
    findings.push(finding(file, firstMeaningful + 1, 'syntax-directive',
      `syntax directive does not pin a major frontend version: ${first.trim()}`));
  }

  // single-stage
  const exemptSingle = lines.some((l) => /#\s*single-stage-exempt:\s*\S/.test(l));
  if (froms.length < 2 && !exemptSingle) {
    findings.push(finding(file, froms[0].line, 'single-stage',
      'only one FROM; separate the build stage from the runtime stage, or add `# single-stage-exempt: <reason>`'));
  }

  // base-image-floating
  for (const from of froms) {
    const ref = from.args.split(/\s+/).filter((t) => !t.startsWith('--'))[0] || '';
    if (ref.startsWith('$')) continue; // resolved from a build arg; check-image-pinning owns the default
    const nameAndTag = ref.split('@')[0];
    if (ref.includes('@sha256:')) continue;
    const tag = nameAndTag.includes(':') ? nameAndTag.slice(nameAndTag.lastIndexOf(':') + 1) : '';
    if (tag === '') {
      findings.push(finding(file, from.line, 'base-image-floating', `FROM ${ref} has no tag, so it resolves to :latest`));
    } else if (tag === 'latest') {
      findings.push(finding(file, from.line, 'base-image-floating', `FROM ${ref} pins :latest`));
    } else if (/^\d+$/.test(tag)) {
      findings.push(finding(file, from.line, 'base-image-floating',
        `FROM ${ref} pins a bare major; a bare major moves under you on every upstream minor release`));
    }
  }

  // Stage partition. The final stage is everything after the last FROM.
  const lastFromIndex = instructions.lastIndexOf(froms[froms.length - 1]);
  const finalStage = instructions.slice(lastFromIndex);

  // final-stage-root
  const users = finalStage.filter((ins) => ins.op === 'USER');
  const lastUser = users.length ? users[users.length - 1] : null;
  if (!lastUser) {
    findings.push(finding(file, froms[froms.length - 1].line, 'final-stage-root',
      'the final stage sets no USER, so the container runs as root'));
  } else if (/^(root|0)\b/.test(lastUser.args.trim())) {
    findings.push(finding(file, lastUser.line, 'final-stage-root',
      `the final stage ends as USER ${lastUser.args.trim()}; set a non-root user or UID`));
  }

  // final-stage-build-tooling
  for (const ins of finalStage) {
    if (ins.op !== 'RUN') continue;
    const body = ins.args;
    const installs = INSTALL_PATTERNS.some((re) => re.test(body));
    if (!installs) continue;
    if (REMOVAL_PATTERNS.some((re) => re.test(body))) continue;
    findings.push(finding(file, ins.line, 'final-stage-build-tooling',
      'the final stage installs packages or dependencies; do that in a build stage and COPY --from, or remove the tooling in the same RUN'));
  }

  // context-copy-before-install, evaluated per stage
  let stageStart = 0;
  for (let i = 0; i < instructions.length; i++) {
    if (instructions[i].op === 'FROM' && i !== stageStart) {
      checkStageCopyOrder(instructions.slice(stageStart, i), file, findings);
      stageStart = i;
    }
  }
  checkStageCopyOrder(instructions.slice(stageStart), file, findings);

  // missing-oci-revision-label
  const hasRevision = instructions.some(
    (ins) => ins.op === 'LABEL' && /org\.opencontainers\.image\.revision/.test(ins.args)
  );
  if (!hasRevision) {
    findings.push(finding(file, froms[froms.length - 1].line, 'missing-oci-revision-label',
      'no LABEL org.opencontainers.image.revision; a running container cannot be traced back to a commit'));
  }

  // missing-healthcheck
  const hasHealthcheck = finalStage.some((ins) => ins.op === 'HEALTHCHECK');
  const healthExempt = lines.some((l) => /#\s*healthcheck-exempt:\s*\S/.test(l));
  if (!hasHealthcheck && !healthExempt) {
    findings.push(finding(file, froms[froms.length - 1].line, 'missing-healthcheck',
      'the final stage has no HEALTHCHECK and no `# healthcheck-exempt: <reason>` comment'));
  }

  // .dockerignore
  const ignorePath = path.join(path.dirname(file), '.dockerignore');
  if (!fs.existsSync(ignorePath)) {
    findings.push(finding(file, 1, 'dockerignore-missing',
      `no .dockerignore at ${ignorePath}; the whole working tree is uploaded as build context`));
  } else {
    const entries = readLines(ignorePath)
      .map((l) => l.trim())
      .filter((l) => l !== '' && !l.startsWith('#'));
    for (const want of required) {
      const covered = entries.some((e) => e === want || e === `${want}/` || e === `**/${want}` || e === `${want}/**`);
      if (!covered) {
        findings.push(finding(ignorePath, 1, 'dockerignore-incomplete',
          `.dockerignore does not exclude "${want}"`));
      }
    }
  }

  return findings;
}

function checkStageCopyOrder(stage, file, findings) {
  let firstInstallLine = null;
  for (const ins of stage) {
    if (ins.op === 'RUN' && INSTALL_PATTERNS.some((re) => re.test(ins.args))) {
      firstInstallLine = ins.line;
      break;
    }
  }
  if (firstInstallLine === null) return;
  for (const ins of stage) {
    if (ins.line >= firstInstallLine) break;
    if (ins.op !== 'COPY' && ins.op !== 'ADD') continue;
    const operands = ins.args.split(/\s+/).filter((t) => !t.startsWith('--'));
    if (operands.length < 2) continue;
    const sources = operands.slice(0, -1);
    if (sources.some((s) => s === '.' || s === './' || s === '*')) {
      findings.push(finding(file, ins.line, 'context-copy-before-install',
        `${ins.op} copies the whole context before the dependency install on line ${firstInstallLine}; every source edit then invalidates the install layer`));
    }
  }
}

/** Join continuation lines so a multi-line RUN is one instruction with the line it started on. */
function parseInstructions(lines) {
  const out = [];
  let i = 0;
  while (i < lines.length) {
    const startLine = i + 1;
    let text = lines[i];
    if (/^\s*(#|$)/.test(text)) { i++; continue; }
    while (/\\\s*$/.test(text) && i + 1 < lines.length) {
      i++;
      const next = lines[i];
      if (/^\s*#/.test(next)) continue; // a comment inside a continuation is dropped by BuildKit
      text = `${text.replace(/\\\s*$/, '')} ${next.trim()}`;
    }
    const m = /^\s*([A-Za-z]+)\s+([\s\S]*)$/.exec(text);
    if (m) out.push({ op: m[1].toUpperCase(), args: m[2].trim(), line: startLine });
    i++;
  }
  return out;
}

function selfTest() {
  process.stdout.write('check-dockerfile-contract --self-test\n');
  const dir = path.join(fixturesDir(), 'dockerfile');

  const good = checkDockerfile(path.join(dir, 'good', 'Dockerfile'));
  expect(good.length, 0, 'compliant fixture produces no finding');

  const bad = checkDockerfile(path.join(dir, 'bad', 'Dockerfile'));
  const byRule = {};
  for (const f of bad) byRule[f.rule] = (byRule[f.rule] || 0) + 1;
  expect(byRule['syntax-directive'] || 0, 1, 'missing syntax directive');
  expect(byRule['single-stage'] || 0, 1, 'single-stage build');
  expect(byRule['base-image-floating'] || 0, 1, 'floating base image');
  expect(byRule['final-stage-root'] || 0, 1, 'final stage runs as root');
  expect(byRule['final-stage-build-tooling'] || 0, 1, 'build tooling in the final stage');
  expect(byRule['context-copy-before-install'] || 0, 1, 'whole-context COPY before install');
  expect(byRule['missing-oci-revision-label'] || 0, 1, 'missing OCI revision label');
  expect(byRule['missing-healthcheck'] || 0, 1, 'missing healthcheck');
  expect(byRule['dockerignore-incomplete'] || 0, 2, 'incomplete .dockerignore');

  let cannotRun = 0;
  try {
    checkDockerfile(path.join(dir, 'bad', '.dockerignore'));
  } catch (err) {
    if (err instanceof CannotRun) cannotRun = EXIT_CANNOT_RUN;
  }
  expect(cannotRun, EXIT_CANNOT_RUN, 'a file with no FROM raises CannotRun (exit 2)');

  expect(reportFindings(bad, { quiet: true }), EXIT_FINDINGS, 'findings map to exit 1');
  expect(reportFindings([], { quiet: true }), EXIT_CLEAN, 'no findings maps to exit 0');

  process.stdout.write('self-test passed\n');
  return EXIT_CLEAN;
}

run(main);
