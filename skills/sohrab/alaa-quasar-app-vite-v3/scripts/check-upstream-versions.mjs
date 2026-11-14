#!/usr/bin/env node

// Package-manager-neutral npm snapshot for the Quasar toolchain.
//
// Exit codes are meaningful and "could not run" is never reported as "clean":
//   0  every requested package was fetched
//   2  at least one package could not be fetched; the rest are still printed
//   3  bad usage
//
// See --help. Fleet note: this is the only copy of this script; other skills
// route here rather than duplicating it.

import https from 'node:https'
import { URL } from 'node:url'

const PACKAGES = [
  'quasar', '@quasar/app-vite', '@quasar/extras', 'vite', 'vue',
  'vue-router', 'pinia', 'workbox-build', 'workbox-core',
]
const SHOW_ALL_TAGS = new Set(['@quasar/app-vite'])
const RESOLVE_STABLE_MAJORS = { '@quasar/app-vite': [2, 3] }
const PEER_RANGES_FOR = new Set(['@quasar/app-vite'])

const DEFAULT_TIMEOUT_MS = 15000
const DEFAULT_RETRIES = 1

const EXIT_OK = 0
const EXIT_PARTIAL = 2
const EXIT_USAGE = 3

const HELP = `check-upstream-versions.mjs - read the current npm registry state for the Quasar toolchain.

Usage:
  node check-upstream-versions.mjs [options]

Options:
  -h, --help            Print this help and exit 0.
      --timeout <ms>    Per-request timeout. Default ${DEFAULT_TIMEOUT_MS}.
      --retries <n>     Retries per package after a timeout or network error.
                        Default ${DEFAULT_RETRIES}.
      --package <name>  Restrict to one package. Repeatable.

Output:
  JSON on stdout. Each package is either { latest, publishedAt, ... } or
  { error: "<message>" }. A top-level "errors" array lists every package that
  could not be read, and "ok" is false when that array is non-empty.

Exit codes:
  0  every requested package was fetched
  2  at least one package could not be fetched (the others are still printed)
  3  bad usage

Proxy:
  HTTPS_PROXY / https_proxy is honoured via CONNECT, and NO_PROXY / no_proxy is
  respected. A registry behind a proxy therefore works without extra flags.
`

function parseArguments(argv) {
  const options = {
    help: false,
    timeoutMs: DEFAULT_TIMEOUT_MS,
    retries: DEFAULT_RETRIES,
    packages: [],
  }
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i]
    if (arg === '-h' || arg === '--help') { options.help = true; continue }
    if (arg === '--timeout') {
      const value = Number(argv[++i])
      if (!Number.isFinite(value) || value <= 0) throw new Error('--timeout needs a positive number of milliseconds')
      options.timeoutMs = value
      continue
    }
    if (arg === '--retries') {
      const value = Number(argv[++i])
      if (!Number.isInteger(value) || value < 0) throw new Error('--retries needs a non-negative integer')
      options.retries = value
      continue
    }
    if (arg === '--package') {
      const value = argv[++i]
      if (!value) throw new Error('--package needs a package name')
      options.packages.push(value)
      continue
    }
    throw new Error(`Unknown argument: ${arg}`)
  }
  return options
}

export function compareVersions(a, b) {
  const pa = String(a).split('.').map(Number)
  const pb = String(b).split('.').map(Number)
  for (let i = 0; i < 3; i += 1) {
    if ((pa[i] ?? 0) !== (pb[i] ?? 0)) return (pa[i] ?? 0) - (pb[i] ?? 0)
  }
  return 0
}

export function highestStableForMajor(versions, major) {
  const match = versions
    .filter((v) => !v.includes('-') && v.startsWith(`${major}.`))
    .sort(compareVersions)
  return match.length ? match[match.length - 1] : null
}

export function shouldBypassProxy(hostname, noProxy) {
  if (!noProxy) return false
  return noProxy
    .split(',')
    .map((entry) => entry.trim().toLowerCase())
    .filter(Boolean)
    .some((entry) => {
      if (entry === '*') return true
      const bare = entry.startsWith('.') ? entry.slice(1) : entry
      const host = hostname.toLowerCase()
      return host === bare || host.endsWith(`.${bare}`)
    })
}

function proxyForRequest(targetUrl) {
  const noProxy = process.env.NO_PROXY ?? process.env.no_proxy ?? ''
  if (shouldBypassProxy(targetUrl.hostname, noProxy)) return null
  const proxy = process.env.HTTPS_PROXY ?? process.env.https_proxy ?? ''
  return proxy ? new URL(proxy) : null
}

function connectThroughProxy(proxyUrl, targetUrl, timeoutMs) {
  return new Promise((resolve, reject) => {
    import('node:http').then((http) => {
      const request = http.request({
        host: proxyUrl.hostname,
        port: proxyUrl.port || 80,
        method: 'CONNECT',
        path: `${targetUrl.hostname}:${targetUrl.port || 443}`,
        headers: proxyUrl.username
          ? { 'Proxy-Authorization': `Basic ${Buffer.from(`${proxyUrl.username}:${proxyUrl.password}`).toString('base64')}` }
          : {},
        timeout: timeoutMs,
      })
      request.on('connect', (res, socket) => {
        if (res.statusCode !== 200) {
          socket.destroy()
          reject(new Error(`Proxy CONNECT failed with status ${res.statusCode}`))
          return
        }
        resolve(socket)
      })
      request.on('timeout', () => { request.destroy(new Error('Proxy CONNECT timed out')) })
      request.on('error', reject)
      request.end()
    }, reject)
  })
}

async function fetchJson(url, timeoutMs) {
  const targetUrl = new URL(url)
  const proxyUrl = proxyForRequest(targetUrl)
  const socket = proxyUrl ? await connectThroughProxy(proxyUrl, targetUrl, timeoutMs) : null

  return new Promise((resolve, reject) => {
    const request = https.get(url, {
      headers: {
        'User-Agent': 'version-check/1',
        Accept: 'application/json',
      },
      ...(socket ? { socket, agent: false, servername: targetUrl.hostname } : {}),
    }, (response) => {
      if (response.statusCode !== 200) {
        response.resume()
        reject(new Error(`HTTP ${response.statusCode} from ${targetUrl.host}`))
        return
      }
      let data = ''
      response.setEncoding('utf8')
      response.on('data', (chunk) => { data += chunk })
      response.on('end', () => {
        try { resolve(JSON.parse(data)) }
        catch { reject(new Error('Registry returned a body that is not JSON')) }
      })
    })
    request.setTimeout(timeoutMs, () => {
      request.destroy(new Error(`Request timed out after ${timeoutMs} ms`))
    })
    request.on('error', reject)
  })
}

export function summarize(name, payload) {
  const distTags = payload['dist-tags'] ?? {}
  const latest = distTags.latest
  const info = { latest: latest ?? null, publishedAt: latest ? payload.time?.[latest] ?? null : null }
  if (SHOW_ALL_TAGS.has(name)) info.distTags = distTags

  const majors = RESOLVE_STABLE_MAJORS[name]
  if (majors) {
    const allVersions = Object.keys(payload.versions ?? {})
    info.latestStableByMajor = {}
    for (const major of majors) {
      const stable = highestStableForMajor(allVersions, major)
      info.latestStableByMajor[`v${major}`] = stable
        ? { version: stable, publishedAt: payload.time?.[stable] ?? null }
        : null
    }
  }

  if (PEER_RANGES_FOR.has(name) && latest && payload.versions?.[latest]) {
    const manifest = payload.versions[latest]
    info.engines = manifest.engines ?? null
    info.peerDependencies = manifest.peerDependencies ?? null
  }
  return info
}

async function getPackageInfo(name, timeoutMs, retries) {
  const url = `https://registry.npmjs.org/${encodeURIComponent(name)}`
  let lastError
  for (let attempt = 0; attempt <= retries; attempt += 1) {
    try { return summarize(name, await fetchJson(url, timeoutMs)) }
    catch (error) { lastError = error }
  }
  throw lastError
}

async function main() {
  let options
  try { options = parseArguments(process.argv.slice(2)) }
  catch (error) {
    console.error(error.message)
    console.error('Run with --help for usage.')
    process.exitCode = EXIT_USAGE
    return
  }

  if (options.help) { console.log(HELP); return }

  const names = options.packages.length ? options.packages : PACKAGES
  const result = {
    checkedAt: new Date().toISOString(),
    ok: true,
    errors: [],
    note: 'Installed versions decide behaviour. This is registry state, not what the target repository has installed. Detect the installed @quasar/app-vite major before giving config or CLI advice.',
    packages: {},
  }

  const settled = await Promise.all(names.map(async (name) => {
    try { return { name, info: await getPackageInfo(name, options.timeoutMs, options.retries) } }
    catch (error) { return { name, error: error instanceof Error ? error.message : String(error) } }
  }))

  for (const entry of settled) {
    if (entry.error) {
      result.packages[entry.name] = { error: entry.error }
      result.errors.push({ package: entry.name, error: entry.error })
    } else {
      result.packages[entry.name] = entry.info
    }
  }

  result.ok = result.errors.length === 0
  console.log(JSON.stringify(result, null, 2))
  if (!result.ok) {
    console.error(`${result.errors.length} of ${names.length} packages could not be read; the rest are printed above. This run is NOT a clean check.`)
    process.exitCode = EXIT_PARTIAL
  } else {
    process.exitCode = EXIT_OK
  }
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : String(error))
  process.exitCode = 1
})
