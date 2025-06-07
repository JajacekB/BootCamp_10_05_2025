# zrobić funkcję restaurację
# zamów pizza, zamów napój
# w zalezności od zamówienia ma zwrócić odpowiednie funkcje
# uzyć tych funkcji  w glownym programie


print("Cześć")


def pizzeria(zamowienie):
    def pizza():
        print("Wybrałeś Pizza Capricoza")

    def napoj():
        print("wybrałeś Coca-Cola")

    def brak():
        print("Nie mamy tego w menu")

    match zamowienie:
        case "pizza":
            return pizza
        case "cola":
            return napoj
        case _:
            return brak


wydaj = pizzeria(zamowienie="pizza")
print(wydaj())

wydaj = pizzeria(zamowienie="cola")
print(wydaj())

wydaj = pizzeria(zamowienie="schabowy")
print(wydaj())

order = input("Co mamy podać ").lower()
wydaj = pizzeria(order)
print(wydaj())
