lista = []
print(lista)
print(type(lista))
print(bool(lista))

pusta_lista = list()
print(pusta_lista)
print(type(pusta_lista))
print(bool(pusta_lista))

lista_2 = [10, 20, 30]
print(lista_2)
print(type(lista_2))

lista_3 = [10.77, 30.66, 67, 15]
print(lista_3)
print(type(lista_3))

lista_mieszana = [10, 5.2, "Oko", "Radek"]
print(lista_mieszana)
print(type(lista_mieszana))
print(len(lista_mieszana))

print(10 * "-")

lista.append("Radek")
lista.append("Maciek")
lista.append("Tomek")
lista.append("Zenek")
lista.append("Marta")
lista.append("Ania")
print(lista)
print(type(lista))
print(len(lista))

print(10 * " ")

print(lista[1])
print(lista[3])
print(lista[5])

print(" ")

print(lista[len(lista) -1])
print(lista[-1])
print(lista[-2])
print(lista[-3])
print(lista[-4])
print(lista[-5])
print(lista[-6])

print(10 * "_")

print(lista[0:4])
print(lista[:4])
print(lista[1:3])
print(lista[:2])
print(lista[-3:])
print(lista[-2:])
print(lista[-1:])
print(lista[-1:][0])
print(lista[-4:-2][1])
print(lista[-1][0])
print(lista[:])
print(lista[2:5])
print(lista[2:])

print(10 * "+")

print(lista[-3:0])
print(lista[0:-3])
print(lista[0:3])

print(lista[2:2])
print(lista[2:3])
print(lista[4:12])
print(lista[7:12])

print(10 *" ")

lista.insert(1, "Karolina")
print(lista)
print(len(lista))

print(10 *" ")

print(lista.pop(0))
print(lista)

ind = lista.index("Zenek")
print("Numer idneksu Zenka to", ind)
print(lista.pop(ind))
print(lista)
lista.insert(3, "Zenek")
lista.append("Zenek")
print(lista)
print("Numer idneksu Zenka to", ind)
print(lista.pop(ind))
print(lista)
ind = lista.index("Zenek")
print("Numer idneksu Zenka to", ind)
print(lista.pop())
print(lista)
lista.append("Zenek")
print(lista)

print(10 * "-")

lista.append("Maciek")
print(lista)
lista.remove("Maciek")
print(lista)

print("Marta" in lista)
print("Marcin" in lista)

print(lista.remove("Marta"))
print(lista)

lista.append("Marta")
lista.append("Marta")
lista.append("Marcin")

print(lista)
print(lista.index("Marta"))

print(100 * "=")

a = 1
b = 3
print(f"{a=}, {b=}")
a = b
print(f"{a=}, {b=}")
b = 7
print(f"{a=}, {b=}")

lista4 = lista
print(f"{lista}")
print(f"{lista4}")

lista_copy = lista.copy()

print(10 * " ")

lista.clear()

print(lista)
print(lista4)
print(lista_copy)

print(f"adres: {id(lista)}")
print(f"adres: {id(lista4)}")
print(f"adres: {id(lista_copy)}")

print(10 * "-")

liczby = [45, 999, 34, 22, 13.34, 687]
print(liczby)
print(type(liczby))

liczby.sort()
print(liczby)

liczby_a = [45, 999, 34, 22, 13.34, 687, "A"]
print(liczby_a)
print(type(liczby_a))

# liczby_a.sort()

lista_osoby = ['Radek', 'Tomek', 'Zenek', 'Ania', 'Karolina', 'Magda']
print(lista_osoby)
print(type(lista_osoby))
print(sorted(lista_osoby))
print(lista_osoby)
lista_osoby.sort()
print(lista_osoby)

print(10 * '+')

lista_alfabet = ['a', 'z', 'p', 'd']
print(lista_alfabet)
lista_alfabet.sort()
print(lista_alfabet)

lista_alfabet_pol = ['a', 'z', 'ą', 'p','ń', 'd']
print(lista_alfabet_pol)
lista_alfabet_pol.sort()
print(lista_alfabet_pol)

print(' ')

print(liczby)
liczby.sort(reverse=True)
print(liczby)

print(liczby[::-1])
print(liczby)
print(liczby[0:4:2])
print(liczby[-3:0:-1])

print(" ")

liczby_3 = [ 3, 8, 5, 12, 1]
print(liczby_3)
liczby_3.reverse()
print(liczby_3)

print(lista_osoby)
lista_osoby.reverse()
print(lista_osoby)

print(111 *'=')

print(liczby)
liczby[3] = 666
print(liczby)
print(liczby [5])
print(liczby [-1])
print(liczby [1:4])
print(liczby [-5:-2])
print(liczby.pop(1))
print(liczby)
liczby.remove(22)
print(liczby)
print(liczby [::-1])

print(10 * '-')
