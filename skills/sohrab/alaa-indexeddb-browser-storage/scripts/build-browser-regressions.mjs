#!/usr/bin/env node
// Node 24+. Prepare an isolated real-IndexedDB harness; does not serve or open it.
import { mkdir, readFile, readdir, writeFile, copyFile } from 'node:fs/promises';
import { resolve, join } from 'node:path';
import { stripTypeScriptTypes } from 'node:module';

const destination = process.argv[2];
if (!destination) throw new Error('Usage: node build-browser-regressions.mjs <new-output-directory>');
const root = resolve(destination);
await mkdir(root); // Refuse an existing directory instead of replacing unrelated artifacts.
await mkdir(join(root, 'examples'));
for (const file of await readdir(new URL('../examples/', import.meta.url))) {
  if (!file.endsWith('.ts') || file.endsWith('.test.ts')) continue;
  const source = await readFile(new URL(`../examples/${file}`, import.meta.url), 'utf8');
  const javascript = stripTypeScriptTypes(source, { mode: 'transform' })
    .replace(/(from\s+['"]\.\/[^'"]+)(['"])/g, '$1.js$2');
  await writeFile(join(root, 'examples', file.replace(/\.ts$/, '.js')), javascript);
}
await copyFile(new URL('./browser-storage-cases.mjs', import.meta.url), join(root, 'cases.mjs'));
await writeFile(join(root, 'index.html'), `<!doctype html>
<html lang="en"><meta charset="utf-8"><title>IndexedDB example regression harness</title>
<h1>IndexedDB example regressions</h1><p>Uses isolated test databases on this origin. No network or application data.</p>
<pre id="result">RUNNING</pre><script type="module">
import { runStorageCases } from './cases.mjs';
const output = document.querySelector('#result');
const results = await runStorageCases();
output.textContent = JSON.stringify(results, null, 2);
document.title = results.every(row => row.status === 'PASS') ? 'PASS IndexedDB' : 'FAIL IndexedDB';
</script></html>`);
console.log(`Prepared isolated browser harness: ${root}`);
