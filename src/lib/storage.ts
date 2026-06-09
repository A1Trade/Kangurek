"use client";

/**
 * Tracking postepu w localStorage.
 * Kazda lekcja ma liste WSZYSTKICH podejsc - kazda wersja moze byc zrobiona wiele razy.
 */

import { applyReview, isoDay, newReview, type ReviewItem } from "./srs";
import { BADGES } from "./badges";
import { LESSON_PLAN } from "./lesson-plan";

function lessonIdToNumber(lid: string): number | null {
  const m = lid.match(/^l(\d{2})$/);
  return m ? parseInt(m[1], 10) : null;
}

export function lessonIdToBlock(lid: string): string | undefined {
  const num = lessonIdToNumber(lid);
  if (num === null) return undefined;
  const plan = LESSON_PLAN.find((p) => p.number === num);
  return plan?.blockCode;
}

export function lessonIdToTopic(lid: string): string | undefined {
  const num = lessonIdToNumber(lid);
  if (num === null) return undefined;
  const plan = LESSON_PLAN.find((p) => p.number === num);
  return plan?.topic;
}

const KEY = "kangurek-progress-v4";
const KEY_V3 = "kangurek-progress-v3";
const KEY_V2 = "kangurek-progress-v2";
const KEY_V1 = "kangurek-progress-v1";

export type ProblemAttempt = {
  picked: string;
  correct: boolean;
  attempts: number;
  attemptedAt: string;
};

export type VersionAttempt = {
  versionId: string;
  attemptNumber: number;
  startedAt: string;
  finishedAt?: string;
  durationSec: number;
  problems: Record<string, ProblemAttempt>;
  quizScore?: number;
  quizMax?: number;
  completed: boolean;
};

export type LessonProgress = {
  lessonId: string;
  attempts: VersionAttempt[];
  lastActiveVersion: string;
};

export type StreakInfo = {
  current: number;
  longest: number;
  lastActivityDate: string; // YYYY-MM-DD
};

export type Progress = {
  lessons: Record<string, LessonProgress>;
  reviews: Record<string, ReviewItem>;
  streak: StreakInfo;
  badges: { id: string; earnedAt: string }[];
};

const empty = (): Progress => ({
  lessons: {},
  reviews: {},
  streak: { current: 0, longest: 0, lastActivityDate: "" },
  badges: [],
});

function read(): Progress {
  if (typeof window === "undefined") return empty();
  try {
    const raw = window.localStorage.getItem(KEY);
    if (raw) return { ...empty(), ...JSON.parse(raw) };
    // migrate v3 -> v4 (zachowaj lekcje, dodaj puste reviews/streak/badges)
    const v3 = window.localStorage.getItem(KEY_V3);
    if (v3) {
      const p = { ...empty(), ...JSON.parse(v3) };
      window.localStorage.setItem(KEY, JSON.stringify(p));
      return p;
    }
    // migrate v2 -> v4
    const v2 = window.localStorage.getItem(KEY_V2);
    if (v2) {
      const p = migrateV2(JSON.parse(v2));
      window.localStorage.setItem(KEY, JSON.stringify(p));
      return p;
    }
    // migrate v1 -> v4
    const v1 = window.localStorage.getItem(KEY_V1);
    if (v1) {
      const p = migrateV1(JSON.parse(v1));
      window.localStorage.setItem(KEY, JSON.stringify(p));
      return p;
    }
    return empty();
  } catch {
    return empty();
  }
}

type V2VersionAttempt = {
  versionId: string;
  startedAt?: string;
  finishedAt?: string;
  durationSec: number;
  problems: Record<string, ProblemAttempt>;
  quizScore?: number;
  quizMax?: number;
  completed: boolean;
};

type V2Lesson = {
  lessonId: string;
  versions: Record<string, V2VersionAttempt>;
  lastActiveVersion: string;
};

function migrateV2(v2: { lessons?: Record<string, V2Lesson> }): Progress {
  const p = empty();
  for (const [lessonId, l] of Object.entries(v2.lessons ?? {})) {
    const attempts: VersionAttempt[] = [];
    for (const v of Object.values(l.versions ?? {})) {
      attempts.push({
        versionId: v.versionId,
        attemptNumber: 1,
        startedAt: v.startedAt ?? new Date().toISOString(),
        finishedAt: v.finishedAt,
        durationSec: v.durationSec,
        problems: v.problems ?? {},
        quizScore: v.quizScore,
        quizMax: v.quizMax,
        completed: v.completed,
      });
    }
    p.lessons[lessonId] = {
      lessonId,
      attempts,
      lastActiveVersion: l.lastActiveVersion ?? "v1",
    };
  }
  return p;
}

function migrateV1(v1: { lessonsCompleted?: Record<string, { quizScore: number; completedAt: string }> }): Progress {
  const p = empty();
  for (const [lessonId, data] of Object.entries(v1.lessonsCompleted ?? {})) {
    p.lessons[lessonId] = {
      lessonId,
      lastActiveVersion: "v1",
      attempts: [
        {
          versionId: "v1",
          attemptNumber: 1,
          startedAt: data.completedAt,
          finishedAt: data.completedAt,
          durationSec: 0,
          problems: {},
          quizScore: data.quizScore,
          quizMax: 3,
          completed: true,
        },
      ],
    };
  }
  return p;
}

function write(p: Progress) {
  if (typeof window === "undefined") return;
  window.localStorage.setItem(KEY, JSON.stringify(p));
  window.dispatchEvent(new Event("kangurek-progress-update"));
}

export function getProgress(): Progress {
  return read();
}

function ensureLesson(p: Progress, lessonId: string): LessonProgress {
  if (!p.lessons[lessonId]) {
    p.lessons[lessonId] = { lessonId, attempts: [], lastActiveVersion: "v1" };
  }
  return p.lessons[lessonId];
}

/** Zwraca aktywne (nieukonczone) podejscie dla danej wersji, jezeli istnieje. */
function findActiveAttempt(l: LessonProgress, versionId: string): VersionAttempt | undefined {
  for (let i = l.attempts.length - 1; i >= 0; i--) {
    const a = l.attempts[i];
    if (a.versionId === versionId && !a.completed) return a;
  }
  return undefined;
}

function nextAttemptNumber(l: LessonProgress, versionId: string): number {
  let max = 0;
  for (const a of l.attempts) {
    if (a.versionId === versionId && a.attemptNumber > max) max = a.attemptNumber;
  }
  return max + 1;
}

/**
 * Rozpoczyna podejscie. Jezeli jest aktywne (nieukonczone) - kontynuuje je.
 * Jezeli ostatnie bylo ukonczone - zaczyna NOWE podejscie (atemptNumber+1).
 */
export function startLessonVersion(lessonId: string, versionId: string) {
  const p = read();
  const l = ensureLesson(p, lessonId);
  l.lastActiveVersion = versionId;
  const active = findActiveAttempt(l, versionId);
  if (!active) {
    l.attempts.push({
      versionId,
      attemptNumber: nextAttemptNumber(l, versionId),
      startedAt: new Date().toISOString(),
      durationSec: 0,
      problems: {},
      completed: false,
    });
  }
  write(p);
}

/** Wymusza nowe podejscie (uzywane przez przycisk "zrob jeszcze raz"). */
export function restartLessonVersion(lessonId: string, versionId: string) {
  const p = read();
  const l = ensureLesson(p, lessonId);
  l.lastActiveVersion = versionId;
  // jezeli jest aktywne i puste - zostaw, w przeciwnym razie dodaj nowe
  const active = findActiveAttempt(l, versionId);
  if (active && Object.keys(active.problems).length === 0 && active.quizScore === undefined) {
    active.startedAt = new Date().toISOString();
  } else {
    l.attempts.push({
      versionId,
      attemptNumber: nextAttemptNumber(l, versionId),
      startedAt: new Date().toISOString(),
      durationSec: 0,
      problems: {},
      completed: false,
    });
  }
  write(p);
}

export type ProblemMeta = {
  topic: string;
  block?: string;
};

export function recordProblemAttempt(
  lessonId: string,
  versionId: string,
  problemId: string,
  picked: string,
  correct: boolean,
  meta?: ProblemMeta,
) {
  const p = read();
  const l = ensureLesson(p, lessonId);
  let active = findActiveAttempt(l, versionId);
  if (!active) {
    active = {
      versionId,
      attemptNumber: nextAttemptNumber(l, versionId),
      startedAt: new Date().toISOString(),
      durationSec: 0,
      problems: {},
      completed: false,
    };
    l.attempts.push(active);
  }
  const prev = active.problems[problemId];
  active.problems[problemId] = {
    picked,
    correct,
    attempts: (prev?.attempts ?? 0) + 1,
    attemptedAt: new Date().toISOString(),
  };

  // --- SRS: dodaj/aktualizuj review jezeli bledne ---
  if (!correct && meta) {
    if (!p.reviews[problemId]) {
      p.reviews[problemId] = newReview(problemId, lessonId, versionId, meta.topic, meta.block);
    } else {
      // bledna powtorzenie -> reset
      p.reviews[problemId] = applyReview(p.reviews[problemId], false);
    }
  } else if (correct && p.reviews[problemId] && !p.reviews[problemId].mastered) {
    // poprawna odpowiedz w trakcie zwyklej lekcji tez liczy sie jako review
    p.reviews[problemId] = applyReview(p.reviews[problemId], true);
  }

  // --- Streak: aktualizuj jezeli pierwsza aktywnosc dzisiaj ---
  bumpStreak(p);
  // --- Badges: sprawdz nowe ---
  checkBadges(p);

  write(p);
}

function bumpStreak(p: Progress) {
  const today = isoDay();
  const last = p.streak.lastActivityDate;
  if (last === today) return;
  if (!last) {
    p.streak.current = 1;
  } else {
    const yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);
    if (last === isoDay(yesterday)) {
      p.streak.current += 1;
    } else {
      p.streak.current = 1;
    }
  }
  p.streak.lastActivityDate = today;
  if (p.streak.current > p.streak.longest) {
    p.streak.longest = p.streak.current;
  }
}

function checkBadges(p: Progress) {
  const ctx = computeBadgeContext(p);
  const owned = new Set(p.badges.map((b) => b.id));
  for (const def of BADGES) {
    if (owned.has(def.id)) continue;
    if (def.check(p, ctx)) {
      p.badges.push({ id: def.id, earnedAt: new Date().toISOString() });
    }
  }
}

function computeBadgeContext(p: Progress) {
  let totalCorrect = 0;
  let totalAttempted = 0;
  let perfectQuizzes = 0;
  const uniqueOriginalsCorrect = new Set<string>();
  const perDay: Record<string, number> = {};
  const blockMastery: Record<string, number> = {};

  for (const l of Object.values(p.lessons)) {
    let lessonHasCompleted = false;
    for (const a of l.attempts) {
      if (a.completed) lessonHasCompleted = true;
      if (a.completed && a.quizScore !== undefined && a.quizMax === a.quizScore) {
        perfectQuizzes += 1;
      }
      for (const [pid, pr] of Object.entries(a.problems)) {
        totalAttempted += 1;
        if (pr.correct) {
          totalCorrect += 1;
          if (pid.startsWith("kangur-maluch-")) {
            uniqueOriginalsCorrect.add(pid);
          }
          const day = pr.attemptedAt.slice(0, 10);
          perDay[day] = (perDay[day] ?? 0) + 1;
        }
      }
    }
    if (lessonHasCompleted) {
      const block = lessonIdToBlock(l.lessonId);
      if (block) {
        blockMastery[block] = (blockMastery[block] ?? 0) + 1;
      }
    }
  }

  const oneDayMax = Object.values(perDay).reduce((m, v) => Math.max(m, v), 0);

  return {
    totalCorrect,
    totalAttempted,
    uniqueOriginalsCorrect: uniqueOriginalsCorrect.size,
    streakCurrent: p.streak.current,
    streakLongest: p.streak.longest,
    perfectQuizzes,
    blockMastery,
    oneDayMax,
  };
}

export function finishLessonVersion(
  lessonId: string,
  versionId: string,
  quizScore: number,
  quizMax: number,
) {
  const p = read();
  const l = ensureLesson(p, lessonId);
  const active = findActiveAttempt(l, versionId);
  if (!active) return;
  active.finishedAt = new Date().toISOString();
  active.durationSec = Math.max(
    0,
    Math.round((new Date(active.finishedAt).getTime() - new Date(active.startedAt).getTime()) / 1000),
  );
  active.quizScore = quizScore;
  active.quizMax = quizMax;
  active.completed = true;
  write(p);
}

export function getLessonProgress(lessonId: string): LessonProgress | undefined {
  return read().lessons[lessonId];
}

/** Najnowsze podejscie dla wersji (zakonczone lub w trakcie). */
export function getLatestVersionAttempt(lessonId: string, versionId: string): VersionAttempt | undefined {
  const l = read().lessons[lessonId];
  if (!l) return undefined;
  for (let i = l.attempts.length - 1; i >= 0; i--) {
    if (l.attempts[i].versionId === versionId) return l.attempts[i];
  }
  return undefined;
}

export function getAttemptsForVersion(lessonId: string, versionId: string): VersionAttempt[] {
  const l = read().lessons[lessonId];
  if (!l) return [];
  return l.attempts.filter((a) => a.versionId === versionId);
}

export function resetProgress() {
  if (typeof window === "undefined") return;
  window.localStorage.removeItem(KEY);
  window.localStorage.removeItem(KEY_V2);
  window.localStorage.removeItem(KEY_V1);
  window.dispatchEvent(new Event("kangurek-progress-update"));
}

// =================
// SRS / BADGES / WEAK TOPICS
// =================

import { isDueToday } from "./srs";

/** Zadania do powtorzenia dzis (SRS). */
export function getDueReviews(): ReviewItem[] {
  const p = read();
  return Object.values(p.reviews).filter(isDueToday);
}

/** Wszystkie zadania bledne (lista pomylek). */
export function getAllErrors(): ReviewItem[] {
  const p = read();
  return Object.values(p.reviews);
}

/** Zarejestruj wynik powtorki SRS (poza zwykla lekcja). */
export function recordReviewAnswer(problemId: string, correct: boolean) {
  const p = read();
  const item = p.reviews[problemId];
  if (!item) return;
  p.reviews[problemId] = applyReview(item, correct);
  bumpStreak(p);
  checkBadges(p);
  write(p);
}

/** Streak info. */
export function getStreak(): StreakInfo {
  return read().streak;
}

/** Lista zdobytych badge IDs. */
export function getBadges(): { id: string; earnedAt: string }[] {
  return read().badges;
}

/** Statystyki per topic — pokazuje slabe tematy. */
export function getTopicStats(): Record<string, { correct: number; wrong: number; pct: number }> {
  const p = read();
  const stats: Record<string, { correct: number; wrong: number }> = {};
  for (const l of Object.values(p.lessons)) {
    const topic = lessonIdToTopic(l.lessonId);
    if (!topic) continue;
    for (const a of l.attempts) {
      for (const pr of Object.values(a.problems)) {
        if (!stats[topic]) stats[topic] = { correct: 0, wrong: 0 };
        if (pr.correct) stats[topic].correct += 1;
        else stats[topic].wrong += 1;
      }
    }
  }
  const out: Record<string, { correct: number; wrong: number; pct: number }> = {};
  for (const [k, v] of Object.entries(stats)) {
    const total = v.correct + v.wrong;
    out[k] = { ...v, pct: total === 0 ? 0 : Math.round((v.correct / total) * 100) };
  }
  return out;
}

/** Zwraca top 3 najsłabsze tematy (% poprawnych). Filtruje te z >=3 probami. */
export function getWeakTopics(): { topic: string; pct: number; total: number }[] {
  const stats = getTopicStats();
  const list: { topic: string; pct: number; total: number }[] = [];
  for (const [topic, s] of Object.entries(stats)) {
    const total = s.correct + s.wrong;
    if (total < 3) continue;
    list.push({ topic, pct: s.pct, total });
  }
  list.sort((a, b) => a.pct - b.pct);
  return list.slice(0, 3);
}

/** Sumaryczne statystyki dla dziennika. */
export function getSummary() {
  const p = read();
  const lessons = Object.values(p.lessons);
  const completedLessons = lessons.filter((l) =>
    l.attempts.some((a) => a.completed),
  );
  let totalProblems = 0;
  let correctProblems = 0;
  let totalSec = 0;
  let totalAttempts = 0;
  let completedAttempts = 0;
  for (const l of lessons) {
    for (const a of l.attempts) {
      totalAttempts += 1;
      if (a.completed) completedAttempts += 1;
      totalSec += a.durationSec;
      for (const pr of Object.values(a.problems)) {
        totalProblems += 1;
        if (pr.correct) correctProblems += 1;
      }
    }
  }
  return {
    lessonsTotal: lessons.length,
    lessonsCompleted: completedLessons.length,
    totalAttempts,
    completedAttempts,
    totalProblems,
    correctProblems,
    accuracyPct: totalProblems === 0 ? 0 : Math.round((correctProblems / totalProblems) * 100),
    totalMinutes: Math.round(totalSec / 60),
  };
}
