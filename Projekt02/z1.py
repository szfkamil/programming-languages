import math

def czy_pierwsza(n: int) -> bool:
    """
    Weryfikuje, czy podana liczba całkowita n jest liczbą pierwszą.
    Zwraca True, jeśli jest pierwsza, w przeciwnym razie False.
    """
    if n <= 1:
        return False
    
    # Sprawdzamy dzielniki tylko do pierwiastka z n.
    limit = math.isqrt(n) # zwraca cz. całkowitą z pierwiastka kwadratowego
    
    # Zaczynamy sprawdzanie od najmniejszej liczby pierwszej, czyli 2.
    for i in range(2, limit + 1): # (start, stop, step) 
        if n % i == 0:
            return False
            
    return True

def wypisz_pierwsze_w_zakresie(poczatek: int, koniec: int) -> None:
    """
    Iteruje przez domknięty przedział [poczatek, koniec] i wypisuje liczby pierwsze.
    """
    for liczba in range(poczatek, koniec + 1): # range jest prawostronnie otwarte, dlatego koniec + 1
        if czy_pierwsza(liczba):
            print(liczba, end=" ")
    print()

wypisz_pierwsze_w_zakresie(1, 50)