"use client";

import { useEffect, useMemo, useState } from "react";
import type { Lesson } from "@/types/schemas";
import { ProblemCard } from "@/components/ProblemCard";
import { Quiz } from "@/components/Quiz";
import {
  startLessonVersion,
  restartLessonVersion,
  getLatestVersionAttempt,
  getAttemptsForVersion,
} from "@/lib/storage";

const BLOCK_TINT: Record<string, string> = {
  A: "from-amber-200 to-orange-300",
  B: "from-orange-200 to-rose-300",
  C: "from-rose-200 to-pink-300",
  D: "from-fuchsia-200 to-purple-300",
  E: "from-violet-200 to-indigo-300",
  F: "from-indigo-200 to-blue-300",
  G: "from-sky-200 to-cyan-300",
  H: "from-teal-200 to-emerald-300",
  I: "from-emerald-200 to-green-300",
};

export function LessonView({ lesson }: { lesson: Lesson }) {
  const [versionId, setVersionId] = useState<string>(lesson.versions[0].versionId);
  const [sessionKey, setSessionKey] = useState(0);

  useEffect(() => {
    startLessonVersion(lesson.id, versionId);
  }, [lesson.id, versionId, sessionKey]);

  const current = useMemo(
    () => lesson.versions.find((v) => v.versionId === versionId) ?? lesson.versions[0],
    [lesson.versions, versionId],
  );

  const solutionsById = new Map(current.solutions.map((s) => [s.problemId, s]));

  const startNewAttempt = () => {
    restartLessonVersion(lesson.id, versionId);
    setSessionKey((k) => k + 1);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const switchVersion = (newVersion: string) => {
    setVersionId(newVersion);
    setSessionKey((k) => k + 1);
  };

  return (
    <div className="space-y-6 kanim">
      {/* Hero */}
      <header className="khero relative overflow-hidden p-6 md:p-8">
        <div className={`absolute -top-16 -right-16 w-56 h-56 rounded-full bg-gradient-to-br ${BLOCK_TINT[lesson.blockCode]} opacity-50 blur-2xl pointer-events-none`} />
        <div className="relative">
          <div className="flex items-center gap-2 flex-wrap mb-2">
            <span className="kbadge kbadge-orange">Blok {lesson.blockCode}</span>
            <span className="text-[13px] text-slate-600">{lesson.block}</span>
            <span className="text-slate-400">·</span>
            <span className="k-pill">
              <span aria-hidden>⏱</span> {lesson.estimatedMinutes} min
            </span>
          </div>
          <h1 className="text-3xl md:text-4xl font-bold tracking-tight text-slate-900 leading-tight">
            {lesson.title}
          </h1>
          <div className="text-[13px] text-slate-500 mt-2">
            Lekcja {lesson.number} · {lesson.topic.replace(/_/g, " ")}
          </div>
        </div>
      </header>

      {/* Theory */}
      <section className="grid md:grid-cols-3 gap-3">
        <TheoryCard icon="🌍" title="Sytuacja z zycia" content={lesson.theory.intro} tint="bg-amber-100/40 border-amber-200" />
        <TheoryCard icon="🧰" title="Narzedzie" content={lesson.theory.tool} tint="bg-sky-100/40 border-sky-200" />
        <TheoryCard icon="🎯" title="Trik na Kangurze" content={lesson.theory.trick} tint="bg-emerald-100/40 border-emerald-200" />
      </section>

      <VersionPicker lesson={lesson} versionId={versionId} onChange={switchVersion} onRestart={startNewAttempt} />

      <section key={`warm-${versionId}-${sessionKey}`} className="space-y-3">
        <h2 className="text-xl font-bold tracking-tight text-slate-900 flex items-center gap-2">
          <span aria-hidden>🦘</span> Rozgrzewka
          <span className="k-pill ml-auto">{current.warmup.length} zadan</span>
        </h2>
        {current.warmup.map((p, i) => (
          <ProblemCard
            key={`${versionId}-${sessionKey}-${p.id}`}
            problem={p}
            solution={solutionsById.get(p.id)}
            showNumber={i + 1}
            lessonId={lesson.id}
            versionId={versionId}
            blockCode={lesson.blockCode}
          />
        ))}
      </section>

      <section key={`chal-${versionId}-${sessionKey}`} className="space-y-3">
        <h2 className="text-xl font-bold tracking-tight text-slate-900 flex items-center gap-2">
          <span aria-hidden>🔥</span> Wyzwanie
          <span className="k-pill ml-auto">{current.challenge.length} zadania</span>
        </h2>
        {current.challenge.map((p, i) => (
          <ProblemCard
            key={`${versionId}-${sessionKey}-${p.id}`}
            problem={p}
            solution={solutionsById.get(p.id)}
            showNumber={current.warmup.length + i + 1}
            lessonId={lesson.id}
            versionId={versionId}
            blockCode={lesson.blockCode}
          />
        ))}
      </section>

      <section key={`quiz-${versionId}-${sessionKey}`}>
        <Quiz lessonId={lesson.id} versionId={versionId} questions={lesson.quiz} onRestart={startNewAttempt} />
      </section>
    </div>
  );
}

function TheoryCard({ icon, title, content, tint }: { icon: string; title: string; content: string; tint: string }) {
  return (
    <div className={`rounded-3xl border p-5 ${tint} backdrop-blur space-y-2`}>
      <div className="flex items-center gap-2">
        <span aria-hidden className="text-xl">{icon}</span>
        <h3 className="font-semibold text-slate-900 tracking-tight">{title}</h3>
      </div>
      <p className="text-[14px] text-slate-700 leading-relaxed whitespace-pre-line">{content}</p>
    </div>
  );
}

function VersionPicker({
  lesson,
  versionId,
  onChange,
  onRestart,
}: {
  lesson: Lesson;
  versionId: string;
  onChange: (id: string) => void;
  onRestart: () => void;
}) {
  const [tick, setTick] = useState(0);
  useEffect(() => {
    const upd = () => setTick((t) => t + 1);
    window.addEventListener("kangurek-progress-update", upd);
    return () => window.removeEventListener("kangurek-progress-update", upd);
  }, []);

  if (lesson.versions.length <= 1) return null;

  return (
    <section className="kcard space-y-3">
      <div className="flex items-center gap-2">
        <span aria-hidden className="text-base">🔄</span>
        <span className="font-semibold text-slate-900 tracking-tight">Wersja zadan</span>
      </div>
      <div className="flex items-center gap-2 flex-wrap">
        {lesson.versions.map((v) => {
          void tick;
          const all = getAttemptsForVersion(lesson.id, v.versionId);
          const completedCount = all.filter((a) => a.completed).length;
          const latest = all.length > 0 ? all[all.length - 1] : undefined;
          const isActive = v.versionId === versionId;
          const best = all
            .filter((a) => a.quizScore !== undefined)
            .reduce<{ quizScore: number; quizMax: number } | null>(
              (b, a) =>
                b === null || (a.quizScore ?? 0) > b.quizScore
                  ? { quizScore: a.quizScore ?? 0, quizMax: a.quizMax ?? 0 }
                  : b,
              null,
            );
          let badge = "nowa";
          if (completedCount > 0) badge = `${completedCount}× · best ${best?.quizScore}/${best?.quizMax}`;
          else if (latest && !latest.completed) badge = "w trakcie";
          return (
            <button
              key={v.versionId}
              type="button"
              onClick={() => onChange(v.versionId)}
              className={`kbtn kbtn-sm ${isActive ? "kbtn-primary" : "kbtn-secondary"}`}
            >
              {v.label}
              <span className="opacity-75 ml-1.5 text-[11px]">({badge})</span>
            </button>
          );
        })}
      </div>
      <p className="text-[12px] text-slate-500">
        Zmiana wersji wczytuje inne zadania (teoria i quiz zostaja). Kazde podejscie zapisuje sie osobno w dzienniku.
      </p>
      {(() => {
        void tick;
        const latest = getLatestVersionAttempt(lesson.id, versionId);
        if (latest?.completed) {
          return (
            <button type="button" onClick={onRestart} className="kbtn kbtn-sm kbtn-secondary self-start">
              ↻ Zrob te wersje jeszcze raz
            </button>
          );
        }
        return null;
      })()}
    </section>
  );
}
