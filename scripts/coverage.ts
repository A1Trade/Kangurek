/**
 * Raport pokrycia: ile oryginalnych zadan Kangurka jest uzytych w lekcjach.
 * Cel: 120/120 - kazde oryginalne zadanie ma swoje miejsce w kursie.
 *
 * Uzycie: npm run coverage
 */
import { readFileSync, readdirSync, existsSync } from "node:fs";
import { join } from "node:path";

const PARSED = "data/parsed";
const LESSONS = "data/lessons";

type P = { id: string; year: number | null; number: number | null; topic: string; difficulty: string };

function loadAllOriginals(): P[] {
  if (!existsSync(PARSED)) return [];
  const all: P[] = [];
  for (const f of readdirSync(PARSED).filter((f) => f.endsWith(".json"))) {
    const d = JSON.parse(readFileSync(join(PARSED, f), "utf-8"));
    for (const p of d.problems ?? []) all.push(p);
  }
  return all;
}

function usageMap(): Map<string, string[]> {
  const map = new Map<string, string[]>();
  if (!existsSync(LESSONS)) return map;
  for (const f of readdirSync(LESSONS).filter((f) => f.endsWith(".json"))) {
    const d = JSON.parse(readFileSync(join(LESSONS, f), "utf-8"));
    for (const v of d.versions ?? []) {
      for (const p of [...(v.warmup ?? []), ...(v.challenge ?? [])]) {
        if (p.year) {
          if (!map.has(p.id)) map.set(p.id, []);
          map.get(p.id)!.push(`${d.id}/${v.versionId}`);
        }
      }
    }
  }
  return map;
}

const all = loadAllOriginals();
const usage = usageMap();
const used = all.filter((p) => usage.has(p.id));
const unused = all.filter((p) => !usage.has(p.id));

console.log("=".repeat(56));
console.log(`POKRYCIE ORYGINALOW KANGURKA W LEKCJACH`);
console.log("=".repeat(56));
console.log(`Lacznie oryginalow:  ${all.length}`);
console.log(`Uzytych w lekcjach:  ${used.length}  (${Math.round((used.length / all.length) * 100)}%)`);
console.log(`Nieuzytych:          ${unused.length}`);
console.log("");

const byTopic: Record<string, { used: number; total: number }> = {};
for (const p of all) {
  byTopic[p.topic] ??= { used: 0, total: 0 };
  byTopic[p.topic].total += 1;
  if (usage.has(p.id)) byTopic[p.topic].used += 1;
}
console.log("Wg tematu (uzyte / lacznie):");
for (const [t, c] of Object.entries(byTopic).sort((a, b) => b[1].total - a[1].total)) {
  const bar = "#".repeat(Math.round((c.used / c.total) * 20)).padEnd(20, ".");
  console.log(`  ${t.padEnd(24)} ${bar} ${c.used}/${c.total}`);
}

if (unused.length > 0) {
  console.log("");
  console.log(`NIEUZYTE (${unused.length}):`);
  const byYear: Record<string, P[]> = {};
  for (const p of unused) {
    const y = String(p.year);
    byYear[y] ??= [];
    byYear[y].push(p);
  }
  for (const [y, list] of Object.entries(byYear).sort()) {
    console.log(`  ${y}: ${list.map((p) => `#${p.number}`).join(", ")}`);
  }
}

if (process.argv.includes("--duplicates")) {
  console.log("");
  console.log("Uzyte wielokrotnie:");
  for (const [id, where] of usage) {
    if (where.length > 1) console.log(`  ${id}: ${where.join(", ")}`);
  }
}

console.log("");
console.log(used.length === all.length ? "CEL OSIAGNIETY: 120/120 oryginalow w kursie." : `Do celu brakuje: ${unused.length} zadan.`);
