# funkcje zagnieżdżone, funkcje wewnętrzne
# funkcja w funkcji
# wykorzystywane w dekoratorze

def fun1():
    print("To jest funkcja fun1")

    def fun2():
        print("to jest funkcja fun2")

#     fun2()
    return fun2


fun1()
print()
func = fun1()
print(func)
print(type(func))
func()

