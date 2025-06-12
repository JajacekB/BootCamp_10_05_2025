def dekorator(func):
    def wrapper():
        result = func()
        return result.upper()

    return wrapper

def bold_decorator(func):
    def wrapper():
        result = func()
        return f"\033[1m" + result + "\033[0m"

    return wrapper


@dekorator
@bold_decorator
def letters():
    letters = input("Podaj swoje imię i nazwisko ")
    return (letters)


print(letters())


@bold_decorator
@dekorator
def greetings():
    return "Hello World"


print(greetings())
