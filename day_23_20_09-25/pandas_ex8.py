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


print(111 * '+')
df = pd.DataFrame({'Miasto': ['Warszawa', 'Kraków', "Łódź", "Warszawa", "Gliwice"]})
print(df)

# df["Miasto"].replace("Warszawa", "Warszawa-Stolica", inplace=True)
df['Miasto'] = df['Miasto'].replace("Warszawa", "Warszawa-Stolica")
print(df.to_string())

df = pd.DataFrame({'Miasto': ['Warszawa', 'Kraków', "Łódź", "Warszawa", "Gliwice"]})
df['Miasto'] = df['Miasto'].replace({"Warszawa": "Warszawa-Stolica", "Kraków": "Kraków-Zamkowy"})
print(df)

df = pd.DataFrame({'Wiek': [18, 25, 30, 15, 40]})
print(df)

df["Kategoria"] = "Dorosły"
print(df)

df.loc[df["Wiek"] < 18, "Kategoria"] = "Niepełnoletni"
print(df)

df = pd.DataFrame({'Miasto': ['Warszawa', 'Kraków', "Łódź", "Warszawa", "Gliwice"]})
# df["Miasto"] = df["Miasto"].replace("Łódź", "Łódź Przemysłowa", regex=True)
df["Miasto"] = df["Miasto"].replace(r"^Ł", "Łódź Przemysłowa", regex=True)
print(df.to_string())
df["Miasto"] = df["Miasto"].replace(r"^Ł.*", "Łódź Przemysłowa", regex=True)
print(df.to_string())

df = pd.DataFrame({'Wiek': [18, 25, 30, 15, 40, 70]})
df["Kategoria"] = df["Wiek"].apply(lambda x: "Senior" if x > 60 else "Dorosły")
print(df)

def zmien(x):
    if x > 60:
        return "Senior"
    else:
        return "Dorosły"

df = pd.DataFrame({'Wiek': [18, 25, 30, 15, 40, 70]})
df["Kategoria"] = df["Wiek"].apply(zmien)
print(df)

df = pd.DataFrame({'Miasto': ['Warszawa123', 'Kraków456', "Łódź", "Warszawa789", "Gliwice"]})
df["Miasto"] = df["Miasto"].replace(r"\d+", "", regex=True)
print(df)

