#!/usr/bin/env node
// check-design-system.mjs -- deterministic checks for the rules in
// alaa-ui-ux-design-system. A design rule with no tool that reports its
// violation is a preference; this script is what makes several of them rules.
//
// No dependencies. Node 18+. Reads only; never writes inside the target repo.

import { readdirSync, readFileSync, statSync, mkdtempSync, mkdirSync, writeFileSync, rmSync } from "node:fs";
import { join, extname, relative, resolve } from "node:path";
import { tmpdir } from "node:os";

const EXIT_CLEAN = 0;
const EXIT_VIOLATIONS = 1;
const EXIT_COULD_NOT_RUN = 2;
const EXIT_SELF_TEST_FAILED = 3;

const SKIP_DIRS = new Set([
  "node_modules", "dist", "build", "coverage", ".git", ".quasar", ".nx",
  ".idea", ".vscode", ".tmp", ".temp", ".playwright-mcp", "__pycache__", "public"
]);

const SOURCE_EXT = new Set([".vue", ".scss", ".css", ".sass", ".ts", ".tsx", ".js"]);
const STYLE_EXT = new Set([".vue", ".scss", ".css", ".sass"]);

// Files allowed to hold raw values: they are the theme source of truth.
const THEME_FILE_HINTS = [
  "style.css", "tokens", "theme", "variables", "palette", "default-light", "default-dark"
];

// ---------------------------------------------------------------- utilities

function walk(root, out = []) {
  let entries;
  try {
    entries = readdirSync(root, { withFileTypes: true });
  } catch {
    return out;
  }
  for (const e of entries) {
    if (e.isDirectory()) {
      if (SKIP_DIRS.has(e.name)) continue;
      walk(join(root, e.name), out);
    } else if (e.isFile() && SOURCE_EXT.has(extname(e.name))) {
      out.push(join(root, e.name));
    }
  }
  return out;
}

function isThemeFile(path) {
  const lower = path.toLowerCase();
  return THEME_FILE_HINTS.some(h => lower.includes(h));
}

function isCommentLine(line) {
  const t = line.trim();
  return t.startsWith("//") || t.startsWith("*") || t.startsWith("/*") ||
         t.startsWith("<!--") || t.startsWith("#");
}

// ------------------------------------------------------------ colour maths

function srgbToLinear(c) {
  const v = c / 255;
  return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
}

function parseColor(value) {
  const v = String(value).trim().toLowerCase();
  let m = /^#([0-9a-f]{3}|[0-9a-f]{6})$/.exec(v);
  if (m) {
    let h = m[1];
    if (h.length === 3) h = h.split("").map(c => c + c).join("");
    return [parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16), parseInt(h.slice(4, 6), 16)];
  }
  m = /^rgba?\(\s*([\d.]+)[\s,]+([\d.]+)[\s,]+([\d.]+)/.exec(v);
  if (m) return [Number(m[1]), Number(m[2]), Number(m[3])];
  m = /^oklch\(\s*([\d.]+%?)\s+([\d.]+)\s+([\d.]+)/.exec(v);
  if (m) {
    const L = m[1].endsWith("%") ? parseFloat(m[1]) / 100 : Number(m[1]);
    return oklchToRgb(L, Number(m[2]), Number(m[3]));
  }
  return null;
}

function oklchToRgb(L, C, H) {
  const a = C * Math.cos((H * Math.PI) / 180);
  const b = C * Math.sin((H * Math.PI) / 180);
  const l_ = L + 0.3963377774 * a + 0.2158037573 * b;
  const m_ = L - 0.1055613458 * a - 0.0638541728 * b;
  const s_ = L - 0.0894841775 * a - 1.291485548 * b;
  const l = l_ ** 3, m = m_ ** 3, s = s_ ** 3;
  const lin = [
    4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
    -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
    -0.0041960863 * l - 0.7034186147 * m + 1.707614701 * s
  ];
  return lin.map(c => {
    const v = c <= 0.0031308 ? 12.92 * c : 1.055 * Math.pow(c, 1 / 2.4) - 0.055;
    return Math.max(0, Math.min(255, Math.round(v * 255)));
  });
}

function luminance(rgb) {
  const [r, g, b] = rgb.map(srgbToLinear);
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

function contrastRatio(a, b) {
  const la = luminance(a), lb = luminance(b);
  const hi = Math.max(la, lb), lo = Math.min(la, lb);
  return (hi + 0.05) / (lo + 0.05);
}

// ------------------------------------------------------- CSS custom props

function parseCustomPropertyBlocks(css) {
  const blocks = [];
  const re = /([^{}]+)\{([^{}]*)\}/g;
  let m;
  while ((m = re.exec(css)) !== null) {
    const selector = m[1].trim().split("\n").pop().trim();
    const body = m[2];
    if (!body.includes("--")) continue;
    const props = new Map();
    const pre = /(--[a-z0-9-]+)\s*:\s*([^;]+);/gi;
    let p;
    while ((p = pre.exec(body)) !== null) {
      props.set(p[1], p[2].trim().replace(/\s+/g, " "));
    }
    if (props.size === 0) continue;
    const line = css.slice(0, m.index).split("\n").length;
    blocks.push({ selector, props, line });
  }
  return blocks;
}

// Token families whose values do not depend on the theme.
const THEME_INVARIANT = /^--[a-z]*-?(spacing|space|radius|typography|font|line-height|letter|layout|z-index|zindex|breakpoint|motion|duration|ease)\b/i;

function isThemeInvariant(name) {
  return THEME_INVARIANT.test(name) ||
    /-(spacing|radius|font-size|font-weight|line-height|font-family)-/.test(name);
}

function resolveValue(name, props, depth = 0) {
  if (depth > 6) return null;
  const raw = props.get(name);
  if (!raw) return null;
  const direct = parseColor(raw);
  if (direct) return direct;
  const varRef = /^var\(\s*(--[a-z0-9-]+)/i.exec(raw);
  if (varRef) return resolveValue(varRef[1], props, depth + 1);
  return null;
}

// ------------------------------------------------------------ check: tokens

const RAW_COLOR_RE = /(#[0-9a-fA-F]{3}\b|#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{8}\b|\brgba?\([^)]*\)|\bhsla?\([^)]*\)|\boklch\([^)]*\))/g;
const ARBITRARY_UTILITY_RE = /\b(?:bg|text|border|z|w|h|p|m|gap|rounded|shadow)-\[[^\]]+\]/g;
const RAW_ZINDEX_RE = /(?:^|[^-\w])z-index\s*:\s*(-?\d+)/gi;

function checkTokens(files, opts) {
  const findings = [];
  for (const f of files) {
    if (!STYLE_EXT.has(extname(f))) continue;
    if (isThemeFile(f)) continue;
    const lines = readFileSync(f, "utf8").split("\n");
    lines.forEach((line, i) => {
      if (isCommentLine(line)) return;
      // A line declaring a custom property is defining a token, not consuming one.
      if (/^\s*--[a-z0-9-]+\s*:/i.test(line)) return;
      for (const m of line.matchAll(RAW_COLOR_RE)) {
        if (/^(#fff|#ffffff|#000|#000000)$/i.test(m[0]) && opts.allowBlackWhite) continue;
        findings.push({ file: f, line: i + 1, rule: "raw-color", detail: m[0].trim() });
      }
      for (const m of line.matchAll(ARBITRARY_UTILITY_RE)) {
        findings.push({ file: f, line: i + 1, rule: "arbitrary-utility", detail: m[0] });
      }
      for (const m of line.matchAll(RAW_ZINDEX_RE)) {
        findings.push({ file: f, line: i + 1, rule: "raw-z-index", detail: `z-index: ${m[1]}` });
      }
    });
  }
  return findings;
}

// ------------------------------------------------------------ check: themes

function checkThemes(files) {
  const findings = [];
  const themeFiles = files.filter(f => isThemeFile(f) && /\.(css|scss|sass)$/.test(f));
  if (themeFiles.length === 0) {
    return { findings, ran: false, reason: "no theme stylesheet found (looked for style.css, tokens*, theme*, variables*)" };
  }
  for (const f of themeFiles) {
    const blocks = parseCustomPropertyBlocks(readFileSync(f, "utf8"));
    if (blocks.length < 2) continue;
    const base = blocks.reduce((a, b) => (b.props.size > a.props.size ? b : a), blocks[0]);
    for (const blk of blocks) {
      if (blk === base) continue;
      const missing = [];
      for (const name of base.props.keys()) {
        if (isThemeInvariant(name)) continue;
        if (!blk.props.has(name)) missing.push(name);
      }
      if (missing.length) {
        findings.push({
          file: f, line: blk.line, rule: "incomplete-theme",
          detail: `theme block "${blk.selector}" omits ${missing.length} theme-dependent role(s) declared in "${base.selector}": ${missing.join(", ")}`
        });
      }
    }
  }
  return { findings, ran: true };
}

// ---------------------------------------------------------- check: contrast

function derivePairs(props) {
  const names = [...props.keys()];
  const pairs = [];
  const has = n => props.has(n);

  for (const n of names) {
    const m = /^(--.*?)on-(.+)$/.exec(n);
    if (m) {
      const fill = m[1] + m[2];
      if (has(fill)) pairs.push([n, fill, 4.5, "on-role / fill"]);
    }
  }
  for (const n of names) {
    if (!n.endsWith("-text")) continue;
    const bg = n.replace(/-text$/, "-bg");
    if (has(bg)) pairs.push([n, bg, 4.5, "family text / family bg"]);
  }
  // A role is a foreground candidate only if it names text. A role naming a
  // surface or a background is never a foreground, even when it ends in
  // "-muted" -- pairing two surfaces at a text threshold is noise, and a
  // checker that reports noise gets switched off.
  const isSurfaceName = n => /(surface|background|-bg$|page$|panel)/.test(n);
  const fgs = names.filter(n =>
    (/-(foreground|text|ink|body|heading|muted)$/.test(n) || /-text-/.test(n)) && !isSurfaceName(n));
  // An inverse surface (dark, code, inverse) carries inverse text, and nothing
  // in the role names says which. Cross-pairing ordinary foregrounds against it
  // produces guaranteed failures that are not defects. It needs an explicit
  // on-* role instead, and the absence of one is the finding.
  const isInverse = n => /(dark|code|inverse|invert|scrim|overlay)/.test(n);
  const bgs = names.filter(n => isSurfaceName(n) && !/-(foreground|text|ink)$/.test(n) && !isInverse(n));
  for (const fg of fgs) for (const bg of bgs) pairs.push([fg, bg, 4.5, "text / surface"]);
  for (const n of names) {
    if (!/border-strong$|ring$/.test(n)) continue;
    for (const bg of bgs) pairs.push([n, bg, 3.0, "boundary / surface"]);
  }
  return pairs;
}

// An inverse surface with no on-* counterpart cannot be checked, and cannot be
// used safely either: nothing states which foreground belongs on it.
function unpairedInverseSurfaces(props) {
  const names = [...props.keys()];
  const out = [];
  for (const n of names) {
    if (!/(surface|background|-bg$)/.test(n)) continue;
    if (!/(dark|code|inverse|invert)/.test(n)) continue;
    const onName = n.replace(/^(--[a-z]*-?)/, "$1on-");
    const alt = n.replace(/(--.*?)([a-z-]+)$/, "$1on-$2");
    if (!props.has(onName) && !props.has(alt)) out.push(n);
  }
  return out;
}

function checkContrast(files) {
  const findings = [];
  const rows = [];
  const themeFiles = files.filter(f => isThemeFile(f) && /\.(css|scss|sass)$/.test(f));
  if (themeFiles.length === 0) {
    return { findings, rows, ran: false, reason: "no theme stylesheet found" };
  }
  let anyPair = false;
  for (const f of themeFiles) {
    const blocks = parseCustomPropertyBlocks(readFileSync(f, "utf8"));
    if (!blocks.length) continue;
    const base = blocks.reduce((a, b) => (b.props.size > a.props.size ? b : a), blocks[0]);
    for (const blk of blocks) {
      const merged = new Map(base.props);
      for (const [k, v] of blk.props) merged.set(k, v);
      for (const name of unpairedInverseSurfaces(blk.props)) {
        findings.push({
          file: f, line: blk.line, rule: "unpaired-inverse-surface",
          detail: `${blk.selector}: ${name} is an inverse surface with no on-* role, so no foreground is declared for it and its contrast cannot be checked`
        });
      }
      for (const [fgName, bgName, min, kind] of derivePairs(merged)) {
        const fg = resolveValue(fgName, merged);
        const bg = resolveValue(bgName, merged);
        if (!fg || !bg) continue;
        anyPair = true;
        const r = contrastRatio(fg, bg);
        rows.push({ file: f, theme: blk.selector, fgName, bgName, ratio: r, min, kind });
        if (r < min) {
          findings.push({
            file: f, line: blk.line, rule: "contrast",
            detail: `${blk.selector}: ${fgName} on ${bgName} = ${r.toFixed(2)}:1, needs ${min}:1 (${kind})`
          });
        }
      }
    }
  }
  if (!anyPair) return { findings, rows, ran: false, reason: "theme stylesheet found but no resolvable role pairs in it" };
  return { findings, rows, ran: true };
}

// ------------------------------------------------------------- check: icons

const DIRECTIONAL_ICON_RE = new RegExp(
  String.raw`\b((?:arrow|caret|chevron|arrow-line|arrow-fat|arrow-bend|arrow-u|arrow-square|caret-double|caret-circle)[a-z-]*-(?:left|right))\b`,
  "gi"
);
const DIRECTION_AWARE_HINT = /\b(isRtl|is-rtl|dir\s*===|direction\s*===|useDirection|directionHelpers|logicalIcon|resolveIcon|mirror|scaleX)\b/;

function checkIcons(files) {
  const findings = [];
  for (const f of files) {
    const ext = extname(f);
    if (![".vue", ".ts", ".tsx", ".js"].includes(ext)) continue;
    const text = readFileSync(f, "utf8");
    const lines = text.split("\n");
    const fileIsDirectionAware = DIRECTION_AWARE_HINT.test(text);
    lines.forEach((line, i) => {
      if (isCommentLine(line)) return;
      for (const m of line.matchAll(DIRECTIONAL_ICON_RE)) {
        if (fileIsDirectionAware && DIRECTION_AWARE_HINT.test(line)) continue;
        findings.push({
          file: f, line: i + 1, rule: "unmirrored-icon",
          detail: `"${m[1]}" names a physical direction at a call site; resolve by logical role instead`
        });
      }
    });
  }
  return findings;
}

// -------------------------------------------------------------- check: bidi

const BIDI_CONTROLS = {
  "‎": "U+200E LRM", "‏": "U+200F RLM", "⁦": "U+2066 LRI",
  "⁧": "U+2067 RLI", "⁨": "U+2068 FSI", "⁩": "U+2069 PDI"
};

function checkBidi(files) {
  const findings = [];
  for (const f of files) {
    if (/fixture|__tests__|\.spec\.|\.test\./.test(f)) continue;
    const lines = readFileSync(f, "utf8").split("\n");
    lines.forEach((line, i) => {
      for (const [ch, label] of Object.entries(BIDI_CONTROLS)) {
        if (line.includes(ch)) {
          findings.push({ file: f, line: i + 1, rule: "bidi-control-character", detail: `${label} in source; set direction in CSS instead` });
        }
      }
    });
  }
  return findings;
}

// ----------------------------------------------------------- starter palettes

const STARTER_PALETTES = {
  "SaaS / trust": { primary: "#2563EB", "on-primary": "#FFFFFF", accent: "#EA580C", "on-accent": "#430D00", background: "#F8FAFC", surface: "#FFFFFF", foreground: "#1E293B", "muted-foreground": "#64748B", "border-subtle": "#E2E8F0", "border-strong": "#8F949C", destructive: "#DC2626" },
  "Dashboard / ops": { primary: "#3730A3", "on-primary": "#FFFFFF", accent: "#0D9488", "on-accent": "#00201C", background: "#F1F5F9", surface: "#FFFFFF", foreground: "#0F172A", "muted-foreground": "#475569", "border-subtle": "#CBD5E1", "border-strong": "#8B94A0", destructive: "#B91C1C" },
  "Premium (dark-first)": { primary: "#E7E5E4", "on-primary": "#1C1917", accent: "#C9A962", "on-accent": "#4C3F25", background: "#0C0A09", surface: "#1C1917", foreground: "#FAFAF9", "muted-foreground": "#A8A29E", "border-subtle": "#292524", "border-strong": "#6A6664", destructive: "#F87171" },
  "Playful / education": { primary: "#7C3AED", "on-primary": "#FFFFFF", accent: "#D47F00", "on-accent": "#442400", background: "#FEFCE8", surface: "#FFFFFF", foreground: "#292524", "muted-foreground": "#57534E", "border-subtle": "#E7E5E4", "border-strong": "#959393", destructive: "#DC2626" }
};

function checkPalettes() {
  const findings = [];
  const rows = [];
  for (const [name, p] of Object.entries(STARTER_PALETTES)) {
    const checks = [
      ["on-primary", "primary", 4.5], ["on-accent", "accent", 4.5],
      ["foreground", "surface", 4.5], ["foreground", "background", 4.5],
      ["muted-foreground", "surface", 4.5], ["destructive", "surface", 4.5],
      ["accent", "surface", 3.0], ["primary", "surface", 3.0],
      ["border-strong", "surface", 3.0]
    ];
    for (const [fg, bg, min] of checks) {
      const r = contrastRatio(parseColor(p[fg]), parseColor(p[bg]));
      rows.push({ palette: name, fg, bg, ratio: r, min });
      if (r < min) findings.push({ file: "references/32-starter-palettes.md", line: 0, rule: "palette-contrast", detail: `${name}: ${fg} on ${bg} = ${r.toFixed(2)}:1, needs ${min}:1` });
    }
  }
  return { findings, rows };
}

// ------------------------------------------------------------------ output

function printFindings(findings, root) {
  for (const f of findings) {
    const where = f.line ? `${relative(root, f.file) || f.file}:${f.line}` : f.file;
    console.log(`${where}  [${f.rule}]  ${f.detail}`);
  }
}

const HELP = `check-design-system.mjs -- deterministic checks for alaa-ui-ux-design-system

USAGE
  node scripts/check-design-system.mjs [CHECKS...] [--root <dir>] [<dir>]

CHECKS (default: --all)
  --all            every check below except --palettes
  --tokens         raw colour, arbitrary-utility and raw z-index values in
                   components (theme files are exempt)
  --themes         a theme block that omits a theme-dependent role declared
                   in the base block
  --contrast       every derivable foreground/fill pair, per theme block,
                   against its WCAG minimum
  --icons          physical-direction icon names written at a call site with
                   no direction-aware resolution
  --bidi           bidi control characters (U+200E, U+200F, U+2066-U+2069)
                   in source
  --palettes       recompute and print the ratios in
                   references/32-starter-palettes.md (needs no repo)

OPTIONS
  --root <dir>     repository root to scan. Defaults to the current working
                   directory. A bare positional argument is also accepted.
  --quiet          suppress the per-pair contrast table and the summary
  --self-test      run against built-in fixtures in the system temp directory
                   (never inside the target repo) and verify each check finds
                   what it should
  -h, --help       this text

EXIT CODES
  0  clean          every requested check ran and found nothing
  1  violations     at least one check ran and found something
  2  could not run  bad arguments, unreadable root, or a check had no input
                    (for example --contrast with no theme stylesheet). This is
                    deliberately distinct from 0: an unrun check is never
                    reported as clean.
  3  self-test failed
`;

// ------------------------------------------------------------------ self-test

function selfTest() {
  const dir = mkdtempSync(join(tmpdir(), "alaa-ds-selftest-"));
  let failures = 0;
  const expect = (name, cond, detail) => {
    if (cond) { console.log(`  PASS  ${name}`); }
    else { console.log(`  FAIL  ${name}${detail ? " -- " + detail : ""}`); failures++; }
  };
  try {
    mkdirSync(join(dir, "src", "theme"), { recursive: true });

    writeFileSync(join(dir, "src", "Bad.scss"), [
      ".card {",
      "  color: #1E293B;",
      "  background: rgb(255, 0, 0);",
      "  z-index: 9999;",
      "}",
      "// color: #ABCDEF in a comment must not be reported",
      ".ok { color: var(--alaa-color-text); }"
    ].join("\n"));

    writeFileSync(join(dir, "src", "Good.scss"), ".ok { color: var(--fg); background: var(--surface); }\n");
    writeFileSync(join(dir, "src", "Arb.vue"), '<template><div class="bg-[#123456] z-[9999]" /></template>\n');

    writeFileSync(join(dir, "src", "theme", "style.css"), [
      ":root {",
      "  --alaa-color-accent: #F59E0B;",
      "  --alaa-color-on-accent: #FFFFFF;",
      "  --alaa-color-surface: #FFFFFF;",
      "  --alaa-color-foreground: #1E293B;",
      "  --alaa-feedback-warning-text: #92400E;",
      "  --alaa-feedback-warning-bg: #FFFBEB;",
      "  --alaa-spacing-md: 1rem;",
      "}",
      '[data-theme="dark"] {',
      "  --alaa-color-accent: #FFB240;",
      "  --alaa-color-on-accent: #3A2400;",
      "  --alaa-color-surface: #0F172A;",
      "  --alaa-color-foreground: #F8FAFC;",
      "}"
    ].join("\n"));

    writeFileSync(join(dir, "src", "Icons.vue"), [
      "<template>",
      '  <q-icon name="ph:arrow-left" />',
      '  <q-icon name="ph:caret-right" />',
      '  <q-icon name="ph:check-circle" />',
      "  <q-icon :name=\"isRtl ? 'ph:arrow-left' : 'ph:arrow-right'\" />",
      "</template>"
    ].join("\n"));

    // The fixture holds the real U+200E code point, written as an escape so
    // this file stays pure ASCII and survives any transport.
    writeFileSync(join(dir, "src", "Bidi.ts"), "export const label = \"‎-marked\";\n");

    const files = walk(dir);
    expect("walk finds fixture files", files.length >= 6, `found ${files.length}`);

    const tok = checkTokens(files, {});
    expect("tokens: reports the raw hex", tok.some(f => f.rule === "raw-color" && f.detail === "#1E293B"));
    expect("tokens: reports the rgb() literal", tok.some(f => f.rule === "raw-color" && f.detail.startsWith("rgb(")));
    expect("tokens: reports the raw z-index", tok.some(f => f.rule === "raw-z-index"));
    expect("tokens: reports the arbitrary utility", tok.some(f => f.rule === "arbitrary-utility"));
    expect("tokens: ignores a comment line", !tok.some(f => f.detail === "#ABCDEF"));
    expect("tokens: ignores the theme file", !tok.some(f => f.file.includes("theme")));
    expect("tokens: ignores a var() consumer", !tok.some(f => f.file.endsWith("Good.scss")));

    const th = checkThemes(files);
    expect("themes: ran", th.ran === true, th.reason);
    expect("themes: reports the omitted warning roles",
      th.findings.some(f => f.detail.includes("--alaa-feedback-warning-text") && f.detail.includes("--alaa-feedback-warning-bg")));
    expect("themes: does not report the theme-invariant spacing token",
      !th.findings.some(f => f.detail.includes("--alaa-spacing-md")));

    const ct = checkContrast(files);
    expect("contrast: ran", ct.ran === true, ct.reason);
    expect("contrast: reports white on the light accent",
      ct.findings.some(f => f.detail.includes("on-accent") && f.detail.includes(":root")));
    expect("contrast: passes the dark accent pair",
      !ct.findings.some(f => f.detail.includes('data-theme="dark"') && f.detail.includes("on-accent")));

    const ic = checkIcons(files);
    expect("icons: reports the literal arrow-left", ic.some(f => f.detail.includes("arrow-left")));
    expect("icons: reports the literal caret-right", ic.some(f => f.detail.includes("caret-right")));
    expect("icons: ignores check-circle", !ic.some(f => f.detail.includes("check-circle")));
    expect("icons: ignores the direction-aware line", ic.filter(f => f.line === 5).length === 0, "line 5 should be exempt");

    const bd = checkBidi(files);
    expect("bidi: reports the LRM", bd.some(f => f.detail.includes("U+200E")));

    const pal = checkPalettes();
    expect("palettes: all shipped rows pass", pal.findings.length === 0, pal.findings.map(f => f.detail).join("; "));
    expect("palettes: produced a row set", pal.rows.length === 36, `${pal.rows.length} rows`);

    const empty = mkdtempSync(join(tmpdir(), "alaa-ds-empty-"));
    try {
      const r = checkThemes(walk(empty));
      expect("themes: reports could-not-run on an empty tree", r.ran === false);
    } finally {
      rmSync(empty, { recursive: true, force: true });
    }
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
  console.log(failures === 0 ? "\nself-test: PASS" : `\nself-test: FAIL (${failures})`);
  return failures === 0 ? EXIT_CLEAN : EXIT_SELF_TEST_FAILED;
}

// ----------------------------------------------------------------- main

function main(argv) {
  const args = argv.slice(2);
  if (args.includes("-h") || args.includes("--help")) { console.log(HELP); return EXIT_CLEAN; }
  if (args.includes("--self-test")) return selfTest();

  const quiet = args.includes("--quiet");
  let root = null;
  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--root") { root = args[i + 1]; i++; }
    else if (!args[i].startsWith("--")) root = args[i];
  }
  root = resolve(root || process.cwd());

  const wanted = new Set(args.filter(a => a.startsWith("--") && a !== "--quiet" && a !== "--root"));
  const palettesOnly = wanted.has("--palettes") && wanted.size === 1;
  const all = wanted.size === 0 || wanted.has("--all");

  if (palettesOnly) {
    const { findings, rows } = checkPalettes();
    let current = "";
    for (const r of rows) {
      if (r.palette !== current) { current = r.palette; console.log(`\n${current}`); }
      console.log(`  ${(r.fg + " on " + r.bg).padEnd(38)} ${r.ratio.toFixed(2).padStart(6)}:1  need ${r.min}  ${r.ratio >= r.min ? "PASS" : "FAIL"}`);
    }
    console.log(findings.length ? `\n${findings.length} palette pair(s) FAIL` : "\nall palette pairs pass");
    return findings.length ? EXIT_VIOLATIONS : EXIT_CLEAN;
  }

  let st;
  try { st = statSync(root); } catch { console.error(`could not run: cannot read root ${root}`); return EXIT_COULD_NOT_RUN; }
  if (!st.isDirectory()) { console.error(`could not run: root is not a directory ${root}`); return EXIT_COULD_NOT_RUN; }

  const files = walk(root);
  if (files.length === 0) {
    console.error(`could not run: no .vue/.scss/.css/.ts source files under ${root}`);
    return EXIT_COULD_NOT_RUN;
  }

  const findings = [];
  const couldNotRun = [];
  const summary = [];

  if (all || wanted.has("--tokens")) {
    const f = checkTokens(files, {});
    findings.push(...f); summary.push(["tokens", f.length, "ran"]);
  }
  if (all || wanted.has("--themes")) {
    const r = checkThemes(files);
    if (!r.ran) { couldNotRun.push(`themes: ${r.reason}`); summary.push(["themes", 0, "COULD NOT RUN"]); }
    else { findings.push(...r.findings); summary.push(["themes", r.findings.length, "ran"]); }
  }
  if (all || wanted.has("--contrast")) {
    const r = checkContrast(files);
    if (!r.ran) { couldNotRun.push(`contrast: ${r.reason}`); summary.push(["contrast", 0, "COULD NOT RUN"]); }
    else {
      findings.push(...r.findings);
      summary.push(["contrast", r.findings.length, `ran (${r.rows.length} pairs)`]);
      if (!quiet) {
        console.log("--- contrast, every resolvable pair ---");
        for (const row of r.rows) {
          console.log(`  ${row.theme.padEnd(24)} ${(row.fgName + " on " + row.bgName).padEnd(56)} ${row.ratio.toFixed(2).padStart(6)}:1 need ${row.min} ${row.ratio >= row.min ? "PASS" : "FAIL"}`);
        }
        console.log("");
      }
    }
  }
  if (all || wanted.has("--icons")) {
    const f = checkIcons(files);
    findings.push(...f); summary.push(["icons", f.length, "ran"]);
  }
  if (all || wanted.has("--bidi")) {
    const f = checkBidi(files);
    findings.push(...f); summary.push(["bidi", f.length, "ran"]);
  }

  printFindings(findings, root);

  if (!quiet) {
    console.log(`\n--- summary for ${root} (${files.length} source files) ---`);
    for (const [name, n, state] of summary) console.log(`  ${name.padEnd(10)} ${String(n).padStart(5)} finding(s)  ${state}`);
  }
  for (const c of couldNotRun) console.error(`COULD NOT RUN -- ${c}`);

  if (couldNotRun.length) return EXIT_COULD_NOT_RUN;
  return findings.length ? EXIT_VIOLATIONS : EXIT_CLEAN;
}

process.exit(main(process.argv));
