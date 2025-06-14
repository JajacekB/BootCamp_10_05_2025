# iterator

lista = [1, 2, 3, 4, 5]
print(lista)
for i in lista:
    print(i)

# print(next(lista))

iterator = iter(lista)
print(iterator)
print(type(iterator))
# for i in iterator:
#     print(i)



print(111 * "-")
print(next(iterator))

print("Nuda")
print("Nic się nie dzieje")
for x in range(5):
    print(x, sep=" | ", end="")
print()
print(next(iterator))
print(next(iterator))
print(next(iterator))
print(next(iterator))


class Count:
    """
    Klasa będąca iteratorem
    """

    def __init__(self, low, high):
        """
        Metoda
        :param low:
        :param high:
        """
        self.current = low
        self.high = high

    def __int__(self):
        return self

    def __next__(self):
        if self.current > self.high:
            raise StopIteration
        else:
            self.current += 1
            return self.current - 1


print("----------")
counter = Count(1, 20)
print(next(counter))
print(next(counter))
print(next(counter))
print(next(counter))
print(next(counter))

print("-------")
while True:
    try:
        number = next(counter)
        print(number)
    except StopIteration:
        break

print(15 * "-")
counter2 = Count(1, 7)
print(next(counter2))
print(next(counter2))
print(next(counter2))
print(next(counter2))

counter3 = Count(5, 39)
print(next(counter3))