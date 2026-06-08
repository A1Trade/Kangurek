"""Aplikuje polski tekst (z PDF) do problemow w lekcjach.
Tylko dla kangur-maluch-* problemow gdzie mamy dane w polish_text.json."""
import json
import re
from pathlib import Path

with open("scripts/polish_text.json", encoding="utf-8") as f:
    POLISH = json.load(f)


def clean(text: str) -> str:
    # usun adresy stron i resztki
    text = re.sub(r"www\.kangur[-\w]*\.pl", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    # usun "Pytania po N punkty" jezeli wpadlo
    text = re.sub(r"\s*Pytania po \d+\s+punkt[yó]w?\s*", " ", text).strip()
    return text


DATA_DIR = Path("data/lessons")
modified = 0
stmts = 0
choices_n = 0
for i in range(1, 51):
    lid = f"l{i:02d}"
    path = DATA_DIR / f"{lid}.json"
    with open(path, encoding="utf-8") as f:
        d = json.load(f)

    for v in d["versions"]:
        for p in v["warmup"] + v["challenge"]:
            pid = p["id"]
            if pid in POLISH:
                pol = POLISH[pid]
                p["statement"] = clean(pol["statement"])
                # tylko nadpisz choices jezeli zawieraja polskie znaki (czyli sa lepsze)
                has_polish_choices = any(
                    any(c in v for c in "ąćęłńóśżźĄĆĘŁŃÓŚŻŹ")
                    for v in pol["choices"].values()
                )
                if has_polish_choices:
                    for k in "ABCDE":
                        if pol["choices"].get(k):
                            p["choices"][k] = clean(pol["choices"][k])
                            choices_n += 1
                stmts += 1

    with open(path, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    modified += 1

print(f"Zmodyfikowano {modified} plikow")
print(f"Zaktualizowano {stmts} statementow")
print(f"Zaktualizowano {choices_n} odpowiedzi (z polskimi znakami)")
