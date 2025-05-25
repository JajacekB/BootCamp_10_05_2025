import pandas

data = pandas.read_csv('dane/records_2.csv', delimiter=";")

print(data)

print(data.columns)
print(data.values)

print(data.items)