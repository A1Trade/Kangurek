import { NextResponse } from "next/server";
import { Problem, TopicTag, ProblemDifficulty } from "@/types/schemas";
import { z } from "zod";
import { callJson } from "@/lib/agents/anthropic";

const Body = z.object({
  topic: TopicTag,
  difficulty: ProblemDifficulty.default("3pkt"),
  subtopic: z.string().optional(),
  avoidIds: z.array(z.string()).default([]),
});

const SYSTEM = `Jestes autorem zadan w stylu konkursu Kangur Maluch (klasy 3-4 SP).
Generujesz JEDNO zadanie z 5 odpowiedziami ABCDE, dokladnie jedna poprawna.

Wymagania:
- Jezyk polski, krotkie zdania, kontekst zabawny (zwierzaki, gry, sklep, kosmici).
- Liczby przyjazne 10-latkowi - bez ulamkow dziesietnych, bez procentow.
- 4 zle odpowiedzi to typowe bledy ucznia (a nie losowe liczby).
- NIE uzywaj "wszystkie powyzsze" / "zadne z powyzszych".

Format wyjscia: wylacznie JSON zgodny z Problem (id, source, year=null, number=null, difficulty, topic, subtopic, statement, hasImage=false, imageNote=null, choices{A..E}, correct).
id: "live-{random8}"`;

export async function POST(req: Request) {
  try {
    const body = Body.parse(await req.json());
    const user = `Wygeneruj jedno zadanie:
- temat: ${body.topic}
- podtemat: ${body.subtopic ?? "(dowolny w temacie)"}
- trudnosc: ${body.difficulty}
- unikalny id: "live-${Math.random().toString(36).slice(2, 10)}"
- omijaj te zadania (zeby sie nie powtarzac): ${body.avoidIds.join(", ") || "(brak)"}

Zwroc JEDEN obiekt JSON Problem.`;
    const problem = await callJson<unknown>({
      model: "sonnet",
      system: SYSTEM,
      user,
      maxTokens: 1500,
      temperature: 0.8,
    });
    const validated = Problem.parse(problem);
    return NextResponse.json({ problem: validated });
  } catch (e) {
    return NextResponse.json(
      { error: (e as Error).message ?? "blad" },
      { status: 500 },
    );
  }
}
