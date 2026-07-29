#!/usr/bin/env node
// check-image-pinning.mjs — image reference determinism, and the freshness check.
//
// Enforces `alaa-docker-production references/45-registry-and-mirrors.md`.
//
// Two jobs. First, every image reference in a production-shaped file resolves to something that
// does not move: not `latest`, not a bare major, and — inside a `${VAR:-default}` — a default that
// is itself compliant, which is the case today's tooling passes. Second, `--versions` prints the
// pinned upstream lines this skill states, each with the command or URL that re-derives it, and
// `image-eol-line` reports an image built on a line that is out of support. A version written into
// a file goes stale silently; a version the checker knows about goes stale loudly.

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

const HELP = `Usage:
  node check-image-pinning.mjs [options] <file-or-directory>...

Description:
  Assert that every image reference in a Compose or Swarm stack file resolves to a fixed artifact,
  and that no image is built on an upstream line that has left support.

Rules:
  image-floating-latest  The reference resolves to \`:latest\` or carries no tag at all.
  image-bare-major       The tag is a bare major (\`postgres:18\`), which moves on every upstream
                         minor release without any change in this repository.
  image-default-floating The reference is \`\${VAR:-default}\` and the default is floating. The
                         variable being set in one environment does not make the file correct: the
                         default is what a Swarm manager with a clean environment will deploy.
  image-no-digest        Only with --release. A release manifest pins by digest, because a tag is
                         a mutable pointer and a rebuild under the same tag is undetectable.
  image-eol-line         The image is built on a language or distribution line that is out of
                         support as of the date in --versions. Security patches stop arriving and
                         no scanner finding will ever be fixable.
  image-not-mirrored     Only with --mirror-var. A public upstream image is written as a literal
                         instead of being routed through the mirror variable, so the mirror that
                         governs the application base image does not govern this one.

Options:
  --release              Also require a digest on every image.
  --mirror-var NAME      Require public upstream images to be prefixed with \${NAME:-...}.
  --private-host HOST[,HOST...]  Registry hosts that are first-party and exempt from --mirror-var.
  --versions             Print the pinned upstream lines with the command or URL that re-derives
                         each one, and exit 0.
  --quiet                Print nothing; use the exit code only.
  --self-test            Run against the fixtures shipped beside this script and exit 0.
  -h, --help             Show this help and exit 0.

Exit codes:
  0  clean, or --help / --versions / --self-test succeeded
  1  at least one finding
  2  could not run: a path that does not exist, an unreadable file, or an input set that matched
     no files
`;

// Every row was verified on 2026-07-29 against the source named in `source`. `recheck` is the one
// command or URL that re-derives the value, so a later wave checks rather than trusts.
export const VERSION_REGISTER = {
  verified: '2026-07-29',
  rows: [
    {
      subject: 'Docker Engine',
      value: '29.6.2 (16 July 2026)',
      source: 'https://docs.docker.com/engine/release-notes/29/',
      recheck: 'docker version --format "{{.Server.Version}}" ; https://docs.docker.com/engine/release-notes/29/',
    },
    {
      subject: 'Docker Compose',
      value: 'v5.3.1 (7 July 2026); v5.3.0 added native init containers',
      source: 'https://github.com/docker/compose/releases',
      recheck: 'docker compose version ; https://github.com/docker/compose/releases',
    },
    {
      subject: 'Dockerfile frontend',
      value: 'docker/dockerfile:1 — pins the stable major and fetches the newest syntax per build',
      source: 'https://docs.docker.com/reference/dockerfile/',
      recheck: 'docker buildx build --print=outline . ; https://hub.docker.com/r/docker/dockerfile/tags',
    },
    {
      subject: 'Build provenance default',
      value: 'provenance mode=min is added by default; --provenance=mode=max, --provenance=false, BUILDX_NO_DEFAULT_ATTESTATIONS',
      source: 'https://docs.docker.com/build/metadata/attestations/',
      recheck: 'docker buildx imagetools inspect <ref> --format "{{json .Provenance}}"',
    },
    {
      subject: 'Swarm mode status',
      value: 'current and supported; Classic Swarm is the discontinued product, Swarm mode is not',
      source: 'https://docs.docker.com/engine/swarm/',
      recheck: 'https://docs.docker.com/engine/swarm/ — look for a deprecation banner',
    },
    {
      subject: 'Alpine',
      value: '3.24 stable (3.24.0, 9 June 2026); 3.21 and newer still supported; 3.20 support ended 2026-04-01',
      source: 'https://www.alpinelinux.org/releases/',
      recheck: 'https://www.alpinelinux.org/releases/ — read the "supported until" column',
    },
    {
      subject: 'Debian slim',
      value: '13 "trixie" stable, point release 13.6 (11 July 2026); 12 "bookworm" is oldstable',
      source: 'https://www.debian.org/releases/',
      recheck: 'https://www.debian.org/releases/ — the page names the current stable codename',
    },
    {
      subject: 'PHP',
      value: '8.5 newest; 8.4 and 8.5 in active support; 8.3 security-only to 2027-12-31; 8.2 security-only to 2026-12-31; 8.1 and older EOL',
      source: 'https://www.php.net/supported-versions.php',
      recheck: 'https://www.php.net/supported-versions.php',
    },
    {
      subject: 'Node.js',
      value: '24 "Krypton" Active LTS (maintenance from 2026-10-20, EOL 2028-04-30); 22 "Jod" maintenance; 26 Current; 20 and older EOL',
      source: 'https://github.com/nodejs/Release',
      recheck: 'https://github.com/nodejs/Release — read the release schedule table',
    },
  ],
};

// An image line is out of support when its tag starts with one of these prefixes.
const EOL_LINES = [
  { image: /^(.*\/)?node$/, tags: [/^(0|4|6|8|10|12|14|16|18|19|20|21|23|25)(\D|$)/], why: 'Node.js line is past end-of-life; see --versions' },
  { image: /^(.*\/)?php$/, tags: [/^(5|7|8\.0|8\.1)(\D|$)/], why: 'PHP line is past end-of-life; see --versions' },
  { image: /^(.*\/)?alpine$/, tags: [/^3\.(1\d|20)(\D|$)/], why: 'Alpine line is past end-of-support; see --versions' },
  { image: /^(.*\/)?debian$/, tags: [/^(buster|stretch|jessie|10|9|8)(\D|$)/], why: 'Debian line is archived; see --versions' },
];

const COMPOSE_NAME = /^(docker-)?compose.*\.ya?ml$/i;
const IMAGE_LINE = /^\s*image:\s*(.+?)\s*$/;

function main(argv) {
  if (argv.includes('-h') || argv.includes('--help')) {
    process.stdout.write(HELP);
    return EXIT_CLEAN;
  }
  if (argv.includes('--versions')) return printVersions();
  if (argv.includes('--self-test')) return selfTest();

  const quiet = argv.includes('--quiet');
  const options = { release: argv.includes('--release'), mirrorVar: null, privateHosts: [] };
  const targets = [];
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === '--quiet' || arg === '--release') continue;
    if (arg === '--mirror-var') {
      options.mirrorVar = argv[++i];
      if (!options.mirrorVar) throw new CannotRun('--mirror-var requires a variable name');
      continue;
    }
    if (arg === '--private-host') {
      const value = argv[++i];
      if (!value) throw new CannotRun('--private-host requires a comma-separated list');
      options.privateHosts = value.split(',').map((s) => s.trim()).filter(Boolean);
      continue;
    }
    if (arg.startsWith('--')) throw new CannotRun(`unknown option: ${arg}`);
    targets.push(arg);
  }
  if (targets.length === 0) throw new CannotRun('no input path given; pass a file or a directory');

  const files = collectTargets(targets, (name) => COMPOSE_NAME.test(name));
  const findings = [];
  for (const file of files) findings.push(...checkFile(file, options));
  return reportFindings(findings, { quiet });
}

function printVersions() {
  process.stdout.write(`pinned upstream values, verified ${VERSION_REGISTER.verified}\n`);
  for (const row of VERSION_REGISTER.rows) {
    process.stdout.write(`\n${row.subject}\n  value:   ${row.value}\n  source:  ${row.source}\n  recheck: ${row.recheck}\n`);
  }
  return EXIT_CLEAN;
}

export function checkFile(file, options = {}) {
  const lines = readLines(file);
  const findings = [];

  lines.forEach((line, idx) => {
    if (/^\s*#/.test(line)) return;
    const m = IMAGE_LINE.exec(stripTrailingComment(line));
    if (!m) return;
    const lineNo = idx + 1;
    let raw = m[1].trim();
    if ((raw.startsWith('"') && raw.endsWith('"')) || (raw.startsWith("'") && raw.endsWith("'"))) {
      raw = raw.slice(1, -1);
    }

    // Substitute every `${VAR:-default}` with its default. The default is what a manager with a
    // clean environment deploys, so the default is the thing that has to be compliant.
    const effective = raw.replace(/\$\{([A-Za-z_][A-Za-z0-9_]*):-([^}]*)\}/g, (_m, _n, d) => d);
    const viaDefault = effective !== raw;

    if (effective.includes('$')) return; // still variable-driven; nothing literal left to judge
    if (effective === '') {
      findings.push(finding(file, lineNo, 'image-default-floating',
        `image ${raw} defaults to an empty reference; Compose will fail at deploy time with an unhelpful message`));
      return;
    }

    const rule = viaDefault ? 'image-default-floating' : null;
    const { name, tag, digest } = splitRef(effective);

    if (digest) {
      // pinned by digest; tag rules do not apply
    } else if (tag === null) {
      findings.push(finding(file, lineNo, rule || 'image-floating-latest',
        `image ${raw} has no tag, so it resolves to :latest`));
    } else if (tag === 'latest') {
      findings.push(finding(file, lineNo, rule || 'image-floating-latest',
        `image ${raw} resolves to :latest, which is a mutable pointer`));
    } else if (/^\d+$/.test(tag)) {
      findings.push(finding(file, lineNo, rule || 'image-bare-major',
        `image ${raw} pins the bare major "${tag}", which moves on every upstream minor release`));
    }

    if (options.release && !digest) {
      findings.push(finding(file, lineNo, 'image-no-digest',
        `image ${raw} is not pinned by digest; a release manifest records name:tag@sha256:...`));
    }

    if (tag) {
      for (const entry of EOL_LINES) {
        if (!entry.image.test(name)) continue;
        if (entry.tags.some((re) => re.test(tag))) {
          findings.push(finding(file, lineNo, 'image-eol-line', `image ${raw}: ${entry.why}`));
        }
      }
    }

    if (options.mirrorVar) {
      const prefixed = raw.includes(`\${${options.mirrorVar}`);
      const host = name.includes('/') && name.split('/')[0].includes('.') ? name.split('/')[0] : null;
      const isPrivate = host && (options.privateHosts || []).some((h) => host === h);
      // A reference that is nothing but `${VAR:-name:tag}` with no registry host is the service's
      // own image, built from this repository. It is not an upstream pull, so the mirror rule does
      // not apply to it; its floating default is already reported as image-default-floating.
      const ownImage = /^\$\{[A-Za-z_][A-Za-z0-9_]*:-[^}]*\}$/.test(raw) && !host;
      if (!prefixed && !isPrivate && !ownImage) {
        findings.push(finding(file, lineNo, 'image-not-mirrored',
          `image ${raw} is a literal public reference; prefix it with \${${options.mirrorVar}:-...} so the mirror governs it`));
      }
    }
  });

  return findings;
}

function splitRef(ref) {
  const atIndex = ref.indexOf('@');
  const digest = atIndex === -1 ? null : ref.slice(atIndex + 1);
  const withoutDigest = atIndex === -1 ? ref : ref.slice(0, atIndex);
  const lastColon = withoutDigest.lastIndexOf(':');
  const lastSlash = withoutDigest.lastIndexOf('/');
  if (lastColon > lastSlash) {
    return { name: withoutDigest.slice(0, lastColon), tag: withoutDigest.slice(lastColon + 1), digest };
  }
  return { name: withoutDigest, tag: digest ? '' : null, digest };
}

function stripTrailingComment(line) {
  let out = '';
  let quote = null;
  for (let i = 0; i < line.length; i++) {
    const ch = line[i];
    if (quote) { out += ch; if (ch === quote) quote = null; continue; }
    if (ch === '"' || ch === "'") { quote = ch; out += ch; continue; }
    if (ch === '#' && i > 0 && /\s/.test(line[i - 1])) break;
    out += ch;
  }
  return out;
}

function selfTest() {
  process.stdout.write('check-image-pinning --self-test\n');
  const dir = path.join(fixturesDir(), 'pinning');

  const clean = checkFile(path.join(dir, 'clean.compose.yml'));
  expect(clean.length, 0, 'compliant fixture produces no finding');

  const dirty = checkFile(path.join(dir, 'violations.compose.yml'));
  const byRule = {};
  for (const f of dirty) byRule[f.rule] = (byRule[f.rule] || 0) + 1;
  expect(byRule['image-floating-latest'] || 0, 2, 'literal :latest and untagged references');
  expect(byRule['image-bare-major'] || 0, 1, 'bare-major tag');
  expect(byRule['image-default-floating'] || 0, 1, 'floating default inside ${VAR:-...}');
  expect(byRule['image-eol-line'] || 0, 2, 'images on end-of-life upstream lines');

  const release = checkFile(path.join(dir, 'clean.compose.yml'), { release: true });
  expect(release.filter((f) => f.rule === 'image-no-digest').length, 2, 'release mode requires a digest');

  const mirrored = checkFile(path.join(dir, 'clean.compose.yml'), {
    mirrorVar: 'PUBLIC_DOCKER_REGISTRY',
    privateHosts: ['registry.example.invalid'],
  });
  expect(mirrored.filter((f) => f.rule === 'image-not-mirrored').length, 1, 'public image not routed through the mirror variable');

  let cannotRun = 0;
  try {
    checkFile(path.join(dir, 'absent.compose.yml'));
  } catch (err) {
    if (err instanceof CannotRun) cannotRun = EXIT_CANNOT_RUN;
  }
  expect(cannotRun, EXIT_CANNOT_RUN, 'missing file raises CannotRun (exit 2)');

  expect(VERSION_REGISTER.rows.every((r) => r.recheck && r.source), true, 'every pinned value carries a source and a recheck command');
  expect(reportFindings(dirty, { quiet: true }), EXIT_FINDINGS, 'findings map to exit 1');
  expect(reportFindings([], { quiet: true }), EXIT_CLEAN, 'no findings maps to exit 0');

  process.stdout.write('self-test passed\n');
  return EXIT_CLEAN;
}

run(main);
