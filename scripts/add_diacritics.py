"""Dodaje polskie znaki diakrytyczne do tekstu w lekcjach (statements, choices, solutions,
hints, theory, quiz). Uzywa slownika typowych slow matematycznych.

Dziala na wszystkich polach tekstowych z wyjatkiem id, source, year, number, correct."""
import json
import re
from pathlib import Path

# Slownik ASCII -> diacritic (czeste slowa w zadaniach matematycznych)
# Format: ascii_word -> polish_word (case-sensitive, ale zostaje aplikowany case-insensitive)
DIACRITICS = {
    # Czeste czasowniki
    "uloz": "ułóż", "ulozyc": "ułożyć", "ulozyl": "ułożył", "ulozyla": "ułożyła",
    "ulozyc": "ułożyć", "ulozyli": "ułożyli", "uloza": "ułożą",
    "wpisz": "wpisz", "wpisac": "wpisać", "wpisal": "wpisał", "wpisala": "wpisała",
    "policz": "policz", "policzyc": "policzyć", "policzyl": "policzył", "policzyla": "policzyła",
    "podzielic": "podzielić", "podzielono": "podzielono", "podzielil": "podzielił",
    "wybierz": "wybierz", "wybrac": "wybrać", "wybral": "wybrał", "wybrala": "wybrała",
    "narysuj": "narysuj", "narysowac": "narysować", "narysowal": "narysował", "narysowala": "narysowała",
    "narysowano": "narysowano",
    "zaznaczyc": "zaznaczyć", "zaznacz": "zaznacz",
    "obliczyc": "obliczyć", "oblicz": "oblicz", "obliczyl": "obliczył", "obliczyla": "obliczyła",
    "kupil": "kupił", "kupila": "kupiła", "kupili": "kupili", "kupic": "kupić",
    "dostal": "dostał", "dostala": "dostała", "dostali": "dostali",
    "rozdac": "rozdać", "rozdal": "rozdał", "rozdala": "rozdała",
    "byl": "był", "byla": "była", "bylo": "było", "byli": "byli", "byly": "były",
    "miec": "mieć", "ma": "ma", "mial": "miał", "miala": "miała", "mialo": "miało",
    "mieli": "mieli", "mialy": "miały",
    "wziac": "wziąć", "wzial": "wziął", "wziela": "wzięła", "wzielo": "wzięło", "wzieto": "wzięto",
    "zostawil": "zostawił", "zostawila": "zostawiła", "zostalo": "zostało",
    "zjadl": "zjadł", "zjadla": "zjadła", "zjedli": "zjedli", "zjesc": "zjeść",
    "wynosi": "wynosi", "wyniesie": "wyniesie", "wyniku": "wyniku",
    "stanela": "stanęła", "stanal": "stanął", "stoja": "stoją",
    "siedzi": "siedzi", "siedza": "siedzą", "siedzaca": "siedzącą",
    "patrzy": "patrzy", "popatrz": "popatrz",
    "rozni": "różni", "roznia": "różnią", "rozne": "różne", "roznych": "różnych",
    "rozna": "różna", "rozny": "różny",
    "moga": "mogą", "moze": "może", "moglby": "mógłby", "mozna": "można",
    "musi": "musi", "musza": "muszą", "musial": "musiał",
    "wie": "wie", "wiedzac": "wiedząc",
    "zapisuje": "zapisuje", "zapisac": "zapisać", "zapisal": "zapisał",
    "rozdziela": "rozdziela", "rozdzielic": "rozdzielić",
    "rozszczepia": "rozszczepia",
    "pomyslal": "pomyślał", "pomysl": "pomyśl",
    "uzywaja": "używają", "uzywal": "używał", "uzyl": "użył", "uzyc": "użyć",
    "konczy": "kończy", "konca": "końca", "koniec": "koniec",
    "wraca": "wraca", "wrocic": "wrócić", "wrocila": "wróciła",
    "schodzi": "schodzi", "schodzic": "schodzić",

    # Liczebniki / okreslenia ilosci
    "dwoch": "dwóch", "trzech": "trzech", "czterech": "czterech",
    "pieciu": "pięciu", "szesciu": "sześciu", "siedmiu": "siedmiu",
    "osmiu": "ośmiu", "dziewieciu": "dziewięciu", "dziesieciu": "dziesięciu",
    "tysiac": "tysiąc", "tysiaca": "tysiąca", "tysiece": "tysiące",
    "piec": "pięć", "szesc": "sześć", "osiem": "osiem", "dziewiec": "dziewięć",
    "dziesiec": "dziesięć",
    "dwunascie": "dwunaście", "trzynascie": "trzynaście", "czternascie": "czternaście",
    "pietnascie": "piętnaście", "szesnascie": "szesnaście",
    "siedemnascie": "siedemnaście", "osiemnascie": "osiemnaście", "dziewietnascie": "dziewiętnaście",
    "dwadziescia": "dwadzieścia",
    "wszystko": "wszystko", "wszystkie": "wszystkie", "wszystkich": "wszystkich",
    "wszyscy": "wszyscy", "wszystkim": "wszystkim",
    "polowa": "połowa", "polowe": "połowę", "polowy": "połowy", "polowie": "połowie",
    "polowke": "połówkę",
    "kazdy": "każdy", "kazda": "każda", "kazde": "każde", "kazdym": "każdym",
    "kazdej": "każdej", "kazdego": "każdego", "kazdym": "każdym", "kazdemu": "każdemu",
    "rowno": "równo", "rowna": "równa", "rowne": "równe", "rownych": "równych",
    "rownosc": "równość", "rownosci": "równości", "rownej": "równej", "rownie": "równie",
    "rownowadze": "równowadze",
    "wiecej": "więcej", "mniej": "mniej",

    # Rzeczowniki
    "ksiazka": "książka", "ksiazke": "książkę", "ksiazek": "książek", "ksiazki": "książki",
    "ksiazkach": "książkach", "ksiazkowy": "książkowy",
    "klocek": "klocek", "klocki": "klocki", "klockow": "klocków", "klockami": "klockami",
    "stol": "stół", "stoly": "stoły", "stolow": "stołów", "stole": "stole",
    "dom": "dom", "domu": "domu", "domow": "domów", "domek": "domek",
    "dziecko": "dziecko", "dzieci": "dzieci", "dziecmi": "dziećmi",
    "lacznie": "łącznie", "laczny": "łączny", "laczna": "łączna",
    "lacze": "łączę", "polaczyl": "połączył", "polaczyc": "połączyć",
    "patyczki": "patyczki", "patyczek": "patyczek", "patyczkow": "patyczków",
    "olowek": "ołówek", "olowki": "ołówki", "olowkow": "ołówków",
    "owoc": "owoc", "owoce": "owoce", "owocow": "owoców",
    "jablko": "jabłko", "jablka": "jabłka", "jablek": "jabłek", "jablek": "jabłek",
    "lod": "lód", "lody": "lody", "lodow": "lodów", "lodzie": "lodzie", "lodow": "lodów",
    "kazda": "każda", "kazdym": "każdym",
    "jaglki": "jabłka", "wszystkim": "wszystkim",
    "drzewa": "drzewa", "drzewo": "drzewo", "drzew": "drzew",
    "obraz": "obraz", "obrazek": "obrazek", "obrazki": "obrazki", "obrazkow": "obrazków",
    "rysunek": "rysunek", "rysunki": "rysunki", "rysunku": "rysunku",
    "obrocenie": "obrócenie", "obrocony": "obrócony", "obroc": "obróć",
    "polowie": "połowie", "polowa": "połowa", "polowy": "połowy",
    "kraj": "kraj", "kraju": "kraju", "krajow": "krajów",
    "klasa": "klasa", "klasy": "klasy", "klasie": "klasie",
    "uczen": "uczeń", "uczniow": "uczniów", "uczniowie": "uczniowie",
    "ucznia": "ucznia", "uczennica": "uczennica",
    "matematyczny": "matematyczny", "matematyka": "matematyka", "matematyki": "matematyki",
    "konkurs": "konkurs", "konkursowy": "konkursowy",
    "punkty": "punkty", "punkt": "punkt", "punktow": "punktów", "punktem": "punktem",
    "punktach": "punktach", "punktow": "punktów",
    "minuta": "minuta", "minuty": "minuty", "minut": "minut", "minute": "minutę",
    "godzina": "godzina", "godziny": "godziny", "godzin": "godzin", "godzine": "godzinę",
    "dzien": "dzień", "dnia": "dnia", "dni": "dni",
    "tydzien": "tydzień", "tygodnia": "tygodnia", "tygodni": "tygodni",
    "miesiac": "miesiąc", "miesiace": "miesiące", "miesiecy": "miesięcy",
    "rok": "rok", "roku": "roku", "lat": "lat",
    "kwadrat": "kwadrat", "kwadraty": "kwadraty", "kwadratow": "kwadratów",
    "kwadracie": "kwadracie",
    "trojkat": "trójkąt", "trojkata": "trójkąta", "trojkaty": "trójkąty",
    "trojkatow": "trójkątów", "trojkacie": "trójkącie",
    "kolko": "kółko", "kolka": "kółka", "kol": "kół",
    "kolo": "koło", "kola": "koła",
    "ucho": "ucho", "ust": "ust",
    "noga": "noga", "nogi": "nogi", "nog": "nóg",
    "ekran": "ekran",
    "wodzie": "wodzie", "wody": "wody", "woda": "woda",
    "babcia": "babcia", "babci": "babci",
    "mama": "mama", "tato": "tato", "tata": "tata",
    "siostra": "siostra", "siostry": "siostry", "siostrze": "siostrze",
    "brat": "brat", "brata": "brata", "braci": "braci",
    "kolega": "kolega", "kolegi": "kolegi", "kolegow": "kolegów",
    "kolezanke": "koleżankę", "kolezanki": "koleżanki", "kolezanka": "koleżanka",
    "klamerka": "klamerka", "klamerki": "klamerki", "klamerek": "klamerek",
    "kostka": "kostka", "kostki": "kostki", "kostek": "kostek",
    "kropka": "kropka", "kropki": "kropki", "kropek": "kropek",
    "linijka": "linijka", "linijki": "linijki",
    "sciezka": "ścieżka", "scieżki": "ścieżki",
    "swiec": "świec", "swieca": "świeca", "swiece": "świecę",
    "zwierze": "zwierzę", "zwierzeta": "zwierzęta", "zwierzat": "zwierząt",
    "krolik": "królik", "krolika": "królika", "krolikow": "królików",
    "krowa": "krowa", "krowy": "krowy",
    "ges": "gęś", "gesi": "gęsi",
    "owca": "owca", "owce": "owce", "owieczek": "owieczek", "owieczki": "owieczki",
    "kura": "kura", "kury": "kury",
    "pies": "pies", "psa": "psa", "psy": "psy", "psow": "psów",
    "kot": "kot", "koty": "koty", "kotow": "kotów",
    "pajak": "pająk", "pajaki": "pająki", "pajakow": "pająków",
    "swieczka": "świeczka", "swieczki": "świeczki", "swieczke": "świeczkę",

    # Przymiotniki
    "rowny": "równy", "rowna": "równa", "rowne": "równe",
    "wlasciwy": "właściwy", "wlasciwa": "właściwa", "wlasciwie": "właściwie",
    "lawka": "ławka", "lawki": "ławki", "lawek": "ławek",
    "krotki": "krótki", "krotka": "krótka", "krotsze": "krótsze", "krotszy": "krótszy",
    "dluzszy": "dłuższy", "dluzsza": "dłuższa", "dluzsze": "dłuższe",
    "dlugi": "długi", "dluga": "długa", "dlugie": "długie", "dlugosc": "długość",
    "dlugosci": "długości", "dlugoscia": "długością",
    "wielki": "wielki", "wielka": "wielka", "wielkie": "wielkie",
    "maly": "mały", "mala": "mała", "male": "małe", "malych": "małych",
    "ladny": "ładny", "ladna": "ładna", "ladnie": "ładnie",
    "zolty": "żółty", "zolta": "żółta", "zolte": "żółte",
    "czerwony": "czerwony", "czerwona": "czerwona", "czerwone": "czerwone",
    "niebieski": "niebieski", "niebieska": "niebieska", "niebieskie": "niebieskie",
    "zielony": "zielony", "zielona": "zielona", "zielone": "zielone",
    "czarny": "czarny", "czarna": "czarna", "czarne": "czarne",
    "bialy": "biały", "biala": "biała", "biale": "białe",
    "okragly": "okrągły", "okragla": "okrągła", "okragle": "okrągłe",
    "okrazenie": "okrążenie", "okrazenia": "okrążenia",
    "swiatek": "świątek",
    "scisniety": "ściśnięty",

    # Spojniki, zaimki, przyslowki
    "ktora": "która", "ktory": "który", "ktore": "które", "ktorego": "którego",
    "ktorzy": "którzy", "ktorych": "których", "ktorej": "której", "ktorym": "którym",
    "moj": "mój", "moja": "moja", "moje": "moje",
    "twoj": "twój", "twoja": "twoja", "twoje": "twoje",
    "jezeli": "jeżeli", "jezeli": "jeżeli",
    "ze": "że", "moze": "może",
    "wlasnie": "właśnie", "wlasna": "własna", "wlasny": "własny",
    "tez": "też",
    "az": "aż", "az do": "aż do",
    "swoj": "swój", "swoja": "swoja", "swoje": "swoje", "swych": "swych",
    "sasiad": "sąsiad", "sasiednie": "sąsiednie", "sasiad": "sąsiad",
    "sasiedni": "sąsiedni", "sasiednia": "sąsiednia",

    # Czasowniki czasowe / orientacja
    "wczesniej": "wcześniej", "pozniej": "później", "poznym": "późnym",
    "wlasciwie": "właściwie",
    "obecnie": "obecnie", "obecny": "obecny",
    "wczoraj": "wczoraj", "dzis": "dziś", "jutro": "jutro",
    "rano": "rano", "wieczorem": "wieczorem", "wieczor": "wieczór",
    "poludnie": "południe", "polnoc": "północ",

    # Pol / strona
    "strona": "strona", "strony": "strony", "stron": "stron",
    "strone": "stronę", "stronie": "stronie",
    "lewy": "lewy", "lewa": "lewa", "lewo": "lewo", "lewej": "lewej",
    "prawy": "prawy", "prawa": "prawa", "prawo": "prawo", "prawej": "prawej",
    "gora": "góra", "gory": "góry", "gore": "górę", "gorny": "górny",
    "dol": "dół", "dolu": "dołu", "dolny": "dolny",
    "przod": "przód", "tyl": "tył", "tylu": "tyłu",
    "wzdluz": "wzdłuż", "obok": "obok", "przez": "przez",
    "miedzy": "między",
    "naprzeciw": "naprzeciw",

    # Inne
    "pojeczynczy": "pojedynczy", "pojedyncze": "pojedyncze",
    "uwazaj": "uważaj", "uwazac": "uważać", "uwazany": "uważany",
    "imie": "imię",
    "rece": "ręce", "ramie": "ramię",
    "drogi": "drogi", "droga": "droga", "drog": "dróg",
    "wedrowal": "wędrował", "wedruje": "wędruje",
    "spedza": "spędza", "spedzic": "spędzić", "spedzil": "spędził",
    "skok": "skok", "skoki": "skoki", "skokow": "skoków",
    "skoczy": "skoczy", "skacze": "skacze", "skoczyc": "skoczyć",
    "sciezka": "ścieżka", "scieżki": "ścieżki",
    "scianie": "ścianie", "sciany": "ściany",
    "rozmiaru": "rozmiaru", "rozmiary": "rozmiary",
    "rzutow": "rzutów", "rzucac": "rzucać", "rzucil": "rzucił",
    "trafil": "trafił", "trafic": "trafić", "trafia": "trafia",
    "lacznie": "łącznie", "lacznosc": "łączność",
    "kanapek": "kanapek", "kanapka": "kanapka",

    # Skrocone formy w popularnych zadaniach
    "stand": "stand",
    "nalezy": "należy",
    "kazdy": "każdy",
    "polowe": "połowę",
    "calosc": "całość", "caly": "cały", "calego": "całego",
    "calej": "całej", "calych": "całych",
}


# Skompiluj regex
def build_regex():
    keys = sorted(DIACRITICS.keys(), key=len, reverse=True)
    pattern = r"\b(" + "|".join(re.escape(k) for k in keys) + r")\b"
    return re.compile(pattern, re.IGNORECASE)


REGEX = build_regex()


def fix_text(text: str) -> str:
    if not text or any(c in text for c in "ąćęłńóśżźĄĆĘŁŃÓŚŻŹ"):
        # juz ma polskie znaki - nie ruszamy (oryginaly Kangurka)
        return text

    def repl(m: re.Match) -> str:
        orig = m.group(1)
        lower = orig.lower()
        if lower not in DIACRITICS:
            return orig
        repl_word = DIACRITICS[lower]
        # zachowaj wielkosc liter pierwsza
        if orig[0].isupper():
            repl_word = repl_word[0].upper() + repl_word[1:]
        return repl_word

    return REGEX.sub(repl, text)


def fix_obj(obj):
    if isinstance(obj, str):
        return fix_text(obj)
    elif isinstance(obj, list):
        return [fix_obj(x) for x in obj]
    elif isinstance(obj, dict):
        return {k: (fix_obj(v) if k not in {"id", "source", "correct", "answer", "problemId", "blockCode", "versionId"} else v)
                for k, v in obj.items()}
    return obj


DATA_DIR = Path("data/lessons")
modified = 0
for i in range(1, 51):
    lid = f"l{i:02d}"
    path = DATA_DIR / f"{lid}.json"
    with open(path, encoding="utf-8") as f:
        d = json.load(f)

    d_fixed = fix_obj(d)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(d_fixed, f, ensure_ascii=False, indent=2)
    modified += 1

print(f"Zmodyfikowano {modified} plikow lekcji")

# Pokaz statystyke
total_chars = 0
polish_chars = 0
for i in range(1, 51):
    with open(f"data/lessons/l{i:02d}.json", encoding="utf-8") as f:
        txt = f.read()
    total_chars += len(txt)
    polish_chars += sum(1 for c in txt if c in "ąćęłńóśżźĄĆĘŁŃÓŚŻŹ")
print(f"Polskie znaki: {polish_chars} z {total_chars} ({100*polish_chars/total_chars:.2f}%)")
