class Animal:

    def __init__(self, name):
        self.name = name

    def info(self):
        print(f"Imię; {self.name}")


class Cat(Animal):
    def __init__(self, name, color):
        super().__init__(name)
        self.color = color

    def info(self):
        super().info()
        print(f"Kolor: {self.color}")


class Tiger(Cat):
    def __init__(self, name, color, liczba_paskow):
        super().__init__(name, color)
        self.liczba_pasków = liczba_paskow

    def info(self):
        super().info()
        print(f"Liczba pasków: {self.liczba_pasków}")

animal = Animal("Bezimienny")
animal.info()

cat1 = Cat("Filemon", "szylkret")
cat1.info()

tiger =Tiger("Zenek", "Zółty", 10)
tiger.info()