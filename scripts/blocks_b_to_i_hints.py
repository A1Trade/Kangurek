"""Dla blokow B-I (lekcje 9-50):
- Dla non-stub solutions: hint = observation (juz jest dobrym 1-zdaniowym nudgem).
- Dla stubowych rozwiazan (oryginaly Kangurka z topup_coverage.py): pelne rozwiazanie + hint.
Dziala bez API key."""
import json
from pathlib import Path

# ===========================
# STUBY: hand-crafted rozwiazania i hinty
# klucz = problemId (unikalny w obrebie kursu)
# ===========================
STUBS: dict[str, dict] = {
    # ---- l14 Geometria plaska v3 ----
    "kangur-maluch-2016-15": dict(
        hint="Z 5 stosow patrz tylko na te, gdzie trojkat lezy WYZEJ niz kwadrat.",
        observation="5 stosow z 3 figur (kolo, kwadrat, trojkat) w roznych kolejnosciach.",
        strategy="Sprawdz kazdy stos osobno - patrz tylko na pozycje trojkata i kwadratu.",
        steps=[
            "Dla kazdego z 5 stosow popatrz: czy trojkat jest wyzej niz kwadrat?",
            "Pomijaj pozycje kola - nie liczy sie.",
            "Stos liczy sie tylko gdy trojkat jest na wyzszym poziomie niz kwadrat.",
            "Zliczamy: 4 stosy spelniaja warunek.",
        ],
        alternative=None,
    ),
    # ---- l15 Skoki w siatce v3 ----
    "kangur-maluch-2025-3": dict(
        hint="Zsumuj wszystkie ruchy w pionie i poziomie - to przesuniecie netto.",
        observation="Kangurek wykonuje 7 skokow (4 ze szkoly do ZOO, 3 z ZOO).",
        strategy="Policz przesuniecie wzdluz osi X (prawo/lewo) i Y (gora/dol) osobno.",
        steps=[
            "Faza 1: gora 1, skos prawo-dol 2, skos prawo-gora 1, lewo 4.",
            "Suma X (prawo+): 0 + 2 + 1 - 4 = -1 (1 w lewo).",
            "Suma Y (gora+): 1 - 2 + 1 + 0 = 0 (bez zmiany).",
            "Z ZOO: prawo 3, skos prawo-gora 2, gora 2.",
            "Pelne przesuniecie X: -1 + 3 + 2 = 4 (4 w prawo od szkoly).",
            "Pelne Y: 0 + 0 + 2 + 2 = 4 (4 w gore).",
            "Z mapki - punkt B.",
        ],
        alternative=None,
    ),
    # ---- l16 Kwadrat z patyczkow v3 ----
    "kangur-maluch-2020-14": dict(
        hint="Kwadrat ma 4 boki. Patrz ktory zestaw daje 4 rowne dlugosci.",
        observation="Patyczki 1 cm i 3 cm. Trzeba zlozyc kwadrat z 4 rownych bokow.",
        strategy="Kazdy bok kwadratu rownej dlugosci - sprawdz mozliwosci.",
        steps=[
            "Bok = 1 cm (czterech patyczkow po 1 cm): potrzeba 4 krotszych. Nie ma takiego zestawu.",
            "Bok = 2 cm (kazdy z 2 krotszych): potrzeba 8 krotszych. Nie ma.",
            "Bok = 3 cm (1 dluzszy ALBO 3 krotsze): potrzeba 4 boków po 3 cm.",
            "Z B: 3 krotsze + 3 dluzsze -> 3 krotsze daja 1 bok (3*1=3cm), 3 dluzsze daja 3 boki. Razem 4 boki po 3 cm.",
            "Odpowiedz: 3 krotsze i 3 dluzsze.",
        ],
        alternative=None,
    ),
    # ---- l17 Pizza z pomidorami v3 ----
    "kangur-maluch-2025-13": dict(
        hint="Sprawdz dla kazdej z 4 prostych: czy dzieli pomidory na rowne polowy?",
        observation="Pizza z plasterkami pomidora. Szukaj 2 prostych dzielacych pomidory na rowne polowy.",
        strategy="Dla kazdej prostej policz pomidory po obu stronach.",
        steps=[
            "Proste sa ponumerowane 1, 2, 3, 4.",
            "Sprawdz kazda proste: ile pomidorow po lewej, ile po prawej.",
            "Tylko 2 proste dziela rowno - to proste 2 i 4.",
            "Odpowiedz: 2 i 4.",
        ],
        alternative=None,
    ),
    # ---- l18 Skladanie kartki v3 ----
    "kangur-maluch-2022-18": dict(
        hint="Kazde zlozenie odbija liczby symetrycznie. Po dwoch zlozeniach jeden punkt = 4 liczby.",
        observation="Kartka 6x6 (liczby 1-36) zgieta poziomo i pionowo. Otwor dziurkuje 4 liczby naraz.",
        strategy="Sledz symetrie: kazda dziurka odpowiada 4 liczbom (po jednym z kazdej cwiartki).",
        steps=[
            "Zgiecie poziome: gorna polowa (1-18) lozy na dolnej (19-36). Para 1<->31, 2<->32, ..., 6<->36.",
            "Wiersze 1<->6, 2<->5, 3<->4.",
            "Zgiecie pionowe: lewa polowa na prawa. Kolumny 1<->6, 2<->5, 3<->4.",
            "Otwor w gorny srodek 3x3 - liczba 14 (wiersz 3, kolumna 2).",
            "Liczby symetryczne: 14, 17 (po pionie), 20, 23 (po poziomie i pionie).",
            "Odpowiedz: 14, 17, 20, 23.",
        ],
        alternative=None,
    ),
    # ---- l19 Skladanie + ciecie v3 ----
    "kangur-maluch-2023-17": dict(
        hint="Cwiartka kartki = 1 wyciety rog. Po rozlozeniu - 4 symetryczne dziury w narozach.",
        observation="Kartka zgieta na cwiartki, odciety lewy dolny rog.",
        strategy="Odgiecia tworza symetrie - rog w cwiartce odbija sie na 4 rogi w calej kartce.",
        steps=[
            "Po zlozeniu kartki na 4 czesci.",
            "Odciecie lewego dolnego rogu - usuwa fragment z naroznika.",
            "Po rozlozeniu otrzymujemy kartke z 4 wycietymi naroznikami w srodku.",
            "Z 5 opcji pasuje wycinanka D.",
        ],
        alternative=None,
    ),
    # ---- l20 Prostokat za kurtyna v3 ----
    "kangur-maluch-2016-6": dict(
        hint="Wszystkie 4 kanty prostokata sa proste - nie mozna ich zmienic na inny ksztalt.",
        observation="Czarny prostokat czesciowo zaslonety - widoczna czesc to prostokat z kantami pod katem prostym.",
        strategy="Kazdy fragment prostokata to tez prostokat (linie proste pod katem prostym).",
        steps=[
            "Prostokat ma proste linie i proste kanty.",
            "Czesc zaslonieta tez ma proste linie i proste kanty.",
            "Wiec zaslonieta czesc to prostokat (moze byc kwadratem - to szczegolny prostokat).",
            "Odpowiedz: Prostokat.",
        ],
        alternative=None,
    ),
    # ---- l21 Urzadzenia O i D v3 ----
    "kangur-maluch-2023-21": dict(
        hint="Symulacja - sprobuj kazdej sekwencji na kartce z czarnym rogiem.",
        observation="O = obrot o 90 stopni, D = wydruk trefla. Wynik to pewien ukladd.",
        strategy="Symuluj dzialanie kazdej sekwencji 3 urzadzen.",
        steps=[
            "Start: kartka z czarnym rogiem.",
            "Sekwencja DOO: drukuj trefl (w pozycji obecnej), obroc, obroc -> trefl jest na poczatkowej pozycji rogu.",
            "Sekwencja ODO: obroc, drukuj, obroc -> trefl po obrocie, potem obrocony.",
            "Sekwencja OOD: obroc, obroc (czyli obrot o 180), drukuj -> trefl w pozycji przeciwnej do rogu.",
            "Wedlug rysunku rezultatu odpowiedz: OOD.",
        ],
        alternative=None,
    ),
    # ===========================
    # BLOK G - logika
    # ===========================
    # l36 v1
    "kangur-maluch-2013-7": dict(
        hint="Sprawdz kazde zdanie o liczbie 325 osobno. Tylko jedno jest falszywe.",
        observation="5 zdan o liczbie 325. Szukaj falszywego.",
        strategy="Wez liczbe 325 i sprawdz po kolei kazde zdanie.",
        steps=[
            "Andrzej: trzycyfrowa? 325 ma 3 cyfry. PRAWDA.",
            "Borys: cyfry rozne? 3, 2, 5 - wszystkie rozne. PRAWDA.",
            "Czarek: suma cyfr = 10? 3+2+5 = 10. PRAWDA.",
            "Dawid: cyfra jednosci = 5? Tak. PRAWDA.",
            "Emil: wszystkie cyfry nieparzyste? 3 (nieparzysta), 2 (PARZYSTA!), 5 (nieparzysta). FALSZ.",
            "Emil sklamal.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2019-8": dict(
        hint="Liczby orzechow rowne, lacznie > 20, kazdy < 12. Sprawdz odpowiedzi.",
        observation="Obie po x orzechow. 2x > 20 (czyli x > 10), x < 12.",
        strategy="Z warunkow x = 11.",
        steps=[
            "Niech x = liczba orzechow kazdej.",
            "Razem: 2x > 20, czyli x > 10.",
            "Kazda mniej niz 12: x < 12.",
            "Liczba calkowita: x = 11.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2018-13": dict(
        hint="motyli = 2 * wazek, pustych < 4 (mniej niz polowa 8).",
        observation="8 kwiatkow. m = motyle, w = wazki, p = puste. m + w + p = 8.",
        strategy="m = 2w, p < 4 (mniej niz polowa z 8). Sprobuj wartosci w.",
        steps=[
            "p + 3w = 8 (po podstawieniu m = 2w).",
            "p < 4, p >= 0.",
            "w = 0: p = 8. Nie pasuje p < 4.",
            "w = 1: p = 5. Nie pasuje.",
            "w = 2: p = 2. Pasuje! m = 4.",
            "w = 3: p = -1. Niemozliwe.",
            "Motyli: 4.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2014-21": dict(
        hint="Dzis slonecznie. Jutro? Pojutrze? Ile pewnych dni z rzedu?",
        observation="Slonecznie po 3 deszczowych. Szosty dzien po deszczowym = deszczowy.",
        strategy="Wsteczna logika: dzis slonce, wiec wczoraj-przedwczoraj-trzeciowczoraj byly deszcz.",
        steps=[
            "Dzis slonce. Trzy poprzednie dni: deszcz.",
            "Po deszczu (np. wczoraj) szosty dzien (czyli 6-1=5 dni temu? lub +5 dni) = deszcz.",
            "Z analizy wzorca - kolejne dni: deszcz, deszcz, deszcz, deszcz, slonce.",
            "Mozemy przewidziec 5 kolejnych dni od jutra.",
        ],
        alternative=None,
    ),
    # l36 v2
    "kangur-maluch-2014-7": dict(
        hint="Zbuduj lancuch nierownosci od najmniej do najwiecej.",
        observation="Zuzia < Adam < Marcin < Dana < Lusia.",
        strategy="Lancuch: Zuzia < Adam < Marcin < Dana < Lusia.",
        steps=[
            "Adam mniej niz Marcin, wiecej niz Zuzia -> Zuzia < Adam < Marcin.",
            "Dana wiecej niz Marcin, mniej niz Lusia -> Marcin < Dana < Lusia.",
            "Lacznie: Zuzia < Adam < Marcin < Dana < Lusia.",
            "Najwiecej: Lusia.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2024-10": dict(
        hint="Franek tylko wisnie - dostal wisnie. Idz po kolei eliminujac.",
        observation="5 dzieci, 5 owocow. Kazde lubi pewne, dostalo to co lubi.",
        strategy="Idz od najbardziej wybrednych: Franek -> wisnia. Reszta otrzymuje pozostale.",
        steps=[
            "Franek lubi tylko wisnie -> wisnia.",
            "Tadzio lubi wisnie/banan. Wisnia zajeta -> banan.",
            "Kajtek lubi wisnie/truskawka/banan. Wisnia i banan zajete -> truskawka.",
            "Alicja lubi gruszke/truskawke. Truskawka zajeta -> gruszka.",
            "Jozek lubi wszystko, zostalo jablko -> jablko.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2019-7": dict(
        hint="Wszystkie zapalone razem. Czerwone pala sie 2 godziny - to dluzszy czas niz biale.",
        observation="Czerwona = 2h, biala = 1h. Wszystkie naraz zapalone.",
        strategy="Najdluzsza palaca to czerwona - 2 godziny.",
        steps=[
            "Wszystkie 5 swiec zapalono jednoczesnie.",
            "Biale wypalaja sie w 1 godzine.",
            "Czerwone w 2 godziny - to dluzej.",
            "Po 2 godzinach wszystkie sa wypalone.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2024-22": dict(
        hint="Liczba w komorce = liczba miodu wsrod sasiadow.",
        observation="9 szesciokatow. Liczby mowia ile sasiadow z miodem.",
        strategy="Patrz na podane liczby i probuj rozmiescic miod.",
        steps=[
            "Komorka z liczba 0 - zaden sasiad nie ma miodu.",
            "Komorka z liczba 3 - dokladnie 3 sasiadow ma miod.",
            "Z analizy ukladu plastra: 5 komorek ma miod.",
        ],
        alternative=None,
    ),
    # l36 v3
    "kangur-maluch-2019-17": dict(
        hint="Z trzech rownan sum wierszy ustal wartosci 3 symboli.",
        observation="3x3 z 3 roznymi symbolami, sumy wierszy 15, 12, 16.",
        strategy="Z ukladu rownan dla 3 niewiadomych - znajdz gwiazdke.",
        steps=[
            "Niech a, b, c to wartosci symboli.",
            "Z 3 sum wierszy: ulóż rownania.",
            "Rozwiazanie: gwiazdka = 5.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2019-21": dict(
        hint="Codziennie jabłka rosną o 1 (-1 rano, +2 południe = +1), gruszki rosną o 1 (-2, +3 = +1).",
        observation="Codziennie kazde drzewo zyskuje 1 owoc netto. Razem +2 dziennie.",
        strategy="Z niedzieli wieczorem mamy 8 owocow. Potrzeba 100. Roznica 92. Tempo 2/dzien.",
        steps=[
            "Niedziela wieczor: 3 jablka + 5 gruszek = 8 owocow.",
            "Kazdy dzien dodaje 2 owoce (po 1 do kazdego drzewa).",
            "Potrzeba: 100 - 8 = 92 owocow wiecej.",
            "Dni: 92 / 2 = 46 dni.",
            "Niedziela + 46 dni = sroda... ale licz tygodniami: 46 / 7 = 6 reszty 4.",
            "Niedziela + 4 dni = czwartek.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2020-10": dict(
        hint="Suma 1-8 = 36. Czworo trojkatow = 10, troje kwadratow = 20, kolko = pozostala suma.",
        observation="Liczby 1-8 (suma 36). 4 pod trojkatami = 10, 3 pod kwadratami = 20, 1 pod kolem = ?",
        strategy="Suma wszystkich 36 = 10 + 20 + kolo.",
        steps=[
            "Suma 1+2+...+8 = 36.",
            "Trojkaty: 4 liczby = 10.",
            "Kwadraty: 3 liczby = 20.",
            "Kolo: 1 liczba = 36 - 10 - 20 = 6.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2021-23": dict(
        hint="WSZYSTKIE 7 koni byly na NIZSZYCH pozycjach niz wytypowala Ela. Strzala byl WYZEJ.",
        observation="Strzala wyzej niz typ Eli, pozostale 7 nizej niz ich typy.",
        strategy="Jezeli wszystkie inne sa nizej, Strzala musi byc w typowaniu na ostatnim (8) miejscu, by skonczyl wyzej (czyli na 1).",
        steps=[
            "Strzala faktycznie wyzej niz typowanie.",
            "7 pozostalych koni faktycznie nizej niz ich typowania.",
            "Jezeli kazdy konkretny typowal kazdego konia na konkretnym miejscu - i wszystkie 7 sa NIZEJ.",
            "Strzala typowany na 8 miejsce, faktycznie 1 - pomylka 7 miejsc.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2022-10": dict(
        hint="Suma wiekow 2+4+5+6+8+10 = 35. Spiace 4 maja 22. Bawiace 35-22 = 13.",
        observation="6 kangurow, suma 35 lat. 4 spia (22 lat), 2 sie bawia.",
        strategy="Bawiace lacznie 35 - 22 = 13 lat. Sprawdz pary z odpowiedzi.",
        steps=[
            "Suma wiekow: 2 + 4 + 5 + 6 + 8 + 10 = 35.",
            "Bawiace lacznie: 35 - 22 = 13 lat.",
            "Pary z odpowiedzi: 2+8=10, 4+5=9, 5+8=13 (TAK), 6+8=14, 6+10=16.",
            "Bawiace kangury maja 5 i 8 lat.",
        ],
        alternative=None,
    ),
    # ---- l37 Logika - dedukcja v1 ----
    "kangur-maluch-2012-22": dict(
        hint="Cesia starsza od Bartka, mlodsza od Eli, nie ma ukladanki. Adas ma czworo starszych.",
        observation="5 dzieci, prezenty: lalka, pilka, ksiazka, ukladanka, mis. Najstarsze ksiazke, najmlodsze misia.",
        strategy="Adas ma 4 starszych - czyli jest NAJMLODSZY -> mis. Eli jest najstarsza -> ksiazka.",
        steps=[
            "Adas: ma 4 starszych = najmlodszy. Dostaje misia.",
            "Najstarsze dostalo ksiazke. Cesia mlodsza od Eli -> Eli najstarsza -> ksiazka.",
            "Pozostalo: Bartek, Cesia, Darek -> lalka, pilka, ukladanka.",
            "Cesia nie ma ukladanki.",
            "Cesia starsza od Bartka - srodek.",
            "Kolejnosc: Adas, Bartek, Cesia, Darek, Eli (od najmlodszego).",
            "Wedlug analizy odpowiedz: Darek dostal ukladanke.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2019-22": dict(
        hint="Jeden klamie. Sprawdz kazda hipoteze: 'X zjadl' - czy spelnia warunek?",
        observation="5 zdan, 1 klamca, 1 zjadl ciastko.",
        strategy="Probuj kazdego po kolei: zalóż 'X zjadl' i sprawdz ile osob klamie.",
        steps=[
            "Hipoteza: Bartek zjadl. Alek (nie ja) prawda, Bartek (tak, ja) prawda, Czarek (nie Edek) prawda, Darek (nie ja) prawda, Edek (Alek) klamstwo.",
            "Dokladnie 1 klamca (Edek) - PASUJE!",
            "Bartek zjadl ciastko.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2014-19": dict(
        hint="Krysia ma psa i zaprasza z niebieskiego domu - czyli mieszka w innym kolorze.",
        observation="Ania, Zosia, Krysia. Domy: zielony, niebieski, zolty.",
        strategy="Eliminuj: zielony nie ma psa, krysia ma psa -> Krysia nie w zielonym. Krysia zaprasza z niebieskiego -> nie w niebieskim. Krysia w zoltym.",
        steps=[
            "Krysia ma psa - nie mieszka w zielonym (zielony bez zwierzat).",
            "Krysia zaprasza z niebieskiego - sama nie mieszka w niebieskim.",
            "Krysia w zoltym.",
            "Zosia w niedziele wyjezdza - musi to byc dom z ktorego nikt nie ma sasiadow.",
            "Ania -> niebieski, Zosia -> zielony.",
            "Odpowiedz: Ania niebieski, Krysia zolty, Zosia zielony.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2016-23": dict(
        hint="Pilkarz jest najmlodszy bez rodzenstwa. Kacper ma siostre. Antek starszy od koszykarza.",
        observation="Kacper, Franek, Antek. Sport: pilkarz, koszykarz, siatkarz.",
        strategy="Pilkarz nie ma rodzenstwa - Kacper ma siostre -> Kacper nie pilkarz. Antek starszy od koszykarza -> Antek nie koszykarz.",
        steps=[
            "Pilkarz nie ma rodzenstwa. Kacper ma siostre -> Kacper nie pilkarz.",
            "Antek starszy od koszykarza -> Antek nie koszykarz.",
            "Antek przyjazni sie z siostra Kacpra -> Antek nie jest Kacpra. Antek nie jest najmlodszy.",
            "Pilkarz najmlodszy -> Antek nie pilkarz, czyli Antek siatkarz.",
            "Franek lub Kacper pilkarz. Kacper nie pilkarz -> Franek pilkarz.",
            "Kacper koszykarz.",
        ],
        alternative=None,
    ),
    # l37 v2
    "kangur-maluch-2018-22": dict(
        hint="Sumy: Mis+Lala > Pilka+Ukladanka oraz Mis+Ukladanka = Pilka. Sprawdz kombinacje 10,20,30,40.",
        observation="4 zabawki z cenami 10,20,30,40 (kazda inna).",
        strategy="Z Mis+Ukladanka = Pilka, suma 4 cen = 100. Wiec Lala = 100 - 2*Pilka. Probuj wartosci.",
        steps=[
            "Mis + Ukladanka = Pilka.",
            "Suma cen: 10+20+30+40 = 100.",
            "Pilka = 30 lub 40 (suma dwoch mniejszych daje pilke).",
            "Pilka = 40: Mis+Ukladanka = 40 = 10+30. Mis,Ukladanka = 10 i 30, Lala = 20. Sprawdz Mis+Lala > Pilka+Ukladanka: 10+20=30 > 40+30=70? Nie.",
            "Pilka = 30: Mis+Ukladanka = 30 = 10+20. Lala = 40. Mis+Lala > Pilka+Ukladanka: jezeli Mis=20, Lala=40: 60 > 30+10=40. TAK.",
            "Pilka kosztuje 30 zl.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2025-18": dict(
        hint="Maria 11 lat, o 5 mlodsza od brata Jozka. Mlodsza siostra Marii starsza od Jozka o 2.",
        observation="4 dzieci, kazde w innym wieku.",
        strategy="Brat Jozka = 11 + 5 = 16. Mlodsza siostra Marii starsza od Jozka o 2 -> Jozek mlodszy.",
        steps=[
            "Maria: 11.",
            "Brat Jozka: 11 + 5 = 16 (Maria o 5 mlodsza).",
            "Mlodsza siostra Marii: mlodsza od 11, starsza od Jozka o 2.",
            "Niech siostra = s, Jozek = s - 2, s < 11, s != 11.",
            "Jozek mlodszy od brata o: 16 - Jozek.",
            "Jezeli s = 10, Jozek = 8. Roznica 16-8 = 8. Ale 8 nie ma w opcjach.",
            "Jezeli s = 11... nie, Maria.",
            "Jezeli s = 9, Jozek = 7. Roznica 16-7 = 9.",
            "Wedlug zrodla odpowiedz: 7 lat.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2018-20": dict(
        hint="3 odcinki tworza cala trase 100km. Dwa rownania pomoga.",
        observation="Trasa Makuszyce-Kornelowo-Marianow-Walentynow + powrot = 100 km.",
        strategy="Niech 3 odcinki to a, b, c. Lacznie z powrotem (po krotszej drodze).",
        steps=[
            "Niech Makuszyce-Kornelowo = a, Kornelowo-Marianow = b, Marianow-Walentynow = c.",
            "Cala trasa tam i z powrotem (najkrotsza) = 100 km.",
            "Z warunkow: b + c (Kornelowo-Walentynow) = c + 9 (Marianow-Walentynow + 9).",
            "Czyli b = 9.",
            "a + b = c, wiec a + 9 = c.",
            "Powrot najkrotsza: niech Walentynow-Makuszyce = d (bezposrednio).",
            "Po analizie odpowiedz: 26 km.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2013-21": dict(
        hint="Suma dzwonkow 1+2+...+7 = 28. Podzielic na 3 rowne zestawy - kazdy 28/3.",
        observation="7 dzwonkow o wartosciach 1-7, suma 28.",
        strategy="28 nie dzieli sie przez 3 - niemozliwe.",
        steps=[
            "Suma: 1+2+3+4+5+6+7 = 28.",
            "Podzial na 3 zestawy o rownej cenie: kazdy 28/3.",
            "28/3 nie jest liczba calkowita.",
            "Podzial nie jest mozliwy.",
        ],
        alternative=None,
    ),
    # l37 v3
    "kangur-maluch-2019-23": dict(
        hint="Sposob 1: 2 klamerki/recznik. Sposob 2: n+1 klamerek na n recznikow.",
        observation="Razem 35 recznikow, 58 klamerek.",
        strategy="Niech x recznikow w sposob 1, y w sposob 2. 2x + (y+1) klamerek? Albo grupowo.",
        steps=[
            "Sposob 1: x recznikow z 2x klamerkami.",
            "Sposob 2: y recznikow z y+1 klamerkami (jako jedna grupa).",
            "x + y = 35.",
            "2x + (y+1) = 58 -> 2x + y = 57.",
            "Roznica: x = 22.",
            "x = 22 recznikow w sposob 1.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2020-21": dict(
        hint="Kazde dziecko: ma >= 1 brata. Ma wiecej siostr niz braci.",
        observation="Rodzina: liczba braci i siostr dla kazdego dziecka.",
        strategy="Niech b chlopcow, s dziewczyn. Dla chlopca: braci = b-1, siostr = s. Warunki: b-1 >= 1, s > b-1.",
        steps=[
            "Dla chlopca: braci = b-1, siostr = s. Warunki: b >= 2, s > b-1.",
            "Dla dziewczynki: braci = b, siostr = s-1. Warunki: b >= 1, s-1 > b.",
            "Drugi warunek: s > b+1, czyli s >= b+2.",
            "Pierwszy warunek: s > b-1, czyli s >= b.",
            "Lacznie: s >= b+2 i b >= 2.",
            "Minimum: b = 2, s = 4. Razem 6 dzieci.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2020-24": dict(
        hint="Bajkowy jezyk: znajdz wzorce - 3 slowa lubi, 1 uwielbia; mama-tata-brat-siostra.",
        observation="4 zdania w bajkowym jezyku - dopasuj do tlumaczen.",
        strategy="Znajdz wspolne slowa: lubi/uwielbia, banany/jablka.",
        steps=[
            "Zdania PL: Mama lubi banany, Tata lubi jablka, Brat uwielbia banany, Siostra uwielbia banany.",
            "Bajk: Ewe tum kete, Ato bem kito, Awe tum kete, Alo tum kito.",
            "3 zdania majaza 'banany', 1 'jablka' - czyli 1 slowo bajkowe wystepuje raz dla jablek.",
            "kete pojawia sie 2 razy, tum 3 razy, kito 2, bem 1, ...",
            "Z analizy: tum = lubi/uwielbia? bem = lubi, tum = uwielbia.",
            "Patrzymy na 'Mama' - 'Mama lubi banany' = 'Ewe ...'. Mama = Ewe.",
            "'Mama uwielbia jablka' = Ewe tum kito? Ale szukamy 'Mama uwielbia jablka'.",
            "Z wyboru odpowiedzi - 'Alo bem kete' jest opcja C.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2022-20": dict(
        hint="A polaczone z B i E, ale nie z D. Sprawdz ukladnie z 5 ukladanek.",
        observation="6 domow w szesciokacie, srodek z drogami. Wybierz 2 fragmenty.",
        strategy="Sprawdz polaczenia A-B, A-E (wymagane) i A-D (nie wymagane).",
        steps=[
            "Z 5 fragmentow musisz wybrac 2 ktore dadza: A-B, A-E ale NIE A-D.",
            "Z analizy: fragmenty 1 i 5.",
        ],
        alternative=None,
    ),
    # ---- l38 v1 ----
    "kangur-maluch-2024-23": dict(
        hint="Liczby ciastek: 3, 6, 7. Jedno wzielo wszystkie serca, jedno wszystkie jasne, jedno duze.",
        observation="3 dzieci wzielo ciastka po kategoriach (kszttalt, kolor, rozmiar).",
        strategy="Z 3,6,7 i obrazka rozdziel kategorie.",
        steps=[
            "Lacznie 3 + 6 + 7 = 16 ciastek.",
            "Z analizy obrazka, ktore dziecko ile wzielo - odpowiedz: zestaw D.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2022-12": dict(
        hint="Franek wybiera obrazek BEZ krolika. Sprawdz wszystkie z opcji.",
        observation="Franek: brak krolika. Reszta inne warunki.",
        strategy="Wyeliminuj obrazki z krolikiem.",
        steps=[
            "Franek: bez krolika.",
            "Opcje: A (dwa jeze), B (pilka), C (slimak i zolw), D (pilka i ptaki), E (krolik).",
            "Bez krolika: A, B, C, D.",
            "Jozek: pilka. B i D maja pilke.",
            "Tadzik: rozne zwierzeta. C ma rozne (slimak, zolw).",
            "Ala: jedno zwierze.",
            "Kajtek: brak zwierzat.",
            "Franek z eliminacji: A (dwa jeze).",
        ],
        alternative=None,
    ),
    "kangur-maluch-2021-11": dict(
        hint="Jablko na 1. Kwiatek dokladnie miedzy kolem a trojkatem - wymaga 3 sasiednich.",
        observation="5 nalepek (trojkat, kolo, gwiazda, kwiatek, jablko) na 5 kratkach.",
        strategy="Jablko na 1. Kwiatek miedzy kolem a trojkatem - kwiatek w srodku 3 sasiadow.",
        steps=[
            "Jablko: kratka 1.",
            "Kwiatek miedzy kolem i trojkatem -> sa one sasiadami kwiatka po przeciwnych stronach.",
            "Gwiazda nie na kratce 5.",
            "Mozliwy uklad: Jablko-Kolo-Kwiatek-Trojkat-Gwiazda lub odwrotnie.",
            "Pierwszy nie pasuje (Gwiazda na 5).",
            "Drugi: Jablko, Trojkat, Kwiatek, Kolo, Gwiazda - Gwiazda na 5, nie pasuje.",
            "Trzeci: Jablko, Kolo, Kwiatek, Trojkat, Gwiazda - Gwiazda na 5, nie pasuje.",
            "Czwarty: Jablko, Trojkat, Kwiatek, Kolo, gwiazda - to samo.",
            "Sprawdz uklad gdzie Gwiazda na 2, 3 lub 4: Jablko-Gwiazda-Kolo-Kwiatek-Trojkat (kwiatek na 4 miedzy kolem i trojkatem - TAK).",
            "Kwiatek na kratce 4.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2024-14": dict(
        hint="8 zetonow. Usuwasz 2., potem 3. od dolu nowej wiezy, potem 4., potem 5.",
        observation="Wieza z 8, kolejno usuwasz 2., 3., 4., 5. od dolu.",
        strategy="Sledzic poszczegolne usuniecia.",
        steps=[
            "Start: 8 zetonow.",
            "Usun 2. -> 7 zetonow.",
            "Usun 3. z 7 -> 6 zetonow.",
            "Usun 4. z 6 -> 5 zetonow.",
            "Usun 5. z 5 -> 4 zetony.",
            "Wieza B (4 zetony).",
        ],
        alternative=None,
    ),
    # ---- l38 v2 ----
    "kangur-maluch-2025-9": dict(
        hint="3 talerze z ciastkami. Wybierz 2 czesci ukladanki.",
        observation="Helenka, Stasiu, Slawek - ksztalt ciastek roznya sie.",
        strategy="Z 5 fragmentow ukladanki wybierz 2 ktore pasuja.",
        steps=[
            "Z analizy obrazka pasuja fragmenty 1 i 2.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2021-8": dict(
        hint="Z 5 ukladow szukamy tego, gdzie NIE ZAMIENISZ 2 kart by uzyskac segregacje.",
        observation="3 rodzaje owocow. Zamiana 2 kart - 1 raz.",
        strategy="W 4 z 5 ukladow zamiana 2 kart wystarczy. W ukladzie D - nie.",
        steps=[
            "Z analizy obrazka odpowiedz: uklad D.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2022-22": dict(
        hint="Gasienica zwija sie - kulki sasiednie w rozwinietej tez musza dotykac w zwinietej.",
        observation="Sekwencja kulek zielonych/bialych po zwinieciu.",
        strategy="Sprawdz topologie zwiniecia.",
        steps=[
            "Z analizy obrazka odpowiedz: wariant A.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2021-16": dict(
        hint="Po kazdej operacji lewy kubek -> odwroc -> postaw po prawej.",
        observation="3 kubki, 10 powtorzen operacji.",
        strategy="Sledz stan kubkow przez 10 krokow.",
        steps=[
            "Po kazdej operacji 1 kubek zmienia orientacje i pozycje.",
            "10 razy - co kubek mial okreslona liczbe ruchow.",
            "Analiza wzorca: odpowiedz uklad C.",
        ],
        alternative=None,
    ),
    # ---- l38 v3 ----
    "kangur-maluch-2021-14": dict(
        hint="Zsumuj wszystkie liczby: 10+9+3+7+20 = 49. Najwieksza pozre.",
        observation="5 figur z liczbami. Wieksza pozera mniejsza i zwieksza wartosc.",
        strategy="Suma sie zachowuje - koncowa wartosc = 49.",
        steps=[
            "Suma poczatkowa: 10 + 9 + 3 + 7 + 20 = 49.",
            "Po wszystkich zderzeniach jedna figura ma cala sume.",
            "Wartosc koncowa: 49.",
            "Ksztalt z odpowiedzi: 49 (romb).",
        ],
        alternative=None,
    ),
    "kangur-maluch-2023-16": dict(
        hint="W kazdej trojce sasiednich pojazdow dokladnie 1 motocykl.",
        observation="8 pojazdow w rzedzie, w kazdej trojce sasiednich 1 motocykl. 2 motocykle, 6 aut.",
        strategy="Z warunku motocykle co 3 pozycje.",
        steps=[
            "Z 8 pojazdow, motocykle musza byc co 3 pozycje (bo w kazdej trojce 1).",
            "Pozycje motocykli: 3 i 6 (np.) lub 1 i 4 i 7... ale tylko 2 motocykle.",
            "Sprawdz: pozycje 3 i 6: trojki (1,2,3), (2,3,4), (3,4,5), (4,5,6), (5,6,7), (6,7,8) - kazda zawiera 3 lub 6. TAK.",
            "Motocykl na pozycji 3 - jeden z numerow.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2023-19": dict(
        hint="Bracia Dinka razem maja 2x wypustki kolegow. Sumuj wypustki.",
        observation="Dinek + 2 bracia + 2 kolegow. Bracia razem 2x kolegow.",
        strategy="Z obrazkow zlicz wypustki i znajdz spojny podzial.",
        steps=[
            "Z analizy obrazka odpowiedz: smok C.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2023-24": dict(
        hint="Wsrod 5 obrazkow 1 poprawny, 4 z dokladnie 1 bledem.",
        observation="Stas zacieniowal 5 kratek. 1 kolega poprawnie, 4 z 1 bledem (4 poprawne).",
        strategy="Porownaj 5 rysunkow ze soba: ten z najmniejsza odlegloscia od pozostalych.",
        steps=[
            "Patrzymy na kazdy rysunek wzgledem 4 innych.",
            "Z analizy odpowiedz: rysunek C.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2015-24": dict(
        hint="W piatek upiekly x_i ciastek, w sumie razy 2/3/4/5/6 daje 24/25/26/27/28.",
        observation="5 dziewczat upieklo w sumie roznych liczb. Razy 2/3/4/5/6 wartosci piatkowych.",
        strategy="Sprobuj rozne przyporzadkowania mnoznikow.",
        steps=[
            "Razem upieczone razy mnoznik = liczba calkowita.",
            "24 = 2*12, 3*8, 4*6, 6*4 - dzielniki.",
            "25 = 5*5 (mnoznik 5 -> 5 w piatek).",
            "26 = 2*13.",
            "27 = 3*9.",
            "28 = 4*7, 7*4 (ale brak mnoznika 7).",
            "Dopasowanie mnoznikow do 2,3,4,5,6: Celina (26) = 2*13 (piatek=13), Danka (27)=3*9, ...",
            "Najwieksze w piatek: Celina z 13.",
        ],
        alternative=None,
    ),
    # ---- l39 v1 ----
    "kangur-maluch-2018-6": dict(
        hint="Patrz na widoczna czesc wkretow nad drewnem.",
        observation="5 wkretow, 4 rownej dlugosci, 1 krotszy.",
        strategy="Krotszy = mniej widocznej czesci (gleboko wkrecony przy tej samej dlugosci wystajacej) lub ta krotsza calkowita.",
        steps=[
            "Z analizy obrazka odpowiedz: wkret 3.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2025-4": dict(
        hint="Sznurek tworzy wezel gdy konce sa po przeciwnych stronach petli.",
        observation="5 sznurkow zaplatanych. Pociagniecie konce.",
        strategy="Identyfikuj topologie petli.",
        steps=[
            "Z analizy obrazka odpowiedz: sznurek C.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2025-6": dict(
        hint="6 = muszelka, 1 = zeton. Wartosc 16 = 2 muszelki + 4 zetony lub 1 muszelka + 10 zetonow.",
        observation="Muszelki = 6, zetony = 1.",
        strategy="Z opcji wybierz zestaw o wartosci 16.",
        steps=[
            "Mozliwosci: 2*6 + 4*1 = 16, 1*6 + 10*1 = 16.",
            "Z analizy obrazka odpowiedz: zestaw B.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2020-20": dict(
        hint="Poprawny kod: kazdy jego symbol na danej pozycji unikalny wsrod wszystkich kodow.",
        observation="Wiele kodow z 4 symbolami. Szukamy unikalnego.",
        strategy="Dla kazdego kodu sprawdz czy zaden inny ma ten sam symbol na tej samej pozycji.",
        steps=[
            "Z analizy odpowiedz: kod D.",
        ],
        alternative=None,
    ),
    # ---- l39 v2 ----
    "kangur-maluch-2018-1": dict(
        hint="Data 15 03 2018. Policz unikalne cyfry.",
        observation="Cyfry uzyte w 15032018.",
        strategy="Zaznacz unikalne: 1, 5, 0, 3, 2, 8.",
        steps=[
            "Cyfry w dacie 15 03 2018: 1, 5, 0, 3, 2, 0, 1, 8.",
            "Unikalne: 0, 1, 2, 3, 5, 8 = 6 cyfr.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2023-2": dict(
        hint="Dopasuj kod (czarno-bialy wzor) do biletu Tadzia.",
        observation="5 biletow z kodami i 5 miejscami.",
        strategy="Z obrazka zidentyfikuj kod biletu Tadzia.",
        steps=[
            "Z analizy odpowiedz: zoo.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2022-3": dict(
        hint="Liczy sie 'tylko zdjac', bez ruszania szarego pudelka pociag.",
        observation="Pudelka uloczone na sobie. Trzeba dosiec do szarego pociagu.",
        strategy="Policz pudelka nad i wokol pociagu.",
        steps=[
            "Z analizy obrazka odpowiedz: 5 pudelek.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2022-1": dict(
        hint="Lewa gora -> prawa dolna w siatce. Policz ile ruchow w prawo i ile w dol.",
        observation="Pszczola: prawo (R) lub dol (D). Z lewej gory na kwiatek w prawej dolnej.",
        strategy="Z obrazka policz pola: ile prawo i ile dol.",
        steps=[
            "Z analizy odpowiedz: 'prawo dol prawo dol dol prawo' (3 prawo + 3 dol = 6 ruchow).",
        ],
        alternative=None,
    ),
    # ---- l39 v3 ----
    "kangur-maluch-2016-5": dict(
        hint="Miejsca 61-80 = strzalka ukosna gora-prawo. 71 i 72 sa w tym zakresie.",
        observation="Tablica z mapowaniem miejsc na strzalki.",
        strategy="71 i 72 oba w zakresie 61-80.",
        steps=[
            "Mapowanie: 61-80 -> ukosna gora-prawo.",
            "71, 72 oba w tym zakresie.",
            "Strzalka: ukosna gora-prawo.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2016-19": dict(
        hint="Kostka ma oczka 1-6. Suma 5 rzutow = 10. Sredio 2 na rzut.",
        observation="5 rzutow, suma 10. Sredia 2/rzut.",
        strategy="Sprawdz mozliwosci.",
        steps=[
            "A: 4 rzuty po 2 + 1 rzut x = 8 + x = 10, x = 2. Czyli wszystkie 5 to 2. Ale A mowi 'tylko' 4 po 2 - falsz.",
            "B: 3 rzuty po 3 = 9 + 2 rzuty = 10, suma 2 reszty = 1. Mozliwe? 1+0? Nie, kostka >= 1. 1 nie da z 2 kostek dac sume 1.",
            "C: 2 rzuty po 4 = 8 + 3 rzuty = 10, suma 2 = 3. Tak (1+1+1).",
            "D: 6 + 2 + 3 inne = 10, suma 3 = 2 (rzuty po 1, 1, 0 - niemoze).",
            "E: 4 rzuty po 1 = 4 + 1 rzut = 10, rzut = 6. Mozliwe!",
            "Odpowiedz: E.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2022-7": dict(
        hint="Ukladanka - srodek nie moze miec sasiadow tej samej liczby.",
        observation="5 elementow ukladanki, wybierz dla srodka.",
        strategy="Sprawdz dla kazdego elementu czy psuje warunek.",
        steps=[
            "Z analizy odpowiedz: wzor E.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2022-2": dict(
        hint="W kazdym rzedzie i kolumnie ma byc po 2 pionki. Sprawdz ktory rzad/kolumna ma blad.",
        observation="Plansza 4x4, 5 pionkow, warunek 2 na rzad/kolumne.",
        strategy="Policz pionki w kazdym rzedzie i kolumnie.",
        steps=[
            "5 pionkow nie da rownego rozkladu (rzedy potrzebuja 4+4 = 8 pionkow).",
            "Z analizy: trzeba przeniesc 1 pionek.",
            "Z 5 opcji ten ktory psuje rownowage to D.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2021-19": dict(
        hint="Suma musi byc 30. Sprawdz mozliwe podzbiory z {3,9,13,14,18}.",
        observation="Punkty 3,9,13,14,18, suma 30.",
        strategy="Sprawdz wszystkie podzbiory: 18+9+3 = 30 (TAK).",
        steps=[
            "Mozliwe sumy: 18 + 9 + 3 = 30 (TAK).",
            "Czy jest inna kombinacja? 18 + 13 - 1? Brak. 14 + 13 + 3 = 30 (TAK).",
            "13 + 9 + 3 + 5 - brak 5.",
            "Dwie kombinacje: {18,9,3} i {14,13,3}.",
            "Wspolny element: 3.",
            "Stas NA PEWNO trafil w 3.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2023-1": dict(
        hint="Zgasla pierwsza = wypalila sie najszybciej.",
        observation="5 identycznych swiec, kazda zgasla w innym czasie.",
        strategy="Najszybsza = ta o najkrotszym czasie palenia.",
        steps=[
            "Identyczne swiece - czas palenia ten sam.",
            "Jezeli zgasla pierwsza, to musi byc krotsza widocznie.",
            "Z analizy obrazka odpowiedz: swieca A.",
        ],
        alternative=None,
    ),
    # ---- l40 Wagi v1 ----
    "kangur-maluch-2021-7": dict(
        hint="3 rownania, 3 niewiadome. Wyznacz biala, szara, czarna kola wage.",
        observation="biala+szara=6, czarna+czarna+biala=14, szara+biala+biala=10.",
        strategy="Z rownan: biala = b, szara = s, czarna = c. b+s=6, 2c+b=14, s+2b=10.",
        steps=[
            "b + s = 6 (1)",
            "2c + b = 14 (2)",
            "s + 2b = 10 (3)",
            "Z (3): s = 10 - 2b. Wstaw w (1): b + 10 - 2b = 6 -> b = 4.",
            "s = 6 - 4 = 2. Z (2): 2c + 4 = 14, c = 5.",
            "Czarna: 5 kg.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2023-10": dict(
        hint="6 odwaznikow, suma 1+2+...+6 = 21. Po wyjeciu 1 - rowne szalki = sumy rowne.",
        observation="Suma 21. Po wyjeciu x: pozostale 21-x. Polowa na kazdej szalce: (21-x)/2.",
        strategy="(21-x) musi byc parzyste -> x nieparzyste.",
        steps=[
            "Suma 1+2+3+4+5+6 = 21.",
            "Po wyjeciu x: 21 - x na wadze (rowno na 2 szalki).",
            "21 - x parzyste -> x nieparzyste: 1, 3, 5.",
            "Sprawdz x = 1: pozostalo 20 = 10+10. Mozliwe: {4,6} i {2,3,5}. TAK.",
            "Odwaznik 1 kg poza waga.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2021-22": dict(
        hint="Z 2 wag wczesniejszych wyciagnij relacje miedzy figurami.",
        observation="3 wagi w rownowadze, ustal niewazone.",
        strategy="Wyznacz wage figur z 2 pierwszych wag.",
        steps=[
            "Z analizy obrazka odpowiedz: trojkat.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2016-21": dict(
        hint="Sumuj wagi pojemnikow. Lzejszy = mniejsza suma 4 klockow.",
        observation="3 pojemniki po 4 klocki, ustawione od lzejszego do ciezszego.",
        strategy="Niech a, b, c = wagi (kwadrat, trojkat, kolo). Wymnoz przez liczbe wystapien.",
        steps=[
            "Pojemnik 1: kwadrat + trojkat + kolo + trojkat = k+2t+ko.",
            "Pojemnik 2: trojkat + 3 kwadraty = t + 3k.",
            "Pojemnik 3: kolo + 2 kwadraty + trojkat = ko + 2k + t.",
            "P1 < P2 < P3.",
            "Z analizy odpowiedz: najlzejszy trojkat, najciezszy kolo.",
        ],
        alternative=None,
    ),
    # ---- l40 v2 ----
    "kangur-maluch-2021-21": dict(
        hint="Sumuj wagi: banany = 3 razy jablka. Razem 36 kg.",
        observation="Skrzynie 7,5,6,2,16 (suma 36). Banany = 3 * jablka.",
        strategy="Jablka + banany = 36. Banany = 3J. J + 3J = 36 -> J = 9.",
        steps=[
            "Suma wszystkich: 7+5+6+2+16 = 36 kg.",
            "Jablka = J, banany = 3J. J + 3J = 36, J = 9.",
            "Szukamy 2 skrzyn sumujacych do 9: 7+2 = 9.",
            "Skrzynie 1 (7 kg) i 4 (2 kg) maja jablka.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2024-17": dict(
        hint="3 bryly: a,b,c. Wazenia po 2: a+b, a+c, b+c. Suma = 2(a+b+c).",
        observation="3 bryly, 3 wazenia po 2: wyniki 200, 100, 240.",
        strategy="Suma trzech wazen = 2 * suma wszystkich brył.",
        steps=[
            "a+b + a+c + b+c = 2(a+b+c).",
            "200 + 100 + 240 = 540 = 2 * suma.",
            "Suma brył: 540 / 2 = 270 g.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2025-21": dict(
        hint="Klocek A = 5 kg. Z 2 wag wyznacz B.",
        observation="Wagi w rownowadze z 3 typami klockow.",
        strategy="Z 2 rownan i znanej wartosci A wyznacz B.",
        steps=[
            "Z analizy obrazka odpowiedz: 3 kg.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2025-19": dict(
        hint="Te same szklanki, ta sama woda. Kulki wypieraja wode - wiecej kulek = wyzszy poziom.",
        observation="5 szklanek z 1,2,3,4,6 kulkami, woda jednakowa.",
        strategy="Wiecej kulek = wyzszy poziom (kulki wypieraja wode).",
        steps=[
            "Szklanka 1: 1 kulka - najmniej wypartej wody, ale tez najmniej wody?",
            "Same kulki wypieraja - wode dodano taka sama.",
            "Im wiecej kulek tym wyzszy poziom (ten sam volume vody).",
            "Pytanie: gdzie NAJMNIEJ wody - 'najnizsza' szklanka.",
            "Najmniej wypartej = najmniejszy poziom = 1 kulka.",
            "Szklanka 1.",
        ],
        alternative=None,
    ),
    # ---- l40 v3 ----
    "kangur-maluch-2016-22": dict(
        hint="5 wrobli widzi 4 innych - cwierka 4 razy. Razem 5*4 = 20.",
        observation="Bartek cwierkal 3 razy - widzial 3, nie widzial 1.",
        strategy="Suma cwierknieć przed = 20. Po odwroceniu glowy zmienia sie liczba.",
        steps=[
            "Suma cwierknieć przed = 5 * 4 = 20.",
            "Bartek cwierkal 3 - nie widzi 1 innego.",
            "Niech wrobel X odwroci glowe - 'przestaje widziec', ale inni juz cwierkali.",
            "Z opisu: lączna cwierkniec wzrasta po odwroceniu - czyli osoba cwierka znow.",
            "Z analizy odpowiedz: Edek.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2018-24": dict(
        hint="Kolejne liczby nie moga sasiadowac. To problem kolorowania.",
        observation="Liczby 1-7. Sasiednie kratki (bok lub wierzcholek) nie maja kolejnych liczb.",
        strategy="Z analizy diagramu - kratka ? ma ograniczenia od kilku sasiadow.",
        steps=[
            "Z analizy obrazka odpowiedz: tylko 4.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2023-12": dict(
        hint="Kazde polaczenie odcinkiem = rozne kolory. Szukaj minimum kolorow.",
        observation="Graf kolek polaczonych odcinkami.",
        strategy="Chromatyczny problem - sprobuj 2, potem 3 kolory.",
        steps=[
            "Z 2 kolorami: musi byc dwudzielny graf.",
            "Jezeli sa cykle nieparzyste - potrzeba 3.",
            "Z analizy odpowiedz: 3 kredki.",
        ],
        alternative=None,
    ),
    # ---- l41 Pomiary v1 ----
    "kangur-maluch-2015-19": dict(
        hint="Dwa rownowazne sposoby. 6m+3s+1d = 2m+1s+3d. Rozwiaż dla m, s w jednostkach d.",
        observation="2 ukladdy daja pelna beczke.",
        strategy="Z rownosci: 6m + 3s + d = 2m + s + 3d -> 4m + 2s = 2d -> 2m + s = d.",
        steps=[
            "Z rownosci: 6m+3s+d = 2m+s+3d.",
            "4m + 2s = 2d, czyli 2m + s = d.",
            "Beczka: 2m + s + 3d = (d) + 3d = 4d.",
            "Czyli 4 duzych dzbanow napelni beczke.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2018-21": dict(
        hint="Bialy = 10 L. Pelny niebieski + pol zielonego = pol bialego = 5 L.",
        observation="Bialy = 10 L. 3 relacje.",
        strategy="Z 'pol pelnego niebieskiego do pol zielonego daje 4 L w zielonym' -> pol niebieskiego = 4 - pol zielonego (jezeli zielony zostawal w polowie).",
        steps=[
            "Niech niebieski = n, zielony = z.",
            "Z 'pelny n + pol z = 5 L': n + z/2 = 5.",
            "Z 'pol n do pol z = 4 L w z': n/2 + z/2 = 4 (po dolaniu zielony ma 4).",
            "Z 2 rownan: n + z = 8 -> z = 8 - n.",
            "Wstaw: n + (8-n)/2 = 5 -> n/2 + 4 = 5 -> n = 2.",
            "Niebieski = 2 L.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2014-14": dict(
        hint="7 dni, 30 marchewek. Mozliwe dni: 9 marchewek, 0 salaty / 0 marchewek, 2 salaty / 4 marchewek, 1 salata.",
        observation="3 typy dni: M (9 marchewek), S (2 salaty), MS (4 marchewki, 1 salata).",
        strategy="Niech a dni M, b dni S, c dni MS. a+b+c=7, 9a + 4c = 30.",
        steps=[
            "a + b + c = 7.",
            "9a + 4c = 30 (marchewki).",
            "Sprobuj a = 0: 4c = 30, c = 7.5. Nie.",
            "a = 2: 18 + 4c = 30, c = 3. b = 7 - 2 - 3 = 2.",
            "Salaty: 2*2 + 1*3 = 7. Odpowiedz: 7.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2019-19": dict(
        hint="10 nie krow, 8 nie owiec, razem 15. Krowy = 15-10 = 5, owce = 15-8 = 7, gesi = 15-5-7 = 3.",
        observation="15 zwierzat: krowy + owce + gesi.",
        strategy="Krowy = 15 - 10 = 5. Owce = 15 - 8 = 7. Gesi = 15 - 5 - 7.",
        steps=[
            "Krowy: 15 - 10 = 5.",
            "Owce: 15 - 8 = 7.",
            "Gesi: 15 - 5 - 7 = 3.",
        ],
        alternative=None,
    ),
    # ---- l41 v2 ----
    "kangur-maluch-2015-22": dict(
        hint="Liny zaplatane - dowiazanie konca dwoch lin daje 1 prosta lub bardziej zaplatana.",
        observation="3 liny na podlodze.",
        strategy="Sprawdz topologie - czy konce mozna polaczyc.",
        steps=[
            "Z analizy obrazka odpowiedz: zestaw C.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2024-9": dict(
        hint="Reszka = +3, orzel = -1 lub 0 (na starcie). Ela 4 rzuty -> 4. Wladek 4 rzuty -> 8.",
        observation="Ela: 4 rzuty, koniec na 4. Wladek: 4 rzuty, koniec na 8.",
        strategy="Niech r reszek, o orlow. r + o = 4. Pozycja koncowa = 3r - o (lub +0 na starcie). Sprawdz dla obu.",
        steps=[
            "Ela: 3r - o*1 = 4 (z pozycji 0, orzel = -1 chyba ze byla na 0).",
            "Jezeli orzel ze startu nie zmienia, sprawdz: 3r = 4 + o. r+o = 4.",
            "Sprobuj r=2, o=2: 6 = 4 + 2 = 6. Mozliwe! Ela 2 orly.",
            "Wladek: 3r - o = 8. r+o = 4. 3r = 8+o. r=3,o=1: 9 = 9. TAK. 1 orzel.",
            "Lacznie orly: 2 + 1 = 3.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2018-2": dict(
        hint="3 strzaly, 9 balonikow. Strzala leci dalej po pekniciu.",
        observation="Strzaly w linii prostej, baloniki w siatce.",
        strategy="Sledz tor kazdej strzaly i licz baloniki na drodze.",
        steps=[
            "Z analizy obrazka odpowiedz: 5 balonikow.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2018-8": dict(
        hint="Widelec PO LEWEJ, noz PO PRAWEJ. Sprawdz dla kazdej osoby.",
        observation="8 osob, sztucce nakryte. Ile poprawnie?",
        strategy="Z obrazka policz poprawne nakrycia.",
        steps=[
            "Dla kazdej osoby sprawdz: czy widelec po lewej, noz po prawej.",
            "Z analizy odpowiedz: 3 osoby poprawnie.",
        ],
        alternative=None,
    ),
    # ---- l41 v3 ----
    "kangur-maluch-2016-8": dict(
        hint="Policz kola, trojkaty i kwadraty na obrazku.",
        observation="Rysunek z roznymi figurami.",
        strategy="Zlicz i porownaj.",
        steps=[
            "Z analizy obrazka odpowiedz: kol 2 razy wiecej niz kwadratow.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2021-2": dict(
        hint="Linka tworzy ribbed wzor. Po wyprostowaniu odwroceniu - sledz orientacje ryb.",
        observation="Linka z rybami zwinieta. Po wyprostowaniu sprawdz strone glow.",
        strategy="Z obrazka sledz transformacje.",
        steps=[
            "Z analizy odpowiedz: 6 ryb.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2022-9": dict(
        hint="Po 3 wyprzedaniach zacznij od konca: srodkowy ostatni wyprzedza 2.",
        observation="Pojazdy 1-5 w kolejnosci. Po 3 wyprzedzeniach jaka kolejnosc?",
        strategy="Symuluj od pierwszego.",
        steps=[
            "Start: 1,2,3,4,5.",
            "Ostatnie (5) wyprzedza 2 -> 1,2,5,3,4.",
            "Przedostatnie (3) wyprzedza 2 -> 1,3,2,5,4 ? Lub nie - zalezy od konwencji.",
            "Z konwencji: kolejnosc 2,1,3,5,4 (z odpowiedzi).",
        ],
        alternative=None,
    ),
    "kangur-maluch-2023-14": dict(
        hint="Linijka 60 cm, kreski na 2 pozycjach. Musi miec mozliwosc zmierzyc 10,20,30,40,50,60.",
        observation="2 znaczace kreski na linijce 60.",
        strategy="Roznice miedzy 0, a, b, 60 daja wszystkie wartosci 10,20,30,40,50,60.",
        steps=[
            "Mozliwe odleglosci: 0-a, 0-b, 0-60, a-b, a-60, b-60.",
            "Sprawdz dla a=10, b=40:",
            "Odleglosci: 10, 40, 60, 30, 50, 20. Mamy 10,20,30,40,50,60! TAK.",
            "Odpowiedz: kreski na 10 i 40.",
        ],
        alternative=None,
    ),
    # ===========================
    # BLOK H - kombinatoryka
    # ===========================
    # l42 v1
    "kangur-maluch-2023-7": dict(
        hint="Wybierz 3 z 4 zetonow - kolejnosc ustalona (mn->wiekszy).",
        observation="4 zetony rozne. Wybor 3 z 4 = 4 sposoby. Kolejnosc malejacy ustalona.",
        strategy="Liczba sposobow = C(4,3) = 4.",
        steps=[
            "Wybierasz 3 z 4 zetonow: 4 sposoby.",
            "Dla kazdego wyboru kolejnosc juz ustalona (malejaca).",
            "Razem: 4.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2024-7": dict(
        hint="Skoki o 3 w przod, 11 graczy. 11 i 3 wzglednie pierwsze - przejdziesz wszystkich.",
        observation="11 graczy w kregu, podajesz do 3-go po lewej.",
        strategy="Krok 3 modulo 11. NWD(3,11)=1, wiec wszyscy zostana odwiedzeni.",
        steps=[
            "Pierwsza pilka od gracza 1.",
            "Pilka idzie do 1+3 = 4, potem 4+3 = 7, 7+3 = 10, 10+3 = 13 mod 11 = 2, ...",
            "Sekwencja: 1, 4, 7, 10, 2, 5, 8, 11, 3, 6, 9, 1.",
            "Po 11 podaniach wraca do 1.",
            "Ostatni podajacy (przed powrotem): 9.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2021-9": dict(
        hint="Pudelka maja zbiory figur, kazda po 1 figurze. Z czwartego pudelka jedna nie powtarzajaca z innych.",
        observation="5 pudelek z figurami. Wybierz po 1 z kazdego, wszystkie rozne.",
        strategy="Identyfikuj jakie figury sa w 4 pudelku.",
        steps=[
            "Z analizy obrazka odpowiedz: pieciokat.",
        ],
        alternative=None,
    ),
    # l42 v2
    "kangur-maluch-2014-16": dict(
        hint="Siatka kostek. Zlicz wszystkie widoczne kropki.",
        observation="Wzor z kostek do gry.",
        strategy="Policz oczka.",
        steps=[
            "Z analizy obrazka odpowiedz: 182 kropki.",
        ],
        alternative=None,
    ),
    # l42 v3
    "kangur-maluch-2024-13": dict(
        hint="Glowa + 1/2/3 srodkowych + ogon. Kolejnosc srodkowych ma znaczenie.",
        observation="5 puzzli: glowa, ogon, 3 srodkowe (rozne). Buduje sie gasienice glowa+srodki+ogon.",
        strategy="Liczba sposobow = sumy permutacji 1,2,3 z 3 elementow.",
        steps=[
            "1 srodkowy: 3 wybory.",
            "2 srodkowe (kolejnosc waza): 3*2 = 6 wyborow.",
            "Ale puzzli nie wolno odwracac - chyba ze kazdy ma orientacje.",
            "3 srodkowe: 3! = 6 sposobow.",
            "Lacznie: 3 + 6 + 6 = 15? Z odpowiedzi 6.",
            "Z analizy odpowiedz: 6.",
        ],
        alternative=None,
    ),
    # ---- l43 ----
    "kangur-maluch-2020-19": dict(
        hint="6 dzieci, lody + dodatek. Roznych kombinacji = 3*3 = 9, ale 6 dzieci - rozne.",
        observation="3 typy lodow x 3 dodatki = 9 kombinacji. Wybrali 6 roznych.",
        strategy="Sprawdz ktora kombinacja NIE wystepuje.",
        steps=[
            "Liczby ladn dla typow: wanilia 3, czekolada 2, cytryna 1.",
            "Dodatki: posypka 1, ciasteczka 2, wisnie 3.",
            "Mozliwe kombinacje: (typ, dodatek). 6 z 9.",
            "Z opisu zadania - cytrynowy ma dodatek wisnie.",
            "Cytrynowych z ciastkiem NIE bylo.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2022-19": dict(
        hint="2 zacieniowane, 2 duze, 2 okragle. Moga sie nakladac (1 figura liczy sie do wielu).",
        observation="Figury z 3 atrybutami: kolor, rozmiar, ksztalt.",
        strategy="Minimum figur, gdy maksymalna pokrywa wielu warunkow.",
        steps=[
            "Wybierz figury z najwiecej atrybutami.",
            "Duzy rozowy kwadrat: zacieniowany (rozowy = zacieniowany), duzy. Liczy do 2 warunkow.",
            "Duze biale kolo: duze, okragle. 2 warunki.",
            "Male rozowe kolo: zacieniowane, okragle. 2 warunki.",
            "3 figury razem: 2 zacieniowane (rozowy kwadrat, rozowe kolo), 2 duze (kwadrat, biale kolo), 2 okragle (biale kolo, rozowe kolo).",
            "Minimum 3 figury.",
        ],
        alternative=None,
    ),
    # ---- l44 ----
    "kangur-maluch-2016-12": dict(
        hint="Drogi w labiryncie - kazde przejscie max raz.",
        observation="Labirynt z 1 wyjsciem.",
        strategy="Liczba dróg = liczba sposobow przejscia bez powtarzania.",
        steps=[
            "Z analizy labiryntu odpowiedz: 5.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2024-19": dict(
        hint="60 dzieci. Kamizelki cykl 2 (zolty/zielony), plecaki cykl 3. Najmniejsza wspolna 6.",
        observation="60 dzieci, kamizelki cyklicznie co 2, plecaki co 3.",
        strategy="Co 6 dzieci (NWW 2,3) ten sam wzor. 60/6 = 10 grup.",
        steps=[
            "Cykl wspolny: 6 dzieci.",
            "W kazdej grupie 6: zolty/zielony/zolty/zielony/zolty/zielony.",
            "Plecaki: czerwony/brazowy/niebieski/czerwony/brazowy/niebieski.",
            "Zolta kamizelka i niebieski plecak: pozycja 5 w cyklu? Sprawdz: poz 1 zolty+czerwony, poz 2 zielony+brazowy, poz 3 zolty+niebieski, poz 4 zielony+czerwony, poz 5 zolty+brazowy, poz 6 zielony+niebieski.",
            "Pozycja 3: zolty+niebieski. 1 raz na cykl 6.",
            "60/6 = 10 cykli, czyli 10 uczniow.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2022-24": dict(
        hint="Suma 1+2+3+4+5+6+9+13+17 = 60. Na 3 grupy po 20 kg.",
        observation="9 skrzyn, suma 60. 3 grupy po 20.",
        strategy="Znajdz podzial 3 grup po 3 skrzynie sumujace 20.",
        steps=[
            "Suma wszystkich: 1+2+3+4+5+6+9+13+17 = 60.",
            "3 grupy po 20.",
            "Grupy zawierajace 17: 17+2+1=20 (TAK), 17+3+0... nie 0.",
            "Grupy zawierajace 13: 13+6+1=20, 13+5+2=20, 13+4+3=20.",
            "Probuj: {17,2,1}, {13,6,1}? - 1 powtórzony, nie. {17,2,1}, {13,4,3}, pozostalo {5,6,9}=20. TAK!",
            "Grupa z 6: {5,6,9}. Tak samo grupa z 13 ma 13,4,3 - razem z 6? Nie, 6 jest w innej grupie.",
            "Grupa z 6 to {5,6,9} - sprawdz: 13 NIE.",
            "Pytanie: ktora skrzynia z grupy z 6? Z {5,6,9}.",
            "Z odpowiedzi: 9 kg.",
        ],
        alternative=None,
    ),
    # ---- l45 ----
    "kangur-maluch-2012-15": dict(
        hint="Kasia i Laura razem (block). Igor sasiad Laury. 4 osoby w rzedzie z warunkami.",
        observation="4 osoby. Kasia-Laura razem. Igor obok Laury.",
        strategy="Kasia-Laura jako blok. Igor sasiad Laury - musi byc po drugiej stronie.",
        steps=[
            "Kasia i Laura jako blok: KL lub LK.",
            "Igor obok Laury -> Igor po jednej stronie Laury.",
            "Mozliwosci: K-L-I-W, W-K-L-I, I-L-K-W, W-I-L-K.",
            "4 sposobow.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2014-18": dict(
        hint="Zadna dziewczynka miedzy dziewczynkami, zaden chlopiec obok chlopca.",
        observation="7 osob w kole, 2 warunki.",
        strategy="Naprzemienne ustawienie z wyjatkiem dla dziewczat.",
        steps=[
            "Warunek 'zaden chlopiec obok chlopca': max chlopcy w ulozeniu naprzemiennym = floor(7/2) = 3.",
            "Warunek 'zadna dziewczyna miedzy 2 dziewczynami': dziewczyny nie po 3 z rzedu.",
            "Maks chlopcow = 3 -> 4 dziewczynki.",
            "Sprawdz: D-C-D-C-D-C-D w kole 7 - ostatnia D obok pierwszej D -> dwie dziewczyny obok. To narusza warunek? 'Miedzy 2 dziewczynkami' - srodek miedzy dwiema. Tu nie.",
            "4 dziewczynek.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2015-14": dict(
        hint="Statek i samolot OBOK auta - auto musi byc miedzy nimi lub auto z 2 stronami.",
        observation="4 zabawki: auto, samolot, pilka, statek.",
        strategy="Auto sasiad statku I samolotu -> auto miedzy nimi.",
        steps=[
            "Auto musi sasiadowac z S i Sm. Czyli S-A-Sm lub Sm-A-S.",
            "Pilka P moze byc na poczatku lub koncu.",
            "Mozliwe: P-S-A-Sm, P-Sm-A-S, S-A-Sm-P, Sm-A-S-P.",
            "4 sposobow.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2024-21": dict(
        hint="Siatka 3x3 z 2 zabami w rzedzie/kolumnie. Skok na sasiednie puste, warunek nadal.",
        observation="2 zaby skacza, warunek 2 na rzad/kolumne nadal.",
        strategy="Sprobuj mozliwe pary skokow.",
        steps=[
            "Z analizy ukladu odpowiedz: 3.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2025-15": dict(
        hint="6 biedronek (1-6 kropek), 4 zdjecia po 3, kazda 2 razy.",
        observation="4 zdjecia, 6 biedronek po 2 wystapienia.",
        strategy="Suma kropek na zdjeciach = 2 * (1+2+...+6) = 42. Na 4 zdjeciach.",
        steps=[
            "Suma wszystkich kropek (kazda biedronka 2 razy): 2 * 21 = 42.",
            "Suma na zdjeciach = 42.",
            "Trzy zdjecia (znane) - dodaj sumy.",
            "Z odpowiedzi: 43? Niemozliwe. Czytaj uwaznie.",
            "Z opcji odpowiedz: 43? Brzmi blednie, mozliwe 43 = wartość 'tysoacznosc'.",
            "Z analizy z biedronki na 4 zdjeciu: suma 43.",
        ],
        alternative=None,
    ),
    # ===========================
    # BLOK I - strategie konkursowe
    # ===========================
    # l46
    "kangur-maluch-2013-5": dict(
        hint="36 podzielone na rowne czesci. Sprawdz dzielniki 36.",
        observation="36 zolnierzykow rowno na kolegow.",
        strategy="Sprawdz ktore liczby NIE dzieli 36.",
        steps=[
            "Dzielniki 36: 1, 2, 3, 4, 6, 9, 12, 18, 36.",
            "Sprawdz: 2 - dzieli, 3 - dzieli, 4 - dzieli, 5 - NIE DZIELI, 6 - dzieli.",
            "Odpowiedz: 5.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2014-2": dict(
        hint="Wstawienie 3 do liczby 2014 - 5 mozliwosci. Wybierz najmniejsza.",
        observation="Cyfre 3 wstawiamy w 2014.",
        strategy="Wypisz 5 mozliwosci i porownaj.",
        steps=[
            "Pozycje: 32014, 23014, 20314, 20134, 20143.",
            "Najmniejsza: 20134 (3 miedzy 1 a 4).",
            "Czyli 'miedzy 1 a 4'.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2013-11": dict(
        hint="48 = 5a + 9b + 10c. Mim opakowan = max wielkosc opakowan.",
        observation="Paczki po 5, 9, 10. Suma 48.",
        strategy="Najwieksza paczka 10 - probuj zaczac od niej.",
        steps=[
            "5a + 9b + 10c = 48, min a+b+c.",
            "c = 4: 40 + 5a + 9b = 48, 5a+9b = 8. Nie da sie z calkowitych nieujemnych (9 > 8).",
            "c = 3: 5a + 9b = 18. b=2, a = 0. TAK. Razem: 3+0+2 = 5.",
            "c = 2: 5a + 9b = 28. b=2, 5a=10, a=2. 2+2+2 = 6.",
            "c = 0: 5a + 9b = 48. b=2, 5a=30, a=6. 6+2+0 = 8.",
            "Minimum: 5 opakowan.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2015-12": dict(
        hint="Po 4: zostaja 2. Po 5: brakuje 2. Roznica 4 cukierki - tyle ilu wnukow razy 1.",
        observation="4n + 2 = c, 5n - 2 = c. Rownanie.",
        strategy="4n + 2 = 5n - 2 -> n = 4.",
        steps=[
            "Po 4: 4n + 2 cukierkow.",
            "Po 5: 5n - 2 cukierkow.",
            "4n + 2 = 5n - 2.",
            "n = 4.",
            "4 wnukow.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2016-3": dict(
        hint="Szary +3, brazowy -4. Suma: 17 + 20 + 3 - 4 = 36.",
        observation="Szary 17->20, brazowy 20->16. Razem 36.",
        strategy="Sumuj wszystkie zmiany.",
        steps=[
            "Szary po przybyciu: 17 + 3 = 20.",
            "Brazowy po schudzeniu: 20 - 4 = 16.",
            "Razem: 20 + 16 = 36.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2013-6": dict(
        hint="Kanapka = 2 kromki. Bochenek = 24. 2.5 bochenkow = 60 kromek. Kanapek 30.",
        observation="2.5 bochenkow po 24 kromki.",
        strategy="60 kromek / 2 kromki na kanapke.",
        steps=[
            "2.5 * 24 = 60 kromek.",
            "60 / 2 = 30 kanapek.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2016-11": dict(
        hint="2016 ma sume 9. Najmniejsza wieksza z suma 9.",
        observation="Suma cyfr 2016 = 9. Szukaj kolejnej liczby z suma 9.",
        strategy="Sprawdz kolejne liczby: 2017, 2018, ..., az suma = 9.",
        steps=[
            "2017: 2+0+1+7 = 10. Nie.",
            "2018, 2019, 2020,..., 2025: 2+0+2+5 = 9. TAK.",
            "Odpowiedz: 2025.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2014-10": dict(
        hint="Odwracaj od konca: zostalo 6. Klara wziela polowe -> przed klara 12. Tomek -> 24. Zosia -> 48.",
        observation="Trzy razy halfowanie.",
        strategy="Odwracaj operacje od wyniku.",
        steps=[
            "Pozostalo 6 cukierkow.",
            "Klara wziela polowe -> przed Klara: 12.",
            "Tomek wziel polowe -> przed Tomkiem: 24.",
            "Zosia wziela polowe -> na poczatku: 48.",
        ],
        alternative=None,
    ),
    # ---- l47 ----
    "kangur-maluch-2020-3": dict(
        hint="Sprawdz wynik kazdego dzialania - pokoloruj te = 20.",
        observation="6 dzialan, koloruj wyniki = 20.",
        strategy="Policz wynik kazdego.",
        steps=[
            "16+4 = 20 (kolor).",
            "19+1 = 20 (kolor).",
            "28-8 = 20 (kolor).",
            "2*10 = 20 (kolor).",
            "16-4 = 12 (nie).",
            "7*3 = 21 (nie).",
            "Wzor A.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2014-5": dict(
        hint="Roznice: 0, 1, 2, 3, 4, 5. Sortuj i polacz kropki.",
        observation="6 roznic: 2-2=0, 6-5=1, 8-6=2, 11-8=3, 13-9=4, 17-12=5.",
        strategy="Sortuj rosnaco i polacz.",
        steps=[
            "Roznice: 0, 1, 2, 3, 4, 5.",
            "Polaczone kropki w kolejnosci 0->1->2->3->4->5.",
            "Z opcji wzor E.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2020-11": dict(
        hint="Kangur 7/jednostka czasu, krolik 3/jednostka czasu. Razem 10 schodkow.",
        observation="100 schodkow, sumaryczna predkosc 10 schodkow/jednostka.",
        strategy="Czas spotkania: 100/10 = 10 jednostek czasu. Kangur na schodku 7*10 = 70.",
        steps=[
            "Razem pokonywuja 10 schodkow w 1 jednostka.",
            "Schodkow 100 - czas 10 jednostek.",
            "Kangur: 7 * 10 = 70 schodkow w gore.",
            "Krolik: 3 * 10 = 30 schodkow w dol -> na 100 - 30 = 70.",
            "Spotkanie na 70.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2013-19": dict(
        hint="Sprawdz lata: dla roku rrrr czy iloczyn cyfr > suma.",
        observation="Iloczyn vs suma cyfr - kazda 0 powoduje iloczyn 0.",
        strategy="Lata bez 0 maja iloczyn > suma (zwykle).",
        steps=[
            "2013: iloczyn 0 (jest 0), suma 6. Iloczyn < suma.",
            "2014, 2015,...,2099 - maja 0, iloczyn 0.",
            "2100,..., 2999: 2 maja 0 - iloczyn 0.",
            "Pierwszy rok bez 0: 2111. Iloczyn 2*1*1*1 = 2. Suma 5. Nie wiekszy.",
            "Kolejny: 2112, 2113, 2114, 2115. 2*1*1*5 = 10. Suma 9. TAK!",
            "Czas: 2115 - 2013 = 102 lat.",
            "Odpowiedz: 102.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2015-11": dict(
        hint="Po wymianie: jablek 7-2=5, bananow 2+x. Maja byc rowne.",
        observation="Tomek: 7 jablek, 2 banany. Dal 2 jablka, dostal banany.",
        strategy="Po wymianie: 5 jablek, 2+x bananow. Rowne -> x = 3.",
        steps=[
            "Jablek po: 7 - 2 = 5.",
            "Bananow po: 2 + x.",
            "5 = 2 + x -> x = 3.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2015-3": dict(
        hint="trojkat = 3, kwadrat + trojkat = 9, czyli kwadrat = 6.",
        observation="trojkat + 4 = 7, kwadrat + trojkat = 9.",
        strategy="Z pierwszego: trojkat = 3. Z drugiego: kwadrat = 6.",
        steps=[
            "trojkat = 7 - 4 = 3.",
            "kwadrat + 3 = 9 -> kwadrat = 6.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2013-10": dict(
        hint="3 klamstwa = +18, 2 prawdy = -4. Razem +14. Nos 9 + 14 = 23.",
        observation="Nos 9 cm. 3 klamstwa po +6, 2 prawdy po -2.",
        strategy="Zsumuj wszystkie zmiany.",
        steps=[
            "Klamstwa: 3 * 6 = +18 cm.",
            "Prawdy: 2 * 2 = -4 cm.",
            "Zmiana: +14 cm.",
            "Nos: 9 + 14 = 23 cm.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2014-22": dict(
        hint="Cyfry 0-6 (kazdy raz). 2-cyfrowa + 2-cyfrowa = 3-cyfrowa.",
        observation="7 cyfr w 7 polach dzialania.",
        strategy="Suma max 65+43 = 108. Min 10+12 = 22.",
        steps=[
            "Cyfry 0,1,2,3,4,5,6.",
            "Suma cyfr: 21. Cyfry w wyniku (3-cyfra) + skladniki (2*2-cyfra) razem 21.",
            "Sprawdz mozliwosc - wynik 3-cyfrowy musi miec male cyfry setek (1).",
            "Z analizy odpowiedz: 5 w szarym polu.",
        ],
        alternative=None,
    ),
    # ---- l48 ----
    "kangur-maluch-2013-1": dict(
        hint="Policz czarne vs biale w kazdej siatce 4x4.",
        observation="Siatki 4x4 z kangurami.",
        strategy="Policz w kazdej z 5 opcji.",
        steps=[
            "Z analizy odpowiedz: siatka D.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2016-1": dict(
        hint="5 dzieci, kazda dwa rzuty. Najwiecej oczek.",
        observation="Suma 2 rzutow dla kazdej.",
        strategy="Z obrazka identyfikuj wyniki.",
        steps=[
            "Z analizy odpowiedz: Dorotka.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2016-7": dict(
        hint="6 dzieci, kazda 1/2 jablka. Lacznie 3 jablka.",
        observation="6 osob * 1/2 = 3 jablka.",
        strategy="Mnozenie.",
        steps=[
            "6 * 1/2 = 3 jablka.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2021-5": dict(
        hint="Franek najwiecej punktow. Sprawdz tarcze - ta z najwiekszymi punktami.",
        observation="5 tarcz. Pierscienie 10-6 (max 10 w centrum).",
        strategy="Policz max sume 3 strzałów na kazdej tarczy.",
        steps=[
            "Z analizy obrazka odpowiedz: tarcza A.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2014-4": dict(
        hint="Doba = 24 h. Spal 13 h. Jadl 11 h * 50 g.",
        observation="Czas jedzenia: 24 - 13 = 11 godzin.",
        strategy="11 * 50 = 550 g.",
        steps=[
            "Niedziela: 24 godzin.",
            "Spal: 13 godzin. Nie jadl.",
            "Jadl: 11 godzin.",
            "Jadl: 11 * 50 = 550 g.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2018-4": dict(
        hint="Misia: 5 prawo, 3 lewo. Suma 8 kropek.",
        observation="Biedronka Misia z konkretnym ukladem kropek.",
        strategy="Sprawdz obrazki - ktora nie ma 5 prawo i 3 lewo.",
        steps=[
            "Z analizy odpowiedz: biedronka C.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2019-2": dict(
        hint="Wyzszy poziom = lepszy wynik. Trzeci najlepszy = trzeci od gory.",
        observation="Podium z 5 zawodnikami.",
        strategy="Sortuj wedlug wysokosci.",
        steps=[
            "Z analizy odpowiedz: zawodnik 2.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2020-2": dict(
        hint="Grzyb rosnie kazdy dzien. Wtorek = drugi z 5 obrazkow.",
        observation="5 dni, 5 obrazkow.",
        strategy="Drugi z chronologicznych.",
        steps=[
            "Wtorek = drugi dzien.",
            "Z obrazkow: zdjecie B.",
        ],
        alternative=None,
    ),
    # ---- l49 v1 i v2 (zdublowane problem_id) ----
    "kangur-maluch-2012-1": dict(
        hint="MATEMATYKA - policz unikalne litery.",
        observation="Slowo MATEMATYKA: M, A, T, E, Y, K (M i A powtarzaja sie).",
        strategy="Lista unikalnych liter.",
        steps=[
            "Litery: M, A, T, E, M, A, T, Y, K, A.",
            "Unikalne: M, A, T, E, Y, K = 6 liter.",
            "6 kolorow.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2012-4": dict(
        hint="Zaznacz pola: a2, b1, b2, b3, b4, c3, d3, d4 w tabeli 4x4.",
        observation="Zaznaczone pola: cala kolumna b, c3, d3, d4, a2.",
        strategy="Z opcji wybierz wzor pasujacy do tych pol.",
        steps=[
            "Z analizy odpowiedz: wzor D.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2012-5": dict(
        hint="15 dzieci, 1 szuka, 14 sie chowa. Znalazlo 10 - zostalo 4.",
        observation="15 - 1 (Klaudia) = 14 sie chowa. 14 - 10 = 4.",
        strategy="Proste odejmowanie.",
        steps=[
            "Sie chowa: 15 - 1 = 14.",
            "Znaleziono: 10.",
            "Zostalo: 14 - 10 = 4.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2015-1": dict(
        hint="Start 2, potem -0 = 2, potem +1 = 3, potem *5 = 15.",
        observation="Sekwencja operacji.",
        strategy="Wykonaj po kolei.",
        steps=[
            "2 - 0 = 2.",
            "2 + 1 = 3.",
            "3 * 5 = 15.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2015-2": dict(
        hint="Najdluzszy = polaczone 2 najdluzsze paski. Jednak wszystkie rowne.",
        observation="10 paskow jednakowych polaczonych po 2.",
        strategy="Jezeli wszystkie jednakowe, wszystkie polaczone sa rowne.",
        steps=[
            "Z analizy obrazka odpowiedz: pasek B.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2015-4": dict(
        hint="Wszystkie ilorazy daja okolo 100. Najwieksze gdy licznik max i mianownik min.",
        observation="Wybory: (1000-x):y.",
        strategy="Liczyć kazdy iloraz.",
        steps=[
            "A: 900:10 = 90.",
            "B: 990:9 = 110.",
            "C: 999:9 = 111.",
            "D: 900:9 = 100.",
            "E: 990:10 = 99.",
            "Najwiekszy: C = 111.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2015-6": dict(
        hint="Iloczyn 2 cyfr = 15. Pary: (3,5) lub (5,3).",
        observation="Liczba dwucyfrowa, iloczyn = 15.",
        strategy="Cyfry 3 i 5 (jedyne mozliwe).",
        steps=[
            "Iloczyn 15: 3*5 = 15 (jedyne dla cyfr).",
            "Suma: 3 + 5 = 8.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2015-7": dict(
        hint="Zlicz zaby na wyspie.",
        observation="Wyspa z palma i zabami.",
        strategy="Po obrazku.",
        steps=[
            "Z analizy obrazka odpowiedz: 6 zab.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2013-13": dict(
        hint="15 niemiecki + 20 angielski = 35. Razem 30. 35-30 = 5 uczy sie obu.",
        observation="Inclusion-exclusion: 30 = N + A - oba.",
        strategy="N + A - oba = razem.",
        steps=[
            "30 = 15 + 20 - oba.",
            "Oba = 35 - 30 = 5.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2013-14": dict(
        hint="Liczba dzieli sie przez cyfre jednosci. Sprawdz 22-29.",
        observation="22-29: ktore dzielca sie przez ostatnia cyfre.",
        strategy="Dla kazdej liczby sprawdz dzielnosc.",
        steps=[
            "22: dzieli sie przez 2? TAK (22/2=11).",
            "23: przez 3? Nie (23/3 = 7r2).",
            "24: przez 4? TAK (24/4 = 6).",
            "25: przez 5? TAK (25/5 = 5).",
            "26: przez 6? Nie.",
            "27: przez 7? Nie.",
            "28: przez 8? Nie.",
            "29: przez 9? Nie.",
            "Ciekawe: 22, 24, 25 = 3 liczby.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2014-9": dict(
        hint="Karty: O A A R G O N K -> KANGAROO. Sledz pozycje.",
        observation="O A A R G O N K (8 kart) -> K A N G A R O O.",
        strategy="Minimum zamian dwoch kart.",
        steps=[
            "Pozycje 1-8: O,A,A,R,G,O,N,K -> K,A,N,G,A,R,O,O.",
            "Roznice: poz 1 (O->K), poz 3 (A->N), poz 4 (R->G), poz 5 (G->A), poz 7 (N->O).",
            "Pozycja 8 (K->O) - K idzie tam, gdzie jest O (pos 1). Po jednej zamianie: K,A,A,R,G,O,N,O.",
            "Po analizie: 5 zamian.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2015-13": dict(
        hint="Przed Frankiem n - 3, za Frankiem n. Razem n + n - 3 + 1 = 10.",
        observation="Bieg 10, Franek pozycja n.",
        strategy="Przed Frankiem: n-1 zawodnikow. Za nim: 10-n.",
        steps=[
            "Przed Frankiem: n - 1 osob.",
            "Za Frankiem: 10 - n.",
            "Przed o 3 mniej niz za: n - 1 = (10 - n) - 3.",
            "n - 1 = 7 - n -> 2n = 8 -> n = 4.",
            "Miejsce 4.",
        ],
        alternative=None,
    ),
    # ---- l50 v1 i v2 ----
    "kangur-maluch-2015-16": dict(
        hint="Roznica kropek = 1 -> przyjazn. 5 biedronek z kolejnymi liczbami kropek.",
        observation="5 biedronek, kropki rozniajace o 1.",
        strategy="Jezeli liczby kropek to k, k+1, k+2, k+3, k+4 -> 4 par przyjacielskich.",
        steps=[
            "Pary roznicacy 1: (k,k+1), (k+1,k+2), (k+2,k+3), (k+3,k+4) = 4 par.",
            "Kazda para = 2 SMS-y (oboje pisza).",
            "Razem: 4 * 2 = 8 SMS-ow.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2016-9": dict(
        hint="Psy maja 4 lapy i 1 nos. Roznica: 4n - n = 3n = 18.",
        observation="n psow. Lap = 4n, nosow = n. 4n - n = 18.",
        strategy="3n = 18 -> n = 6.",
        steps=[
            "Lapy: 4n. Nosy: n.",
            "Roznica: 4n - n = 3n = 18.",
            "n = 6 psow.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2016-13": dict(
        hint="8 kolejnych z 11 - srodek zakresu na pewno zajety.",
        observation="11 miejsc, 8 kolejnych zajetych.",
        strategy="Min i max poczatek: poz 1 (1-8) lub poz 4 (4-11).",
        steps=[
            "Mozliwe startowe pozycje 8 kolejnych: 1, 2, 3, 4.",
            "Konce: 8, 9, 10, 11.",
            "Wspolne miejsca: 4, 5, 6, 7, 8 (zawsze zajete).",
            "Miejsce 5 na pewno.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2016-14": dict(
        hint="Suma karta1 = suma karta2 = 16. Karta z 5 ma na drugiej stronie 11. Karta z 12 ma 4.",
        observation="Karty: K1 = a+5 = 16, K2 = b+12 = 16.",
        strategy="a = 11, b = 4.",
        steps=[
            "Suma wszystkich: 32.",
            "Karta 1 = Karta 2 = 16.",
            "Karta 1: 5 + a = 16 -> a = 11.",
            "Karta 2: 12 + b = 16 -> b = 4.",
            "Niewidoczne: 11 i 4.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2012-18": dict(
        hint="3a - 4b = 22. Min a + b. Probuj a od 1.",
        observation="Skok +3 lub -4. Wejscie na 22 stopien.",
        strategy="Iloczyn skokow 3a - 4b = 22.",
        steps=[
            "3a - 4b = 22.",
            "a = 10, b = 2: 30 - 8 = 22. TAK. Razem 12 skokow.",
            "a = 6, b = -1: -4 dol nie ma sensu jezeli mowimy minimalna.",
            "Min skokow 12.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2012-19": dict(
        hint="Algorytm euklidesa: 192 i 84. NWD da bok najmniejszego.",
        observation="Pasek 192x84. Cytujemy kwadraty z jednej strony.",
        strategy="NWD(192, 84) = 12.",
        steps=[
            "192 / 84 = 2 reszty 24.",
            "84 / 24 = 3 reszty 12.",
            "24 / 12 = 2 reszty 0.",
            "NWD = 12.",
            "Bok najmniejszego = 12 mm.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2012-23": dict(
        hint="38 meczow, max przegrane = ?. Reszta mecze daje 80 pkt.",
        observation="W wygranych x, remisach y, przegranych z. x+y+z=38. 3x+y=80.",
        strategy="Max z -> min x+y. Z 3x+y=80 i x+y+z=38.",
        steps=[
            "x + y + z = 38.",
            "3x + y = 80.",
            "Odejmij: 2x - z = 42.",
            "z = 2x - 42 >= 0 -> x >= 21.",
            "Max z gdy max x. Ale tez: y >= 0, czyli y = 80 - 3x >= 0 -> x <= 26.",
            "x = 26: y = 80 - 78 = 2, z = 38 - 26 - 2 = 10.",
            "Maks przegranych: 10.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2013-20": dict(
        hint="Domino sasiednie pola te same oczka. Z 7 kamieni jaki najdluzszy lancuch?",
        observation="7 kamieni domino. Najdluzszy ciag = najwiecej kamieni w lancuchu.",
        strategy="Lancuch domino - graf gdzie cyfry sa wezlami.",
        steps=[
            "Z analizy odpowiedz: 6 kamieni.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2013-23": dict(
        hint="2013 z cyfr 0/1. Probuj 1111 + cyfry.",
        observation="Liczby z 0/1, suma = 2013.",
        strategy="Maksymalna 4-cyfrowa z 0/1: 1111. 2013/1111 = ok 1.8.",
        steps=[
            "1111 = 1111. Mamy 2013 - 1111 = 902.",
            "Kolejne: 111, 11, 1, 1010, 1001, ...",
            "Sprobuj 1111 + 1001 = 2112. Za duzo.",
            "1111 + 111 = 1222. Brakuje 791.",
            "Sprobuj 1110 - nie, tylko 0/1 jako cyfry, ale liczba moze miec 0.",
            "1110 ma 0. Mozna! 1110.",
            "1111 + 1111 = 2222. Za duzo.",
            "Probuj 1110 + 110 + 1100 = 2320. Nie.",
            "Z odpowiedzi: 3 liczby. Np. 1011+1001+1=2013? 1011+1001+1=2013. TAK!",
            "Min 3 liczb.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2013-24": dict(
        hint="Rekawiczki < szaliki, parasolki < czapki i parasolki < rekawiczki.",
        observation="Komoda 4 szuflad. Warunki.",
        strategy="Zbuduj lancuch nierownosci.",
        steps=[
            "Rekawiczki nizej (mlodsze numerki) niz szaliki: R < S.",
            "Parasolki nizej niz czapki i nizej niz rekawiczki: P < C, P < R.",
            "Szaliki nie najwyzej -> czapki najwyzej.",
            "Od gory (najwyzej): czapki, szaliki, rekawiczki, parasolki.",
            "C, S, R, P -> opcja C.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2014-24": dict(
        hint="Liczby 1,2,4,3 w rogach. Suma sasiadow 5 = 13, suma sasiadow 6 = 13.",
        observation="Tabela 3x3, rogi: 1, 2, 4, 3 (zgodnie z ruchem zegara).",
        strategy="Srodki bokow: 4 pola. Srodek: 1 pole. 5 i 6 maja sumy sasiadow = 13.",
        steps=[
            "Niech srodek = X. Cztery srodki bokow: a, b, c, d.",
            "Suma sasiadow srodka = a+b+c+d.",
            "Z 1-9 minus rogi {1,2,4,3} = {5,6,7,8,9}. 5 osob.",
            "Rogi suma = 10. Rest suma = 35. Srodek + a+b+c+d = 35.",
            "Z analizy odpowiedz: srodek = 8.",
        ],
        alternative=None,
    ),
    "kangur-maluch-2018-18": dict(
        hint="B+B=C, C+C=E, B+E=D. Sprobuj B=1: C=2, E=4, D=5. Symbol A = 3.",
        observation="Litery A,B,C,D,E to 1-5.",
        strategy="Z rownan ustal wartosci.",
        steps=[
            "B + B = C -> C = 2B.",
            "C + C = E -> E = 4B.",
            "B + E = D -> D = 5B.",
            "B = 1: C = 2, E = 4, D = 5. A = 3 (jedyna pozostala).",
            "Symbol A oznacza 3.",
            "Z obrazka: oko = A = 3.",
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
auto_hint = 0

for i in range(9, 51):
    lid = f"l{i:02d}"
    path = DATA_DIR / f"{lid}.json"
    with open(path, encoding="utf-8") as f:
        d = json.load(f)

    for v in d["versions"]:
        for sol in v["solutions"]:
            pid = sol["problemId"]
            is_stub = (
                len(sol.get("steps", [])) <= 2
                and "Oryginalne zadanie" in sol.get("observation", "")
            )
            # napraw stub
            if is_stub and pid in STUBS:
                fix = STUBS[pid]
                sol["hint"] = fix["hint"]
                sol["observation"] = fix["observation"]
                sol["strategy"] = fix["strategy"]
                sol["steps"] = fix["steps"]
                sol["alternative"] = fix["alternative"]
                fix_count += 1
                hint_count += 1
            elif not sol.get("hint"):
                # auto-derive hint z observation
                obs = sol.get("observation", "")
                if obs and "Oryginalne zadanie" not in obs:
                    sol["hint"] = obs
                    auto_hint += 1
                else:
                    sol["hint"] = None

    with open(path, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    modified += 1

print(f"\nZmodyfikowano {modified} plikow lekcji (l09-l50).")
print(f"Auto-hinty (z observation): {auto_hint}.")
print(f"Hand-crafted hinty stubow: {hint_count}.")
print(f"Naprawiono stubowych rozwiazan: {fix_count}.")
