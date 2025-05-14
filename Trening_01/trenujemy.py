tekst = "Witaj Świecie"
print(tekst)
print(type(tekst))

print(tekst.upper())
print(tekst.lower())

print(tekst[:6] + tekst[6].lower() + tekst[7:])

name = "Jacek"
print(name)
print(len(tekst))
print(tekst[2], tekst[0:3], tekst[2:5], tekst[::2])
print(tekst[::-1])


str1 = "___HELLO***WORLD---"
print(str1)
print(str1.strip("_"))
print(str1.strip("*"))
print(str1.strip("-"))

print(str1.rstrip("-"))
print(str1.lstrip("_"))

print(10 * '_')

print(tekst)

print(tekst.removeprefix("Witaj"))
print(tekst.removesuffix("Świecie"))
print(tekst.count("i"))
print(tekst.count("i", 2, 6 ))
print(tekst.index("i"))
print(tekst.index("i", 1, 5))

print(10 * '+')

str2 = 'Hello World'

print(str2.replace("He", "HO"))
print(str2.replace(" ", ""))
print(str2.center(59))

ege = 54
print(name)
print(ege)

print(75 * '-')

print(f"Mam na imię {name}, {ege} lat i lubie Pythona.")
print(f"\tMam na imię {name},\n\t{ege} lat \n\ti lubie Pythona.\b")

print(75 * '+')

tekst_old = "Witaj %s!"
print(tekst_old % name)

print("To teraz witaj", name)
