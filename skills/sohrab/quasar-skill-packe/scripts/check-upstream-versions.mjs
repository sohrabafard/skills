#!/usr/bin/env node

import https from 'node:https'

const packages = [
  'quasar',
  '@quasar/app-vite',
  'vite',
  'vue',
  'vue-router',
  'workbox-build',
]

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
  const latest = payload['dist-tags']?.latest

  return {
    latest,
    publishedAt: latest ? payload.time?.[latest] ?? null : null,
  }
}

async function main() {
  const result = {
    checkedAt: new Date().toISOString(),
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
