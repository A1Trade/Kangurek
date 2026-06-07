"use client";

import { useEffect, useState } from "react";
import { getProgress } from "@/lib/storage";

export function ProgressBar({ total }: { total: number }) {
  const [done, setDone] = useState(0);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    const update = () => {
      const p = getProgress();
      const completed = Object.values(p.lessons).filter((l) =>
        l.attempts.some((a) => a.completed),
      ).length;
      setDone(completed);
    };
    update();
    window.addEventListener("kangurek-progress-update", update);
    return () => window.removeEventListener("kangurek-progress-update", update);
  }, []);

  const pct = total === 0 ? 0 : Math.round((done / total) * 100);
  return (
    <div className="kcard">
      <div className="flex items-center justify-between mb-2.5">
        <div className="flex items-center gap-2">
          <span aria-hidden className="text-base">🎯</span>
          <span className="font-semibold text-slate-900 tracking-tight">Twoj postep</span>
        </div>
        <div className="text-sm text-slate-600 font-medium">
          {mounted ? (
            <>
              <span className="text-slate-900 font-bold">{done}</span> / {total}{" "}
              <span className="text-slate-500">·</span>{" "}
              <span className="text-amber-600 font-bold">{pct}%</span>
            </>
          ) : (
            "..."
          )}
        </div>
      </div>
      <div className="h-2 bg-slate-200/70 rounded-full overflow-hidden">
        <div
          className="h-full kprog transition-all duration-700"
          style={{ width: `${mounted ? pct : 0}%` }}
        />
      </div>
    </div>
  );
}

export function LessonDoneBadge({ lessonId }: { lessonId: string }) {
  const [done, setDone] = useState(false);
  useEffect(() => {
    const update = () => {
      const p = getProgress();
      const lesson = p.lessons[lessonId];
      setDone(!!lesson && lesson.attempts.some((a) => a.completed));
    };
    update();
    window.addEventListener("kangurek-progress-update", update);
    return () => window.removeEventListener("kangurek-progress-update", update);
  }, [lessonId]);

  if (!done) return null;
  return (
    <span className="kbadge kbadge-green">
      <span aria-hidden>✓</span> zrobione
    </span>
  );
}
