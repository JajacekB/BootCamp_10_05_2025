# dziedziczenie po wielu klasch

class A:
    def method(self):
        print("Metoda z klasy A")


class B:
    def method(self):
        print("Metoda z klasy B")


a = A()
a.method()

b = B()
b.method()


class C(B,A):
    """
    Klasa C dziedziczy po
    """


c = C()
c.method()

print(C.__mro__)


class D(A,B):
    """
    Klasa Dziedziczy po Ai B
    """


d = D()
d.method()

print(D.__mro__)


class E(A,B):
    def method(self):
        print("Metoda z klasy E")


e = E()
e.method()

class F(B,A):
    """
    Klasa dziedziczy po klasie A i B
    """

    def method(self):
        A.method(self)


f = F()
f.method()


class G(A,B):
    """
    Dziedziczenie po A i B
    """

    def method(self):
        super().method()
        print("Dopisanie")


g= G()
g.method()


class H(A, B):

    def method(self):
        B.method(self)
        super().method()
        print("Dopisanie w klasie H")


h= H()
h.method()

print(H.__mro__)