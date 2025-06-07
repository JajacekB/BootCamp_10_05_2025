# decorator


def dekorator(func):
    def wew():
        print("Dekoruj")
        return func()

    return wew


@dekorator
def hej():
    print("Hey!!!")


hej()