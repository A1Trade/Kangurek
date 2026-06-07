# Kangurek 🦘

Aplikacja edukacyjna do przygotowania ucznia klasy 4 SP do konkursu **Kangur Matematyczny (kategoria MALUCH)**.
50 lekcji w 9 blokach tematycznych. Lekcje, zadania, podpowiedzi i symulacja konkursu generowane przez Claude AI (Anthropic).

## Stack

- **Next.js 16** (App Router) + **React 19** + **TypeScript** + **Tailwind 4**
- **Anthropic SDK** (Claude Opus 4.7 / Sonnet 4.6 / Haiku 4.5)
- **Zod** do walidacji JSON-ow generowanych przez AI
- **localStorage** do trackingu postepu (zero backendu)

## Szybki start

```bash
# 1. Zaleznosci - juz zainstalowane, ale gdy klonujesz na nowo:
npm install

# 2. Klucz Anthropic (https://console.anthropic.com/settings/keys)
cp .env.local.example .env.local
# wklej do ANTHROPIC_API_KEY=sk-ant-...

# 3. Sparsuj arkusze historyczne (PDF) do JSON-ow
npm run parse:arkusze            # wszystkie 13 arkuszy (~5 minut, ~$0.30 API)
npm run parse:arkusze -- 2019    # tylko jeden rok (do testu)
npm run parse:arkusze -- --force # nadpisz juz sparsowane

# 4. Wygeneruj 50 lekcji (Opus 4.7)
npm run generate:lessons              # caly kurs (~15-20 minut, ~$10-15 API)
npm run generate:lessons -- 1-3       # tylko lekcje 1-3 (test jakosci)
npm run generate:lessons -- --force   # nadpisz

# 5. Dev server
npm run dev
# -> otworz http://localhost:3000
```

## Struktura projektu

```
data/
  arkusze/         # PDF-y historycznych arkuszy (wrzucone recznie)
  parsed/          # JSON-y z wyekstrahowanymi zadaniami (output parsera)
  lessons/         # 50 wygenerowanych lekcji (l01.json ... l50.json)
  index.json       # spis lekcji do UI

src/
  app/
    page.tsx                  # lista 50 lekcji pogrupowanych w bloki
    lekcje/[id]/page.tsx      # widok pojedynczej lekcji
    symulacja/                # pelny konkurs 24 zadania / 75 min
    api/
      podpowiedz/route.ts     # POST -> Haiku 4.5 daje hint
      wytlumacz/route.ts      # POST -> Opus 4.7 tlumaczy zadanie
      generuj/route.ts        # POST -> Sonnet 4.6 generuje nowe zadanie

  components/
    ProblemCard.tsx           # zadanie z ABCDE, podpowiedzia, rozwiazaniem
    Quiz.tsx                  # quiz koncowy lekcji (3 pytania)
    ProgressBar.tsx           # tracker postepu (localStorage)

  lib/
    agents/anthropic.ts       # wrapper na Anthropic SDK
    lesson-plan.ts            # plan 50 lekcji (statyczny)
    data/lessons.ts           # ladowanie JSON-ow lekcji
    storage.ts                # localStorage helpers

  types/schemas.ts            # Zod: Problem, Solution, Lesson, QuizQuestion

scripts/
  parse-arkusze.ts            # build-time: PDF -> JSON
  generate-lessons.ts         # build-time: plan + arkusze -> lekcje
```

## Agenci AI

### Build-time (offline, w scripts/)

| Agent | Model | Zadanie |
|---|---|---|
| Parser arkuszy | Sonnet 4.6 | Czyta PDF, ekstrahuje 24 zadania, klasyfikuje, rozwiazuje |
| Generator lekcji | Opus 4.7 | Teoria + 7 zadan + rozwiazania + quiz, na bazie planu i przykladow |

### Runtime (online, API routes)

| Endpoint | Model | Zadanie |
|---|---|---|
| `/api/podpowiedz` | Haiku 4.5 | Progresywna podpowiedz (poziom 1-3) |
| `/api/wytlumacz` | Opus 4.7 | Alternatywne tlumaczenie zadania |
| `/api/generuj` | Sonnet 4.6 | Nowe zadanie na zywo o danym temacie/trudnosci |

## Plan 50 lekcji

| Blok | Lekcje | Temat |
|---|---|---|
| A | 1-8 | Liczby i dzialania |
| B | 9-13 | Wzory, ciagi, regularnosci |
| C | 14-21 | Geometria plaska |
| D | 22-26 | Geometria przestrzenna |
| E | 27-32 | Pomiary i jednostki |
| F | 33-35 | Czas i kalendarz |
| G | 36-41 | Logika i myslenie |
| H | 42-45 | Kombinatoryka i liczenie |
| I | 46-50 | Strategie konkursowe + symulacje |

Pelny plan (z podtematami i celami nauczania): [src/lib/lesson-plan.ts](src/lib/lesson-plan.ts)

## Komendy

```bash
npm run dev               # dev server (Turbopack)
npm run build             # produkcyjny build
npm start                 # start produkcyjny
npm run lint              # ESLint
npm run parse:arkusze     # PDF -> JSON
npm run generate:lessons  # generacja lekcji
```

## Uwagi

- **Arkusze sa tylko referencja stylu** dla generatora - lekcje sa pisane od nowa, nie kopiuja oryginalnych zadan.
- **Kategoria MALUCH** to klasy 3-4 SP. Dla klasy 4 to wlasciwa kategoria.
- **Postep zapisuje sie w localStorage** - kazda przegladarka ma osobny licznik.
- **Symulacja konkursu** losuje 24 zadania (8x3pkt + 8x4pkt + 8x5pkt) z bazy oryginalnych arkuszy.
