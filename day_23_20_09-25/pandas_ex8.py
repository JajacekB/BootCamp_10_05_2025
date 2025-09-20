import pandas as pd

data = pd.read_csv('data_with_date.csv')
print(data)

data.loc[7, "Duration"] = 45

print(data.loc[7])

data = pd.read_csv('data_with_date.csv')
for x in data.index:
    if data.loc[x, "Duration"] > 120:
        data.loc[x, "Duration"] = 120

print(data)

data = pd.read_csv('data_with_date.csv')

for x in data.index:
    if data.loc[x, "Duration"] > 120:
        data.drop(x, inplace=True)

print(data)

data = pd.read_csv('data_with_date.csv')
data['Duration'] = data["Duration"].clip(upper=120)
print(111 * '#')
print("Clop", data)

data = pd.read_csv('data_with_date.csv')
data['Duration'] = data["Duration"].where(data["Duration"] <= 120, 120)
print(111 * '#')
print("where:", data)

data = pd.read_csv('data_with_date.csv')
data["Duration"] = data["Duration"].mask(data["Duration"] > 120, 120)

data = pd.read_csv('data_with_date.csv')
data = data[data["Duration"] <= 120]
print(data)

data = pd.read_csv('data_with_date.csv')
data = data.query("Duration <= 120")
print(111 * '@')
print(data)


