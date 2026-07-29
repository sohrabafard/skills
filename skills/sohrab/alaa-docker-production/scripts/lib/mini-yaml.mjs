// A deliberately small YAML reader for Compose and Swarm stack files.
//
// Why not a YAML library: the checkers must run from a fresh checkout with no `npm install`, on
// Windows, against a read-only tree. A dependency-free reader that supports exactly the subset
// Compose files use, and refuses everything else, is safer than a full parser that guesses.
//
// Supported: block mappings, block sequences, single-line flow sequences and single-line flow
// mappings, single- and double-quoted scalars, plain scalars, comments, one leading document
// marker.
//
// Refused, with a CannotRun error rather than a silent misparse: tab indentation, anchors and
// aliases (`&a`, `*a`), merge keys (`<<`), block scalars (`|`, `>`), a flow collection spanning
// more than one line, multiple documents. Refusing is the point: a checker that quietly misparses its input and then
// reports "clean" is the worst outcome available to it.

import { CannotRun, readLines } from './common.mjs';

const LINE = Symbol('line');
const LINES = Symbol('lines');

export { LINE, LINES };

/** Line number (1-based) at which `key` was defined on mapping node `node`, or 0. */
export function lineOf(node, key) {
  if (!node || typeof node !== 'object') return 0;
  if (key === undefined) return node[LINE] || 0;
  return (node[LINES] && node[LINES][key]) || node[LINE] || 0;
}

export function parseComposeFile(file) {
  const lines = readLines(file);
  return parseLines(lines, file);
}

export function parseLines(lines, file = '<input>') {
  const items = [];
  let sawDocMarker = false;

  for (let i = 0; i < lines.length; i++) {
    const raw = lines[i];
    const lineNo = i + 1;
    if (raw.includes('\t') && /^\s*\t/.test(raw)) {
      throw new CannotRun(`${file}:${lineNo}: tab used for indentation; YAML forbids it`);
    }
    const stripped = stripComment(raw, file, lineNo);
    if (stripped.trim() === '') continue;
    if (stripped.trim() === '---') {
      if (sawDocMarker) throw new CannotRun(`${file}:${lineNo}: multiple YAML documents are not supported`);
      sawDocMarker = true;
      continue;
    }
    if (stripped.trim() === '...') continue;
    const indent = stripped.length - stripped.trimStart().length;
    const text = stripped.trim();
    for (const bad of ['&', '*', '<<:', '{']) {
      if (bad === '&' && /(^|:\s)&\S/.test(text)) {
        throw new CannotRun(`${file}:${lineNo}: YAML anchors are not supported by this checker`);
      }
      if (bad === '*' && /(^|:\s)\*\S/.test(text)) {
        throw new CannotRun(`${file}:${lineNo}: YAML aliases are not supported by this checker`);
      }
      if (bad === '<<:' && text.startsWith('<<:')) {
        throw new CannotRun(`${file}:${lineNo}: YAML merge keys are not supported by this checker`);
      }
    }
    if (/:\s*[|>][-+0-9]*\s*$/.test(text)) {
      throw new CannotRun(`${file}:${lineNo}: block scalars (| or >) are not supported by this checker`);
    }
    items.push({ indent, text, lineNo });
  }

  const cursor = { i: 0 };
  const root = parseBlock(items, cursor, items.length ? items[0].indent : 0, file);
  if (cursor.i < items.length) {
    throw new CannotRun(`${file}:${items[cursor.i].lineNo}: unexpected indentation; checker cannot parse this file`);
  }
  return root;
}

function stripComment(raw, file, lineNo) {
  let out = '';
  let quote = null;
  for (let i = 0; i < raw.length; i++) {
    const ch = raw[i];
    if (quote) {
      out += ch;
      if (ch === quote) quote = null;
      continue;
    }
    if (ch === '"' || ch === "'") {
      quote = ch;
      out += ch;
      continue;
    }
    if (ch === '#' && (i === 0 || /\s/.test(raw[i - 1]))) break;
    out += ch;
  }
  if (quote) throw new CannotRun(`${file}:${lineNo}: unterminated quote; checker cannot parse this file`);
  return out;
}

function parseBlock(items, cursor, indent, file) {
  if (cursor.i >= items.length) return null;
  if (items[cursor.i].text.startsWith('- ') || items[cursor.i].text === '-') {
    return parseSequence(items, cursor, indent, file);
  }
  return parseMapping(items, cursor, indent, file);
}

function parseMapping(items, cursor, indent, file) {
  const node = {};
  Object.defineProperty(node, LINE, { value: items[cursor.i].lineNo, enumerable: false });
  Object.defineProperty(node, LINES, { value: {}, enumerable: false });

  while (cursor.i < items.length) {
    const item = items[cursor.i];
    if (item.indent < indent) break;
    if (item.indent > indent) {
      throw new CannotRun(`${file}:${item.lineNo}: unexpected indentation inside a mapping`);
    }
    const m = /^("[^"]*"|'[^']*'|[^:]+):(\s+(.*))?$/.exec(item.text);
    if (!m) {
      if (item.text.startsWith('- ')) break;
      throw new CannotRun(`${file}:${item.lineNo}: cannot parse mapping entry: ${item.text}`);
    }
    const key = unquote(m[1].trim());
    const inline = m[3] === undefined ? '' : m[3].trim();
    node[LINES][key] = item.lineNo;
    cursor.i++;

    if (inline !== '') {
      node[key] = parseScalarOrFlow(inline, file, item.lineNo);
      continue;
    }
    const next = cursor.i < items.length ? items[cursor.i] : null;
    if (!next || next.indent <= indent) {
      node[key] = null;
      continue;
    }
    node[key] = parseBlock(items, cursor, next.indent, file);
  }
  return node;
}

function parseSequence(items, cursor, indent, file) {
  const list = [];
  Object.defineProperty(list, LINE, { value: items[cursor.i].lineNo, enumerable: false });
  while (cursor.i < items.length) {
    const item = items[cursor.i];
    if (item.indent < indent) break;
    if (item.indent > indent) throw new CannotRun(`${file}:${item.lineNo}: unexpected indentation inside a sequence`);
    if (!item.text.startsWith('- ') && item.text !== '-') break;
    const rest = item.text === '-' ? '' : item.text.slice(2).trim();
    cursor.i++;
    if (rest === '') {
      const next = cursor.i < items.length ? items[cursor.i] : null;
      list.push(next && next.indent > indent ? parseBlock(items, cursor, next.indent, file) : null);
      continue;
    }
    if (!rest.startsWith('{') && !rest.startsWith('[') && /^("[^"]*"|'[^']*'|[^:]+):(\s|$)/.test(rest)) {
      // "- key: value" starts a mapping whose effective indent is the dash column plus two.
      const synthetic = [{ indent: indent + 2, text: rest, lineNo: item.lineNo }];
      while (cursor.i < items.length && items[cursor.i].indent > indent && !items[cursor.i].text.startsWith('- ')) {
        synthetic.push(items[cursor.i]);
        cursor.i++;
      }
      const sub = { i: 0 };
      list.push(parseMapping(synthetic, sub, indent + 2, file));
      continue;
    }
    list.push(parseScalarOrFlow(rest, file, item.lineNo));
  }
  return list;
}

function parseScalarOrFlow(text, file, lineNo) {
  if (text.startsWith('[')) {
    if (!text.endsWith(']')) throw new CannotRun(`${file}:${lineNo}: multi-line flow sequence is not supported`);
    const inner = text.slice(1, -1).trim();
    if (inner === '') return [];
    return splitFlow(inner, file, lineNo).map((piece) => unquote(piece.trim()));
  }
  if (text.startsWith('{')) {
    if (!text.endsWith('}')) throw new CannotRun(`${file}:${lineNo}: multi-line flow mapping is not supported`);
    const node = {};
    Object.defineProperty(node, LINE, { value: lineNo, enumerable: false });
    Object.defineProperty(node, LINES, { value: {}, enumerable: false });
    const inner = text.slice(1, -1).trim();
    if (inner === '') return node;
    for (const piece of splitFlow(inner, file, lineNo)) {
      const entry = piece.trim();
      const m = /^("[^"]*"|'[^']*'|[^:]+):\s*([\s\S]*)$/.exec(entry);
      if (!m) throw new CannotRun(`${file}:${lineNo}: cannot parse flow-mapping entry: ${entry}`);
      const key = unquote(m[1].trim());
      node[LINES][key] = lineNo;
      node[key] = parseScalarOrFlow(m[2].trim(), file, lineNo);
    }
    return node;
  }
  return unquote(text);
}

function splitFlow(inner, file, lineNo) {
  const out = [];
  let cur = '';
  let quote = null;
  let depth = 0;
  for (const ch of inner) {
    if (quote) {
      cur += ch;
      if (ch === quote) quote = null;
      continue;
    }
    if (ch === '"' || ch === "'") {
      quote = ch;
      cur += ch;
      continue;
    }
    if (ch === '[' || ch === '{') depth++;
    if (ch === ']' || ch === '}') depth--;
    if (ch === ',' && depth === 0) {
      out.push(cur);
      cur = '';
      continue;
    }
    cur += ch;
  }
  if (quote) throw new CannotRun(`${file}:${lineNo}: unterminated quote in flow sequence`);
  out.push(cur);
  return out;
}

function unquote(text) {
  if (text.length >= 2 && text[0] === '"' && text[text.length - 1] === '"') return text.slice(1, -1);
  if (text.length >= 2 && text[0] === "'" && text[text.length - 1] === "'") return text.slice(1, -1);
  return text;
}
