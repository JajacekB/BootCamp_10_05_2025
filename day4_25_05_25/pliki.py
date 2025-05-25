# praca z plikami

fh = open("tekst_fh.txt", "w")
fh.write("Radek\n")
fh.close()

# context manager - pozwala na bezpieczną pracę z plikiem
# with

with open("test.log", "w", encoding="utf-8") as file:
    file.write("Radek\n")
    file.write("Kolejna\n")
    file.write("Jeszcze jedna\n")
    file.write("Jeszcze jedna\n")
    file.write("Jeszcze jedna\n")
    file.write("Jeszcze jedna\n")
    file.write("Jeśće jedna\n")
#file.write("")

with open("../test.log", "w") as fh:
    fh.write("Plik w innym miejscu")

with open("../test.log", "w") as fh:
    fh.write("Nadpisanie")

# with open("../test.log", "x") as fh:
#     fh.write("Nadpisanie")

# with open("../test2.log", "x") as fh:
    fh.write("Pisanie\n")

# with open("test.log", "a", encoding="utf-8") as file:
#     fh.write("Dopisanie\n")
#     fh.write("Dopisanie\n")
#     fh.write("Dopisanie\n")
#     fh.write("Dopisanie\n")
#     fh.write("Dopisanie\n")
#     fh.write("Dśopisanie\n")

with open("test_log", "r", encoding="utf-8") as f:
    lines = f.read()

print(lines)

with open("linie.txt", "w") as f:
    f.write("pierwsza linia\n")
    f.write("Druga linia\n")
    f.write("Trzecia linia\n")

# with open("linie.txt", "r") as f:
#     tekst = fh.read()
# print(tekst)
# print(repr(tekst))

with open("linie.txt", "r") as fh:
    linie = fh.readlines()

print(linie)
print(111 * "-")
print(repr(linie))

with open("linie.txt", "r") as f:
    pierwsza_linia = f.readline()
print(pierwsza_linia)

with open("linie.txt", "r") as file:
    for linia in file:
        print(linia.strip())

