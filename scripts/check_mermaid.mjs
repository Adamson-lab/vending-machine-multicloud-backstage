// Parse every Mermaid diagram in the repo: diagrams/*.mmd and ```mermaid fences in *.md.
// Usage: node scripts/check_mermaid.mjs [repoRoot]
import { JSDOM } from 'jsdom';
import fs from 'fs';
import path from 'path';

const dom = new JSDOM('<!DOCTYPE html><body></body>');
globalThis.window = dom.window;
globalThis.document = dom.window.document;
Object.defineProperty(globalThis, 'navigator', { value: dom.window.navigator, configurable: true });
const mermaid = (await import('mermaid')).default;
mermaid.initialize({ startOnLoad: false });

const root = path.resolve(process.argv[2] || '.');
const skip = new Set(['node_modules', '.git', 'evidence']);

function* walk(dir) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (skip.has(e.name)) continue;
    const p = path.join(dir, e.name);
    if (e.isDirectory()) yield* walk(p);
    else yield p;
  }
}

const items = [];
for (const f of walk(root)) {
  if (f.endsWith('.mmd')) items.push({ label: path.relative(root, f), text: fs.readFileSync(f, 'utf8') });
  else if (f.endsWith('.md')) {
    const md = fs.readFileSync(f, 'utf8');
    let i = 0;
    for (const m of md.matchAll(/```mermaid\n([\s\S]*?)```/g)) {
      items.push({ label: `${path.relative(root, f)}#${++i}`, text: m[1] });
    }
  }
}

let bad = 0;
for (const it of items.sort((a, b) => a.label.localeCompare(b.label))) {
  try { await mermaid.parse(it.text); console.log('OK  ', it.label); }
  catch (e) { bad++; console.log('FAIL', it.label, String(e.message || e).split('\n').slice(0, 3).join(' | ')); }
}
console.log(`${items.length - bad}/${items.length} diagrams parse`);
process.exit(bad ? 1 : 0);
