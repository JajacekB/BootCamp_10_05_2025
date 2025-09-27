def decyzja_po_ifach(wiek,zarobki):
    if wiek > 30 and zarobki > 4000:
        return "Pozyczka przyznana"
    else:
        return "Pożyczka odrzucona"

def drzewo_2(wiek, zarobki):
    if wiek > 50:
        if zarobki > 60_000:
            return "OK"
        else:
            return "NO"

    else:
        if wiek > 30:
            if zarobki > 40_000:
                return "OK"
            else:
                return "NO"
        else:
            return "NO"

print(drzewo_2(30, 4_000))
print(drzewo_2(55, 7_000))
print(drzewo_2(25, 100_000))