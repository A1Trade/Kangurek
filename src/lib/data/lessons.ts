import { readFileSync, existsSync, readdirSync } from "node:fs";
import { join } from "node:path";
import { Lesson, LessonIndexEntry, type Lesson as LessonT, type LessonIndexEntry as LessonIndexT } from "@/types/schemas";
import { LESSON_PLAN } from "@/lib/lesson-plan";

const LESSONS_DIR = join(process.cwd(), "data", "lessons");
const INDEX_PATH = join(process.cwd(), "data", "index.json");

export function getLessonIndex(): LessonIndexT[] {
  if (existsSync(INDEX_PATH)) {
    try {
      const raw = JSON.parse(readFileSync(INDEX_PATH, "utf-8"));
      const arr = LessonIndexEntry.array().parse(raw);
      return arr.sort((a, b) => a.number - b.number);
    } catch {
      // fall through to filesystem scan
    }
  }
  // fallback: scan directory
  if (existsSync(LESSONS_DIR)) {
    const files = readdirSync(LESSONS_DIR).filter((f) => f.endsWith(".json"));
    const idx: LessonIndexT[] = [];
    for (const f of files) {
      try {
        const data = JSON.parse(readFileSync(join(LESSONS_DIR, f), "utf-8"));
        idx.push({
          id: data.id,
          number: data.number,
          block: data.block,
          blockCode: data.blockCode,
          title: data.title,
          topic: data.topic,
          estimatedMinutes: data.estimatedMinutes,
        });
      } catch {}
    }
    return idx.sort((a, b) => a.number - b.number);
  }
  return [];
}

/**
 * Zwraca pelny plan lekcji - wpisy z LESSON_PLAN wzbogacone informacja czy lekcja juz wygenerowana.
 * Dzieki temu UI dziala nawet przed generacja: pokazujemy 'placeholder' z opisem.
 */
export function getPlanWithStatus(): Array<{
  number: number;
  blockCode: string;
  block: string;
  title: string;
  topic: string;
  generated: boolean;
  id: string;
  estimatedMinutes: number;
}> {
  const index = getLessonIndex();
  const generated = new Set(index.map((i) => i.number));
  return LESSON_PLAN.map((p) => {
    const id = `l${String(p.number).padStart(2, "0")}`;
    return {
      number: p.number,
      blockCode: p.blockCode,
      block: p.block,
      title: p.title,
      topic: p.topic,
      generated: generated.has(p.number),
      id,
      estimatedMinutes: 15,
    };
  });
}

export function getLesson(id: string): LessonT | null {
  const path = join(LESSONS_DIR, `${id}.json`);
  if (!existsSync(path)) return null;
  try {
    const raw = JSON.parse(readFileSync(path, "utf-8"));
    return Lesson.parse(raw);
  } catch {
    return null;
  }
}

export function getAllLessons(): LessonT[] {
  if (!existsSync(LESSONS_DIR)) return [];
  const files = readdirSync(LESSONS_DIR).filter((f) => f.endsWith(".json"));
  const lessons: LessonT[] = [];
  for (const f of files) {
    try {
      const data = JSON.parse(readFileSync(join(LESSONS_DIR, f), "utf-8"));
      lessons.push(Lesson.parse(data));
    } catch {}
  }
  return lessons.sort((a, b) => a.number - b.number);
}
