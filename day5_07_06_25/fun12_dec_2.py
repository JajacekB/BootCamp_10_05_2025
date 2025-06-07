def dekorator(func):
    def wrapper():
        result = func()
        return result.upper()

    return wrapper

#  def bold_decorator(func):
#      def wrapper():
#          result = func()
#          return f"\033[1m" + "\033[om"
#  
#      return wrapper()
#  
#  @bold_decorator
@dekorator
def letters():
    letters = input("Podaj swoje imię i nazwisko ")
    return (letters)


print(letters())
