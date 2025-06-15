from multipledispatch import dispatch

class Printer:

    @dispatch(str)
    def show(self, txt):
        print("Text:", txt)

    @dispatch(int)
    def show(self, number):
        print("Liczba:", number)

    @dispatch(list)
    def show(self, arr):
        print("Lista:", arr)


p = Printer()
p.show("HELLO")
p.show(123)
p.show([1, 2, 3, 4, 5])
