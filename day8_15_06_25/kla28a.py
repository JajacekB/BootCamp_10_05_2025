class Person:
    def __init__(self, name):
        self.__name = name

    @property
    def name(self):
        """ Getter - umożliwia czytanie .name"""
        print("Pobieram imię")
        return self.__name

    @name.setter
    def name(self, value):
        """Setter - ustawia .name"""
        if not isinstance(value, str):
            raise ValueError("To musi byćstring")
        print("Ustawiam imię")
        self.__name = value

    @name.deleter
    def name(self):
        """Deleter - kasowanie atrybutu"""
        print("Usuwam imię")
        del self.__name


p = Person("Alicja")
print(p.name)

p.name = "Janek"
print(p.name)

# p.name = 123
# print(p.name)

del p.name
# print(p.name)