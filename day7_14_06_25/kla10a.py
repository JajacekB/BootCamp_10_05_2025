from abc import ABC, abstractmethod


class Counter(ABC):
    def __init__(self, values=0):
        self.values = values

    def increment(self, by=1):
        self.values += by

    @abstractmethod
    def drukuj(self):
        pass

    @classmethod
    def from_counter(cls, counter):
        # Counter(bc.values)
        return cls(counter.values)

    @staticmethod
    def from_string():
        print("Metoda statyczna")

class NewCounter(Counter):
    """
    Licznik bez metody drukuj
    """


# nc = NewCounter()


class BoundedCounter(Counter):
    """
    Klasa musi nadpisać metodę drukuj()
    """

    MAX = 100

    def __init__(self, values=0):
        if values > self.MAX:
            raise ValueError(f"Wartość nie może byc większa od {self.MAX}")
        super().__init__(values)

    def drukuj(self):
        print("Drukuj...", self.values)


bc = BoundedCounter()
bc.drukuj()
bc.increment()
bc.drukuj()
bc.increment(5)
bc.drukuj()

# bc2 = BoundedCounter(101)

bc2 = BoundedCounter(bc.values)
bc2.drukuj()

bc3 = BoundedCounter.from_counter(bc)
bc3.drukuj()

bc4 = bc2.from_counter(bc3)
bc4.drukuj()

Counter.from_string()
print(Counter)