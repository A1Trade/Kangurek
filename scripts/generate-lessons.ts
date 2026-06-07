/**
 * Generator 50 lekcji. Dla kazdej lekcji z LESSON_PLAN:
 *  1. Wybiera 4-6 oryginalnych zadan Kangurka pasujacych do tematu (jako styl-reference).
 *  2. Wola Opus 4.7 z masterprompt -> dostaje cala lekcje (teoria + 7 zadan + rozwiazania + quiz).
 *  3. Waliduje Zodem i zapisuje do data/lessons/{id}.json + aktualizuje index.json.
 *
 * Uzycie:
 *   npm run generate:lessons          # wszystkie nowe lekcje
 *   npm run generate:lessons -- 5     # tylko lekcja 5
 *   npm run generate:lessons -- 1-10  # lekcje 1 do 10
 *   npm run generate:lessons -- --force # nadpisz istniejace
 */
import { readFileSync, writeFileSync, existsSync, readdirSync, mkdirSync } from "node:fs";
import { join } from "node:path";
import { config } from "dotenv";
import Anthropic from "@anthropic-ai/sdk";
import { Lesson, type Problem as ProblemT, type LessonIndexEntry } from "../src/types/schemas";
import { LESSON_PLAN } from "../src/lib/lesson-plan";

config({ path: ".env.local" });

const PARSED_DIR = "data/parsed";
const OUT_DIR = "data/lessons";
const INDEX_PATH = "data/index.json";
const MODEL = "claude-opus-4-7";

const args = process.argv.slice(2);
const FORCE = args.includes("--force");
const filterArg = args.find((a) => /^\d+(-\d+)?$/.test(a));
const range = parseRange(filterArg);

mkdirSync(OUT_DIR, { recursive: true });

const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY! });

function parseRange(s: string | undefined): [number, number] | null {
  if (!s) return null;
  const m = s.match(/^(\d+)(?:-(\d+))?$/);
  if (!m) return null;
  const lo = parseInt(m[1], 10);
  const hi = m[2] ? parseInt(m[2], 10) : lo;
  return [lo, hi];
}

function loadAllParsedProblems(): ProblemT[] {
  if (!existsSync(PARSED_DIR)) return [];
  const files = readdirSync(PARSED_DIR).filter((f) => f.endsWith(".json"));
  const all: ProblemT[] = [];
  for (const f of files) {
    try {
      const data = JSON.parse(readFileSync(join(PARSED_DIR, f), "utf-8"));
      if (Array.isArray(data.problems)) all.push(...data.problems);
    } catch {
      // skip
    }
  }
  return all;
}

function pickReferenceProblems(all: ProblemT[], topic: string, subtopic: string, n: number): ProblemT[] {
  const byTopic = all.filter((p) => p.topic === topic);
  const sub = subtopic.toLowerCase().split(/[ ,]+/).filter((w) => w.length > 3);
  const scored = byTopic.map((p) => {
    const haystack = (p.statement + " " + p.subtopic).toLowerCase();
    const score = sub.reduce((acc, w) => acc + (haystack.includes(w) ? 1 : 0), 0);
    return { p, score };
  });
  scored.sort((a, b) => b.score - a.score);
  return scored.slice(0, n).map((s) => s.p);
}

const MASTER_PROMPT_SYS = `ROLA: Jestes doswiadczonym nauczycielem matematyki w polskiej szkole podstawowej i wieloletnim autorem zadan do konkursu Kangur Matematyczny w kategorii MALUCH (klasy 3-4 SP). Uczyles setki dzieci jak myslec matematycznie, nie tylko liczyc.

ODBIORCA: 10-letni uczeń klasy 4, polskojezyczny, zna tabliczke mnozenia i dzialania na liczbach do 1000, zna podstawy figur plaskich. Cel: przygotowanie do konkursu Kangur w marcu.

ZADANIE: Wygeneruj kompletna tresc lekcji wedlug danego briefu i przykladow stylu Kangurka.

WYMAGANIA TRESCIOWE:
1. TEORIA (3 czesci):
   - intro (50-100 slow): zacznij od konkretnego przykladu z zycia (gra, sport, sklep, dom, szkola). Wciagnij ucznia od pierwszej linijki.
   - tool (100-200 slow): wprowadz narzedzie/strategie. Pokaz jak myslec o tym problemie - nie definicja podrecznikowa, tylko sposob mysleinia.
   - trick (50-100 slow): co Kangur LUBI sprawdzac z tego tematu i jak to zauwazyc. To 'sekret' ktory rozwiazuje pol zadan.
   - JEZYK: krotkie zdania, slowa znane 10-latkowi, ZERO zargonu matematycznego (zamiast 'cyfra dziesiatek' powiedz 'druga cyfra od konca'). NIE pisz 'oczywiscie', 'latwo zauwazyc', 'trywialnie', 'drogi uczniu'.

2. WARMUP - 5 zadan poziomu 3pkt (rozgrzewka):
   - format ABCDE, dokladnie jedna poprawna
   - 1 krok mysleinia, liczby przyjazne dla pamieci
   - kontekst zabawny w stylu Kangurka (zwierzaki, gry, kosmici, smieszne sytuacje)
   - kazde zadanie SAMODZIELNE - nie odwoluje sie do innych

3. CHALLENGE - 2 zadania poziomu 4-5 pkt (trudniejsze):
   - 2-3 kroki mysleinia, wymaga uzycia strategii z teorii
   - moga miec wieksza historie/kontekst
   - jedno z nich moze byc 'rebusowe' - z mala niespodzianka

4. SOLUTIONS - rozwiazania DLA KAZDEGO z 7 zadan (warmup + challenge) w tej samej kolejnosci co zadania:
   - observation (1 zdanie): co od razu widac
   - strategy (1-2 zdania): ktora technika z teorii
   - steps: tablica krokow, kazdy krok jako osobny string, kazdy krotki
   - answer: poprawna litera (musi sie zgadzac z correct w zadaniu!)
   - alternative: czy dalo sie szybciej / inaczej (lub null)

5. QUIZ koncowy - DOKLADNIE 3 pytania:
   - jednozdaniowe, 3 odpowiedzi A/B/C
   - sprawdza ZROZUMIENIE strategii, nie pamiec faktow
   - kazde z krotkim wyjasnieniem (1 zdanie)

ZAKAZY:
- NIE uzywaj odpowiedzi 'wszystkie powyzsze' ani 'zadne z powyzszych' (Kangur tego nie uzywa w MALUCH).
- NIE wprowadzaj pojec spoza programu klasy 4 (ulamki dziesietne, procenty, rownania, pierwiastki).
- NIE pisz 'drogi uczniu', 'kochany dzieciaku'.
- NIE powtarzaj polecenia w rozwiazaniu.
- NIE kopiuj doslownie zadan z przykladow stylu - tylko naladuj sie ich klimatem.
- Liczby przyjazne: maksymalnie 3-cyfrowe w wynikach, bez ulamkow dziesietnych.

POPRAWNOSC:
- ABSOLUTNIE krytyczna - rozwiaz kazde zadanie sam, sprawdz odpowiedz dwa razy.
- correct w zadaniu MUSI sie zgadzac z answer w solution.
- Wszystkie 5 odpowiedzi ABCDE musza byc rozne i sensowne (zle odpowiedzi to typowe bledy ucznia).

FORMAT WYJSCIA: WYLACZNIE poprawny JSON. Bez markdownu, bez komentarzy, bez bloku triple-backtick. Tylko surowy JSON.

ID zadan generowanych: 'gen-l{NN}-w{i}' dla warmup (i=1..5), 'gen-l{NN}-c{i}' dla challenge (i=1..2).
source dla generowanych: 'generated-{lessonId}-{numer}'.
year=null, number=null dla generowanych.`;

function buildUserPrompt(planItem: (typeof LESSON_PLAN)[number], refs: ProblemT[]) {
  const lessonId = `l${String(planItem.number).padStart(2, "0")}`;
  const refsText =
    refs.length === 0
      ? "(brak - parser jeszcze nie uruchomiony, generuj wylacznie na bazie swojej wiedzy o Kangurku)"
      : refs
          .map(
            (r, i) =>
              `[${i + 1}] [${r.difficulty}, ${r.year ?? "?"}#${r.number ?? "?"}] ${r.statement}\n   A) ${r.choices.A}  B) ${r.choices.B}  C) ${r.choices.C}  D) ${r.choices.D}  E) ${r.choices.E}\n   poprawna: ${r.correct}`
          )
          .join("\n\n");

  return `LEKCJA NR ${planItem.number} (id=${lessonId})
BLOK: ${planItem.blockCode} - ${planItem.block}
TYTUL: ${planItem.title}
TEMAT KLASYFIKACJI: ${planItem.topic}
PODTEMAT: ${planItem.subtopic}
CELE LEKCJI:
${planItem.goals.map((g) => "  - " + g).join("\n")}

PRZYKLADY STYLU KANGURKA (oryginalne zadania z arkuszy historycznych - inspirujsie klimatem, NIE kopiuj):
${refsText}

Wygeneruj pelna lekcje wg schematu Lesson. Pamietaj: id lekcji = "${lessonId}", number = ${planItem.number}, blockCode = "${planItem.blockCode}", block = "${planItem.block}", title = "${planItem.title}", topic = "${planItem.topic}", estimatedMinutes = 15.`;
}

function parseJsonLenient(raw: string): unknown {
  let s = raw.trim();
  if (s.startsWith("```")) {
    s = s.replace(/^```(?:json)?\s*/, "").replace(/```\s*$/, "");
  }
  const firstBrace = s.search(/[\[{]/);
  if (firstBrace > 0) s = s.slice(firstBrace);
  const lastBrace = Math.max(s.lastIndexOf("}"), s.lastIndexOf("]"));
  if (lastBrace > -1 && lastBrace < s.length - 1) s = s.slice(0, lastBrace + 1);
  return JSON.parse(s);
}

async function generateLesson(planItem: (typeof LESSON_PLAN)[number], refs: ProblemT[]) {
  const user = buildUserPrompt(planItem, refs);
  const resp = await client.messages.create({
    model: MODEL,
    max_tokens: 16000,
    temperature: 0.7,
    system: MASTER_PROMPT_SYS,
    messages: [{ role: "user", content: user }],
  });

  const text = resp.content
    .filter((b) => b.type === "text")
    .map((b) => (b as { type: "text"; text: string }).text)
    .join("");

  const json = parseJsonLenient(text);
  const lesson = Lesson.parse(json);
  return { lesson, usage: resp.usage };
}

async function main() {
  if (!process.env.ANTHROPIC_API_KEY) {
    console.error("Brak ANTHROPIC_API_KEY. Utworz .env.local.");
    process.exit(1);
  }

  const allProblems = loadAllParsedProblems();
  console.log(`Zaladowano ${allProblems.length} oryginalnych zadan z arkuszy.`);
  if (allProblems.length === 0) {
    console.log("[ostrzezenie] brak zadan referencyjnych - lekcje beda generowane wylacznie z wiedzy modelu.");
  }

  let plan = LESSON_PLAN;
  if (range) {
    plan = plan.filter((p) => p.number >= range[0] && p.number <= range[1]);
  }
  console.log(`Do wygenerowania: ${plan.length} lekcji.`);

  const index: LessonIndexEntry[] = [];

  for (const item of plan) {
    const lessonId = `l${String(item.number).padStart(2, "0")}`;
    const outPath = join(OUT_DIR, `${lessonId}.json`);
    if (existsSync(outPath) && !FORCE) {
      console.log(`[${lessonId}] juz istnieje, pomijam.`);
      try {
        const existing = JSON.parse(readFileSync(outPath, "utf-8"));
        index.push({
          id: existing.id,
          number: existing.number,
          block: existing.block,
          blockCode: existing.blockCode,
          title: existing.title,
          topic: existing.topic,
          estimatedMinutes: existing.estimatedMinutes,
        });
      } catch {}
      continue;
    }

    const refs = pickReferenceProblems(allProblems, item.topic, item.subtopic, 5);
    console.log(`[${lessonId}] ${item.title}  (refs: ${refs.length})`);
    try {
      const { lesson, usage } = await generateLesson(item, refs);
      writeFileSync(outPath, JSON.stringify(lesson, null, 2), "utf-8");
      index.push({
        id: lesson.id,
        number: lesson.number,
        block: lesson.block,
        blockCode: lesson.blockCode,
        title: lesson.title,
        topic: lesson.topic,
        estimatedMinutes: lesson.estimatedMinutes,
      });
      console.log(`[${lessonId}] OK  tokens in=${usage.input_tokens} out=${usage.output_tokens}`);
    } catch (e) {
      console.error(`[${lessonId}] BLAD:`, (e as Error).message);
    }
  }

  // odbuduj pelny index ze wszystkich lekcji w katalogu (zeby zachowac wczesniej zapisane)
  const fullIndex: LessonIndexEntry[] = [];
  for (const f of readdirSync(OUT_DIR).filter((f) => f.endsWith(".json"))) {
    try {
      const data = JSON.parse(readFileSync(join(OUT_DIR, f), "utf-8"));
      fullIndex.push({
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
  fullIndex.sort((a, b) => a.number - b.number);
  writeFileSync(INDEX_PATH, JSON.stringify(fullIndex, null, 2), "utf-8");
  console.log(`\nGotowe. Index: ${fullIndex.length} lekcji w ${INDEX_PATH}`);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
