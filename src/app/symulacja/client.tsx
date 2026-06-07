"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import type { Problem } from "@/types/schemas";

const TOTAL_SECONDS = 75 * 60;

function pickSet(all: Problem[]): Problem[] {
  const by = (d: string) => all.filter((p) => p.difficulty === d);
  const sample = (arr: Problem[], n: number) => {
    const copy = [...arr];
    const out: Problem[] = [];
    for (let i = 0; i < n && copy.length > 0; i++) {
      const idx = Math.floor(Math.random() * copy.length);
      out.push(copy.splice(idx, 1)[0]);
    }
    return out;
  };
  return [...sample(by("3pkt"), 8), ...sample(by("4pkt"), 8), ...sample(by("5pkt"), 8)];
}

function pointsFor(diff: string): number {
  if (diff === "3pkt") return 3;
  if (diff === "4pkt") return 4;
  return 5;
}

export function SymulacjaClient({ allProblems }: { allProblems: Problem[] }) {
  const [started, setStarted] = useState(false);
  const [problems, setProblems] = useState<Problem[]>([]);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [submitted, setSubmitted] = useState(false);
  const [seconds, setSeconds] = useState(TOTAL_SECONDS);
  const tickRef = useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => {
    if (started && !submitted) {
      tickRef.current = setInterval(() => {
        setSeconds((s) => {
          if (s <= 1) {
            clearInterval(tickRef.current!);
            setSubmitted(true);
            return 0;
          }
          return s - 1;
        });
      }, 1000);
      return () => {
        if (tickRef.current) clearInterval(tickRef.current);
      };
    }
  }, [started, submitted]);

  const score = useMemo(() => {
    let s = 0;
    for (const p of problems) {
      if (answers[p.id] === p.correct) s += pointsFor(p.difficulty);
    }
    return s;
  }, [problems, answers]);

  const maxScore = problems.reduce((acc, p) => acc + pointsFor(p.difficulty), 0);

  if (allProblems.length < 24) {
    return (
      <div className="kcard">
        <div className="text-3xl mb-2" aria-hidden>🦘</div>
        <h1 className="text-2xl font-bold tracking-tight text-slate-900 mb-2">
          Symulacja konkursu
        </h1>
        <p className="text-slate-700 text-[15px]">
          Symulacja bedzie dostepna gdy w bazie pojawi sie wiecej zadan z arkuszy historycznych.
          Aktualnie mamy <strong>{allProblems.length}</strong> zadan. Potrzeba co najmniej 24.
        </p>
      </div>
    );
  }

  if (!started) {
    return (
      <div className="space-y-6 kanim">
        <header className="khero p-6 md:p-8 relative overflow-hidden">
          <div className="absolute -top-12 -right-10 w-44 h-44 rounded-full bg-gradient-to-br from-rose-300 to-orange-300 opacity-60 blur-2xl pointer-events-none" />
          <div className="relative flex items-start gap-4">
            <span aria-hidden className="text-4xl">🦘</span>
            <div className="flex-1">
              <p className="text-[12px] uppercase tracking-wider font-bold text-amber-700/80 mb-1">
                Konkurs Kangur · Maluch
              </p>
              <h1 className="text-3xl md:text-4xl font-bold tracking-tight text-slate-900">
                Symulacja konkursu
              </h1>
              <p className="text-[15px] text-slate-700 mt-2">
                24 zadania · 75 minut · format ABCDE
              </p>
            </div>
          </div>
        </header>

        <div className="grid sm:grid-cols-3 gap-3">
          <div className="kstat kstat-green">
            <div className="text-[11px] uppercase tracking-wider font-semibold text-slate-500">
              Zadania 1–8
            </div>
            <div className="text-2xl font-bold tracking-tight text-slate-900 mt-1">3 pkt</div>
            <div className="text-[11px] text-slate-500 mt-1">rozgrzewka</div>
          </div>
          <div className="kstat kstat-amber">
            <div className="text-[11px] uppercase tracking-wider font-semibold text-slate-500">
              Zadania 9–16
            </div>
            <div className="text-2xl font-bold tracking-tight text-slate-900 mt-1">4 pkt</div>
            <div className="text-[11px] text-slate-500 mt-1">srodek tabeli</div>
          </div>
          <div className="kstat kstat-pink">
            <div className="text-[11px] uppercase tracking-wider font-semibold text-slate-500">
              Zadania 17–24
            </div>
            <div className="text-2xl font-bold tracking-tight text-slate-900 mt-1">5 pkt</div>
            <div className="text-[11px] text-slate-500 mt-1">wyzwanie</div>
          </div>
        </div>

        <div className="kcard space-y-2 text-[14px] text-slate-700">
          <div className="font-semibold text-slate-900 tracking-tight mb-1">Zasady</div>
          <ul className="list-disc list-inside space-y-1 marker:text-amber-500">
            <li>Maksymalnie <strong>96 punktow</strong>.</li>
            <li>Mozesz pomijac zadania i wracac do nich pozniej.</li>
            <li>Po uplywie czasu praca konczy sie automatycznie.</li>
          </ul>
        </div>

        <button
          type="button"
          onClick={() => {
            setProblems(pickSet(allProblems));
            setStarted(true);
          }}
          className="kbtn kbtn-primary text-base"
        >
          ▶ Start — rozpocznij symulacje
        </button>
      </div>
    );
  }

  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  const answered = Object.keys(answers).length;
  const lowTime = seconds < 300;

  return (
    <div className="space-y-4 kanim">
      <div className="sticky top-2 z-40 glass-strong rounded-3xl p-4 flex items-center justify-between gap-4">
        <div>
          <div className="text-[10px] uppercase tracking-wider font-semibold text-slate-500">
            Pozostalo
          </div>
          <div
            className={`text-3xl font-mono font-bold tracking-tight ${
              lowTime ? "text-rose-600" : "text-slate-900"
            }`}
          >
            {String(mins).padStart(2, "0")}:{String(secs).padStart(2, "0")}
          </div>
        </div>
        <div className="flex-1 text-right">
          <div className="text-[10px] uppercase tracking-wider font-semibold text-slate-500">
            Odpowiedzi
          </div>
          <div className="text-2xl font-bold tracking-tight text-slate-900">
            {answered} <span className="text-slate-400 text-lg">/ 24</span>
          </div>
        </div>
        {!submitted && (
          <button
            onClick={() => {
              if (confirm("Zakonczyc symulacje teraz?")) setSubmitted(true);
            }}
            className="kbtn kbtn-secondary kbtn-sm"
          >
            Zakoncz
          </button>
        )}
      </div>

      {submitted && (
        <div className="kcard text-center space-y-3 bg-emerald-50/70 border border-emerald-200">
          <div className="text-5xl font-bold tracking-tight text-emerald-700">
            {score} <span className="text-slate-400 text-3xl">/ {maxScore}</span>
          </div>
          <div className="text-slate-700 text-[15px]">
            {score >= 80
              ? "🥇 Wynik konkursowy! Masz duze szanse na nagrode."
              : score >= 60
                ? "🥈 Bardzo dobrze! Jeszcze troche treningu."
                : score >= 40
                  ? "🥉 Dobry start. Wroc do lekcji z najtrudniejszych blokow."
                  : "Bez stresu — to byl trening. Wroc do lekcji i sprobuj jeszcze raz!"}
          </div>
          <button
            onClick={() => {
              setStarted(false);
              setSubmitted(false);
              setAnswers({});
              setSeconds(TOTAL_SECONDS);
            }}
            className="kbtn kbtn-primary"
          >
            ↻ Sprobuj jeszcze raz
          </button>
        </div>
      )}

      {problems.map((p, i) => (
        <SymProblem
          key={p.id}
          problem={p}
          number={i + 1}
          picked={answers[p.id] ?? null}
          submitted={submitted}
          onPick={(letter) => setAnswers((a) => ({ ...a, [p.id]: letter }))}
        />
      ))}
    </div>
  );
}

function SymProblem({
  problem,
  number,
  picked,
  submitted,
  onPick,
}: {
  problem: Problem;
  number: number;
  picked: string | null;
  submitted: boolean;
  onPick: (letter: string) => void;
}) {
  return (
    <div className="kcard space-y-3">
      <div className="flex items-center gap-2 flex-wrap">
        <span className="text-[15px] font-bold tracking-tight text-slate-900">
          Zadanie {number}
        </span>
        <span className="kbadge kbadge-gray">{pointsFor(problem.difficulty)} pkt</span>
        {problem.year && (
          <span className="kbadge kbadge-orange">
            🦘 {problem.year} · zad. {problem.number}
          </span>
        )}
      </div>
      <p className="text-[16px] leading-relaxed text-slate-800">{problem.statement}</p>
      {problem.hasImage && problem.imageNote && (
        <div className="rounded-2xl bg-slate-100/70 border border-slate-200 px-4 py-3 text-[13px] text-slate-600 italic">
          🖼️ Wyobraz sobie: {problem.imageNote}
        </div>
      )}
      <div className="grid sm:grid-cols-2 gap-2.5">
        {(["A", "B", "C", "D", "E"] as const).map((letter) => {
          const isCorrect = letter === problem.correct;
          const isPicked = letter === picked;
          let cls = "kchoice";
          if (submitted) {
            if (isCorrect) cls += " kchoice-correct";
            else if (isPicked) cls += " kchoice-wrong";
            else cls += " kchoice-disabled";
          } else if (isPicked) cls += " kchoice-selected";
          return (
            <button
              key={letter}
              type="button"
              disabled={submitted}
              className={cls}
              onClick={() => onPick(letter)}
              aria-pressed={isPicked}
            >
              <span className="kchoice-letter">{letter}</span>
              <span className="flex-1 self-center">{problem.choices[letter]}</span>
            </button>
          );
        })}
      </div>
    </div>
  );
}
