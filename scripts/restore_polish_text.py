"""Wyciaga z PDF-ow Kangurka tekst zadan z polskimi znakami (a, c, e, l, o, s, z, n)
i zapisuje mape problemId -> {statement, choices: {A..E}} do JSON.
Potem aplikuje je do lekcji w data/lessons/.

Dla PDF-ow bez warstwy tekstu (2016, 2025) - pomija (zostawia ASCII).
"""
import re
import json
from pathlib import Path
import fitz

PDF_MAP = {
    2012: "data/arkusze/m_2012.pdf",
    2013: "data/arkusze/m_2013.pdf",
    2014: "data/arkusze/m_2014.pdf",
    2015: "data/arkusze/m_2015.pdf",
    2018: "data/arkusze/m_2018.pdf",
    2019: "data/arkusze/m_2019.pdf",
    2020: "data/arkusze/m_2020.pdf",
    2021: "data/arkusze/m_2021.pdf",
    2022: "data/arkusze/m_2022.pdf",
    2023: "data/arkusze/M-2023-PL.pdf",
    2024: "data/arkusze/M-2024-PL.pdf",
}

# Regex: numer.\s, potem treść do A) ... B) ... C) ... D) ... E) ...
NUM_RE = re.compile(r"^\s*(\d{1,2})\.\s")
ANSWER_RE = re.compile(r"^([A-E])\)\s*(.*)$")


def parse_pdf(year: int, pdf_path: str) -> dict[int, dict]:
    """Zwraca {number: {statement: str, choices: {A..E}}}."""
    doc = fitz.open(pdf_path)
    # Sklej caly tekst z pages w jeden ciag (zachowujac kolejnosc) z page break markers
    full_text = ""
    for page in doc:
        full_text += page.get_text() + "\n"
    doc.close()

    # Podziel na bloki zadan: znajdz wszystkie pozycje "N. " na poczatku linii
    lines = full_text.split("\n")

    # Znajdz indeksy linii zaczynajacych zadania (1. ... 24.)
    # Heurystyka: znajdz pierwsze wystapienie kazdego numeru 1-24 w kolejnosci montonicznej
    candidates: list[tuple[int, int]] = []  # (line_idx, number)
    for i, line in enumerate(lines):
        m = NUM_RE.match(line)
        if not m:
            continue
        num = int(m.group(1))
        if not (1 <= num <= 24):
            continue
        candidates.append((i, num))

    # Wybierz pierwsze wystapienie kazdej liczby w rosnacej kolejnosci
    starts: list[tuple[int, int]] = []
    next_expected = 1
    used_indices: set[int] = set()
    for i, num in candidates:
        if num == next_expected:
            starts.append((i, num))
            used_indices.add(i)
            next_expected += 1
            if next_expected > 24:
                break

    # Fallback: jezeli nie znaleziono wszystkich, dopelnij brakujace szukajac dalej
    if next_expected <= 24:
        for i, num in candidates:
            if i in used_indices:
                continue
            if num >= next_expected:
                # czy jest miedzy starts?
                if not any(n == num for _, n in starts):
                    starts.append((i, num))
        starts.sort(key=lambda x: x[0])

    if not starts:
        return {}

    result: dict[int, dict] = {}
    for j, (start_idx, num) in enumerate(starts):
        end_idx = starts[j + 1][0] if j + 1 < len(starts) else len(lines)
        block_lines = lines[start_idx:end_idx]

        # Polacz linie i znajdz odpowiedzi A) B) C) D) E)
        # Statement = wszystko przed pierwsza linia A)
        statement_lines = []
        choices = {"A": "", "B": "", "C": "", "D": "", "E": ""}
        current_choice: str | None = None
        choice_lines: dict[str, list[str]] = {k: [] for k in "ABCDE"}

        for li, raw in enumerate(block_lines):
            line = raw.strip()
            if li == 0:
                # usun "N. " z poczatku
                line = NUM_RE.sub("", line, count=1)
            am = ANSWER_RE.match(line)
            if am:
                current_choice = am.group(1)
                choice_lines[current_choice].append(am.group(2))
            elif current_choice is None:
                if line:
                    statement_lines.append(line)
            else:
                if line:
                    choice_lines[current_choice].append(line)

        statement = " ".join(statement_lines).strip()
        # zlej linie wyborow
        for k in "ABCDE":
            choices[k] = " ".join(choice_lines[k]).strip()

        # Czyszczenie: usun "Pytania po X punkty" jezeli wpadlo
        statement = re.sub(r"\s*Pytania po \d+ punkt[yó]w?\s*", " ", statement).strip()

        # Heurystyka: jezeli statement zawiera tylko bardzo malo tekstu, prawdopodobnie blad
        if len(statement) < 5:
            continue

        result[num] = {
            "statement": statement,
            "choices": choices,
        }

    return result


def main():
    all_data: dict[str, dict] = {}
    for year, path in PDF_MAP.items():
        p = Path(path)
        if not p.exists():
            print(f"BRAK: {path}")
            continue
        parsed = parse_pdf(year, str(p))
        polish_count = sum(
            1 for d in parsed.values() if any(c in d["statement"] for c in "ąćęłńóśżźĄĆĘŁŃÓŚŻŹ")
        )
        print(f"{year}: {len(parsed)} zadan ({polish_count} z polskimi znakami)")
        for num, d in parsed.items():
            pid = f"kangur-maluch-{year}-{num}"
            all_data[pid] = d

    out = Path("scripts/polish_text.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    print(f"\nZapisano {len(all_data)} zadan do {out}")


if __name__ == "__main__":
    main()
