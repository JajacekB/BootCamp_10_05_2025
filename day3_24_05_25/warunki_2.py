# Od Python 3.10 istnieje match case

lista = []
lang = input("Podaj znany ci język programowania ").lower()
match lang:
    case "python":
        print("Lubie Python")
        lista.append(lang.capitalize())
    case "java":
        print("Java to kawa")
        lista.append(lang.capitalize())
    case "C++":
        print("To za trudne")
        lista.append(lang.capitalize())
    case _:  #odpowiednik else
        print("Nie znam tego języka")
print(f"Lista z opowiedziami {lista}")

dane = [1, 2, 3]
dane = {"nazwa": 'Radek', "wiek": 45}
match dane:
    case [a, b, c]:
        print(f" Lista z trzema elementami {a=}, {b=}, {c=}")
    case {'nazwa': n, "wiek": w}:
        print(f" Słownik reprezentujący osobę {n}, wiek {w}")
    case _:
        print("Błędny typ danych")

