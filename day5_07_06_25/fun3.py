# zasięg zmiennych

a = 10
b = 10

def dodaj():
    a = 6
    b = 8
    print(a + b)


def dodaj2():
    print(a + b)


def dodaj3():
    global a
    a = 5
    b = 67
    print(a + b)



print(f"Zmienna a i b z góry {a=}, {b=}")
dodaj()
print(f"Zmienna a i b z góry {a=}, {b=}")
dodaj2()
print(f"Zmienna a i b z góry {a=}, {b=}")
dodaj3()
print(f"Zmienna a i b z góry {a=}, {b=}")
dodaj2()

print()

