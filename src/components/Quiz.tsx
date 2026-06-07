"use client";

import { useState } from "react";
import type { QuizQuestion } from "@/types/schemas";
import { finishLessonVersion } from "@/lib/storage";

export function Quiz({
  lessonId,
  versionId,
  questions,
  onRestart,
}: {
  lessonId: string;
  versionId: string;
  questions: QuizQuestion[];
  onRestart?: () => void;
}) {
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [submitted, setSubmitted] = useState(false);

  const score = questions.reduce(
    (acc, q, i) => acc + (answers[i] === q.correct ? 1 : 0),
    0,
  );

  const submit = () => {
    if (Object.keys(answers).length < questions.length) return;
    setSubmitted(true);
    finishLessonVersion(lessonId, versionId, score, questions.length);
  };

  return (
    <div className="space-y-4">
      <div className="flex items-baseline gap-3">
        <h3 className="text-2xl font-bold tracking-tight text-slate-900">Quiz koncowy</h3>
        <span className="text-[13px] text-slate-500">3 krotkie pytania</span>
      </div>
      {questions.map((q, i) => (
        <div key={i} className="kcard space-y-3">
          <div className="font-semibold text-slate-900 text-[15px]">
            {i + 1}. {q.q}
          </div>
          <div className="grid sm:grid-cols-3 gap-2.5">
            {(["A", "B", "C"] as const).map((letter) => {
              const isPicked = answers[i] === letter;
              const isCorrect = q.correct === letter;
              let cls = "kchoice";
              if (submitted) {
                if (isCorrect) cls += " kchoice-correct";
                else if (isPicked) cls += " kchoice-wrong";
                else cls += " kchoice-disabled";
              } else if (isPicked) {
                cls += " kchoice-selected";
              }
              return (
                <button
                  key={letter}
                  type="button"
                  className={cls}
                  disabled={submitted}
                  onClick={() => setAnswers((a) => ({ ...a, [i]: letter }))}
                  aria-pressed={isPicked}
                >
                  <span className="kchoice-letter">{letter}</span>
                  <span className="flex-1 self-center">{q.choices[letter]}</span>
                </button>
              );
            })}
          </div>
          {submitted && (
            <div className="text-sm bg-slate-100/70 backdrop-blur border border-slate-200 rounded-2xl px-4 py-2.5 text-slate-700">
              <span className="font-semibold">Wyjasnienie:</span> {q.explain}
            </div>
          )}
        </div>
      ))}

      {!submitted ? (
        <button
          type="button"
          onClick={submit}
          disabled={Object.keys(answers).length < questions.length}
          className="kbtn kbtn-primary"
        >
          Sprawdz odpowiedzi
        </button>
      ) : (
        <div
          className={`kcard text-center space-y-3 ${
            score === questions.length ? "bg-emerald-50/80" : "bg-amber-50/80"
          }`}
        >
          <div className="text-[44px] font-bold leading-none tracking-tight">
            <span className={score === questions.length ? "text-emerald-600" : "text-amber-600"}>
              {score}
            </span>
            <span className="text-slate-400"> / {questions.length}</span>
          </div>
          <div className="text-slate-700 text-[15px]">
            {score === questions.length
              ? "🎉 Komplet! Lekcja zaliczona."
              : score >= questions.length - 1
                ? "Bardzo dobrze, lekcja zaliczona!"
                : "Lekcja zaliczona — mozesz wrocic i poczytac teorie jeszcze raz."}
          </div>
          {onRestart && (
            <button type="button" onClick={onRestart} className="kbtn kbtn-primary">
              ↻ Zrob te wersje jeszcze raz
            </button>
          )}
        </div>
      )}
    </div>
  );
}
