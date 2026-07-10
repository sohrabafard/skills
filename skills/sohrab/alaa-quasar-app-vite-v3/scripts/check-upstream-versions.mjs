#!/usr/bin/env node

// Package-manager-neutral npm snapshot. app-vite 3.0.1 became stable on
// 2026-07-07; report stable v2/v3 separately because v2 remains maintenance.
import https from 'node:https'

const packages = [
  'quasar', '@quasar/app-vite', '@quasar/extras', 'vite', 'vue',
  'vue-router', 'pinia', 'workbox-build', 'workbox-core',
]
const showAllTags = new Set(['@quasar/app-vite'])
const resolveStableMajors = { '@quasar/app-vite': [2, 3] }

function compareVersions(a, b) {
  const pa = a.split('.').map(Number)
  const pb = b.split('.').map(Number)
  for (let i = 0; i < 3; i += 1) {
    if ((pa[i] ?? 0) !== (pb[i] ?? 0)) return (pa[i] ?? 0) - (pb[i] ?? 0)
  }
  return 0
}

function highestStableForMajor(versions, major) {
  const match = versions
    .filter((v) => !v.includes('-') && v.startsWith(`${major}.`))
    .sort(compareVersions)
  return match.length ? match[match.length - 1] : null
}

function fetchJson(url) {
  return new Promise((resolve, reject) => {
    const request = https.get(url, {
      headers: {
        'User-Agent': 'alaa-quasar-app-vite-v3-skill',
        Accept: 'application/json',
      },
    }, (response) => {
      if (response.statusCode !== 200) {
        reject(new Error(`Request failed for ${url} with status ${response.statusCode}`))
        response.resume()
        return
      }
      let data = ''
      response.setEncoding('utf8')
      response.on('data', (chunk) => { data += chunk })
      response.on('end', () => {
        try { resolve(JSON.parse(data)) }
        catch (error) { reject(error) }
      })
    })
    request.on('error', reject)
  })
}

async function getPackageInfo(name) {
  const url = `https://registry.npmjs.org/${encodeURIComponent(name)}`
  const payload = await fetchJson(url)
  const distTags = payload['dist-tags'] ?? {}
  const latest = distTags.latest
  const info = { latest, publishedAt: latest ? payload.time?.[latest] ?? null : null }
  if (showAllTags.has(name)) info.distTags = distTags

  const majors = resolveStableMajors[name]
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
  return info
}

async function main() {
  const result = {
    checkedAt: new Date().toISOString(),
    note: '@quasar/app-vite v3 is the stable production line (holds the `latest` dist-tag). v2 is maintenance-only; latestStableByMajor.v2 exists for repos that have not migrated. Detect the installed major before giving config/CLI advice.',
    packages: {},
  }
  for (const name of packages) result.packages[name] = await getPackageInfo(name)
  console.log(JSON.stringify(result, null, 2))
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : String(error))
  process.exitCode = 1
})
