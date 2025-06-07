def sub_decorator(func):
    def wrapper(num1, num2):
        if num1 < num2:
            num1, num2 = num2, num1
        return func(num1, num2)

    return wrapper

@sub_decorator
def subsract(num1, num2):
    res = num1 - num2
    print("result is: ", res)


subsract(2, 4)
subsract(6, 3)
subsract(3, 6)
a, b = 1, 2
a, b = b, a
print(f"{a=}, {b=}")
