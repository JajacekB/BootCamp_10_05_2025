print(10 > 9)
print(10 == 9)
print(10 < 9)

a = 200
b = 33

if b > a:
    print("b is greater than a")
else:
    print("b is not greater than a")

print(bool("Hello"))
print(bool(15))

x = "Hello"
y = 15
print(bool(x))
print(bool(y))

print(bool("abc"))
print(bool(123))
print(bool(["aplle", "cherry", "banana"]))

print(bool(False))
print(bool(None))
print(bool(0))
print(bool(""))
print(bool(()))
print(bool([]))
print(bool({}))

print(" ")

class myclass():
    def __len__(self):
        return 0

myobj = myclass()
print(bool(myobj))

print(" ")

def myFunction():
    return True

print(myFunction())

print(" ")

def myFunction2():
    return True

if myFunction2():
    print("YES")
else:
    print("NO")

print(" ")

x = 200
print(isinstance(x, int))
print(isinstance(x, float))
print(isinstance(x, str))

print(" ")

thislist = ["apple", "banana", "cherry", "orange", "kiwi", "mango"]
print(thislist)
thislist[1:3] = ["blackcurrant", "watermelon"]
print(thislist)

print("")

thislist = ["apple", "banana", "cherry"]
print(thislist)
thislist[1:2] = ["blackcurrant", "watermelon"]
print(thislist)

print(" ")

thislist = ["apple", "banana", "cherry"]
print(thislist)
thislist[1:3] = ["watermelon"]
print(thislist)

print("")

thislist = ["apple", "banana", "cherry"]
print(thislist)
thislist.insert(2, "watermelon")
print(thislist)

print("")

thislist = ["apple", "banana", "cherry"]
print(thislist)
thislist.insert(1, "orange")
print(thislist)

print("")

thislist = ["apple", "banana", "cherry"]
print(thislist)
tropical = ["mango", "pineapple", "papaya"]
print(tropical)
thislist.extend(tropical)
print(thislist)

print("")

