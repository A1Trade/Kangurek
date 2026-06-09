"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import type { LessonIndexEntry } from "@/types/schemas";
import {
  getProgress,
  getSummary,
  resetProgress,
  type LessonProgress,
  type Progress,
  type VersionAttempt,
} from "@/lib/storage";

function fmtTime(sec: number) {
  if (sec < 60) return `${sec}s`;
  const m = Math.floor(sec / 60);
  const s = sec % 60;
  return `${m}m ${s}s`;
}

function fmtDateTime(iso?: string) {
  if (!iso) return "-";
  const d = new Date(iso);
  return d.toLocaleString("pl-PL", {
    day: "2-digit",
    month: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export function DziennikClient({ index }: { index: LessonIndexEntry[] }) {
  const [progress, setProgress] = useState<Progress>({
    lessons: {},
    reviews: {},
    streak: { current: 0, longest: 0, lastActivityDate: "" },
    badges: [],
  });
  const [summary, setSummary] = useState({
    lessonsTotal: 0,
    lessonsCompleted: 0,
    totalAttempts: 0,
    completedAttempts: 0,
    totalProblems: 0,
    correctProblems: 0,
    accuracyPct: 0,
    totalMinutes: 0,
  });
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    const update = () => {
      setProgress(getProgress());
      setSummary(getSummary());
    };
    update();
    window.addEventListener("kangurek-progress-update", update);
    return () => window.removeEventListener("kangurek-progress-update", update);
  }, []);

  if (!mounted) {
    return <div className="kcard text-center text-slate-500">Ładowanie dziennika...</div>;
  }

  const indexById = new Map(index.map((i) => [i.id, i]));
  const startedLessons = Object.values(progress.lessons).sort((a, b) => {
    const na = indexById.get(a.lessonId)?.number ?? 999;
    const nb = indexById.get(b.lessonId)?.number ?? 999;
    return na - nb;
  });

  const mastery =
    summary.totalProblems === 0
      ? 0
      : Math.round(
          ((summary.correctProblems / summary.totalProblems) * 0.7 +
            (summary.lessonsCompleted / Math.max(1, index.length)) * 0.3) *
            100,
        );

  return (
    <div className="space-y-6 kanim">
      <nav className="text-[13px]">
        <Link href="/" className="kbtn kbtn-ghost kbtn-sm">
          ← Wszystkie lekcje
        </Link>
      </nav>

      <header className="khero p-6 md:p-8 relative overflow-hidden">
        <div className="absolute -top-12 -right-10 w-44 h-44 rounded-full bg-gradient-to-br from-amber-200 to-pink-300 opacity-50 blur-2xl pointer-events-none" />
        <div className="relative flex items-start gap-4">
          <span aria-hidden className="text-4xl">📒</span>
          <div className="flex-1">
            <h1 className="text-3xl md:text-4xl font-bold tracking-tight text-slate-900">
              Twoj dziennik
            </h1>
            <p className="text-[15px] text-slate-700 mt-1">
              Kazde podejscie do lekcji zapisuje sie osobno. Powtarzaj zeby utrwalic strategie.
            </p>
          </div>
        </div>
      </header>

      {/* Stats */}
      <section className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        <StatCard
          icon="✅"
          label="Lekcje"
          value={`${summary.lessonsCompleted}/${index.length || "?"}`}
          hint={`${summary.completedAttempts} podejsc ukonczonych`}
          tone="green"
        />
        <StatCard
          icon="⏱"
          label="Czas razem"
          value={fmtTime(summary.totalMinutes * 60)}
          hint={`${summary.totalAttempts} podejsc lacznie`}
          tone="amber"
        />
        <StatCard
          icon="🎯"
          label="Trafnosc"
          value={`${summary.accuracyPct}%`}
          hint={`${summary.correctProblems} / ${summary.totalProblems} zadan`}
          tone="blue"
        />
        <StatCard
          icon="🏆"
          label="Opanowanie"
          value={`${mastery}%`}
          hint="70% trafnosc + 30% ukonczenie"
          tone="purple"
        />
      </section>

      <div className="text-right">
        <button
          type="button"
          className="text-[12px] text-slate-500 hover:text-rose-600 underline underline-offset-2"
          onClick={() => {
            if (confirm("Skasowac wszystkie wyniki? Ta operacja jest nieodwracalna.")) {
              resetProgress();
            }
          }}
        >
          Wyczysc dziennik
        </button>
      </div>

      {startedLessons.length === 0 ? (
        <div className="kcard text-center text-slate-600 py-8">
          <div className="text-3xl mb-2" aria-hidden>🦘</div>
          <div>Jeszcze nic nie zrobiles!</div>
          <Link href="/" className="kbtn kbtn-primary mt-4">
            Zacznij od lekcji 1
          </Link>
        </div>
      ) : (
        <div className="space-y-3">
          {startedLessons.map((l) => (
            <LessonRow key={l.lessonId} lesson={l} meta={indexById.get(l.lessonId)} />
          ))}
        </div>
      )}
    </div>
  );
}

function StatCard({
  icon,
  label,
  value,
  hint,
  tone,
}: {
  icon: string;
  label: string;
  value: string;
  hint?: string;
  tone: "amber" | "green" | "blue" | "purple" | "pink";
}) {
  const cls = {
    amber: "kstat-amber",
    green: "kstat-green",
    blue: "kstat-blue",
    purple: "kstat-purple",
    pink: "kstat-pink",
  }[tone];
  return (
    <div className={`kstat ${cls}`}>
      <div className="flex items-start justify-between">
        <div className="text-[11px] font-semibold uppercase tracking-wider text-slate-500">
          {label}
        </div>
        <span aria-hidden className="text-lg opacity-80">{icon}</span>
      </div>
      <div className="text-3xl font-bold tracking-tight text-slate-900 mt-1">{value}</div>
      {hint && <div className="text-[11px] text-slate-500 mt-1">{hint}</div>}
    </div>
  );
}

function LessonRow({
  lesson,
  meta,
}: {
  lesson: LessonProgress;
  meta?: LessonIndexEntry;
}) {
  const [expanded, setExpanded] = useState(false);
  const byVersion = new Map<string, VersionAttempt[]>();
  for (const a of lesson.attempts) {
    if (!byVersion.has(a.versionId)) byVersion.set(a.versionId, []);
    byVersion.get(a.versionId)!.push(a);
  }
  const versionIds = Array.from(byVersion.keys()).sort();
  const totalCompleted = lesson.attempts.filter((a) => a.completed).length;
  const bestAttempt = lesson.attempts
    .filter((a) => a.quizScore !== undefined)
    .reduce<VersionAttempt | null>(
      (b, a) => (b === null || (a.quizScore ?? 0) > (b.quizScore ?? 0) ? a : b),
      null,
    );

  return (
    <div className="kcard">
      <button
        type="button"
        onClick={() => setExpanded((e) => !e)}
        className="w-full flex items-center justify-between text-left"
      >
        <div className="flex items-center gap-4 min-w-0">
          {meta && (
            <span className={`knum knum-${meta.blockCode} flex-shrink-0`}>{meta.number}</span>
          )}
          <div className="min-w-0">
            <div className="font-semibold text-slate-900 tracking-tight truncate">
              {meta?.title ?? lesson.lessonId}
            </div>
            <div className="text-[12px] text-slate-500 mt-0.5">
              {lesson.attempts.length} podejsc · {totalCompleted} ukonczonych
              {bestAttempt?.quizScore !== undefined && (
                <span>
                  {" · "}🏆 quiz {bestAttempt.quizScore}/{bestAttempt.quizMax}
                </span>
              )}
            </div>
          </div>
        </div>
        <span className="text-slate-400 text-lg">{expanded ? "⌃" : "⌄"}</span>
      </button>

      {expanded && (
        <div className="mt-4 space-y-4">
          {versionIds.map((vid) => {
            const attempts = byVersion.get(vid)!;
            return (
              <div key={vid} className="space-y-2">
                <div className="flex items-center gap-2">
                  <span className="kbadge kbadge-orange">Wersja {vid}</span>
                  <span className="text-[12px] text-slate-500">
                    {attempts.length} {attempts.length === 1 ? "podejscie" : "podejsc"}
                  </span>
                </div>
                {attempts.map((a) => (
                  <AttemptDetail key={`${vid}-${a.attemptNumber}`} a={a} />
                ))}
              </div>
            );
          })}
          {meta && (
            <Link href={`/lekcje/${lesson.lessonId}`} className="kbtn kbtn-secondary kbtn-sm inline-flex">
              Otworz lekcje
            </Link>
          )}
        </div>
      )}
    </div>
  );
}

function AttemptDetail({ a }: { a: VersionAttempt }) {
  const problems = Object.entries(a.problems);
  const correct = problems.filter(([, p]) => p.correct).length;
  return (
    <div className="rounded-2xl border border-slate-200/70 bg-white/60 backdrop-blur p-4">
      <div className="flex items-center justify-between flex-wrap gap-2">
        <div className="text-[13px] font-semibold text-slate-900 flex items-center gap-2">
          Podejscie #{a.attemptNumber}
          {a.completed ? (
            <span className="kbadge kbadge-green">ukonczone</span>
          ) : (
            <span className="kbadge kbadge-amber">w trakcie</span>
          )}
        </div>
        <div className="text-[11px] text-slate-500">
          {a.startedAt && <span>start {fmtDateTime(a.startedAt)}</span>}
          {a.finishedAt && <span> · koniec {fmtDateTime(a.finishedAt)}</span>}
        </div>
      </div>
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-3">
        <MiniStat label="Czas" value={fmtTime(a.durationSec)} />
        <MiniStat label="Trafione" value={`${correct} / ${problems.length}`} />
        <MiniStat label="Quiz" value={a.quizScore !== undefined ? `${a.quizScore} / ${a.quizMax}` : "—"} />
        <MiniStat
          label="Trafnosc"
          value={problems.length === 0 ? "—" : `${Math.round((correct / problems.length) * 100)}%`}
        />
      </div>
      {problems.length > 0 && (
        <div className="mt-3">
          <div className="text-[11px] text-slate-500 mb-1.5">Per-zadanie:</div>
          <div className="flex gap-1.5 flex-wrap">
            {problems.map(([pid, p]) => (
              <span
                key={pid}
                title={`${pid} · wybrane: ${p.picked} · prob: ${p.attempts}`}
                className={p.correct ? "kbadge kbadge-green" : "kbadge kbadge-red"}
              >
                {p.correct ? "✓" : "✗"} {p.picked}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

function MiniStat({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <div className="text-[10px] uppercase tracking-wider font-semibold text-slate-500">
        {label}
      </div>
      <div className="text-[15px] font-bold text-slate-900 tracking-tight">{value}</div>
    </div>
  );
}
