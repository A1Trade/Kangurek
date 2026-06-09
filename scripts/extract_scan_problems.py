"""Ekstrakcja pojedynczych zadan z skanowanych PDF-ow (2016, 2025) - tych ktore nie maja
warstwy tekstu. Wykonuje:
1. Render strony do PNG (z odpowiednia rotacja dla landscape 2025)
2. OCR (RapidOCR) -> pozycje numerow zadan
3. Crop fragmentow miedzy kolejnymi numerami
4. Zapis do public/images/orig/{year}-{N}.png
"""
import re
import os
os.environ.setdefault("OMP_NUM_THREADS", "2")

import fitz
from rapidocr_onnxruntime import RapidOCR
from pathlib import Path
import json

NUM_RE = re.compile(r"^\s*(\d{1,2})\.\s")
ZOOM = 2.5
OUT_DIR = Path("public/images/orig")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Konfiguracja per PDF: czy rotowac landscape pages
SCAN_PDFS = {
    2016: {"path": "data/arkusze/m_2016.pdf", "rotate_landscape": 0},
    2025: {"path": "data/arkusze/M-2025-PL.pdf", "rotate_landscape": 270},
}

# Spodziewane numery zadan na kazdej stronie (po renderowaniu)
# Format: year -> {page_idx: [list of expected nums]}
EXPECTED = {
    2016: {0: [1, 2, 3, 4, 5], 1: [6, 7, 8, 9, 10, 11, 12, 13],
           2: [14, 15, 16, 17, 18, 19, 20], 3: [21, 22, 23, 24]},
    2025: {0: [1, 2, 3, 4, 5], 1: [6, 7, 8, 9, 10, 11, 12],
           2: [13, 14, 15, 16, 17, 18], 3: [19, 20, 21, 22, 23, 24]},
}


def fill_missing_anchors(found: list[tuple[int, int, int]], expected: list[int], page_h: int):
    """Interpoluje pozycje brakujacych numerow miedzy znalezionymi sasiadami."""
    if not found:
        return found
    found_by_num = {n: (y, x) for n, y, x in found}
    result: list[tuple[int, int, int]] = []
    for num in expected:
        if num in found_by_num:
            y, x = found_by_num[num]
            result.append((num, y, x))
            continue
        # interpoluj
        # znajdz najblizsze ZNALEZIONE numery przed i po
        prev_n = max((n for n in found_by_num if n < num), default=None)
        next_n = min((n for n in found_by_num if n > num), default=None)
        if prev_n is None and next_n is None:
            continue
        if prev_n is None:
            # extrapolate from next
            y_next, _ = found_by_num[next_n]
            # zalozmy ze pierwsze zadanie jest na page start (y=50)
            est_y = max(50, y_next - (next_n - num) * 300)
        elif next_n is None:
            y_prev, _ = found_by_num[prev_n]
            est_y = min(page_h - 100, y_prev + (num - prev_n) * 300)
        else:
            y_prev, _ = found_by_num[prev_n]
            y_next, _ = found_by_num[next_n]
            ratio = (num - prev_n) / (next_n - prev_n)
            est_y = int(y_prev + ratio * (y_next - y_prev))
        result.append((num, int(est_y), 0))
    return result

ocr = RapidOCR()


def render_page(page, rotate_deg: int):
    mat = fitz.Matrix(ZOOM, ZOOM)
    if rotate_deg:
        mat = mat * fitz.Matrix(rotate_deg)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    # zwroc bytes + wymiary
    return pix.tobytes("png"), pix.width, pix.height


def find_problem_anchors(img_path: str) -> list[tuple[int, int]]:
    """Zwraca liste (num, y_top) dla problemow znalezionych przez OCR."""
    result, _ = ocr(img_path)
    if not result:
        return []
    anchors: list[tuple[int, int]] = []
    for line in result:
        bbox, text, conf = line
        m = NUM_RE.match(text)
        if not m:
            continue
        num = int(m.group(1))
        if not (1 <= num <= 24):
            continue
        if conf < 0.5:
            continue
        # bbox = [[x,y]*4]; y_top = min y
        y_top = min(int(p[1]) for p in bbox)
        x_left = min(int(p[0]) for p in bbox)
        anchors.append((num, y_top, x_left))
    # dedupe: pierwsze wystapienie w kolejnosci rosnacej numerow
    anchors.sort(key=lambda a: a[1])  # sortuj po y
    # Wez pierwsze wystapienie kazdego numeru
    seen: set[int] = set()
    cleaned: list[tuple[int, int, int]] = []
    for num, y, x in anchors:
        if num in seen:
            continue
        seen.add(num)
        cleaned.append((num, y, x))
    return cleaned


def process(year: int, config: dict) -> dict[int, str]:
    pdf_path = config["path"]
    rotate_land = config["rotate_landscape"]
    doc = fitz.open(pdf_path)
    saved: dict[int, str] = {}

    # Render kazdej strony jako tymczasowy PNG, potem OCR
    for pi, page in enumerate(doc):
        is_land = page.rect.width > page.rect.height
        rotate = rotate_land if is_land else 0
        tmp_png = f"/tmp/{year}-p{pi}.png"
        # render
        mat = fitz.Matrix(ZOOM, ZOOM)
        if rotate:
            mat = mat * fitz.Matrix(rotate)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        pix.save(tmp_png)
        page_w, page_h = pix.width, pix.height

        anchors = find_problem_anchors(tmp_png)
        if not anchors:
            print(f"  {year} page {pi}: 0 anchors")
            continue

        # Sortuj po y - kolejnosc czytania
        anchors.sort(key=lambda a: a[1])
        # Interpolacja brakujacych numerow
        expected = EXPECTED.get(year, {}).get(pi, [])
        if expected:
            anchors = fill_missing_anchors(anchors, expected, page_h)
            anchors.sort(key=lambda a: a[1])
        print(f"  {year} page {pi}: numery {[a[0] for a in anchors]}")

        # Crop pomiedzy kolejnymi
        for i, (num, y, x) in enumerate(anchors):
            y_end = anchors[i + 1][1] if i + 1 < len(anchors) else page_h
            # padding gory: 10px, dolu: 5px
            crop_y0 = max(0, y - 10)
            crop_y1 = min(page_h, y_end - 5)
            crop_x0 = 0
            crop_x1 = page_w

            if crop_y1 - crop_y0 < 50:
                continue

            # Renderuj wycinek jako nowy pixmap (musimy ponownie z PDF, bo pixmap juz mamy)
            pix2 = page.get_pixmap(
                matrix=mat,
                clip=None,
                alpha=False,
            )
            # Lepiej: uzyj PIL/pixmap do wyciecia z istniejacego pix
            from PIL import Image
            img = Image.open(tmp_png)
            cropped = img.crop((crop_x0, crop_y0, crop_x1, crop_y1))
            out_path = OUT_DIR / f"{year}-{num}.png"
            cropped.save(out_path)
            saved[num] = f"/images/orig/{year}-{num}.png"

        # usun tymczasowy
        try:
            os.remove(tmp_png)
        except OSError:
            pass

    doc.close()
    return saved


def main():
    all_saved: dict[str, str] = {}
    for year, cfg in SCAN_PDFS.items():
        print(f"\n=== {year} ===")
        saved = process(year, cfg)
        for num, src in saved.items():
            pid = f"kangur-maluch-{year}-{num}"
            all_saved[pid] = src
        print(f"  saved: {len(saved)} obrazow")

    # zaktualizuj map - dodaj do istniejacej
    map_path = Path("scripts/extracted_images.json")
    if map_path.exists():
        with open(map_path, encoding="utf-8") as f:
            existing = json.load(f)
    else:
        existing = {}

    # Usun stare wpisy 2016-page* / 2025-page* (fallbacks)
    cleaned = {
        k: v for k, v in existing.items()
        if not (("/2016-page" in v) or ("/2025-page" in v))
    }
    cleaned.update(all_saved)

    with open(map_path, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=2)
    print(f"\nMapa zaktualizowana: {len(all_saved)} nowych, lacznie {len(cleaned)}")


if __name__ == "__main__":
    main()
