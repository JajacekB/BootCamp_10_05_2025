class DefoultDict(dict):
    def __missing__(self, key):
        return "default"


d_python = {}
print(type(d_python))
print(d_python)
d_python['name'] = "Radek"
print(d_python['name'])

d1 = DefoultDict()
print(d1["name"])

class ZeroDefaultDict(dict):
    def __missing__(self, key):
        self[key] = 0
        return 0


d2 = ZeroDefaultDict()
print(d2)
print(d2["name"])
print(d2)
print(d2['name'])
d2['name'] = "Radek"
print(d2)

class CaseInsensitiveDict(dict):
    def __missing__(self, key):
        if isinstance(key, str):
            return self.get(key.casefold())
        return None

d3 = CaseInsensitiveDict()
d3['name'] = "Radek"
print(d3['NAme'])
d3[1] = "Radek"
print(d3)
print(d3[2])
