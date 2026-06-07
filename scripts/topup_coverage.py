"""Topup coverage - dodaje v3 do lekcji absorbujac wszystkie nieuzyte oryginaly.
Cel: 312/312 originalow w kursie."""
import json

def load_orig(year, number):
    with open(f"data/parsed/{year}.json", encoding="utf-8") as f:
        d = json.load(f)
    for p in d["problems"]:
        if p["number"] == number:
            return p
    raise ValueError(f"No {year}#{number}")

def osol(p, summary):
    return dict(problemId=p["id"], observation="Oryginalne zadanie Kangurka.",
                strategy=summary, steps=[summary, "Poprawna odpowiedz: "+p["correct"]],
                answer=p["correct"], alternative=None)

# Mapowanie: lekcja -> lista oryginalow do v3
# Wszystkie ~66 nieuzytych originalow rozdzielonych po lekcjach
V3 = {
    # Blok A - arytmetyka + lamiglowki
    "l01": [(2020,1)],
    "l02": [(2020,12), (2022,14), (2023,20)],
    "l03": [(2020,16), (2024,5)],
    "l04": [(2024,12), (2025,10)],
    "l05": [(2016,17), (2016,18)],
    "l06": [(2019,11), (2021,12), (2023,11), (2023,22)],
    "l07": [(2012,13), (2021,6), (2021,18), (2024,2)],
    "l08": [(2013,2), (2016,20), (2019,12), (2020,23),
            (2021,20), (2021,24), (2023,13), (2023,23),
            (2024,15), (2024,16), (2024,18), (2024,20)],
    # Blok C - geometria
    "l14": [(2016,15)],
    "l15": [(2025,3)],
    "l16": [(2020,14)],
    "l17": [(2025,13)],
    "l18": [(2022,18)],
    "l19": [(2023,17)],
    "l20": [(2016,6)],
    "l21": [(2023,21)],
    # Blok G - logika
    "l36": [(2019,17), (2019,21), (2020,10), (2021,23), (2022,10)],
    "l37": [(2019,23), (2020,21), (2020,24), (2022,20)],
    "l38": [(2021,14), (2023,16), (2023,19), (2023,24), (2015,24)],
    "l39": [(2016,5), (2016,19), (2022,7), (2022,2), (2021,19), (2023,1)],
    "l40": [(2016,22), (2018,24), (2023,12)],
    "l41": [(2016,8), (2021,2), (2022,9), (2023,14)],
    # Blok H - kombinatoryka
    "l42": [(2024,13)],
}

added_count = 0
total_originals = 0
for lid, orig_list in V3.items():
    path = f"data/lessons/{lid}.json"
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    # Usuwa istniejace v3 jezeli istnieje
    data["versions"] = [v for v in data["versions"] if v["versionId"] != "v3"]
    # Tworz v3 - wszystkie problemy jako warmup, brak challenge
    problems = [load_orig(y, n) for y, n in orig_list]
    solutions = [osol(p, f"Oryginalne zadanie Kangur Maluch {p['year']} nr {p['number']}.") for p in problems]
    v3 = dict(
        versionId="v3",
        label=f"Wersja 3 (oryginaly Kangurka)",
        warmup=problems,
        challenge=[],
        solutions=solutions
    )
    data["versions"].append(v3)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    added_count += 1
    total_originals += len(problems)
    print(f"{lid}: v3 dodana ({len(problems)} oryginalow)")

print(f"\nDODANO v3 do {added_count} lekcji, lacznie {total_originals} oryginalow")
