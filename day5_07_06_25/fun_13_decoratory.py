def sub_decorator(func):
    def wrapper(num1, num2):
        if num1 < num2:
            num1, num2 = num2, num1
        return func(num1, num2)

    return wrapper


@sub_decorator
def substract(num1, num2):
    res = num1 - num2
    print("Result is:", res)


substract(2, 4)  # Result is: 2
substract(6, 3)  # Result is: 3
substract(3, 6)  # Result is: 3
a, b = 1, 2
a, b = b, a
print(f"{a=}, {b=}")