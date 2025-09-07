from numpy import random

x = random.randint(100, size=5)
print(x)

x = random.randint(100, size=(3, 5))
print(x)

x = random.rand(5)
print(x)
print(x.dtype)

x = random.rand(3, 6)
print(x)

x = random.choice([3, 5, 7, 9])
print(x)

x= random.choice([3, 5, 7, 9], size=(3, 5))
print(x)

x = random.choice([3, 5, 7, 9], 2, replace=False)
print(f"{x=}")

gen = random.default_rng()
x = gen.choice([3, 5, 7, 9], 2, replace=False)
print(x)

x = random.random_sample((5,))
print(x)

