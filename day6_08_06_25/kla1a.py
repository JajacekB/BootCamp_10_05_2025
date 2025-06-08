import math


class MyFirstClass:
    """
    Klasa w Python opisująca punkty w przestrzeni x i y
    """

    def __init__(self, x=0, y=0):
        """
        Metod inicjująca
        :param x:
        :param y:
        """
        self.x = x
        self.y = y

    def move(self, x:float, y:float) -> None:
        """

        :param x:
        :param y:
        :return:
        """
        self.x = x
        self.y = y

    def reset(self):
        self.move(0, 0)

    # math.hypot()
    def calculate(self, other:"MyFirstClass") -> float:
        """
        metoda zwraca odłegłość
        :param other:
        :return:
        """
        return math.hypot(self.x - other.x, self.y - other.y)


    def __str__(self):
        return f"({self.x, self.y})"

    def __repr__(self):
        return f"Point({self.x, self.y}) "


ob = MyFirstClass()
print(ob)
print(ob.x)
print(ob.y)

ob2 = MyFirstClass(59, 34)
print(ob2)

ob.move(23, 89)
print(ob)
print(ob2)

print(ob.calculate(ob2))
print(ob2.calculate(ob))

ob.reset()
print(ob)
print(ob2)
print(ob.calculate(ob2))


lista_ob = [ob, ob2]
print(lista_ob)