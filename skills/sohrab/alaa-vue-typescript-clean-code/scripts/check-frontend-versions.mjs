#!/usr/bin/env node

// check-frontend-versions.mjs
//
// Prints installed-versus-latest for the packages whose versions gate the rules
// asserted by alaa-vue-typescript-clean-code:
//   references/20-typescript-composition-contract.md  (Vue 3.5 / 3.6, Pinia 3)
//   references/24-typescript-project-and-antipatterns.md (the TypeScript line)
//   references/50-quasar-vite-pinia-contract.md       (Pinia, router, Vite)
//
// Installed versions are read from the repository, never from the network:
// package-lock.json / npm-shrinkwrap.json first, then yarn.lock, then
// pnpm-lock.yaml, then node_modules/<pkg>/package.json, then the declared range
// in package.json (marked as a range, not an installed version).
//
// Package-manager-neutral: it talks to the npm registry directly over HTTPS and
// every request carries a timeout, because a registry that accepts a connection
// and then stalls would otherwise hang the caller with no diagnostic.
//
// Exit codes:
//   0  clean          - every gated package resolved, no drift worth reporting
//   1  drift          - at least one package is behind its latest, or the
//                       installed major differs from the major this skill gates
//   2  could not run  - bad arguments, no package.json, or every registry
//                       lookup failed. Distinct from 0 on purpose: "could not
//                       run" is reported as unverified, never as clean.
//   3  self-test failed

import https from 'node:https'
import fs from 'node:fs'
import path from 'node:path'
import process from 'node:process'

const SCRIPT = 'check-frontend-versions.mjs'
const USER_AGENT = 'alaa-vue-typescript-clean-code-skill'
const DEFAULT_TIMEOUT_MS = 8000
// ALAA_NPM_REGISTRY exists so the timeout and failure paths can be exercised
// against a controlled host; production runs use the default.
const REGISTRY = process.env.ALAA_NPM_REGISTRY || 'https://registry.npmjs.org'

// name -> the major this skill's rules are written against, or null when the
// skill states no major-specific rule for it.
const GATED = {
  vue: 3,
  'vue-router': 4,
  pinia: 3,
  vite: null,
  typescript: 6,
  'vue-tsc': null,
  '@quasar/app-vite': 3,
  quasar: 2,
}

function usage() {
  return `${SCRIPT} - installed vs latest for the packages this skill's version gates depend on

Usage:
  node ${SCRIPT} [--dir <path>] [--timeout <ms>] [--offline] [--json]
  node ${SCRIPT} --self-test
  node ${SCRIPT} --help

Options:
  --dir <path>     Project root holding package.json. Default: current directory.
  --timeout <ms>   Per-request timeout. Default: ${DEFAULT_TIMEOUT_MS}.
  --offline        Report installed versions only; make no network request.

Environment:
  ALAA_NPM_REGISTRY  Override the registry base URL (used to exercise the
                     timeout and failure paths against a controlled host).
  --json           Emit machine-readable JSON instead of a table.
  --self-test      Run the built-in checks (no network) and exit.
  --help, -h       Show this message.

Exit codes:
  0  clean         every gated package resolved and no drift worth reporting
  1  drift         a package is behind latest, or its major differs from the gated major
  2  could not run bad arguments, no package.json, or every registry lookup failed
  3  self-test failed

"Could not run" is deliberately distinct from "clean": an unreachable registry is
reported as unverified, never rounded down to a pass.`
}

function parseArgs(argv) {
  const opts = { dir: process.cwd(), timeout: DEFAULT_TIMEOUT_MS, offline: false, json: false, help: false, selfTest: false }
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i]
    if (arg === '--help' || arg === '-h') opts.help = true
    else if (arg === '--self-test') opts.selfTest = true
    else if (arg === '--offline') opts.offline = true
    else if (arg === '--json') opts.json = true
    else if (arg === '--dir') { opts.dir = argv[++i]; if (!opts.dir) throw new Error('--dir needs a path') }
    else if (arg === '--timeout') {
      const raw = argv[++i]
      const value = Number(raw)
      if (!Number.isFinite(value) || value <= 0) throw new Error(`--timeout needs a positive number of milliseconds, got ${raw}`)
      opts.timeout = value
    }
    else throw new Error(`unknown argument: ${arg}`)
  }
  return opts
}

// --- version helpers -------------------------------------------------------

export function cleanVersion(raw) {
  if (typeof raw !== 'string') return null
  const match = raw.match(/(\d+)\.(\d+)\.(\d+)(?:[-+][0-9A-Za-z.-]+)?/)
  return match ? match[0] : null
}

export function majorOf(version) {
  const cleaned = cleanVersion(version)
  return cleaned ? Number(cleaned.split('.')[0]) : null
}

export function compareVersions(a, b) {
  const pa = String(a).split('-')[0].split('.').map(Number)
  const pb = String(b).split('-')[0].split('.').map(Number)
  for (let i = 0; i < 3; i += 1) {
    const da = pa[i] ?? 0
    const db = pb[i] ?? 0
    if (da !== db) return da - db
  }
  return 0
}

// --- reading installed versions from the repository ------------------------

function readJson(file) {
  try { return JSON.parse(fs.readFileSync(file, 'utf8')) }
  catch { return null }
}

export function fromNpmLock(lock, name) {
  if (!lock || typeof lock !== 'object') return null
  const packages = lock.packages
  if (packages && typeof packages === 'object') {
    const entry = packages[`node_modules/${name}`]
    if (entry && typeof entry.version === 'string') return entry.version
  }
  const deps = lock.dependencies
  if (deps && typeof deps === 'object' && deps[name] && typeof deps[name].version === 'string') {
    return deps[name].version
  }
  return null
}

export function fromYarnLock(text, name) {
  if (typeof text !== 'string') return null
  const lines = text.split('\n')
  for (let i = 0; i < lines.length; i += 1) {
    const header = lines[i]
    if (!header || header.startsWith('#') || /^\s/.test(header)) continue
    if (!header.includes(`${name}@`)) continue
    for (let j = i + 1; j < lines.length && /^\s/.test(lines[j]); j += 1) {
      const m = lines[j].match(/^\s+version:?\s+"?([^"\s]+)"?/)
      if (m) return m[1]
    }
  }
  return null
}

export function fromPnpmLock(text, name) {
  if (typeof text !== 'string') return null
  const escaped = name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
  const patterns = [
    new RegExp(`^\\s*/${escaped}@([0-9][^(:\\s]*)`, 'm'),
    new RegExp(`^\\s*${escaped}@([0-9][^(:\\s]*)`, 'm'),
  ]
  for (const re of patterns) {
    const m = text.match(re)
    if (m) return cleanVersion(m[1])
  }
  return null
}

function installedVersion(dir, name) {
  for (const lockName of ['package-lock.json', 'npm-shrinkwrap.json']) {
    const lock = readJson(path.join(dir, lockName))
    const found = fromNpmLock(lock, name)
    if (found) return { version: cleanVersion(found), source: lockName }
  }
  for (const [lockName, reader] of [['yarn.lock', fromYarnLock], ['pnpm-lock.yaml', fromPnpmLock]]) {
    const file = path.join(dir, lockName)
    if (fs.existsSync(file)) {
      const found = reader(fs.readFileSync(file, 'utf8'), name)
      if (found) return { version: cleanVersion(found), source: lockName }
    }
  }
  const pkg = readJson(path.join(dir, 'node_modules', name, 'package.json'))
  if (pkg && pkg.version) return { version: cleanVersion(pkg.version), source: 'node_modules' }
  return null
}

function declaredRange(manifest, name) {
  for (const field of ['dependencies', 'devDependencies', 'peerDependencies', 'optionalDependencies']) {
    const group = manifest[field]
    if (group && typeof group === 'object' && typeof group[name] === 'string') return group[name]
  }
  return null
}

// --- registry --------------------------------------------------------------

function fetchJson(url, timeoutMs) {
  return new Promise((resolve, reject) => {
    let settled = false
    const finish = (fn, value) => { if (!settled) { settled = true; fn(value) } }

    const request = https.get(
      url,
      { headers: { 'User-Agent': USER_AGENT, Accept: 'application/vnd.npm.install-v1+json' } },
      (response) => {
        if (response.statusCode !== 200) {
          response.resume()
          finish(reject, new Error(`HTTP ${response.statusCode} for ${url}`))
          return
        }
        let data = ''
        response.setEncoding('utf8')
        response.on('data', (chunk) => { data += chunk })
        response.on('end', () => {
          try { finish(resolve, JSON.parse(data)) }
          catch (error) { finish(reject, error) }
        })
        response.on('error', (error) => finish(reject, error))
      },
    )

    // Both are needed: setTimeout covers a socket that connects and then goes
    // quiet; the outer timer covers a request that never reaches a socket at all.
    request.setTimeout(timeoutMs, () => {
      request.destroy(new Error(`timeout after ${timeoutMs}ms for ${url}`))
    })
    const guard = setTimeout(() => {
      request.destroy(new Error(`timeout after ${timeoutMs}ms for ${url}`))
    }, timeoutMs + 500)
    guard.unref?.()

    request.on('error', (error) => { clearTimeout(guard); finish(reject, error) })
    request.on('close', () => clearTimeout(guard))
  })
}

async function latestVersion(name, timeoutMs) {
  const url = `${REGISTRY}/${name.replace('/', '%2F')}`
  const body = await fetchJson(url, timeoutMs)
  const latest = body?.['dist-tags']?.latest
  if (!latest) throw new Error(`no dist-tags.latest for ${name}`)
  return latest
}

// --- self-test -------------------------------------------------------------

function selfTest() {
  const failures = []
  const check = (label, actual, expected) => {
    const a = JSON.stringify(actual)
    const e = JSON.stringify(expected)
    if (a !== e) failures.push(`${label}: expected ${e}, got ${a}`)
  }

  check('cleanVersion caret', cleanVersion('^3.5.13'), '3.5.13')
  check('cleanVersion prerelease', cleanVersion('3.6.0-rc.2'), '3.6.0-rc.2')
  check('cleanVersion junk', cleanVersion('workspace:*'), null)
  check('majorOf', majorOf('~2.18.1'), 2)
  check('compare patch', Math.sign(compareVersions('3.5.13', '3.5.9')), 1)
  check('compare equal', compareVersions('3.5.13', '3.5.13'), 0)
  check('compare major', Math.sign(compareVersions('2.9.9', '3.0.0')), -1)
  check('compare prerelease ignores tag', compareVersions('3.6.0-rc.2', '3.6.0'), 0)

  check('npm lock packages form', fromNpmLock({ packages: { 'node_modules/vue': { version: '3.5.13' } } }, 'vue'), '3.5.13')
  check('npm lock dependencies form', fromNpmLock({ dependencies: { pinia: { version: '3.0.1' } } }, 'pinia'), '3.0.1')
  check('npm lock missing', fromNpmLock({ packages: {} }, 'vue'), null)

  check('yarn lock classic', fromYarnLock('vue@^3.5.0:\n  version "3.5.13"\n  resolved "..."\n', 'vue'), '3.5.13')
  check('yarn lock berry', fromYarnLock('"vue@npm:^3.5.0":\n  version: 3.5.13\n', 'vue'), '3.5.13')
  check('pnpm lock', fromPnpmLock('packages:\n\n  /vue@3.5.13(typescript@6.0.2):\n    resolution: {}\n', 'vue'), '3.5.13')
  check('pnpm lock scoped', fromPnpmLock("  /@quasar/app-vite@3.0.1:\n", '@quasar/app-vite'), '3.0.1')

  const args = parseArgs(['--offline', '--timeout', '1234'])
  check('parseArgs offline', args.offline, true)
  check('parseArgs timeout', args.timeout, 1234)
  let rejected = false
  try { parseArgs(['--timeout', 'soon']) } catch { rejected = true }
  check('parseArgs rejects bad timeout', rejected, true)
  let unknown = false
  try { parseArgs(['--nope']) } catch { unknown = true }
  check('parseArgs rejects unknown flag', unknown, true)

  if (failures.length) {
    console.error(`${SCRIPT} self-test FAILED (${failures.length}):`)
    for (const failure of failures) console.error(`  - ${failure}`)
    return 3
  }
  console.log(`${SCRIPT} self-test passed (18 checks)`)
  return 0
}

// --- main ------------------------------------------------------------------

async function main() {
  let opts
  try { opts = parseArgs(process.argv.slice(2)) }
  catch (error) {
    console.error(`${SCRIPT}: ${error.message}`)
    console.error(usage())
    return 2
  }

  if (opts.help) { console.log(usage()); return 0 }
  if (opts.selfTest) return selfTest()

  const manifestPath = path.join(opts.dir, 'package.json')
  if (!fs.existsSync(manifestPath)) {
    console.error(`${SCRIPT}: no package.json in ${opts.dir} - could not run.`)
    console.error('Run this from a repository root, or pass --dir <path>.')
    return 2
  }
  const manifest = readJson(manifestPath)
  if (!manifest) {
    console.error(`${SCRIPT}: package.json in ${opts.dir} is not valid JSON - could not run.`)
    return 2
  }

  const names = Object.keys(GATED).filter((name) => declaredRange(manifest, name) !== null)
  if (names.length === 0) {
    console.error(`${SCRIPT}: none of the gated packages are declared in ${manifestPath} - could not run.`)
    console.error(`Gated packages: ${Object.keys(GATED).join(', ')}`)
    return 2
  }

  const rows = []
  let lookupAttempts = 0
  let lookupFailures = 0

  for (const name of names) {
    const found = installedVersion(opts.dir, name)
    const range = declaredRange(manifest, name)
    const row = {
      name,
      installed: found?.version ?? null,
      source: found?.source ?? null,
      declared: range,
      latest: null,
      latestError: null,
      gatedMajor: GATED[name],
      notes: [],
    }
    if (!opts.offline) {
      lookupAttempts += 1
      try { row.latest = await latestVersion(name, opts.timeout) }
      catch (error) { row.latestError = error.message; lookupFailures += 1 }
    }
    if (!row.installed) row.notes.push('not installed here; the declared range is a range, not a version')
    if (row.installed && row.gatedMajor !== null && majorOf(row.installed) !== row.gatedMajor) {
      row.notes.push(`installed major ${majorOf(row.installed)} differs from the major this skill gates (${row.gatedMajor})`)
    }
    if (row.installed && row.latest && compareVersions(row.installed, row.latest) < 0) {
      row.notes.push('behind latest')
    }
    rows.push(row)
  }

  if (!opts.offline && lookupAttempts > 0 && lookupFailures === lookupAttempts) {
    console.error(`${SCRIPT}: every registry lookup failed (${lookupFailures}/${lookupAttempts}) - could not run.`)
    for (const row of rows) console.error(`  ${row.name}: ${row.latestError}`)
    console.error('Report this as unverified. Do not report the version gates as checked.')
    return 2
  }

  if (opts.json) {
    console.log(JSON.stringify({ dir: opts.dir, offline: opts.offline, rows }, null, 2))
  }
  else {
    const width = Math.max(...rows.map((r) => r.name.length), 8)
    console.log(`${'package'.padEnd(width)}  ${'installed'.padEnd(12)}  ${'latest'.padEnd(12)}  notes`)
    for (const row of rows) {
      const latest = row.latest ?? (opts.offline ? '(offline)' : `(error: ${row.latestError})`)
      const notes = row.notes.length ? row.notes.join('; ') : ''
      console.log(`${row.name.padEnd(width)}  ${(row.installed ?? '-').padEnd(12)}  ${String(latest).padEnd(12)}  ${notes}`)
    }
    if (lookupFailures > 0) {
      console.log(`\n${lookupFailures} of ${lookupAttempts} registry lookups failed; those rows are unverified, not clean.`)
    }
    console.log('\nThe rules these versions gate: references/20-typescript-composition-contract.md,')
    console.log('references/24-typescript-project-and-antipatterns.md, references/50-quasar-vite-pinia-contract.md.')
  }

  const drift = rows.some((row) => row.notes.some((note) => note === 'behind latest' || note.startsWith('installed major')))
  return drift ? 1 : 0
}

const invokedDirectly = process.argv[1] && process.argv[1].endsWith('check-frontend-versions.mjs')
if (invokedDirectly) {
  main().then((code) => { process.exitCode = code }).catch((error) => {
    console.error(`${SCRIPT}: unexpected failure - ${error.message}`)
    process.exitCode = 2
  })
}
