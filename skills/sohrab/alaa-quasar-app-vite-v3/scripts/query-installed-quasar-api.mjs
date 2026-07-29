#!/usr/bin/env node

// Delegate exact API output to the target project's installed Quasar CLI.
import { existsSync, readFileSync, realpathSync, statSync } from 'node:fs'
import { createRequire } from 'node:module'
import { dirname, isAbsolute, relative, resolve } from 'node:path'
import { spawnSync } from 'node:child_process'
import { tmpdir } from 'node:os'

const usage = `query-installed-quasar-api.mjs - bridge to the target project's own Quasar CLI.

Usage:
  node query-installed-quasar-api.mjs [--project <path>] <symbol|list> [quasar describe options]

Options:
  -h, --help        Print this help and exit 0.
      --self-test   Run offline self-checks of the internal logic and exit 0 on
                    success or 1 on failure. Makes no network request and needs
                    no Quasar project.
      --project <p> Directory (or a file inside one) to search upward from for a
                    package.json declaring @quasar/app-vite. Default: cwd.

Examples:
  node query-installed-quasar-api.mjs QTable -p -s -e -m
  node query-installed-quasar-api.mjs --project ../app QSelect -p -f map
  node query-installed-quasar-api.mjs --project ../app list storage

Exit codes:
  0  the project-local quasar describe ran and exited 0
  2  this bridge could not run: no project found, dependencies not installed,
     no CLI bin entry, or the CLI ended on a signal. "Could not run" is never
     reported as a clean result.
  3  bad usage: no symbol or list query given
  *  any other code is the project-local quasar describe's own exit status,
     propagated unchanged

Diagnostics go to stderr so stdout carries only the CLI's output.
The target project must declare and have installed @quasar/app-vite and quasar.`

const EXIT_CANNOT_RUN = 2
const EXIT_USAGE = 3

class BridgeError extends Error {
  constructor(message, code = EXIT_CANNOT_RUN) { super(message); this.code = code }
}

function fail(message, code = EXIT_CANNOT_RUN) { throw new BridgeError(message, code) }

function readJson(path, label) {
  try { return JSON.parse(readFileSync(path, 'utf8')) }
  catch (error) {
    const detail = error instanceof Error ? error.message : String(error)
    fail(`Cannot read ${label} at ${path}: ${detail}`)
  }
}

function declaredDependencies(packageJson) {
  return {
    ...packageJson.dependencies,
    ...packageJson.devDependencies,
    ...packageJson.optionalDependencies,
  }
}

function normalizeStartPath(input) {
  const path = resolve(input)
  if (!existsSync(path)) fail(`Project path does not exist: ${path}`)
  return statSync(path).isDirectory() ? path : dirname(path)
}

function findQuasarProject(input) {
  let current = normalizeStartPath(input)
  while (true) {
    const packageJsonPath = resolve(current, 'package.json')
    if (existsSync(packageJsonPath)) {
      const packageJson = readJson(packageJsonPath, 'project package.json')
      if (declaredDependencies(packageJson)['@quasar/app-vite']) {
        return { root: current, packageJsonPath }
      }
    }
    const parent = dirname(current)
    if (parent === current) break
    current = parent
  }
  fail(`No Quasar CLI + Vite project declaring @quasar/app-vite was found from ${input} upward.`)
}

function parseArguments(argv) {
  let project = process.cwd()
  const describeArgs = []
  for (let index = 0; index < argv.length; index += 1) {
    const argument = argv[index]
    if (argument === '--help' || argument === '-h') return { help: true, selfTest: false, project, describeArgs }
    if (argument === '--self-test') return { help: false, selfTest: true, project, describeArgs }
    if (argument === '--project') {
      const value = argv[index + 1]
      if (!value) fail('--project requires a path.')
      project = value
      index += 1
      continue
    }
    if (argument.startsWith('--project=')) {
      project = argument.slice('--project='.length)
      if (!project) fail('--project requires a path.')
      continue
    }
    describeArgs.push(argument)
  }
  if (describeArgs[0] === 'describe') describeArgs.shift()
  return { help: false, selfTest: false, project, describeArgs }
}

function resolveInstalledPackage(requireFromProject, name) {
  try {
    const packageJsonPath = requireFromProject.resolve(`${name}/package.json`)
    return {
      packageJsonPath,
      packageJson: readJson(packageJsonPath, `${name} package.json`),
    }
  }
  catch (error) {
    const detail = error instanceof Error ? error.message : String(error)
    fail(`${name} is declared but not resolvable from the project. Install dependencies with the repository's existing package manager. ${detail}`)
  }
}

function resolveQuasarBin(appVitePackage) {
  const bin = typeof appVitePackage.packageJson.bin === 'string'
    ? appVitePackage.packageJson.bin
    : appVitePackage.packageJson.bin?.quasar
  if (!bin) fail('The installed @quasar/app-vite package does not expose a quasar CLI bin entry.')

  const packageDir = dirname(appVitePackage.packageJsonPath)
  const binPath = realpathSync(resolve(packageDir, bin))
  const relativeBinPath = relative(realpathSync(packageDir), binPath)
  if (relativeBinPath.startsWith('..') || isAbsolute(relativeBinPath)) {
    fail(`Refusing to execute a Quasar CLI outside the installed package: ${binPath}`)
  }
  return binPath
}

function displayPath(path) { return path.replaceAll('\\', '/') }

function selfTest() {
  const failures = []
  const check = (label, condition) => { if (!condition) failures.push(label) }

  const a = parseArguments(['--project', '../app', 'QTable', '-p', '-s'])
  check('--project is consumed with its value', a.project === '../app')
  check('describe args survive --project', a.describeArgs.join(' ') === 'QTable -p -s')

  const b = parseArguments(['--project=../app', 'list', 'storage'])
  check('--project=<path> form is parsed', b.project === '../app')
  check('list query survives', b.describeArgs.join(' ') === 'list storage')

  const c = parseArguments(['describe', 'QSelect'])
  check('a leading "describe" is dropped', c.describeArgs.join(' ') === 'QSelect')

  check('--help is detected', parseArguments(['--help']).help === true)
  check('-h is detected', parseArguments(['-h']).help === true)
  check('--self-test is detected', parseArguments(['--self-test']).selfTest === true)

  const deps = declaredDependencies({
    dependencies: { quasar: '^2' },
    devDependencies: { '@quasar/app-vite': '^3' },
  })
  check('declaredDependencies merges dependency kinds', deps['@quasar/app-vite'] === '^3' && deps.quasar === '^2')

  let missingProjectMessage = ''
  try { findQuasarProject(tmpdir()) }
  catch (error) { missingProjectMessage = error.message }
  check('a missing project fails with an actionable message',
    missingProjectMessage.includes('@quasar/app-vite') && missingProjectMessage.includes('upward'))

  let noBinMessage = ''
  try { resolveQuasarBin({ packageJsonPath: '/nowhere/package.json', packageJson: {} }) }
  catch (error) { noBinMessage = error.message }
  check('a package with no bin entry fails clearly', noBinMessage.includes('bin entry'))

  check('displayPath normalizes separators', displayPath('a\\b\\c') === 'a/b/c')

  if (failures.length === 0) {
    console.log('self-test: ok (12 checks, no network, no project required)')
    return 0
  }
  for (const failure of failures) console.error(`self-test FAILED: ${failure}`)
  return 1
}

function main() {
  const { help, selfTest: runSelfTest, project, describeArgs } = parseArguments(process.argv.slice(2))
  if (help) {
    console.log(usage)
    return
  }
  if (runSelfTest) {
    process.exitCode = selfTest()
    return
  }
  if (describeArgs.length === 0) fail(`Missing Quasar API symbol or list query.\n\n${usage}`, EXIT_USAGE)

  const quasarProject = findQuasarProject(project)
  const requireFromProject = createRequire(quasarProject.packageJsonPath)
  const appVitePackage = resolveInstalledPackage(requireFromProject, '@quasar/app-vite')
  const quasarPackage = resolveInstalledPackage(requireFromProject, 'quasar')
  const quasarBin = resolveQuasarBin(appVitePackage)
  const args = describeArgs.includes('--no-color') ? describeArgs : [...describeArgs, '--no-color']

  console.error(`[alaa-quasar-api] project=${displayPath(quasarProject.root)}`)
  console.error(`[alaa-quasar-api] @quasar/app-vite=${appVitePackage.packageJson.version} quasar=${quasarPackage.packageJson.version}`)
  console.error('[alaa-quasar-api] source=project-local quasar describe')

  const result = spawnSync(process.execPath, [quasarBin, 'describe', ...args], {
    cwd: quasarProject.root,
    env: { ...process.env, FORCE_COLOR: '0', NO_COLOR: '1' },
    stdio: 'inherit',
  })
  if (result.error) fail(`Failed to run the project-local Quasar CLI: ${result.error.message}`)
  if (result.status === null) {
    fail(`The project-local Quasar CLI ended without an exit status${result.signal ? ` (signal: ${result.signal})` : ''}.`)
  }
  process.exitCode = result.status
}

try { main() }
catch (error) {
  console.error(error instanceof Error ? error.message : String(error))
  process.exitCode = error instanceof BridgeError ? error.code : EXIT_CANNOT_RUN
}
