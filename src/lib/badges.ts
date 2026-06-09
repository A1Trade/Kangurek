"use client";

import type { Progress } from "./storage";

export type BadgeDef = {
  id: string;
  emoji: string;
  name: string;
  desc: string;
  check: (p: Progress, ctx: BadgeContext) => boolean;
};

export type BadgeContext = {
  totalCorrect: number;
  totalAttempted: number;
  uniqueOriginalsCorrect: number; // unikalne kangur-maluch-* poprawnie
  streakCurrent: number;
  streakLongest: number;
  perfectQuizzes: number; // quiz 3/3
  blockMastery: Record<string, number>; // blockCode -> liczba ukonczonych lekcji
  oneDayMax: number; // max zadan poprawnie w jeden dzien
};

export const BADGES: BadgeDef[] = [
  {
    id: "first-step",
    emoji: "🐣",
    name: "Pierwszy krok",
    desc: "Rozwiaz pierwsze zadanie poprawnie",
    check: (_p, c) => c.totalCorrect >= 1,
  },
  {
    id: "streak-3",
    emoji: "🔥",
    name: "3 dni z rzedu",
    desc: "Cwicz przez 3 dni z rzedu",
    check: (_p, c) => c.streakCurrent >= 3 || c.streakLongest >= 3,
  },
  {
    id: "streak-7",
    emoji: "⚡",
    name: "Tydzien z Kangurkiem",
    desc: "Cwicz przez 7 dni z rzedu",
    check: (_p, c) => c.streakCurrent >= 7 || c.streakLongest >= 7,
  },
  {
    id: "streak-30",
    emoji: "👑",
    name: "Niezlomny",
    desc: "Cwicz przez 30 dni z rzedu",
    check: (_p, c) => c.streakLongest >= 30,
  },
  {
    id: "century",
    emoji: "💯",
    name: "Setka",
    desc: "Rozwiaz poprawnie 100 zadan",
    check: (_p, c) => c.totalCorrect >= 100,
  },
  {
    id: "marathon",
    emoji: "🏃",
    name: "Maraton",
    desc: "Rozwiaz 50 zadan w jeden dzien",
    check: (_p, c) => c.oneDayMax >= 50,
  },
  {
    id: "originalist-20",
    emoji: "🦘",
    name: "Tropiciel oryginalow",
    desc: "Rozwiaz 20 oryginalnych zadan z Kangura",
    check: (_p, c) => c.uniqueOriginalsCorrect >= 20,
  },
  {
    id: "originalist-100",
    emoji: "🏆",
    name: "Znawca oryginalow",
    desc: "Rozwiaz 100 oryginalnych zadan z Kangura",
    check: (_p, c) => c.uniqueOriginalsCorrect >= 100,
  },
  {
    id: "quiz-perfect-5",
    emoji: "⭐",
    name: "Quiz mistrzu",
    desc: "Zrob 5 quizow z wynikiem 3/3",
    check: (_p, c) => c.perfectQuizzes >= 5,
  },
  {
    id: "block-a",
    emoji: "🔢",
    name: "Mistrz arytmetyki",
    desc: "Ukoncz wszystkie 8 lekcji bloku A",
    check: (_p, c) => (c.blockMastery["A"] ?? 0) >= 8,
  },
  {
    id: "block-c",
    emoji: "📐",
    name: "Mistrz geometrii",
    desc: "Ukoncz wszystkie 8 lekcji bloku C",
    check: (_p, c) => (c.blockMastery["C"] ?? 0) >= 8,
  },
  {
    id: "block-g",
    emoji: "🧠",
    name: "Mistrz logiki",
    desc: "Ukoncz wszystkie 6 lekcji bloku G",
    check: (_p, c) => (c.blockMastery["G"] ?? 0) >= 6,
  },
  {
    id: "block-h",
    emoji: "🎲",
    name: "Mistrz kombinatoryki",
    desc: "Ukoncz wszystkie 4 lekcje bloku H",
    check: (_p, c) => (c.blockMastery["H"] ?? 0) >= 4,
  },
  {
    id: "all-blocks",
    emoji: "🌟",
    name: "Wszechstronny",
    desc: "Ukoncz co najmniej 1 lekcje z kazdego bloku A-I",
    check: (_p, c) => "ABCDEFGHI".split("").every((b) => (c.blockMastery[b] ?? 0) >= 1),
  },
];
