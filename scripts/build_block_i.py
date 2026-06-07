"""Blok I - lekcje 46-50: strategie konkursowe + 2 symulacje konkursu."""
import json

def orig(year, number):
    with open(f"data/parsed/{year}.json", encoding="utf-8") as f:
        d = json.load(f)
    for p in d["problems"]:
        if p["number"] == number:
            return p
    raise ValueError(f"No {year}#{number}")

def gen(lid, ver, sfx, diff, topic, subtopic, statement, choices, correct):
    return dict(id=f"gen-l{lid}-{ver}-{sfx}", source=f"generated-l{lid}-{ver}-{sfx}",
                year=None, number=None, difficulty=diff, topic=topic, subtopic=subtopic,
                statement=statement, hasImage=False, imageNote=None, choices=choices, correct=correct)

def sol(pid, obs, strat, steps, ans, alt=None):
    return dict(problemId=pid, observation=obs, strategy=strat, steps=steps, answer=ans, alternative=alt)

# Helper - dla originalow: solution po prostu cytuje poprawna odpowiedz (latwiejsze niz ich pelne rozwiazania)
def osol(p, summary):
    return dict(problemId=p["id"], observation="Oryginalne zadanie Kangurka.",
                strategy=summary, steps=[summary, "Poprawna odpowiedz: "+p["correct"]],
                answer=p["correct"], alternative=None)

def lesson(lid, number, title, topic, minutes, intro, tool, trick, v1, v2, quiz):
    return dict(id=lid, number=number, block="Strategie konkursowe", blockCode="I",
                title=title, topic=topic, estimatedMinutes=minutes,
                theory=dict(intro=intro, tool=tool, trick=trick),
                versions=[v1, v2], quiz=quiz)

def ver(vid, label, warmup, challenge, solutions):
    return dict(versionId=vid, label=label, warmup=warmup, challenge=challenge, solutions=solutions)

LESSONS = []

# ================= LEKCJA 46: Jak czytac zadanie =================
l46_v1_orig = [orig(2013,5), orig(2014,2), orig(2013,11), orig(2015,12)]
l46_v2_orig = [orig(2016,3), orig(2013,6), orig(2016,11), orig(2014,10)]

l46 = lesson("l46", 46, "Jak czytac zadanie Kangurka", "lamiglowki", 14,
    "Najczestszy blad w Kangurze: ktos rozwiazuje zadanie poprawnie, ale odpowiada na inne pytanie. 'Ile zostalo?' a uczen liczy 'ile bylo'. Czytanie zadania to klucz - przed liczeniem zatrzymaj sie i sprawdz: czego dokladnie pytaja?",
    "Sztuczka 1: PRZECZYTAJ DWA RAZY. Najpierw szybko, potem powoli. Po drugim razie podkresl: co dane, czego szukam.\n\nSztuczka 2: WYPISZ DANE. Z zadania wyciagnij liczby, jednostki, warunki. Latwiej je polaczyc.\n\nSztuczka 3: SPRAWDZ JEDNOSTKE ODPOWIEDZI. Pyta o cm a odpowiedzi w m - moze pulapka. Albo pyta o LICZBE a odpowiedzi to OPISY.\n\nSztuczka 4: POMYSL O SENSIE. Czy mozliwe? Cena 1000 zl za jablko? Prawdopodobnie blad odczytu albo zlepa interpretacja.",
    "Pulapka Kangurka: dlugie zadania z 3-4 zdaniami opisu. Czesto pierwsze 2 zdania to OZDOBNIK (postacie, kontekst), a kluczowe info w ostatnim zdaniu. Czytaj do konca - inaczej rozwiazesz inne zadanie.",
    ver("v1", "Wersja 1 (oryginalna)",
        [gen(46,"v1","w1","3pkt","lamiglowki","czego pytaja",
            "Zadanie pyta 'Ile bananow zostalo?'. Na poczatku bylo 15, zjedzono 8. Co odpowiadasz?",
            {"A":"7 (zostalo)","B":"8 (zjedli)","C":"15 (poczatek)","D":"23 (suma)","E":"Nie wiadomo"},"A"),
         gen(46,"v1","w2","3pkt","lamiglowki","pulapka wyboru",
            "Zadanie: 'Ola ma 3 czerwone, 4 zielone, 5 niebieskich kulek. Ile NIEBIESKICH?'",
            {"A":"3","B":"4","C":"5","D":"12","E":"15"},"C"),
         gen(46,"v1","w3","3pkt","lamiglowki","podkresl kluczowe",
            "W zadaniu 'Mama kupila pol kg jablek po 4 zl za kg. Ile zaplacila?', co jest kluczem?",
            {"A":"Sama mama","B":"Pol kg i cena 4 zl/kg","C":"Tylko 4 zl","D":"Tylko pol kg","E":"Nic"},"B"),
         l46_v1_orig[0], l46_v1_orig[1]],
        [l46_v1_orig[2], l46_v1_orig[3]],
        [sol("gen-l46-v1-w1","Pytaja o reszte - 15-8=7.","Czytanie pytania.",["Zostalo: 15 - 8 = 7"],"A"),
         sol("gen-l46-v1-w2","Pytaja TYLKO o niebieskie.","Selekcja informacji.",["Niebieskich = 5"],"C"),
         sol("gen-l46-v1-w3","Klucz: ilosc + cena za jednostke.","Identyfikacja danych.",["Pol kg razy 4 zl/kg = 2 zl"],"B"),
         osol(l46_v1_orig[0],"Daniel 36 zolnierzykow rozdziela rowno. 5 nie jest dzielnikiem 36."),
         osol(l46_v1_orig[1],"Wstawiamy 3 do 2014. Najmniejsza: 20134 (miedzy 1 a 4)."),
         osol(l46_v1_orig[2],"48 pomarancz, opakowania 5, 9, 10. Najmniej opakowan: 5."),
         osol(l46_v1_orig[3],"Babcia, po 4 i zostane 2, po 5 i brakuje 2. Wnukow: 4.")]),
    ver("v2", "Wersja 2 (powtorka)",
        [gen(46,"v2","w1","3pkt","lamiglowki","ile wzielo",
            "Pyta: 'Ile dzieci zostalo bez nagrody?'. Bylo 20, nagrody dostalo 15. Odpowiedz?",
            {"A":"5","B":"15","C":"20","D":"35","E":"Nie wiadomo"},"A"),
         gen(46,"v2","w2","3pkt","lamiglowki","co dane",
            "Zadanie: 'Trojkat ma boki 3, 4, 5 cm. Ile wynosi obwod?'. Co liczymy?",
            {"A":"Pole","B":"Wysokosc","C":"Obwod = suma bokow","D":"Najdluzszy bok","E":"Najkrotszy bok"},"C"),
         gen(46,"v2","w3","3pkt","lamiglowki","ostatnie zdanie",
            "Zadanie zaczyna sie 'Bajka o smoku...' i konczy 'Ile lat ma smok?'. Co zwracac uwage?",
            {"A":"Na poczatek (bajke)","B":"Na konkretne pytanie (lat smoka)","C":"Na imie bohatera","D":"Na ilosc zdan","E":"Tylko na liczby"},"B"),
         l46_v2_orig[0], l46_v2_orig[1]],
        [l46_v2_orig[2], l46_v2_orig[3]],
        [sol("gen-l46-v2-w1","20 - 15 = 5 bez nagrody.","Roznica.",["20-15=5"],"A"),
         sol("gen-l46-v2-w2","Obwod = suma bokow.","Definicja obwodu.",["3+4+5=12 cm"],"C"),
         sol("gen-l46-v2-w3","Skup sie na konkretnym pytaniu na koncu.","Identyfikacja pytania.",["Pytanie: ile lat ma smok"],"B"),
         osol(l46_v2_orig[0],"Szary 17+3=20, brazowy 20-4=16. Razem 36 kg."),
         osol(l46_v2_orig[1],"Mama 2 i pol bochenka = 60 kromek = 30 kanapek."),
         osol(l46_v2_orig[2],"Suma cyfr 2016 = 9. Najmniejsza wieksza: 2025 (suma 9)."),
         osol(l46_v2_orig[3],"Koszyk - polowa po polowie po polowie - 6. Poczatek = 48.")]),
    [dict(q="Najczestszy blad w Kangurze:",
          choices={"A":"Liczenie","B":"Czytanie zadania","C":"Pisanie"}, correct="B",
          explain="Niedokladne czytanie - odpowiadanie na inne pytanie."),
     dict(q="Przed liczeniem nalezy:",
          choices={"A":"Przeczytac dwa razy","B":"Zgadnac","C":"Pomijac"}, correct="A",
          explain="Dwukrotne czytanie - identyfikujesz dane i pytanie."),
     dict(q="Klucz informacji w zadaniu zwykle:",
          choices={"A":"Na poczatku","B":"W ostatnim zdaniu","C":"W tytule"}, correct="B",
          explain="Pytanie i kluczowe info czesto w ostatnim zdaniu.")])
LESSONS.append(l46)

# ================= LEKCJA 47: Szukaj wzoru =================
l47_v1_orig = [orig(2020,3), orig(2014,5), orig(2020,11), orig(2013,19)]
l47_v2_orig = [orig(2015,11), orig(2015,3), orig(2013,10), orig(2014,22)]

l47 = lesson("l47", 47, "Szukaj wzoru zamiast liczyc", "lamiglowki", 14,
    "Kangurek 24 zadania w 75 minut = 3 minuty na zadanie. Liczenie kazdego elementu po kolei to przegrana. Znacznie szybciej: znajdz WZOR, ZAREGULE, klucz - i policz raz, potem uogolnij. To trenowanie 'matematycznej intuicji'.",
    "Sztuczka 1: SUMA 1+2+...+N = N RAZY (N+1) PRZEZ 2. Nie sumuj po kolei! Suma 1-10 = 10*11/2 = 55. Suma 1-100 = 100*101/2 = 5050.\n\nSztuczka 2: ROZNICE STALE = CIAG ARYTMETYCZNY. Jezeli kazdy kolejny element ma roznice stala, wyciagasz wzor: a + (n-1)*d.\n\nSztuczka 3: ODWRACANIE OPERACJI. Wynik 100, ostatnio mnozono przez 5: cofnij dzielac. Lancuch operacji rozwijasz wstecz.\n\nSztuczka 4: PARZYSTOSC I OSTATNIA CYFRA. Czesto wystarczy sprawdzic parzystosc albo ostatnia cyfre wyniku, by wyeliminowac 3 z 5 odpowiedzi.",
    "Pulapka: zadanie 'ile sposobow' z konkretnymi liczbami pyta o WZOR, nie pelne wypisanie. Wzor pozwala odpowiedziec w 10 sekund, wypisanie - w 10 minut. Trenuj rozpoznawanie wzorow.",
    ver("v1", "Wersja 1 (oryginalna)",
        [gen(47,"v1","w1","3pkt","lamiglowki","suma 1 do N",
            "Ile to 1 + 2 + 3 + ... + 10?",
            {"A":"45","B":"50","C":"55","D":"60","E":"100"},"C"),
         gen(47,"v1","w2","3pkt","lamiglowki","ciag arytmetyczny",
            "Jaki bedzie 10. element w ciagu 2, 5, 8, 11, 14...?",
            {"A":"23","B":"26","C":"29","D":"32","E":"35"},"C"),
         gen(47,"v1","w3","3pkt","lamiglowki","cykle dni",
            "Dzis sroda. Jaki dzien bedzie za 700 dni?",
            {"A":"Poniedzialek","B":"Wtorek","C":"Sroda","D":"Czwartek","E":"Niedziela"},"C"),
         l47_v1_orig[0], l47_v1_orig[1]],
        [l47_v1_orig[2], l47_v1_orig[3]],
        [sol("gen-l47-v1-w1","Wzor: n*(n+1)/2 = 10*11/2.","Wzor na sume.",["10*11/2 = 55"],"C"),
         sol("gen-l47-v1-w2","a + (n-1)*d = 2 + 9*3 = 29.","Wzor ciagu.",["2 + 9*3 = 2+27 = 29"],"C"),
         sol("gen-l47-v1-w3","700:7 = 100, reszta 0.","Wzor cykliczny.",["700:7=100 reszta 0, ten sam dzien"],"C"),
         osol(l47_v1_orig[0],"Tabelka kolorowanka wynik 20. Pole z 2+10, 16+4, 19+1 - kolorowanka A."),
         osol(l47_v1_orig[1],"Marysia kolejne roznice: 0,1,2,3,4,5. Polacz kropki E."),
         osol(l47_v1_orig[2],"Kangur 7 schodkow gora, krolik 3 dol, 100 schodkow. Spotykaja na 70."),
         osol(l47_v1_orig[3],"Cyfra 5 pojawia sie 16 razy w numeracji. Max stron: 102 lat (rok 2115).")]),
    ver("v2", "Wersja 2 (powtorka)",
        [gen(47,"v2","w1","3pkt","lamiglowki","suma duza",
            "Ile to 1 + 2 + 3 + ... + 20?",
            {"A":"100","B":"150","C":"200","D":"210","E":"400"},"D"),
         gen(47,"v2","w2","3pkt","lamiglowki","odwrocenie",
            "Mysle liczbe. Mnoze przez 5, dodaje 3, wynik 38. Jaka liczba?",
            {"A":"5","B":"6","C":"7","D":"8","E":"10"},"C"),
         gen(47,"v2","w3","3pkt","lamiglowki","parzystosc",
            "Suma trzech nieparzystych liczb jest:",
            {"A":"Parzysta","B":"Nieparzysta","C":"Raz tak raz tak","D":"Zerem","E":"Niewiazoma"},"B"),
         l47_v2_orig[0], l47_v2_orig[1]],
        [l47_v2_orig[2], l47_v2_orig[3]],
        [sol("gen-l47-v2-w1","Wzor: 20*21/2 = 210.","Wzor sumy.",["20*21/2 = 210"],"D"),
         sol("gen-l47-v2-w2","Cofnij: (38-3):5 = 35:5 = 7.","Odwrocenie operacji.",["38-3=35, 35:5=7"],"C"),
         sol("gen-l47-v2-w3","Niepar+nieprar=par, par+nieprar=nieprar.","Parzystosc sumy.",["3 niepar = nieprar"],"B"),
         osol(l47_v2_orig[0],"Tomek 16 nieb kulek. 3 nieb=1 czerw, 2 czerw=5 zielonych. Max 10 zielonych."),
         osol(l47_v2_orig[1],"Helenka rownania: tr+4=7, kw+tr=9. Tr=3, kw=6."),
         osol(l47_v2_orig[2],"Pelna szklanka 400g, pusta 100g. Polowka wody=150g, razem 250g."),
         osol(l47_v2_orig[3],"Cyfry 0-6 w diagram a+b=c, dwucyfrowe+dwucyfrowe=trzycyfrowe. Cyfra w polu szarym=5.")]),
    [dict(q="Suma 1+2+...+100 to:",
          choices={"A":"500","B":"5050","C":"50000"}, correct="B",
          explain="100*101/2 = 5050."),
     dict(q="W ciagu z stala roznica wzor to:",
          choices={"A":"a+n*d","B":"a+(n-1)*d","C":"n!"}, correct="B",
          explain="N-ty wyraz: a + (n-1)*roznica."),
     dict(q="Najszybsze sprawdzenie odpowiedzi to:",
          choices={"A":"Parzystosc lub ostatnia cyfra","B":"Pelne liczenie","C":"Zgadywanie"}, correct="A",
          explain="Parzystosc/cyfra koncowa eliminuja czesc odpowiedzi natychmiast.")])
LESSONS.append(l47)

# ================= LEKCJA 48: Eliminacja ABCDE =================
l48_v1_orig = [orig(2013,1), orig(2016,1), orig(2016,7), orig(2021,5)]
l48_v2_orig = [orig(2014,4), orig(2018,4), orig(2019,2), orig(2020,2)]

l48 = lesson("l48", 48, "Eliminacja odpowiedzi ABCDE", "lamiglowki", 14,
    "Kazda odpowiedz w Kangurku to A, B, C, D albo E - jedna z 5. Zamiast szukac poprawnej, ELIMINUJ niepoprawne. Czesto 3 z 5 mozna wyrzucic w 10 sekund - zostaja 2, miedzy ktorymi wybierasz dokladniej.",
    "Sztuczka 1: ROZMIAR. Jezeli wynik powinien byc okolo 50, odpowiedzi 5 i 500 mozna wyrzucic od razu.\n\nSztuczka 2: PARZYSTOSC. Wynik MUSI byc parzysty/nieparzysty? Wyrzuc te o zlej parzystosci.\n\nSztuczka 3: OSTATNIA CYFRA. 23 razy 7 - 3*7=21, ostatnia 1. Z odpowiedzi szukaj tylko konczacych sie na 1.\n\nSztuczka 4: SENS. Liczba dzieci ujemna? Negatywne pole? Zero powierzchni? Eliminuj 'niemozliwe' odpowiedzi.",
    "Pulapka: nie WSZYSTKIE odpowiedzi sa eliminowane technikami. Zostaja 2-3 'realnie mozliwe'. Tutaj juz musisz sprawdzic dokladniej. Eliminacja to sposob na PRZYSPIESZENIE, nie na pominiecie liczenia w 100%.",
    ver("v1", "Wersja 1 (oryginalna)",
        [gen(48,"v1","w1","3pkt","lamiglowki","eliminacja parzystosci",
            "Suma trzech parzystych. Eliminuj odpowiedzi nieparzyste. Ktorych odpowiedzi NIE eliminujesz?",
            {"A":"7","B":"8","C":"11","D":"13","E":"15"},"B"),
         gen(48,"v1","w2","3pkt","lamiglowki","eliminacja rozmiaru",
            "Liczba dzieci w klasie. Ktora odpowiedz NA PEWNO NIE pasuje?",
            {"A":"20","B":"25","C":"100","D":"30","E":"15"},"C"),
         gen(48,"v1","w3","3pkt","lamiglowki","eliminacja ostatniej cyfry",
            "13 razy 4 - ostatnia cyfra wyniku to 3*4=12, czyli 2. Ktora odpowiedz pasuje?",
            {"A":"50","B":"51","C":"52","D":"53","E":"54"},"C"),
         l48_v1_orig[0], l48_v1_orig[1]],
        [l48_v1_orig[2], l48_v1_orig[3]],
        [sol("gen-l48-v1-w1","Suma parzystych = parzysta. Tylko 8 parzysta.","Parzystosc.",["8 jedyna parzysta"],"B"),
         sol("gen-l48-v1-w2","100 dzieci to za duzo na klase.","Rozmiar.",["Klasa max 30-40, 100 niemoz."],"C"),
         sol("gen-l48-v1-w3","Ostatnia cyfra 52 = 2.","Ostatnia cyfra.",["13*4=52, kon. 2"],"C"),
         osol(l48_v1_orig[0],"Czarnych kangurow wiecej niz bialych - rysunek D."),
         osol(l48_v1_orig[1],"Ania, Basia, Cesia, Dorotka, Ela kostka 2 razy. Dorotka najwiecej oczek."),
         osol(l48_v1_orig[2],"Ania i 5 kolezanek dziela jablka po pol - 3 jablka."),
         osol(l48_v1_orig[3],"Franek 5 tarcz, 3 strzaly kazda. Najwiecej Franek - tarcza A.")]),
    ver("v2", "Wersja 2 (powtorka)",
        [gen(48,"v2","w1","3pkt","lamiglowki","eliminacja zerem",
            "Pole prostokata 5x4 cm. Ktora odpowiedz NA PEWNO NIE pasuje?",
            {"A":"15","B":"20","C":"0","D":"22","E":"25"},"C"),
         gen(48,"v2","w2","3pkt","lamiglowki","kazda eliminacja",
            "Cyfra ostatnia 27*3 to 7*3=21, czyli 1. Ktora odp pasuje?",
            {"A":"80","B":"81","C":"82","D":"83","E":"84"},"B"),
         gen(48,"v2","w3","3pkt","lamiglowki","logiczna eliminacja",
            "Liczba minut w godzinie - ktora odp NA PEWNO bledna?",
            {"A":"15","B":"30","C":"60","D":"100","E":"45"},"D"),
         l48_v2_orig[0], l48_v2_orig[1]],
        [l48_v2_orig[2], l48_v2_orig[3]],
        [sol("gen-l48-v2-w1","Pole 5*4=20. 0 niemozliwe.","Eliminacja zerem.",["Pole nie moze byc 0"],"C"),
         sol("gen-l48-v2-w2","Ostatnia cyfra 81 = 1.","Ostatnia cyfra.",["27*3=81, kon.1"],"B"),
         sol("gen-l48-v2-w3","Godzina ma 60 minut. 100 niemozliwe.","Granica wartosci.",["60 max"],"D"),
         osol(l48_v2_orig[0],"Koala 50 g lisci na godz. Spal 13 godz, nie 11. 550 g."),
         osol(l48_v2_orig[1],"Biedronka Misia 5 kropek prawo, 3 lewo. NIE jest biedronka C."),
         osol(l48_v2_orig[2],"Trzecie miejsce na podium = zawodnik nr 2."),
         osol(l48_v2_orig[3],"Grzyb rosnie codziennie. Wtorek = drugi dzien = drugie zdjecie B.")]),
    [dict(q="Eliminacja przez ostatnia cyfre:",
          choices={"A":"Wystarcza","B":"Szybko zawegza pole","C":"Nigdy nie pomaga"}, correct="B",
          explain="Szybko zostaje 1-2 odpowiedzi."),
     dict(q="100 dzieci w klasie:",
          choices={"A":"Mozliwe","B":"Niemozliwe","C":"Zalezy"}, correct="B",
          explain="Typowa klasa 25-30 dzieci, 100 jest absurdalne."),
     dict(q="Eliminacja zostawia zwykle:",
          choices={"A":"Wszystkie","B":"1-2 odpowiedzi","C":"Zero"}, correct="B",
          explain="Zwykle zostaja 2 realne odpowiedzi.")])
LESSONS.append(l48)

# ================= LEKCJA 49: Symulacja konkursu cz. 1 =================
l49_problems_3pkt = [
    orig(2012,1), orig(2012,4), orig(2012,5), orig(2015,1),
    orig(2015,2), orig(2015,4), orig(2015,6), orig(2015,7)
]
l49_problems_4pkt = [
    orig(2013,13), orig(2013,14), orig(2014,9), orig(2015,13)
]

l49 = lesson("l49", 49, "Symulacja konkursu Kangur - czesc 1", "lamiglowki", 35,
    "Pierwsza polowa pelnego konkursu Kangur Maluch: 12 zadan, 35 minut. Zadania 1-8 za 3 punkty, 9-12 za 4 punkty. To trening pod presja czasu. Nie sprawdzaj odpowiedzi po kazdym zadaniu - rozwiazuj cala czesc, potem sprawdz.",
    "Sztuczka 1: ZARZADZAJ CZASEM. 35 min na 12 zadan = ~3 min na zadanie. Latwiejsze (3pkt) szybciej, na 4pkt mozesz wiecej.\n\nSztuczka 2: NIE UTKNIJ. Jezeli nie wiesz po 3 min - pomiń, idź dalej. Wrocisz na koncu.\n\nSztuczka 3: ZAZNACZAJ OPCJE. Lekko zaznaczaj 'mozliwe' i 'eliminuj'. Latwiej wrocic.\n\nSztuczka 4: SPRAWDZAJ KAZDA ODPOWIEDZ. Po wyborze ABCDE - spojrz jeszcze raz na zadanie. Czy odpowiadasz na to, o co pytaja?",
    "W konkursie liczy sie kazda sekunda. Trenuj rozpoznawanie 'typowych' zadan Kangurka - jezeli widzisz cos podobnego do tego, co juz robiles, masz przewage. Symulacja to wlasnie ten trening.",
    ver("v1", "Wersja 1 (oryginalna)",
        l49_problems_3pkt,
        l49_problems_4pkt,
        [osol(l49_problems_3pkt[0],"Slowo MATEMATYKA: 6 unikalnych liter (M,A,T,E,Y,K)."),
         osol(l49_problems_3pkt[1],"Iza zaciemnila pola w tabeli 4x4 - wzor D."),
         osol(l49_problems_3pkt[2],"15 dzieci, znaleziono 10, bez Klaudii - 14 chowajacych - 10 = 4."),
         osol(l49_problems_3pkt[3],"Lancuch dzialan: 2-0+1=3, 3*5=15."),
         osol(l49_problems_3pkt[4],"Stas 10 paskow polaczyl po 2 - najdluzszy B."),
         osol(l49_problems_3pkt[5],"Najwiekszy iloraz: (1000-1):9 = 999:9 = 111 - C."),
         osol(l49_problems_3pkt[6],"Iloczyn cyfr 2-cyf liczby = 15 (np. 35). Suma 3+5=8."),
         osol(l49_problems_3pkt[7],"Zaby na wyspie z palma - 6."),
         osol(l49_problems_4pkt[0],"30 uczniow, niem 15, ang 20. Wspolnych: 15+20-30=5."),
         osol(l49_problems_4pkt[1],"Liczby 22, 24, 25 podzielne przez cyfre jednosci - 3 ciekawe."),
         osol(l49_problems_4pkt[2],"Z OARGONKA do KANGAROO min 5 zamian."),
         osol(l49_problems_4pkt[3],"10 zawodnikow, przed Frankiem o 3 mniej niz za. 4. miejsce.")]),
    ver("v2", "Wersja 2 (powtorka)",
        l49_problems_3pkt,
        l49_problems_4pkt,
        [osol(l49_problems_3pkt[0],"6 unikalnych liter w MATEMATYKA."),
         osol(l49_problems_3pkt[1],"Wzor pol Izy - D."),
         osol(l49_problems_3pkt[2],"15-Klaudia-10znalezionych = 4 nieznalezionych."),
         osol(l49_problems_3pkt[3],"2-0+1=3, 3*5=15."),
         osol(l49_problems_3pkt[4],"Najdluzszy pasek B."),
         osol(l49_problems_3pkt[5],"(1000-1):9 = 111 = najwiekszy."),
         osol(l49_problems_3pkt[6],"3*5=15, 3+5=8."),
         osol(l49_problems_3pkt[7],"6 zab na wyspie."),
         osol(l49_problems_4pkt[0],"15+20-30=5 uczniow dwoch jezykow."),
         osol(l49_problems_4pkt[1],"22, 24, 25 ciekawe (3)."),
         osol(l49_problems_4pkt[2],"5 zamian liter dla KANGAROO."),
         osol(l49_problems_4pkt[3],"Franek na 4. miejscu.")]),
    [dict(q="Ile zadan w pierwszej polowie konkursu?",
          choices={"A":"10","B":"12","C":"24"}, correct="B",
          explain="Polowa z 24 zadan = 12."),
     dict(q="Ile czasu na 1 zadanie srednio?",
          choices={"A":"1 min","B":"3 min","C":"10 min"}, correct="B",
          explain="35 min : 12 zadan = ~3 min."),
     dict(q="Co robic gdy utkniesz?",
          choices={"A":"Pomiń, wroc pozniej","B":"Siedziec az do konca","C":"Zostawic"}, correct="A",
          explain="Pomijasz, idziesz dalej, wracasz na koniec.")])
LESSONS.append(l49)

# ================= LEKCJA 50: Symulacja konkursu cz. 2 + omowienie =================
l50_problems_4pkt = [
    orig(2015,16), orig(2016,9), orig(2016,13), orig(2016,14)
]
l50_problems_5pkt = [
    orig(2012,18), orig(2012,19), orig(2012,23), orig(2013,20),
    orig(2013,23), orig(2013,24), orig(2014,24), orig(2018,18)
]

l50 = lesson("l50", 50, "Symulacja konkursu Kangur - czesc 2 + omowienie", "lamiglowki", 40,
    "Druga polowa konkursu - 12 zadan, 40 minut. Zadania 13-16 za 4 punkty, 17-24 za 5 punktow. To najtrudniejsza czesc - ale tez najwiecej punktow. Po skonczeniu - sprawdz, omow z nauczycielem, naucz sie na bledach. To OSTATNIA lekcja kursu.",
    "Sztuczka 1: 5 PUNKTOW = WARTO SIE POTRUDZIC. Na 5 pkt zadania moga zajac 5-7 min - czas dobrze zainwestowany.\n\nSztuczka 2: NIE BOJ SIE POMINAC. Jezeli zadanie wyglada na 'beznadziejne' - lepiej zrobic 3 inne na 5 pkt = 15 pkt, niz utkac.\n\nSztuczka 3: SPRAWDZ STRATEGIE Z POPRZEDNICH LEKCJI. Eliminacja ABCDE, szukanie wzoru, parzystosc - to wszystko teraz sluzy.\n\nSztuczka 4: PO SYMULACJI - OMOW BLEDY. Najwazniejsza nauka to zrozumienie, GDZIE poszlo nie tak. Nie tylko 'co byla poprawna odpowiedz', ale 'jakim sposobem dojsc do niej'.",
    "Po pelnej symulacji wiesz, gdzie sa Twoje slabe punkty. Wroc do tych blokow w kursie. Powtorz wersje 2 lekcji w slabych obszarach. Powtorka 2-3 razy ZNACZNIE poprawia wyniki. Sukces w Kangurku to praca, nie talent.",
    ver("v1", "Wersja 1 (oryginalna)",
        l50_problems_4pkt,
        l50_problems_5pkt,
        [osol(l50_problems_4pkt[0],"5 biedronek, sasiednie roznia kropki o 1. 8 SMS-ow."),
         osol(l50_problems_4pkt[1],"Lap psow o 18 wiecej niz nosow. 6 psow (kazdy 3 wiecej)."),
         osol(l50_problems_4pkt[2],"11 miejsc parkingowych, 8 kolejnych zajete. Na pewno zajete: 5."),
         osol(l50_problems_4pkt[3],"Suma 4 liczb na 2 kartach = 32, kazda karta = 16. 5->11, 12->4."),
         osol(l50_problems_5pkt[0],"Pchla schody, skoki +3/-4. Min liczba do 22. stopnia: 12."),
         osol(l50_problems_5pkt[1],"Prostokat 192x84 mm. NMW=12. Najmniejszy kwadrat 12 mm."),
         osol(l50_problems_5pkt[2],"38 meczow, 80 pkt, max porazek: 10 (26 wygranych, 2 remisy)."),
         osol(l50_problems_5pkt[3],"7 kamieni domino w rzad z rownymi sasiadami. Maks 6 kamieni."),
         osol(l50_problems_5pkt[4],"Emilka rozwiesila 35 recznikow, 58 klamerek. Sposob 1: 22 reczniki."),
         osol(l50_problems_5pkt[5],"Komoda 4 szuflady z warunkami. Uklad C: Czapki, Szaliki, Rekawiczki, Parasolki."),
         osol(l50_problems_5pkt[6],"Tabelka 3x3 z 1-9, warunki na liczby 5 i 6. Srodek = 8."),
         osol(l50_problems_5pkt[7],"Bajkowy jezyk z symbolami 1-5. Symbol = 3 to oko (A).")]),
    ver("v2", "Wersja 2 (powtorka)",
        l50_problems_4pkt,
        l50_problems_5pkt,
        [osol(l50_problems_4pkt[0],"8 SMS-ow miedzy przyjaciolkami biedronkami."),
         osol(l50_problems_4pkt[1],"6 psow daje +18 lap nad nosami."),
         osol(l50_problems_4pkt[2],"Miejsce 5 zawsze zajete (przeciecie wszystkich blokow 8 z 11)."),
         osol(l50_problems_4pkt[3],"Niewidoczne strony kart: 11 i 4."),
         osol(l50_problems_5pkt[0],"12 skokow pchly do 22. stopnia (3a-4b=22, a+b min)."),
         osol(l50_problems_5pkt[1],"NMW(192,84)=12, najmniejszy kwadrat 12 mm."),
         osol(l50_problems_5pkt[2],"Max porazek 10."),
         osol(l50_problems_5pkt[3],"Najdluzszy rzad domino 6 kamieni."),
         osol(l50_problems_5pkt[4],"22 reczniki sposobem 1."),
         osol(l50_problems_5pkt[5],"Komoda wedlug warunkow - uklad C."),
         osol(l50_problems_5pkt[6],"Srodek tabeli = 8."),
         osol(l50_problems_5pkt[7],"Symbol 3 = oko.")]),
    [dict(q="Po symulacji najwazniejsze:",
          choices={"A":"Wynik","B":"Omowic bledy","C":"Zapomnec"}, correct="B",
          explain="Zrozumienie bledow daje najwiecej nauki."),
     dict(q="Zadanie za 5 pkt warte:",
          choices={"A":"Pominac","B":"Potrudzic sie","C":"Zgadnac"}, correct="B",
          explain="5 pkt to duzo - warte 5-7 min uwagi."),
     dict(q="Klucz do sukcesu w Kangurku:",
          choices={"A":"Talent","B":"Trening i powtorki","C":"Szczescie"}, correct="B",
          explain="Powtorka + analiza bledow = sukces.")])
LESSONS.append(l50)

# ================= ZAPIS =================
for les in LESSONS:
    with open(f"data/lessons/{les['id']}.json", "w", encoding="utf-8") as f:
        json.dump(les, f, ensure_ascii=False, indent=2)
    print(f"{les['id']}: OK ({les['title']})")
print(f"DONE - {len(LESSONS)} lekcji")
