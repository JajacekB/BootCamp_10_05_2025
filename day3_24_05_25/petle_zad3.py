# while -  sterowana warunkiem

# pętla nieskończona
# while True:
#     print("Komunikat !!!")

licznik = 0
while True:
    print("Komunikat 1 !!")
    licznik += 1
    if licznik  > 15:
        break

print()

licznik = 0
while licznik < 15:
    licznik += 1
    print("Komunikat 2 !!!!")

# password = input("Podaj hasło")
# while password != "Secret":
#     password = input("Błędne hasło, podaj poprawne")
#     print('Hasło poprawne')

# lista = []
# lista_int = []
# while True:
#     wej = input("Podaj liczbę")
#     if not wej.isnumeric():
#         break
#     lista.append(wej)
#     lista_int.append(int(wej))
#
# print(lista)
# print(lista_int)

my_list = [1, 5, 2, 3, 5, 4, 5, 6, 5]
element_to_remove = 5
while element_to_remove in my_list:
    my_list.remove(element_to_remove)

print(my_list)

print(10 * '/')

my_list = [1, 7, 2, 3, 7, 4, 7, 5, 6, 7]
print(my_list)
my_list = [usunac for usunac in my_list if usunac !=7]
print(my_list)




