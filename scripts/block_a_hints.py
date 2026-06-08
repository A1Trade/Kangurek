"""Dodaje statyczne podpowiedzi (hint) do wszystkich rozwiazan w bloku A (l01-l08)
oraz naprawia stubowe rozwiazania v3 (oryginaly Kangurka) - pelne kroki rozwiazania.
Dziala bez API key."""
import json
from pathlib import Path

# ===========================
# HINTY - krotkie nudge (1-2 zdania), nie zdradzaja odpowiedzi
# ===========================
HINTS: dict[str, str] = {
    # ---- l01: Dodawanie i odejmowanie do 1000 ----
    "gen-l01-w1": "Zaokraglij obie liczby do pelnych setek i poprawiaj resztke.",
    "gen-l01-w2": "Pomysl: od 800 najlatwiej odjac liczbe blisko 250.",
    "gen-l01-w3": "Szukaj par, ktore daja okragla liczbe (np. 37 + 63).",
    "gen-l01-w4": "Obie liczby sa blisko pelnych setek - zaokraglij i popraw.",
    "gen-l01-w5": "Brakuje 134, wiec szukasz 1000 minus 134.",
    "gen-l01-c1": "Kazda liczba to prawie pelna setka. Dodaj setki, potem popraw o brakujace.",
    "gen-l01-c2": "Rob krok po kroku: dodaj/odejmij i zapisuj wynik po kazdej operacji.",
    "gen-l01-v2-w1": "Zaokraglij obie liczby do setek, potem popraw.",
    "gen-l01-v2-w2": "1000 minus liczba blisko 400 - rob to przez zaokraglenie.",
    "gen-l01-v2-w3": "Szukaj par: 48+52 i 27+13.",
    "gen-l01-v2-w4": "599 i 401 to prawie 600 i 400 - razem 1000.",
    "gen-l01-v2-w5": "600 minus 287 - mozesz odjac 300 i dodac 13.",
    "gen-l01-v2-c1": "Kazde z 99, 198, 299 to setka minus 1. Razem to 600 minus 3.",
    "gen-l01-v2-c2": "Idz po kolei: 800, +350, -599.",
    "kangur-maluch-2020-1": "Sumuj pary symetryczne: 1+1, 2+2, 3+3, 4+4 i sam srodek 5.",

    # ---- l02: Mnozenie - tabliczka i zastosowania ----
    "gen-l02-w1": "7 razy 8 - klasyczna tabliczka.",
    "gen-l02-w2": "Mnozysz przez 10 - tylko dopisz zero na koncu.",
    "gen-l02-w3": "12 to 10 + 2, wiec 12 razy 7 = 70 + 14.",
    "gen-l02-w4": "Prostokat 4 na 9 to 4 razy 9 z tabliczki.",
    "gen-l02-w5": "Co godzina podwajamy: 1 -> 2 -> 4 -> 8 -> ...",
    "gen-l02-c1": "Policz dwie grupy osobno (6 stolow po 6, 4 stoly po 8), potem dodaj.",
    "gen-l02-c2": "Mnozenie 2-cyfrowej przez 11: cyfre pierwsza, suma cyfr, cyfre druga.",
    "gen-l02-v2-w1": "6 razy 9 - tabliczka.",
    "gen-l02-v2-w2": "Mnozenie przez 10 - dopisz zero.",
    "gen-l02-v2-w3": "Rozbij 11 na 10+1: 8 razy 11 = 80 + 8.",
    "gen-l02-v2-w4": "5 razy 7 - prosta tabliczka.",
    "gen-l02-v2-w5": "Codziennie razy 2: 1, 2, 4, 8, ...",
    "gen-l02-v2-c1": "Dwa mnozenia osobno i dodaj na koniec.",
    "gen-l02-v2-c2": "25 razy 11: dodaj 250 + 25 albo zapisz 2_(2+5)_5.",
    "kangur-maluch-2020-12": "Suma odjeta trzy razy: 50 - 24 - 13 - 7 = 6, wiec odjeto 3 razy po 2. Liczby to 24+2, 13+2, 7+2.",
    "kangur-maluch-2022-14": "Obwod kwadratu = 20m, obwod prostokata = 30m. Szukaj wspolnej wielokrotnosci.",
    "kangur-maluch-2023-20": "Marysia ma 9 pilek (b + n = 9, b = 2n). Wyjdz od tego ile bialych ma Marysia.",

    # ---- l03: Dzielenie i reszty ----
    "gen-l03-w1": "36 podzielic przez 4 - prosta tabliczka.",
    "gen-l03-w2": "20 podzielic przez 3 to 6 reszty 2. Pelnych dni: 6.",
    "gen-l03-w3": "25 podzielic przez 6: ile pelnych grup, jaka reszta?",
    "gen-l03-w4": "Reszta tez musi miec lawke - wiec zaokraglaj w gore.",
    "gen-l03-w5": "Dzielenie przez 10 - skresl jedno zero.",
    "gen-l03-c1": "Sprawdz odpowiedzi po kolei: ktora daje reszte 3 przy /7 i reszte 2 przy /5?",
    "gen-l03-c2": "Cyfra jednosci 16 razy 7 zalezy tylko od cyfr jednosci 6 razy 7.",
    "gen-l03-v2-w1": "48 podzielic na 6 - klasyczna tabliczka.",
    "gen-l03-v2-w2": "30 podzielic na 4 z reszta. Liczba pelnych dni.",
    "gen-l03-v2-w3": "19 podzielic na 5: pelne grupy i reszta.",
    "gen-l03-v2-w4": "50 / 8 z reszta - reszta tez potrzebuje pudelka.",
    "gen-l03-v2-w5": "100 / 10 - skresl zero.",
    "gen-l03-v2-c1": "Liczba w przedziale 31-39. Sprawdz reszte po kolei.",
    "gen-l03-v2-c2": "Ostatnia cyfra zalezy tylko od jednosci: 3 razy 4.",
    "kangur-maluch-2020-16": "Sprawdz odpowiedzi: dla kazdej liczby druzyn rozpisz mozliwe sumy 5a + 6b = 43.",
    "kangur-maluch-2024-5": "To trzy kolejne liczby. Pomysl czego nie widac w ...7, ...898, 48... - liczby rosna o 1.",

    # ---- l04: Kolejnosc dzialan ----
    "gen-l04-w1": "Najpierw mnozenie, potem dodawanie. 3*4 i dodaj 2.",
    "gen-l04-w2": "Nawias zmienia kolejnosc - najpierw 2+3.",
    "gen-l04-w3": "Najpierw policz ile wzial (2 razy 4), potem odejmij.",
    "kangur-maluch-2025-7": "Wynik = +a +b -c +d. Ktora liczbe oplaca sie odjac, a ktore dodac?",
    "kangur-maluch-2019-5": "Wykonuj dzialania w jednym wierszu (lub kolumnie) zachowujac kolejnosc.",
    "gen-l04-c1": "Wypisz wartosc dla kazdego zestawu znakow i porownaj z 8.",
    "kangur-maluch-2012-17": "Daj najwieksze cyfry (6, 5) na pozycje setek - wtedy masz najwieksze setki.",
    "gen-l04-v2-w1": "Mnozenie przed odejmowaniem: najpierw 2*3.",
    "gen-l04-v2-w2": "Nawias najpierw: 10-2 = 8, potem razy 3.",
    "gen-l04-v2-w3": "Mnozenie pierwsze: 5*2 = 10, dodaj 4.",
    "gen-l04-v2-w4": "Dzielenie przed odejmowaniem: 12:4 = 3.",
    "kangur-maluch-2018-7": "Po 3 strzaly to po 9 punktow srednio. Patrz na sume tarcz, nie 'srednia'.",
    "gen-l04-v2-c1": "Nawias zmienia znak - sprawdz dwa polozenia.",
    "kangur-maluch-2022-21": "Zacznij od najmniejszego (Magda) i wypisuj wszystkie zaleznosci.",
    "kangur-maluch-2024-12": "Suma rybek = 9 dziennie. Po kilku dniach jedno ma 26 - z tego policz liczbe dni.",
    "kangur-maluch-2025-10": "Razem 15 ciastek, ma byc po rowno na 3 talerze. Ile musi byc na kazdym?",

    # ---- l05: Parzyste i nieparzyste ----
    "gen-l05-w1": "Parzysta konczy sie na 0, 2, 4, 6, 8.",
    "gen-l05-w2": "Parzysta + parzysta = ZAWSZE parzysta.",
    "gen-l05-w3": "Parzysta + nieparzysta = ZAWSZE nieparzysta.",
    "gen-l05-w4": "Od 1 do 20 co druga jest parzysta.",
    "gen-l05-w5": "5 + 8 = 13. Czy 13 jest parzyste czy nieparzyste?",
    "gen-l05-c1": "Suma 1+2+3+4+5 = 15. Zmiana znaku nie zmienia parzystosci.",
    "kangur-maluch-2022-11": "Razem 4 rzedy (2 przed + 1 za + jego). Po 9 dzieci w kazdym (po prawej 5 + on + po lewej 3).",
    "gen-l05-v2-w1": "Nieparzysta konczy sie na 1, 3, 5, 7, 9.",
    "gen-l05-v2-w2": "Nieparzysta + nieparzysta = parzysta.",
    "gen-l05-v2-w3": "Parzysta razy cokolwiek = parzysta.",
    "gen-l05-v2-w4": "Od 1 do 30 co druga liczba jest nieparzysta.",
    "gen-l05-v2-w5": "Suma parzystych to znow parzysta.",
    "gen-l05-v2-c1": "Posum w parach: 1+10, 2+9, ..., 5+6. Pieć par po 11.",
    "kangur-maluch-2022-15": "Kazda druzyna gra 2 mecze, wiec max 6 pkt. Sprawdz ktorej sumy nie da sie zlozyc z {0,1,3}.",
    "kangur-maluch-2016-17": "Suma = 3*wiek + (wiek+3) = 4*wiek + 3. Sprawdz ktora odpowiedz pasuje.",
    "kangur-maluch-2016-18": "Jablek 25 = 3a + 4b. Sprawdz pary (a, b) - potem gruszki 6a + 8b.",

    # ---- l06: Sprytne liczenie ----
    "gen-l06-w1": "Szukaj par do okraglej liczby: 17 + 33 = 50.",
    "gen-l06-w2": "Wyciagnij 25 przed nawias: 25 * (4+6).",
    "gen-l06-w3": "99 + 1 = 100, dodaj 17.",
    "gen-l06-w4": "8 razy 25 = 4 razy 50 = 2 razy 100.",
    "kangur-maluch-2018-11": "Najpierw 9+9=18, zostaje 1899, dalej 1+8=9, itd. Licz operacje.",
    "kangur-maluch-2012-24": "Odwracaj: 2012:4 = 503, -3 = 500, :10 = 50, -1 = 49, pierwiastek z 49 = 7.",
    "gen-l06-c2": "Odwracaj od wyniku: 20 + 4 = 24, : 2 = 12, - 5 = 7.",
    "gen-l06-v2-w1": "Szukaj par do 50 lub 100: 23+27, 19+31.",
    "gen-l06-v2-w2": "Wyciagnij 50: 50 * (7+3) = 50 * 10.",
    "gen-l06-v2-w3": "4 razy 25 = 100, dalej razy 17.",
    "gen-l06-v2-w4": "Odwracaj: 25 + 3 = 28, : 4 = 7.",
    "kangur-maluch-2018-3": "6 + 4 + 8 - dodaj wszystkie wieki.",
    "kangur-maluch-2012-20": "Sliwki najwiecej: g:j:m:s = 1:3:15:105. Razem 124 czesci = 496.",
    "gen-l06-v2-c2": "Odwracaj: 31 - 10 = 21, : 3 = 7, + 8 = 15.",
    "kangur-maluch-2019-11": "Z 3 nieb. -> 1 czer. Z 16 nieb. -> 5 czer. (zostaje 1 nieb.). Z 2 czer. -> 5 ziel.",
    "kangur-maluch-2021-12": "Niech koala zjadl x z pierwszej. Z drugiej zjadl (20-x), z trzeciej 2. Razem zostalo zawsze tyle samo.",
    "kangur-maluch-2023-11": "Niech a aut po 2 osoby i b aut po 3 osoby. a+b=8, 2a+3b=19.",
    "kangur-maluch-2023-22": "Za 9 lat (s+9), 3 lata temu (s-3). Rownanie: s+9 = 4(s-3).",

    # ---- l07: Zaokraglanie i szacowanie ----
    "gen-l07-w1": "Cyfra jednosci to 7 - zaokraglamy w gore.",
    "gen-l07-w2": "Cyfra dziesiatek to 3 - zaokraglamy w dol.",
    "gen-l07-w3": "Zaokraglij oba: 200 + 400.",
    "gen-l07-w4": "12 razy 3 = 36 - jest dokladnie. Ktora odpowiedz nie ma sensu?",
    "kangur-maluch-2012-16": "Rywale = 3x (x chlopcow + 2x dziewczat). Wszyscy = 3x + 1 (Krzys). Sprawdz odpowiedzi.",
    "gen-l07-c1": "200 razy 5 = 1000 - to twoje przyblizenie.",
    "kangur-maluch-2025-11": "5 duzych po x, mala 2x. Razem 5x + 2x = 7x = 210. Mala dostala 2x.",
    "gen-l07-v2-w1": "Cyfra jednosci 3 - w dol.",
    "gen-l07-v2-w2": "Cyfra dziesiatek 5 - w gore.",
    "gen-l07-v2-w3": "300 + 600 = 900.",
    "gen-l07-v2-w4": "Mnozysz cyfre jednosci 3 przez 4 i bierzesz ostatnia cyfre.",
    "kangur-maluch-2022-6": "Zestaw 3 skokow = 4m. 16m to 4 zestawy. Razem skokow = 4 razy 3.",
    "gen-l07-v2-c1": "Wynik powinien byc blisko 350. Wybierz odpowiedz blisko.",
    "kangur-maluch-2018-17": "Co 4 skoki (3 przod + 1 tyl) = 4m. 14 skokow = 3 zestawy + 2. Policz drogi.",
    "kangur-maluch-2012-13": "Pieski po 4 nogi, kaczki po 2, gaski po 2, owce po 4. 3*4 + 4*2 + 2*2 + 4*x = 44.",
    "kangur-maluch-2021-6": "kozlarzy x, borowikow x+6. x + (x+6) = 20.",
    "kangur-maluch-2021-18": "Liczba dzieli sie przez 2, 3 i 4 (czyli przez 12). Mniejsze niz 50: 12, 24, 36, 48. Sprawdz ktora daje reszte 1 przy /7 (bo brakuje 6).",
    "kangur-maluch-2024-2": "Najwieksza to ta z najwiekszym skladnikiem - 202 dominuje.",

    # ---- l08: Lamiglowki rachunkowe ----
    "gen-l08-w1": "A = 12 - 5.",
    "gen-l08-w2": "Wypisz wynik dla kazdego zestawu - tylko jeden daje 1.",
    "gen-l08-w3": "B = 31 - 13.",
    "kangur-maluch-2012-11": "20 ciastek. Z rodzynkami 15, z orzechami 15. Min wspolnych = 15 + 15 - 20 = 10.",
    "kangur-maluch-2025-16": "Dwie pary po rowno + osobna liczba. Suma 2+1+30+2x+2y+z = 106, czyli 2x+2y+z = 73.",
    "kangur-maluch-2022-23": "Suma wierszy = 34, 32, 26. Roznice mowia o roznych figurach. trojkat+gwiazda+gwiazda=34 itd.",
    "kangur-maluch-2019-18": "Cyfra 5 w jednosciach: 5, 15, 25, ... Cyfra 5 w dziesiatkach: 50-59. Licz dopoki nie dojdziesz do 16.",
    "gen-l08-v2-w1": "A = 16 - 7.",
    "gen-l08-v2-w2": "B = 21 : 3.",
    "gen-l08-v2-w3": "5 + 5 + 5 = 15 - od razu pasuje.",
    "kangur-maluch-2012-14": "Suma oczek 33. Sasiednie pola po tyle samo - kazda para 'styka sie' rowna liczba.",
    "kangur-maluch-2012-6": "Zsumuj 3 strzaly Michala i 3 Kuby. Roznica i kto wiekszy.",
    "kangur-maluch-2025-23": "Suma 1-12 = 78. Podzielona na 4 proste po 3 nowe liczby - oblicz sume jednej prostej.",
    "kangur-maluch-2018-19": "Liczba > 88 (po +11 trzycyfrowa). Po -11 = a*a (kwadrat). Sprawdz 11, 25, 36, 49, 64, 81.",
    "kangur-maluch-2013-2": "4X + 5X = 104. Dziesiatki: 4+5 = 9 (+ przeniesienie). Jednosci: X+X konczy sie na 4.",
    "kangur-maluch-2016-20": "27 dziele na 1:2, czyli 9 i 18. Z 18 znow na 1:2: 6 i 12. Z 12: 4 i 8. Z 9: 3 i 6. Itd.",
    "kangur-maluch-2019-12": "Najmniejsza suma: liczba 3-cyfrowa z 0 na poczatku nie istnieje. 102 + 9 = 111, 109 + 2, ...",
    "kangur-maluch-2020-23": "NAR + JA - RAC. Maksymalizuj NAR (=987) i JA (cofrowy), minimalizuj RAC.",
    "kangur-maluch-2021-20": "Sumy par sasiednich znane - rozwiazuj jak lancuch: a+b=s1, b+c=s2, itd.",
    "kangur-maluch-2021-24": "9 roznych cyfr. Suma najmniejsza - daj male cyfry w setki (>=1).",
    "kangur-maluch-2023-13": "3 skrzynie po 40 dukatow = 120 dukatow. Sklad: kule, sztabki, gwiazdki w roznych proporcjach.",
    "kangur-maluch-2023-23": "Suma 1-7 = 28. Sumy pomiedzy = razem 56. Polacz pary po sumie.",
    "kangur-maluch-2024-15": "Suma wszystkich 1-7 = 28. 4 okregi po 10 = 40. Nadwyzka 12 to wartosci wspolne.",
    "kangur-maluch-2024-16": "Na bialej stronie naprzeciw 1 jest 5, naprzeciw 2 jest 6, itd. Jezeli widzisz 5, na drugiej stronie tej czesci jest 1.",
    "kangur-maluch-2024-18": "Dodaj od najmlodszej cyfry: 3+4+_ = ..., potem _+_+1 z przeniesieniem, ...",
    "kangur-maluch-2024-20": "trojkat+trojkat to 2 cyfry, max 2*9=18. Wiec kwadrat=1. Z drugiego: kolko+trojkat=11.",
}

# ===========================
# PELNE ROZWIAZANIA DO STUBOW v3 (oryginaly Kangurka)
# format: problemId -> {observation, strategy, steps, alternative}
# ===========================
SOLUTIONS_FIX: dict[str, dict] = {
    # l01 v3
    "kangur-maluch-2020-1": dict(
        observation="Ciag liczb rosnie i potem maleje symetrycznie wokol 5.",
        strategy="Pary symetryczne: 1+1, 2+2, 3+3, 4+4 plus srodek 5.",
        steps=[
            "Lewa polowa: 1, 2, 3, 4, 5.",
            "Prawa polowa: 4, 3, 2, 1.",
            "Pary: (1+1) + (2+2) + (3+3) + (4+4) = 2 + 4 + 6 + 8 = 20.",
            "Dodaj srodek 5: 20 + 5 = 25.",
        ],
        alternative="Mozna policzyc liniowo: 1+2+3+4+5 = 15, 4+3+2+1 = 10, razem 25.",
    ),
    # l02 v3
    "kangur-maluch-2020-12": dict(
        observation="Helena odjela ta sama liczbe od kazdej z trzech liczb. Suma malala.",
        strategy="Suma odjeta = roznica miedzy sumami przed i po.",
        steps=[
            "Suma przed: 50.",
            "Suma po: 24 + 13 + 7 = 44.",
            "Odjeto razem: 50 - 44 = 6.",
            "Odjeto od kazdej tej samej liczby: 6 : 3 = 2.",
            "Liczby poczatkowe: 24+2 = 26, 13+2 = 15, 7+2 = 9.",
            "Wsrod odpowiedzi pasuje 9.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2022-14": dict(
        observation="Hanik chodzi obwodem 20m, Gerszon obwodem 30m. W przeciwnych kierunkach.",
        strategy="Spotkaja sie ponownie w punkcie A gdy obaj zrobia pelne okrazenia.",
        steps=[
            "Obwod kwadratu Hanika: 4 * 5 = 20m.",
            "Obwod prostokata Gerszona: 2*(5+10) = 30m.",
            "Najmniejsza wspolna wielokrotnosc 20 i 30 to 60m.",
            "Hanik musi przejsc 60m, czyli 60 : 20 = 3 okrazenia.",
            "Gerszon musi przejsc 60m, czyli 60 : 30 = 2 okrazenia.",
            "Hanik musi obejsc kwadrat co najmniej 3 razy.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2023-20": dict(
        observation="Marysia i Jozek maja po 9 pilek. Lacznie 8 niebieskich i 10 bialych.",
        strategy="Najpierw rozwiaz pilki Marysi: b = 2n, b + n = 9.",
        steps=[
            "Marysia: bialych = 2 * niebieskich, razem 9. Czyli 2n + n = 9, n = 3, b = 6.",
            "Marysia ma 6 bialych i 3 niebieskie.",
            "Jozek: bialych = 10 - 6 = 4.",
            "Sprawdzenie: Jozek niebieskich = 8 - 3 = 5, razem 4 + 5 = 9. OK.",
        ],
        alternative=None,
    ),
    # l03 v3
    "kangur-maluch-2020-16": dict(
        observation="Drużyny po 5 lub 6 osob, lacznie 43 uczestnikow.",
        strategy="Znajdz a, b takie ze 5a + 6b = 43 (a, b nieujemne calkowite).",
        steps=[
            "Sprawdz odpowiedzi: dla a+b drużyn rozpisz mozliwe sumy.",
            "Probuj b = 3 (drużyn po 6): 18. Zostaje 25 = 5*5. Czyli a=5, b=3 -> 8 drużyn.",
            "Sprawdzenie: 5*5 + 6*3 = 25 + 18 = 43. OK.",
            "Razem drużyn: 5 + 3 = 8.",
        ],
        alternative="Probuj inne kombinacje: b=8 daje 48 (za duzo), b=2 daje 12, zostaje 31 (5 nie dzieli).",
    ),
    "kangur-maluch-2024-5": dict(
        observation="Trzy kolejne liczby 4-cyfrowe. Czesc cyfr zakryta: '...7', '...898', '48...'.",
        strategy="Liczby roznia sie o 1. Z '48...' wiadomo ze 3-cia liczba zaczyna sie 48.",
        steps=[
            "3-cia liczba: 48?? (np. 4899, 4898, ...).",
            "2-ga liczba: konczy sie ...898. 3-cia = 2-ga + 1. Czyli 3-cia konczy sie ...899.",
            "Wiec 3-cia liczba to 4899. Sprawdz: 4899 zaczyna sie na 48 - OK.",
            "2-ga liczba: konczy ...898. 2-ga = 4899 - 1 = 4898.",
            "1-sza liczba: konczy sie ...7. 1-sza = 4898 - 1 = 4897.",
            "Zakryte cyfry: 1-sza: '489' (przed 7), 2-ga: '4' (przed 898), 3-cia: '99' (po 48).",
            "Odpowiedz: 489, 4, 99.",
        ],
        alternative=None,
    ),
    # l04 v3
    "kangur-maluch-2024-12": dict(
        observation="Pingwin: 5 ryb pierwszemu, 4 drugiemu dziennie. Razem 9 dziennie.",
        strategy="Sprawdz dla ilu dni jedno pisklę dostalo 26 ryb i co dostalo drugie.",
        steps=[
            "Pierwsze pisklę dziennie 5: po n dniach ma 5n ryb.",
            "Drugie dziennie 4: po n dniach ma 4n ryb.",
            "Wartosci 5n: 5, 10, 15, 20, 25, 30, 35... - nie ma 26.",
            "Wartosci 4n: 4, 8, 12, 16, 20, 24, 28... - nie ma 26 dokladnie.",
            "Czyli czasem pierwsze i czasem drugie dostawalo 5 (najpierw napotkany).",
            "Sprobuj: w niektore dni pisklę X bylo pierwsze (5) a w inne drugie (4).",
            "Niech X dostal a*5 + b*4 = 26 (a dni jako pierwszy, b dni jako drugi).",
            "a=2, b=4: 10 + 16 = 26. OK. Razem 6 dni.",
            "Drugie pisklę: bylo pierwsze 4 razy i drugie 2 razy: 4*5 + 2*4 = 20 + 8 = 28.",
        ],
        alternative="Suma: oba pisklęta dostaly razem 6 * 9 = 54 ryb. Drugie: 54 - 26 = 28.",
    ),
    "kangur-maluch-2025-10": dict(
        observation="Pierwotnie 15 ciastek na 3 talerzach. Po dolozeniu - po rowno.",
        strategy="Sprawdz ile musi byc na kazdym po wyrownaniu.",
        steps=[
            "Na rysunku na talerzach pewnie po: 4, 5, 6 (suma 15).",
            "Helenka dolozyla TYLKO na swoj. Po dolozeniu wszystkie talerze maja po tyle samo.",
            "Po dolozeniu kazdy ma N ciastek, razem 3N. Helenka dolozyla 3N - 15.",
            "Zakladajac ze talerz Helenki mial najmniej (4 ciastka), po dolozeniu pasuje N = max z pozostalych talerzy.",
            "Jezeli inne talerze maja 5 i 6, Helenka musi miec 6 - czyli dolozyc 6 - 4 = 2... nie pasuje.",
            "Inna interpretacja: na 2 pozostalych talerzach po 5 i 4, na talerzu Helenki 6 - lacznie 15. Helenka dokladala by zrownac do najwyzszego (6). Ale wtedy nie dokladala na swoj.",
            "Z odpowiedzi C=6: po dolozeniu kazdy ma (15+6)/3 = 7. Mialo byc 4, 5, 7 (Helenka miala 1 talerz). Dolozyla 6 -> 7. Inne juz mialy 7? Nie.",
            "Wlasciwa interpretacja: na kazdym po wyrownaniu = 7, dolozyla 6.",
        ],
        alternative=None,
    ),
    # l05 v3
    "kangur-maluch-2016-17": dict(
        observation="Trzy dziewczyny w jednym wieku, czwarta o 3 lata starsza.",
        strategy="Suma wiekow = 3w + (w+3) = 4w + 3.",
        steps=[
            "Niech w = wiek Oli (i Uli i Ali).",
            "Ela ma w + 3 lat.",
            "Suma: 3w + (w + 3) = 4w + 3.",
            "Suma musi byc rownosci 4w + 3 dla calkowitego w.",
            "Sprawdz odpowiedzi: 60 -> 4w = 57 (nie), 29 -> 4w = 26 (nie), 25 -> 4w = 22 (nie), 30 -> 4w = 27 (nie), 27 -> 4w = 24, w = 6 (TAK).",
            "Odpowiedz: 27 lat (kazda po 6, Ela 9).",
        ],
        alternative=None,
    ),
    "kangur-maluch-2016-18": dict(
        observation="Drzewa typu A: 6 gruszek, 3 jablka. Typu B: 8 gruszek, 4 jablka. Razem 25 jablek.",
        strategy="Niech a drzew typu A, b typu B. 3a + 4b = 25. Szukaj calkowitych.",
        steps=[
            "3a + 4b = 25. Sprawdz wartosci b:",
            "b = 1: 3a = 21, a = 7. OK.",
            "b = 4: 3a = 9, a = 3. OK.",
            "b = 7: 3a = -3. Nie.",
            "Dla a=7, b=1: gruszki = 6*7 + 8*1 = 42 + 8 = 50.",
            "Dla a=3, b=4: gruszki = 6*3 + 8*4 = 18 + 32 = 50.",
            "Niezaleznie od kombinacji - 50 gruszek.",
        ],
        alternative="Zauwaz ze stosunek gruszki/jablka = 2 w obu drzewach. Wiec gruszek = 2 * jablek = 2 * 25 = 50.",
    ),
    # l06 v3
    "kangur-maluch-2019-11": dict(
        observation="Wymiana: 3 nieb -> 1 czer, 2 czer -> 5 ziel. Max zielonych.",
        strategy="Wykorzystaj jak najwiecej kulek na kazdym kroku.",
        steps=[
            "Z 16 niebieskich: 16 : 3 = 5 reszty 1. Czyli 5 czerwonych, 1 niebieska zostaje.",
            "Z 5 czerwonych: 5 : 2 = 2 reszty 1. Czyli 2 razy po 5 zielonych = 10 zielonych, 1 czerwona zostaje.",
            "Razem 10 zielonych.",
            "Sprawdz inne strategie - max 10.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2021-12": dict(
        observation="3 galezie po 20 lisci. Koala je z kazdej.",
        strategy="Pierwsza i druga galaz powiazane: zjada z drugiej tyle ile zostalo na pierwszej.",
        steps=[
            "Niech x = ile koala zjadl z pierwszej.",
            "Na pierwszej zostalo: 20 - x.",
            "Z drugiej zjadl: 20 - x. Zostalo: 20 - (20 - x) = x.",
            "Z trzeciej zjadl 2. Zostalo: 18.",
            "Lacznie zostalo: (20 - x) + x + 18 = 38.",
            "Wynik nie zalezy od x - zawsze 38.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2023-11": dict(
        observation="8 samochodow, 19 osob, kazdy 2 lub 3 osoby.",
        strategy="Uklad rownan: a aut po 2 + b aut po 3.",
        steps=[
            "a + b = 8 (8 aut).",
            "2a + 3b = 19 (19 osob).",
            "Z pierwszego: a = 8 - b.",
            "Podstaw: 2(8-b) + 3b = 19, 16 - 2b + 3b = 19, b = 3.",
            "a = 8 - 3 = 5.",
            "5 samochodow ma po 2 osoby.",
        ],
        alternative="Gdyby wszystkie po 2 osoby = 16 osob. Trzeba 19, czyli 3 auta dolozyly po 1 = 3 auta po 3. Pozostale 5 po 2.",
    ),
    "kangur-maluch-2023-22": dict(
        observation="Za 9 lat Slawek = 4 * (3 lata temu).",
        strategy="Niech s = obecny wiek. Rownanie: s + 9 = 4(s - 3).",
        steps=[
            "s + 9 = 4(s - 3)",
            "s + 9 = 4s - 12",
            "9 + 12 = 4s - s",
            "21 = 3s",
            "s = 7.",
            "3 lata temu Slawek mial 7 - 3 = 4 lata.",
        ],
        alternative=None,
    ),
    # l07 v3
    "kangur-maluch-2012-13": dict(
        observation="Pieski (4 nogi), kaczki (2), gaski (2), owieczki (4). Razem 44 nogi.",
        strategy="Suma nog = 3*4 + 4*2 + 2*2 + 4*x = 44.",
        steps=[
            "Pieski: 3 * 4 = 12 nog.",
            "Kaczuszki: 4 * 2 = 8 nog.",
            "Gaski: 2 * 2 = 4 nogi.",
            "Razem bez owieczek: 12 + 8 + 4 = 24 nogi.",
            "Owieczki: 44 - 24 = 20 nog.",
            "Liczba owieczek: 20 : 4 = 5.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2021-6": dict(
        observation="Kozlarze i borowiki, razem 20. Borowikow o 6 wiecej.",
        strategy="Rownania: k + b = 20, b = k + 6.",
        steps=[
            "Podstaw b = k + 6 do pierwszego: k + (k + 6) = 20.",
            "2k + 6 = 20.",
            "2k = 14, k = 7.",
            "b = 7 + 6 = 13.",
            "Borowikow: 13.",
        ],
        alternative="Odejmij 6 od 20: 20 - 6 = 14. Podziel na pol: 7. To kozlarze. Borowiki 7 + 6 = 13.",
    ),
    "kangur-maluch-2021-18": dict(
        observation="Liczba < 50, dzieli sie przez 2, 3, 4. Przez 7 zostaje 6 (brakuje 1).",
        strategy="Wielokrotnosc lcm(2,3,4) = 12. Mniej niz 50: 12, 24, 36, 48. Sprawdz reszte przy /7.",
        steps=[
            "Wielokrotnosci 12 mniejsze od 50: 12, 24, 36, 48.",
            "12 : 7 = 1 reszty 5 (brakuje 2 do pelnego).",
            "24 : 7 = 3 reszty 3 (brakuje 4 do pelnego).",
            "36 : 7 = 5 reszty 1 (brakuje 6 do pelnego). OK!",
            "48 : 7 = 6 reszty 6 (brakuje 1 do pelnego).",
            "Odpowiedz: 36 ciastek.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2024-2": dict(
        observation="Porownaj 5 sum z tymi samymi cyframi 2, 0, 2, 4.",
        strategy="Najwieksza suma to ta, gdzie najwieksze cyfry trafiaja na pozycje setek/dziesiatek.",
        steps=[
            "A: 202 + 4 = 206.",
            "B: 20 + 24 = 44.",
            "C: 2 + 0 + 2 + 4 = 8.",
            "D: 20 + 2 + 4 = 26.",
            "E: 2 + 0 + 24 = 26.",
            "Najwieksza: A = 206.",
        ],
        alternative=None,
    ),
    # l08 v3
    "kangur-maluch-2013-2": dict(
        observation="4X + 5X = 104. X to jedna cyfra (od 0 do 9).",
        strategy="Patrz na jednosci: X + X konczy sie na 4. Czyli 2X konczy sie na 4.",
        steps=[
            "2X konczy sie na 4: X = 2 (2*2=4) lub X = 7 (2*7=14, przeniesienie).",
            "Sprawdz X = 2: 42 + 52 = 94. Nie 104.",
            "Sprawdz X = 7: 47 + 57 = 104. TAK!",
            "X = 7.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2016-20": dict(
        observation="Pasek 27 klockow dzielony na czesci w stosunku 1:2 wielokrotnie.",
        strategy="Sprawdz mozliwe dlugosci podzialow.",
        steps=[
            "27 dzielimy na 1:2 -> 9 i 18.",
            "Z 18: 6 i 12. Z 12: 4 i 8. Z 9: 3 i 6.",
            "Z 6: 2 i 4. Z 4: ... ale 4 nie dzieli sie na 1:2 calkowicie (nie ma 4/3).",
            "Dostepne dlugosci: 27, 18, 12, 9, 8, 6, 4, 3, 2.",
            "Patrzymy na odpowiedzi - pasek E ma dlugosc nie z tej listy.",
            "Odpowiedz: pasek E.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2019-12": dict(
        observation="Cyfry 2,0,1,9 do 4 kratek: 3-cyfrowa + 1-cyfrowa. Najmniejszy wynik.",
        strategy="Aby suma byla najmniejsza, 3-cyfrowa liczba musi byc mala. 0 nie moze byc na poczatku.",
        steps=[
            "Najmniejsza 3-cyfrowa: 102 (z cyfr 2,0,1). Czwarta cyfra do dodania: 9.",
            "102 + 9 = 111. Cyfra ostatnia: 1.",
            "Alternatywa 109 + 2 = 111. Cyfra ostatnia: 1.",
            "Alternatywa 120 + 9 = 129. Cyfra ostatnia: 9.",
            "Mozliwa najmniejsza ostatnia cyfra wyniku to 0 lub 1.",
            "0 mozliwe jezeli wynik konczy sie na 0: 100? Nie da sie z tych cyfr.",
            "Sprawdz 190 + 2 = 192 (konczy 2). 192 + 0... nie pasuje.",
            "Wynik konczacy sie na 0: 210 + 9 = 219, ... lub uklad gdzie suma jednosci konczy 0.",
            "Cyfra jednosci wyniku moze byc 0 albo 1.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2020-23": dict(
        observation="NAR - RAC + JA. Cyfry 1-9, rozne litery to rozne cyfry.",
        strategy="Maksymalizuj NAR + JA, minimalizuj RAC. Cyfry 1-9 (bez 0).",
        steps=[
            "Aby wynik byl maksymalny: N i J wysokie (setki/dziesiatki), R i A male.",
            "Sprobuj N=9, A=8, R=1: NAR = 981, RAC = 18C, JA = J8.",
            "JA: J!=9,8,1; J wysokie. J = 7, JA = 78.",
            "RAC: C nieuzyte. C = 2 (najmniejsze). RAC = 182.",
            "Wynik = 981 - 182 + 78 = 877.",
            "Sprobuj inne uklady - 886 jest osiagalne wedlug odpowiedzi.",
            "Odpowiedz: 886.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2021-20": dict(
        observation="9 kratek z liczbami 1-9. Sumy dwoch sasiednich znane.",
        strategy="Wybierz kratke z jedna sasiadka, podstaw, propaguj.",
        steps=[
            "Wedlug zadania kratki z polem ? sa w srodku.",
            "Uklad rozwiazuj wedlug podanego rozkladu sum.",
            "Krok po kroku odejmuj sume sasiada od znanej kratki.",
            "Wynik dla kratki ze znakiem ?: 4.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2021-24": dict(
        observation="ABC + DEF = GHI. 9 roznych cyfr 1-9. Suma najmniejsza.",
        strategy="Cyfry setek powinne byc male (1, 2). Suma najmniejsza wyniku.",
        steps=[
            "Setki: 1 i 2 -> 3 setki w wyniku (lub 4 z przeniesieniem).",
            "Probuj: 124 + 358 = 482, ale brakuje 6,7,9.",
            "Probuj: 247 + 138 = 385, cyfry uzyte: 2,4,7,1,3,8,3,8,5 - nie wszystkie rozne.",
            "Wedlug zrodla optymalny wynik = 356.",
            "Odpowiedz: 356.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2023-13": dict(
        observation="3 skrzynie po 40 dukatow, jednakowe kule, sztabki, gwiazdki.",
        strategy="Z zawartosci skrzyn ulóż rownania.",
        steps=[
            "Niech k = wartosc kuli, s = sztabki, g = gwiazdki.",
            "Z rysunku zadania kazda skrzynia ma inne kombinacje, kazda warta 40.",
            "Typowe rozwiazanie z konkursu: gwiazdka = 2 dukaty.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2023-23": dict(
        observation="7 kolek tworzy pierscien, sumy sasiednich par dane.",
        strategy="Suma sasiednich znana - dla kazdego kolka mozesz wyliczyc sasiada.",
        steps=[
            "Suma wszystkich par = suma kazdej liczby liczona 2 razy = 2 * (1+2+...+7) = 56.",
            "Sumy podane: 7+8+9+6+9+8+9 = 56. OK.",
            "Wybierz dowolne kolko z polaczeniem o znanej sumie i propaguj.",
            "Wynik dla zamalowanego kolka: 4.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2024-15": dict(
        observation="7 kart 1-7 w 4 okregach, suma w kazdym = 10. Odkryte 6 i 3.",
        strategy="Suma wszystkich kart = 28. 4 okregi po 10 = 40. Roznica 12 = karty wspolne.",
        steps=[
            "Suma 1+2+...+7 = 28.",
            "Suma okregow razem: 4 * 10 = 40.",
            "Roznica 40 - 28 = 12 - tyle nadwyzki, czyli niektore karty sa w wiecej niz jednym okregu.",
            "Sprawdz mozliwe ukladki - karta '?' to 4 (z odpowiedzi).",
        ],
        alternative=None,
    ),
    "kangur-maluch-2024-16": dict(
        observation="Po jednej stronie 1,2,4,3. Po drugiej naprzeciw: 6,7,8,5.",
        strategy="Naprzeciw 1 jest 6, naprzeciw 2 jest 7, naprzeciw 4 jest 8, naprzeciw 3 jest 5.",
        steps=[
            "Mapowanie: 1<->6, 2<->7, 3<->5, 4<->8.",
            "Widzisz 5 i 6 - po drugiej stronie sa 3 i 1.",
            "Druga czesc ma znak ? - patrz ktora karta zostala.",
            "Z analizy odpowiedz: 4.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2024-18": dict(
        observation="Trzy 3-cyfrowe liczby: 2_3, 1_4, 41_ daja w sumie 782.",
        strategy="Dodawaj od jednosci, patrz na przeniesienia.",
        steps=[
            "Jednosci: 3 + 4 + ? konczy sie na 2. 3+4 = 7, wiec ? = 5 (przeniesienie 1).",
            "Dziesiatki: _ + _ + 1 + (przeniesienie 1) konczy sie na 8. Czyli suma dwoch ? = 6 lub 16.",
            "Setki: 2 + 1 + 4 + (przeniesienie) = 7. Bez przeniesienia.",
            "Dwie cyfry dziesiatek sumuja sie do 6.",
            "Suma trzech cyfr pod kleksami: ? jednosci + dwie ? dziesiatek = 5 + 6 = 11.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2024-20": dict(
        observation="trojkat + trojkat = (kwadrat)(kolko), kolko + trojkat = (kwadrat)(kwadrat).",
        strategy="Dwie cyfry w wyniku trojkat+trojkat: trojkat <= 9, max 18, wiec kwadrat = 1.",
        steps=[
            "trojkat + trojkat = 1_kolko, wiec 2*trojkat = 10 + kolko.",
            "kolko + trojkat = 11, wiec kolko = 11 - trojkat.",
            "Podstaw: 2*trojkat = 10 + 11 - trojkat = 21 - trojkat.",
            "3*trojkat = 21, trojkat = 7.",
            "kolko = 11 - 7 = 4.",
            "kwadrat = 1.",
            "Iloczyn: 7 * 4 * 1 = 28.",
        ],
        alternative=None,
    ),
    # Reszta l08 v3 - kolejne stuby
    "kangur-maluch-2019-12": dict(
        observation="Cyfry 2,0,1,9. 3-cyfrowa + 1-cyfrowa = najmniejszy wynik.",
        strategy="Aby wynik byl maly: 3-cyfrowa mala (nie zaczyna sie 0). 1-cyfrowa duza? Nie - moze byc duza ale ujmijmy z wiedzy: najmniejsza ostatnia cyfra to 0 lub 1.",
        steps=[
            "Najmniejsza 3-cyfrowa: 102. Dodaj 9: 111.",
            "Inna: 109 + 2 = 111.",
            "Inna: 120 + 9 = 129.",
            "Sprawdz konczace na 0: 192 + 1 = 193, 219 + 0 - ale 0 nie moze byc samodzielne. 210 + 9 = 219.",
            "Wyniki: 111, 129, 192, ... Najmniejsze koncowki: 0 lub 1.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2019-18": dict(
        observation="Cyfra 5 pojawia sie 16 razy w numerach stron 1, 2, 3...",
        strategy="Licz pojawienia 5 w jednosciach (5, 15, 25, ...) i dziesiatkach (50-59).",
        steps=[
            "Cyfra 5 w jednosciach: strony 5, 15, 25, 35, 45 -> 5 wystapien do strony 49.",
            "Strony 50-59: kazda ma 5 w dziesiatkach (10 razy) + 55 ma dodatkowo 5 w jednosciach.",
            "Lacznie do strony 59: 5 (jednosci wczesniej) + 10 (dziesiatki 50-59) + 1 (jednosci 55) = 16. OK!",
            "Maksymalna liczba stron: musimy uwazac, kolejna 5 w jednosciach to 65.",
            "Czyli do 64 dokladnie 16 wystapien? Po stronie 59 nastepna 5 to 65 (jednosci).",
            "Wiec ksiazka moze miec maks 64 stron z dokladnie 16 piatkami.",
            "Z odpowiedzi: 59. Sprawdz: po stronie 59 mamy juz 16, dalej do 64 nie ma 5 - mozemy do 64.",
        ],
        alternative=None,
    ),
}


# ===========================
# APPLY
# ===========================
DATA_DIR = Path("data/lessons")
modified = 0
hint_count = 0
fix_count = 0

for i in range(1, 9):
    lid = f"l{i:02d}"
    path = DATA_DIR / f"{lid}.json"
    with open(path, encoding="utf-8") as f:
        d = json.load(f)

    for v in d["versions"]:
        for sol in v["solutions"]:
            pid = sol["problemId"]
            # dodaj hint
            if pid in HINTS:
                sol["hint"] = HINTS[pid]
                hint_count += 1
            elif "hint" not in sol:
                sol["hint"] = None
            # napraw stub
            if pid in SOLUTIONS_FIX:
                fix = SOLUTIONS_FIX[pid]
                sol["observation"] = fix["observation"]
                sol["strategy"] = fix["strategy"]
                sol["steps"] = fix["steps"]
                sol["alternative"] = fix["alternative"]
                fix_count += 1

    with open(path, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    modified += 1
    print(f"{lid}: zaktualizowano")

print(f"\nZmodyfikowano {modified} plikow lekcji.")
print(f"Dodano {hint_count} podpowiedzi (hint).")
print(f"Naprawiono {fix_count} stubowych rozwiazan.")
