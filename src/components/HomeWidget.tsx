"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { getDueReviews, getStreak, getWeakTopics, getBadges } from "@/lib/storage";
import { BADGES } from "@/lib/badges";
import { LESSON_PLAN } from "@/lib/lesson-plan";

const TOPIC_LABEL: Record<string, string> = {
  arytmetyka: "arytmetyka",
  wzory_i_ciagi: "wzory i ciagi",
  geometria_plaska: "geometria plaska",
  geometria_przestrzenna: "geometria przestrzenna",
  pomiary_jednostki: "pomiary i jednostki",
  czas_kalendarz: "czas i kalendarz",
  logika: "logika",
  kombinatoryka: "kombinatoryka",
  pieniadze: "pieniadze",
  lamiglowki: "lamiglowki",
};

export function HomeWidget() {
  const [mounted, setMounted] = useState(false);
  const [streak, setStreak] = useState({ current: 0, longest: 0, lastActivityDate: "" });
  const [dueCount, setDueCount] = useState(0);
  const [weak, setWeak] = useState<{ topic: string; pct: number; total: number }[]>([]);
  const [badgeCount, setBadgeCount] = useState(0);

  useEffect(() => {
    function refresh() {
      setStreak(getStreak());
      setDueCount(getDueReviews().length);
      setWeak(getWeakTopics());
      setBadgeCount(getBadges().length);
    }
    refresh();
    setMounted(true);
    window.addEventListener("kangurek-progress-update", refresh);
    return () => window.removeEventListener("kangurek-progress-update", refresh);
  }, []);

  if (!mounted) return null;

  const hasAny = streak.current > 0 || dueCount > 0 || weak.length > 0 || badgeCount > 0;
  if (!hasAny) return null;

  const weakSuggestion = weak[0];
  let suggestedLesson: string | null = null;
  if (weakSuggestion) {
    const lessonInBlock = LESSON_PLAN.find((p) => p.topic === weakSuggestion.topic);
    if (lessonInBlock) suggestedLesson = `l${String(lessonInBlock.number).padStart(2, "0")}`;
  }

  return (
    <section className="grid sm:grid-cols-2 lg:grid-cols-4 gap-3">
      {/* Streak */}
      <div className="kcard p-4 flex items-center gap-3">
        <span className="text-3xl" aria-hidden>🔥</span>
        <div>
          <div className="text-xs uppercase tracking-wider text-slate-500 font-semibold">Seria</div>
          <div className="text-2xl font-bold text-slate-900 leading-none">{streak.current}</div>
          <div className="text-[11px] text-slate-500 mt-0.5">
            {streak.current === 0 ? "zacznij dzis!" : `rekord: ${streak.longest}`}
          </div>
        </div>
      </div>

      {/* Do powtorki */}
      <Link
        href="/powtorka"
        className={`kcard p-4 flex items-center gap-3 ${dueCount === 0 ? "opacity-60" : "hover:scale-[1.02] transition"}`}
      >
        <span className="text-3xl" aria-hidden>📚</span>
        <div>
          <div className="text-xs uppercase tracking-wider text-slate-500 font-semibold">Do powtorki</div>
          <div className="text-2xl font-bold text-slate-900 leading-none">{dueCount}</div>
          <div className="text-[11px] text-slate-500 mt-0.5">
            {dueCount === 0 ? "wszystko ogarniete" : "klikni, zeby zaczac"}
          </div>
        </div>
      </Link>

      {/* Slabe tematy */}
      {weakSuggestion ? (
        <Link
          href={suggestedLesson ? `/lekcje/${suggestedLesson}` : "/lekcje"}
          className="kcard p-4 flex items-center gap-3 hover:scale-[1.02] transition"
        >
          <span className="text-3xl" aria-hidden>🎯</span>
          <div className="min-w-0">
            <div className="text-xs uppercase tracking-wider text-slate-500 font-semibold">Slaby temat</div>
            <div className="text-[15px] font-bold text-slate-900 leading-tight truncate">
              {TOPIC_LABEL[weakSuggestion.topic] ?? weakSuggestion.topic}
            </div>
            <div className="text-[11px] text-slate-500 mt-0.5">{weakSuggestion.pct}% poprawnych</div>
          </div>
        </Link>
      ) : (
        <div className="kcard p-4 flex items-center gap-3 opacity-60">
          <span className="text-3xl" aria-hidden>🎯</span>
          <div>
            <div className="text-xs uppercase tracking-wider text-slate-500 font-semibold">Slabe tematy</div>
            <div className="text-[13px] text-slate-700 mt-0.5">cwicz wiecej, by zobaczyc</div>
          </div>
        </div>
      )}

      {/* Odznaki */}
      <Link
        href="/odznaki"
        className="kcard p-4 flex items-center gap-3 hover:scale-[1.02] transition"
      >
        <span className="text-3xl" aria-hidden>🏅</span>
        <div>
          <div className="text-xs uppercase tracking-wider text-slate-500 font-semibold">Odznaki</div>
          <div className="text-2xl font-bold text-slate-900 leading-none">
            {badgeCount}<span className="text-base font-normal text-slate-500">/{BADGES.length}</span>
          </div>
          <div className="text-[11px] text-slate-500 mt-0.5">zdobytych</div>
        </div>
      </Link>
    </section>
  );
}
