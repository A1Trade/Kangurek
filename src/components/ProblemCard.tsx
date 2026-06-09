"use client";

import { useState } from "react";
import type { Problem, Solution } from "@/types/schemas";
import { recordProblemAttempt } from "@/lib/storage";

type Props = {
  problem: Problem;
  solution?: Solution;
  showNumber?: number;
  lessonId?: string;
  versionId?: string;
  blockCode?: string;
};

const DIFF_LABEL: Record<string, string> = { "3pkt": "3 pkt", "4pkt": "4 pkt", "5pkt": "5 pkt" };
const DIFF_BADGE: Record<string, string> = {
  "3pkt": "kbadge kbadge-green",
  "4pkt": "kbadge kbadge-amber",
  "5pkt": "kbadge kbadge-pink",
};

function problemOrigin(p: Problem): { label: string; cls: string } {
  if (p.year !== null && p.number !== null) {
    return {
      label: `🦘 Kangur Maluch ${p.year} · zad. ${p.number}`,
      cls: "kbadge kbadge-orange",
    };
  }
  if (p.id.startsWith("live-")) {
    return { label: "✨ Wygenerowane teraz", cls: "kbadge kbadge-purple" };
  }
  return { label: "📝 Zadanie autorskie", cls: "kbadge kbadge-blue" };
}

export function ProblemCard({ problem, solution, showNumber, lessonId, versionId, blockCode }: Props) {
  const [selected, setSelected] = useState<string | null>(null);
  const [revealed, setRevealed] = useState(false);
  const [showSolution, setShowSolution] = useState(false);
  const [explain, setExplain] = useState<string | null>(null);
  const [loadingExplain, setLoadingExplain] = useState(false);

  const origin = problemOrigin(problem);

  const confirm = () => {
    if (!selected || revealed) return;
    setRevealed(true);
    if (lessonId && versionId) {
      recordProblemAttempt(lessonId, versionId, problem.id, selected, selected === problem.correct, {
        topic: problem.topic,
        block: blockCode,
      });
    }
  };

  const requestExplain = async () => {
    setLoadingExplain(true);
    try {
      const r = await fetch("/api/wytlumacz", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ problem }),
      });
      if (!r.ok) setExplain("Tlumaczenie AI niedostepne - brak klucza API.");
      else {
        const data = await r.json();
        setExplain(data.explanation ?? "(brak wyjasnienia)");
      }
    } catch {
      setExplain("Nie udalo sie pobrac wyjasnienia.");
    } finally {
      setLoadingExplain(false);
    }
  };

  return (
    <div className="kcard space-y-4">
      <div className="flex items-center gap-2 flex-wrap">
        {showNumber !== undefined && (
          <span className="text-[15px] font-bold text-slate-900 tracking-tight">
            Zadanie {showNumber}
          </span>
        )}
        <span className={DIFF_BADGE[problem.difficulty]}>{DIFF_LABEL[problem.difficulty]}</span>
        <span className={origin.cls}>{origin.label}</span>
      </div>

      <p className="text-[17px] leading-relaxed text-slate-800">{problem.statement}</p>

      {problem.imageSrc ? (
        <div className="rounded-2xl bg-white border border-slate-200 p-2 overflow-hidden">
          <img
            src={problem.imageSrc}
            alt={problem.imageNote ?? "Rysunek do zadania"}
            className="w-full h-auto rounded-xl"
            loading="lazy"
          />
        </div>
      ) : problem.hasImage && problem.imageNote ? (
        <div className="rounded-2xl bg-slate-100/70 backdrop-blur border border-slate-200 px-4 py-3 text-[13px] text-slate-600 italic flex gap-2">
          <span aria-hidden>🖼️</span>
          <span>{problem.imageNote}</span>
        </div>
      ) : null}

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
              aria-pressed={isSelected}
            >
              <span className="kchoice-letter">{letter}</span>
              <span className="flex-1 self-center">{text}</span>
              {revealed && isCorrect && <span aria-hidden className="self-center text-emerald-600 font-bold">✓</span>}
              {revealed && isSelected && !isCorrect && (
                <span aria-hidden className="self-center text-rose-600 font-bold">✗</span>
              )}
            </button>
          );
        })}
      </div>

      {!revealed && (
        <div className="flex gap-2 flex-wrap items-center">
          <button
            type="button"
            onClick={confirm}
            disabled={!selected}
            className="kbtn kbtn-primary"
          >
            ✓ Zatwierdz {selected ?? ""}
          </button>
        </div>
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
            <span aria-hidden className="text-base">
              {selected === problem.correct ? "🎉" : "💪"}
            </span>
            <span>
              {selected === problem.correct
                ? "Brawo, poprawnie!"
                : `Niestety, poprawna to ${problem.correct}.`}
            </span>
          </div>

          {solution && (
            <div>
              <button
                type="button"
                onClick={() => setShowSolution((s) => !s)}
                className="kbtn kbtn-secondary kbtn-sm"
              >
                {showSolution ? "Ukryj rozwiazanie" : "Pokaz rozwiazanie krok po kroku"}
              </button>
              {showSolution && <SolutionView solution={solution} />}
            </div>
          )}

          <button
            type="button"
            onClick={requestExplain}
            className="kbtn kbtn-ghost kbtn-sm"
            disabled={loadingExplain}
          >
            🤖 {loadingExplain ? "Mysle..." : "Wytlumacz mi to inaczej (AI)"}
          </button>
          {explain && (
            <div className="rounded-2xl border border-violet-200/60 px-4 py-3 text-sm text-violet-900 whitespace-pre-wrap"
                 style={{ background: "linear-gradient(180deg, rgba(175,82,222,0.08), rgba(175,82,222,0.03))" }}>
              {explain}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

function SolutionView({ solution }: { solution: Solution }) {
  return (
    <div className="mt-3 rounded-2xl border border-amber-200/60 p-4 space-y-2.5 text-sm text-slate-800"
         style={{ background: "linear-gradient(180deg, rgba(255,149,0,0.08), rgba(255,149,0,0.03))" }}>
      <div>
        <span className="font-semibold text-amber-800">👀 Co od razu widac:</span> {solution.observation}
      </div>
      <div>
        <span className="font-semibold text-amber-800">🧭 Strategia:</span> {solution.strategy}
      </div>
      <div>
        <div className="font-semibold text-amber-800 mb-1.5">📝 Krok po kroku:</div>
        <ol className="list-decimal list-inside space-y-1 marker:text-amber-700 marker:font-bold">
          {solution.steps.map((s, i) => (
            <li key={i}>{s}</li>
          ))}
        </ol>
      </div>
      {solution.alternative && (
        <div>
          <span className="font-semibold text-amber-800">💡 Sprytniej?</span> {solution.alternative}
        </div>
      )}
    </div>
  );
}
