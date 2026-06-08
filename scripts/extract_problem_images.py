"""Wyciaga z PDF-ow arkuszy Kangurka wycinki zadan i zapisuje jako PNG.
Dla kazdego zadania znajduje pozycje numeru ('N.') na stronie i kropuje obszar
od tego numeru do nastepnego (lub do dolu strony).

Output: public/images/orig/{year}-{number}.png
"""
import re
import json
from pathlib import Path
import fitz  # pymupdf

PDF_MAP = {
    2012: "data/arkusze/m_2012.pdf",
    2013: "data/arkusze/m_2013.pdf",
    2014: "data/arkusze/m_2014.pdf",
    2015: "data/arkusze/m_2015.pdf",
    2016: "data/arkusze/m_2016.pdf",
    2018: "data/arkusze/m_2018.pdf",
    2019: "data/arkusze/m_2019.pdf",
    2020: "data/arkusze/m_2020.pdf",
    2021: "data/arkusze/m_2021.pdf",
    2022: "data/arkusze/m_2022.pdf",
    2023: "data/arkusze/M-2023-PL.pdf",
    2024: "data/arkusze/M-2024-PL.pdf",
    2025: "data/arkusze/M-2025-PL.pdf",
}

OUT_DIR = Path("public/images/orig")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Regex dla numeru zadania na poczatku bloku (od 1 do 24, kropka, spacja)
NUM_RE = re.compile(r"^\s*(\d{1,2})\.\s")
ZOOM = 2.5  # rozdzielczosc (1.0 = 72 dpi; 2.5 = ~180 dpi)
MARGIN = 8  # padding wokol cropu


def extract_year(year: int, pdf_path: str) -> dict[int, str]:
    """Zwraca dict number -> sciezka do PNG."""
    doc = fitz.open(pdf_path)
    saved: dict[int, str] = {}

    # Najpierw zbierz wszystkie 'kotwice' (problem_no, page, y0, x0, x1)
    anchors: list[tuple[int, int, float, float, float]] = []

    for pi, page in enumerate(doc):
        page_h = page.rect.height
        page_w = page.rect.width
        blocks = page.get_text("blocks")
        for b in blocks:
            x0, y0, x1, y1, txt, *_ = b
            m = NUM_RE.match(txt)
            if not m:
                continue
            num = int(m.group(1))
            # filtr: tylko numery 1-24 w glownej kolumnie
            if not (1 <= num <= 24):
                continue
            anchors.append((num, pi, y0, x0, x1))

    if not anchors:
        return saved

    # Sortuj wedlug (page, y)
    anchors.sort(key=lambda a: (a[1], a[2]))

    # Deduplikuj: czasem ten sam numer pojawia sie wielokrotnie (np. obrazek z liczba)
    # Zatrzymaj pierwsze wystapienie kazdego numeru
    seen: set[int] = set()
    unique_anchors: list[tuple[int, int, float, float, float]] = []
    for a in anchors:
        if a[0] in seen:
            continue
        seen.add(a[0])
        unique_anchors.append(a)

    # Dla kazdej kotwicy znajdz koniec (start kolejnej kotwicy na tej samej stronie
    # ALBO koniec strony jezeli nastepna jest na innej stronie)
    for i, (num, pi, y0, x0, x1) in enumerate(unique_anchors):
        page = doc[pi]
        page_h = page.rect.height
        page_w = page.rect.width

        # Szukaj nastepnej kotwicy na tej samej stronie
        next_y = page_h
        for j in range(i + 1, len(unique_anchors)):
            n2, p2, y2, _, _ = unique_anchors[j]
            if p2 == pi:
                next_y = y2
                break
            elif p2 > pi:
                break

        # Crop rectangle: szeroka kolumna (od lewej do prawej krawedzi tekstu)
        # x0=45, x1=545 to typowe ramy strony
        crop_x0 = max(0, 35)
        crop_x1 = min(page_w, page_w - 25)
        crop_y0 = max(0, y0 - MARGIN)
        crop_y1 = min(page_h, next_y - 2)

        if crop_y1 - crop_y0 < 30:
            # za maly - pomin
            continue

        clip = fitz.Rect(crop_x0, crop_y0, crop_x1, crop_y1)
        mat = fitz.Matrix(ZOOM, ZOOM)
        pix = page.get_pixmap(matrix=mat, clip=clip, alpha=False)
        out_path = OUT_DIR / f"{year}-{num}.png"
        pix.save(out_path)
        saved[num] = f"/images/orig/{year}-{num}.png"

    doc.close()
    return saved


def extract_year_pages_fallback(year: int, pdf_path: str) -> dict[int, str]:
    """Fallback dla PDF-ow bez warstwy tekstu (skany): renderuj cale strony i przypisz
    je do zadan heurystycznie (6 zadan/strone, z pominieciem strony okladkowej jezeli to mozliwe).
    """
    doc = fitz.open(pdf_path)
    saved: dict[int, str] = {}
    # Render wszystkich stron jako PNG
    page_files: dict[int, str] = {}
    for pi, page in enumerate(doc):
        mat = fitz.Matrix(ZOOM, ZOOM)
        # Niektore skany maja zawartosc obrocona o 180 stopni
        # (np. 2025 - strony landscape sa do gory nogami)
        rotate = 0
        if year == 2025 and page.rect.width > page.rect.height:
            rotate = 180
        if rotate:
            mat = mat * fitz.Matrix(rotate)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        out_path = OUT_DIR / f"{year}-page{pi + 1}.png"
        pix.save(out_path)
        page_files[pi] = f"/images/orig/{year}-page{pi + 1}.png"

    n_pages = len(doc)
    # Heurystyka: pierwsza strona to okladka jezeli > 2 strony, inaczej zadania od pierwszej
    if n_pages >= 4:
        # zad 1-6 na page 1, 7-12 na page 2, 13-18 na page 3, 19-24 na page 4 (lub okladka jako page 0)
        # sprawdz: 2016/2025 maja 4 strony - prawdopodobnie wszystkie sa z zadaniami
        # dla bezpieczenstwa: kazda strona dostaje 6 kolejnych zadan, page index 0..3 -> 1-6,7-12,13-18,19-24
        for num in range(1, 25):
            page_idx = (num - 1) // 6
            if page_idx < n_pages:
                saved[num] = page_files[page_idx]
    else:
        # uproszczone
        per_page = max(1, 24 // n_pages)
        for num in range(1, 25):
            page_idx = min((num - 1) // per_page, n_pages - 1)
            saved[num] = page_files[page_idx]

    doc.close()
    return saved


def main():
    all_saved: dict[str, str] = {}  # problemId -> src
    for year, path in PDF_MAP.items():
        p = Path(path)
        if not p.exists():
            print(f"BRAK: {path}")
            continue
        saved = extract_year(year, str(p))
        if not saved:
            # PDF bez warstwy tekstu -> fallback z pelnymi stronami
            saved = extract_year_pages_fallback(year, str(p))
            print(f"{year}: {len(saved)} obrazow (fallback: pelne strony)")
        else:
            print(f"{year}: {len(saved)} obrazow")
        for num, src in saved.items():
            pid = f"kangur-maluch-{year}-{num}"
            all_saved[pid] = src

    # zapisz mape do pliku, potem inne skrypty moga ja uzyc
    with open("scripts/extracted_images.json", "w", encoding="utf-8") as f:
        json.dump(all_saved, f, ensure_ascii=False, indent=2)
    print(f"\nRAZEM: {len(all_saved)} obrazow zmapowanych do problemId")
    print(f"Pliki w public/images/orig/")
    print(f"Mapa: scripts/extracted_images.json")


if __name__ == "__main__":
    main()
