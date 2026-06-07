"use client";

/**
 * Tracking postepu w localStorage.
 * Kazda lekcja ma liste WSZYSTKICH podejsc - kazda wersja moze byc zrobiona wiele razy.
 */

const KEY = "kangurek-progress-v3";
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

export type Progress = {
  lessons: Record<string, LessonProgress>;
};

const empty = (): Progress => ({ lessons: {} });

function read(): Progress {
  if (typeof window === "undefined") return empty();
  try {
    const raw = window.localStorage.getItem(KEY);
    if (raw) return { ...empty(), ...JSON.parse(raw) };
    // migrate v2 -> v3
    const v2 = window.localStorage.getItem(KEY_V2);
    if (v2) {
      const p = migrateV2(JSON.parse(v2));
      window.localStorage.setItem(KEY, JSON.stringify(p));
      return p;
    }
    // migrate v1 -> v3
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

export function recordProblemAttempt(
  lessonId: string,
  versionId: string,
  problemId: string,
  picked: string,
  correct: boolean,
) {
  const p = read();
  const l = ensureLesson(p, lessonId);
  let active = findActiveAttempt(l, versionId);
  if (!active) {
    // rozpocznij implicitnie
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
  write(p);
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
