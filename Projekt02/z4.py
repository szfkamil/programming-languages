def czy_wczesniejsza(data1: dict, data2: dict) -> bool:
    """
    Porównuje dwie daty reprezentowane jako słowniki.
    Zwraca True, jeśli data1 jest chronologicznie mniejsza (wcześniejsza) niż data2.
    """
    if data1["rok"] != data2["rok"]:
        return data1["rok"] < data2["rok"]
        
    # Miesiąc (sprawdzany tylko gdy lata są równe)
    if data1["miesiac"] != data2["miesiac"]:
        return data1["miesiac"] < data2["miesiac"]
        
    # Dzień (sprawdzany tylko gdy lata i miesiące są równe)
    return data1["dzien"] < data2["dzien"]

def sortowanie_przez_wstawianie(tablica_dat: list[dict]) -> None:
    """
    Sortuje listę słowników (dat) rosnąco algorytmem Insertion Sort.
    Modyfikuje przekazaną listę w miejscu.
    """
    n = len(tablica_dat)
    
    for i in range(1, n):
        klucz = tablica_dat[i]
        j = i - 1 # wskazuje na ostatni element w posortowanej części
        
        # Przesuwamy elementy podtablicy posortowanej, które są chronologicznie
        # późniejsze od 'klucza', o jedną pozycję w prawo.
        while j >= 0 and czy_wczesniejsza(klucz, tablica_dat[j]):
            tablica_dat[j + 1] = tablica_dat[j]
            j -= 1
            
        tablica_dat[j + 1] = klucz

# Inicjalizacja danych wejściowych 
daty_do_posortowania = [
    {"dzien": 15, "miesiac": 10, "rok": 2023},
    {"dzien": 1, "miesiac": 1, "rok": 2024},
    {"dzien": 15, "miesiac": 10, "rok": 2022},
    {"dzien": 5, "miesiac": 10, "rok": 2023},
    {"dzien": 28, "miesiac": 2, "rok": 2024}
]

sortowanie_przez_wstawianie(daty_do_posortowania)

print("Posortowane daty:")
for data in daty_do_posortowania:
    # Użycie formatowania z zerem wiodącym (np. 05 zamiast 5) dla czytelności
    print(f"{data['dzien']:02d}-{data['miesiac']:02d}-{data['rok']}")