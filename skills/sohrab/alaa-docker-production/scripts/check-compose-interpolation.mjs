#!/usr/bin/env node
// check-compose-interpolation.mjs — the fail-closed interpolation checker.
//
// Enforces `alaa-docker-production references/25-fail-closed-interpolation.md`.
//
// Two passes. The syntactic pass is a port of
// `service-runtime-kit/scripts/validate-runtime.sh:73-118` and asserts the same three things it
// does: no bare `$VAR`, no `${VAR}` without a modifier, and only the colon forms `:?` and `:-`.
// The semantic pass is the half neither the kit nor this skill has ever had: a variable in the
// fleet safety-control register may not carry a default at all (class A), or may not carry the
// specific default that disables it (class B).

import fs from 'node:fs';
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
import { classify, isDisablingDefault, REGISTER, validateExtraEntries } from './lib/safety-controls.mjs';

const HELP = `Usage:
  node check-compose-interpolation.mjs [options] <file-or-directory>...

Description:
  Assert that every variable interpolated into a Compose or Swarm stack file fails closed, and
  that no variable in the fleet safety-control register carries a default that disables it.

Rules:
  bare-interpolation      \`$VAR\` with no braces. Compose accepts it and substitutes empty when
                          unset, so the file deploys with the value missing.
  no-modifier             \`\${VAR}\` with neither \`:?\` nor \`:-\`. Same failure, braced.
  colonless-modifier      \`\${VAR-default}\` or \`\${VAR?message}\`. The colon-less forms treat a set
                          but empty variable as set, so \`VAR=\` in the shell defeats them.
  unsupported-modifier    \`\${VAR:+x}\` or \`\${VAR+x}\`. Allowlist the variable in a --register file
                          if a fleet file genuinely needs the alternate-value form.
  safety-control-default  A class-A register member written with \`:-\` in any form, including an
                          empty default. Class A means no default is ever correct.
  safety-control-disabled A class-B register member whose default is the value that turns the
                          control off (an empty or zero cap, a permissive toggle, a wildcard).

  A finding is silenced only by an in-file waiver comment on the preceding line:
    # safety-control-waiver: VAR_NAME reason=<one line saying why this default is correct here>
  A waiver with no reason= text is itself a finding (waiver-without-reason).

  A variable can be added to the register from inside the file it appears in:
    # safety-control: VAR_NAME — why a wrong default for this variable is a production defect
  Class A is assumed for an in-file declaration, because a variable worth declaring by hand is a
  variable whose value must come from outside the file.

Options:
  --register FILE   JSON file of extra register entries, merged ahead of the built-in register.
                    Shape: {"entries":[{"id":"...","class":"A"|"B","pattern":"...","why":"...",
                    "disabling":["..."]}]}
  --list-register   Print the effective register and exit 0.
  --quiet           Print nothing; use the exit code only.
  --self-test       Run against the fixtures shipped beside this script and exit 0 on success.
  -h, --help        Show this help and exit 0.

Exit codes:
  0  clean, or --help / --list-register / --self-test succeeded
  1  at least one finding
  2  could not run: a path that does not exist, an unreadable file, an unparsable --register
     file, or an input set that matched no files
`;

const COMPOSE_NAME = /^(docker-)?compose.*\.ya?ml$/i;

function main(argv) {
  if (argv.includes('-h') || argv.includes('--help')) {
    process.stdout.write(HELP);
    return EXIT_CLEAN;
  }
  if (argv.includes('--self-test')) return selfTest();

  const quiet = argv.includes('--quiet');
  const listOnly = argv.includes('--list-register');
  let extraEntries = [];
  const targets = [];

  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === '--quiet' || arg === '--list-register') continue;
    if (arg === '--register') {
      const file = argv[++i];
      if (!file) throw new CannotRun('--register requires a file path');
      let parsed;
      try {
        parsed = JSON.parse(fs.readFileSync(file, 'utf8'));
      } catch (err) {
        throw new CannotRun(`--register file is not readable JSON: ${file}: ${err.message}`);
      }
      try {
        extraEntries = validateExtraEntries(parsed, file);
      } catch (err) {
        throw new CannotRun(err.message);
      }
      continue;
    }
    if (arg.startsWith('--')) throw new CannotRun(`unknown option: ${arg}`);
    targets.push(arg);
  }

  if (listOnly) {
    for (const entry of [...extraEntries, ...REGISTER]) {
      process.stdout.write(`${entry.id}\tclass ${entry.class}\t/${entry.pattern}/\n`);
    }
    return EXIT_CLEAN;
  }

  if (targets.length === 0) throw new CannotRun('no input path given; pass a file or a directory');

  const files = collectTargets(targets, (name) => COMPOSE_NAME.test(name));
  const findings = [];
  for (const file of files) findings.push(...checkFile(file, extraEntries));
  return reportFindings(findings, { quiet });
}

export function checkFile(file, extraEntries = []) {
  const lines = readLines(file);
  const findings = [];
  const waivers = new Map(); // line number of the waived line -> reason
  const declared = [];

  lines.forEach((line, idx) => {
    const waiver = /#\s*safety-control-waiver:\s*([A-Za-z_][A-Za-z0-9_]*)\s*(.*)$/.exec(line);
    if (waiver) {
      const reason = /reason=(.+)$/.exec(waiver[2] || '');
      if (!reason || reason[1].trim() === '') {
        findings.push(
          finding(file, idx + 1, 'waiver-without-reason',
            `waiver for ${waiver[1]} states no reason=; a waiver with no argument is a silenced rule, not an accepted one`)
        );
      } else {
        waivers.set(`${idx + 2}:${waiver[1]}`, reason[1].trim());
      }
    }
    const decl = /#\s*safety-control:\s*([A-Za-z_][A-Za-z0-9_]*)\s*[—-]\s*(.+)$/.exec(line);
    if (decl) {
      declared.push({ id: `in-file:${decl[1]}`, class: 'A', pattern: `^${decl[1]}$`, why: decl[2].trim() });
    }
  });

  const register = [...declared, ...extraEntries];

  lines.forEach((line, idx) => {
    const lineNo = idx + 1;
    if (/^\s*#/.test(line)) return; // Compose parses YAML, which drops comment lines before interpolation
    const code = stripTrailingComment(line);
    for (const token of scanTokens(code)) {
      const { name, modifier, value } = token;
      const waived = waivers.get(`${lineNo}:${name}`);

      if (modifier === null) {
        findings.push(finding(file, lineNo, 'bare-interpolation',
          `$${name} is unbraced; write \${${name}:?why it is required} or \${${name}:-default}`));
        continue;
      }
      if (modifier === '') {
        findings.push(finding(file, lineNo, 'no-modifier',
          `\${${name}} has no modifier; write \${${name}:?why it is required} or \${${name}:-default}`));
        continue;
      }
      if (modifier === '-' || modifier === '?') {
        findings.push(finding(file, lineNo, 'colonless-modifier',
          `\${${name}${modifier}…} treats an empty value as set; use \${${name}:${modifier}…}`));
        continue;
      }
      if (modifier === ':+' || modifier === '+') {
        findings.push(finding(file, lineNo, 'unsupported-modifier',
          `\${${name}${modifier}…} is an alternate-value form; this fleet permits only :? and :-`));
        continue;
      }
      if (modifier === ':-') {
        const entry = classify(name, register);
        if (!entry) continue;
        if (entry.class === 'A') {
          if (waived) continue;
          findings.push(finding(file, lineNo, 'safety-control-default',
            `${name} matches register entry ${entry.id}; no default is permitted, write \${${name}:?…}. ${firstSentence(entry.why)} Full argument: references/25-fail-closed-interpolation.md, entry ${entry.id}.`));
        } else if (isDisablingDefault(entry, value)) {
          if (waived) continue;
          findings.push(finding(file, lineNo, 'safety-control-disabled',
            `${name} defaults to "${value}", which disables the control (register entry ${entry.id}). ${firstSentence(entry.why)} Full argument: references/25-fail-closed-interpolation.md, entry ${entry.id}.`));
        }
      }
    }
  });

  return findings;
}

/** First sentence of a register entry's argument, so a finding line stays one screen wide. */
function firstSentence(text) {
  const m = /^(.*?[.!?])(\s|$)/.exec(text);
  return m ? m[1] : text;
}

/** Drop a trailing `# comment` that is outside quotes. Compose never interpolates a comment. */
function stripTrailingComment(line) {
  let out = '';
  let quote = null;
  for (let i = 0; i < line.length; i++) {
    const ch = line[i];
    if (quote) {
      out += ch;
      if (ch === quote) quote = null;
      continue;
    }
    if (ch === '"' || ch === "'") { quote = ch; out += ch; continue; }
    if (ch === '#' && i > 0 && /\s/.test(line[i - 1])) break;
    out += ch;
  }
  return out;
}

/**
 * Yield every interpolation token on a line, honouring `$$` escapes the way Compose does: an odd
 * number of preceding `$` characters means the token is escaped and is not interpolated.
 * `modifier` is null for `$VAR`, '' for `${VAR}`, otherwise one of `:?`, `:-`, `?`, `-`, `:+`, `+`.
 */
function scanTokens(code) {
  const tokens = [];
  const re = /\$\{([A-Za-z_][A-Za-z0-9_]*)|\$([A-Za-z_][A-Za-z0-9_]*)/g;
  let m;
  while ((m = re.exec(code)) !== null) {
    let dollars = 0;
    for (let j = m.index - 1; j >= 0 && code[j] === '$'; j--) dollars++;
    if (dollars % 2 === 1) continue; // escaped: $${VAR} reaches the container as ${VAR}
    if (m[2] !== undefined) {
      tokens.push({ name: m[2], modifier: null, value: '' });
      continue;
    }
    const name = m[1];
    const after = code.slice(m.index + m[0].length);
    if (after.startsWith('}')) { tokens.push({ name, modifier: '', value: '' }); continue; }
    const mod = /^(:\?|:-|:\+|\?|-|\+)/.exec(after);
    if (!mod) { tokens.push({ name, modifier: '', value: '' }); continue; }
    const rest = after.slice(mod[1].length);
    tokens.push({ name, modifier: mod[1], value: readUntilClosingBrace(rest) });
  }
  return tokens;
}

/** Read a default value, tracking nesting so `${A:-${B:-x}}` yields `${B:-x}` and not `${B:-x`. */
function readUntilClosingBrace(rest) {
  let depth = 0;
  let out = '';
  for (let i = 0; i < rest.length; i++) {
    const ch = rest[i];
    if (ch === '$' && rest[i + 1] === '{') { depth++; out += '${'; i++; continue; }
    if (ch === '}') {
      if (depth === 0) return out;
      depth--;
    }
    out += ch;
  }
  return out;
}

function selfTest() {
  process.stdout.write('check-compose-interpolation --self-test\n');
  const dir = path.join(fixturesDir(), 'compose');

  const clean = checkFile(path.join(dir, 'clean.compose.yml'));
  expect(clean.length, 0, 'clean fixture produces no finding');

  const dirty = checkFile(path.join(dir, 'violations.compose.yml'));
  const byRule = {};
  for (const f of dirty) byRule[f.rule] = (byRule[f.rule] || 0) + 1;
  expect(byRule['bare-interpolation'] || 0, 2, 'bare $VAR findings');
  expect(byRule['no-modifier'] || 0, 1, 'braced-no-modifier findings');
  expect(byRule['colonless-modifier'] || 0, 2, 'colon-less modifier findings');
  expect(byRule['unsupported-modifier'] || 0, 1, 'alternate-value modifier findings');
  expect(byRule['safety-control-default'] || 0, 4, 'class-A default findings');
  expect(byRule['safety-control-disabled'] || 0, 3, 'class-B disabling-default findings');
  expect(byRule['waiver-without-reason'] || 0, 1, 'waiver with no reason findings');

  const escaped = checkFile(path.join(dir, 'escapes.compose.yml'));
  expect(escaped.length, 0, 'escaped $$ and commented lines produce no finding');

  let cannotRun = 0;
  try {
    checkFile(path.join(dir, 'does-not-exist.yml'));
  } catch (err) {
    if (err instanceof CannotRun) cannotRun = EXIT_CANNOT_RUN;
  }
  expect(cannotRun, EXIT_CANNOT_RUN, 'missing file raises CannotRun (exit 2)');

  expect(reportFindings(dirty, { quiet: true }), EXIT_FINDINGS, 'findings map to exit 1');
  expect(reportFindings([], { quiet: true }), EXIT_CLEAN, 'no findings maps to exit 0');

  process.stdout.write('self-test passed\n');
  return EXIT_CLEAN;
}

run(main);
