x = 1
y = 2.8
z = 3j

print(type(x))
print(type(y))
print(type(z))

print(" ")

x = 1
y = 357924680
z = -35369075

print(type(x))
print(type(y))
print(type(z))

print(" ")

x = 1.10
y = 1.0
z = - 35.59

print(type(x))
print(type(y))
print(type(z))

print(" ")

x = 35e3
y = 12E4
z = -87.7e100

print(x, type(x))
print(y, type(y))
print(z, type(z))

print(" ")

x = 3+5j
y = 5j
z = -5j

print(x, type(x))
print(y, type(y))
print(z, type(z))

print(" ")

x = 1
y = 2.8
z = 3+5j

a = float(x)
b = int(y)
c = complex(x)

print(a, type(a))
print(b, type(b))
print(c, type(c))

print(" ")

import random

d = random.randrange(1, 10)
print(d, type(d))

print(" ")

x = int(1)
y = int(2.8)
z = int("5")

print(x, type(x))
print(y, type(y))
print(z, type(z))

print(" ")

x = float(1)
y = float(2.8)
z = float("5")
w = float("-7.9")

print(x, type(x))
print(y, type(y))
print(z, type(z))
print(w, type(w))

print(" ")

x = str("world")
y = str(59)
z = str(-4.8)
w = str(7+3j)

print(x, type(x))
print(y, type(y))
print(z, type(z))
print(w, type(w))

print(" ")

print('hello')
print("hello")

print(" ")

print("It's alright")
print("He is called 'Johny'")
print('He is called "Johny"')

print(" ")

a = "Helo"
print(a)

print("")

a = """Lorem ipsum dolor sit amet,
consectetur adipiscing elit,
sed do eiusmod tempor incididunt
ut labore et dolore magna aliqua."""

print(a)

b = '''Lorem ipsum dolor sit amet,
consectetur adipiscing elit,
sed do eiusmod tempor incididunt
ut labore et dolore magna aliqua.'''

print(b)

print("")

a = "Hello World"
print(a[1])
print(a[6])

print(" ")

for x in "banana":
    print(x)

print(" ")

a = "Hello World"
print(len(a))

txt = "The best things in life are free!"
print("free" in txt)

if "free" in txt:
    print("Yes, 'free' is present")

print("expensive" not in txt)

if "expensive" not in txt:
    print("No, 'expensive is NOT present")

print("-")

b = "Hello, World!"
print(b[2:5])
print(b[:5])
print(b[2:])
print(b[-5:-2])
print(b[2:10:2])
print(b[-1:-9:-2])

print(" ")

a = "Hello, World!"
print(a.upper())
print(a.lower())
a = "   Hello, World!   "
print(a)
print(a.strip())
print(a.replace("H", "Y"))
print(a.split(","))

print(100 * "+")
print(" ")

a = "Hello"
b = "World"
c = a + b
print(c)
c = a + " " +b
print(c)

print(" ")

age = 54
print("My name is Jacek and I am ", age)
txt = "My name is Jacek, I am " + str(age)
print(txt)

print(" ")
txt = f"My name is Jacek and I am {age}"
print(txt)
print(f"My name is Jacek, I am {age}")

price = 135
txt = f"The price is {price:.2f} dollars"
print(txt)
print(f"The price of shoes is {price:.2f} dollars")

txt = f"The price is {20 * price} dollars"
print(txt)

txt = "We are the so-called \"Vikings\" from the North!"
print(txt)
print(type(txt))
