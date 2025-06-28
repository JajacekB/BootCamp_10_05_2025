import xml.etree.ElementTree as ET

def GenerateXML(filename):
    root = ET.Element("Catalog")

    m1 = ET.Element('mobile')
    root.append(m1)


    b1.text = "Redmi"

    c1 = ET.SubElement(m1, 'price')
    c1.text = "6999"

    m2 = ET.SubElement('mobile')
    root.append(m2)

    d1 = ET.SubElement(m3)

    b2.text = "Samsung"

    c2 = ET.SubElement(m2, "brand")
    c2.txt = "9999"

    tree = ET.ElementTree(root)

    with open(filename, "wb") as file:
        tree.werite(file, xml.decLaratiom=True)
