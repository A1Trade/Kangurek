import Link from "next/link";
import { getPlanWithStatus } from "@/lib/data/lessons";
import { BLOCKS } from "@/lib/lesson-plan";
import { ProgressBar, LessonDoneBadge } from "@/components/ProgressBar";
import { HomeWidget } from "@/components/HomeWidget";

const BLOCK_ICON: Record<string, string> = {
  A: "🧮", B: "🔀", C: "📐", D: "🧊", E: "📏",
  F: "🕒", G: "🧠", H: "🎲", I: "🏆",
};

export default function HomePage() {
  const plan = getPlanWithStatus();
  const generatedCount = plan.filter((p) => p.generated).length;

  return (
    <div className="space-y-8 kanim">
      {/* Hero */}
      <section className="khero p-8 md:p-10">
        <div className="flex items-start gap-4">
          <span aria-hidden className="text-5xl drop-shadow-sm">🦘</span>
          <div className="flex-1">
            <p className="text-[13px] font-semibold uppercase tracking-wider text-amber-700/80 mb-1">
              Kurs MALUCH · klasa 4
            </p>
            <h1 className="k-hero-title text-3xl font-bold text-slate-900 mb-2">
              Zostan mistrzem Kangurka.
            </h1>
            <p className="text-[15px] text-slate-700 leading-snug max-w-xl">
              50 lekcji po 10–20 minut. Krotka teoria, zadania w stylu Kangurka i quiz.
              Mozesz tez wziac udzial w pelnej symulacji konkursu.
            </p>
            <div className="mt-5 flex gap-2 flex-wrap">
              <Link href="/lekcje/l01" className="kbtn kbtn-primary">
                Zacznij naukę →
              </Link>
              <Link href="/symulacja" className="kbtn kbtn-secondary">
                Symulacja konkursu
              </Link>
            </div>
          </div>
        </div>
      </section>

      <HomeWidget />

      <ProgressBar total={plan.length} />

      {generatedCount < plan.length && (
        <div className="kcard flex items-start gap-3">
          <span className="text-2xl" aria-hidden>⏳</span>
          <div className="text-sm text-slate-700">
            <strong className="text-slate-900">Trwa rozbudowa tresci.</strong> Aktualnie dostepnych:{" "}
            <strong>{generatedCount} / {plan.length}</strong> lekcji.
            Reszta pojawi sie wkrotce — wracaj!
          </div>
        </div>
      )}

      {/* Bloki tematyczne */}
      <div className="space-y-10">
        {BLOCKS.map((block) => {
          const items = plan.filter((p) => p.blockCode === block.code);
          return (
            <section key={block.code}>
              <div className="flex items-baseline gap-3 mb-4 px-1">
                <span className="text-2xl" aria-hidden>{BLOCK_ICON[block.code]}</span>
                <div>
                  <div className="text-[11px] uppercase tracking-wider font-bold text-slate-500">
                    Blok {block.code} · lekcje {block.lessons}
                  </div>
                  <h2 className="text-xl font-bold text-slate-900 tracking-tight">{block.title}</h2>
                </div>
              </div>
              <div className="grid sm:grid-cols-2 gap-3">
                {items.map((item) => (
                  <Link
                    key={item.id}
                    href={item.generated ? `/lekcje/${item.id}` : "#"}
                    aria-disabled={!item.generated}
                    className={`ktile flex items-start gap-4 ${
                      !item.generated ? "ktile-locked" : ""
                    }`}
                  >
                    <div className={`knum knum-${item.blockCode}`}>{item.number}</div>
                    <div className="flex-1 min-w-0">
                      <div className="font-semibold text-slate-900 text-[15px] tracking-tight">
                        {item.title}
                      </div>
                      <div className="mt-1 flex items-center gap-2 flex-wrap">
                        <span className="k-pill">
                          <span aria-hidden>⏱</span> {item.estimatedMinutes} min
                        </span>
                        <LessonDoneBadge lessonId={item.id} />
                        {!item.generated && (
                          <span className="kbadge kbadge-gray">wkrotce</span>
                        )}
                      </div>
                    </div>
                  </Link>
                ))}
              </div>
            </section>
          );
        })}
      </div>
    </div>
  );
}
