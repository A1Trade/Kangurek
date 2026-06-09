import { getAllLessons } from "@/lib/data/lessons";
import { PowtorkaClient } from "./client";

export const metadata = { title: "Powtorka SRS · Kangurek" };

export default function PowtorkaPage() {
  const lessons = getAllLessons();
  // przekaz mape problemId -> {problem, solution, lessonTitle}
  const all: Record<string, { problem: unknown; solution: unknown; lessonTitle: string; blockCode: string }> = {};
  for (const lesson of lessons) {
    for (const v of lesson.versions) {
      const solById = new Map(v.solutions.map((s) => [s.problemId, s]));
      for (const p of [...v.warmup, ...v.challenge]) {
        if (!all[p.id]) {
          all[p.id] = {
            problem: p,
            solution: solById.get(p.id),
            lessonTitle: lesson.title,
            blockCode: lesson.blockCode,
          };
        }
      }
    }
  }
  return <PowtorkaClient bank={all} />;
}
