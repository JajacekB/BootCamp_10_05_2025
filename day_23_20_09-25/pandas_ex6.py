import pandas as pd

df = pd.read_csv("data.csv")
print(df.info())

df.fillna(130, inplace=True)
print(df.info())

print(df.loc[141])

df = pd.read_csv("data.csv")
df.fillna({"Calories":130}, inplace=True)
print(df.info())

print(df.loc[141])

df = pd.read_csv('data.csv')
df["Calories"] = df['Calories'].fillna(130)
df.info()
print(df.loc[141])

# df['Calories'].fillna(130, inplace=True)
df.info()
print(df.loc[141])

df = pd.read_csv('data.csv')

x = df['Calories'].mean()
print("Średnia wynosi: ", x)

df['Calories'] = df["Calories"].fillna(x)
print(df.loc[141])
x = df['Calories'].mean()
print("Średnia wynosi: ", x)

data = {"Wiek": [25, 30, 35, 40, 45, 50, 55, 60, 65]}

df = pd.DataFrame(data)
mediana_wiek = df["Wiek"].median()
print("Mediana wieku: ", mediana_wiek)

df = pd.read_csv('data.csv')
mediana_cal = df["Calories"].median()
df['Calories'] = df["Calories"].fillna(mediana_cal)
print("Mediana cal: ", mediana_cal)
print(df.loc[141])
print(111 * "#")
print()


df = pd.read_csv('data.csv')
mode_data = df["Calories"].mode()
print("Najczęstsza wartość: ", mode_data)
df['Calories'] = df["Calories"].fillna(mode_data[0])
print(df.loc[141])


print(111 * "#")
print()

df = pd.read_csv('data.csv')
print(df[df.isna().any(axis=1)])

print(111 * "#")
print()

print(df[df["Calories"].isna()])


