/**
 * Parsuje PDF-y z data/arkusze do data/parsed/{year}.json
 *
 * Strategia:
 *   - Wysylamy PDF do Claude Sonnet 4.6 jako dokument (widzi tekst + obrazy).
 *   - Model ekstrahuje 24 zadania z ABCDE, klasyfikuje temat i sam je rozwiazuje.
 *   - Wszystko w jednym wywolaniu na arkusz.
 *
 * Uzycie:
 *   npm run parse:arkusze           # wszystkie arkusze, pomija juz zrobione
 *   npm run parse:arkusze -- 2019   # tylko jeden rok
 *   npm run parse:arkusze -- --force # nadpisz
 */
import { readFileSync, writeFileSync, existsSync, readdirSync, mkdirSync } from "node:fs";
import { join, basename } from "node:path";
import { config } from "dotenv";
import Anthropic from "@anthropic-ai/sdk";
import { Problem, type Problem as ProblemT } from "../src/types/schemas";
import { z } from "zod";

config({ path: ".env.local" });

const ARKUSZE_DIR = "data/arkusze";
const OUTPUT_DIR = "data/parsed";
const MODEL = "claude-sonnet-4-6";

const args = process.argv.slice(2);
const FORCE = args.includes("--force");
const YEAR_FILTER = args.find((a) => /^\d{4}$/.test(a));

mkdirSync(OUTPUT_DIR, { recursive: true });

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY!,
});

const ParsedSheet = z.object({
  year: z.number().int(),
  category: z.literal("MALUCH"),
  problems: z.array(Problem),
});

const SYSTEM = `Jestes ekspertem od polskich konkursow matematycznych Kangur. Twoje zadanie: zekstrahowac wszystkie zadania z arkusza konkursowego Kangur MALUCH (klasy 3-4 SP) z PDF i zwrocic je jako poprawny JSON.

ZASADY EKSTRAKCJI:
- Arkusz MALUCH ma zazwyczaj 24 zadania.
- Zadania 1-8 sa za 3 punkty (proste), 9-16 za 4 punkty (srednie), 17-24 za 5 punktow (trudne).
- Kazde zadanie ma DOKLADNIE 5 odpowiedzi: A) B) C) D) E).
- Jezeli zadanie wymaga rysunku/obrazka ktorego nie da sie odtworzyc tekstem - opisz co rysunek przedstawia w polu imageNote i ustaw hasImage=true.
- Treso zadania (statement) PRZEPISZ DOSLOWNIE z PDF, z polskimi znakami (a, e, o, s, c, l, n, z, z).
- W choices A-E zapisz TYLKO sama tresc odpowiedzi (bez liter "A)", "B)").
- Klasyfikuj topic do jednej z wartosci enum (patrz schemat).

ROZWIAZANIE:
- Dla kazdego zadania SAMODZIELNIE ustal poprawna odpowiedz (correct: A/B/C/D/E).
- To zadania dla 10-latkow - rozwiaz w glowie krok po kroku, sprawdz dwa razy.
- Jezeli zadanie wymaga rysunku ktorego nie widzisz wyraznie, zaznacz hasImage=true i wybierz najbardziej prawdopodobna odpowiedz.

POLA WYJSCIA na zadanie:
{
  "id": "kangur-maluch-{rok}-{numer}",  // np. "kangur-maluch-2019-12"
  "source": "kangur-maluch-{rok}-{numer}",
  "year": <rok>,
  "number": <numer 1-24>,
  "difficulty": "3pkt" | "4pkt" | "5pkt",
  "topic": "arytmetyka" | "wzory_i_ciagi" | "geometria_plaska" | "geometria_przestrzenna" | "pomiary_jednostki" | "czas_kalendarz" | "logika" | "kombinatoryka" | "pieniadze" | "lamiglowki",
  "subtopic": "krotki opis, np. dzielenie z reszta",
  "statement": "<tekst zadania doslownie z PDF>",
  "hasImage": <true|false>,
  "imageNote": <null lub opis rysunku>,
  "choices": { "A": "...", "B": "...", "C": "...", "D": "...", "E": "..." },
  "correct": "A" | "B" | "C" | "D" | "E"
}

WYJSCIE: jeden obiekt JSON o ksztalcie:
{ "year": <rok>, "category": "MALUCH", "problems": [<24 zadania>] }

ZAWSZE odpowiadaj WYLACZNIE poprawnym JSON-em, bez komentarzy, bez markdownu, bez bloku triple-backtick. Tylko surowy JSON.`;

function extractYear(filename: string): number | null {
  const m = filename.match(/(\d{4})/);
  return m ? parseInt(m[1], 10) : null;
}

function parseJsonLenient(raw: string): unknown {
  let s = raw.trim();
  if (s.startsWith("```")) {
    s = s.replace(/^```(?:json)?\s*/, "").replace(/```\s*$/, "");
  }
  const firstBrace = s.search(/[\[{]/);
  if (firstBrace > 0) s = s.slice(firstBrace);
  return JSON.parse(s);
}

async function parseOne(pdfPath: string): Promise<{ year: number; problems: ProblemT[] }> {
  const filename = basename(pdfPath);
  const year = extractYear(filename);
  if (!year) throw new Error(`Nie moge wyciagnac roku z nazwy: ${filename}`);

  const pdfBytes = readFileSync(pdfPath);
  const pdfBase64 = pdfBytes.toString("base64");

  console.log(`  -> wysylam ${filename} (${(pdfBytes.length / 1024).toFixed(0)} KB) do Claude...`);

  const resp = await client.messages.create({
    model: MODEL,
    max_tokens: 16000,
    temperature: 0.1,
    system: SYSTEM,
    messages: [
      {
        role: "user",
        content: [
          {
            type: "document",
            source: {
              type: "base64",
              media_type: "application/pdf",
              data: pdfBase64,
            },
          },
          {
            type: "text",
            text: `To jest arkusz Kangur MALUCH z roku ${year}. Wyekstrahuj wszystkie zadania (1-24), klasyfikuj temat i podaj poprawna odpowiedz dla kazdego. Zwroc czysty JSON.`,
          },
        ],
      },
    ],
  });

  const text = resp.content
    .filter((b) => b.type === "text")
    .map((b) => (b as { type: "text"; text: string }).text)
    .join("");

  const parsed = parseJsonLenient(text);
  const validated = ParsedSheet.parse(parsed);

  console.log(
    `  <- ${validated.problems.length} zadan, tokens in=${resp.usage.input_tokens} out=${resp.usage.output_tokens}`
  );
  return { year: validated.year, problems: validated.problems };
}

async function main() {
  if (!process.env.ANTHROPIC_API_KEY) {
    console.error("Brak ANTHROPIC_API_KEY. Utworz .env.local z kluczem.");
    process.exit(1);
  }

  let files = readdirSync(ARKUSZE_DIR)
    .filter((f) => f.toLowerCase().endsWith(".pdf"))
    .filter((f) => !f.includes("(1)")) // skip duplicate m_2015 (1).pdf
    .map((f) => join(ARKUSZE_DIR, f));

  if (YEAR_FILTER) {
    files = files.filter((f) => extractYear(basename(f))?.toString() === YEAR_FILTER);
  }

  console.log(`Znaleziono ${files.length} arkuszy do przetworzenia${YEAR_FILTER ? ` (rok ${YEAR_FILTER})` : ""}.`);

  for (const file of files) {
    const year = extractYear(basename(file));
    if (!year) {
      console.warn(`Pomijam (brak roku): ${file}`);
      continue;
    }
    const outPath = join(OUTPUT_DIR, `${year}.json`);
    if (existsSync(outPath) && !FORCE) {
      console.log(`[${year}] juz zrobione, pomijam (--force aby nadpisac).`);
      continue;
    }
    console.log(`[${year}] parsuje ${basename(file)}...`);
    try {
      const result = await parseOne(file);
      writeFileSync(outPath, JSON.stringify(result, null, 2), "utf-8");
      console.log(`[${year}] OK -> ${outPath}`);
    } catch (e) {
      console.error(`[${year}] BLAD:`, (e as Error).message);
      if ((e as Error).message.includes("zod")) {
        console.error((e as Error).stack);
      }
    }
  }

  console.log("\nGotowe.");
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
