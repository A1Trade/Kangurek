import { NextResponse } from "next/server";
import { Problem } from "@/types/schemas";
import { z } from "zod";
import { callText } from "@/lib/agents/anthropic";

const Body = z.object({
  problem: Problem,
  level: z.number().int().min(1).max(3).default(1),
});

const SYSTEM = `Jestes pomocnym nauczycielem matematyki dla 10-latka przygotowujacego sie do konkursu Kangur Maluch.
Twoja rola: dac PODPOWIEDZ ktora kieruje na trop, ale NIE podaje gotowej odpowiedzi.

Poziom 1: jeden trop w stylu "zacznij od policzenia X" albo "zauwaz, ze...". Maks 2 zdania.
Poziom 2: pierwszy konkretny krok rozwiazania. Maks 3 zdania.
Poziom 3: prawie wszystko poza ostatnim krokiem. Maks 5 zdan.

NIE podawaj poprawnej odpowiedzi A/B/C/D/E. NIE pisz dlugich tekstow. Po prostu trop.
Pisz po polsku, prosto, jak do 10-latka. Bez zargonu.`;

export async function POST(req: Request) {
  try {
    const body = Body.parse(await req.json());
    const user = `Zadanie: ${body.problem.statement}
Odpowiedzi: A) ${body.problem.choices.A}  B) ${body.problem.choices.B}  C) ${body.problem.choices.C}  D) ${body.problem.choices.D}  E) ${body.problem.choices.E}

Podaj podpowiedz poziomu ${body.level}.`;
    const text = await callText({
      model: "haiku",
      system: SYSTEM,
      user,
      maxTokens: 300,
      temperature: 0.6,
    });
    return NextResponse.json({ hint: text.trim() });
  } catch (e) {
    return NextResponse.json(
      { error: (e as Error).message ?? "blad" },
      { status: 500 },
    );
  }
}
