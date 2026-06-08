"""Aplikuje sciezki imageSrc do wszystkich problemow w JSON lekcji.
Korzysta z mapy wygenerowanej przez extract_problem_images.py.
"""
import json
from pathlib import Path

with open("scripts/extracted_images.json", encoding="utf-8") as f:
    IMG_MAP = json.load(f)

DATA_DIR = Path("data/lessons")
modified = 0
imgs_applied = 0
no_image_for_problem = 0

for i in range(1, 51):
    lid = f"l{i:02d}"
    path = DATA_DIR / f"{lid}.json"
    with open(path, encoding="utf-8") as f:
        d = json.load(f)

    for v in d["versions"]:
        for p in v["warmup"] + v["challenge"]:
            pid = p["id"]
            if pid in IMG_MAP:
                p["imageSrc"] = IMG_MAP[pid]
                imgs_applied += 1
            else:
                # zachowaj null jezeli nie istnieje
                if "imageSrc" not in p:
                    p["imageSrc"] = None
                if p.get("hasImage"):
                    no_image_for_problem += 1

    with open(path, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    modified += 1

print(f"Zmodyfikowano {modified} lekcji")
print(f"Zaaplikowano imageSrc: {imgs_applied}")
print(f"Zadan z hasImage bez obrazu: {no_image_for_problem}")
