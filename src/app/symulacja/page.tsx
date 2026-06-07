import { readFileSync, readdirSync, existsSync } from "node:fs";
import { join } from "node:path";
import { Problem, type Problem as ProblemT } from "@/types/schemas";
import { SymulacjaClient } from "./client";

function loadAllOriginalProblems(): ProblemT[] {
  const dir = join(process.cwd(), "data", "parsed");
  if (!existsSync(dir)) return [];
  const all: ProblemT[] = [];
  for (const f of readdirSync(dir).filter((f) => f.endsWith(".json"))) {
    try {
      const data = JSON.parse(readFileSync(join(dir, f), "utf-8"));
      if (Array.isArray(data.problems)) {
        for (const p of data.problems) {
          try {
            all.push(Problem.parse(p));
          } catch {}
        }
      }
    } catch {}
  }
  return all;
}

export default function SymulacjaPage() {
  const all = loadAllOriginalProblems();
  return <SymulacjaClient allProblems={all} />;
}
