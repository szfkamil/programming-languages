import math

def suma_dzielnikow_wlasciwych(n: int) -> int:
    """
    Oblicza sumę wszystkich dzielników właściwych liczby n.
    """
    
    # Zwraca 0 dla n <= 1, ponieważ 1 nie ma dzielników właściwych mniejszych od siebie.
    if n <= 1:
        return 0
        
    # Jedynka jest zawsze dzielnikiem właściwym każdej liczby > 1
    suma = 1 
    limit = math.isqrt(n)
    
    for i in range(2, limit + 1):
        if n % i == 0:
            suma += i
            
            drugi_czynnik = n // i 
            
            # Mechanizm obronny przed liczbami będącymi pełnymi kwadratami, np 36 = 6*6
            if i != drugi_czynnik:
                suma += drugi_czynnik
                
    return suma

def wypisz_zaprzyjaznione(poczatek: int, koniec: int) -> None:
    """
    Wyszukuje i wypisuje pary liczb zaprzyjaźnionych w zadanym przedziale [poczatek, koniec].
    """
    for a in range(poczatek, koniec + 1):
        b = suma_dzielnikow_wlasciwych(a)
        
        # Warunek a < b zapobiega dwóm błędom logicznym:
        # 1. Wypisaniu liczb doskonałych (gdzie a == b)
        # 2. Powielaniu par (aby nie wypisać (220, 284) a później (284, 220))
        if a < b and b <= koniec:
            if suma_dzielnikow_wlasciwych(b) == a:
                print(f"Para zaprzyjaźniona: ({a}, {b})")

wypisz_zaprzyjaznione(1, 2000)