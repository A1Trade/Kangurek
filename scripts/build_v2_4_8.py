"""Dodaje wersje 2 (powtorka) do lekcji 4-8. Mix oryginalow + autorskich."""
import json

def load_original(year, number):
    with open(f"data/parsed/{year}.json", encoding="utf-8") as f:
        d = json.load(f)
    for p in d["problems"]:
        if p["number"] == number:
            return p
    raise ValueError(f"No problem {year}#{number}")

def gen(sfx, lesson, diff, topic, subtopic, statement, choices, correct):
    return dict(id=f"gen-l{lesson:02d}-v2-{sfx}", source=f"generated-l{lesson:02d}-v2-{sfx}",
                year=None, number=None, difficulty=diff, topic=topic, subtopic=subtopic,
                statement=statement, hasImage=False, imageNote=None, choices=choices, correct=correct)

def sol(pid, obs, strat, steps, ans, alt=None):
    return dict(problemId=pid, observation=obs, strategy=strat, steps=steps, answer=ans, alternative=alt)

V2 = {}

# ===== L04 v2: Kolejnosc dzialan =====
V2["l04"] = dict(versionId="v2", label="Wersja 2 (powtorka)",
    warmup=[
        gen("w1",4,"3pkt","arytmetyka","mnozenie przed odejmowaniem",
            "Ile to 10 - 2 razy 3?", {"A":"4","B":"24","C":"6","D":"14","E":"18"}, "A"),
        gen("w2",4,"3pkt","arytmetyka","nawias zmienia kolejnosc",
            "Ile to (10 - 2) razy 3?", {"A":"4","B":"24","C":"30","D":"36","E":"16"}, "B"),
        gen("w3",4,"3pkt","arytmetyka","mnozenie przed dodawaniem",
            "Ile to 4 + 5 razy 2?", {"A":"18","B":"14","C":"20","D":"13","E":"9"}, "B"),
        gen("w4",4,"3pkt","arytmetyka","dzielenie przed odejmowaniem",
            "Ile to 20 - 12 : 4?", {"A":"2","B":"8","C":"17","D":"11","E":"14"}, "C"),
        load_original(2018,7),
    ],
    challenge=[
        gen("c1",4,"4pkt","arytmetyka","wstawianie nawiasu",
            "Gdzie wstawic nawias w dzialaniu 12 - 4 - 2, by wynik byl rowny 10?",
            {"A":"(12 - 4) - 2","B":"12 - (4 - 2)","C":"Bez nawiasu juz jest 10","D":"Nie da sie","E":"12 - 4 - (2)"}, "B"),
        load_original(2022,21),
    ],
    solutions=[
        sol("gen-l04-v2-w1","Mnozenie przed odejmowaniem.","Kolejnosc dzialan.",
            ["2 razy 3 = 6","10 - 6 = 4"],"A"),
        sol("gen-l04-v2-w2","Nawias najpierw.","Nawias przed mnozeniem.",
            ["10 - 2 = 8","8 razy 3 = 24"],"B"),
        sol("gen-l04-v2-w3","Mnozenie przed dodawaniem.","Kolejnosc dzialan.",
            ["5 razy 2 = 10","4 + 10 = 14"],"B"),
        sol("gen-l04-v2-w4","Dzielenie przed odejmowaniem.","Kolejnosc dzialan.",
            ["12 : 4 = 3","20 - 3 = 17"],"C"),
        sol("kangur-maluch-2018-7","Trzy proby po 3 strzaly, znane sumy 27 i 23.",
            "Analiza punktow na tarczy.",
            ["Tarcza ma pierscienie o roznych wartosciach","Z ukladu strzal w probie 3 suma wynosi 19"],"B",
            "Wymaga odczytania wartosci trafien z rysunku."),
        sol("gen-l04-v2-c1","Cel: wynik 10. Sprawdz polozenia nawiasu.","Sprawdzanie.",
            ["Bez nawiasu: 12 - 4 - 2 = 6","(12-4)-2 = 8 - 2 = 6","12-(4-2) = 12 - 2 = 10 - TAK"],"B",
            "Nawias dookola odejmowania zmienia znak."),
        sol("kangur-maluch-2022-21","Uklad zaleznosci miedzy dziecmi.","Wyrazic wszystko przez Magde.",
            ["Magda = m","Kinga = m + 2","Emilka = Kinga - 3 = m - 1","Jola = Emilka + 1 = m","Wladek = Jola + 3 = m + 3","Magda = m, Jola = m - rowne!"],"E"),
    ])

# ===== L05 v2: Parzyste/nieparzyste =====
V2["l05"] = dict(versionId="v2", label="Wersja 2 (powtorka)",
    warmup=[
        gen("w1",5,"3pkt","arytmetyka","rozpoznanie nieparzystej",
            "Ktora z liczb jest nieparzysta: 4, 8, 15, 22, 30?",
            {"A":"4","B":"8","C":"15","D":"22","E":"30"}, "C"),
        gen("w2",5,"3pkt","arytmetyka","nieparzysta + nieparzysta",
            "Suma dwoch liczb nieparzystych jest zawsze:",
            {"A":"Parzysta","B":"Nieparzysta","C":"Raz tak raz tak","D":"Zerem","E":"Liczba 1"}, "A"),
        gen("w3",5,"3pkt","arytmetyka","parzysta razy nieparzysta",
            "Iloczyn liczby parzystej i nieparzystej jest zawsze:",
            {"A":"Parzysty","B":"Nieparzysty","C":"Raz tak raz tak","D":"Zerem","E":"Suma"}, "A"),
        gen("w4",5,"3pkt","arytmetyka","liczenie nieparzystych w zakresie",
            "Ile nieparzystych liczb jest od 1 do 30?",
            {"A":"10","B":"15","C":"14","D":"30","E":"20"}, "B"),
        gen("w5",5,"3pkt","arytmetyka","suma trzech parzystych",
            "Suma trzech liczb parzystych jest zawsze:",
            {"A":"Parzysta","B":"Nieparzysta","C":"Raz tak raz tak","D":"Zerem","E":"Liczba 3"}, "A"),
    ],
    challenge=[
        gen("c1",5,"4pkt","arytmetyka","parzystosc sumy ciagu",
            "Czy suma wszystkich liczb od 1 do 10 (1+2+3+...+10) jest parzysta?",
            {"A":"Parzysta, wynik 55","B":"Nieparzysta, wynik 55","C":"Parzysta, wynik 50","D":"Nieparzysta, wynik 45","E":"Parzysta, wynik 56"}, "B"),
        load_original(2022,15),
    ],
    solutions=[
        sol("gen-l05-v2-w1","Nieparzysta konczy sie na 1,3,5,7,9.","Sprawdz ostatnia cyfre.",
            ["15 konczy sie na 5 - nieparzysta","Pozostale (4,8,22,30) parzyste"],"C"),
        sol("gen-l05-v2-w2","Nieparzysta + nieparzysta = parzysta.","Wzor parzystosci.",
            ["3 + 5 = 8 (parzysta)","7 + 9 = 16 (parzysta)","Zawsze parzysta"],"A"),
        sol("gen-l05-v2-w3","Parzysta razy cokolwiek = parzysta.","Wzor mnozenia.",
            ["2 razy 3 = 6 (parzysty)","4 razy 7 = 28 (parzysty)","Zawsze parzysty"],"A"),
        sol("gen-l05-v2-w4","Co druga liczba jest nieparzysta.","Polowa zakresu.",
            ["Nieparzyste: 1,3,5,...,29","Razem 15 sztuk"],"B"),
        sol("gen-l05-v2-w5","Parzysta + parzysta + parzysta = parzysta.","Wzor.",
            ["2 + 4 + 6 = 12 (parzysta)","Suma parzystych zawsze parzysta"],"A"),
        sol("gen-l05-v2-c1","Suma 1+2+...+10. Policz ja sprytnie.","Pary do 11.",
            ["Pary: 1+10, 2+9, 3+8, 4+7, 5+6 - kazda po 11","5 par razy 11 = 55","55 konczy sie na 5 - nieparzysta"],"B",
            "Mozna tez liczyc po kolei: 55."),
        sol("kangur-maluch-2022-15","3 druzyny, kazda gra 2 mecze. Jakiej sumy nie da sie zdobyc?",
            "Wypisanie mozliwych sum punktow.",
            ["Mozliwe wyniki 2 meczow: 2W=6, 1W1R=4, 1W1P=3, 2R=2, 1R1P=1, 2P=0","Mozliwe sumy: 0,1,2,3,4,6","Brakuje: 5"],"D"),
    ])

# ===== L06 v2: Sprytne liczenie =====
V2["l06"] = dict(versionId="v2", label="Wersja 2 (powtorka)",
    warmup=[
        gen("w1",6,"3pkt","arytmetyka","pary do 100",
            "Ile to 23 + 19 + 27 + 31?",
            {"A":"90","B":"95","C":"100","D":"105","E":"110"}, "C"),
        gen("w2",6,"3pkt","arytmetyka","rozdzielnosc mnozenia",
            "Ile to 50 razy 7 + 50 razy 3?",
            {"A":"350","B":"500","C":"450","D":"550","E":"600"}, "B"),
        gen("w3",6,"3pkt","arytmetyka","grupowanie czynnikow",
            "Ile to 4 razy 17 razy 25?",
            {"A":"1700","B":"680","C":"1600","D":"425","E":"170"}, "A"),
        gen("w4",6,"3pkt","arytmetyka","odwracanie operacji",
            "Mysle liczbe, mnoze przez 4, odejmuje 3, wynik to 25. Jaka liczba?",
            {"A":"5","B":"6","C":"7","D":"8","E":"28"}, "C"),
        load_original(2018,3),
    ],
    challenge=[
        load_original(2012,20),
        gen("c2",6,"5pkt","arytmetyka","dluga sekwencja operacji",
            "Mysle liczbe. Odejmuje 8, mnoze przez 3, dodaje 10. Wynik to 31. Jaka jest moja liczba?",
            {"A":"13","B":"15","C":"17","D":"11","E":"21"}, "B"),
    ],
    solutions=[
        sol("gen-l06-v2-w1","Szukam par do 100.","Lacznosc.",
            ["23 + 27 = 50","19 + 31 = 50","50 + 50 = 100"],"C"),
        sol("gen-l06-v2-w2","Rozdzielnosc: 50*(7+3).","Rozdzielnosc mnozenia.",
            ["50 razy 7 + 50 razy 3 = 50 razy 10 = 500"],"B"),
        sol("gen-l06-v2-w3","Szukam okraglego produktu: 4 razy 25 = 100.","Grupowanie czynnikow.",
            ["4 razy 25 = 100","100 razy 17 = 1700"],"A"),
        sol("gen-l06-v2-w4","Odwracam operacje od wyniku.","Krok po kroku wstecz.",
            ["Wynik 25, ostatnio odjeto 3: 25 + 3 = 28","Przedtem mnozono przez 4: 28 : 4 = 7"],"C"),
        sol("kangur-maluch-2018-3","Hela 6, siostra o 2 mlodsza, brat o 2 starszy.",
            "Liczenie wieku kazdego.",
            ["Hela = 6","Siostra = 6 - 2 = 4","Brat = 6 + 2 = 8","Suma: 6 + 4 + 8 = 18"],"C"),
        sol("kangur-maluch-2012-20","Owoce w proporcjach: sliwki najwiecej.",
            "Wyrazic wszystko przez liczbe sliwek.",
            ["Mandarynki = sliwki : 7","Jablka = mandarynki : 5","Gruszki = jablka : 3","Suma musi byc 496, liczba sliwek dzielna przez 105","Sprawdz 420: 420 + 60 + 12 + 4 = 496 - pasuje","Sliwek bylo 420"],"E"),
        sol("gen-l06-v2-c2","Trzy operacje - odwracam od wyniku.","Krok po kroku wstecz.",
            ["Wynik 31, ostatnio dodano 10: 31 - 10 = 21","Przedtem mnozono przez 3: 21 : 3 = 7","Przedtem odjeto 8: 7 + 8 = 15"],"B"),
    ])

# ===== L07 v2: Zaokraglanie =====
V2["l07"] = dict(versionId="v2", label="Wersja 2 (powtorka)",
    warmup=[
        gen("w1",7,"3pkt","arytmetyka","zaokraglanie do dziesiatek",
            "Liczba 73 zaokraglona do dziesiatek to:",
            {"A":"70","B":"80","C":"73","D":"75","E":"60"}, "A"),
        gen("w2",7,"3pkt","arytmetyka","zaokraglanie do setek",
            "Liczba 651 zaokraglona do setek to:",
            {"A":"600","B":"650","C":"700","D":"660","E":"651"}, "C"),
        gen("w3",7,"3pkt","arytmetyka","szacowanie sumy",
            "Najlepsze oszacowanie 312 + 589 to:",
            {"A":"800","B":"900","C":"1000","D":"700","E":"850"}, "B"),
        gen("w4",7,"3pkt","arytmetyka","ostatnia cyfra iloczynu",
            "Jaka jest ostatnia cyfra liczby 23 razy 4?",
            {"A":"0","B":"2","C":"8","D":"6","E":"4"}, "B"),
        load_original(2022,6),
    ],
    challenge=[
        gen("c1",7,"4pkt","arytmetyka","eliminacja przez ostatnia cyfre",
            "Filip obliczyl 48 razy 7. Wie, ze 48 to okolo 50, wiec wynik to okolo 350. Ktora odpowiedz jest poprawna?",
            {"A":"296","B":"316","C":"336","D":"376","E":"406"}, "C"),
        load_original(2018,17),
    ],
    solutions=[
        sol("gen-l07-v2-w1","Cyfra jednosci 3 (<5) - w dol.","Zaokraglanie do dziesiatek.",
            ["Cyfra jednosci to 3 (<5)","Zaokraglamy w dol: 73 -> 70"],"A"),
        sol("gen-l07-v2-w2","Cyfra dziesiatek 5 (>=5) - w gore.","Zaokraglanie do setek.",
            ["Cyfra dziesiatek to 5 (>=5)","Zaokraglamy w gore: 651 -> 700"],"C"),
        sol("gen-l07-v2-w3","Zaokraglij oba skladniki.","Szacowanie.",
            ["312 ~ 300","589 ~ 600","Suma ~ 900"],"B",
            "Dokladnie 312+589=901 - blisko 900."),
        sol("gen-l07-v2-w4","Ostatnia cyfra zalezy tylko od cyfr jednosci.","Patrz ostatnia cyfre.",
            ["Ostatnia cyfra 23 to 3","3 razy 4 = 12, ostatnia cyfra 2"],"B",
            "Dokladnie 23 razy 4 = 92."),
        sol("kangur-maluch-2022-6","Zestaw 3 skokow: 2m + 1m + 1m = 4m.",
            "Liczba zestawow i skokow.",
            ["Jeden zestaw = 2 + 1 + 1 = 4 m, 3 skoki","16 m : 4 m = 4 zestawy","4 zestawy razy 3 skoki = 12 skokow"],"E"),
        sol("gen-l07-v2-c1","48 razy 7 ~ 50 razy 7 = 350. Szukaj odpowiedzi blisko 350.",
            "Szacowanie + eliminacja.",
            ["48 ~ 50, czyli wynik okolo 350","Odpowiedzi: 296, 316, 336, 376, 406","Najblizej 350: 336 lub 376","Dokladnie: 48 razy 7 = 336"],"C",
            "8 razy 7 = 56, ostatnia cyfra 6 - pasuje do 336."),
        sol("kangur-maluch-2018-17","Po 3 skokach przod 1 skok tyl, kazdy skok 2m.",
            "Liczenie postepu na zestaw skokow.",
            ["14 skokow = 3 grupy po 4 skoki (3 przod + 1 tyl) + 2 dodatkowe przod","Kazda grupa: 3 przod - 1 tyl = 2 skoki postepu = 4 m","3 grupy razy 4 m = 12 m","2 dodatkowe skoki przod razy 2 m = 4 m","Razem 12 + 4 = 16 m"],"B"),
    ])

# ===== L08 v2: Lamiglowki =====
V2["l08"] = dict(versionId="v2", label="Wersja 2 (powtorka)",
    warmup=[
        gen("w1",8,"3pkt","lamiglowki","brakujacy skladnik",
            "W dzialaniu A + 7 = 16 jaka cyfra to A?",
            {"A":"7","B":"8","C":"9","D":"6","E":"23"}, "C"),
        gen("w2",8,"3pkt","lamiglowki","brakujacy czynnik",
            "W dzialaniu 3 razy B = 21 jaka liczba to B?",
            {"A":"6","B":"7","C":"8","D":"3","E":"18"}, "B"),
        gen("w3",8,"3pkt","lamiglowki","wstawianie znakow",
            "Wstaw znaki + lub - miedzy liczby 5 _ 5 _ 5, by otrzymac 15. Ktory zestaw dziala?",
            {"A":"5 + 5 + 5","B":"5 + 5 - 5","C":"5 - 5 - 5","D":"5 - 5 + 5","E":"Nie da sie"}, "A"),
        load_original(2012,14),
        load_original(2012,6),
    ],
    challenge=[
        load_original(2025,23),
        load_original(2018,19),
    ],
    solutions=[
        sol("gen-l08-v2-w1","A + 7 = 16, czyli A = 16 - 7.","Odwrocenie dodawania.",
            ["A = 16 - 7 = 9"],"C"),
        sol("gen-l08-v2-w2","3 razy B = 21, czyli B = 21 : 3.","Odwrocenie mnozenia.",
            ["B = 21 : 3 = 7"],"B"),
        sol("gen-l08-v2-w3","Cel: 15. Sprawdz zestawy znakow.","Sprawdzanie.",
            ["5 + 5 + 5 = 15 - TAK","5 + 5 - 5 = 5, nie","Pozostale daja 5 lub mniej"],"A"),
        sol("kangur-maluch-2012-14","Waz z 7 kamieni domino, lacznie 33 oczka, 2 kamienie zabrane.",
            "Sasiednie pola maja po tyle samo oczek.",
            ["Sasiadujace pola domina maja rowne oczka","Z lacznej sumy 33 i widocznych kamieni","Po analizie na polu ? jest 4 oczka"],"C",
            "Wymaga sledzenia regul ukladania domina."),
        sol("kangur-maluch-2012-6","Dwie tarcze rzutek, kazdy gracz 3 strzaly.",
            "Sumowanie trafien.",
            ["Sumujemy 3 trafienia Michala i 3 trafienia Kuby","Michal ma wieksza sume o 2 punkty"],"C",
            "Wymaga odczytania wartosci trafien z rysunku."),
        sol("kangur-maluch-2025-23","12 kol z liczbami 1-12, rowne sumy na prostych.",
            "Uklad rownan z czesciowo wypelnionych kol.",
            ["Suma wszystkich liczb 1-12 = 78","Z warunkow rownych sum na prostych liniach","Po wyliczeniu w miejscu ? wpada liczba 5"],"C",
            "Wymaga sledzenia kazdej prostej linii diagramu."),
        sol("kangur-maluch-2018-19","Liczba dwucyfrowa: +11 daje trzycyfrowa, -11 daje iloczyn rownych cyfr.",
            "Sprawdzanie warunkow.",
            ["+11 trzycyfrowa: liczba >= 89","-11 iloczyn rownych jednocyfrowych: wynik z {1,4,9,16,25,36,49,64,81}","Liczba - 11 >= 78, wiec wynik = 81","Liczba = 81 + 11 = 92"],"E"),
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
