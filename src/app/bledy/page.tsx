import { getAllLessons } from "@/lib/data/lessons";
import { BledyClient } from "./client";

export const metadata = { title: "Moje bledy · Kangurek" };

export default function BledyPage() {
  const lessons = getAllLessons();
  const bank: Record<string, { problem: unknown; lessonTitle: string; blockCode: string; lessonId: string }> = {};
  for (const lesson of lessons) {
    for (const v of lesson.versions) {
      for (const p of [...v.warmup, ...v.challenge]) {
        if (!bank[p.id]) {
          bank[p.id] = {
            problem: p,
            lessonTitle: lesson.title,
            blockCode: lesson.blockCode,
            lessonId: lesson.id,
          };
        }
      }
    }
  }
  return <BledyClient bank={bank} />;
}
