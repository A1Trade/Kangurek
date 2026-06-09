"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { getAllErrors } from "@/lib/storage";
import type { Problem } from "@/types/schemas";
import type { ReviewItem } from "@/lib/srs";

type Props = {
  bank: Record<string, { problem: unknown; lessonTitle: string; blockCode: string; lessonId: string }>;
};

const DIFF_BADGE: Record<string, string> = {
  "3pkt": "kbadge kbadge-green",
  "4pkt": "kbadge kbadge-amber",
  "5pkt": "kbadge kbadge-pink",
};

export function BledyClient({ bank }: Props) {
  const [items, setItems] = useState<ReviewItem[]>([]);
  const [filterBlock, setFilterBlock] = useState<string>("all");
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setItems(getAllErrors());
    setMounted(true);
  }, []);

  if (!mounted) return null;

  const filtered = items.filter((it) => {
    if (filterBlock === "all") return true;
    const entry = bank[it.problemId];
    return entry?.blockCode === filterBlock;
  });

  const blocks = Array.from(new Set(items.map((it) => bank[it.problemId]?.blockCode).filter(Boolean))).sort();
  const masteredCount = items.filter((it) => it.mastered).length;

  return (
    <div className="space-y-6">
      <header className="kcard p-5">
        <h1 className="text-2xl font-bold text-slate-900 mb-1">Moje bledy</h1>
        <p className="text-[14px] text-slate-600">
          Lista wszystkich zadan, w ktorych sie pomylyles. {masteredCount > 0 && <span className="font-semibold text-emerald-700">{masteredCount} juz opanowanych! 🌟</span>}
        </p>
        <div className="mt-4 flex gap-2 flex-wrap">
          <button
            onClick={() => setFilterBlock("all")}
            className={filterBlock === "all" ? "kbtn kbtn-primary kbtn-sm" : "kbtn kbtn-secondary kbtn-sm"}
          >
            Wszystkie ({items.length})
          </button>
          {blocks.map((b) => (
            <button
              key={b}
              onClick={() => setFilterBlock(b!)}
              className={filterBlock === b ? "kbtn kbtn-primary kbtn-sm" : "kbtn kbtn-secondary kbtn-sm"}
            >
              Blok {b}
            </button>
          ))}
        </div>
        {items.length > 0 && (
          <div className="mt-3">
            <Link href="/powtorka" className="kbtn kbtn-primary">
              📚 Powtorz dzisiejsze
            </Link>
          </div>
        )}
      </header>

      {filtered.length === 0 ? (
        <div className="kcard text-center py-10">
          <div className="text-4xl mb-2">✨</div>
          <p className="text-slate-700">
            {items.length === 0
              ? "Jeszcze zadnych pomylek - rozwiazuj zadania, pomylki pojawia sie tutaj."
              : "Brak pomylek w wybranym bloku."}
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {filtered.map((it) => {
            const entry = bank[it.problemId];
            if (!entry) return null;
            const problem = entry.problem as Problem;
            const lastAttempt = it.history[it.history.length - 1];
            return (
              <Link
                key={it.problemId}
                href={`/lekcje/${entry.lessonId}`}
                className="kcard p-4 hover:scale-[1.01] transition block"
              >
                <div className="flex items-start gap-3">
                  <div className="text-2xl">{it.mastered ? "🌟" : "❌"}</div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 flex-wrap mb-1.5">
                      <span className={DIFF_BADGE[problem.difficulty]}>{problem.difficulty}</span>
                      <span className="kbadge kbadge-blue">{entry.lessonTitle}</span>
                      <span className="kbadge kbadge-gray">Blok {entry.blockCode}</span>
                      {it.mastered ? (
                        <span className="kbadge kbadge-green">opanowane</span>
                      ) : (
                        <span className="text-[11px] text-slate-500">
                          wraca: {it.nextReviewAt}
                        </span>
                      )}
                    </div>
                    <p className="text-[14px] text-slate-800 line-clamp-2">{problem.statement}</p>
                    <div className="text-[11px] text-slate-500 mt-1">
                      Probować: {it.history.length}× · ostatnio:{" "}
                      {lastAttempt?.correct ? "✓" : "✗"}
                    </div>
                  </div>
                </div>
              </Link>
            );
          })}
        </div>
      )}
    </div>
  );
}
