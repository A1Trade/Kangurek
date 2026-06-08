import { z } from "zod";

export const AnswerLetter = z.enum(["A", "B", "C", "D", "E"]);
export type AnswerLetter = z.infer<typeof AnswerLetter>;

export const ProblemDifficulty = z.enum(["3pkt", "4pkt", "5pkt"]);
export type ProblemDifficulty = z.infer<typeof ProblemDifficulty>;

export const TopicTag = z.enum([
  "arytmetyka",
  "wzory_i_ciagi",
  "geometria_plaska",
  "geometria_przestrzenna",
  "pomiary_jednostki",
  "czas_kalendarz",
  "logika",
  "kombinatoryka",
  "pieniadze",
  "lamiglowki",
]);
export type TopicTag = z.infer<typeof TopicTag>;

export const Problem = z.object({
  id: z.string(),
  source: z.string().describe("np. 'kangur-maluch-2019-12' lub 'gen-l05-q3'"),
  year: z.number().int().nullable(),
  number: z.number().int().nullable(),
  difficulty: ProblemDifficulty,
  topic: TopicTag,
  subtopic: z.string().describe("krotki opis podtematu, np. 'dzielenie z reszta'"),
  statement: z.string().describe("tresc zadania, gotowa do wyswietlenia"),
  hasImage: z.boolean().default(false),
  imageNote: z.string().nullable().default(null).describe("jezeli zadanie wymaga rysunku, opis tego co przedstawia"),
  imageSrc: z.string().nullable().default(null).describe("sciezka do obrazu w public/ (np. /images/orig/2020-6.png)"),
  choices: z.object({
    A: z.string(),
    B: z.string(),
    C: z.string(),
    D: z.string(),
    E: z.string(),
  }),
  correct: AnswerLetter,
});
export type Problem = z.infer<typeof Problem>;

export const Solution = z.object({
  problemId: z.string(),
  hint: z.string().nullable().default(null).describe("krotka podpowiedz (1 zdanie) - pokazywana przed rozwiazaniem"),
  observation: z.string().describe("co od razu widac w zadaniu (1 zdanie)"),
  strategy: z.string().describe("ktora technika z teorii pasuje"),
  steps: z.array(z.string()).describe("krok po kroku, kazdy krok osobno"),
  answer: AnswerLetter,
  alternative: z.string().nullable().describe("inne podejscie / sprytniejszy sposob"),
});
export type Solution = z.infer<typeof Solution>;

export const QuizQuestion = z.object({
  q: z.string(),
  choices: z.object({ A: z.string(), B: z.string(), C: z.string() }),
  correct: z.enum(["A", "B", "C"]),
  explain: z.string(),
});
export type QuizQuestion = z.infer<typeof QuizQuestion>;

export const LessonVersion = z.object({
  versionId: z.string().describe("np. 'v1', 'v2', 'v3'"),
  label: z.string().describe("nazwa wersji, np. 'Wersja 1 (oryginalna)'"),
  warmup: z.array(Problem).describe("5 zadan poziomu 3pkt"),
  challenge: z.array(Problem).describe("2 zadania poziomu 4-5pkt"),
  solutions: z.array(Solution).describe("rozwiazania do warmup + challenge w tej samej kolejnosci"),
});
export type LessonVersion = z.infer<typeof LessonVersion>;

export const Lesson = z.object({
  id: z.string().describe("np. 'l01'"),
  number: z.number().int().min(1).max(80),
  block: z.string().describe("nazwa bloku tematycznego"),
  blockCode: z.enum(["A", "B", "C", "D", "E", "F", "G", "H", "I"]),
  title: z.string(),
  topic: TopicTag,
  estimatedMinutes: z.number().int().min(5).max(60),
  theory: z.object({
    intro: z.string().describe("przyklad z zycia (50-100 slow)"),
    tool: z.string().describe("narzedzie / strategia (100-200 slow)"),
    trick: z.string().describe("co Kangur lubi sprawdzac i jak to zauwazyc (50-100 slow)"),
  }),
  versions: z.array(LessonVersion).min(1).max(3).describe("1-3 zestawow zadan (theory wspolne, quiz wspolny)"),
  quiz: z.array(QuizQuestion).length(3).describe("3 krotkie pytania koncowe (wspolne dla wszystkich wersji)"),
});
export type Lesson = z.infer<typeof Lesson>;

export const LessonIndexEntry = z.object({
  id: z.string(),
  number: z.number().int(),
  block: z.string(),
  blockCode: z.string(),
  title: z.string(),
  topic: TopicTag,
  estimatedMinutes: z.number().int(),
});
export type LessonIndexEntry = z.infer<typeof LessonIndexEntry>;

export const LessonPlanItem = z.object({
  number: z.number().int(),
  blockCode: z.enum(["A", "B", "C", "D", "E", "F", "G", "H", "I"]),
  block: z.string(),
  title: z.string(),
  topic: TopicTag,
  subtopic: z.string(),
  goals: z.array(z.string()).describe("2-4 cele nauczania"),
});
export type LessonPlanItem = z.infer<typeof LessonPlanItem>;
