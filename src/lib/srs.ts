"use client";

/**
 * Spaced Repetition System (Anki-like).
 * Bledne zadania wracaja po 1, 3, 7, 14 dniach.
 * Poprawna odpowiedz - awansuje do nastepnego interwalu.
 * Bledna - resetuje do 1 dnia.
 */

export const SRS_INTERVALS = [1, 3, 7, 14] as const;

export type ReviewItem = {
  problemId: string;
  lessonId: string;
  versionId: string;
  topic: string; // TopicTag
  block?: string; // blockCode
  intervalIdx: number; // 0..3 -> 1, 3, 7, 14 dni
  nextReviewAt: string; // ISO date YYYY-MM-DD
  mastered: boolean; // gdy przeszedl wszystkie interwaly
  history: { ts: string; correct: boolean }[];
  firstWrongAt: string;
};

function todayDate(): Date {
  const d = new Date();
  d.setHours(0, 0, 0, 0);
  return d;
}

function addDays(date: Date, days: number): Date {
  const d = new Date(date);
  d.setDate(d.getDate() + days);
  d.setHours(0, 0, 0, 0);
  return d;
}

export function isoDay(d: Date = new Date()): string {
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  return `${y}-${m}-${day}`;
}

/** Tworzy nowy ReviewItem dla swiezo zlej odpowiedzi. */
export function newReview(
  problemId: string,
  lessonId: string,
  versionId: string,
  topic: string,
  block?: string,
): ReviewItem {
  const nowIso = new Date().toISOString();
  return {
    problemId,
    lessonId,
    versionId,
    topic,
    block,
    intervalIdx: 0,
    nextReviewAt: isoDay(addDays(todayDate(), SRS_INTERVALS[0])),
    mastered: false,
    history: [{ ts: nowIso, correct: false }],
    firstWrongAt: nowIso,
  };
}

/** Aktualizuje istniejacy ReviewItem na podstawie odpowiedzi w sesji powtorkowej. */
export function applyReview(item: ReviewItem, correct: boolean): ReviewItem {
  const nowIso = new Date().toISOString();
  const updated = { ...item, history: [...item.history, { ts: nowIso, correct }] };
  if (correct) {
    const nextIdx = item.intervalIdx + 1;
    if (nextIdx >= SRS_INTERVALS.length) {
      updated.mastered = true;
      updated.intervalIdx = nextIdx;
    } else {
      updated.intervalIdx = nextIdx;
      updated.nextReviewAt = isoDay(addDays(todayDate(), SRS_INTERVALS[nextIdx]));
    }
  } else {
    // reset do pierwszego interwalu
    updated.intervalIdx = 0;
    updated.nextReviewAt = isoDay(addDays(todayDate(), SRS_INTERVALS[0]));
    updated.mastered = false;
  }
  return updated;
}

export function isDueToday(item: ReviewItem): boolean {
  if (item.mastered) return false;
  return item.nextReviewAt <= isoDay();
}
