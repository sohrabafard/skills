// Shared helpers for the alaa-docker-production checkers.
//
// Every checker in this directory obeys the same four contracts:
//   1. `--help` prints usage, the rules it enforces, and the exit-code table.
//   2. Exit 0 means clean, 1 means findings, 2 means the checker could not run. A file it could
//      not read, a directory that does not exist, a YAML construct it does not support and an
//      unparsable register are all exit 2 and never exit 0.
//   3. It strips a trailing carriage return from every line it reads, so a CRLF checkout compares
//      the same as an LF one.
//   4. It writes nothing. No temporary directory is created anywhere, because the owner's
//      checkout is read-only in places.

import path from 'node:path';
import fs from 'node:fs';

export const EXIT_CLEAN = 0;
export const EXIT_FINDINGS = 1;
export const EXIT_CANNOT_RUN = 2;

export class CannotRun extends Error {}

/** Read a UTF-8 text file and split it into lines with any trailing CR removed. */
export function readLines(file) {
  let raw;
  try {
    raw = fs.readFileSync(file, 'utf8');
  } catch (err) {
    throw new CannotRun(`cannot read ${file}: ${err.message}`);
  }
  if (raw.charCodeAt(0) === 0xfeff) raw = raw.slice(1); // strip a UTF-8 BOM
  return raw.split('\n').map((line) => (line.endsWith('\r') ? line.slice(0, -1) : line));
}

export function readText(file) {
  return readLines(file).join('\n');
}

export function statOrCannotRun(target) {
  try {
    return fs.statSync(target);
  } catch (err) {
    throw new CannotRun(`path does not exist or cannot be inspected: ${target} (${err.message})`);
  }
}

/**
 * Expand each argument into a list of files. A file argument is used as-is. A directory argument
 * is scanned (non-recursively by default) for names matching `matcher`. A directory that matches
 * nothing is a "could not run" condition, not a clean result: a checker that reports success on
 * an empty input set is the defect class this batch exists to remove.
 */
export function collectTargets(args, matcher, { recursive = false } = {}) {
  const files = [];
  for (const arg of args) {
    const st = statOrCannotRun(arg);
    if (st.isFile()) {
      files.push(path.resolve(arg));
      continue;
    }
    if (!st.isDirectory()) throw new CannotRun(`not a file or directory: ${arg}`);
    walk(path.resolve(arg), files, matcher, recursive, 0);
  }
  if (files.length === 0) {
    throw new CannotRun(
      `no matching input files found under: ${args.join(', ')}. ` +
        'Pass an explicit file path if the name does not match the expected pattern.'
    );
  }
  return [...new Set(files)].sort();
}

function walk(dir, out, matcher, recursive, depth) {
  if (depth > 8) return;
  let entries;
  try {
    entries = fs.readdirSync(dir, { withFileTypes: true });
  } catch (err) {
    throw new CannotRun(`cannot list ${dir}: ${err.message}`);
  }
  for (const entry of entries) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (!recursive) continue;
      if (['.git', 'node_modules', 'vendor', '_to_delete'].includes(entry.name)) continue;
      walk(full, out, matcher, recursive, depth + 1);
    } else if (entry.isFile() && matcher(entry.name)) {
      out.push(full);
    }
  }
}

/** A finding is always file + line + rule id + message, so a report line is greppable. */
export function finding(file, line, rule, message) {
  return { file, line, rule, message };
}

export function reportFindings(findings, { quiet = false } = {}) {
  if (quiet) return findings.length === 0 ? EXIT_CLEAN : EXIT_FINDINGS;
  if (findings.length === 0) {
    process.stdout.write('clean: 0 findings\n');
    return EXIT_CLEAN;
  }
  for (const f of findings) {
    process.stdout.write(`${f.file}:${f.line}: ${f.rule}: ${f.message}\n`);
  }
  process.stdout.write(`${findings.length} finding(s)\n`);
  return EXIT_FINDINGS;
}

/** Run a checker main() and map exceptions onto the exit-code contract. */
export function run(main) {
  try {
    const code = main(process.argv.slice(2));
    process.exit(code);
  } catch (err) {
    if (err instanceof CannotRun) {
      process.stderr.write(`could not run: ${err.message}\n`);
      process.exit(EXIT_CANNOT_RUN);
    }
    process.stderr.write(`could not run: unexpected error: ${err && err.stack ? err.stack : err}\n`);
    process.exit(EXIT_CANNOT_RUN);
  }
}
