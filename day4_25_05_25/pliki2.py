

with open("linie.txt", "r+") as f:
    lines = f.readlines()
    f.seek(0)
    f.write("Nowa \n")
    f.writelines(lines[1:])
    f.truncate()
print(lines)

with open("plik.txt", "w+") as f:
    f.write("Nowa linia\n")
    f.seek(0)
    print(f.read())

