#!/usr/bin/env node

// Refreshes the upstream version snapshot used by this skill pack.
// Package-manager-neutral: talks to the npm registry directly over HTTPS.
//
// For @quasar/app-vite it prints every dist-tag AND resolves the latest stable
// release per requested major. Two lines are live at once: v3 (currently the
// `latest` tag, in RC) and v2 (stable, production). The registry carries no
// dedicated v2 dist-tag, so the v2 production version is computed from the
// packument's version list (highest non-prerelease 2.x). The installed major
// decides whether v2 or v3 guidance applies; for production prefer stable v2.

import https from 'node:https'

const packages = [
  'quasar',
  '@quasar/app-vite',
  'vite',
  'vue',
  'vue-router',
  'pinia',
  'workbox-build',
]

// Packages where seeing all dist-tags matters (multiple supported lines).
const showAllTags = new Set(['@quasar/app-vite'])

// Packages where the latest *stable* release for a given major must be reported
// even when it is not on a dist-tag (the stable-first production line).
const resolveStableMajors = { '@quasar/app-vite': [2] }

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
    const request = https.get(
      url,
      {
        headers: {
          'User-Agent': 'codex-quasar-skill-packe',
          Accept: 'application/json',
        },
      },
      (response) => {
        if (response.statusCode !== 200) {
          reject(new Error(`Request failed for ${url} with status ${response.statusCode}`))
          response.resume()
          return
        }

        let data = ''

        response.setEncoding('utf8')
        response.on('data', (chunk) => {
          data += chunk
        })
        response.on('end', () => {
          try {
            resolve(JSON.parse(data))
          }
          catch (error) {
            reject(error)
          }
        })
      },
    )

    request.on('error', reject)
  })
}

async function getPackageInfo(name) {
  const url = `https://registry.npmjs.org/${encodeURIComponent(name)}`
  const payload = await fetchJson(url)
  const distTags = payload['dist-tags'] ?? {}
  const latest = distTags.latest

  const info = {
    latest,
    publishedAt: latest ? payload.time?.[latest] ?? null : null,
  }

  if (showAllTags.has(name)) {
    info.distTags = distTags
  }

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
    note: '@quasar/app-vite has two live lines: v3 (the `latest` dist-tag, RC) and v2 (stable/production, reported under latestStableByMajor.v2). For production prefer stable v2. Detect the installed major before giving config/CLI advice.',
    packages: {},
  }

  for (const name of packages) {
    result.packages[name] = await getPackageInfo(name)
  }

  console.log(JSON.stringify(result, null, 2))
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : String(error))
  process.exitCode = 1
})
