def bezpieczna_pozycja_flawiusza(n: int) -> int:
    """
    Wyznacza bezpieczną pozycję w kręgu dla problemu Józefa Flawiusza.
    Zakłada stały krok eliminacji równy 2 (eliminacja osoby bezpośrednio po lewej).
    """
    if n < 1:
        raise ValueError("Liczba osób w kręgu musi być dodatnia.")
        
    pozycja = 0 
    
    for i in range(2, n + 1):
        pozycja = (pozycja + 2) % i # Jaki indeks posiada ocalały w kręgu o obecnym rozmiarze i?
    
        
    return pozycja + 1

print(bezpieczna_pozycja_flawiusza(22))