"""Dodaje wersje 2 (powtorka) do lekcji 9-13 (Blok B). Mix oryginalow + autorskich."""
import json

def load_original(year, number):
    with open(f"data/parsed/{year}.json", encoding="utf-8") as f:
        d = json.load(f)
    for p in d["problems"]:
        if p["number"] == number:
            return p
    raise ValueError(f"No {year}#{number}")

def gen(sfx, lesson, diff, subtopic, statement, choices, correct):
    return dict(id=f"gen-l{lesson}-v2-{sfx}", source=f"generated-l{lesson}-v2-{sfx}",
                year=None, number=None, difficulty=diff, topic="wzory_i_ciagi", subtopic=subtopic,
                statement=statement, hasImage=False, imageNote=None, choices=choices, correct=correct)

def sol(pid, obs, strat, steps, ans, alt=None):
    return dict(problemId=pid, observation=obs, strategy=strat, steps=steps, answer=ans, alternative=alt)

V2 = {}

# ===== L09 v2: Ciagi liczbowe =====
V2["l09"] = dict(versionId="v2", label="Wersja 2 (powtorka)",
    warmup=[
        gen("w1",9,"3pkt","ciag co 3",
            "Jaka liczba jest nastepna w ciagu: 3, 6, 9, 12, ?",
            {"A":"13","B":"14","C":"15","D":"16","E":"18"},"C"),
        gen("w2",9,"3pkt","ciag malejacy co 5",
            "Jaka liczba jest nastepna w ciagu malejacym: 50, 45, 40, 35, ?",
            {"A":"25","B":"28","C":"30","D":"32","E":"33"},"C"),
        gen("w3",9,"3pkt","ciag mnozony przez 3",
            "W ciagu 1, 3, 9, 27, ? kazda liczba to poprzednia razy 3. Jaka jest nastepna?",
            {"A":"54","B":"64","C":"72","D":"81","E":"90"},"D"),
        gen("w4",9,"3pkt","ciag co 3 od dwojki",
            "Jaka liczba jest nastepna: 2, 5, 8, 11, ?",
            {"A":"12","B":"13","C":"14","D":"15","E":"16"},"C"),
        load_original(2020,6),
    ],
    challenge=[
        gen("c1",9,"4pkt","ciag kwadratow",
            "W ciagu 1, 4, 9, 16, ? kazda liczba to kolejna liczba pomnozona przez sama siebie. Jaka jest nastepna?",
            {"A":"20","B":"24","C":"25","D":"30","E":"36"},"C"),
        gen("c2",9,"5pkt","ciag z rosnacymi roznicami",
            "W ciagu 3, 4, 6, 9, 13, 18, ? roznice rosna: 1, 2, 3, 4, 5. Jaka liczba jest nastepna?",
            {"A":"22","B":"23","C":"24","D":"25","E":"26"},"C"),
    ],
    solutions=[
        sol("gen-l9-v2-w1","Roznica stala 3.","Znajdz roznice.",["Roznica zawsze 3","12 + 3 = 15"],"C"),
        sol("gen-l9-v2-w2","Ciag maleje co 5.","Znajdz roznice.",["Kazda liczba o 5 mniejsza","35 - 5 = 30"],"C"),
        sol("gen-l9-v2-w3","Liczby szybko rosna - mnozenie.","Sprawdz mnozenie.",["Kazda liczba to poprzednia razy 3","27 razy 3 = 81"],"D"),
        sol("gen-l9-v2-w4","Roznica stala 3.","Znajdz roznice.",["Roznica zawsze 3","11 + 3 = 14"],"C"),
        sol("kangur-maluch-2020-6","Skok co 3 od liczby 1, ale tylko po dostepnych liczbach.",
            "Ciag 1, 4, 7, 10... i sprawdzanie dostepnosci.",
            ["Ciag co 3 od 1: 1, 4, 7, 10, 13, 16, 19, 22...","Sprawdzamy, ktore liczby sa narysowane","22 nie ma narysowanego, najwieksza osiagalna to 19"],"D"),
        sol("gen-l9-v2-c1","Liczby to kwadraty: 1x1, 2x2, 3x3, 4x4.","Rozpoznaj kwadraty.",
            ["1, 4, 9, 16 to 1x1, 2x2, 3x3, 4x4","Nastepna: 5x5 = 25"],"C"),
        sol("gen-l9-v2-c2","Roznice rosna o 1.","Roznice tworza wlasny ciag.",
            ["Roznice: 1, 2, 3, 4, 5","Nastepna roznica: 6","18 + 6 = 24"],"C"),
    ])

# ===== L10 v2: Wzory w obrazkach =====
V2["l10"] = dict(versionId="v2", label="Wersja 2 (powtorka)",
    warmup=[
        gen("w1",10,"3pkt","wzor domkow z patyczkow",
            "Z patyczkow uklada sie domki w rzedzie: 1 domek to 6 patyczkow, 2 domki to 11, 3 domki to 16. Ile patyczkow na 5 domkow?",
            {"A":"21","B":"24","C":"26","D":"30","E":"31"},"C"),
        gen("w2",10,"3pkt","wzor kropek w rzedach",
            "Wzor z kropek: rzad 1 ma 2 kropki, rzad 2 ma 4, rzad 3 ma 6. Ile kropek ma rzad 8?",
            {"A":"14","B":"16","C":"18","D":"12","E":"20"},"B"),
        gen("w3",10,"3pkt","suma poziomow wiezy",
            "Wieza z klockow: poziom 1 ma 2 klocki, poziom 2 ma 4, poziom 3 ma 6, poziom 4 ma 8. Ile klockow ma cala wieza 4-poziomowa?",
            {"A":"16","B":"18","C":"20","D":"24","E":"30"},"C"),
        gen("w4",10,"3pkt","wzor plotka z desek",
            "Plotek: 1 sekcja to 3 deski, 2 sekcje to 5, 3 sekcje to 7. Ile desek na 10 sekcji?",
            {"A":"19","B":"20","C":"21","D":"23","E":"30"},"C"),
        load_original(2020,8),
    ],
    challenge=[
        gen("c1",10,"4pkt","zapalki w siatce kwadratow",
            "Siatka kwadratow z zapalek: 1x1 to 4 zapalki, 2x2 to 12, 3x3 to 24. Ile zapalek na siatke 4x4?",
            {"A":"32","B":"36","C":"40","D":"44","E":"48"},"C"),
        gen("c2",10,"5pkt","suma poziomow choinki",
            "Choinka z klockow ma 6 poziomow: 1, 3, 5, 7, 9 i 11 klockow. Ile klockow ma cala choinka?",
            {"A":"30","B":"33","C":"36","D":"42","E":"49"},"C"),
    ],
    solutions=[
        sol("gen-l10-v2-w1","Pierwszy domek 6, kazdy kolejny +5.","Oddziel poczatek od przyrostu.",
            ["1 domek: 6 patyczkow","Kazdy kolejny dodaje 5","5 domkow: 6 + 5 razy 4 = 6 + 20 = 26"],"C"),
        sol("gen-l10-v2-w2","Liczby kropek: 2, 4, 6... rosna o 2.","Znajdz przyrost.",
            ["Rzad n ma 2 razy n kropek","Rzad 8: 2 razy 8 = 16"],"B"),
        sol("gen-l10-v2-w3","Poziomy 2, 4, 6, 8 - sumujemy.","Suma ciagu.",
            ["2 + 4 + 6 + 8 = 20"],"C"),
        sol("gen-l10-v2-w4","Pierwsza sekcja 3 deski, kazda kolejna +2.","Oddziel poczatek od przyrostu.",
            ["1 sekcja: 3 deski","Kazda kolejna dodaje 2","10 sekcji: 3 + 2 razy 9 = 3 + 18 = 21"],"C"),
        sol("kangur-maluch-2020-8","Plot z listew - liczymy strukture.",
            "Znajdz przyrost listew na metr.",
            ["Plot 4 m ma okreslona liczbe listew","Plot 8 m to dwa razy dluzszy odcinek","Po przeliczeniu struktury wychodzi 34 listwy"],"E",
            "Wymaga policzenia listew poziomych i pionowych w jednym metrze plotu."),
        sol("gen-l10-v2-c1","Liczby zapalek: 4, 12, 24 - rosna szybciej.","Znajdz wzor przyrostu.",
            ["Siatka N na N: zapalki = 2 razy N razy (N+1)","Sprawdz 3x3: 2 razy 3 razy 4 = 24 OK","4x4: 2 razy 4 razy 5 = 40"],"C"),
        sol("gen-l10-v2-c2","Sumujemy klocki ze wszystkich poziomow.","Suma ciagu nieparzystych.",
            ["1 + 3 + 5 + 7 + 9 + 11 = 36"],"C",
            "Suma pierwszych 6 liczb nieparzystych to 6 razy 6 = 36."),
    ])

# ===== L11 v2: Magiczne kwadraty =====
V2["l11"] = dict(versionId="v2", label="Wersja 2 (powtorka)",
    warmup=[
        gen("w1",11,"3pkt","brakujaca liczba w wierszu",
            "W magicznym kwadracie suma rzedu to 12. W jednym rzedzie sa juz liczby 7 i 2. Jaka jest trzecia liczba?",
            {"A":"2","B":"3","C":"4","D":"5","E":"6"},"B"),
        gen("w2",11,"3pkt","suma magiczna kwadratu 3x3",
            "Ile wynosi suma magiczna kwadratu 3x3 zbudowanego z liczb od 1 do 9?",
            {"A":"12","B":"13","C":"14","D":"15","E":"18"},"D"),
        gen("w3",11,"3pkt","brakujaca liczba na przekatnej",
            "W magicznym kwadracie suma magiczna to 15. Przekatna ma juz liczby 4 i 5. Jaka jest trzecia liczba?",
            {"A":"5","B":"6","C":"7","D":"8","E":"9"},"B"),
        gen("w4",11,"3pkt","brakujaca liczba w kolumnie",
            "W magicznym kwadracie suma kolumny to 21. W kolumnie sa juz 9 i 4. Jaka jest trzecia liczba?",
            {"A":"6","B":"7","C":"8","D":"9","E":"10"},"C"),
        load_original(2014,6),
    ],
    challenge=[
        load_original(2016,16),
        load_original(2015,20),
    ],
    solutions=[
        sol("gen-l11-v2-w1","Brakujaca = suma minus dwie znane.","Brakujaca liczba.",["12 - 7 - 2 = 3"],"B"),
        sol("gen-l11-v2-w2","Magiczny kwadrat 3x3 z 1-9 - suma kazdej linii.","Regula sumy magicznej.",
            ["Suma wszystkich liczb 1-9 = 45","Trzy rzedy daja te sama sume","45 : 3 = 15"],"D"),
        sol("gen-l11-v2-w3","Brakujaca = suma magiczna minus dwie znane.","Brakujaca liczba.",["15 - 4 - 5 = 6"],"B"),
        sol("gen-l11-v2-w4","Brakujaca = suma minus dwie znane.","Brakujaca liczba.",["21 - 9 - 4 = 8"],"C"),
        sol("kangur-maluch-2014-6","Iloczyn dwoch sasiednich liczb daje liczbe nad nimi.",
            "Wspinanie sie po piramidzie iloczynow.",
            ["Dolny rzad: 1, ?, ?, 1","Srodkowy rzad: 2, szare, 2 - kazda liczba to iloczyn dwoch pod nia","Szczyt 64 - iloczyn dwoch liczb srodkowego rzedu","Po wyliczeniu w szarym polu wychodzi 4"],"D"),
        sol("kangur-maluch-2016-16","Latinski kwadrat 3x3 z liczb 1, 2, 3.",
            "Kazda liczba raz w wierszu i kolumnie.",
            ["Pokazane: 1 w rogu, 2 w srodku","Uzupelniamy tak, by 1, 2, 3 byly raz w wierszu i kolumnie","Suma dwoch zacieniowanych pol wynosi 4"],"C"),
        sol("kangur-maluch-2015-20","Krzyz z 5 pol, suma kolumny = suma rzedu.",
            "Srodek jest wspolny dla rzedu i kolumny.",
            ["Suma liczb 2+3+5+6+7 = 23","Rzad + kolumna - srodek = 23, rzad = kolumna","Srodek musi byc nieparzysty: 3, 5 lub 7","W pole ? mozna wpisac 3, 5 lub 7"],"E"),
    ])

# ===== L12 v2: Rozkladanie =====
V2["l12"] = dict(versionId="v2", label="Wersja 2 (powtorka)",
    warmup=[
        gen("w1",12,"3pkt","rozklad na sume dwoch liczb",
            "Na ile sposobow mozna zapisac liczbe 6 jako sume dwoch liczb wiekszych od 0? (kolejnosc nie ma znaczenia)",
            {"A":"2","B":"3","C":"4","D":"5","E":"6"},"B"),
        gen("w2",12,"3pkt","rozklad na iloczyn",
            "Na ile sposobow mozna zapisac liczbe 18 jako iloczyn dwoch liczb?",
            {"A":"2","B":"3","C":"4","D":"5","E":"6"},"B"),
        gen("w3",12,"3pkt","rozmiana monet",
            "Na ile sposobow mozna ulozyc 8 zlotych z monet 5 zl i 1 zl?",
            {"A":"1","B":"2","C":"3","D":"4","E":"5"},"B"),
        gen("w4",12,"3pkt","suma trzech jednakowych",
            "Liczba 12 to suma trzech jednakowych liczb. Jaka to liczba?",
            {"A":"3","B":"4","C":"5","D":"6","E":"12"},"B"),
        load_original(2021,3),
    ],
    challenge=[
        load_original(2015,21),
        gen("c2",12,"5pkt","liczba dzielnikow",
            "Ile dzielnikow ma liczba 36 (liczb, przez ktore dzieli sie bez reszty)?",
            {"A":"6","B":"7","C":"8","D":"9","E":"12"},"D"),
    ],
    solutions=[
        sol("gen-l12-v2-w1","Wypisuje sumy systematycznie.","Systematyczne wypisywanie.",
            ["1 + 5 = 6","2 + 4 = 6","3 + 3 = 6","Czyli 3 sposoby"],"B"),
        sol("gen-l12-v2-w2","Szukam par dzielnikow 18.","Pary dzielnikow.",
            ["1 razy 18","2 razy 9","3 razy 6","Czyli 3 sposoby"],"B"),
        sol("gen-l12-v2-w3","Licze ile monet 5 zl: 0 lub 1.","Systematyczne wypisywanie.",
            ["0 monet 5zl + 8 monet 1zl","1 moneta 5zl + 3 monety 1zl","Czyli 2 sposoby"],"B"),
        sol("gen-l12-v2-w4","Trzy jednakowe liczby daja 12.","Dzielenie.",["12 : 3 = 4"],"B"),
        sol("kangur-maluch-2021-3","Elementy ukladanki tworza zapis dzialania.",
            "Odczytanie dzialania z ulozonego prostokata.",
            ["Cztery elementy ukladanki tworza dzialanie z cyframi 3, 2, 1 i znakiem +","Po poprawnym ulozeniu wynik dzialania wynosi 24"],"D"),
        sol("kangur-maluch-2015-21","Iloczyny numerow kul: Helenka 0, Agnieszka 72, Lusia 90.",
            "Helenka ma kule 0 (bo iloczyn 0). Rozklad pozostalych.",
            ["Helenka ma kule 0 - stad jej iloczyn 0","Agnieszka: 4 kule o iloczynie 72","Lusia: 3 kule o iloczynie 90","Po rozdzieleniu Helenka ma kule 0, 7 i 8","Suma: 0 + 7 + 8 = 15"],"E"),
        sol("gen-l12-v2-c2","Wypisuje dzielniki parami.","Pary dzielnikow.",
            ["1 i 36","2 i 18","3 i 12","4 i 9","6 i 6 (jeden dzielnik)","Dzielniki: 1,2,3,4,6,9,12,18,36 - razem 9"],"D"),
    ])

# ===== L13 v2: Znajdz regule =====
V2["l13"] = dict(versionId="v2", label="Wersja 2 (powtorka)",
    warmup=[
        gen("w1",13,"3pkt","regula maszyny - razy 2 plus 1",
            "Maszyna: 1 daje 3, 2 daje 5, 3 daje 7. Jaka liczbe da dla 6?",
            {"A":"11","B":"12","C":"13","D":"14","E":"15"},"C"),
        gen("w2",13,"3pkt","regula maszyny - dzielenie przez 2",
            "Maszyna: 10 daje 5, 20 daje 10, 30 daje 15. Jaka liczbe da dla 50?",
            {"A":"20","B":"25","C":"30","D":"35","E":"40"},"B"),
        gen("w3",13,"3pkt","wzor cykliczny 4-elementowy",
            "Figury powtarzaja sie: A, B, C, D, A, B, C, D... Ktora figura jest pietnasta w kolejnosci?",
            {"A":"A","B":"B","C":"C","D":"D","E":"E"},"C"),
        gen("w4",13,"3pkt","regula maszyny - razy 3",
            "Maszyna: 2 daje 6, 3 daje 9, 4 daje 12. Jaka liczbe da dla 7?",
            {"A":"14","B":"18","C":"21","D":"24","E":"28"},"C"),
        load_original(2023,3),
    ],
    challenge=[
        load_original(2021,17),
        load_original(2025,12),
    ],
    solutions=[
        sol("gen-l13-v2-w1","Porownuje wejscie z wyjsciem.","Testuj regule razy 2 plus 1.",
            ["1 razy 2 + 1 = 3 OK","2 razy 2 + 1 = 5 OK","Dla 6: 6 razy 2 + 1 = 13"],"C"),
        sol("gen-l13-v2-w2","Wyjscie to polowa wejscia.","Testuj regule dzielenia.",
            ["10 : 2 = 5, 20 : 2 = 10, 30 : 2 = 15","Dla 50: 50 : 2 = 25"],"B"),
        sol("gen-l13-v2-w3","Cykl ma 4 figury - uzyj reszty z dzielenia.","Wzor cykliczny.",
            ["Cykl: A(1), B(2), C(3), D(4)","15 : 4 = 3 reszta 3","Reszta 3 = trzecia w cyklu = C"],"C"),
        sol("gen-l13-v2-w4","Wyjscie to wejscie razy 3.","Testuj regule mnozenia.",
            ["2 razy 3 = 6, 3 razy 3 = 9, 4 razy 3 = 12","Dla 7: 7 razy 3 = 21"],"C"),
        sol("kangur-maluch-2023-3","Rownanie z monetami i znakami zapytania.",
            "Odejmij znane wartosci od obu stron.",
            ["20 + 10 + 10 + ? + ? + 1 = 50 + 1","Lewa bez znakow zapytania: 41","Prawa: 51","2 razy ? = 51 - 41 = 10, czyli ? = 5"],"C"),
        sol("kangur-maluch-2021-17","Diagram 3x3 ze strzalkami od liczby mniejszej do wiekszej.",
            "Strzalki pokazuja porzadek liczb.",
            ["Wpisane sa 5 i 7","Strzalki prowadza od mniejszej do wiekszej","Po analizie kierunkow strzalek w polu ? wychodzi 8"],"E"),
        sol("kangur-maluch-2025-12","Diagram kol - liczba w kolku dolnym to suma dwoch gornych.",
            "Sumowanie polaczonych kol.",
            ["Ala wpisala 6, pozostale liczby 1-5 i 7","Kazde dolne kolko = suma dwoch polaczonych gornych","Po wyliczeniu w kolku z gwiazdka wychodzi 5"],"D"),
    ])

for lid, version in V2.items():
    path = f"data/lessons/{lid}.json"
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    data["versions"] = [v for v in data["versions"] if v["versionId"] != "v2"]
    data["versions"].append(version)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"{lid}: v2 dodana ({len(version['warmup'])}+{len(version['challenge'])} zadan)")
print("DONE")
