# dziedziczenie diamentowe
class A:
    def method(self):
        print("Metoda z klasy A")


class B(A):
    def method(self):
        print("Methoda z klasy B")


class C(A):
    def method(self):
        print("Methoda z klasy C")


class D(B, C):
    """
    Klasa dziedziczy
    """


d =D()
d.method()

print(D.__mro__)


# class E(A, D):
#     pass

class F(D, A):
    pass


print(F.__mro__)