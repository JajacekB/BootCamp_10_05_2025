from mypyc.ir.ops import PrimitiveOp

tekst = "Witaj Świecie"
print(tekst)
print(type(tekst))

tekst.upper()
print(tekst)
print(tekst.upper())
print(tekst)
tekst_upper = tekst.upper()
print(tekst_upper)

tekst_lower = tekst.lower()
print(tekst_lower)

name = "Jacek"

print(name[0])
print(name[1])
print(name[2])
print(name[3])
print(name[4])

print(len(name))

print(name[2:4])
print(name[:4])
print(name[:])

my_str = "  Hello Everyone  "

print(my_str)
print(my_str.strip())
print(my_str.rstrip())
print(my_str.lstrip())

my_str2 = "***Hello***World***"
print(my_str2)
print(my_str2.strip("*"))
print(my_str2.rstrip("*"))
print(my_str2.lstrip("*"))

print(tekst)

print(tekst.removeprefix("Witaj"))
print(tekst.removesuffix("Świecie"))

print(tekst.count("i"))
print(tekst.count("i", 0, 4))
print(tekst.count("j", 0, 4))
print(tekst.index("j"))

print(my_str2)

print(my_str2.replace("HE", 'Ho'))

print(my_str)

print(my_str.replace(" ", ""))
print(my_str.center(40))

print("Mój ulubiony serial \"Alternatywy 4\"")
print('Mój ulubiny serial "Alternatywy4"')

imie = "Jacek"
formatted_tex = f"Mam na imię {imie} i libie Pythona."
print(formatted_tex)

formatted_tex2 = f"\tMam na imię {imie}\n i lubię Pythona.\b"
print(formatted_tex2)

starszy = "Witaj %s!"
print(starszy % name)

print("""Tekst
    wielolinijkowy""")

"""Komentarz
    wielolinijkowy"""