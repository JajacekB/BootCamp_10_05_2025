from xml.dom import minidom

root = minidom.Document()

xml = root.createElement('root')
root.appendChild(xml)

productChild = root.createElement('product')
productChild.setAttribute('name', 'Python to Python')
xml.appendChild(productChild)

print(root)

xmlStr = root.toprettyxml()
print(type(xmlStr))
print(xmlStr)

savePath = "ptp.xml"
with open(savePath, "w") as f:
    f.write(xmlStr)
