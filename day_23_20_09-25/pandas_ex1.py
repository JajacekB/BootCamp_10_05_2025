import pandas as pd

# print(pd.__version__)

name_dict = {"name": ["Radek", "Tomek"]}

a = [1, 2, 3]
myvar = pd.Series(a)
print(myvar)

print(myvar[0])

myvar = pd.Series(a, index=["x","y","z"])
print(myvar)

print(myvar["y"])

calories = {'day1':420, "day2": 320, "day3": 390}
myvar = pd.Series(calories)
print(myvar)

myvar = pd.Series(calories, index=["day1", "day2"])
print(myvar)

data = {
    "calories":[420, 380, 390],
    "duration": [50, 40, 45]
}

df = pd.DataFrame(data)
print(df)

print(df.loc[0])

print(type(df.loc[0]))

print(df.loc[[0,1]])
print(type(df.loc[[0,1]]))

df = pd.DataFrame(
    {
        "Name":[
            "Tomek",
            "Radek",
            "Zenek",
            "Anna"
        ],
        "Age": [22, 45, 35, 29],
        "Sex": ["male", "male", "other", "female"]
    }
)

print(df)

print(df['Age'])

print(df['Age'].max())

print(df.describe())

print(df.loc[0])

