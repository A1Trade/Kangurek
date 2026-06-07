import Link from "next/link";
import { notFound } from "next/navigation";
import { getLesson, getLessonIndex } from "@/lib/data/lessons";
import { LessonView } from "@/components/LessonView";

export async function generateStaticParams() {
  return getLessonIndex().map((i) => ({ id: i.id }));
}

export default async function LessonPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const lesson = getLesson(id);
  if (!lesson) notFound();

  return (
    <div className="space-y-6">
      <nav className="flex items-center justify-between text-[13px]">
        <Link href="/" className="kbtn kbtn-ghost kbtn-sm">
          ← Wszystkie lekcje
        </Link>
        <Link href="/dziennik" className="kbtn kbtn-ghost kbtn-sm">
          Moj dziennik →
        </Link>
      </nav>

      <LessonView lesson={lesson} />

      <NextPrev currentNumber={lesson.number} />
    </div>
  );
}

function NextPrev({ currentNumber }: { currentNumber: number }) {
  const index = getLessonIndex();
  const prev = index.find((i) => i.number === currentNumber - 1);
  const next = index.find((i) => i.number === currentNumber + 1);
  return (
    <div className="flex justify-between gap-2 pt-4">
      {prev ? (
        <Link href={`/lekcje/${prev.id}`} className="kbtn kbtn-secondary">
          ← {prev.title}
        </Link>
      ) : (
        <span />
      )}
      {next ? (
        <Link href={`/lekcje/${next.id}`} className="kbtn kbtn-primary">
          {next.title} →
        </Link>
      ) : (
        <span />
      )}
    </div>
  );
}
