# zrobić funkcję restaurację
# zamów pizza, zamów napój
# w zalezności od zamówienia ma zwrócić odpowiednie funkcje
# uzyć tych funkcji  w glownym programie


print("Cześć")


def pizzeria(zamowienie):
    print("Witamy w Pizzerii 'Capone'")

    def pizza(skladniki = "margeritta"):
        print("Wybrałeś Pizza: ", skladniki)

    def napoj():
        print("wybrałeś Coca-Cola", )

    def brak():
        print("Nie mamy tego w menu")

    match zamowienie.casefold().strip():
        case "pizza":
            return pizza
        case "cola":
            return napoj
        case _:
            return brak


wydaj = pizzeria("pizza")
print(wydaj())

wydaj("pieczarki, szynka")



wydaj = pizzeria("cola")
print(wydaj())

wydaj = pizzeria(zamowienie="schabowy")
print(wydaj())
order = input("Co mamy podać ")
wydaj = pizzeria(order)

