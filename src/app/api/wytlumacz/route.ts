import { NextResponse } from "next/server";
import { Problem } from "@/types/schemas";
import { z } from "zod";
import { callText } from "@/lib/agents/anthropic";

const Body = z.object({
  problem: Problem,
  question: z.string().optional(),
});

const SYSTEM = `Jestes cierpliwym nauczycielem matematyki tlumaczacym zadania konkursowe Kangur Maluch 10-latkowi.
Wytlumacz zadanie inaczej niz zwykle rozwiazanie - znajdz analogie z zycia, narysuj obraz slowami, podziel na bardzo male krokid.

Struktura odpowiedzi:
1. "Co to zadanie naprawde pyta" - przeloz jezyk zadania na proste pytanie.
2. "Co masz w reku" - co wiemy, co mozemy uzyc.
3. "Maly plan" - 2-3 kroki jak do tego dojsc.
4. "Sprawdz" - jak wiesz, ze odpowiedz jest dobra.

Pisz krotkimi zdaniami. Bez zargonu. Jak najwiecej obrazow, porownan, analogii do swiata 10-latka (gry, sport, zwierzaki, sklep).
Max 250 slow. Po polsku.`;

export async function POST(req: Request) {
  try {
    const body = Body.parse(await req.json());
    const user = `Zadanie:
${body.problem.statement}

Odpowiedzi:
A) ${body.problem.choices.A}
B) ${body.problem.choices.B}
C) ${body.problem.choices.C}
D) ${body.problem.choices.D}
E) ${body.problem.choices.E}

Poprawna: ${body.problem.correct}

${body.question ? `Pytanie ucznia: ${body.question}` : "Wytlumacz to zadanie po swojemu, inaczej niz zwykle rozwiazanie."}`;
    const text = await callText({
      model: "opus",
      system: SYSTEM,
      user,
      maxTokens: 1200,
      temperature: 0.6,
    });
    return NextResponse.json({ explanation: text.trim() });
  } catch (e) {
    return NextResponse.json(
      { error: (e as Error).message ?? "blad" },
      { status: 500 },
    );
  }
}
