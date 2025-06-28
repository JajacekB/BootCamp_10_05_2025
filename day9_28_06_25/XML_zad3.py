from xml.dom import minidom

DOMTree = minidom.parse("dane.xml")

print(DOMTree.toxml())


cNodes = DOMTree.childNodes
print(cNodes)

znajomi = cNodes[0]
print("Znajomi: ", znajomi)

print(znajomi.getElementsByTagName("osoba"))

person = znajomi.getElementsByTagName("osoba")
print(person[0].toxml())


print(person[1].toxml())


osoba = person[0]
imie = osoba.getElementsByTagName("imie")[0]
print(imie)
imie1 = imie.firstChild.data
print(imie1)
atrybut = imie.getAttribute("foo")
print(atrybut)


