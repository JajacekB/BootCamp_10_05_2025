if 5> 3:
    print("Five is greater than three")
if 5 > 2:
    print("Five is greater than two")

x = str(3)
y = int(3)
z = float(3)

print(f" {x=}, {y=}, {z=}")
print(f" {type(x)=}, {type(y)=}, {type(z)=}")

x = "3"
y = 3
z = 3.0

print(f" {x=}, {y=}, {z=}")
print(f" {type(x)=}, {type(y)=}, {type(z)=}")

a, b, c, = 1, 2, 3,
print(a)
print(b)
print(c)

e = f = g = "Pomelo"
print(e)
print(f)
print(g)

fruit = ["Lemon", "Orange", "Pomelo"]
e, f, g, = fruit
print(e)
print(f)
print(g)

print(" ")

k = "Python is awesome"
print(k)

l = "Python"
m = "is"
n = "awesome"
print(l)
print(m)
print(n)
print(l, m, n)
print(l + m + n)
o = "Python"
p = " is "
r = "awesome"
print((o + p + r))
print(a + b + c)

liczba = 10
name: str = "Johny"

print(liczba, name)
print(str(liczba) + name)
print(liczba + len(name))

print(111 * "+")

k = "awesome"
def myfunc():
    print("Python is " + k)

myfunc()

print(' ')

s = "awesome"

def myfunc():
    s = "fantastic"
    print("Python is " + s)

myfunc()

print("Python is " + s)

print(" ")

def myfunc():
    global s
    s = "fantastic"

myfunc()

print("Python is", s)

t = "awesome"

def myfunc():
  global t
  t = "fantastic"

myfunc()

print("Python is " + t)