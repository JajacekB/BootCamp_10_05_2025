from pprint import pprint


class ContactList(list['Contact']):
    """
    Lista z metodą search
    """

    def search(self, name):
        matching_contacts = []
        for c in self:
            if name.casefold() in c.name.casefold():
                matching_contacts.append(c)
        return matching_contacts



class Contact:
    all_contacts = ContactList()

    def __init__(self, name, email):
        self.name = name
        self.email = email
        Contact.all_contacts.append(self)

    def __repr__(self):
        return f"{self.name!r} {self.email!r}"


class Suplier(Contact):
    """
    Klasa Suplier
    """

    def order(self, order):
        print(f"{order} zamowiono od {self.name}")

    def __repr__(self):
        return f"{self.name}, {self.email}"


class Friend(Suplier):
    """
    Klasa dziedziczy po Suplier
    """

    def __init__(self, name, email, phone="00000000000"):
        super().__init__(name, email)
        self.phone = phone

    def __repr__(self):
        return f"{self.__class__.__name__} {self.name} {self.email} +49{self.phone}"


lista = ContactList
print(type(lista))
print(lista)

c1 = Contact("Adam", "adam@wp.pl")
c2 = Contact("Radek", "radek@wp.pl")
c3 = Contact("Tomek", "tomek@wp.pl")

print(c1.all_contacts)
print(c2.all_contacts)
print(c3.all_contacts)
print(Contact.all_contacts)

s1 = Suplier("Marek", "marek@02.pl")
print(Contact.all_contacts)
print(s1.all_contacts)

s1.order("kawa")

print(s1.all_contacts.search("Radek"))

f1 = Friend("Marcin", "marcin@o2.pl", 456873259)
print(f1)
f1.order("herbata")
print(f1.all_contacts)

pprint(f1.all_contacts)