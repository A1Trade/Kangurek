"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { getDueReviews, recordReviewAnswer } from "@/lib/storage";
import type { Problem, Solution } from "@/types/schemas";
import type { ReviewItem } from "@/lib/srs";

type BankEntry = {
  problem: unknown;
  solution: unknown;
  lessonTitle: string;
  blockCode: string;
};

type Props = {
  bank: Record<string, BankEntry>;
};

const DIFF_BADGE: Record<string, string> = {
  "3pkt": "kbadge kbadge-green",
  "4pkt": "kbadge kbadge-amber",
  "5pkt": "kbadge kbadge-pink",
};

export function PowtorkaClient({ bank }: Props) {
  const [queue, setQueue] = useState<ReviewItem[]>([]);
  const [done, setDone] = useState<{ pid: string; correct: boolean }[]>([]);
  const [idx, setIdx] = useState(0);
  const [selected, setSelected] = useState<string | null>(null);
  const [revealed, setRevealed] = useState(false);
  const [showSol, setShowSol] = useState(false);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setQueue(getDueReviews());
    setMounted(true);
  }, []);

  if (!mounted) return null;

  if (queue.length === 0) {
    return (
      <div className="kcard text-center py-12 space-y-4">
        <div className="text-5xl">🎉</div>
        <h1 className="text-2xl font-bold text-slate-900">Nie ma nic do powtorki!</h1>
        <p className="text-slate-600">Zadania wracaja tutaj po 1, 3, 7, 14 dniach od pomylki.</p>
        <Link href="/" className="kbtn kbtn-primary inline-block">Wroc do lekcji</Link>
      </div>
    );
  }

  if (idx >= queue.length) {
    const correct = done.filter((d) => d.correct).length;
    return (
      <div className="kcard text-center py-12 space-y-4">
        <div className="text-5xl">✨</div>
        <h1 className="text-2xl font-bold text-slate-900">Powtorka skonczona!</h1>
        <p className="text-slate-700 text-lg">
          {correct} / {done.length} poprawnie.
        </p>
        <div className="text-sm text-slate-500">
          Zadania w ktorych sie pomylyles wroca jutro. Poprawnie - za {[1, 3, 7, 14][Math.min(3, 1)]} dni i dalej.
        </div>
        <Link href="/" className="kbtn kbtn-primary inline-block">Wroc do lekcji</Link>
      </div>
    );
  }

  const item = queue[idx];
  const entry = bank[item.problemId];
  if (!entry) {
    // brak danych - pomin
    setIdx(idx + 1);
    return null;
  }
  const problem = entry.problem as Problem;
  const solution = entry.solution as Solution | undefined;

  const confirm = () => {
    if (!selected || revealed) return;
    setRevealed(true);
    const correct = selected === problem.correct;
    recordReviewAnswer(item.problemId, correct);
    setDone([...done, { pid: item.problemId, correct }]);
  };

  const next = () => {
    setSelected(null);
    setRevealed(false);
    setShowSol(false);
    setIdx(idx + 1);
  };

  return (
    <div className="space-y-6">
      <header className="kcard p-5">
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs uppercase tracking-wider font-semibold text-slate-500">
            Powtorka SRS
          </span>
          <span className="text-sm font-semibold text-slate-700">
            {idx + 1} / {queue.length}
          </span>
        </div>
        <h1 className="text-xl font-bold text-slate-900 mb-1">
          Zadania, w ktorych mialeś klopot
        </h1>
        <p className="text-[13px] text-slate-600">
          Powtarzasz po 1, 3, 7, 14 dniach. Poprawna = dluzszy odstep.
        </p>
        <div className="mt-3 h-1.5 rounded-full bg-slate-200 overflow-hidden">
          <div
            className="h-full bg-emerald-500 transition-all"
            style={{ width: `${((idx + (revealed ? 1 : 0)) / queue.length) * 100}%` }}
          />
        </div>
      </header>

      <div className="kcard space-y-4">
        <div className="flex items-center gap-2 flex-wrap text-[13px]">
          <span className={DIFF_BADGE[problem.difficulty]}>{problem.difficulty}</span>
          <span className="kbadge kbadge-blue">{entry.lessonTitle}</span>
          <span className="kbadge kbadge-gray">Blok {entry.blockCode}</span>
        </div>

        <p className="text-[17px] leading-relaxed text-slate-800">{problem.statement}</p>

        {problem.imageSrc && (
          <div className="rounded-2xl bg-white border border-slate-200 p-2 overflow-hidden">
            <img src={problem.imageSrc} alt="Rysunek zadania" className="w-full h-auto rounded-xl" loading="lazy" />
          </div>
        )}

        <div className="grid sm:grid-cols-2 gap-2.5">
          {(["A", "B", "C", "D", "E"] as const).map((letter) => {
            const text = problem.choices[letter];
            const isCorrect = letter === problem.correct;
            const isSelected = letter === selected;
            let cls = "kchoice";
            if (revealed) {
              if (isCorrect) cls += " kchoice-correct";
              else if (isSelected) cls += " kchoice-wrong";
              else cls += " kchoice-disabled";
            } else if (isSelected) {
              cls += " kchoice-selected";
            }
            return (
              <button
                key={letter}
                type="button"
                className={cls}
                onClick={() => !revealed && setSelected(letter)}
                disabled={revealed}
              >
                <span className="kchoice-letter">{letter}</span>
                <span className="flex-1 self-center">{text}</span>
                {revealed && isCorrect && <span className="self-center text-emerald-600 font-bold">✓</span>}
                {revealed && isSelected && !isCorrect && (
                  <span className="self-center text-rose-600 font-bold">✗</span>
                )}
              </button>
            );
          })}
        </div>

        {!revealed && (
          <button onClick={confirm} disabled={!selected} className="kbtn kbtn-primary">
            ✓ Zatwierdz {selected ?? ""}
          </button>
        )}

        {revealed && (
          <div className="space-y-3">
            <div
              className={`rounded-2xl px-4 py-3 text-sm font-semibold flex items-center gap-2 ${
                selected === problem.correct
                  ? "bg-emerald-50/80 text-emerald-800 border border-emerald-200/60"
                  : "bg-rose-50/80 text-rose-800 border border-rose-200/60"
              }`}
            >
              <span>{selected === problem.correct ? "🎉" : "💪"}</span>
              <span>
                {selected === problem.correct
                  ? "Brawo! Wraca za dluzszy czas."
                  : `Niestety, poprawna to ${problem.correct}. Wraca jutro.`}
              </span>
            </div>
            {solution && (
              <div>
                <button
                  type="button"
                  onClick={() => setShowSol((s) => !s)}
                  className="kbtn kbtn-secondary kbtn-sm"
                >
                  {showSol ? "Ukryj" : "Pokaz rozwiazanie"}
                </button>
                {showSol && (
                  <div className="mt-3 rounded-2xl border border-amber-200/60 p-4 space-y-2 text-sm text-slate-800"
                       style={{ background: "linear-gradient(180deg, rgba(255,149,0,0.08), rgba(255,149,0,0.03))" }}>
                    <div><strong>👀</strong> {solution.observation}</div>
                    <div><strong>🧭</strong> {solution.strategy}</div>
                    <ol className="list-decimal list-inside space-y-1">
                      {solution.steps.map((s, i) => (
                        <li key={i}>{s}</li>
                      ))}
                    </ol>
                  </div>
                )}
              </div>
            )}
            <button onClick={next} className="kbtn kbtn-primary">
              Nastepne →
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
