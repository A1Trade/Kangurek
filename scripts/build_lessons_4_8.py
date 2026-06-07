"""Generuje lekcje 4-8 jako pliki l04.json - l08.json.
Kazda lekcja: theory + 1 wersja z mixem oryginalow Kangurka + zadania autorskie + quiz."""
import json, os

def load_original(year, number):
    with open(f"data/parsed/{year}.json", encoding="utf-8") as f:
        d = json.load(f)
    for p in d["problems"]:
        if p["number"] == number:
            return p
    raise ValueError(f"No problem {year}#{number}")

def gen(id_suffix, lesson, difficulty, topic, subtopic, statement, choices, correct):
    return dict(
        id=f"gen-l{lesson:02d}-{id_suffix}", source=f"generated-l{lesson:02d}-{id_suffix}",
        year=None, number=None,
        difficulty=difficulty, topic=topic, subtopic=subtopic,
        statement=statement, hasImage=False, imageNote=None,
        choices=choices, correct=correct,
    )

def sol(problem_id, observation, strategy, steps, answer, alternative=None):
    return dict(problemId=problem_id, observation=observation, strategy=strategy,
                steps=steps, answer=answer, alternative=alternative)

# ============= LEKCJA 4: Kolejnosc dzialan =============
l04_warmup = [
    gen("w1", 4, "3pkt", "arytmetyka", "kolejnosc bez nawiasow",
        "Ile to 2 + 3 razy 4?",
        {"A":"14","B":"20","C":"24","D":"10","E":"9"}, "A"),
    gen("w2", 4, "3pkt", "arytmetyka", "rola nawiasow",
        "Ile to (2 + 3) razy 4?",
        {"A":"14","B":"20","C":"24","D":"10","E":"9"}, "B"),
    gen("w3", 4, "3pkt", "arytmetyka", "mnozenie i odejmowanie",
        "W koszu bylo 30 jablek. Wladek wzial 2 razy po 4 jablka. Ile zostalo?",
        {"A":"20","B":"22","C":"24","D":"26","E":"28"}, "B"),
    load_original(2025, 7),
    load_original(2019, 5),
]
l04_challenge = [
    gen("c1", 4, "4pkt", "arytmetyka", "wstawianie znakow",
        "Wstaw znaki + lub - miedzy liczby 9 _ 3 _ 2 tak, by otrzymac wynik 8. Ktory zestaw znakow jest poprawny?",
        {"A":"9 + 3 + 2","B":"9 + 3 - 2","C":"9 - 3 + 2","D":"9 - 3 - 2","E":"Nie da sie"}, "C"),
    load_original(2012, 17),
]
l04_solutions = [
    sol("gen-l04-w1", "Mnozenie przed dodawaniem.", "Najpierw mnozenie.",
        ["3 razy 4 = 12","Potem 2 + 12 = 14"], "A",
        "Pamietaj: mnozenie i dzielenie maja pierwszenstwo przed +/-."),
    sol("gen-l04-w2", "Nawiasy zmieniaja kolejnosc - liczymy najpierw w nich.", "Najpierw nawias.",
        ["2 + 3 = 5","Potem 5 razy 4 = 20"], "B",
        "Bez nawiasow byloby 14, z nawiasami 20 - 6 wiecej."),
    sol("gen-l04-w3", "2 razy po 4 to mnozenie, potem odejmowanie.", "Mnozenie przed odejmowaniem.",
        ["2 razy 4 = 8","30 - 8 = 22"], "B",
        "Mozna tez liczyc po 4: 30 - 4 = 26, 26 - 4 = 22."),
    sol("kangur-maluch-2025-7", "Wynik to a + b - c + d. Trzeba dac najwieksze do +.",
        "Najwieksze do plusowych, najmniejsze do minus.",
        ["Wynik = a + b - c + d","Maksymalny gdy a, b, d duze i c male","Liczby: 0, 2, 2, 5. Daj 0 jako c (odejmowane)","Pozostale: 5 + 2 + 2 = 9","Najwiekszy: 5 + 2 - 0 + 2 = 9"], "A",
        "Kazda kolejnosc z 0 jako odejmowane daje 9."),
    sol("kangur-maluch-2019-5", "Krzyzowka z dzialaniami - trzeba znalezc spojny uklad.",
        "Sprawdzanie warunkow w roznych polach.",
        ["Z ukladu krzyzowki cyfry 0, 2, 1, 9 i znaki +, -, =","Po rozwiazaniu wszystkich rownan w polu z ? wychodzi 7"], "D",
        "Wymaga uwaznego sledzenia rownan poziomo i pionowo."),
    sol("gen-l04-c1", "Cel: wynik 8. Sprawdz kazdy zestaw znakow.", "Sprawdzanie wynikow.",
        ["9 + 3 + 2 = 14, nie","9 + 3 - 2 = 10, nie","9 - 3 + 2 = 8 - TAK","9 - 3 - 2 = 4, nie"], "C",
        "Z 5 odpowiedzi tylko jedna daje 8."),
    sol("kangur-maluch-2012-17", "Maksymalna suma dwoch liczb 3-cyfrowych z 6 cyfr.",
        "Wieksze cyfry do setek, mniejsze do jednosci.",
        ["Cyfry 1-6 trafiaja na pozycje setek, dziesiatek, jednosci","Najwieksze cyfry (6,5) do setek: 600+500=1100","Srednie (4,3) do dziesiatek: 40+30=70","Najmniejsze (2,1) do jednosci: 2+1=3","Suma: 1100+70+3 = 1173"], "D",
        "Np. 642+531 = 1173."),
]
l04 = dict(
    id="l04", number=4, block="Liczby i dzialania", blockCode="A",
    title="Kolejnosc wykonywania dzialan",
    topic="arytmetyka", estimatedMinutes=15,
    theory=dict(
        intro="Kiedy wpiszesz na kalkulatorze 2 + 3 x 4, kalkulator odpowie 14 - a nie 20. Dlaczego? Bo mnozenie idzie pierwsze. Ta zasada ratuje przed pomylkami, ale tylko jak ja znasz. Dzis nauczysz sie kolejnosci dzialan i tego, kiedy nawiasy zmieniaja wszystko.",
        tool="Sztuczka 1: KOLEJNOSC DZIALAN. Najpierw nawiasy, potem mnozenie i dzielenie, na koncu dodawanie i odejmowanie. Ten porzadek to umowa, ktora wszyscy stosuja.\n\nSztuczka 2: NAWIASY ZMIENIAJA WSZYSTKO. (2 + 3) razy 4 = 20, ale 2 + 3 razy 4 = 14. Roznica 6 - tylko przez dwa znaki nawiasu. Zawsze patrz, czy w zadaniu sa nawiasy.\n\nSztuczka 3: PRZY UKLADANIU WSTAW ZNAKI TAK BY WYNIK BYL ZADANY. Gdy Kangur prosi: wstaw znaki by wyszlo 8 - sprawdzaj kolejne kombinacje znakow systematycznie.",
        trick="W zadaniach 'wstaw nawiasy' albo 'wstaw znaki' praca jest detektywistyczna. Spojrz na wynik, potem cofaj sie. Czesto wystarczy zauwazyc PARZYSTOSC wyniku lub jego ostatnia cyfre - to natychmiast eliminuje czesc odpowiedzi.",
    ),
    versions=[dict(versionId="v1", label="Wersja 1 (oryginalna)",
                   warmup=l04_warmup, challenge=l04_challenge, solutions=l04_solutions)],
    quiz=[
        dict(q="Ile to 5 + 2 razy 3?", choices={"A":"21","B":"11","C":"15"}, correct="B",
             explain="Najpierw 2 razy 3 = 6, potem 5 + 6 = 11."),
        dict(q="Co najpierw w (4 + 6) : 2?", choices={"A":"Nawias","B":"Dzielenie","C":"Mnozenie"}, correct="A",
             explain="Nawiasy zawsze przed dzialaniami arytmetycznymi."),
        dict(q="Bez nawiasow co jest pierwsze: dodawanie czy mnozenie?",
             choices={"A":"Dodawanie","B":"Mnozenie","C":"Po kolei od lewej"}, correct="B",
             explain="Mnozenie i dzielenie maja pierwszenstwo przed dodawaniem i odejmowaniem."),
    ],
)

# ============= LEKCJA 5: Liczby parzyste i nieparzyste =============
l05_warmup = [
    gen("w1", 5, "3pkt", "arytmetyka", "rozpoznanie parzystej",
        "Ktora z liczb jest parzysta: 7, 11, 14, 23, 35?",
        {"A":"7","B":"11","C":"14","D":"23","E":"35"}, "C"),
    gen("w2", 5, "3pkt", "arytmetyka", "suma parzystych",
        "Suma dwoch liczb parzystych jest zawsze:",
        {"A":"Parzysta","B":"Nieparzysta","C":"Czasami parzysta, czasami nieparzysta","D":"Zerem","E":"Liczba pierwsza"}, "A"),
    gen("w3", 5, "3pkt", "arytmetyka", "parzysta + nieparzysta",
        "Suma liczby parzystej i liczby nieparzystej jest zawsze:",
        {"A":"Parzysta","B":"Nieparzysta","C":"Czasami parzysta, czasami nieparzysta","D":"Zerem","E":"Mnozeniem"}, "B"),
    gen("w4", 5, "3pkt", "arytmetyka", "liczba parzystych w zakresie",
        "Ile parzystych liczb jest w zakresie od 1 do 20?",
        {"A":"5","B":"8","C":"10","D":"12","E":"20"}, "C"),
    gen("w5", 5, "3pkt", "arytmetyka", "parzystosc rezultatu",
        "Jana ma 5 ciastek, Wojtek ma 8 ciastek. Czy razem maja liczbe parzysta czy nieparzysta?",
        {"A":"Parzysta - bo razem 12","B":"Nieparzysta - bo razem 13","C":"Parzysta - bo razem 14","D":"Nieparzysta - bo razem 11","E":"Nie da sie ustalic"}, "B"),
]
l05_challenge = [
    gen("c1", 5, "4pkt", "arytmetyka", "parzystosc w lamiglowce",
        "Czy mozna polaczyc piec liczb 1, 2, 3, 4, 5 znakami + i - tak, by otrzymac liczbe PARZYSTA?",
        {"A":"Tak, da sie wynik 0","B":"Tak, da sie wynik 2","C":"Tak, da sie wynik 4","D":"Nie - wynik zawsze nieparzysty","E":"Nie - wynik zawsze rowny 15"}, "D"),
    load_original(2022, 11),
]
l05_solutions = [
    sol("gen-l05-w1", "Parzysta = konczy sie na 0, 2, 4, 6, 8.", "Sprawdz ostatnia cyfre.",
        ["7 -> nieparzysta","11 -> nieparzysta","14 -> konczy sie na 4 - parzysta","23, 35 -> nieparzyste"], "C"),
    sol("gen-l05-w2", "Parzysta + parzysta = parzysta zawsze.", "Wzor parzystosci.",
        ["Parzysta = 2 razy cos","Suma: 2a + 2b = 2(a+b) - dzieli sie przez 2","Czyli parzysta"], "A",
        "Np. 4+6=10, 8+12=20 - wszystkie parzyste."),
    sol("gen-l05-w3", "Parzysta + nieparzysta = nieparzysta.", "Sprawdz na przykladach.",
        ["2 + 3 = 5 (nieparzysta)","4 + 7 = 11 (nieparzysta)","Wzor: parzysta + nieparzysta = nieparzysta"], "B"),
    sol("gen-l05-w4", "Co druga liczba jest parzysta.", "Polowa zakresu.",
        ["Parzyste: 2,4,6,8,10,12,14,16,18,20","Razem 10 sztuk"], "C",
        "Mozna tez: 20 : 2 = 10."),
    sol("gen-l05-w5", "Suma 5 + 8 = 13.", "Suma nieparzysta + parzysta.",
        ["5 nieparzysta, 8 parzysta","5 + 8 = 13 - nieparzysta"], "B"),
    sol("gen-l05-c1", "Suma 1+2+3+4+5 = 15 nieparzysta. Czy znaki to zmienia?",
        "Zmiana + na - dla x zmienia sume o 2x (parzysta).",
        ["Suma wszystkich +: 15 (nieparzysta)","Zmiana + na - dla liczby x zmienia wynik o 2x - liczba parzysta","Parzysta zmiana nie zmienia parzystosci","Wynik zawsze NIEPARZYSTY - parzystej sie nie da"], "D",
        "Klucz: start od 15 (nieparzysta), kazda zmiana znaku to roznica parzysta."),
    sol("kangur-maluch-2022-11", "2 rzedy przed + 1 za + jego rzad = 4 rzedy.",
        "Liczenie pozycji w rzedzie i sumowanie rzedow.",
        ["W rzedzie: 5 (prawo) + 3 (lewo) + Kostek = 9 dzieci","Liczba rzedow: 2 + 1 + 1 = 4","Razem: 4 razy 9 = 36"], "A"),
]
l05 = dict(
    id="l05", number=5, block="Liczby i dzialania", blockCode="A",
    title="Liczby parzyste i nieparzyste",
    topic="arytmetyka", estimatedMinutes=12,
    theory=dict(
        intro="Liczby parzyste mozna ulozyc w pary - 2, 4, 6 cukierkow dziela sie rowno miedzy dwie osoby. Nieparzyste zostawiaja jeden bez pary - 5 cukierkow podzielisz na 2+2 a jeden zostanie. Parzystosc to super narzedzie do szybkich sprawdzen.",
        tool="Sztuczka 1: PARZYSTA = KONCZY SIE NA 0, 2, 4, 6, 8. Patrz tylko na ostatnia cyfre. 1234 jest parzysta, 12345 nieparzysta.\n\nSztuczka 2: WZORY SUMOWANIA.\n- parzysta + parzysta = parzysta\n- nieparzysta + nieparzysta = parzysta\n- parzysta + nieparzysta = nieparzysta\nZapamietaj te trzy zasady - rozwiazuja tysiac zadan.\n\nSztuczka 3: MNOZENIE. Parzysta razy cokolwiek = parzysta. Nieparzysta razy nieparzysta = nieparzysta.",
        trick="W zadaniach typu 'czy mozna otrzymac wynik X?' SAMA PARZYSTOSC eliminuje pol odpowiedzi. Jezeli suma wyjsciowa jest nieparzysta, a kazda dozwolona zmiana zmienia ja o liczbe parzysta - wynik na zawsze pozostaje nieparzysty.",
    ),
    versions=[dict(versionId="v1", label="Wersja 1 (oryginalna)",
                   warmup=l05_warmup, challenge=l05_challenge, solutions=l05_solutions)],
    quiz=[
        dict(q="3 + 7 + 5 to liczba:", choices={"A":"Parzysta","B":"Nieparzysta","C":"Nie da sie"},
             correct="B", explain="3+7=10 (parzysta), +5 = 15 (nieparzysta)."),
        dict(q="Iloczyn 4 razy 7 jest:", choices={"A":"Parzysty","B":"Nieparzysty","C":"Zerem"},
             correct="A", explain="Parzysta (4) razy cokolwiek daje parzysta."),
        dict(q="W workach 23 i 45 kulek. Czy razem parzysta?",
             choices={"A":"Tak","B":"Nie","C":"Trzeba policzyc"}, correct="A",
             explain="Nieparzysta + nieparzysta = parzysta. 23+45=68."),
    ],
)

# ============= LEKCJA 6: Sprytne liczenie =============
l06_warmup = [
    gen("w1", 6, "3pkt", "arytmetyka", "laczenie do okraglej liczby",
        "Ile to 17 + 26 + 33?",
        {"A":"66","B":"76","C":"77","D":"86","E":"96"}, "B"),
    gen("w2", 6, "3pkt", "arytmetyka", "rozdzielnosc mnozenia",
        "Ile to 25 razy 4 + 25 razy 6?",
        {"A":"125","B":"175","C":"250","D":"275","E":"300"}, "C"),
    gen("w3", 6, "3pkt", "arytmetyka", "lacznosc dodawania",
        "Ile to 99 + 17 + 1?",
        {"A":"107","B":"117","C":"118","D":"127","E":"217"}, "B"),
    gen("w4", 6, "3pkt", "arytmetyka", "grupowanie czynnikow",
        "Ile to 8 razy 25?",
        {"A":"150","B":"175","C":"200","D":"225","E":"250"}, "C"),
    load_original(2018, 11),
]
l06_challenge = [
    load_original(2012, 24),
    gen("c2", 6, "5pkt", "arytmetyka", "wynik z sekwencji operacji",
        "Mysle liczbe. Dodaje 5, mnoze przez 2, odejmuje 4. Wynik to 20. Jaka jest moja liczba?",
        {"A":"5","B":"6","C":"7","D":"8","E":"10"}, "C"),
]
l06_solutions = [
    sol("gen-l06-w1", "Szukam par do okraglej liczby.", "Lacznosc.",
        ["17 + 33 = 50","50 + 26 = 76"], "B",
        "Mozna tez po kolei: 17+26=43, 43+33=76."),
    sol("gen-l06-w2", "Rozdzielnosc: 25*(4+6) = 25*10.", "Rozdzielnosc mnozenia wzgledem dodawania.",
        ["25 razy 4 + 25 razy 6 = 25 razy (4+6) = 25 razy 10 = 250"], "C",
        "Bezposrednio: 100 + 150 = 250."),
    sol("gen-l06-w3", "99 + 1 = 100 - zacznij od tej pary.", "Lacznosc - zamien kolejnosc.",
        ["99 + 1 = 100","100 + 17 = 117"], "B"),
    sol("gen-l06-w4", "8 razy 25 - rozbij 8 na 4 razy 2.", "Grupowanie czynnikow.",
        ["8 razy 25 = 4 razy (2 razy 25) = 4 razy 50 = 200"], "C",
        "Albo: 25 razy 4 razy 2 = 100 razy 2 = 200."),
    sol("kangur-maluch-2018-11", "Suma cyfr 9+9=18, potem zastapienie itd.",
        "Iteracja - kazdy krok zmienia liczbe.",
        ["99999 -> 18999 -> 9999 -> 1899 -> 999 -> 189 -> 99 -> 18 -> 9","Liczba operacji: 8"], "E",
        "Trzeba policzyc kazdy krok osobno."),
    sol("kangur-maluch-2012-24", "Z wyniku 2012 odwracaj kazda operacje.",
        "Krok po kroku w odwrotnej kolejnosci.",
        ["2012 : 4 = 503","503 - 3 = 500","500 : 10 = 50","50 - 1 = 49","49 = 7 razy 7, czyli Michal ma 7 lat"], "D",
        "Odwracanie: minus to plus, mnozenie to dzielenie."),
    sol("gen-l06-c2", "Odwracam operacje.", "Krok po kroku wstecz.",
        ["Wynik 20, ostatnio odjeto 4: 20+4=24","Przedtem mnozono przez 2: 24:2=12","Przedtem dodano 5: 12-5=7"], "C"),
]
l06 = dict(
    id="l06", number=6, block="Liczby i dzialania", blockCode="A",
    title="Sprytne liczenie - laczenie i grupowanie",
    topic="arytmetyka", estimatedMinutes=15,
    theory=dict(
        intro="Babcia kupila 17 jablek, 26 gruszek i 33 sliwki. Liczysz po kolei: 17+26=43, potem 43+33=76. Ale jest sprytniej: zauwaz, ze 17 + 33 = 50. Wtedy 50 + 26 = 76 w glowie. Drobna zmiana kolejnosci - znacznie mniej kalkulacji.",
        tool="Sztuczka 1: LACZNOSC. Mozesz zmienic kolejnosc dodawania - szukaj par dajacych okragle liczby (do 10, 50, 100).\n\nSztuczka 2: ROZDZIELNOSC. 25*4 + 25*6 to to samo co 25*(4+6) = 25*10 = 250.\n\nSztuczka 3: GRUPOWANIE CZYNNIKOW. 8 razy 25 - rozbij 8 na 4*2, wtedy 4*(2*25)=4*50=200. Szukaj 'okraglych' produktow jak 4*25, 5*20, 2*50.\n\nSztuczka 4: ODWRACANIE OPERACJI. Gdy ktos mowi 'pomyslalem liczbe, dodalem 5, pomnozylem przez 2 i wyszlo 14', odwroc: 14:2=7, 7-5=2.",
        trick="Kangur uwielbia zadania ze sciezka operacji. Zamiast podstawiac kolejne odpowiedzi, odwroc operacje od wyniku do startu. To 5 razy szybsze i mniej miejsca na blad.",
    ),
    versions=[dict(versionId="v1", label="Wersja 1 (oryginalna)",
                   warmup=l06_warmup, challenge=l06_challenge, solutions=l06_solutions)],
    quiz=[
        dict(q="Najszybciej obliczysz 38 + 47 + 12 + 53 wybierajac:",
             choices={"A":"Po kolei","B":"Pary 38+12 i 47+53","C":"Pary 38+47 i 12+53"}, correct="B",
             explain="38+12=50, 47+53=100, razem 150."),
        dict(q="Ile to 4 razy 25 razy 7?", choices={"A":"700","B":"175","C":"100"}, correct="A",
             explain="4*25=100, 100*7=700."),
        dict(q="Pomyslalem liczbe, pomnozylem przez 3, dodalem 1, wyszlo 16. Jaka liczba?",
             choices={"A":"4","B":"5","C":"6"}, correct="B",
             explain="Odwracam: 16-1=15, 15:3=5."),
    ],
)

# ============= LEKCJA 7: Zaokraglanie i szacowanie =============
l07_warmup = [
    gen("w1", 7, "3pkt", "arytmetyka", "zaokraglanie do 10",
        "Liczba 47 zaokraglona do dziesiatek to:",
        {"A":"40","B":"45","C":"50","D":"47","E":"57"}, "C"),
    gen("w2", 7, "3pkt", "arytmetyka", "zaokraglanie do 100",
        "Liczba 234 zaokraglona do setek to:",
        {"A":"100","B":"200","C":"230","D":"240","E":"300"}, "B"),
    gen("w3", 7, "3pkt", "arytmetyka", "szacowanie sumy",
        "Najszybciej oszacujesz 198 + 405 wybierajac:",
        {"A":"200 + 400 = 600","B":"100 + 400 = 500","C":"200 + 500 = 700","D":"liczenie dokladne","E":"100 + 500 = 600"}, "A"),
    gen("w4", 7, "3pkt", "arytmetyka", "eliminacja zlej odpowiedzi",
        "Ola kupila 12 jablek po 3 zl. Bez dokladnego liczenia - ktora suma NIE moze byc poprawna?",
        {"A":"36 zl","B":"30 zl","C":"60 zl","D":"35 zl","E":"40 zl"}, "C"),
    load_original(2012, 16),
]
l07_challenge = [
    gen("c1", 7, "4pkt", "arytmetyka", "szacowanie i sprawdzenie",
        "Filip pomnozyl 198 przez 5. Ktory z ponizszych wynikow jest najblizszy poprawnego?",
        {"A":"800","B":"950","C":"1000","D":"1500","E":"2000"}, "C"),
    load_original(2025, 11),
]
l07_solutions = [
    sol("gen-l07-w1", "47 jest miedzy 40 a 50. Cyfra jednosci 7 (>=5) - w gore.",
        "Zasada zaokraglania.",
        ["Cyfra jednosci to 7 (>=5)","Zaokraglamy w gore: 47 -> 50"], "C"),
    sol("gen-l07-w2", "234 jest miedzy 200 a 300. Cyfra dziesiatek 3 (<5) - w dol.",
        "Zaokraglenie do setek - patrz cyfre dziesiatek.",
        ["Cyfra dziesiatek to 3 (<5)","Zaokraglamy w dol: 234 -> 200"], "B"),
    sol("gen-l07-w3", "Szacowanie - obie liczby do najblizszych setek.", "Zaokraglij oba.",
        ["198 ~ 200","405 ~ 400","Suma ~ 600"], "A",
        "Dokladnie 198+405=603, oszacowanie 600 jest blisko."),
    sol("gen-l07-w4", "Sprawdz przyblizenie: 12 razy 3 = 36.", "Szacowanie i eliminacja.",
        ["12 razy 3 = 36","Odpowiedzi blisko 36: 30, 35, 36, 40","60 jest za duzo - to byloby 12 razy 5","Eliminuje 60"], "C"),
    sol("kangur-maluch-2012-16", "Rywale = chlopcy + dziewczyny = x + 2x = 3x. Wszyscy = 1 + 3x.",
        "Sprawdzanie ktora odpowiedz daje calkowite x.",
        ["Wszyscy = 1 (Krzys) + 3x","25: 1+3x=25, 3x=24, x=8 - TAK","Pozostale opcje nie daja calkowitego x","Odpowiedz: 25 osob"], "D"),
    sol("gen-l07-c1", "198 razy 5 ~ 200 razy 5 = 1000.", "Szacowanie i porownanie.",
        ["198 ~ 200","200 razy 5 = 1000","Najblizsza odpowiedz: 1000"], "C",
        "Dokladnie: 198 razy 5 = 990."),
    sol("kangur-maluch-2025-11", "5 duzych + 1 mala = 210 g. Mala je 2x duza.",
        "Rownanie z proporcjami.",
        ["Niech duza = d, mala = 2d","5d + 2d = 210","7d = 210, d = 30","Mala = 2 razy 30 = 60 g"], "B"),
]
l07 = dict(
    id="l07", number=7, block="Liczby i dzialania", blockCode="A",
    title="Zaokraglanie i szacowanie",
    topic="arytmetyka", estimatedMinutes=12,
    theory=dict(
        intro="W sklepie widzisz cene 4 zl 87 gr. Pewnie myslisz - 'okolo 5 zl'. To zaokraglanie. Nie musisz znac dokladnej liczby, by miec wyobrazenie. W Kangurku zaokraglanie pomoze Ci ELIMINOWAC zle odpowiedzi w 5 sekund zamiast 5 minut.",
        tool="Sztuczka 1: ZAOKRAGLAJ DO DZIESIATEK. Cyfra jednosci 0-4 w dol, 5-9 w gore. 47 -> 50, 23 -> 20.\n\nSztuczka 2: ZAOKRAGLAJ DO SETEK. Cyfra dziesiatek 0-4 w dol, 5-9 w gore. 347 -> 300, 165 -> 200.\n\nSztuczka 3: SZACUJ SUME LUB PRODUKT. 198 + 405 - zamiast liczyc, zrob 200 + 400 = 600.\n\nSztuczka 4: ELIMINACJA ODPOWIEDZI. Szybkie oszacowanie pozwala odrzucic odpowiedzi za duze lub za male.",
        trick="Najprostsza sztuczka eliminacji: spojrz na cyfre koncowa wyniku. 17 razy 8 - cyfra koncowa to ostatnia cyfra 7*8=56, czyli 6. Z odpowiedzi szukaj tylko konczacych sie na 6.",
    ),
    versions=[dict(versionId="v1", label="Wersja 1 (oryginalna)",
                   warmup=l07_warmup, challenge=l07_challenge, solutions=l07_solutions)],
    quiz=[
        dict(q="Zaokraglij 685 do setek.", choices={"A":"600","B":"700","C":"680"}, correct="B",
             explain="Cyfra dziesiatek 8 (>=5), w gore: 700."),
        dict(q="Najszybciej oszacujesz 489 razy 6:",
             choices={"A":"500 razy 6 = 3000","B":"400 razy 6 = 2400","C":"500 razy 5 = 2500"}, correct="A",
             explain="489 ~ 500, czyli 3000. Dokladnie 2934."),
        dict(q="Cyfra ostatnia 27 razy 4 to:", choices={"A":"6","B":"8","C":"4"}, correct="B",
             explain="Ostatnia cyfra 7*4=28, czyli 8."),
    ],
)

# ============= LEKCJA 8: Lamiglowki rachunkowe =============
l08_warmup = [
    gen("w1", 8, "3pkt", "lamiglowki", "kryptarytm prosty",
        "W dzialaniu A + 5 = 12 jaka cyfra to A?",
        {"A":"5","B":"6","C":"7","D":"8","E":"9"}, "C"),
    gen("w2", 8, "3pkt", "lamiglowki", "wstawianie znakow",
        "Wstaw znaki + lub - miedzy liczby 1 _ 2 _ 3 _ 4 _ 5 tak, by wynik byl rowny 1. Ktory zestaw dziala?",
        {"A":"1 + 2 + 3 + 4 + 5","B":"1 - 2 + 3 + 4 - 5","C":"1 + 2 - 3 + 4 + 5","D":"1 - 2 - 3 - 4 - 5","E":"1 + 2 + 3 - 4 - 5"}, "B"),
    gen("w3", 8, "3pkt", "lamiglowki", "brakujacy skladnik",
        "W dzialaniu 13 + B = 31 jaka liczba to B?",
        {"A":"8","B":"18","C":"22","D":"28","E":"44"}, "B"),
    load_original(2012, 11),
    load_original(2025, 16),
]
l08_challenge = [
    load_original(2022, 23),
    load_original(2019, 18),
]
l08_solutions = [
    sol("gen-l08-w1", "A + 5 = 12, czyli A = 12 - 5.", "Odejmowanie - odwrocenie dodawania.",
        ["A = 12 - 5 = 7"], "C"),
    sol("gen-l08-w2", "Sprawdzam kazdy zestaw znakow.", "Sprawdzanie wynikow.",
        ["1+2+3+4+5 = 15, nie","1-2+3+4-5 = 1 - TAK","Pozostale daja inne wartosci"], "B",
        "Z 5 odpowiedzi tylko jedna daje wynik 1."),
    sol("gen-l08-w3", "13 + B = 31, czyli B = 31 - 13.", "Odejmowanie.",
        ["B = 31 - 13 = 18"], "B"),
    sol("kangur-maluch-2012-11", "20 ciastek, 15 z rodzynkami, 15 z orzechami. Najmniejsza wspolna.",
        "Inkluzja-ekskluzja.",
        ["Rodzynki + orzechy = 15 + 15 = 30","Wspolnych co najmniej: 30 - 20 = 10","Najmniejsza liczba ciastek z obydwoma: 10"], "E"),
    sol("kangur-maluch-2025-16", "Owoce: 2 mango, jablka, 1 gruszka, banany, 30 sliwek - razem 106. Warunki o rownych liczbach.",
        "Uklad warunkow z ograniczeniami.",
        ["Suma znanych bez zatartych: 2 + 1 + 30 = 33","Jablka + banany = 106 - 33 = 73","Po analizie warunkow (dwa rodzaje po tyle samo, jeden o ponad 10 wiekszy) wychodzi: banany = 23"], "E",
        "Wymaga precyzyjnej analizy warunkow rownosci."),
    sol("kangur-maluch-2022-23", "3 rodzaje figur w 3x3 z sumami wierszy 34, 32, 26.",
        "Uklad rownan.",
        ["Niech trojkat=a, gwiazda=b, kolo=c","Wiersz 1 (a,b,b): a + 2b = 34","Wiersz 3 (b,a,a): 2a + b = 26","Dodaj W1+W3: 3a + 3b = 60, czyli a+b = 20","Z W1: a + 2b = 34, podstaw a=20-b: 20+b=34, b=14, a=6","Wiersz 2 (a,b,c): 6 + 14 + c = 32, c = 12"], "D"),
    sol("kangur-maluch-2019-18", "Cyfra 5 pojawia sie dokladnie 16 razy.",
        "Liczenie wystapien cyfry.",
        ["Cyfra 5 w jednosciach: 5, 15, 25, 35, 45 (5 razy do strony 49)","W przedziale 50-59: cyfra 5 w dziesiatkach 10 razy + w 55 jeszcze w jednosciach","Razem do strony 59: 5 + 10 + 1 = 16","Czyli ksiazka ma co najwyzej 59 stron"], "A"),
]
l08 = dict(
    id="l08", number=8, block="Liczby i dzialania", blockCode="A",
    title="Lamiglowki rachunkowe i kryptarytmy",
    topic="lamiglowki", estimatedMinutes=18,
    theory=dict(
        intro="Detektyw matematyczny szuka brakujacej cyfry. A + 5 = 12 gdzie A jest zagadka. To kryptarytm - rozumowanie ktore daje wiecej radosci niz dokladne liczenie. Kangur uwielbia takie zadania, bo trzeba myslec, a nie tylko liczyc.",
        tool="Sztuczka 1: ODWRACAJ OPERACJE. Jezeli A + 5 = 12, to A = 12 - 5 = 7. Brakujaca liczba wychodzi z odejmowania.\n\nSztuczka 2: PATRZ NA OSTATNIA CYFRE. Cyfra koncowa wyniku zalezy tylko od cyfr koncowych skladnikow.\n\nSztuczka 3: SYSTEMATYCZNIE SPRAWDZAJ. Gdy odpowiedz nie jest oczywista, podstawiaj kolejne mozliwosci. Z 5 odpowiedzi zwykle mozesz wykluczyc 2-3 szybko.\n\nSztuczka 4: UKLAD ROWNAN W FIGURACH. Trzy figury, trzy sumy - to uklad rownan. Dodaj wszystko, znajdz wartosci po kolei.",
        trick="W kryptarytmach z DUZYMI liczbami zacznij od KOLUMNY JEDNOSCI - tam zwykle jest pierwsza wskazowka. Przeniesienia z kolumny do kolumny daja kolejne. Idz krok po kroku, nie probuj wszystkiego naraz.",
    ),
    versions=[dict(versionId="v1", label="Wersja 1 (oryginalna)",
                   warmup=l08_warmup, challenge=l08_challenge, solutions=l08_solutions)],
    quiz=[
        dict(q="A + 8 = 15. Ile to A?", choices={"A":"6","B":"7","C":"8"}, correct="B",
             explain="A = 15 - 8 = 7."),
        dict(q="W kryptarytmie z duzymi liczbami zaczynam od:",
             choices={"A":"Kolumny jednosci","B":"Kolumny setek","C":"Srodka"}, correct="A",
             explain="Kolumna jednosci daje pierwsza wskazowke."),
        dict(q="Trzy figury, trzy sumy wierszy - co robie?",
             choices={"A":"Ukladam rownania","B":"Probuje wszystkich liczb","C":"Pomijam"}, correct="A",
             explain="Uklad rownan - dodaj wszystkie i znajdz wartosci po kolei."),
    ],
)

for lesson in [l04, l05, l06, l07, l08]:
    lid = lesson["id"]
    with open(f"data/lessons/{lid}.json", "w", encoding="utf-8") as f:
        json.dump(lesson, f, ensure_ascii=False, indent=2)
    print(f"{lid}: OK")
print("DONE")
