"use client";

import { useEffect, useState } from "react";
import { getBadges, getStreak } from "@/lib/storage";
import { BADGES } from "@/lib/badges";

export function OdznakiClient() {
  const [owned, setOwned] = useState<Record<string, string>>({});
  const [streak, setStreak] = useState({ current: 0, longest: 0, lastActivityDate: "" });
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    function refresh() {
      const arr = getBadges();
      const map: Record<string, string> = {};
      for (const b of arr) map[b.id] = b.earnedAt;
      setOwned(map);
      setStreak(getStreak());
    }
    refresh();
    setMounted(true);
    window.addEventListener("kangurek-progress-update", refresh);
    return () => window.removeEventListener("kangurek-progress-update", refresh);
  }, []);

  if (!mounted) return null;

  const earnedCount = Object.keys(owned).length;
  const pct = Math.round((earnedCount / BADGES.length) * 100);

  return (
    <div className="space-y-6">
      <header className="kcard p-5">
        <h1 className="text-2xl font-bold text-slate-900 mb-1">Odznaki</h1>
        <p className="text-[14px] text-slate-600">
          Zdobyte: <strong>{earnedCount} / {BADGES.length}</strong> ({pct}%)
        </p>
        <div className="mt-3 h-1.5 rounded-full bg-slate-200 overflow-hidden">
          <div className="h-full bg-amber-500" style={{ width: `${pct}%` }} />
        </div>
        <div className="mt-4 flex items-center gap-3 text-sm">
          <span className="text-2xl">🔥</span>
          <div>
            <div className="font-bold text-slate-900">{streak.current} dni z rzedu</div>
            <div className="text-xs text-slate-500">rekord: {streak.longest}</div>
          </div>
        </div>
      </header>

      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-3">
        {BADGES.map((b) => {
          const has = b.id in owned;
          return (
            <div
              key={b.id}
              className={`kcard p-4 flex items-start gap-3 ${has ? "" : "opacity-40 grayscale"}`}
            >
              <div className="text-4xl">{b.emoji}</div>
              <div className="flex-1 min-w-0">
                <div className="font-bold text-slate-900">{b.name}</div>
                <div className="text-[12px] text-slate-600 mt-0.5">{b.desc}</div>
                {has && (
                  <div className="text-[11px] text-emerald-700 mt-1.5 font-semibold">
                    ✓ Zdobyta {new Date(owned[b.id]).toLocaleDateString("pl")}
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
