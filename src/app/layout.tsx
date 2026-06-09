import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: "Kangurek - przygotowanie do konkursu Kangur Maluch",
  description: "50 lekcji matematyki dla klas 3-4 z generowaniem zadan przez AI",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pl" className="h-full antialiased">
      <body className="min-h-full flex flex-col">
        <header className="ktopbar">
          <div className="max-w-5xl mx-auto px-4 py-3 flex items-center justify-between">
            <Link href="/" className="flex items-center gap-2.5 group">
              <span
                aria-hidden
                className="text-2xl transition-transform duration-300 group-hover:scale-110 group-hover:-rotate-6"
              >
                🦘
              </span>
              <div className="flex flex-col leading-tight">
                <span className="text-[17px] font-bold text-slate-900 tracking-tight">Kangurek</span>
                <span className="text-[10px] uppercase tracking-wide text-slate-500 font-semibold">
                  Maluch · klasa 4
                </span>
              </div>
            </Link>
            <nav className="flex gap-1 text-sm flex-wrap">
              <Link href="/" className="kbtn kbtn-ghost kbtn-sm">
                Lekcje
              </Link>
              <Link href="/powtorka" className="kbtn kbtn-ghost kbtn-sm">
                Powtorka
              </Link>
              <Link href="/bledy" className="kbtn kbtn-ghost kbtn-sm">
                Bledy
              </Link>
              <Link href="/odznaki" className="kbtn kbtn-ghost kbtn-sm">
                Odznaki
              </Link>
              <Link href="/dziennik" className="kbtn kbtn-ghost kbtn-sm">
                Dziennik
              </Link>
              <Link href="/symulacja" className="kbtn kbtn-ghost kbtn-sm">
                Symulacja
              </Link>
            </nav>
          </div>
        </header>
        <main className="flex-1 max-w-5xl mx-auto w-full px-4 py-8">{children}</main>
      </body>
    </html>
  );
}
